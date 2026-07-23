#!/usr/bin/env python3
"""
auto_review.py — agentic first-pass review of pending KB drafts.

Workflow
--------
For each pending draft:
  1. Run deterministic safety checks.
  2. Optionally run an LLM second-opinion review.
  3. Compute a verdict: auto_approve | defer_to_human | auto_reject.
  4. Write a sidecar audit report under `auto_review_log/`.
  5. If auto_approve, shell out to `promote.py --approve` and tag the
     `extraction_log.md` line as `AUTO-APPROVED` (distinct from human
     `APPROVED`).

Design
------
- Hard checks (cannot be overridden, even by LLM):
    * schema validation
    * non-empty `contradictions:` on any finding
    * PDF quote-match below threshold (likely fabricated quotes)
    * `provenance.confidence: low`
- Soft checks (an LLM second-opinion CAN override these):
    * `provenance.confidence: medium` on any finding
    * suspicious words in `provenance.flags` (placeholder, verify, todo,
      uncertain, ambiguous, etc.)
    * `strength: weak` or null on any finding
    * sample.n disagrees across findings citing the same paper

Defaults aim conservative — better to defer a fine draft than to
auto-approve a bad one. Tighten with `--require-pdf-match` once your
papers/ dir is populated.

Usage (CLI)
-----------
    # First pass: deterministic only, all pending drafts, auto-promote winners
    python auto_review.py --all

    # Second pass: re-review only those drafts that deferred to human,
    # this time WITH the LLM second opinion
    python auto_review.py --deferred --llm-review

    # One specific draft (debug)
    python auto_review.py --draft drafts/impairments/foo.md

    # Dry run: compute verdicts but DON'T promote or write logs
    python auto_review.py --all --dry-run

    # Tighten: require PDF quote-match (fails closed if PDFs missing)
    python auto_review.py --all --require-pdf-match

    # Two-machine workflow when PDFs aren't on the review machine:
    #
    #   On the no-PDF machine — LLM-augmented review, mark as provisional:
    #     python auto_review.py --all --llm-review --provisional-without-pdf
    #
    #   On the machine with papers/ — finalise the provisional verdicts:
    #     python auto_review.py --pending-pdf
    #
    # On the second pass:
    #   * Drafts whose quotes match the PDF → promoted
    #   * Drafts whose quotes don't match    → auto_reject (LLM was fooled)
    #   * Drafts where PDFs are STILL missing → defer (loud failure)

    # Cowork / human-reviewer workflow (nothing runs locally; a human or
    # a Cowork session supplies the verdicts):
    #
    #   1. Generate a worksheet listing the drafts you want reviewed:
    #        python auto_review.py --deferred --emit-worksheet worksheet.yaml
    #      (or --all, --pending-pdf, --draft <path>)
    #
    #   2. Open worksheet.yaml. For each draft, fill in:
    #        verdict:   approve | agree_defer | reject
    #        rationale: one to three sentences
    #      You can do this manually, or open a new Cowork session
    #      (ideally with a different model line from the extractor —
    #      e.g. extractor=Opus, reviewer=Sonnet) and ask it to fill in
    #      the worksheet for you.
    #
    #   3. Apply the verdicts:
    #        python auto_review.py --apply-verdicts worksheet.yaml \
    #                               --reviewer cowork-claude-sonnet
    #      Sidecar runs are tagged mode=manual_review with the reviewer
    #      name, and approves are auto-promoted.

Usage (module)
--------------
    from auto_review import review_one, review_many, Verdict
    verdict, checks, llm = review_one(Path("drafts/.../foo.md"),
                                       llm_review=False)
    if verdict == Verdict.APPROVE:
        ...
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

# Load .env file if present (python-dotenv optional dependency)
try:
    from dotenv import load_dotenv as _load_dotenv
    _load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=False)
    _load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env", override=False)
except ImportError:
    pass

# ============================================================
# Paths and constants
# ============================================================
ROOT = Path(__file__).resolve().parent
DRAFTS_DIR = ROOT / "drafts"
PAPERS_DIR = ROOT / "papers"
REPORTS_DIR = ROOT / "auto_review_log"
PROMOTE_PY = ROOT / "promote.py"
LOG_PATH = ROOT / "extraction_log.md"

# Which model reviews drafts lives in models.yaml — see model_config.py.
from model_config import resolve as resolve_model  # noqa: E402

_REVIEW_CFG = resolve_model("review")
DEFAULT_LLM_MODEL = _REVIEW_CFG["model"]
PDF_MATCH_THRESHOLD = 0.80   # >= this fraction of quotes must match

# --- Local-model guardrails -------------------------------------------
# The LLM second opinion can PROMOTE a draft into the canonical KB. That
# makes a wrong `override_approve` the most costly error this script can
# make, and a mid-size local model is more likely to make it than a
# frontier model — small models are agreeable, and this prompt actively
# invites them to bless something a deterministic check already flagged.
#
# So local review is asymmetric by default:
#   * escalate_reject / agree_defer  → honoured (both fail SAFE)
#   * override_approve               → downgraded to agree_defer,
#                                      unless --allow-local-override
# Enabling the override flag is reasonable once you've spot-checked the
# model's rationales on a batch you already know the answer to.
ALLOW_LOCAL_OVERRIDE_DEFAULT = False

# Self-consistency: with votes>1 the review runs N times at nonzero
# temperature and an override is honoured ONLY if every run agrees.
# Disagreement across runs is itself the signal — it means the model is
# guessing, which is exactly when you don't want it promoting anything.
DEFAULT_VOTES = 3
VOTE_TEMPERATURE = 0.4

# Soft import of the existing validator + parser
sys.path.insert(0, str(ROOT))
from aphasia_kb import parse_markdown, _validate_v2_entry  # noqa: E402

# Soft import of the quote-locator from annotate_paper
try:
    from annotate_paper import _normalize  # type: ignore
except Exception:
    def _normalize(s: str) -> str:
        """Fallback normalizer: lower + collapse whitespace."""
        return re.sub(r"\s+", " ", s.lower()).strip()


# ============================================================
# Verdicts
# ============================================================
class Verdict:
    APPROVE     = "auto_approve"
    PROVISIONAL = "provisional_approve"   # would auto_approve, but PDF check
                                           # was skipped — held pending PDF
                                           # re-verification on a machine with
                                           # papers/. Does NOT trigger promote.
    DEFER       = "defer_to_human"
    REJECT      = "auto_reject"


@dataclass
class Check:
    name: str
    passed: bool | None       # True/False, or None if check was skipped
    blocker: bool             # True = LLM cannot override
    details: list[str] = field(default_factory=list)

    def to_yaml_dict(self) -> dict:
        d: dict[str, Any] = {"name": self.name, "passed": self.passed,
                             "blocker": self.blocker}
        if self.details:
            d["details"] = self.details
        return d


# ============================================================
# Deterministic checks
# ============================================================

def check_schema_validates(fm: dict, draft_path: Path) -> Check:
    issues: list[str] = []
    _validate_v2_entry(fm, str(draft_path), issues)
    return Check("schema_valid", not issues, blocker=True, details=issues)


def check_provenance_confidence(fm: dict) -> Check:
    """Pass = every finding has provenance.confidence == 'high'."""
    bad: list[str] = []
    for f in fm.get("findings") or []:
        c = (f.get("provenance") or {}).get("confidence")
        if c != "high":
            bad.append(f"{f.get('id', '?')}: confidence={c!r}")
    return Check("all_findings_confidence_high", not bad,
                 blocker=False, details=bad)


def check_provenance_not_low(fm: dict) -> Check:
    """Hard: provenance.confidence == 'low' is never auto-approvable."""
    bad: list[str] = []
    for f in fm.get("findings") or []:
        c = (f.get("provenance") or {}).get("confidence")
        if c == "low":
            bad.append(f"{f.get('id', '?')}: confidence=low")
    return Check("no_low_confidence_findings", not bad,
                 blocker=True, details=bad)


def check_no_contradictions(fm: dict) -> Check:
    bad = [f.get("id") for f in (fm.get("findings") or [])
           if f.get("contradictions")]
    return Check("no_contradictions", not bad, blocker=True,
                 details=[f"{fid} has non-empty contradictions" for fid in bad])


# Words that, when present in provenance.flags, mean "human eyeballs needed".
# `cohort overlap` and `legacy` are routine bookkeeping — not blockers.
_REVIEW_WORDS = re.compile(
    r"\b(placeholder|verify|verified|uncertain|ambiguous|"
    r"unclear|approximate|rough|todo|fixme|review|"
    r"not[\s\-]+extracted|to[\s\-]+confirm)\b",
    re.IGNORECASE,
)
_INFO_WORDS = re.compile(
    r"\b(cohort[\s\-]+overlap|legacy|forward[\s\-]+looking)\b",
    re.IGNORECASE,
)


def check_no_human_review_flags(fm: dict) -> Check:
    bad: list[str] = []
    for f in fm.get("findings") or []:
        flags = (f.get("provenance") or {}).get("flags") or []
        for fl in flags:
            s = str(fl)
            if _INFO_WORDS.search(s):
                continue
            if _REVIEW_WORDS.search(s):
                bad.append(f"{f.get('id')}: {s[:80]}")
                break
    return Check("no_human_review_flags", not bad, blocker=False, details=bad)


def check_strength_moderate_or_better(fm: dict) -> Check:
    bad: list[str] = []
    for f in fm.get("findings") or []:
        s = f.get("strength")
        if s in (None, "weak", "very_weak"):
            bad.append(f"{f.get('id')}: strength={s!r}")
    return Check("strength_moderate_or_better", not bad,
                 blocker=False, details=bad)


def check_cross_finding_consistency(fm: dict) -> Check:
    """Same citation → same sample.n across findings."""
    by_cite: dict[str, set[int]] = {}
    for f in fm.get("findings") or []:
        cite = f.get("citation")
        n = (f.get("sample") or {}).get("n")
        if cite and isinstance(n, int):
            by_cite.setdefault(cite, set()).add(n)
    bad = [f"{cite}: sample.n disagrees: {sorted(ns)}"
           for cite, ns in by_cite.items() if len(ns) > 1]
    return Check("cross_finding_consistency", not bad,
                 blocker=False, details=bad)


def _extract_pdf_text(pdf_path: Path) -> str:
    """Return all text from a PDF (or read .txt directly).

    Falls back to empty string with a noted error if pymupdf is missing.
    """
    if pdf_path.suffix.lower() == ".txt":
        return pdf_path.read_text(encoding="utf-8", errors="ignore")
    try:
        import fitz  # pymupdf
    except ImportError as e:
        raise RuntimeError("pymupdf required for PDF reading "
                           "(pip install pymupdf)") from e
    doc = fitz.open(str(pdf_path))
    return "\n".join(page.get_text() for page in doc)


def check_pdf_quote_match(fm: dict, papers_dir: Path = PAPERS_DIR,
                          threshold: float = PDF_MATCH_THRESHOLD) -> Check:
    """For each finding's citation, locate the PDF in `papers_dir` and
    verify each `source_passages` quote substring-matches the PDF text.

    Returns Check.passed = None (skipped) when no PDF is available for
    any of the cited papers — caller decides how to treat that.
    """
    citations = {f.get("citation") for f in (fm.get("findings") or [])
                 if f.get("citation")}
    citations.discard(None)

    cite_to_pdf: dict[str, Path] = {}
    for cite in citations:
        key = cite.lstrip("@")
        for ext in (".pdf", ".txt"):
            cand = papers_dir / f"{key}{ext}"
            if cand.exists():
                cite_to_pdf[cite] = cand
                break

    if not cite_to_pdf:
        return Check("pdf_quote_match", passed=None, blocker=True,
                     details=[f"no PDFs available in {papers_dir} for any "
                              f"cited paper"])

    text_cache: dict[str, str] = {}
    misses: list[str] = []
    total = 0
    matched = 0
    read_errors: list[str] = []

    for f in fm.get("findings") or []:
        cite = f.get("citation")
        if cite not in cite_to_pdf:
            continue
        if cite not in text_cache:
            try:
                text_cache[cite] = _normalize(_extract_pdf_text(cite_to_pdf[cite]))
            except Exception as e:
                read_errors.append(f"{cite}: {e}")
                text_cache[cite] = ""
        norm_text = text_cache[cite]
        for sp in f.get("source_passages") or []:
            quote = (sp.get("quote") or "").strip()
            if not quote:
                continue
            total += 1
            # Case-insensitive: `_normalize` deliberately preserves case
            # (annotate_paper needs it to locate highlight rects), but for
            # a containment test case only produces false failures — a
            # curator quoting mid-sentence writes "the two groups…" where
            # the paper has "The two groups…". This is a BLOCKER check, so
            # a false failure auto-rejects a perfectly good draft.
            qnorm = _normalize(quote).casefold()
            if qnorm in norm_text.casefold():
                matched += 1
            else:
                misses.append(
                    f"{f.get('id')}.{sp.get('section', '?')} (p.{sp.get('page', '?')}): "
                    f"{quote[:80]}…")

    if total == 0:
        return Check("pdf_quote_match", passed=None, blocker=True,
                     details=["no quotes to match"])

    score = matched / total
    details = [f"matched {matched}/{total} quotes ({score:.0%})"]
    if read_errors:
        details.extend(read_errors)
    if misses:
        details.append(f"{len(misses)} quotes did not match — first 3:")
        details.extend(f"  - {m}" for m in misses[:3])
    return Check("pdf_quote_match", passed=score >= threshold,
                 blocker=True, details=details)


ALL_CHECKS: list = [
    check_schema_validates,
    check_provenance_not_low,
    check_no_contradictions,
    check_pdf_quote_match,
    check_provenance_confidence,
    check_no_human_review_flags,
    check_strength_moderate_or_better,
    check_cross_finding_consistency,
]


def run_deterministic_checks(fm: dict, draft_path: Path,
                             papers_dir: Path = PAPERS_DIR) -> list[Check]:
    """Run every deterministic check and return them in order."""
    out: list[Check] = []
    for fn in ALL_CHECKS:
        try:
            if fn is check_schema_validates:
                out.append(fn(fm, draft_path))
            elif fn is check_pdf_quote_match:
                out.append(fn(fm, papers_dir))
            else:
                out.append(fn(fm))
        except Exception as e:
            out.append(Check(fn.__name__.replace("check_", ""),
                             passed=False, blocker=True,
                             details=[f"check raised: {e}"]))
    return out


# ============================================================
# Verdict logic
# ============================================================

def compute_verdict(checks: list[Check],
                    require_pdf_match: bool = False,
                    provisional_without_pdf: bool = False) -> str:
    """Map check results to a verdict.

    `provisional_without_pdf` (opt-in): when the PDF quote-match was
    skipped (no PDF available) and everything else passes, return
    `provisional_approve` instead of `auto_approve`. The draft is then
    held until re-verified on a machine where the PDF is present.
    """
    schema = next((c for c in checks if c.name == "schema_valid"), None)
    if schema and schema.passed is False:
        return Verdict.REJECT

    pdf = next((c for c in checks if c.name == "pdf_quote_match"), None)
    if pdf and pdf.passed is False:
        return Verdict.REJECT
    if pdf and pdf.passed is None and require_pdf_match:
        return Verdict.DEFER

    blockers_failed = [c for c in checks
                       if c.blocker and c.passed is False
                       and c.name not in ("schema_valid", "pdf_quote_match")]
    if blockers_failed:
        return Verdict.DEFER

    softs_failed = [c for c in checks if not c.blocker and c.passed is False]
    if softs_failed:
        return Verdict.DEFER

    # Would-be APPROVE — downgrade to PROVISIONAL when PDF check was
    # skipped, if the caller asked for that behaviour.
    if provisional_without_pdf and pdf and pdf.passed is None:
        return Verdict.PROVISIONAL
    return Verdict.APPROVE


# ============================================================
# LLM second-opinion (optional)
# ============================================================
LLM_SYSTEM_PROMPT = """\
You review draft entries for a stroke/aphasia research knowledge base.

