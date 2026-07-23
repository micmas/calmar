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
from pathlib import Path

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
        import fitz  # PyMuPDF
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
            m = re.match(r"^##\s+(@\S+)\s*$", line)
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


def _existing_kb_summary(kb_root: Path) -> str:
    """Build a compact list of region/impairment/therapy/predictor IDs
    already in the canonical folders, for the prompt."""
    parts = []
    for bucket in ("regions", "impairments", "therapies", "predictors"):
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
      "bucket": "regions" | "impairments" | "therapies" | "predictors",
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
  - Start with `---` and a YAML frontmatter block (schema_version: 2.3)
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
   to highlight the source PDF.

6. NEVER INVENT: statistics, sample sizes, citations, or effect
   directions. If the paper doesn't report it, use `not_reported`.

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
from ollama_client import (DEFAULT_HOST as DEFAULT_OLLAMA_HOST,  # noqa: E402
                           OllamaError, autosize_num_ctx, chat,
                           check_model_available, is_local)

# Which model to use lives in models.yaml, not here — see model_config.py.
_EXTRACT_CFG = resolve_model("extract")
DEFAULT_MODEL = _EXTRACT_CFG["model"]
DEFAULT_MAX_TOKENS = _EXTRACT_CFG["max_tokens"]
NUM_CTX_FLOOR = 16384   # extraction prompts are always large


def _autosize_num_ctx(prompt: str, max_tokens: int) -> int:
    return autosize_num_ctx(prompt, max_tokens, floor=NUM_CTX_FLOOR)


def call_ollama(prompt: str, model: str, max_tokens: int = 16000,
                host: str = DEFAULT_OLLAMA_HOST,
                num_ctx: int | None = None,
                timeout: int = 3600, monitor: bool = True) -> str:
    """Send the prompt to a local Ollama model, return raw response text.

    Wraps the (long, blocking) call in a background GPU/CPU monitor so a
    CPU spill shows up as it happens rather than as unexplained slowness.
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
    except OllamaError as e:
        raise SystemExit(str(e)) from e
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


def save_drafts(drafts: list, kb_root: Path,
                created_by: str = "agent:local-extract-cli") -> list[Path]:
    saved = []
    for d in drafts:
        bucket = d["bucket"]
        if bucket not in ("regions", "impairments", "therapies", "predictors"):
            print(f"  ⚠ skipping draft with invalid bucket={bucket!r}")
            continue
        out = kb_root / "drafts" / bucket / d["filename"]
        out.parent.mkdir(parents=True, exist_ok=True)
        content, notes = _repair_frontmatter(d["content"], created_by)
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
        fm, _ = parse_markdown(p)
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
                lean: bool = False) -> bool:
    print(f"\n=== {pdf_path.name} ===")
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

    raw = call_ollama(prompt, model, max_tokens=max_tokens,
                      host=host, num_ctx=num_ctx, monitor=monitor,
                      timeout=timeout)
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
                        created_by=f"agent:ollama-extract-cli/{model}")
    n_issues = validate_drafts(saved)
    if n_issues:
        print(f"  ⚠ {n_issues} validation issue(s) — drafts saved anyway "
              f"for review.")
    else:
        print(f"  ✓ {len(saved)} draft(s) validated clean.")

    if out_dir is not None:
        print(f"  ⊙ sandbox mode: skipped annotator + extraction_log "
              f"(nothing outside {out_dir.name}/ was modified)")
        return True

    run_annotator(pdf_path, saved, kb_root)
    log_line = result.get("extraction_log_line") or (
        f"{dt.date.today():%Y-%m-%d} | EXTRACTED | {citation} | "
        f"{','.join(d['filename'] for d in drafts)} | "
        f"{len(saved)} draft(s) | model: {model}"
    )
    append_extraction_log(kb_root / "extraction_log.md", log_line)
    print(f"  Summary: {result.get('summary', '(no summary)')}")
    notes = result.get("notes_for_reviewer")
    if notes:
        print(f"  For reviewer: {notes}")
    return True


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
            args.ollama_host, name_filter="gemma", purpose="extraction")
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
        # Build set of citation keys for which drafts (or canonical
        # entries) already exist — same convention as the file naming.
        existing_keys = set()
        for d in list((kb_root / "drafts").rglob("*.md")) \
               + list((kb_root / "regions").glob("*.md")) \
               + list((kb_root / "impairments").glob("*.md")) \
               + list((kb_root / "therapies").glob("*.md")) \
               + list((kb_root / "predictors").glob("*.md")):
            # Filename pattern: <id>__<citation_key_no_at>.md
            m = re.match(r".+__(.+)\.md$", d.name)
            if m:
                existing_keys.add("@" + m.group(1))

        for pdf in sorted((kb_root / "papers").glob("*.pdf")):
            # Skip the annotator's own outputs
            if pdf.stem.endswith("_annotated"):
                continue

            cit = _infer_citation_key(pdf, existing_keys=existing_keys)
            annotated = pdf.with_name(f"{pdf.stem}_annotated.pdf")

            if cit in existing_keys:
                print(f"  ⏭  {pdf.name}  "
                      f"(drafts already exist for {cit})")
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

    n_ok, n_fail = 0, 0
    for pdf in pdfs:
        try:
            ok = process_one(
                pdf, args.citation, args.model, kb_root, args.dry_run,
                host=args.ollama_host, num_ctx=args.num_ctx,
                max_tokens=args.max_tokens, out_dir=args.out_dir,
                monitor=not args.no_monitor, timeout=args.timeout,
                lean=args.lean,
            )
            if ok:
                n_ok += 1
            else:
                n_fail += 1
        except Exception as e:
            print(f"  ❌ unhandled error: {e}")
            n_fail += 1

    print(f"\nFinished: {n_ok} ok, {n_fail} failed.")
    if not args.dry_run and n_ok > 0:
        print(f"Review with: cd {kb_root} && python promote.py --list")


if __name__ == "__main__":
    main()
