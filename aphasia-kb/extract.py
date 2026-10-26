"""
extract.py — extract aphasia-KB findings from one or more papers.

Reads a PDF, calls a LOCAL model via Ollama with EXTRACTION_SKILL.md +
schema.md + the paper text as the prompt, and saves the resulting
draft entries to aphasia-kb/drafts/. Then runs annotate_paper.py
and appends to extraction_log.md.

Paper full text never leaves this machine — all inference is local.

Usage
-----
    # one paper
    python aphasia-kb/extract.py --pdf aphasia-kb/papers/Foo2024.pdf

    # one paper, explicit citation key (auto-inferred from filename if omitted)
    python aphasia-kb/extract.py \
        --pdf aphasia-kb/papers/Foo2024.pdf \
        --citation '@Foo2024'

    # batch — every PDF in papers/ that doesn't already have drafts
    python aphasia-kb/extract.py --batch

    # explicit batch
    python aphasia-kb/extract.py --pdf papers/Foo2024.pdf papers/Bar2023.pdf

    # dry-run: print the prompt that would be sent (no API call)
    python aphasia-kb/extract.py --pdf papers/Foo2024.pdf --dry-run

Pre-requisites
--------------
1. Ollama running locally, with the model pulled:
       ollama serve            # usually already running as a service
       ollama pull gemma4:26b
   Override the endpoint with OLLAMA_HOST or --ollama-host
   (default: http://localhost:11434).

2. Python deps (`pip install -r requirements.txt` covers them):
       pymupdf, pyyaml, nibabel (for the loader import)
   No SDK needed — Ollama is called over plain HTTP via urllib.

Context window
--------------
A typical 20-page paper builds a ~45K-token prompt. Ollama silently
TRUNCATES anything past num_ctx, and its default is small — that
truncation is the #1 cause of "0 drafts returned". This script sizes
num_ctx from the actual prompt length (+ headroom) and passes it
explicitly. Override with --num-ctx. Large contexts cost RAM/VRAM:
roughly 1–2 GB per 32K tokens on a 26B model, on top of weights.

Cost
----
Zero marginal cost, but slow: expect several minutes per paper on
consumer hardware. Quality will be below a frontier model — budget for
more validation issues at the promote.py review step.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


# ============================================================
# Helpers
# ============================================================
def _load_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def _extract_pdf_text(pdf_path: Path) -> tuple[str, int]:
    """Return (full_text, page_count) for a PDF."""
    try:
        try:
            import pymupdf as fitz  # PyMuPDF >= 1.24
        except ImportError:  # pragma: no cover
            import fitz  # older PyMuPDF
    except ImportError as e:
        raise SystemExit(
            "PyMuPDF is required. Install with:\n"
            "    pip install pymupdf"
        ) from e
    doc = fitz.open(str(pdf_path))
    pages = []
    for i in range(doc.page_count):
        pages.append(f"\n=== PAGE {i+1} ===\n" + doc[i].get_text())
    text = "".join(pages)
    n_pages = doc.page_count
    doc.close()
    return text, n_pages


# Stop words skipped when picking a "topic" suffix from the title
_TITLE_STOPWORDS = {
    "the", "a", "an", "of", "in", "on", "at", "for", "with",
    "and", "or", "but", "to", "from", "by", "is", "as", "be",
    "are", "was", "were", "do", "does", "did", "this", "that",
    "these", "those", "there",
}


def _infer_citation_key(pdf_path: Path,
                        existing_keys: set[str] | None = None) -> str:
    """Infer @AuthorYearTopic from filenames like
    'Yourganov-2015-Predicting aphasia type from br.pdf'.

    Examples:
      Yourganov-2015-Predicting aphasia.pdf  →  @Yourganov2015Predicting
      Mirman2015.pdf                          →  @Mirman2015
      Hillis_2007_aphasia.pdf                →  @Hillis2007Aphasia

    If `existing_keys` is provided and the inferred key collides, append
    letter suffix (b, c, ...) until unique and print a warning.
    The first collision becomes <key>b (the "a" slot is implicit on the
    pre-existing entry so users can read both as "Foo2024a / Foo2024b").
    """
    stem = pdf_path.stem
    # The documented naming is papers/<Key>.pdf. If the stem IS an
    # existing key (case-insensitively), use that key exactly — never
    # re-infer it (which lower-cased "NounVerb" to "Nounverb") and never
    # treat it as a collision.
    if existing_keys:
        by_lower = {k.lstrip("@").lower(): k for k in existing_keys}
        hit = by_lower.get(stem.lower())
        if hit:
            return hit if hit.startswith("@") else f"@{hit}"
    m = re.match(r"^([A-Z][A-Za-z]+)[-_\s]?(\d{4})[-_\s]?(.*)", stem)
    if not m:
        # Last resort: full stem, no collision check possible
        return f"@{stem.replace(' ', '_')}"

    author, year, rest = m.group(1), m.group(2), m.group(3)

    # Find the first significant word in the rest of the filename
    topic = ""
    for raw in re.split(r"[-_\s]+", rest):
        w = re.sub(r"[^A-Za-z0-9]", "", raw)
        if not w:
            continue
        if w.lower() in _TITLE_STOPWORDS:
            continue
        topic = w[0].upper() + w[1:].lower()
        break

    base = f"@{author}{year}"
    key = f"{base}{topic}" if topic else base

    if existing_keys and key in existing_keys:
        # Collision — suffix with letter starting from b
        for suffix in "bcdefghijklmnopqrstuvwxyz":
            candidate = f"{key}{suffix}"
            if candidate not in existing_keys:
                print(f"  ⚠ citation key {key} already exists; "
                      f"using {candidate} instead.")
                return candidate
        # Out of letters? surreal but explicit
        return f"{key}_{len(existing_keys)}"

    return key


def _gather_existing_citation_keys(kb_root: Path) -> set[str]:
    """Scan citations.md and all draft / canonical entry filenames to
    build the set of citation keys already in use."""
    keys = set()
    cit = kb_root / "citations.md"
    if cit.exists():
        for line in cit.read_text().splitlines():
            m = re.match(r"^##\s+(@\S+)", line)      # "## @Key" or "## @Key  [status]"
            if m:
                keys.add(m.group(1))
    for d in list((kb_root / "drafts").rglob("*.md")) \
           + list((kb_root / "regions").glob("*.md")) \
           + list((kb_root / "impairments").glob("*.md")) \
           + list((kb_root / "therapies").glob("*.md")) \
           + list((kb_root / "predictors").glob("*.md")):
        m = re.match(r".+__(.+)\.md$", d.name)
        if m:
            keys.add("@" + m.group(1))
    return keys


def _citation_statuses(kb_root: Path) -> dict[str, str]:
    """@Key -> status tag from the `## @Key  [status]` headers of
    citations.md (extracted / cited / seed / refused …)."""
    out: dict[str, str] = {}
    cit = kb_root / "citations.md"
    if cit.exists():
        for line in cit.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^##\s+(@\S+)\s*(?:\[([\w\-]+)\])?", line)
            if m:
                out[m.group(1)] = (m.group(2) or "").lower()
    return out


MAX_BATCH_PAGES = 60   # --batch skips longer PDFs (monographs, 300-page HTA reports)

_CITATION_LINE = re.compile(r"^\s*citation:\s*['\"]?(@[\w\-]+)", re.M)


def _extracted_citation_keys(kb_root: Path) -> set[str]:
    """Citation keys that already have findings somewhere — in drafts/
    or in any canonical bucket — read from the `citation:` lines of the
    entries themselves, not from filenames (canonical entries are
    named by topic, e.g. regions/left_angular_gyrus.md, and one entry
    can cite many papers). This is what --batch must not re-extract."""
    keys: set[str] = set()
    folders = [kb_root / "drafts"] + [kb_root / b for b in
                                      ("regions", "impairments", "therapies",
                                       "predictors", "reviews", "ingredients")]
    for folder in folders:
        if not folder.is_dir():
            continue
        for md in folder.rglob("*.md"):
            try:
                keys.update(_CITATION_LINE.findall(md.read_text(encoding="utf-8")))
            except OSError:
                continue
    return keys


def _existing_kb_summary(kb_root: Path) -> str:
    """Build a compact list of region/impairment/therapy/predictor IDs
    already in the canonical folders, for the prompt."""
    parts = []
    for bucket in ("regions", "impairments", "therapies", "predictors", "reviews"):
        ids = []
        d = kb_root / bucket
        if d.is_dir():
            for f in sorted(d.glob("*.md")):
                # Read just the YAML frontmatter to get the id
                try:
                    text = f.read_text()
                    m = re.search(r"^id:\s*(\S+)", text, flags=re.MULTILINE)
                    if m:
                        ids.append(m.group(1))
                except Exception:
                    continue
        parts.append(f"{bucket}: " + ", ".join(ids) if ids else f"{bucket}: (none)")
    return "\n".join(parts)


# ============================================================
# Prompt construction
# ============================================================
PROMPT_HEADER = """You are an extraction agent for an aphasia knowledge base.

