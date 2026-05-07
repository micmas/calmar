"""batch_ocr.py — walk papers/ and OCR any image-only PDFs in place.

Detects PDFs whose `pdftotext` output is empty or near-empty (below a
character threshold), runs `ocrmypdf --skip-text` on each, and writes
the searchable result back to the same filename. The original is
overwritten on success — keep your repo under version control.

Usage:
    # See what would happen (default — safe to run any time):
    python batch_ocr.py

    # Actually OCR the candidates:
    python batch_ocr.py --execute

    # Tighter / looser threshold (default 200 chars in first 3 pages):
    python batch_ocr.py --execute --threshold 500

    # Limit to a subdirectory:
    python batch_ocr.py --papers-dir ../papers --execute

Why a threshold rather than zero?
  Some "image-only" PDFs have a few stray ASCII bytes from headers or
  watermarks (Elsevier sometimes embeds a single line of metadata text
  even on otherwise-scanned papers). 200 chars across the first three
  pages is well below any real article's first-page word count and
  comfortably above the noise floor.

Skip rules:
  * filenames ending in `_annotated.pdf` — those are agent outputs
  * symlinks — leave them alone (they should be replaced by rename)
  * already-OCR'd PDFs (text length above threshold) — no-op

Outputs:
  * The OCR'd file replaces the original at the same path
  * A backup is *not* taken — rely on git
  * Per-file results printed to stdout; final summary line for scripting
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_PAPERS_DIR = Path(__file__).resolve().parent / "papers"
DEFAULT_THRESHOLD = 200       # chars in first 3 pages
PROBE_PAGES = 3               # number of pages to sample for text density
OCRMYPDF = shutil.which("ocrmypdf") or "python3 -m ocrmypdf"
PDFTOTEXT = shutil.which("pdftotext") or "pdftotext"


def text_density(pdf: Path, n_pages: int = PROBE_PAGES) -> int:
    """Return character count of `pdftotext` output for the first
    `n_pages` of `pdf`. 0 = no extractable text. Text is whitespace-
    stripped before counting so "    \n   \n" doesn't inflate the
    score."""
    try:
        out = subprocess.run(
            [PDFTOTEXT, "-f", "1", "-l", str(n_pages), str(pdf), "-"],
            capture_output=True, text=True, timeout=30,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"  ⚠ probe failed for {pdf.name}: {e}")
        return -1
    return len("".join(out.stdout.split()))


def is_candidate(pdf: Path, threshold: int) -> tuple[bool, int]:
    """Decide whether `pdf` should be OCR'd. Returns (yes, density)."""
    if pdf.is_symlink():
        return (False, -1)
    if pdf.name.endswith("_annotated.pdf"):
        return (False, -1)
    if pdf.suffix.lower() != ".pdf":
        return (False, -1)
    density = text_density(pdf)
    return (0 <= density < threshold, density)


def run_ocrmypdf(src: Path, dry_run: bool, *, force_ocr: bool = False) -> str:
    """OCR `src` in place. Returns one-line status string."""
    if dry_run:
        return f"  WOULD OCR  {src.name}"
    # ocrmypdf can't write back to the same path while reading, so use a tmp.
    tmp = src.with_suffix(".pdf.ocr-tmp")
    cmd = [
        sys.executable, "-m", "ocrmypdf",
        "--skip-text",                   # leave any existing text alone
        "--quiet",
    ]
    if force_ocr:
        cmd = [c for c in cmd if c != "--skip-text"]
        cmd.append("--force-ocr")
    cmd += [str(src), str(tmp)]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True,
                       timeout=600)
    except subprocess.CalledProcessError as e:
        # If --skip-text saw existing text it errors — retry once with force.
        if not force_ocr and "already has text" in (e.stderr or "").lower():
            tmp.unlink(missing_ok=True)
            return run_ocrmypdf(src, dry_run=False, force_ocr=True)
        tmp.unlink(missing_ok=True)
        return f"  ✗ ERROR    {src.name}: {e.stderr.strip().splitlines()[-1] if e.stderr else e}"
    except subprocess.TimeoutExpired:
        tmp.unlink(missing_ok=True)
        return f"  ✗ TIMEOUT  {src.name} (600s)"
    # Atomically replace the original
    try:
        tmp.replace(src)
    except OSError as e:
        tmp.unlink(missing_ok=True)
        return f"  ✗ REPLACE  {src.name}: {e}"
    new_density = text_density(src)
    return f"  ✓ OCR'd    {src.name}  ({new_density} chars searchable)"


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--papers-dir", type=Path, default=DEFAULT_PAPERS_DIR,
                   help=f"Directory to scan (default: {DEFAULT_PAPERS_DIR})")
    p.add_argument("--threshold", type=int, default=DEFAULT_THRESHOLD,
                   help=f"Char count below which a PDF is considered "
                        f"image-only (default: {DEFAULT_THRESHOLD})")
    p.add_argument("--execute", action="store_true",
                   help="Actually run ocrmypdf (default: dry-run)")
    p.add_argument("--limit", type=int, default=0,
                   help="Stop after OCR'ing N candidates (useful for testing)")
    args = p.parse_args(argv)

    papers = args.papers_dir
    if not papers.is_dir():
        p.error(f"papers dir not found: {papers}")

    pdfs = sorted(papers.glob("*.pdf"))
    print(f"Scanning {len(pdfs)} PDF(s) in {papers}\n"
          f"Threshold: {args.threshold} chars in first {PROBE_PAGES} pages\n"
          f"Mode: {'EXECUTE' if args.execute else 'DRY RUN'}\n")

    candidates: list[tuple[Path, int]] = []
    for pdf in pdfs:
        is_cand, density = is_candidate(pdf, args.threshold)
        if is_cand:
            candidates.append((pdf, density))

    if not candidates:
        print("No image-only candidates found. Nothing to do.")
        return 0

    print(f"Found {len(candidates)} candidate(s):")
    for pdf, density in candidates:
        print(f"  • {pdf.name}  ({density} chars)")
    print()

    if args.limit and len(candidates) > args.limit:
        print(f"--limit {args.limit} → only processing first {args.limit}")
        candidates = candidates[: args.limit]
        print()

    n_ok = n_err = 0
    for pdf, _ in candidates:
        result = run_ocrmypdf(pdf, dry_run=not args.execute)
        print(result)
        if result.startswith("  ✓") or result.startswith("  WOULD"):
            n_ok += 1
        elif result.startswith("  ✗"):
            n_err += 1

    print()
    if args.execute:
        print(f"=== Summary: {n_ok} OCR'd, {n_err} errors ===")
    else:
        print(f"=== Dry run: {n_ok} would be OCR'd. "
              f"Re-run with --execute to commit. ===")
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main())
