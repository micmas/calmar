#!/usr/bin/env python3
"""
strip_cover_pages.py — remove publisher cover sheets from PDFs in papers/.

Downloads often arrive with a page in front of the article that is not
part of it: the JSTOR "Source / Stable URL" sheet, the AJNR / HighWire
"This information is current as of …" page, Taylor & Francis'
"Full Terms & Conditions of access and use", ProQuest's "Reproduced
with permission of the copyright owner", ResearchGate's "See
discussions, stats, and author profiles", Elsevier's "Provided for
non-commercial research and education use". They are noise for the
extractor (it labels pages by PDF index, so every `page` it reports is
off by one), they get OCR'd for nothing, and they confuse the quote
check on short papers.

    python strip_cover_pages.py                 # dry run over papers/
    python strip_cover_pages.py --execute       # strip; originals kept
    python strip_cover_pages.py papers/Foo2024.pdf --pages 2 --execute
                                                # force: drop 2 leading pages

Detection is by text pattern on the leading page(s), never by length
alone, so a real first page is not removed. A page that is mostly one
image (a scan) is never a cover sheet, even when the scanner stamped a
permission line on it. Up to MAX_COVER leading pages are checked in
turn. `--pages N` overrides detection for the files
named on the command line.

With --execute the original is moved to papers/_originals/<name> and
the stripped PDF written at the original path. Nothing is deleted.
Annotated copies (`<Key>_annotated.pdf`) of a stripped paper are stale
afterwards and are listed; regenerate them with annotate_paper.py.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MAX_COVER = 3

# Each pattern is searched case-insensitively in the page's text layer.
# A page is a cover sheet when any ONE of these hits. Keep them specific
# to the sheet, not to the article: "downloaded from" alone appears in
# running footers of real pages.
COVER_PATTERNS: tuple[tuple[str, str], ...] = (
    ("JSTOR", r"stable url|jstor is a not-for-profit|accessed:\s*\d"),
    ("HighWire/AJNR", r"this information is current as"),
    ("Taylor & Francis", r"full terms (&|and) conditions of access and use"),
    ("ProQuest", r"reproduced with permission of the copyright owner"),
    ("ResearchGate", r"see discussions, stats, and author profiles"),
    ("Elsevier author copy", r"provided for non-commercial research and education use"),
    ("Springer author copy", r"your article is protected by copyright"),
    ("ClinicalKey", r"downloaded for .+ at .+ from clinicalkey"),
    ("Wiley", r"terms and conditions \(https://onlinelibrary\.wiley\.com/terms"),
    ("SAGE", r"article reuse guidelines:\s*sagepub\.com/journals-permissions\s*$"),
    ("Cover sheet", r"^\s*(this article was downloaded by|downloaded by:)\s*\["),
)
_COMPILED = [(name, re.compile(p, re.I | re.M)) for name, p in COVER_PATTERNS]


def _open(path: Path):
    try:
        import pymupdf as fitz
    except ImportError:  # pragma: no cover
        import fitz
    return fitz.open(str(path))


SCAN_COVERAGE = 0.5   # image area / page area above which a page is a scan


def _image_coverage(page) -> float:
    area = page.rect.width * page.rect.height
    if not area:
        return 0.0
    cov = 0.0
    for im in page.get_images(full=True):
        for r in page.get_image_rects(im[0]):
            cov += r.width * r.height
    return cov / area


def cover_reason(text: str, page=None) -> str | None:
    """Name of the publisher sheet this page looks like, or None."""
    t = " ".join(text.split())
    if not t:
        return None               # image-only page: cannot tell, keep it
    if page is not None and _image_coverage(page) >= SCAN_COVERAGE:
        return None               # a scanned article page, whatever is stamped on it
    for name, rx in _COMPILED:
        if rx.search(t):
            # SAGE's permission line also appears on real first pages;
            # only call it a sheet when the page is otherwise empty
            if name == "SAGE" and len(t) > 600:
                continue
            return name
    return None


def leading_covers(path: Path) -> list[tuple[int, str]]:
    """[(page_index, reason), ...] for consecutive cover pages at the front."""
    doc = _open(path)
    try:
        out = []
        for i in range(min(MAX_COVER, doc.page_count - 1)):   # never all pages
            why = cover_reason(doc[i].get_text(), doc[i])
            if not why:
                break
            out.append((i, why))
        return out
    finally:
        doc.close()


def strip(path: Path, n: int, originals_dir: Path) -> Path:
    """Drop the first n pages of path; original moved to originals_dir."""
    originals_dir.mkdir(exist_ok=True)
    backup = originals_dir / path.name
    if backup.exists():
        raise FileExistsError(f"{backup} already exists — not overwriting")
    doc = _open(path)
    try:
        if n >= doc.page_count:
            raise ValueError(f"{path.name}: would remove every page")
        doc.delete_pages(list(range(n)))
        tmp = path.with_suffix(".stripped.tmp.pdf")
        doc.save(str(tmp), garbage=3, deflate=True)
    finally:
        doc.close()
    path.rename(backup)
    tmp.rename(path)
    return backup


def _cli(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("files", nargs="*", type=Path,
                    help="PDFs to check (default: every PDF in --papers-dir)")
    ap.add_argument("--papers-dir", type=Path, default=ROOT / "papers")
    ap.add_argument("--pages", type=int,
                    help="with explicit files: drop this many leading pages, no detection")
    ap.add_argument("--execute", action="store_true", help="actually strip")
    args = ap.parse_args(argv)

    if args.pages is not None and not args.files:
        ap.error("--pages needs the file(s) to apply to")

    files = args.files or sorted(
        p for p in args.papers_dir.glob("*.pdf")
        if not p.stem.endswith("_annotated") and not p.name.startswith("."))
    originals = args.papers_dir / "_originals"

    planned: list[tuple[Path, int, str]] = []
    for f in files:
        if not f.exists():
            print(f"missing      {f}")
            continue
        if args.pages is not None:
            planned.append((f, args.pages, f"forced {args.pages}"))
            continue
        try:
            covers = leading_covers(f)
        except Exception as e:  # noqa: BLE001
            print(f"unreadable   {f.name}  ({e})")
            continue
        if covers:
            why = ", ".join(w for _, w in covers)
            planned.append((f, len(covers), why))

    if not planned:
        print("No cover sheets found.")
        return 0

    stale = []
    for f, n, why in planned:
        if args.execute:
            try:
                backup = strip(f, n, originals)
            except Exception as e:  # noqa: BLE001
                print(f"FAILED       {f.name}  ({e})")
                continue
            print(f"stripped     {f.name}  −{n} page{'s' if n > 1 else ''}  [{why}]  original → {backup.relative_to(args.papers_dir.parent)}")
        else:
            print(f"would strip  {f.name}  −{n} page{'s' if n > 1 else ''}  [{why}]")
        ann = f.with_name(f.stem + "_annotated.pdf")
        if ann.exists():
            stale.append(ann.name)

    if stale:
        print("\nAnnotated copies now stale (regenerate with annotate_paper.py): "
              + ", ".join(stale))
    if not args.execute:
        print("\nDry run. Add --execute to strip (originals are kept in papers/_originals/).")
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
