#!/usr/bin/env python3
"""
intake_papers.py — everything that has to happen to a PDF between the
download and the extractor, in one command.

    python intake_papers.py             # dry run: shows what each step would do
    python intake_papers.py --execute   # do it
    python intake_papers.py --from ~/Downloads --execute
                                        # also pull in PDFs from Downloads that
                                        # match a cited paper not yet in papers/

Steps, in order, each one of the standalone scripts:
  0. (--from DIR) copy PDFs out of DIR whose DOI / filename matches a
                            cited key that has no PDF yet; other files in
                            DIR are left untouched, nothing is moved
  1. match_papers.py        rename publisher-named PDFs to <Key>.pdf
  2. strip_cover_pages.py   drop JSTOR / T&F / HighWire / ProQuest … sheets
  3. batch_ocr.py           OCR scanned PDFs (needs ocrmypdf — the step
                            says what is missing and is skipped, the rest
                            still runs)
  4. kb_status.py           the papers line: cited / present / missing,
                            plus files that match no citation key

Each step is dry-run unless --execute is given. --allow-probable lets
step 1 also rename author/year/title matches (see match_papers.py).
Nothing is deleted; originals of stripped or OCR'd files go to
papers/_originals/.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import batch_ocr  # noqa: E402
import kb_status  # noqa: E402
import match_papers  # noqa: E402
import strip_cover_pages  # noqa: E402


def _banner(n: int, title: str) -> None:
    print(f"\n{'─' * 70}\n {n}. {title}\n{'─' * 70}")


def pull_from(src_dir: Path, papers_dir: Path, execute: bool) -> int:
    """Copy PDFs in src_dir that match a cited key with no PDF yet."""
    cites = match_papers.read_citations(ROOT / "citations.md")
    have = {p.stem.lower() for p in papers_dir.glob("*.pdf")}
    n = 0
    for f in sorted(src_dir.glob("*.pdf")):
        try:
            text = match_papers.first_pages_text(f)
        except Exception:  # noqa: BLE001
            continue
        key, how = match_papers.match_one(text, cites, filename=f.name)
        if not key or how == "probable":
            continue
        bare = key.lstrip("@")
        if bare.lower() in have:
            continue
        target = papers_dir / f"{bare}.pdf"
        print(f"{'copied' if execute else 'would copy':12} {f.name}  →  papers/{target.name}")
        if execute:
            shutil.copy2(f, target)
            have.add(bare.lower())
        n += 1
    if not n:
        print(f"nothing in {src_dir} matches a cited paper that is still missing")
    return 0


def _cli(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--papers-dir", type=Path, default=ROOT / "papers")
    ap.add_argument("--execute", action="store_true", help="actually rename / strip / OCR")
    ap.add_argument("--allow-probable", action="store_true",
                    help="also rename author/year/title matches (match_papers.py)")
    ap.add_argument("--no-ocr", action="store_true", help="skip the OCR step")
    ap.add_argument("--from", dest="from_dir", type=Path, metavar="DIR",
                    help="first copy matching PDFs out of DIR (e.g. ~/Downloads)")
    args = ap.parse_args(argv)

    ex = ["--execute"] if args.execute else []
    papers = ["--papers-dir", str(args.papers_dir)]
    rc = 0

    if args.from_dir:
        _banner(0, f"Copy cited papers out of {args.from_dir}")
        src = args.from_dir.expanduser()
        if not src.is_dir():
            print(f"not a directory: {src}")
            return 2
        rc |= pull_from(src, args.papers_dir, args.execute)

    _banner(1, "Rename downloads to their citation key  (match_papers.py)")
    rc |= match_papers._cli(papers + ex + (["--allow-probable"] if args.allow_probable else []))

    _banner(2, "Strip publisher cover sheets  (strip_cover_pages.py)")
    rc |= strip_cover_pages._cli(papers + ex)

    if not args.no_ocr:
        _banner(3, "OCR scanned PDFs  (batch_ocr.py)")
        missing = batch_ocr.missing_tools() if args.execute else []
        if missing:
            print("skipped — OCR tools missing:\n  " + "\n  ".join(missing))
            rc |= 2
        else:
            r = batch_ocr.main(papers + ex)
            rc |= (r if r != 1 else 0)   # 1 = some file failed; reported above

    _banner(4, "Papers status  (kb_status.py)")
    st = kb_status.collect(ROOT)
    missing_keys = [k for k, v in st["papers"].items() if not v["pdf_present"]]
    print(f"  {len(st['papers'])} cited · {len(st['papers']) - len(missing_keys)} with a PDF · "
          f"{len(missing_keys)} missing"
          + (f"  →  python kb_status.py --papers-needed" if missing_keys else ""))
    if st.get("papers_unmatched"):
        print(f"  {len(st['papers_unmatched'])} file(s) match no citation key: "
              + ", ".join(st["papers_unmatched"][:8])
              + (" …" if len(st["papers_unmatched"]) > 8 else ""))
        print("  (add a @Key to citations.md, or remove the file)")

    if not args.execute:
        print("\nDry run throughout. Re-run with --execute to apply all steps.")
    return rc


if __name__ == "__main__":
    sys.exit(_cli())
