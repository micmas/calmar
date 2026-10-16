#!/usr/bin/env python3
"""
auto_review.py — agentic first-pass review of pending KB drafts.

Workflow (GOVERNANCE.md §2–§4)
------------------------------
For each pending draft:
  1. Run deterministic safety checks. These can REJECT or DEFER; they
     never approve. A draft that passes everything is `checks_passed`,
     which is eligible for review, not approved.
  2. Classify the draft into a review tier from its frontmatter:
       Tier A  routine finding appended to an existing entry; an
               independent model may approve it.
       Tier B  therapies/ingredients, strong claims, new entries,
               reviews, flagged or low-confidence drafts; a person must.
  3. Optionally (--llm-review) ask an INDEPENDENT local model — a
     different tag from the extractor — to re-read the paper's text
     layer and answer, per finding: is each passage there, does it
     support the field it is tagged for, is the relationship faithful,
     is strength fair, do the numbers match, are limitations captured,
     is anything contradicting omitted?
  4. A unanimous model `approve` promotes a Tier A draft via
     `promote.py --reviewer model:<tag> --tier A --extractor <tag>`,
     which logs `MODEL-APPROVED`. On Tier B the model's verdict is
     recorded and the draft stays deferred for a person.
  5. Write a sidecar audit report under `auto_review_log/`.

Design
------
- Hard checks (cannot be overridden, even by LLM):
    * schema validation
    * non-empty `contradictions:` on any finding
    * PDF quote-match below threshold (likely fabricated quotes)
    * `provenance.confidence: low`
- Soft checks (defer to a reviewer; a model may still approve Tier A):
    * suspicious words in `provenance.flags` (placeholder, verify, todo,
      uncertain, ambiguous, etc.)
    * sample.n disagrees across findings citing the same paper

Defaults aim conservative — better to defer a fine draft than to
auto-approve a bad one. Tighten with `--require-pdf-match` once your
papers/ dir is populated.

Usage (CLI)
-----------
    # First pass: deterministic checks + tier classification; promotes nothing
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
ALLOW_LOCAL_OVERRIDE_DEFAULT = False   # deprecated; kept for importers

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
    ELIGIBLE    = "checks_passed"         # deterministic checks passed; NOT
                                           # approved — needs a reviewer
    APPROVE     = "auto_approve"          # approved by a model (Tier A) or
                                           # a person via a worksheet
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


# `check_provenance_confidence` (high only) and
# `check_strength_moderate_or_better` are no longer in the default set:
# under GOVERNANCE.md §3 medium confidence and weak strength are ordinary
# Tier A material, and the tier classifier already sends strong/low
# elsewhere. They remain importable for ad-hoc use.
ALL_CHECKS: list = [
    check_schema_validates,
    check_provenance_not_low,
    check_no_contradictions,
    check_pdf_quote_match,
    check_no_human_review_flags,
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

    # Everything passed. That makes the draft ELIGIBLE for review; the
    # deterministic checks never approve (GOVERNANCE.md §2).
    if provisional_without_pdf and pdf and pdf.passed is None:
        return Verdict.PROVISIONAL
    return Verdict.ELIGIBLE


# ============================================================
# Review tiers (GOVERNANCE.md §3)
# ============================================================
TIER_A_BUCKETS = ("regions", "impairments", "predictors")
TIER_A_STRENGTHS = ("weak", "moderate")
TIER_B_EVIDENCE = ("narrative-review", "case-study", "case_study")


def _canonical_exists(fm: dict, draft_path: Path, root: Path = ROOT) -> bool:
    """True when a canonical file with this draft's id already exists in
    the bucket the draft lives in (so approval appends findings)."""
    try:
        bucket = draft_path.resolve().relative_to((root / "drafts").resolve()).parts[0]
    except Exception:
        return False
    return (root / bucket / f"{fm.get('id')}.md").exists()


def classify_tier(fm: dict, checks: list[Check], draft_path: Path,
                  root: Path = ROOT) -> tuple[str, list[str]]:
    """Return ("A" | "B", reasons). Tier B reasons list why a person is
    needed; an empty list means Tier A.

    This is a classification, not a judgement: every rule reads a field
    the extractor wrote or a check result. Anything not provably Tier A
    is Tier B.
    """
    reasons: list[str] = []
    try:
        bucket = draft_path.resolve().relative_to((root / "drafts").resolve()).parts[0]
    except Exception:
        bucket = "?"
    if bucket not in TIER_A_BUCKETS:
        reasons.append(f"bucket {bucket!r} always needs a person")

    schema = next((c for c in checks if c.name == "schema_valid"), None)
    if schema is None or schema.passed is not True:
        reasons.append("schema not clean")
    pdf = next((c for c in checks if c.name == "pdf_quote_match"), None)
    if pdf is None or pdf.passed is not True:
        reasons.append("PDF quote match not run or not passed")
    else:
        m = re.search(r"matched (\d+)/(\d+)", (pdf.details or [""])[0])
        if not m or m.group(1) != m.group(2):
            reasons.append("not every passage matched the PDF exactly")

    if not _canonical_exists(fm, draft_path, root):
        reasons.append("new entry id (not appending to an existing entry)")

    for f in fm.get("findings") or []:
        fid = f.get("id", "?")
        prov = f.get("provenance") or {}
        if prov.get("confidence") not in ("high", "medium"):
            reasons.append(f"{fid}: confidence={prov.get('confidence')!r}")
        if prov.get("flags"):
            reasons.append(f"{fid}: has provenance.flags")
        if f.get("strength") not in TIER_A_STRENGTHS:
            reasons.append(f"{fid}: strength={f.get('strength')!r}")
        eq = str(f.get("evidence_quality") or "")
        if eq in TIER_B_EVIDENCE or f.get("method") == "narrative_review":
            reasons.append(f"{fid}: evidence_quality={eq!r}")
        if f.get("contradictions"):
            reasons.append(f"{fid}: has contradictions")
    return ("B" if reasons else "A"), reasons


# ============================================================
# LLM second-opinion (optional)
# ============================================================
LLM_SYSTEM_PROMPT = """\
You are the independent second reader for a stroke/aphasia research
knowledge base. A different model extracted structured findings from a
paper. You have the paper's full text layer and the draft. Your job is
to re-read the paper and check the draft against it, finding by finding.

