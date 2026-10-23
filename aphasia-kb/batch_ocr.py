"""batch_ocr.py — walk papers/ and OCR any image-only PDFs in place.

Detects PDFs whose leading pages are scans — little or no text in the
text layer, or a page that is one big image with only a stamped line
of text on it (ProQuest puts "Reproduced with permission…" on every
page of a scan) — runs `ocrmypdf --skip-text` on each, and writes the
searchable result back to the same filename. The original is moved to
papers/_originals/ first (papers/ is not under version control).

Needs ocrmypdf with its engines. Simplest is the system package, which
brings Tesseract and Ghostscript with it and works from any venv:
macOS `brew install ocrmypdf`; Debian/Ubuntu `apt install ocrmypdf`.
`pip install ocrmypdf` in the venv also works if tesseract and gs are
on PATH. The script checks before touching anything. Detection itself
uses PyMuPDF only.

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
  comfortably above the noise floor. Independently of the threshold, a
  probed page is a scan when an image covers at least half of it and
  it carries fewer than 400 characters; a PDF most of whose probed
  pages are scans is a candidate.

Skip rules:
  * filenames ending in `_annotated.pdf` — those are agent outputs
  * symlinks — leave them alone (they should be replaced by rename)
  * already-OCR'd PDFs (text length above threshold) — no-op

Outputs:
  * The OCR'd file replaces the original at the same path
  * The original is kept in papers/_originals/<name>
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


def _ocrmypdf_cmd() -> list[str] | None:
    """The ocrmypdf CLI if installed system-wide, else the module in
    this interpreter, else None."""
    exe = shutil.which("ocrmypdf")
    if exe:
        return [exe]
    try:
        import ocrmypdf  # noqa: F401
        return [sys.executable, "-m", "ocrmypdf"]
    except ImportError:
        return None


SCAN_COVERAGE = 0.5           # image area / page area that marks a scanned page
SCAN_MAX_CHARS = 400          # a scanned page may still carry a stamped line
MIN_OCR_CHARS = 1000          # fewer than this after OCR → retry with --force-ocr


def _open(pdf: Path):
    try:
        import pymupdf as fitz
    except ImportError:  # pragma: no cover
        import fitz
    return fitz.open(str(pdf))


def _image_coverage(page) -> float:
    area = page.rect.width * page.rect.height
    if not area:
        return 0.0
    cov = 0.0
    for im in page.get_images(full=True):
        for r in page.get_image_rects(im[0]):
            cov += r.width * r.height
    return cov / area


def probe(pdf: Path, n_pages: int = PROBE_PAGES) -> tuple[int, int, int]:
    """(chars, scanned_pages, probed_pages) over the first `n_pages`.
    chars is whitespace-stripped so "    \n   \n" doesn't inflate it;
    scanned_pages counts pages that are mostly one image with at most a
    stamped line of text. (-1, 0, 0) when the file cannot be read."""
    try:
        doc = _open(pdf)
    except Exception as e:  # noqa: BLE001
        print(f"  ⚠ probe failed for {pdf.name}: {e}")
        return (-1, 0, 0)
    try:
        chars = scanned = probed = 0
        for i in range(min(n_pages, doc.page_count)):
            page = doc[i]
            n = len("".join(page.get_text().split()))
            chars += n
            probed += 1
            if n < SCAN_MAX_CHARS and _image_coverage(page) >= SCAN_COVERAGE:
                scanned += 1
        return (chars, scanned, probed)
    finally:
        doc.close()


def text_density(pdf: Path, n_pages: int = PROBE_PAGES) -> int:
    """Character count of the text layer over the first `n_pages`."""
    return probe(pdf, n_pages)[0]


def is_candidate(pdf: Path, threshold: int) -> tuple[bool, int]:
    """Decide whether `pdf` should be OCR'd. Returns (yes, density)."""
    if pdf.is_symlink():
        return (False, -1)
    if pdf.name.endswith("_annotated.pdf"):
        return (False, -1)
    if pdf.suffix.lower() != ".pdf":
        return (False, -1)
    chars, scanned, probed = probe(pdf)
    if chars < 0:
        return (False, -1)
    thin = chars < threshold
    mostly_scans = probed > 0 and scanned * 2 > probed
    return (thin or mostly_scans, chars)


def missing_tools() -> list[str]:
    """Install hints for whatever OCR needs and is not there."""
    out = []
    if _ocrmypdf_cmd() is None:
        out.append("ocrmypdf:  macOS `brew install ocrmypdf`, Debian `apt install ocrmypdf` "
                   "(or `pip install ocrmypdf` in the venv)")
    if not shutil.which("tesseract"):
        out.append("tesseract:  macOS `brew install tesseract`, Debian `apt install tesseract-ocr`")
    if not shutil.which("gs"):
        out.append("ghostscript:  macOS `brew install ghostscript`, Debian `apt install ghostscript`")
    return out


def run_ocrmypdf(src: Path, dry_run: bool, *, force_ocr: bool = False) -> str:
    """OCR `src` in place. Returns one-line status string."""
    if dry_run:
        return f"  WOULD OCR  {src.name}"
    # ocrmypdf can't write back to the same path while reading, so use a tmp.
    tmp = src.with_suffix(".pdf.ocr-tmp")
    cmd = (_ocrmypdf_cmd() or ["ocrmypdf"]) + [
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
    # Keep the original, then put the OCR'd file at the original path
    try:
        originals = src.parent / "_originals"
        originals.mkdir(exist_ok=True)
        backup = originals / src.name
        if not backup.exists():
            src.rename(backup)
        tmp.replace(src)
    except OSError as e:
        tmp.unlink(missing_ok=True)
        return f"  ✗ REPLACE  {src.name}: {e}"
    new_density = text_density(src)
    # --skip-text leaves a page alone when it has ANY text, so a scan
    # with a stamped permission line comes back unchanged. Redo it with
    # --force-ocr, which rasterises the page and OCRs all of it.
    if not force_ocr and new_density < MIN_OCR_CHARS:
        return run_ocrmypdf(src, dry_run=False, force_ocr=True)
    forced = ", forced" if force_ocr else ""
    return f"  ✓ OCR'd    {src.name}  ({new_density} chars searchable{forced})"


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
    p.add_argument("--all", action="store_true",
                   help="Also probe papers that already have findings (skipped by default: "
                        "a paper that was extracted has a text layer)")
    args = p.parse_args(argv)

    papers = args.papers_dir
    if not papers.is_dir():
        p.error(f"papers dir not found: {papers}")

    pdfs = sorted(f for f in papers.glob("*.pdf") if not f.stem.endswith("_annotated"))
    n_done = 0
    if not args.all:
        try:
            from extract import _extracted_citation_keys
            done = {k.lstrip("@").lower() for k in _extracted_citation_keys(Path(__file__).resolve().parent)}
        except Exception:  # noqa: BLE001 — without the KB, probe everything
            done = set()
        n_done = sum(f.stem.lower() in done for f in pdfs)
        pdfs = [f for f in pdfs if f.stem.lower() not in done]
    print(f"Scanning {len(pdfs)} PDF(s) in {papers}"
          + (f"  ({n_done} already extracted, skipped; --all to include them)" if n_done else "")
          + "\n"
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

    if args.execute:
        missing = missing_tools()
        if missing:
            print("Cannot OCR yet — missing:\n  " + "\n  ".join(missing))
            return 2

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