You read the paper below and produce one or more **draft KB entries**
under schema v2.3. Your output will be saved as markdown files in
`aphasia-kb/drafts/<bucket>/` for human review.

# Output format (REQUIRED)

Return a SINGLE JSON object matching this exact schema, with no
prose or markdown around it:

{
  "drafts": [
    {
      "bucket": "regions" | "impairments" | "therapies" | "predictors" | "reviews",
      "filename": "<entry_id>__<citation_key_no_at>.md",
      "content": "<full markdown including YAML frontmatter and prose body>"
    },
    ...
  ],
  "summary": "<one-line description of what was extracted>",
  "extraction_log_line": "<ISO date> | EXTRACTED | <citation> | <ids> | <details>",
  "notes_for_reviewer": "<anything you want the reviewer to pay extra attention to>"
}

Each draft's `content` field must:
  - Start with `---` and a YAML frontmatter block (schema_version: 2.7)
  - Contain at least one valid `findings` entry (or be empty if you're
    creating a new region/impairment/therapy/predictor entry without findings)
  - Set `status: draft`
  - Set `created_by: "agent"` and `created_on: 2026-01-01` — these are
    placeholders and are overwritten automatically after you respond, so
    do not try to reproduce any long identifier here.
  - Use ONLY straight quotes (" and ') — never curly/smart quotes
    (" " ' '). A single curly quote makes the YAML unparseable.
  - Include verbatim `source_passages` with the `supports` tag for
    each finding
  - For predictor drafts: declare `kind: predictor` and a
    `predictor_type` of `behavioural` / `demographic` / `clinical`
    / `imaging_metric`. See EXTRACTION_SKILL.md §1b for when to use
    a predictor entry vs. a region/impairment/therapy entry.

# Workflow rules (read carefully)

The complete workflow is in EXTRACTION_SKILL.md (below). Key rules:

1. ANCHOR PERSPECTIVE: write region-anchored drafts when the paper
   makes region-tied claims (the typical case). Only spawn impairment-
   or therapy-anchored drafts when the claim isn't tied to a specific
   region.

2. EXISTING IDS: prefer adding findings to entries that already exist
   in the KB (listed below). If you must reference a region/impairment/
   therapy that isn't in the KB, use a sensible new id and flag it in
   `provenance.flags` so the reviewer knows to add it.

3. CITATION: the paper's citation key is provided below. Add a citation
   to citations.md only if it doesn't exist there yet — but DO include
   the key in every finding's `citation` field.

4. CONFIDENCE: be honest. `provenance.confidence: high` only when you
   have the full paper and understood the section end-to-end. Use
   `medium` for inferred fields, `low` for abstract-only or major
   ambiguity. Add specific flags in `provenance.flags`.

5. SOURCE PASSAGES: every finding needs verbatim quotes (1-3 sentences
   each) tagged with their `supports` field. The annotator uses these
   to highlight the source PDF, so a quote must be a run of sentences
   copied exactly from the paper's prose — never a table row, a figure
   caption cell, or values joined with "|". If a number lives only in a
   table, quote the results sentence that refers to the table (e.g.
   "Posterior STG was the strongest predictor of sentence comprehension
   (Table 3)") and put the number itself in the `statistics` fields.
   A finding with no prose passage for its claim is not extractable.
   Aim for one passage per aspect the finding uses: claim, sample,
   method, statistics, and the authors' own limitation.

6. NEVER INVENT: statistics, sample sizes, citations, or effect
   directions. If the paper doesn't report it, use `not_reported`.

7. AUTHOR LIMITATIONS: `author_limitations` is required on every
   finding. Fill it from the authors' own stated caveats (usually the
   Discussion's limitations paragraph) and quote one of them with
   `supports: limitation`. Write `[]` only if the paper states none.

8. RECOVERY PHASE: `sample.phase` is required on every finding with a
   patient sample (schema v2.6). Use the Stroke Recovery and
   Rehabilitation Roundtable bands, from the time post-onset the paper
   reports: hyperacute (0–24 h), acute (1–7 days), early_subacute
   (7 days–3 months), late_subacute (3–6 months), chronic (> 6 months);
   mixed when the sample straddles bands with no dominant one;
   longitudinal when the same patients were measured in two or more
   phases; not_reported when the paper does not say. Keep the paper's
   own wording in `sample.time_post_onset` as well.

9. LESION-MAPPING DESIGN (schema v2.7): every finding whose method is
   LSM, VLSM, RLSM, MLPA, VBCM, lesion_network_mapping or disconnectome
   needs a `lesion_mapping` block, read from the Methods:
     analysis: univariate | multivariate | region_based | network | not_reported
     n_analysed: the number of patients in THIS analysis (int) or not_reported
     min_lesion_overlap: e.g. ">= 5 patients" or not_reported
     lesion_volume_correction: direct (direct total lesion volume control,
       dTLVC) | covariate (volume entered as a covariate / regressed out) |
       none (the paper says it was not controlled) | not_reported
     multiple_comparisons: permutation_fwe | fwe | cluster_fwe | fdr |
       bonferroni | uncorrected | not_reported
   Quote the sentence that states the correction or the volume control
   with `supports: method` or `statistics`. Never guess: use
   not_reported when the paper does not say.
   `sample.cohort`: when the patients come from a named, reused dataset
   (Aphasia Recovery Cohort "ARC", "PLORAS", "OCS", a trial ID such as
   "NCT01927302"), name it; otherwise leave it out.

# Existing KB entries you can target

{kb_summary}

# Citations already defined

{citations}

# EXTRACTION_SKILL.md

{skill}

# schema.md

{schema}

{vocab_checklist}

# Paper

Citation key: {citation}
PDF filename: {pdf_filename}
Page count: {page_count}

{paper_text}
"""


def _vocab_checklist() -> str:
    """Build a compact controlled-vocabulary crib sheet from the validator.

    The vocabularies already appear in schema.md, but by the time a
    mid-size model has read an 800-line skill file plus a full paper,
    they're long out of attention — gemma4 wrote `method: CT` (an
    imaging modality) where the vocab wants `LSM`, on every single
    draft. Restating them immediately before the output spec fixes that
    class of error.

    Generated from aphasia_kb's constants rather than hardcoded, so it
    can never drift from what the validator actually enforces.
    """
    try:
        import aphasia_kb as K
    except ImportError:
        return ""

    def fmt(name: str) -> str:
        v = getattr(K, name, None)
        return " | ".join(sorted(v)) if v else "(unavailable)"

    return f"""
# Controlled vocabularies — EXACT values only

Any other value is rejected by the validator. Do not invent or
abbreviate. If nothing fits, omit the optional field rather than
guessing.

  strength:         {fmt('STRENGTH_VOCAB')}
  direction:        {fmt('DIRECTION_VOCAB')}
  evidence_quality: {fmt('EVIDENCE_VOCAB')}
  confidence:       {fmt('CONFIDENCE_VOCAB')}
  target_kind:      {fmt('TARGET_KIND_VOCAB')}
  relationship:     {fmt('RELATIONSHIP_VOCAB')}
  design:           {fmt('DESIGN_VOCAB')}
  supports:         {fmt('SUPPORTS_VOCAB')}
  method:           {fmt('METHOD_VOCAB')}
  imaging:          {fmt('IMAGING_VOCAB')}

NOTE `method` vs `imaging`: `method` is the ANALYSIS (e.g. LSM, VLSM,
tractography). `imaging` is the SCANNER modality (e.g. CT, MRI). A CT-
based lesion-symptom study is method: LSM, imaging: CT — never
method: CT.

# Required fields — every draft needs all of these

File level:  schema_version, id, name, kind, status, created_by,
             created_on, findings
Each finding: id, target, target_kind, claim, direction, relationship,
             citation, method, design, strength, evidence_quality,
             sample.n, source_passages, provenance
Each provenance block: extracted_by, extracted_on, paper_section,
             confidence, flags   (flags may be an empty list [])

A draft missing any of these is auto-rejected, so it is better to emit
FEWER, COMPLETE drafts than many partial ones.
"""


def build_prompt(skill_md: str, schema_md: str, citations_md: str,
                 kb_summary: str, paper_text: str,
                 citation: str, pdf_filename: str,
                 page_count: int, created_by: str = "agent:local-extract-cli"
                 ) -> str:
    # Use simple string substitution — str.format() chokes on the
    # literal { } in the JSON example inside PROMPT_HEADER.
    out = PROMPT_HEADER
    for key, val in [
        ("{skill}", skill_md),
        ("{schema}", schema_md),
        ("{citations}", citations_md),
        ("{kb_summary}", kb_summary),
        ("{paper_text}", paper_text),
        ("{citation}", citation),
        ("{pdf_filename}", pdf_filename),
        ("{page_count}", str(page_count)),
        ("{created_by}", created_by),
        ("{vocab_checklist}", _vocab_checklist()),
    ]:
        out = out.replace(key, val)
    return out


# ============================================================
# Local inference via Ollama
# ============================================================
from model_config import resolve as resolve_model  # noqa: E402
from phase import PHASE_VOCAB, infer_phase  # noqa: E402
import lesion_mapping as _lesion_mapping  # noqa: E402  (v2.7)
from ollama_client import (DEFAULT_HOST as DEFAULT_OLLAMA_HOST,  # noqa: E402
                           OllamaError, RepetitionLoop, autosize_num_ctx, chat,
                           check_model_available, is_local)

# Which model to use lives in models.yaml, not here — see model_config.py.
_EXTRACT_CFG = resolve_model("extract")
DEFAULT_MODEL = _EXTRACT_CFG["model"]
DEFAULT_MAX_TOKENS = _EXTRACT_CFG["max_tokens"]
NUM_CTX_FLOOR = 16384   # extraction prompts are always large


def _autosize_num_ctx(prompt: str, max_tokens: int) -> int:
    return autosize_num_ctx(prompt, max_tokens, floor=NUM_CTX_FLOOR)


RETRY_HINT = """

IMPORTANT — SECOND ATTEMPT. Your previous response exceeded the output
budget and was discarded. This time: report only the findings that carry
a quantitative result or a direct region–impairment claim (at most 8),
give each at most 3 source_passages, keep every string short, and do
not repeat any object. Produce the complete JSON object."""

LOOP_HINT = """

IMPORTANT — SECOND ATTEMPT. Your previous response was cut off because
you started repeating the same finding or passage over and over. Each
finding, and each source passage, must appear EXACTLY ONCE. Report at
most 8 findings with at most 3 source_passages each, then close the
JSON object and stop."""


def _keep(kind: str, text: str) -> None:
    """Save a cut-off or looped response so the failure can be read."""
    dump = HERE / f"_last_extraction_response_{kind}_{dt.datetime.now():%H%M%S}.txt"
    try:
        dump.write_text(text, encoding="utf-8")
        print(f"  ⚠ {kind} output kept in {dump.name} ({len(text):,} chars)")
    except OSError:
        pass


def call_ollama(prompt: str, model: str, max_tokens: int = 16000,
                host: str = DEFAULT_OLLAMA_HOST,
                num_ctx: int | None = None,
                timeout: int = 3600, monitor: bool = True,
                _attempt: int = 1) -> str:
    """Send the prompt to a local Ollama model, return raw response text.

    Wraps the (long, blocking) call in a background GPU/CPU monitor so a
    CPU spill shows up as it happens rather than as unexplained slowness.

    The response is streamed (ollama_client.chat): a progress line every
    two minutes, and a repetition loop is cut after a few hundred wasted
    tokens. Two retry paths, each used once:
      * loop     → same budget, LOOP_HINT appended (it is a prompt problem)
      * overflow → 50 % larger budget, RETRY_HINT appended (be selective)
    Whatever was generated before a cut is kept in
    _last_extraction_response_{loop,overflow}_<time>.txt. A second
    failure raises OllamaError; the batch loop reports it and moves on.
    """
    if num_ctx is None:
        num_ctx = _autosize_num_ctx(prompt, max_tokens)

    mon_cm = None
    if monitor:
        try:
            from resource_monitor import ResourceMonitor
            mon_cm = ResourceMonitor(host, model, interval=5.0)
        except Exception:
            mon_cm = None

    try:
        if mon_cm is not None:
            with mon_cm:
                res = chat(prompt, model=model, max_tokens=max_tokens,
                           host=host, num_ctx=num_ctx, temperature=0.0,
                           fmt="json", timeout=timeout)
            print(f"  {mon_cm.summary()}")
        else:
            res = chat(prompt, model=model, max_tokens=max_tokens, host=host,
                       num_ctx=num_ctx, temperature=0.0, fmt="json",
                       timeout=timeout)
    except RepetitionLoop as e:
        # Caught by the streaming client after a few hundred wasted
        # tokens, not after the whole budget. Same budget, different
        # instruction: the loop is a prompt problem, not a length one.
        _keep("loop", e.partial)
        if _attempt == 1:
            print(f"  ↻ {e} — retrying once with a no-repetition instruction "
                  f"({dt.datetime.now():%H:%M:%S})", flush=True)
            return call_ollama(prompt + LOOP_HINT, model, max_tokens=max_tokens,
                               host=host, num_ctx=num_ctx, timeout=timeout,
                               monitor=monitor, _attempt=2)
        raise OllamaError(f"looped twice: {e}") from e
    except OllamaError as e:
        # A plain error, not SystemExit: in --batch the loop logs it and
        # continues with the next paper instead of dying.
        raise OllamaError(str(e)) from e
    if res.get("truncated_output"):
        # Genuinely long (the loop detector did not fire): keep what was
        # written, then once ask for a selective pass with a bigger budget.
        _keep("overflow", res["text"])
        if _attempt == 1:
            bigger = int(max_tokens * 1.5)
            print(f"  ↻ output was cut at {max_tokens:,} tokens without looping — "
                  f"retrying once with max_tokens={bigger:,} and a be-selective hint "
                  f"({dt.datetime.now():%H:%M:%S})", flush=True)
            return call_ollama(prompt + RETRY_HINT, model, max_tokens=bigger,
                               host=host, num_ctx=None, timeout=timeout,
                               monitor=monitor, _attempt=2)
        raise OllamaError(f"output still cut at {max_tokens:,} tokens on the second attempt")
    return res["text"]


def _dejson_strays(text: str) -> str:
    """Remove stray backslash line-continuations from a JSON envelope.

    Smaller models (seen on gemma4:12b-mlx) sometimes emit `},\\` then a
    newline between array elements — a backslash sitting OUTSIDE any
    string, which is invalid JSON and aborts the whole parse even though
    every draft is intact. We only strip backslashes that immediately
    precede a newline + structural char ({ [ ]), so escapes inside string
    values (\\n, \\", \\\\) are left alone.
    """
    return re.sub(r"\\+\s*\n(\s*[\{\[\]])", r"\n\1", text)


def parse_response(raw: str) -> dict:
    """Strip any leading/trailing prose around the JSON object and parse.

    Tries the raw text first; only applies the stray-backslash repair as
    a fallback, so a clean response from a well-behaved model is never
    touched.
    """
    start = raw.find("{")
    if start < 0:
        raise ValueError(f"No JSON object found in response. Raw:\n{raw[:500]}")

    for candidate in (raw[start:], _dejson_strays(raw[start:])):
        # Strip trailing markdown fences / prose.
        candidate = candidate.rstrip().rstrip("`").rstrip()
        # Try progressively shorter substrings until valid JSON.
        for end_offset in range(len(candidate),
                                max(0, len(candidate) - 100), -1):
            try:
                return json.loads(candidate[:end_offset])
            except json.JSONDecodeError:
                continue
    # Both attempts failed — raise on the repaired candidate for context.
    return json.loads(_dejson_strays(raw[start:]))


# ============================================================
# Save + validate + post-process
# ============================================================
_SMART_QUOTES = {
    "“": '"', "”": '"',   # curly double quotes
    "‘": "'", "’": "'",   # curly single quotes
    "″": '"', "′": "'",   # prime marks
}


def _repair_frontmatter(content: str, created_by: str) -> tuple[str, list[str]]:
    """Normalize the YAML-frontmatter mechanics that local models get
    wrong — differently on every run. Observed on gemma4:26b so far:

      * curly/smart quotes inside a value  → unterminated YAML string
      * abbreviating the long `created_by` we asked it to transcribe
      * omitting the CLOSING `---` fence entirely
      * ending flush at `---` with no trailing newline

    Any one of these makes the whole entry parse as "no frontmatter" and
    get discarded, so rather than trust the model to delimit the block,
    we re-derive the three parts (open fence / YAML / body) and rebuild a
    canonical `---\\n<yaml>\\n---\\n<body>\\n`. `created_by`/`created_on`
    are overwritten unconditionally: they're facts we know, and letting
    the code set them makes provenance trustworthy (the model can't
    misreport which model produced the draft).

    Returns (repaired_content, notes).
    """
    notes: list[str] = []

    if not content.lstrip().startswith("---"):
        return content, ["no leading --- ; left untouched"]

    # Strip the opening fence (first `---` line), whatever whitespace.
    m = re.match(r"^\s*---[ \t]*\n(.*)$", content, re.DOTALL)
    if not m:
        return content, ["malformed opening fence ; left untouched"]
    remainder = m.group(1)

    # Find the CLOSING fence: a line that is just `---`. If the model
    # never emitted one, treat the whole remainder as frontmatter.
    close = re.search(r"\n---[ \t]*(?:\n|$)", remainder)
    if close:
        fm_block = remainder[:close.start()]
        body = remainder[close.end():]
    else:
        fm_block = remainder.rstrip()
        body = ""
        notes.append("added missing closing ---")

    fixed = fm_block
    for bad, good in _SMART_QUOTES.items():
        if bad in fixed:
            fixed = fixed.replace(bad, good)
    if fixed != fm_block:
        notes.append("straightened smart quotes")

    # An indented `---` inside the YAML (seen 2026-10-22, Griffis2017:
    # between two findings) is never valid there; real fences start at
    # column 0. Drop it rather than lose the whole draft.
    unfenced = re.sub(r"(?m)^[ \t]+---[ \t]*\n", "", fixed)
    if unfenced != fixed:
        notes.append("removed a stray indented ---")
        fixed = unfenced
    # Same for a lone JSON brace left between findings (Lukic2017: "    },").
    unbraced = re.sub(r"(?m)^[ \t]+[{}],?[ \t]*\n", "", fixed)
    if unbraced != fixed:
        notes.append("removed a stray { or }")
        fixed = unbraced

    # Force-set created_by / created_on.
    today = dt.date.today().isoformat()
    if re.search(r"^created_by:.*$", fixed, re.MULTILINE):
        new = re.sub(r"^created_by:.*$", f'created_by: "{created_by}"',
                     fixed, count=1, flags=re.MULTILINE)
        if new != fixed:
            notes.append("rewrote created_by")
        fixed = new
    else:
        fixed = fixed.rstrip() + f'\ncreated_by: "{created_by}"'
        notes.append("inserted created_by")

    if re.search(r"^created_on:.*$", fixed, re.MULTILINE):
        fixed = re.sub(r"^created_on:.*$", f"created_on: {today}",
                       fixed, count=1, flags=re.MULTILINE)
    else:
        fixed = fixed.rstrip() + f"\ncreated_on: {today}"
        notes.append("inserted created_on")

    # Rebuild a canonical, always-parseable structure.
    out = f"---\n{fixed.strip()}\n---\n"
    if body.strip():
        out += body if body.endswith("\n") else body + "\n"
    return out, notes


_LIMITATIONS_FLAG = ("author_limitations not extracted by the model — "
                     "verify against the paper's limitations paragraph")


_LESIONMAP_FLAG = ("lesion_mapping (v2.7 design) not extracted by the model — "
                   "filled from statistics.threshold / confounders where the text says; "
                   "check the Methods")
_REFSPACE_FLAG = ("imaging_details.reference_space not extracted by the model — "
                  "set to not_reported; verify against the paper")
_NON_IMAGING = {"behavioral_only", "clinical_RCT", "meta-analysis",
                "computational_model", "narrative_review"}


def _canonical_entry(kb_root: Path | None, bucket: str, entry_id: str | None) -> dict:
    if not kb_root or not entry_id:
        return {}
    p = kb_root / bucket / f"{entry_id}.md"
    if not p.is_file():
        return {}
    m = re.match(r"^---\n(.*?)\n---", p.read_text(encoding="utf-8"), re.DOTALL)
    try:
        return yaml.safe_load(m.group(1)) or {} if m else {}
    except Exception:  # noqa: BLE001
        return {}


def _normalize_findings(content: str, bucket: str,
                        citation: str | None,
                        kb_root: Path | None = None) -> tuple[str, list[str]]:
    """Parse the repaired draft and fix the omissions a local model makes
    on nearly every draft, each one visibly:

      * `author_limitations` missing → set to [] AND add a provenance
        flag, so the draft validates but lands in Tier B for a person
        (an empty list without the flag would read as "the authors
        stated none", which is almost never true).
      * `region_definition` missing or without `kind` → `kind:
        not_reported` (the schema requires the block on every finding;
        a predictor or therapy finding simply has no region to define).
      * imaging method with no `imaging_details.reference_space` →
        `not_reported` plus a flag; `atlases_used` missing → [].
      * `citation` differing from the resolved key only in case → set
        to the resolved key, so promoted findings join citations.md.
      * entry-level predictor fields (`short_definition`,
        `predictor_type`, `units`, `direction_of_severity`) missing on a
        draft whose id already exists canonically → copied from the
        canonical entry, since promote.py merges the findings into it.

    Re-serialises the frontmatter through YAML; this is a draft, so the
    model's formatting is not worth preserving.
    """
    notes: list[str] = []
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", content, re.DOTALL)
    if not m:
        return content, notes
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except Exception as e:  # noqa: BLE001
        return content, [f"frontmatter not parseable ({e}); left as written"]
    body = m.group(2)
    changed = False
    # reviews/: one entry per review paper, id `<topic>__<Key>` like the
    # canonical ones — otherwise two reviews of the same topic (e.g. two
    # MIT reviews, both `melodic_intonation_therapy_review`) would be
    # merged into one entry on promotion
    if bucket == "reviews" and citation:
        key = citation.lstrip("@")
        if fm.get("id") and not str(fm["id"]).endswith(f"__{key}"):
            old_id = fm["id"]
            fm["id"] = f"{str(old_id).split('__')[0].removesuffix('_review')}__{key}"
            changed = True
            notes.append(f"review id {old_id} → {fm['id']} (one entry per review paper)")
    canon = _canonical_entry(kb_root, bucket, fm.get("id"))
    if canon:
        # the draft adds findings to an existing entry: promote.py merges
        # them into it, so the entry-level fields are the canonical ones
        # (a draft calling it "Melodic Intonation Therapy" next to the
        # canonical "Melodic Intonation Therapy (MIT)" showed as two)
        if canon.get("name") and fm.get("name") != canon["name"]:
            notes.append(f"name {fm.get('name')!r} → canonical {canon['name']!r}")
            fm["name"] = canon["name"]
            changed = True
        for key in ("short_definition", "predictor_type", "units", "direction_of_severity",
                    "short_description", "targets_impairments", "hemisphere"):
            if not fm.get(key) and canon.get(key):
                fm[key] = canon[key]
                changed = True
                notes.append(f"{key} copied from the canonical {fm.get('id')} entry")
    try:
        v27 = float(fm.get("schema_version") or 0) >= 2.7
    except (TypeError, ValueError):
        v27 = False
    for f in fm.get("findings") or []:
        if not isinstance(f, dict):
            continue
        if f.get("author_limitations") is None:
            f["author_limitations"] = []
            prov = f.setdefault("provenance", {})
            flags = prov.setdefault("flags", [])
            if _LIMITATIONS_FLAG not in flags:
                flags.append(_LIMITATIONS_FLAG)
            changed = True
            notes.append(f"{f.get('id')}: author_limitations missing → [] + flag")
        sample = f.get("sample")
        if isinstance(sample, dict) and sample.get("phase") not in PHASE_VOCAB:
            # v2.6: stated phase missing or off-vocabulary → infer it
            # deterministically from the paper's own time_post_onset
            inferred, basis = infer_phase(sample.get("time_post_onset"))
            bad = sample.get("phase")
            sample["phase"] = inferred
            changed = True
            notes.append(f"{f.get('id')}: sample.phase "
                         + (f"{bad!r} → " if bad else "")
                         + f"{inferred} ({basis})")
        if v27 and _lesion_mapping.is_lesion_mapping(f) \
                and not isinstance(f.get("lesion_mapping"), dict):
            # v2.7 draft without its required design block → what the
            # finding's own text supports, flagged. Older drafts are left
            # alone: the loader infers the design for them on read and
            # marks it `lm_source: inferred`.
            lm, _ = _lesion_mapping.finding_lesion_mapping(f)
            f["lesion_mapping"] = lm
            prov = f.setdefault("provenance", {})
            flags = prov.setdefault("flags", [])
            if _LESIONMAP_FLAG not in flags:
                flags.append(_LESIONMAP_FLAG)
            changed = True
            notes.append(f"{f.get('id')}: lesion_mapping inferred + flag")
        rd = f.get("region_definition")
        if f.get("method") != "narrative_review" and \
                (not isinstance(rd, dict) or not rd.get("kind")):
            f["region_definition"] = {"kind": "not_reported",
                                      **({k: v for k, v in rd.items() if k != "kind"}
                                         if isinstance(rd, dict) else {})}
            changed = True
            notes.append(f"{f.get('id')}: region_definition.kind → not_reported")
        methods = f.get("method")
        methods = methods if isinstance(methods, list) else [methods]
        if any(mm not in _NON_IMAGING for mm in methods if mm):
            img = f.get("imaging_details")
            if not isinstance(img, dict):
                img = {}
                f["imaging_details"] = img
            if img.get("reference_space") not in ("MNI152", "MNI305", "Talairach",
                                                  "native", "other", "not_reported"):
                img["reference_space"] = "not_reported"
                prov = f.setdefault("provenance", {})
                flags = prov.setdefault("flags", [])
                if _REFSPACE_FLAG not in flags:
                    flags.append(_REFSPACE_FLAG)
                changed = True
                notes.append(f"{f.get('id')}: reference_space → not_reported + flag")
            if "atlases_used" not in img:
                img["atlases_used"] = []
                changed = True
                notes.append(f"{f.get('id')}: atlases_used → []")
        if citation and isinstance(f.get("citation"), str) and \
                f["citation"] != citation and \
                f["citation"].lstrip("@").lower() == citation.lstrip("@").lower():
            f["citation"] = citation
            changed = True
            notes.append(f"{f.get('id')}: citation case → {citation}")
    if not changed:
        return content, notes
    fm_text = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True,
                             width=100)
    out = f"---\n{fm_text.rstrip()}\n---\n"
    if body.strip():
        out += body if body.endswith("\n") else body + "\n"
    return out, notes


def save_drafts(drafts: list, kb_root: Path,
                created_by: str = "agent:local-extract-cli",
                citation: str | None = None) -> list[Path]:
    saved = []
    for d in drafts:
        bucket = d["bucket"]
        if bucket not in ("regions", "impairments", "therapies", "predictors", "reviews"):
            print(f"  ⚠ skipping draft with invalid bucket={bucket!r}")
            continue
        out = kb_root / "drafts" / bucket / d["filename"]
        out.parent.mkdir(parents=True, exist_ok=True)
        content, notes = _repair_frontmatter(d["content"], created_by)
        content, more = _normalize_findings(content, bucket, citation, kb_root)
        notes.extend(more)
        out.write_text(content, encoding="utf-8")
        saved.append(out)
        suffix = f"   [{'; '.join(notes)}]" if notes else ""
        print(f"  ✓ wrote {out.relative_to(kb_root)}{suffix}")
    return saved


def validate_drafts(saved: list[Path]) -> int:
    """Return count of issues across all saved drafts."""
    try:
        from aphasia_kb import parse_markdown, _validate_v2_entry
    except ImportError:
        print("  ⚠ couldn't import aphasia_kb for validation; skipping")
        return 0
    total = 0
    for p in saved:
        try:
            fm, _ = parse_markdown(p)
        except Exception as e:  # noqa: BLE001 — one bad draft must not stop the paper
            print(f"  ⚠ {p.name}: frontmatter does not parse — fix by hand ({str(e).splitlines()[0]})")
            total += 1
            continue
        if not fm:
            print(f"  ⚠ {p.name}: no frontmatter")
            total += 1
            continue
        fm["_path"] = str(p)
        issues = []
        _validate_v2_entry(fm, str(p), issues)
        if issues:
            print(f"  ⚠ {p.name}: {len(issues)} validation issue(s):")
            for i in issues:
                print(f"      {i}")
            total += len(issues)
    return total


def run_annotator(pdf_path: Path, drafts: list[Path], kb_root: Path) -> bool:
    """Run annotate_paper.py on all drafts for this PDF."""
    if not drafts:
        return False
    cmd = ["python3", str(kb_root / "annotate_paper.py"),
           "--pdf", str(pdf_path),
           "--draft"] + [str(d) for d in drafts]
    print(f"  → annotator: {' '.join(cmd[:3])} ... ({len(drafts)} draft(s))")
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(res.stdout.strip().splitlines()[-1] if res.stdout else "(no output)")
    if res.returncode != 0:
        print(f"  ⚠ annotator returned {res.returncode}")
        print(res.stderr)
        return False
    return True


def append_extraction_log(log_path: Path, line: str):
    if not line:
        return
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(line.rstrip() + "\n")


# ============================================================
# Per-paper pipeline
# ============================================================
def process_one(pdf_path: Path, citation: str | None, model: str,
                kb_root: Path, dry_run: bool,
                host: str = DEFAULT_OLLAMA_HOST,
                num_ctx: int | None = None,
                max_tokens: int = 16000,
                out_dir: Path | None = None,
                monitor: bool = True,
                timeout: int = 3600,
                lean: bool = False,
                progress: tuple[int, int] | None = None) -> bool:
    t_start = time.monotonic()
    tag = f"[{progress[0]}/{progress[1]}]  " if progress else ""
    print(f"\n=== {tag}{pdf_path.name} ===  started {dt.datetime.now():%Y-%m-%d %H:%M:%S}")
    if not pdf_path.exists():
        print(f"  ❌ not found: {pdf_path}")
        return False
    paper_text, n_pages = _extract_pdf_text(pdf_path)
    print(f"  PDF: {n_pages} pages, ~{len(paper_text):,} chars extracted")

    if not citation:
        citation = _infer_citation_key(
            pdf_path, existing_keys=_gather_existing_citation_keys(kb_root),
        )
    print(f"  Citation key: {citation}")

    skill = _load_text(kb_root / "EXTRACTION_SKILL.md")
    schema = _load_text(kb_root / "schema.md")
    kb_summary = _existing_kb_summary(kb_root)

    # Lean mode drops the full bibliography (~11K tokens) from the prompt.
    # It exists so the model can reuse existing citation keys, but for a
    # single-paper CLI run the exact key is already passed explicitly
    # below, so the whole citations.md is near-pure overhead. Cutting it
    # lowers num_ctx, which is what pushes bigger models off the GPU.
    if lean:
        citations = ("(omitted — use exactly the citation key given in the "
                     "Paper section below for every finding's `citation`.)")
    else:
        citations = _load_text(kb_root / "citations.md")

    # Tag provenance with the actual local model, so QC can tell
    # locally-extracted drafts apart from earlier API-extracted ones.
    prompt = build_prompt(skill, schema, citations, kb_summary,
                          paper_text, citation,
                          pdf_path.name, n_pages,
                          created_by=f"agent:ollama-extract-cli/{model}")
    tag = "  [LEAN: citations.md dropped]" if lean else ""
    print(f"  Prompt: {len(prompt):,} chars (~{len(prompt)//4:,} tokens){tag}")

    if dry_run:
        out = kb_root / "_extraction_dry_run.txt"
        out.write_text(prompt, encoding="utf-8")
        print(f"  DRY RUN — wrote prompt to {out}")
        print(f"  Would use num_ctx="
              f"{num_ctx or _autosize_num_ctx(prompt, max_tokens):,}")
        return True

    t_model = time.monotonic()
    print(f"  Model call started {dt.datetime.now():%H:%M:%S} "
          f"({model}, num_ctx={num_ctx or 'auto'}); progress every 2 min, "
          f"loops cut early.", flush=True)
    raw = call_ollama(prompt, model, max_tokens=max_tokens,
                      host=host, num_ctx=num_ctx, monitor=monitor,
                      timeout=timeout)
    print(f"  Model call finished {dt.datetime.now():%H:%M:%S} "
          f"(took {_fmt_elapsed(time.monotonic() - t_model)})", flush=True)
    raw_path = kb_root / f"_last_extraction_response_{pdf_path.stem}.txt"
    raw_path.write_text(raw, encoding="utf-8")

    try:
        result = parse_response(raw)
    except Exception as e:
        print(f"  ❌ couldn't parse JSON response: {e}")
        print(f"  Raw response saved to {raw_path}")
        return False

    drafts = result.get("drafts") or []
    if not drafts:
        print("  ⚠ agent returned 0 drafts")
        print(f"  notes: {result.get('notes_for_reviewer', '(none)')}")
        return False

    # Sandbox mode: write everything under out_dir and touch nothing the
    # real pipeline depends on. Used for model comparison runs, where
    # re-extracting a paper you've already curated would otherwise
    # overwrite its annotated PDF and pollute the extraction log.
    #
    # Clear this paper's prior sandbox drafts first. Different runs (or
    # different models) name entries differently, so without this the
    # dir accumulates stale files and the comparison silently mixes runs.
    if out_dir is not None:
        cit_key = citation.lstrip("@")
        removed = 0
        for old in (out_dir / "drafts").rglob(f"*__{cit_key}.md"):
            old.unlink()
            removed += 1
        if removed:
            print(f"  ⊙ sandbox: cleared {removed} prior draft(s) for "
                  f"{citation}")

    saved = save_drafts(drafts, out_dir or kb_root,
                        created_by=f"agent:ollama-extract-cli/{model}",
                        citation=citation)
    n_issues = validate_drafts(saved)
    if n_issues:
        print(f"  ⚠ {n_issues} validation issue(s) — drafts saved anyway "
              f"for review.")
    else:
        print(f"  ✓ {len(saved)} draft(s) validated clean.")

    if out_dir is not None:
        print(f"  ⊙ sandbox mode: skipped annotator + extraction_log "
              f"(nothing outside {out_dir.name}/ was modified)")
        print(f"  Done {dt.datetime.now():%H:%M:%S} — total "
              f"{_fmt_elapsed(time.monotonic() - t_start)} for this paper{_left(progress)}")
        return True

    run_annotator(pdf_path, saved, kb_root)
    log_line = result.get("extraction_log_line") or (
        f"{dt.date.today():%Y-%m-%d} | EXTRACTED | {citation} | "
        f"{','.join(d['filename'] for d in drafts)} | "
        f"{len(saved)} draft(s) | model: {model}"
    )
    # The model has no clock: it writes whatever date it likes (the
    # 2026-10 batches all came back dated 2026-01-01). Stamp today's.
    today = f"{dt.date.today():%Y-%m-%d}"
    if re.match(r"^\s*\d{4}-\d{2}-\d{2}\s*\|", log_line):
        log_line = re.sub(r"^\s*\d{4}-\d{2}-\d{2}", today, log_line, count=1)
    else:
        log_line = f"{today} | {log_line.strip()}"
    append_extraction_log(kb_root / "extraction_log.md", log_line)
    print(f"  Summary: {result.get('summary', '(no summary)')}")
    notes = result.get("notes_for_reviewer")
    if notes:
        print(f"  For reviewer: {notes}")
    print(f"  Done {dt.datetime.now():%H:%M:%S} — total "
          f"{_fmt_elapsed(time.monotonic() - t_start)} for this paper{_left(progress)}")
    return True


def _left(progress: tuple[int, int] | None) -> str:
    """'; 3 paper(s) left' / '; batch complete' / '' for a single paper."""
    if not progress or progress[1] < 2:
        return ""
    n = progress[1] - progress[0]
    return f"; {n} paper(s) left in the batch" if n else "; batch complete"


def _fmt_elapsed(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h}h {m:02d}m {s:02d}s" if h else f"{m}m {s:02d}s"


# ============================================================
# Main
# ============================================================
def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--pdf", type=Path, nargs="*", default=[],
                   help="One or more PDF paths to extract from.")
    p.add_argument("--batch", action="store_true",
                   help="Process every PDF in aphasia-kb/papers/ that "
                        "doesn't already have a draft with its citation key.")
    p.add_argument("--citation", default=None,
                   help="Citation key (e.g. @Foo2024). Inferred from "
                        "filename if omitted; only used when --pdf is a "
                        "single file.")
    p.add_argument("--model", default=None,
                   help=f"Ollama model tag. Default comes from models.yaml "
                        f"(currently {DEFAULT_MODEL}). Run "
                        f"`python model_config.py` to see resolved config.")
    p.add_argument("--pick-model", action="store_true",
                   help="Interactively choose from your locally-pulled "
                        "gemma models before running (e.g. to A/B 12b vs "
                        "26b). Overrides --model for this run only.")
    p.add_argument("--no-monitor", action="store_true",
                   help="Disable the background GPU/CPU monitor.")
    p.add_argument("--timeout", type=int, default=3600, metavar="SECONDS",
                   help="Give up on the model after this many seconds "
                        "(default 3600 = 1 hour). Lower it (e.g. 900) when "
                        "testing a model that might hang, so a runaway "
                        "fails fast instead of eating an hour.")
    p.add_argument("--lean", action="store_true",
                   help="Drop the full citations.md bibliography (~11K "
                        "tokens) from the prompt. Lowers num_ctx, which "
                        "helps big models fit on the GPU and speeds every "
                        "run. The exact citation key is still passed "
                        "explicitly, so single-paper extraction is "
                        "unaffected in principle — A/B it to confirm.")
    p.add_argument("--ollama-host", default=DEFAULT_OLLAMA_HOST,
                   help=f"Ollama base URL (default: {DEFAULT_OLLAMA_HOST}). "
                        f"Also read from OLLAMA_HOST.")
    p.add_argument("--num-ctx", type=int, default=None,
                   help="Context window in tokens. Default: sized from the "
                        "prompt with headroom. Raise it if you see the "
                        "truncation warning; lower it if you run out of RAM.")
    p.add_argument("--max-tokens", type=int, default=None,
                   help=f"Max tokens to generate (num_predict). Default from "
                        f"models.yaml (currently {DEFAULT_MAX_TOKENS}).")
    p.add_argument("--out-dir", type=Path, default=None, metavar="DIR",
                   help="Sandbox mode: write drafts under DIR/drafts/ "
                        "instead of the real drafts/, and skip the "
                        "annotator and extraction_log. Use this to "
                        "re-extract an already-curated paper for model "
                        "comparison without damaging anything.")
    p.add_argument("--dry-run", action="store_true",
                   help="Build the prompt but don't call the model. "
                        "Saves prompt to aphasia-kb/_extraction_dry_run.txt.")
    args = p.parse_args(argv)

    # Interactive picker takes precedence over --model / config for this
    # run — handy for A/B-ing 12b vs 26b without editing anything.
    if args.pick_model:
        from model_config import pick_model_interactive
        picked = pick_model_interactive(
            args.ollama_host, name_filter=None, purpose="extraction")
        if picked:
            args.model = picked

    # Resolve model/limits through models.yaml so --model, the env vars,
    # and the config file all compose predictably.
    cfg = resolve_model("extract", args.model)
    args.model = cfg["model"]
    if args.max_tokens is None:
        args.max_tokens = cfg["max_tokens"]
    if args.num_ctx is None:
        args.num_ctx = cfg["num_ctx"]

    kb_root = HERE  # this script lives in aphasia-kb/

    pdfs = list(args.pdf)
    if args.batch:
        # Citation keys that already have findings, in drafts/ or in the
        # canonical folders — read from the entries' `citation:` lines.
        # (Until 2026-10 this read filenames only, which canonical
        # entries don't carry, so --batch would have re-extracted the
        # whole KB.)
        existing_keys = _extracted_citation_keys(kb_root)
        all_keys = existing_keys | _gather_existing_citation_keys(kb_root)
        statuses = _citation_statuses(kb_root)

        for pdf in sorted((kb_root / "papers").glob("*.pdf")):
            # Skip the annotator's own outputs
            if pdf.stem.endswith("_annotated"):
                continue

            cit = _infer_citation_key(pdf, existing_keys=all_keys)
            annotated = pdf.with_name(f"{pdf.stem}_annotated.pdf")

            if cit in existing_keys:
                print(f"  ⏭  {pdf.name}  "
                      f"(findings already exist for {cit})")
                continue
            if cit not in all_keys:
                # Never extract under a key made up from a download name:
                # drafts, log lines and the annotated PDF would all carry it.
                print(f"  ⏭  {pdf.name}  (no entry in citations.md — run "
                      f"intake_papers.py, which registers it from its DOI, or add a block)")
                continue
            if statuses.get(cit) == "refused":
                print(f"  ⏭  {pdf.name}  "
                      f"({cit} is [refused] in citations.md — change the tag to extract it)")
                continue
            try:
                import pymupdf as _fz
            except ImportError:  # pragma: no cover
                import fitz as _fz
            with _fz.open(str(pdf)) as _d:
                n_pg = _d.page_count
            if n_pg > MAX_BATCH_PAGES:
                print(f"  ⏭  {pdf.name}  ({n_pg} pages > {MAX_BATCH_PAGES}; too long for one "
                      f"pass — run it alone with --pdf after trimming to the relevant sections)")
                continue
            if annotated.exists():
                print(f"  ⏭  {pdf.name}  "
                      f"(annotated PDF exists at {annotated.name} — "
                      f"delete it to re-extract)")
                continue
            pdfs.append(pdf)

    if not pdfs:
        p.error("No PDFs to process. Pass --pdf <path> or --batch.")

    if len(pdfs) > 1 and args.citation:
        p.error("--citation only valid for a single PDF.")

    # Preflight: fail in 2 seconds, not on paper 1 of 40.
    if not args.dry_run:
        if not is_local(args.ollama_host):
            print(f"⚠ OLLAMA_HOST points at {args.ollama_host}, which is not "
                  f"this machine.\n"
                  f"  Paper text WILL leave your computer. Ctrl-C now if "
                  f"that's not what you want.")
        ok, msg = check_model_available(args.model, args.ollama_host)
        if not ok:
            p.error(msg)
        print(f"✓ {msg}  (model from {cfg['source']})")

    t_batch = time.monotonic()
    n_ok, n_fail = 0, 0
    if len(pdfs) > 1:
        print(f"\n{len(pdfs)} paper(s) to extract, in this order: "
              + ", ".join(p.stem for p in pdfs))
    for i, pdf in enumerate(pdfs, 1):
        try:
            ok = process_one(
                pdf, args.citation, args.model, kb_root, args.dry_run,
                host=args.ollama_host, num_ctx=args.num_ctx,
                max_tokens=args.max_tokens, out_dir=args.out_dir,
                monitor=not args.no_monitor, timeout=args.timeout,
                lean=args.lean, progress=(i, len(pdfs)),
            )
            if ok:
                n_ok += 1
            else:
                n_fail += 1
        except OllamaError as e:
            print(f"  ❌ {pdf.name}: {e}")
            n_fail += 1
        except Exception as e:
            print(f"  ❌ unhandled error: {e}")
            n_fail += 1

    print(f"\nFinished {dt.datetime.now():%Y-%m-%d %H:%M:%S}: {n_ok} ok, "
          f"{n_fail} failed, {_fmt_elapsed(time.monotonic() - t_batch)} total.")
    if not args.dry_run and n_ok > 0:
        print(f"Review with: cd {kb_root} && python promote.py --list")


if __name__ == "__main__":
    main()
