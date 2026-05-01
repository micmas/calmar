"""
extract.py — extract aphasia-KB findings from one or more papers.

Reads a PDF, calls the Anthropic API with EXTRACTION_SKILL.md +
schema.md + the paper text as the prompt, and saves the resulting
draft entries to aphasia-kb/drafts/. Then runs annotate_paper.py
and appends to extraction_log.md.

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
1. ANTHROPIC_API_KEY environment variable set:
       export ANTHROPIC_API_KEY="sk-ant-..."
   Get a key from https://console.anthropic.com → API Keys.

2. Python deps (`pip install -r requirements.txt` covers them):
       anthropic, pymupdf, pyyaml, nibabel (for the loader import)

Cost (approximate, May 2026 pricing)
-------------------------------------
Per typical 20-page paper with the default model (claude-sonnet-4-6):
  ~45K input + ~15K output tokens  ≈  $0.35–0.50 per paper.

Use --model claude-haiku-4-5-20251001 for ~10x cheaper at lower quality.
Use --model claude-opus-4-6 for ~3x more expensive at highest quality.
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
  - Set `status: draft` and `created_by: agent:claude-extract-cli`
  - Set `created_on: <today's ISO date>`
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

# Paper

Citation key: {citation}
PDF filename: {pdf_filename}
Page count: {page_count}

{paper_text}
"""


def build_prompt(skill_md: str, schema_md: str, citations_md: str,
                 kb_summary: str, paper_text: str,
                 citation: str, pdf_filename: str,
                 page_count: int) -> str:
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
    ]:
        out = out.replace(key, val)
    return out


# ============================================================
# Anthropic API call
# ============================================================
def call_anthropic(prompt: str, model: str, max_tokens: int = 16000) -> str:
    """Send the prompt to Claude and return the raw response text."""
    try:
        from anthropic import Anthropic
    except ImportError as e:
        raise SystemExit(
            "anthropic Python SDK is required. Install with:\n"
            "    pip install anthropic"
        ) from e

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise SystemExit(
            "ANTHROPIC_API_KEY env var is not set.\n"
            "  Get a key from https://console.anthropic.com → API Keys.\n"
            "  Then:  export ANTHROPIC_API_KEY='sk-ant-...'"
        )

    client = Anthropic(api_key=api_key)
    print(f"  → Calling {model} ...")
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    # Concatenate text blocks
    parts = []
    for block in response.content:
        if hasattr(block, "text"):
            parts.append(block.text)
    raw = "".join(parts)
    print(f"  ← {response.usage.input_tokens} input + "
          f"{response.usage.output_tokens} output tokens "
          f"(stop_reason={response.stop_reason})")
    return raw


def parse_response(raw: str) -> dict:
    """Strip any leading/trailing prose around the JSON object and parse."""
    # Find the first { and the last matching } (greedy from start)
    start = raw.find("{")
    if start < 0:
        raise ValueError(f"No JSON object found in response. Raw:\n{raw[:500]}")
    # Try to parse from start; if fails, try to handle markdown code fences
    candidate = raw[start:]
    # Strip trailing markdown fences
    candidate = candidate.rstrip().rstrip("`").rstrip()
    # Try parsing progressively shorter substrings until valid JSON
    for end_offset in range(len(candidate), max(0, len(candidate) - 100), -1):
        try:
            return json.loads(candidate[:end_offset])
        except json.JSONDecodeError:
            continue
    # Last resort: full parse failure
    return json.loads(candidate)


# ============================================================
# Save + validate + post-process
# ============================================================
def save_drafts(drafts: list, kb_root: Path) -> list[Path]:
    saved = []
    for d in drafts:
        bucket = d["bucket"]
        if bucket not in ("regions", "impairments", "therapies", "predictors"):
            print(f"  ⚠ skipping draft with invalid bucket={bucket!r}")
            continue
        out = kb_root / "drafts" / bucket / d["filename"]
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(d["content"], encoding="utf-8")
        saved.append(out)
        print(f"  ✓ wrote {out.relative_to(kb_root)}")
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
                kb_root: Path, dry_run: bool) -> bool:
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
    citations = _load_text(kb_root / "citations.md")
    kb_summary = _existing_kb_summary(kb_root)

    prompt = build_prompt(skill, schema, citations, kb_summary,
                          paper_text, citation,
                          pdf_path.name, n_pages)
    print(f"  Prompt: {len(prompt):,} chars (~{len(prompt)//4:,} tokens)")

    if dry_run:
        out = kb_root / "_extraction_dry_run.txt"
        out.write_text(prompt, encoding="utf-8")
        print(f"  DRY RUN — wrote prompt to {out}")
        return True

    raw = call_anthropic(prompt, model)
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

    saved = save_drafts(drafts, kb_root)
    n_issues = validate_drafts(saved)
    if n_issues:
        print(f"  ⚠ {n_issues} validation issue(s) — drafts saved anyway "
              f"for review.")
    else:
        print(f"  ✓ {len(saved)} draft(s) validated clean.")

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
    p.add_argument("--model", default="claude-sonnet-4-6",
                   help="Anthropic model id (default: claude-sonnet-4-6). "
                        "claude-haiku-4-5-20251001 for cheap, "
                        "claude-opus-4-6 for highest quality.")
    p.add_argument("--dry-run", action="store_true",
                   help="Build the prompt but don't call the API. "
                        "Saves prompt to aphasia-kb/_extraction_dry_run.txt.")
    args = p.parse_args(argv)

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

    n_ok, n_fail = 0, 0
    for pdf in pdfs:
        try:
            ok = process_one(
                pdf, args.citation, args.model, kb_root, args.dry_run,
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