For EVERY finding id listed, answer each check from the paper text:
  passage_present       every quoted passage appears verbatim in the text
  passage_supports_field each passage supports the field it is tagged for
                        ([claim] supports the claim, [statistics] the
                        numbers, [sample] the sample, ...), not merely
                        something nearby
  relationship_faithful the paper itself makes the kind of claim recorded
                        (causal vs correlational vs recruitment vs
                        responder); a correlation written up as causal
                        fails this
  strength_fair         `strength` is at or below what the authors claim
                        for their own result
  numbers_match         n, effect sizes, thresholds and p-values match the
                        text and tables exactly
  limitations_captured  the authors' own stated limitations that weaken
                        this finding are recorded
  omissions             a result in the paper that contradicts or
                        qualifies this finding and was left out, or ""
Then give a per-finding verdict: agree (all checks true), disagree (a
check is false), or cannot_verify (the text needed is missing or
unreadable).

Overall verdict:
  approve  every finding is `agree`. Only then.
  defer    anything is `disagree`/`cannot_verify`, or you are unsure.
           This is the normal, safe answer.
  reject   a passage is fabricated, a number is wrong, or the direction
           of a claim is reversed.

Judge only against the paper text. A well-written, confident draft is
not evidence of anything. Use the exact finding ids given; do not invent
ids. Keep `rationale` specific and under 80 words.
"""


# JSON Schema for constrained decoding. Ollama restricts the sampler to
# tokens that keep the output schema-valid, so the model cannot emit a
# verdict outside the enum or skip a required key. This is the single
# biggest reliability win for a mid-size local model — far more robust
# than asking politely for a fenced YAML block.
_CHECK_KEYS = ("passage_present", "passage_supports_field",
               "relationship_faithful", "strength_fair", "numbers_match",
               "limitations_captured")
LLM_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "overall_verdict": {"type": "string",
                            "enum": ["approve", "defer", "reject"]},
        "rationale": {"type": "string"},
        "per_finding": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    **{k: {"type": "boolean"} for k in _CHECK_KEYS},
                    "omissions": {"type": "string"},
                    "concern": {"type": "string"},
                    "verdict": {"type": "string",
                                "enum": ["agree", "disagree", "cannot_verify"]},
                },
                "required": ["id", *_CHECK_KEYS, "omissions", "concern",
                             "verdict"],
            },
        },
    },
    "required": ["overall_verdict", "rationale", "per_finding"],
}

# Legacy verdict names (v1 sidecars and the worksheet path use these).
_V2_TO_V1 = {"approve": "override_approve", "defer": "agree_defer",
             "reject": "escalate_reject"}


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
    if verdict not in ("approve", "defer", "reject"):
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

    # Internal coherence: approving overall while any check is false or
    # any finding is not `agree` means the model contradicted itself.
    if verdict == "approve":
        bad = [str(x.get("id")) for x in pf if isinstance(x, dict)
               and (x.get("verdict") != "agree"
                    or any(x.get(k) is not True for k in _CHECK_KEYS))]
        if bad:
            problems.append(
                f"said approve but did not fully agree on {bad}")
    for x in pf:
        if isinstance(x, dict) and x.get("verdict") == "agree" \
                and any(x.get(k) is False for k in _CHECK_KEYS):
            problems.append(f"{x.get('id')}: verdict agree but a check is false")

    rationale = (parsed.get("rationale") or "").strip()
    if len(rationale) < 15:
        problems.append("rationale empty or too short to audit")

    return problems


def _bare_tag(s: str | None) -> str:
    s = (s or "").strip()
    for pre in ("agent:", "model:"):
        if s.lower().startswith(pre):
            s = s[len(pre):]
    return s.lower()


def reviewer_is_independent(extractor: str | None, reviewer_model: str) -> bool:
    """A model never reviews its own drafts: tags must differ. A missing
    extractor tag cannot be shown independent, so it fails."""
    if not extractor:
        return False
    return _bare_tag(extractor) != _bare_tag(reviewer_model)


def paper_text_for(fm: dict, papers_dir: Path = PAPERS_DIR) -> tuple[str, list[str]]:
    """Full text layer (with page markers) of every paper the draft cites,
    plus a list of citations whose PDF could not be found."""
    cites = []
    for f in fm.get("findings") or []:
        c = f.get("citation")
        if c and c not in cites:
            cites.append(c)
    chunks: list[str] = []
    missing: list[str] = []
    for cite in cites:
        key = cite.lstrip("@")
        found = None
        for ext in (".pdf", ".txt"):
            cand = papers_dir / f"{key}{ext}"
            if cand.exists():
                found = cand
                break
        if not found:
            missing.append(cite)
            continue
        if found.suffix.lower() == ".txt":
            text = found.read_text(encoding="utf-8", errors="ignore")
        else:
            import fitz  # pymupdf
            doc = fitz.open(str(found))
            text = "".join(f"\n=== PAGE {i+1} ===\n" + doc[i].get_text()
                           for i in range(doc.page_count))
            doc.close()
        chunks.append(f"\n\n######## PAPER {cite} ########\n{text}")
    return "".join(chunks), missing


def _one_llm_pass(prompt: str, model: str, host: str, expected_ids: list[str],
                  temperature: float, seed: int | None,
                  max_tokens: int = 4000) -> dict:
    """Single review pass. Returns {verdict, parsed, raw, problems, error}."""
    from ollama_client import OllamaError, chat
    try:
        res = chat(prompt, model=model, system=LLM_SYSTEM_PROMPT,
                   max_tokens=max_tokens, host=host, temperature=temperature,
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
    if res.get("truncated_input"):
        problems.append("prompt truncated at num_ctx — paper not fully read")
    return {"error": None,
            "verdict": (parsed or {}).get("overall_verdict"),
            "parsed": parsed, "raw": raw, "problems": problems}


def llm_second_opinion(fm: dict, det_checks: list[Check],
                       model: str = DEFAULT_LLM_MODEL,
                       host: str | None = None,
                       votes: int = DEFAULT_VOTES,
                       allow_override: bool | None = None,
                       *,
                       tier: str = "B",
                       paper_text: str | None = None,
                       extractor: str | None = None,
                       papers_dir: Path = PAPERS_DIR) -> dict:
    """Ask an INDEPENDENT local model to re-read the paper and review.

    Runs entirely against Ollama — paper text, draft and quotes never
    leave the machine.

    Guardrails, in order of application:
      1. Independence — the reviewer tag must differ from the extractor
         tag (`created_by`), or no approval is possible.
      2. Paper present — without the PDF text the model cannot do the
         second reading; `approve` is downgraded to defer.
      3. Schema-constrained decoding (verdict must be in the enum).
      4. Structural validation — must review exactly the real finding
         ids, must not contradict itself, must give an auditable
         rationale. Any failure ⇒ verdict discarded, draft stays deferred.
      5. Self-consistency — with votes>1, all runs must agree.
      6. Tier — `approve` is honoured only on Tier A (GOVERNANCE.md §3);
         on Tier B it is recorded as agree_defer for a person.

    `allow_override` is accepted for backward compatibility and ignored:
    the tier decides, not a flag.

    Every guardrail fails toward "leave it deferred for a person", which
    is the cheap error. Returns the usual dict plus `guardrails`, which
    records anything that fired so the sidecar YAML stays auditable.
    """
    from ollama_client import DEFAULT_HOST, is_local
    host = host or DEFAULT_HOST

    expected_ids = [str(f.get("id")) for f in (fm.get("findings") or [])]
    if not expected_ids:
        return {"error": "draft has no findings to review", "model": model}

    guardrails: list[str] = []
    if allow_override is not None:
        guardrails.append("allow_override is deprecated and ignored; "
                          "the review tier decides")
    if not is_local(host):
        guardrails.append(f"WARNING: host {host} is not local")

    extractor = extractor or fm.get("created_by")
    independent = reviewer_is_independent(extractor, model)
    if not independent:
        guardrails.append(f"reviewer {model!r} is not independent of the "
                          f"extractor {extractor!r}; cannot approve")

    missing: list[str] = []
    if paper_text is None:
        paper_text, missing = paper_text_for(fm, papers_dir)
    if not paper_text:
        guardrails.append("no paper text available — second reading not "
                          "possible; approve would be downgraded")

    prompt = _build_llm_prompt(fm, det_checks, paper_text, tier)

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
                "guardrails": guardrails, "tier": tier,
                "extractor": extractor, "independent": independent}

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
        if verdict == "reject":
            override = "reject"          # fails safe — always honoured
        elif verdict == "approve":
            if not independent:
                pass                     # guardrail already recorded
            elif not paper_text:
                guardrails.append("model said approve without the paper "
                                  "text; downgraded to defer")
            elif tier != "A":
                guardrails.append(
                    f"model said approve on Tier {tier}; recorded as "
                    f"agree_defer — a person must approve this tier")
            else:
                override = "approve"

    parsed = best["parsed"]
    if isinstance(parsed, dict):
        parsed = dict(parsed)
        parsed["overall_verdict_v1"] = _V2_TO_V1.get(
            parsed.get("overall_verdict"), parsed.get("overall_verdict"))
    return {"model": model, "raw_response": best["raw"],
            "parsed": parsed, "verdict_override": override,
            "votes": votes, "vote_verdicts": [p["verdict"] for p in passes],
            "unanimous": unanimous, "guardrails": guardrails, "error": None,
            "tier": tier, "extractor": extractor, "independent": independent,
            "papers_missing": missing}


def _build_llm_prompt(fm: dict, det_checks: list[Check],
                      paper_text: str = "", tier: str = "B") -> str:
    parts = [f"# Draft under review: {fm.get('id')}",
             f"Kind: {fm.get('kind')}  ·  schema_version: {fm.get('schema_version')}"
             f"  ·  review tier: {tier}",
             f"Extracted by: {fm.get('created_by')}",
             "",
             "## Deterministic checks that failed (if any)"]
    any_failed = False
    for c in det_checks:
        if c.passed is False:
            any_failed = True
            tag = "BLOCKER" if c.blocker else "soft"
            parts.append(f"- [{tag}] {c.name}: " +
                         "; ".join(c.details[:3]) if c.details else c.name)
    if not any_failed:
        parts.append("(none)")

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
        parts.append(f"- direction: {f.get('direction')}  ·  relationship: "
                     f"{f.get('relationship')}")
        parts.append(f"- method: {f.get('method')}  ·  design: {f.get('design')}"
                     f"  ·  evidence_quality: {f.get('evidence_quality')}")
        parts.append(f"- strength: {f.get('strength')}  ·  "
                     f"confidence: {(f.get('provenance') or {}).get('confidence')}")
        sample = f.get("sample") or {}
        if sample:
            parts.append(f"- sample: n={sample.get('n')} · "
                         f"{sample.get('population')} · "
                         f"time post-onset: {sample.get('time_post_onset')}")
        stats = f.get("statistics") or {}
        if stats:
            parts.append(f"- statistics: effect={stats.get('effect_size')} · "
                         f"threshold={stats.get('threshold')} · "
                         f"p={stats.get('p_value')} · CI={stats.get('ci_95')}")
        if f.get("author_limitations"):
            parts.append(f"- author_limitations: {f.get('author_limitations')}")
        flags = (f.get('provenance') or {}).get('flags') or []
        if flags:
            parts.append(f"- flags: {flags}")
        # Full quotes, not truncated: a quote clipped mid-sentence can
        # look like it fails to support a claim it actually supports.
        parts.append("- QUOTED PASSAGES (tag = what each is said to support):")
        for sp in f.get("source_passages") or []:
            q = (sp.get("quote") or "").strip()
            parts.append(f"    - [{sp.get('supports','?')}] "
                         f"(p.{sp.get('page','?')}) \"{q}\"")
        if not (f.get("source_passages") or []):
            parts.append("    (none — a claim with no quotes cannot be "
                         "approved)")

    parts.append("\n## Your task")
    parts.append(f"Re-read the paper text below. For each of {', '.join(ids)} "
                 f"answer every check from the text, then give one overall "
                 f"verdict. When in doubt, answer defer.")
    if paper_text:
        parts.append("\n## Paper text layer (verbatim, with page markers)")
        parts.append(paper_text)
    else:
        parts.append("\n## Paper text layer: NOT AVAILABLE — you cannot "
                     "verify passages; answer cannot_verify where needed.")
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
                 dry_run: bool = False,
                 tier: str | None = None,
                 tier_reasons: list[str] | None = None) -> Path | None:
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
    if tier:
        run["review_tier"] = tier
        run["tier_reasons"] = tier_reasons or []
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
            "extractor":         llm_result.get("extractor"),
            "independent":       llm_result.get("independent"),
            "papers_missing":    llm_result.get("papers_missing"),
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

def auto_promote(draft_path: Path, reviewer: str, *,
                 tier: str | None = None,
                 extractor: str | None = None) -> tuple[bool, str]:
    """Run promote.py --approve on behalf of a named reviewer.

    `reviewer` is `human:<name>` or `model:<tag>`; promote.py refuses
    `auto-reviewer`, enforces that a model may only approve Tier A, that
    the model differs from the extractor, and writes the MODEL-APPROVED
    or APPROVED log line itself. Nothing is retagged after the fact.
    """
    cmd = [sys.executable, str(PROMOTE_PY),
           "--approve", str(draft_path),
           "--reviewer", reviewer]
    if tier:
        cmd += ["--tier", tier]
    if extractor:
        cmd += ["--extractor", extractor]
    res = subprocess.run(cmd, capture_output=True, text=True)
    out = (res.stdout or "") + (res.stderr or "")
    return res.returncode == 0, out


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
               allow_local_override: bool | None = None,
               model_approve: bool = True,
               ) -> tuple[str, list[Check], dict | None]:
    """Review one draft and return (verdict, checks, llm_result_or_None).

    The returned llm_result (when --llm-review ran) carries `tier`,
    `tier_reasons` and `extractor`, which `review_many` needs to call
    promote.py correctly. `allow_local_override` is deprecated/ignored.
    """
    fm, _ = parse_markdown(draft_path)
    checks = run_deterministic_checks(fm, draft_path, papers_dir=papers_dir)
    verdict = compute_verdict(
        checks,
        require_pdf_match=require_pdf_match,
        provisional_without_pdf=provisional_without_pdf,
    )
    tier, tier_reasons = classify_tier(fm, checks, draft_path)

    llm_result = None
    # The model reviewer runs on anything the deterministic checks did
    # not reject: ELIGIBLE (clean) and DEFER (soft/blocker flagged). It
    # can approve only Tier A; reject is always honoured.
    if llm_review and verdict in (Verdict.ELIGIBLE, Verdict.DEFER):
        llm_result = llm_second_opinion(
            fm, checks, model=model, host=ollama_host, votes=votes,
            tier=tier, papers_dir=papers_dir)
        llm_result["tier"] = tier
        llm_result["tier_reasons"] = tier_reasons
        ov = (llm_result or {}).get("verdict_override")
        if ov == "approve" and model_approve:
            verdict = Verdict.APPROVE
            pdf = next((c for c in checks
                        if c.name == "pdf_quote_match"), None)
            if (provisional_without_pdf
                    and pdf is not None and pdf.passed is None):
                verdict = Verdict.PROVISIONAL
        elif ov == "approve" and not model_approve:
            llm_result["guardrails"].append(
                "model approval disabled by --no-model-approve")
            llm_result["verdict_override"] = None
        elif ov == "reject":
            verdict = Verdict.REJECT

    if write_sidecar:
        write_report(draft_path, verdict, checks, llm_result, dry_run=dry_run,
                     tier=tier, tier_reasons=tier_reasons)
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
    reviewer: str = "human:unnamed",
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

    tier, tier_reasons = classify_tier(fm, checks, draft_path)
    manual_record = {
        "model":            reviewer,
        "tier":             tier,
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
    write_report(draft_path, final_verdict, checks, manual_record,
                 tier=tier, tier_reasons=tier_reasons)

    if final_verdict == Verdict.APPROVE and auto_promote_on_approve:
        ok, out = auto_promote(draft_path, reviewer=reviewer, tier=tier,
                               extractor=fm.get("created_by"))
        if not ok:
            raise RuntimeError(f"promote.py refused: {out.strip()}")

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

        tier, tier_reasons = classify_tier(fm, checks, d)
        items.append({
            "draft":             str(d.relative_to(ROOT)),
            "current_verdict":   verdict,
            "review_tier":       tier,
            "tier_reasons":      tier_reasons or None,
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
        "#   - 'approve' promotes via promote.py under YOUR name "
        "(--reviewer human:<name>); the tier is stamped on the entry.\n"
        "#   - 'reject' marks as auto_reject (the draft stays in drafts/).\n"
        "#   - 'agree_defer' keeps it deferred (still needs human attention).\n"
        "#   - schema_valid / pdf_quote_match failures CANNOT be overridden.\n"
        "\n"
    )
    return header + yaml.safe_dump({"drafts": items}, sort_keys=False,
                                   allow_unicode=True, width=100)


def apply_worksheet(path: Path, *,
                    reviewer: str = "human:unnamed",
                    promote: bool = True,
                    papers_dir: Path = PAPERS_DIR,
                    require_pdf_match: bool = False,
                    provisional_without_pdf: bool = False,
                    verbose: bool = True) -> dict:
    """Apply verdicts from a worksheet YAML written by `emit_worksheet`."""
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    items = data.get("drafts") or []

    counts = {Verdict.ELIGIBLE: 0, Verdict.APPROVE: 0,
              Verdict.PROVISIONAL: 0, Verdict.DEFER: 0, Verdict.REJECT: 0}
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
                reviewer: str | None = None,
                dry_run: bool = False,
                promote: bool = True,
                ollama_host: str | None = None,
                votes: int = DEFAULT_VOTES,
                allow_local_override: bool | None = None,
                model_approve: bool = True,
                verbose: bool = True) -> dict:
    """Review many drafts. Returns a summary dict.

    Promotion is triggered ONLY when verdict == Verdict.APPROVE, which
    can only come from a unanimous, independent model review of a Tier A
    draft. The promotion runs as `model:<tag>`; `reviewer` is ignored
    here (a person approves through the worksheet path).
    """
    counts = {Verdict.ELIGIBLE: 0, Verdict.APPROVE: 0,
              Verdict.PROVISIONAL: 0, Verdict.DEFER: 0, Verdict.REJECT: 0}
    tiers = {"A": 0, "B": 0}
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
                model_approve=model_approve,
            )
        except Exception as e:
            if verbose:
                print(f"  ✗ ERROR: {e!r}")
            per_draft.append({"draft": str(d), "error": repr(e)})
            continue
        counts[verdict] += 1
        tier = (llm or {}).get("tier")
        if tier is None:
            try:
                fm, _ = parse_markdown(d)
                tier, _reasons = classify_tier(fm, checks, d)
            except Exception:
                tier = "B"
        tiers[tier] = tiers.get(tier, 0) + 1
        per_draft.append({"draft": str(d), "verdict": verdict, "tier": tier})
        if verbose:
            emoji = {"checks_passed":       "○",
                     "auto_approve":        "✓",
                     "provisional_approve": "◐",
                     "defer_to_human":      "⚠",
                     "auto_reject":         "✗"}[verdict]
            mode  = "+LLM" if llm else "    "
            print(f"  {emoji} [{mode}] {verdict}  · tier {tier}")
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
            ok, out = auto_promote(
                d, reviewer=f"model:{(llm or {}).get('model') or model}",
                tier="A", extractor=(llm or {}).get("extractor"))
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
        "tiers":             tiers,
        "n_promoted":        len(promoted),
        "n_failed_promote":  len(failed_to_promote),
        "promoted":          [str(p) for p in promoted],
        "failed_to_promote": [str(p) for p in failed_to_promote],
        "per_draft":         per_draft,
    }
    if verbose:
        print(f"\nSummary: {counts[Verdict.ELIGIBLE]} checks_passed, "
              f"{counts[Verdict.APPROVE]} model-approved, "
              f"{counts[Verdict.PROVISIONAL]} provisional, "
              f"{counts[Verdict.DEFER]} defer, "
              f"{counts[Verdict.REJECT]} reject  "
              f"· tier A {tiers['A']} / tier B {tiers['B']}  "
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
    p.add_argument("--no-model-approve", action="store_true",
                   help="Record the model's verdicts but never promote on "
                        "them (Tier A approvals become agree_defer). Use "
                        "while calibrating a new reviewer model.")
    p.add_argument("--allow-local-override", action="store_true",
                   help=argparse.SUPPRESS)   # deprecated: tiers decide now
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
    p.add_argument("--reviewer",   default=None,
                   help="With --apply-verdicts: who filled in the worksheet, "
                        "as human:<name> (a bare name is a person). Not used "
                        "by the automatic path — the checks never approve, "
                        "and a model approval is stamped model:<tag>.")
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

    if args.allow_local_override:
        print("⚠ --allow-local-override is deprecated and ignored: the "
              "review tier decides what a model may approve (GOVERNANCE.md).")

    # Mode A: --apply-verdicts — read a worksheet, apply the verdicts.
    # No selector needed; drafts come from the worksheet itself.
    if args.apply_verdicts is not None:
        if not args.apply_verdicts.exists():
            print(f"❌ worksheet not found: {args.apply_verdicts}")
            return 2
        if not args.reviewer:
            p.error("--apply-verdicts requires --reviewer human:<name>")
        from promote import normalize_reviewer
        try:
            args.reviewer = normalize_reviewer(args.reviewer)
        except ValueError as e:
            p.error(str(e))
        if args.reviewer.startswith("model:"):
            p.error("worksheet verdicts are a person's; use --llm-review "
                    "for a model review")
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
        note = ("off (--no-model-approve)" if args.no_model_approve
                else "Tier A only; Tier B always goes to a person")
        print(f"  votes={args.votes}  ·  model approval: {note}")

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
        model_approve=not args.no_model_approve,
    )
    return 0 if summary["n_failed_promote"] == 0 else 1


if __name__ == "__main__":
    sys.exit(_cli())