An automated checker already flagged this draft. You decide one thing:
was that flag correct, or is the draft actually fine?

Answer with exactly one verdict:

  agree_defer      The flag was fair. A human should look. CHOOSE THIS
                   WHEN UNSURE. This is the safe, expected answer.
  override_approve The flag was a false alarm and the draft is clearly
                   correct. Only when you are certain.
  escalate_reject  The draft has a real error the checker missed.

How to decide, per finding:
  1. Read each quote marked [claim]. Does that quote, ON ITS OWN, state
     what the claim says? If you have to infer or fill gaps, it does not.
  2. Does `strength` match the quotes? A quote describing a correlation
     does not support a causal claim.
  3. Is the flag routine bookkeeping, or a real problem?

If ANY finding fails any of these, answer agree_defer.

Important: the draft being well-written, well-formatted, or confident is
NOT evidence that it is correct. Judge only whether the quotes support
the claims.

Give one entry in `per_finding` for EVERY finding id listed, using the
exact ids given. Do not invent ids. Keep `rationale` under 60 words and
make it specific — name the finding and the quote you relied on.
"""


# JSON Schema for constrained decoding. Ollama restricts the sampler to
# tokens that keep the output schema-valid, so the model cannot emit a
# verdict outside the enum or skip a required key. This is the single
# biggest reliability win for a mid-size local model — far more robust
# than asking politely for a fenced YAML block.
LLM_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "overall_verdict": {
            "type": "string",
            "enum": ["agree_defer", "override_approve", "escalate_reject"],
        },
        "rationale": {"type": "string"},
        "per_finding": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "quotes_support_claim": {"type": "boolean"},
                    "concern": {"type": "string"},
                    "supports_approval": {"type": "boolean"},
                },
                "required": ["id", "quotes_support_claim", "concern",
                             "supports_approval"],
            },
        },
    },
    "required": ["overall_verdict", "rationale", "per_finding"],
}


def _validate_llm_payload(parsed: dict | None,
                          expected_ids: list[str]) -> list[str]:
    """Return a list of structural problems with the model's response.

    Any problem here means we do NOT trust the verdict. Catching a
    confabulated or incomplete response is cheap; acting on one is not.
    """
    problems: list[str] = []
    if not isinstance(parsed, dict):
        return ["response was not a JSON object"]

    verdict = parsed.get("overall_verdict")
    if verdict not in ("agree_defer", "override_approve", "escalate_reject"):
        problems.append(f"unknown overall_verdict {verdict!r}")

    pf = parsed.get("per_finding")
    if not isinstance(pf, list):
        problems.append("per_finding missing or not a list")
        return problems

    got_ids = [str(x.get("id")) for x in pf if isinstance(x, dict)]
    missing = [i for i in expected_ids if i not in got_ids]
    invented = [i for i in got_ids if i not in expected_ids]
    if missing:
        problems.append(f"did not review finding(s): {missing}")
    if invented:
        problems.append(f"invented finding id(s) not in the draft: {invented}")

    # Internal coherence: approving overall while flagging a finding as
    # unsupported means the model contradicted itself.
    if verdict == "override_approve":
        bad = [str(x.get("id")) for x in pf if isinstance(x, dict)
               and (x.get("quotes_support_claim") is False
                    or x.get("supports_approval") is False)]
        if bad:
            problems.append(
                f"said override_approve but marked {bad} as unsupported")

    rationale = (parsed.get("rationale") or "").strip()
    if len(rationale) < 15:
        problems.append("rationale empty or too short to audit")

    return problems


def _one_llm_pass(prompt: str, model: str, host: str, expected_ids: list[str],
                  temperature: float, seed: int | None) -> dict:
    """Single review pass. Returns {verdict, parsed, raw, problems, error}."""
    from ollama_client import OllamaError, chat
    try:
        res = chat(prompt, model=model, system=LLM_SYSTEM_PROMPT,
                   max_tokens=2000, host=host, temperature=temperature,
                   seed=seed, fmt=LLM_RESPONSE_SCHEMA, verbose=False)
    except OllamaError as e:
        return {"error": str(e), "verdict": None, "parsed": None, "raw": "",
                "problems": ["transport error"]}

    raw = res["text"]
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        parsed = _parse_llm_yaml(raw)   # legacy/fallback path

    # A model that answers in prose yields a str (or None) here, not a
    # dict. Coerce so downstream never has to care.
    if not isinstance(parsed, dict):
        parsed = None

    problems = _validate_llm_payload(parsed, expected_ids)
    if res.get("truncated_output"):
        problems.append("response truncated at num_predict")
    return {"error": None,
            "verdict": (parsed or {}).get("overall_verdict"),
            "parsed": parsed, "raw": raw, "problems": problems}


def llm_second_opinion(fm: dict, det_checks: list[Check],
                       model: str = DEFAULT_LLM_MODEL,
                       host: str | None = None,
                       votes: int = DEFAULT_VOTES,
                       allow_override: bool = ALLOW_LOCAL_OVERRIDE_DEFAULT
                       ) -> dict:
    """Ask a LOCAL model for a skeptical second opinion on a deferred draft.

    Runs entirely against Ollama — draft text and verbatim quotes never
    leave the machine.

    Guardrails, in order of application:
      1. Schema-constrained decoding (verdict must be in the enum).
      2. Structural validation — must review exactly the real finding
         ids, must not contradict itself, must give an auditable
         rationale. Any failure ⇒ verdict discarded, draft stays deferred.
      3. Self-consistency — with votes>1, all runs must agree.
      4. Override lockout — `override_approve` is downgraded to
         agree_defer unless `allow_override` is True.

    Every guardrail fails toward "leave it deferred for a human", which
    is the cheap error. Returns the usual dict plus `guardrails`, which
    records anything that fired so the sidecar YAML stays auditable.
    """
    from ollama_client import DEFAULT_HOST, is_local
    host = host or DEFAULT_HOST

    expected_ids = [str(f.get("id")) for f in (fm.get("findings") or [])]
    if not expected_ids:
        return {"error": "draft has no findings to review", "model": model}

    prompt = _build_llm_prompt(fm, det_checks)
    guardrails: list[str] = []
    if not is_local(host):
        guardrails.append(f"WARNING: host {host} is not local")

    votes = max(1, votes)
    passes = [
        _one_llm_pass(prompt, model, host, expected_ids,
                      temperature=(0.0 if votes == 1 else VOTE_TEMPERATURE),
                      seed=(None if votes == 1 else 1000 + i))
        for i in range(votes)
    ]

    transport_errs = [p["error"] for p in passes if p["error"]]
    if len(transport_errs) == len(passes):
        return {"model": model, "error": transport_errs[0],
                "verdict_override": None, "parsed": None,
                "guardrails": ["all passes failed to reach Ollama"]}

    good = [p for p in passes if not p["error"] and not p["problems"]]
    rejected = [p for p in passes if p["problems"] and not p["error"]]
    for p in rejected:
        guardrails.append(f"discarded a pass: {'; '.join(p['problems'])}")

    if not good:
        return {"model": model, "parsed": (passes[0] or {}).get("parsed"),
                "raw_response": passes[0].get("raw", ""),
                "verdict_override": None,
                "error": "no structurally valid response; leaving deferred",
                "guardrails": guardrails}

    verdicts = {p["verdict"] for p in good}
    unanimous = len(verdicts) == 1 and len(good) == votes
    if not unanimous:
        guardrails.append(
            f"votes disagreed or were incomplete ({[p['verdict'] for p in good]}"
            f" over {votes} run(s)) — no override applied")

    best = good[0]
    verdict = best["verdict"]

    override = None
    if unanimous:
        if verdict == "escalate_reject":
            override = "reject"          # fails safe — always honoured
        elif verdict == "override_approve":
            if allow_override:
                override = "approve"
            else:
                guardrails.append(
                    "model said override_approve; downgraded to agree_defer "
                    "(local override disabled — pass --allow-local-override "
                    "to trust it)")

    return {"model": model, "raw_response": best["raw"],
            "parsed": best["parsed"], "verdict_override": override,
            "votes": votes, "vote_verdicts": [p["verdict"] for p in passes],
            "unanimous": unanimous, "guardrails": guardrails, "error": None}


def _build_llm_prompt(fm: dict, det_checks: list[Check]) -> str:
    parts = [f"# Draft under review: {fm.get('id')}",
             f"Kind: {fm.get('kind')}  ·  schema_version: {fm.get('schema_version')}",
             "",
             "## Deterministic checks that failed (the deferral reasons)"]
    any_failed = False
    for c in det_checks:
        if c.passed is False:
            any_failed = True
            tag = "BLOCKER" if c.blocker else "soft"
            parts.append(f"- [{tag}] {c.name}: " +
                         "; ".join(c.details[:3]) if c.details else c.name)
    if not any_failed:
        parts.append("(none — escalation path)")

    findings = fm.get("findings") or []
    ids = [str(f.get("id")) for f in findings]

    # State the id list up front AND require it back. A mid-size model
    # skipping a finding is a common failure; making the checklist
    # explicit both reduces it and makes it detectable downstream.
    parts.append(f"\n## Findings to review ({len(ids)} total)")
    parts.append(f"You must return exactly these ids in `per_finding`: "
                 f"{', '.join(ids)}")

    for f in findings:
        parts.append(f"\n### Finding id: {f.get('id')}")
        parts.append(f"- citation: {f.get('citation')}")
        parts.append(f"- target: {f.get('target')} ({f.get('target_kind')})")
        parts.append(f"- CLAIM: {f.get('claim')}")
        parts.append(f"- strength: {f.get('strength')}  ·  "
                     f"confidence: {(f.get('provenance') or {}).get('confidence')}")
        flags = (f.get('provenance') or {}).get('flags') or []
        if flags:
            parts.append(f"- flags: {flags}")
        # Full quotes, not truncated: a quote clipped mid-sentence can
        # look like it fails to support a claim it actually supports.
        # Quote text is the entire basis for the judgement, so it is the
        # last thing that should be shortened to save context.
        parts.append("- QUOTES FROM THE PAPER:")
        for sp in f.get("source_passages") or []:
            q = (sp.get("quote") or "").strip()
            parts.append(f"    - [{sp.get('supports','?')}] "
                         f"(p.{sp.get('page','?')}) \"{q}\"")
        if not (f.get("source_passages") or []):
            parts.append("    (none — a claim with no quotes cannot be "
                         "approved)")

    parts.append(f"\n## Your task")
    parts.append(f"For each of {', '.join(ids)}: do the [claim] quotes above, "
                 f"read literally, state what CLAIM says? Then give one "
                 f"overall verdict. When in doubt, answer agree_defer.")
    return "\n".join(parts)


def _parse_llm_yaml(raw: str) -> dict | None:
    """Find the first ```yaml block in `raw` and parse it.

    Always returns a dict or None — never a bare str. `yaml.safe_load`
    happily parses a prose sentence into a string, which would otherwise
    sail downstream and blow up on `.get`.
    """
    def _load(text: str) -> dict | None:
        try:
            out = yaml.safe_load(text)
        except Exception:
            return None
        return out if isinstance(out, dict) else None

    m = re.search(r"```ya?ml\s*\n(.*?)\n```", raw, re.DOTALL | re.IGNORECASE)
    if m:
        return _load(m.group(1))
    return _load(raw)   # fallback: maybe the model emitted bare YAML


# ============================================================
# Sidecar reports
# ============================================================

def report_path_for(draft_path: Path) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    return REPORTS_DIR / f"{draft_path.stem}.yaml"


def write_report(draft_path: Path, verdict: str, checks: list[Check],
                 llm_result: dict | None = None,
                 dry_run: bool = False) -> Path | None:
    """Append a run entry to the sidecar YAML for this draft."""
    p = report_path_for(draft_path)
    if p.exists():
        report = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    else:
        report = {"draft_path": str(draft_path.relative_to(ROOT)),
                  "runs": []}
    report.setdefault("runs", [])

    run_n = len(report["runs"]) + 1
    run = {
        "run_id":    run_n,
        "timestamp": dt.datetime.now().isoformat(timespec="seconds"),
        "mode":      "with_llm_review" if llm_result else "deterministic_only",
        "verdict":   verdict,
        "checks":    [c.to_yaml_dict() for c in checks],
    }
    if llm_result:
        # Don't dump the full raw response by default if it's huge —
        # keep parsed verdict + first 800 chars of raw for audit.
        raw = llm_result.get("raw_response", "")
        run["llm_review"] = {
            "model":             llm_result.get("model"),
            "backend":           "ollama (local)",
            "verdict_override":  llm_result.get("verdict_override"),
            "parsed":            llm_result.get("parsed"),
            "raw_preview":       (raw or "")[:800],
            "error":             llm_result.get("error"),
            # Guardrail audit trail: which safety nets fired, how the
            # votes split, and whether they agreed. Keep this — it's how
            # you decide later whether the local model is trustworthy
            # enough to hand it --allow-local-override.
            "votes":             llm_result.get("votes"),
            "vote_verdicts":     llm_result.get("vote_verdicts"),
            "unanimous":         llm_result.get("unanimous"),
            "guardrails":        llm_result.get("guardrails") or [],
        }
    report["runs"].append(run)
    report["last_run"]        = run["timestamp"]
    report["latest_verdict"]  = verdict
    report["latest_mode"]     = run["mode"]

    if not dry_run:
        p.write_text(yaml.safe_dump(report, sort_keys=False,
                                    allow_unicode=True),
                     encoding="utf-8")
        return p
    return None


# ============================================================
# Promotion
# ============================================================

def auto_promote(draft_path: Path, reviewer: str = "auto-reviewer") -> tuple[bool, str]:
    """Run promote.py --approve and tag the log line as AUTO-APPROVED."""
    cmd = [sys.executable, str(PROMOTE_PY),
           "--approve", str(draft_path),
           "--reviewer", reviewer]
    res = subprocess.run(cmd, capture_output=True, text=True)
    out = (res.stdout or "") + (res.stderr or "")
    if res.returncode == 0:
        _retag_last_log_line()
    return res.returncode == 0, out


def _retag_last_log_line() -> None:
    """Replace the most recent ' | APPROVED | ' in extraction_log.md
    with ' | AUTO-APPROVED | ' so spot-check greps work later."""
    if not LOG_PATH.exists():
        return
    lines = LOG_PATH.read_text(encoding="utf-8").splitlines(keepends=True)
    for i in range(len(lines) - 1, -1, -1):
        if " | APPROVED | " in lines[i]:
            lines[i] = lines[i].replace(" | APPROVED | ",
                                        " | AUTO-APPROVED | ", 1)
            break
    LOG_PATH.write_text("".join(lines), encoding="utf-8")


# ============================================================
# Public API
# ============================================================

def review_one(draft_path: Path,
               *,
               llm_review: bool = False,
               require_pdf_match: bool = False,
               provisional_without_pdf: bool = False,
               model: str = DEFAULT_LLM_MODEL,
               papers_dir: Path = PAPERS_DIR,
               dry_run: bool = False,
               write_sidecar: bool = True,
               ollama_host: str | None = None,
               votes: int = DEFAULT_VOTES,
               allow_local_override: bool = ALLOW_LOCAL_OVERRIDE_DEFAULT
               ) -> tuple[str, list[Check], dict | None]:
    """Review one draft and return (verdict, checks, llm_result_or_None).

    See module docstring for what `provisional_without_pdf` does, and
    the guardrail notes on `llm_second_opinion` for `votes` /
    `allow_local_override`.
    """
    fm, _ = parse_markdown(draft_path)
    checks = run_deterministic_checks(fm, draft_path, papers_dir=papers_dir)
    verdict = compute_verdict(
        checks,
        require_pdf_match=require_pdf_match,
        provisional_without_pdf=provisional_without_pdf,
    )

    llm_result = None
    # LLM second-opinion runs on DEFER; can lift to APPROVE / drop to REJECT.
    # If lifted to APPROVE but PDF was skipped under provisional mode, we
    # still downgrade to PROVISIONAL (LLM can't substitute for quote
    # verification against the source PDF).
    if llm_review and verdict == Verdict.DEFER:
        llm_result = llm_second_opinion(
            fm, checks, model=model, host=ollama_host, votes=votes,
            allow_override=allow_local_override)
        ov = (llm_result or {}).get("verdict_override")
        if ov == "approve":
            verdict = Verdict.APPROVE
            pdf = next((c for c in checks
                        if c.name == "pdf_quote_match"), None)
            if (provisional_without_pdf
                    and pdf is not None and pdf.passed is None):
                verdict = Verdict.PROVISIONAL
        elif ov == "reject":
            verdict = Verdict.REJECT

    if write_sidecar:
        write_report(draft_path, verdict, checks, llm_result, dry_run=dry_run)
    return verdict, checks, llm_result


# ============================================================
# Cowork / human reviewer path (no API tokens)
# ============================================================
# Workflow:
#   1. Run `auto_review.py --deferred --emit-worksheet worksheet.yaml`
#      → produces a worksheet listing deferred drafts with their failure
#        reasons and finding summaries.
#   2. A human (or Cowork Claude in a separate session, ideally a
#      different model line from the extractor) reads each draft and
#      fills in `verdict:` and `rationale:` per item in the worksheet.
#   3. Run `auto_review.py --apply-verdicts worksheet.yaml`
#      → re-runs deterministic checks, applies each verdict, writes a
#        sidecar run with mode='manual_review' and the reviewer name,
#        promotes the approves.
#
# Hard-reject overrides remain in force: schema-fail and PDF-quote-fail
# always result in REJECT regardless of the manual verdict, because no
# amount of human judgment makes a fabricated quote real.

def apply_manual_verdict(
    draft_path: Path,
    *,
    verdict_override: str,           # "approve" | "agree_defer" | "reject"
    rationale: str,
    per_finding: list[dict] | None = None,
    reviewer: str = "cowork-claude",
    auto_promote_on_approve: bool = True,
    require_pdf_match: bool = False,
    provisional_without_pdf: bool = False,
    papers_dir: Path = PAPERS_DIR,
) -> tuple[str, list[Check]]:
    """Apply a verdict provided by a human or non-API reviewer.

    Re-runs the deterministic checks (so schema/PDF state is fresh),
    then maps the manual verdict + check results to a final verdict:

      - schema_valid == False     → REJECT (cannot override)
      - pdf_quote_match == False  → REJECT (cannot override)
      - else verdict_override:
          "approve"     → APPROVE  (or PROVISIONAL if PDF skipped + flag)
          "reject"      → REJECT
          "agree_defer" → DEFER

    Writes a sidecar run with mode='manual_review' and the reviewer
    name, then optionally promotes via promote.py.
    """
    if verdict_override not in ("approve", "agree_defer", "reject"):
        raise ValueError(
            f"verdict_override must be approve/agree_defer/reject, "
            f"got {verdict_override!r}")

    fm, _ = parse_markdown(draft_path)
    checks = run_deterministic_checks(fm, draft_path, papers_dir=papers_dir)

    # Hard rejections — manual reviewer cannot override these.
    schema = next((c for c in checks if c.name == "schema_valid"), None)
    pdf    = next((c for c in checks if c.name == "pdf_quote_match"), None)
    if schema and schema.passed is False:
        final_verdict = Verdict.REJECT
    elif pdf and pdf.passed is False:
        final_verdict = Verdict.REJECT
    elif verdict_override == "approve":
        final_verdict = Verdict.APPROVE
        if provisional_without_pdf and pdf is not None and pdf.passed is None:
            final_verdict = Verdict.PROVISIONAL
    elif verdict_override == "reject":
        final_verdict = Verdict.REJECT
    else:  # agree_defer
        final_verdict = Verdict.DEFER

    manual_record = {
        "model":            reviewer,
        "verdict_override": ("approve" if verdict_override == "approve"
                             else "reject" if verdict_override == "reject"
                             else None),
        "parsed": {
            "overall_verdict": ("override_approve" if verdict_override == "approve"
                                else "escalate_reject" if verdict_override == "reject"
                                else "agree_defer"),
            "rationale":   rationale,
            "per_finding": per_finding or [],
        },
        "raw_preview": (rationale or "")[:800],
        "error":       None,
    }
    write_report(draft_path, final_verdict, checks, manual_record)

    if final_verdict == Verdict.APPROVE and auto_promote_on_approve:
        auto_promote(draft_path, reviewer=reviewer)

    return final_verdict, checks


def emit_worksheet(drafts: list[Path], *,
                   papers_dir: Path = PAPERS_DIR,
                   require_pdf_match: bool = False,
                   provisional_without_pdf: bool = False,
                   include_quotes: bool = True) -> str:
    """Generate a YAML worksheet for batch review by a human or Cowork
    Claude. Each item shows the draft's failure reasons + a per-finding
    summary so the reviewer can decide without re-opening every file
    (though they should always sample the actual drafts for the most
    consequential decisions)."""
    items: list[dict] = []
    for d in drafts:
        try:
            fm, _ = parse_markdown(d)
            checks = run_deterministic_checks(fm, d, papers_dir=papers_dir)
            verdict = compute_verdict(checks, require_pdf_match,
                                      provisional_without_pdf)
        except Exception as e:
            items.append({"draft": str(d.relative_to(ROOT)),
                          "error": repr(e)})
            continue

        failure_reasons: list[str] = []
        for c in checks:
            if c.passed is False:
                tag = "blk" if c.blocker else "sft"
                first = (c.details or [""])[0]
                failure_reasons.append(f"({tag}) {c.name}: {first}")
            elif c.passed is None and c.blocker:
                failure_reasons.append(f"(skipped) {c.name}: "
                                       f"{(c.details or [''])[0]}")

        findings_summary: list[dict] = []
        for f in fm.get("findings") or []:
            row: dict[str, Any] = {
                "id":         f.get("id"),
                "target":     f.get("target"),
                "claim":      (f.get("claim") or "")[:240],
                "strength":   f.get("strength"),
                "confidence": (f.get("provenance") or {}).get("confidence"),
                "flags":      (f.get("provenance") or {}).get("flags") or [],
            }
            if include_quotes:
                # Just the supports: claim quotes — most relevant for
                # verifying whether a claim is actually backed.
                row["claim_quotes"] = [
                    {"page":   sp.get("page"),
                     "quote":  (sp.get("quote") or "")[:240]}
                    for sp in (f.get("source_passages") or [])
                    if sp.get("supports") == "claim"
                ]
            findings_summary.append(row)

        items.append({
            "draft":             str(d.relative_to(ROOT)),
            "current_verdict":   verdict,
            "failure_reasons":   failure_reasons or None,
            "findings_summary":  findings_summary,
            # ↓ reviewer fills these in:
            "verdict":           None,   # approve | agree_defer | reject
            "rationale":         None,   # 1-3 sentences
            "per_finding":       None,   # optional list of {id, concern,
                                         # supports_approval}
        })

    header = (
        "# auto_review.py worksheet\n"
        "#\n"
        "# For each draft below, fill in:\n"
        "#   verdict:   approve | agree_defer | reject\n"
        "#   rationale: 1-3 sentences explaining the call\n"
        "#   per_finding (optional): list of {id, concern, supports_approval}\n"
        "#\n"
        "# Then apply with:\n"
        "#   python auto_review.py --apply-verdicts <this-file>\n"
        "#\n"
        "# Notes:\n"
        "#   - 'approve' on a deferred draft lifts to auto_approve and "
        "promotes via promote.py.\n"
        "#   - 'reject' marks as auto_reject (the draft stays in drafts/).\n"
        "#   - 'agree_defer' keeps it deferred (still needs human attention).\n"
        "#   - schema_valid / pdf_quote_match failures CANNOT be overridden.\n"
        "\n"
    )
    return header + yaml.safe_dump({"drafts": items}, sort_keys=False,
                                   allow_unicode=True, width=100)


def apply_worksheet(path: Path, *,
                    reviewer: str = "cowork-claude",
                    promote: bool = True,
                    papers_dir: Path = PAPERS_DIR,
                    require_pdf_match: bool = False,
                    provisional_without_pdf: bool = False,
                    verbose: bool = True) -> dict:
    """Apply verdicts from a worksheet YAML written by `emit_worksheet`."""
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    items = data.get("drafts") or []

    counts = {Verdict.APPROVE: 0, Verdict.PROVISIONAL: 0,
              Verdict.DEFER: 0, Verdict.REJECT: 0}
    skipped: list[str] = []
    promoted: list[str] = []

    for item in items:
        draft_rel = item.get("draft")
        if not draft_rel:
            continue
        if "error" in item:
            skipped.append(f"{draft_rel} (worksheet error: {item['error']})")
            continue
        v_in = (item.get("verdict") or "").strip().lower()
        if not v_in:
            skipped.append(f"{draft_rel} (no verdict filled in)")
            continue
        if v_in not in ("approve", "agree_defer", "reject"):
            skipped.append(f"{draft_rel} (invalid verdict {v_in!r})")
            continue

        draft_path = ROOT / draft_rel
        if not draft_path.exists():
            skipped.append(f"{draft_rel} (draft no longer exists)")
            continue

        try:
            final_verdict, _checks = apply_manual_verdict(
                draft_path,
                verdict_override=v_in,
                rationale=item.get("rationale") or "(no rationale provided)",
                per_finding=item.get("per_finding"),
                reviewer=reviewer,
                auto_promote_on_approve=promote,
                require_pdf_match=require_pdf_match,
                provisional_without_pdf=provisional_without_pdf,
                papers_dir=papers_dir,
            )
        except Exception as e:
            skipped.append(f"{draft_rel} (error: {e!r})")
            continue

        counts[final_verdict] += 1
        if final_verdict == Verdict.APPROVE:
            promoted.append(draft_rel)

        if verbose:
            emoji = {Verdict.APPROVE:     "✓",
                     Verdict.PROVISIONAL: "◐",
                     Verdict.DEFER:       "⚠",
                     Verdict.REJECT:      "✗"}[final_verdict]
            print(f"{emoji} {draft_rel}: {v_in} → {final_verdict}")

    if verbose:
        print(f"\nApplied {sum(counts.values())} verdict(s): "
              f"{counts[Verdict.APPROVE]} approve, "
              f"{counts[Verdict.PROVISIONAL]} provisional, "
              f"{counts[Verdict.DEFER]} defer, "
              f"{counts[Verdict.REJECT]} reject")
        if skipped:
            print(f"Skipped {len(skipped)}:")
            for s in skipped:
                print(f"  - {s}")

    return {"counts": counts, "promoted": promoted, "skipped": skipped}


def select_drafts(*, draft: Path | None = None,
                  all_drafts: bool = False,
                  deferred_only: bool = False,
                  pending_pdf_only: bool = False) -> list[Path]:
    """Pick the set of drafts to operate on.

    `pending_pdf_only` selects drafts whose latest verdict was
    `provisional_approve` — i.e., would have auto-approved but PDF
    quote-match was skipped. Use this on the machine that has papers/
    to finalise the verdict.
    """
    if draft:
        return [Path(draft)]
    if not (DRAFTS_DIR.exists() and DRAFTS_DIR.is_dir()):
        return []
    found = sorted(DRAFTS_DIR.rglob("*.md"))
    if deferred_only or pending_pdf_only:
        target = (Verdict.PROVISIONAL if pending_pdf_only
                  else Verdict.DEFER)
        keep: list[Path] = []
        for d in found:
            r = report_path_for(d)
            if not r.exists():
                continue
            try:
                report = yaml.safe_load(r.read_text(encoding="utf-8")) or {}
            except Exception:
                continue
            if report.get("latest_verdict") == target:
                keep.append(d)
        return keep
    if all_drafts:
        return found
    return []


def review_many(drafts: list[Path], *,
                llm_review: bool = False,
                require_pdf_match: bool = False,
                provisional_without_pdf: bool = False,
                model: str = DEFAULT_LLM_MODEL,
                papers_dir: Path = PAPERS_DIR,
                reviewer: str = "auto-reviewer",
                dry_run: bool = False,
                promote: bool = True,
                ollama_host: str | None = None,
                votes: int = DEFAULT_VOTES,
                allow_local_override: bool = ALLOW_LOCAL_OVERRIDE_DEFAULT,
                verbose: bool = True) -> dict:
    """Review many drafts. Returns a summary dict.

    Promotion is triggered ONLY when verdict == Verdict.APPROVE.
    `provisional_approve` is held for re-verification on a machine with
    PDFs available.
    """
    counts = {Verdict.APPROVE: 0, Verdict.PROVISIONAL: 0,
              Verdict.DEFER: 0, Verdict.REJECT: 0}
    promoted: list[Path] = []
    failed_to_promote: list[Path] = []
    per_draft: list[dict] = []

    for d in drafts:
        if verbose:
            print(f"\n→ {d.relative_to(ROOT)}")
        try:
            verdict, checks, llm = review_one(
                d, llm_review=llm_review,
                require_pdf_match=require_pdf_match,
                provisional_without_pdf=provisional_without_pdf,
                model=model, papers_dir=papers_dir,
                dry_run=dry_run, ollama_host=ollama_host, votes=votes,
                allow_local_override=allow_local_override,
            )
        except Exception as e:
            if verbose:
                print(f"  ✗ ERROR: {e!r}")
            per_draft.append({"draft": str(d), "error": repr(e)})
            continue
        counts[verdict] += 1
        per_draft.append({"draft": str(d), "verdict": verdict})
        if verbose:
            emoji = {"auto_approve":        "✓",
                     "provisional_approve": "◐",
                     "defer_to_human":      "⚠",
                     "auto_reject":         "✗"}[verdict]
            mode  = "+LLM" if llm else "    "
            print(f"  {emoji} [{mode}] {verdict}")
            for c in checks:
                if c.passed is False:
                    tag = "blk" if c.blocker else "sft"
                    first = (c.details or [""])[0]
                    print(f"      ⨯ ({tag}) {c.name}: {first}")
                elif c.passed is None:
                    print(f"      · ({'blk' if c.blocker else 'sft'}) "
                          f"{c.name}: skipped — "
                          f"{(c.details or [''])[0]}")
            if llm and llm.get("error"):
                print(f"      ! LLM error: {llm['error']}")
            elif llm and llm.get("verdict_override"):
                print(f"      ↻ LLM overrode: {llm['verdict_override']}")

        if verdict == Verdict.APPROVE and promote and not dry_run:
            ok, out = auto_promote(d, reviewer=reviewer)
            if ok:
                promoted.append(d)
                if verbose:
                    print(f"  → promoted")
            else:
                failed_to_promote.append(d)
                if verbose:
                    print(f"  ⨯ promote.py failed:\n{out}")

    summary = {
        "counts":            counts,
        "n_promoted":        len(promoted),
        "n_failed_promote":  len(failed_to_promote),
        "promoted":          [str(p) for p in promoted],
        "failed_to_promote": [str(p) for p in failed_to_promote],
        "per_draft":         per_draft,
    }
    if verbose:
        print(f"\nSummary: {counts[Verdict.APPROVE]} auto_approve, "
              f"{counts[Verdict.PROVISIONAL]} provisional, "
              f"{counts[Verdict.DEFER]} defer, "
              f"{counts[Verdict.REJECT]} auto_reject  "
              f"(promoted={len(promoted)}, "
              f"failed_promote={len(failed_to_promote)})")
    return summary


# ============================================================
# CLI
# ============================================================

def _cli(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Agentic first-pass review of pending KB drafts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sel = p.add_mutually_exclusive_group(required=True)
    sel.add_argument("--all",         action="store_true",
                     help="Review every pending draft")
    sel.add_argument("--draft",       type=Path,
                     help="Review one specific draft path")
    sel.add_argument("--deferred",    action="store_true",
                     help="Re-review only drafts whose latest verdict was "
                          "defer_to_human (use with --llm-review for the "
                          "second-opinion pass, or with --emit-worksheet for "
                          "Cowork/human review)")
    sel.add_argument("--pending-pdf", action="store_true",
                     help="Re-review only drafts whose latest verdict was "
                          "provisional_approve (i.e., LLM/deterministic "
                          "approved on a no-PDF machine). Implies "
                          "--require-pdf-match.")
    sel.add_argument("--apply-verdicts", type=Path, metavar="WORKSHEET",
                     help="Apply verdicts from a previously emitted "
                          "worksheet YAML (no API call; the verdicts are "
                          "supplied by a human or by Cowork Claude in a "
                          "separate session). Use with --reviewer to tag "
                          "the sidecar.")

    p.add_argument("--emit-worksheet", type=Path, metavar="PATH",
                   help="Instead of running review, emit a YAML worksheet "
                        "of the selected drafts (with failure reasons + "
                        "finding summaries) for batch human/Cowork review. "
                        "Combine with --all, --draft, --deferred, or "
                        "--pending-pdf to choose which drafts go in.")

    p.add_argument("--llm-review", action="store_true",
                   help="Enable LLM second opinion using a LOCAL model via "
                        "Ollama (needs `ollama serve` running). Nothing is "
                        "sent off-machine.")
    p.add_argument("--model",      default=None,
                   help=f"Ollama model tag for LLM review. Default comes "
                        f"from models.yaml (currently {DEFAULT_LLM_MODEL}). "
                        f"Run `python model_config.py` to see it resolved.")
    p.add_argument("--ollama-host", default=None,
                   help="Ollama base URL (default: http://localhost:11434, "
                        "or OLLAMA_HOST).")
    p.add_argument("--votes", type=int, default=DEFAULT_VOTES, metavar="N",
                   help=f"Run the review N times and require unanimity "
                        f"before honouring an override (default: "
                        f"{DEFAULT_VOTES}). N=1 disables self-consistency "
                        f"checking and is faster but less safe.")
    p.add_argument("--allow-local-override", action="store_true",
                   help="Let the local model's `override_approve` actually "
                        "promote a draft into the KB. OFF by default: a "
                        "mid-size local model is agreeable, and a wrong "
                        "approval silently corrupts the KB. escalate_reject "
                        "and agree_defer are always honoured regardless.")
    p.add_argument("--require-pdf-match", action="store_true",
                   help="Refuse to auto-approve when PDF unavailable. "
                        "Default is to skip the PDF check if no papers/ files.")
    p.add_argument("--provisional-without-pdf", action="store_true",
                   help="When PDF is unavailable, mark would-be auto_approve "
                        "verdicts as provisional_approve instead. They will "
                        "NOT be promoted; use --pending-pdf later (on a "
                        "machine with papers/) to finalise them.")
    p.add_argument("--papers-dir", type=Path, default=PAPERS_DIR,
                   help=f"Where the source PDFs live (default: {PAPERS_DIR})")
    p.add_argument("--reviewer",   default="auto-reviewer",
                   help="Reviewer name passed to promote.py")
    p.add_argument("--dry-run",    action="store_true",
                   help="Compute verdicts but DO NOT promote or write logs")
    p.add_argument("--no-promote", action="store_true",
                   help="Compute and log verdicts but skip promote.py "
                        "(useful for previewing)")

    args = p.parse_args(argv)

    # --pending-pdf implies --require-pdf-match: the whole point of
    # re-running these is to verify quotes against the now-available PDF.
    # If PDFs are *still* missing, fail loudly via DEFER instead of
    # silently re-marking as provisional.
    if args.pending_pdf:
        args.require_pdf_match = True

    # Mode A: --apply-verdicts — read a worksheet, apply the verdicts.
    # No selector needed; drafts come from the worksheet itself.
    if args.apply_verdicts is not None:
        if not args.apply_verdicts.exists():
            print(f"❌ worksheet not found: {args.apply_verdicts}")
            return 2
        summary = apply_worksheet(
            args.apply_verdicts,
            reviewer=args.reviewer,
            promote=not args.no_promote,
            papers_dir=args.papers_dir,
            require_pdf_match=args.require_pdf_match,
            provisional_without_pdf=args.provisional_without_pdf,
        )
        # Delete the worksheet once verdicts have been applied — it's a
        # one-shot artifact and leaving it around risks accidental re-use.
        if summary["skipped"]:
            print(f"\n⚠ {len(summary['skipped'])} item(s) were skipped "
                  f"(see above). Worksheet kept at: {args.apply_verdicts}")
        else:
            args.apply_verdicts.unlink()
            print(f"✓ worksheet deleted: {args.apply_verdicts}")
        return 0

    drafts = select_drafts(draft=args.draft, all_drafts=args.all,
                           deferred_only=args.deferred,
                           pending_pdf_only=args.pending_pdf)
    if not drafts:
        print("(no drafts to review)")
        return 0

    # Mode B: --emit-worksheet — write a worksheet for batch review.
    # Doesn't run promotion or write sidecars. Pair with a selector.
    if args.emit_worksheet is not None:
        worksheet = emit_worksheet(
            drafts,
            papers_dir=args.papers_dir,
            require_pdf_match=args.require_pdf_match,
            provisional_without_pdf=args.provisional_without_pdf,
        )
        args.emit_worksheet.write_text(worksheet, encoding="utf-8")
        print(f"✓ worksheet written: {args.emit_worksheet} "
              f"({len(drafts)} draft(s))")
        print(f"  Fill in `verdict:` and `rationale:` for each, then run:")
        print(f"  python auto_review.py --apply-verdicts "
              f"{args.emit_worksheet} --reviewer <your-name>")
        return 0

    # Preflight the local model once, so a long --all run doesn't fail
    # on draft 1 of 60.
    if args.llm_review:
        from ollama_client import check_model_available, is_local
        _cfg = resolve_model("review", args.model)
        args.model = _cfg["model"]
        host = args.ollama_host or os.environ.get(
            "OLLAMA_HOST", "http://localhost:11434")
        if not is_local(host):
            print(f"⚠ OLLAMA_HOST points at {host}, which is not this "
                  f"machine. Draft quotes WILL leave your computer.")
        ok, msg = check_model_available(args.model, host)
        if not ok:
            p.error(msg)
        print(f"✓ {msg}  (model from {_cfg['source']})")
        if args.allow_local_override:
            note = "ENABLED — the local model can promote drafts"
        else:
            note = ("disabled — override_approve will be downgraded to "
                    "agree_defer")
        print(f"  votes={args.votes}  ·  local override {note}")

    # Mode C (default): full review pipeline.
    summary = review_many(
        drafts,
        llm_review=args.llm_review,
        require_pdf_match=args.require_pdf_match,
        provisional_without_pdf=args.provisional_without_pdf,
        model=args.model,
        papers_dir=args.papers_dir,
        reviewer=args.reviewer,
        dry_run=args.dry_run,
        promote=not args.no_promote,
        ollama_host=args.ollama_host,
        votes=args.votes,
        allow_local_override=args.allow_local_override,
    )
    return 0 if summary["n_failed_promote"] == 0 else 1


if __name__ == "__main__":
    sys.exit(_cli())
