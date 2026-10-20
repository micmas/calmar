#!/usr/bin/env python3
"""
match_papers.py — rename downloaded PDFs in papers/ to their citation key.

Drop PDFs into papers/ under whatever name the publisher gave them
(`1-s2.0-S0093934X84710637-main.pdf`, `awp141.pdf`, `brain-2018-363.pdf`)
and run:

    python match_papers.py             # dry run: shows what would be renamed
    python match_papers.py --execute   # rename

How a file is matched, in order:
  1. DOI in the text — the DOI printed on the PDF's first pages, compared
     with the `doi:` lines in citations.md. Unambiguous when it hits.
  2. DOI in the filename — publishers often name the download after the
     DOI suffix (`awp284.pdf`, `01.STR.32.7.1621.pdf`, `88-2-237.pdf`).
  3. Title in the filename — `Assessment_of_arcuate_fascicul.pdf` is a
     prefix of a title in citations.md. Works for image-only scans.
  4. Author + year + title in the text — the first author's surname sits
     in the first 600 characters (the author block), the year is on the
     first pages, and at least 60 % of the title's content words appear
     in the first 600 characters. Reported as "probable"; renamed only
     with --execute --allow-probable.
Files that match nothing, or match a key that already has a PDF, are
listed and left alone. Nothing is ever deleted or overwritten.

A `.txt` sidecar is accepted in place of a PDF for OCR'd scans.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

_DOI = re.compile(r"\b(10\.\d{4,9}/[^\s\"'<>\]\)\},;]+)", re.I)
# "Leff AP, Schofield TM," / "Rothi LJG." — surnames with initials
_AUTHOR_LINE = re.compile(r"^(?:[A-Z][\w'’\-]+(?: [A-Z][\w'’\-]+)*,?\s+[A-Z]{1,4}[,.]\s*)+(?:et al\.?)?$")
_STOP = {"the", "a", "an", "of", "in", "on", "at", "for", "with", "and",
         "or", "to", "from", "by", "is", "as", "after", "its", "an", "versus",
         "vs", "via", "into", "than", "that", "this", "their", "between"}


def _norm_doi(d: str) -> str:
    d = d.strip().lower()
    d = re.sub(r"^https?://(dx\.)?doi\.org/", "", d)
    d = re.sub(r"^doi:\s*", "", d)
    return d.rstrip(".,;:)")


def read_citations(path: Path) -> dict[str, dict]:
    """@Key -> {doi, title, author, year} from citations.md."""
    text = path.read_text(encoding="utf-8")
    out: dict[str, dict] = {}
    blocks = re.split(r"^## (?=@)", text, flags=re.M)[1:]
    for blk in blocks:
        head, _, rest = blk.partition("\n")
        key = head.split()[0].strip()
        lines = [l.strip() for l in rest.split("\n")]
        body = [l for l in lines if l and not l.startswith((">", "#"))]
        doi = None
        for l in lines:
            m = re.search(r"doi:\s*(\S+)", l, re.I)
            if m:
                doi = _norm_doi(m.group(1))
                break
        m = re.match(r"@([A-Za-z\-']+?)(\d{4})", key)
        author = m.group(1).lower() if m else ""
        year = m.group(2) if m else ""
        # The author block is one or more lines of "Surname AB, Surname C,"
        # ending with a period; the title is the next line(s) up to the
        # first line that ends with a period; the journal line is *italic*.
        title_lines: list[str] = []
        in_title = False
        for l in body:
            if l.startswith("*") or l.lower().startswith("doi"):
                break
            if not in_title:
                if _AUTHOR_LINE.match(l):
                    continue
                in_title = True
            title_lines.append(l)
            if l.endswith("."):
                break
        title = " ".join(title_lines).strip()
        out[key] = {"doi": doi, "title": title, "author": author, "year": year}
    return out


def first_pages_text(path: Path, n_pages: int = 3) -> str:
    if path.suffix.lower() == ".txt":
        return path.read_text(encoding="utf-8", errors="ignore")[:20000]
    try:
        import pymupdf as fitz
    except ImportError:  # pragma: no cover
        import fitz
    doc = fitz.open(str(path))
    try:
        return "\n".join(doc[i].get_text() for i in range(min(n_pages, doc.page_count)))
    finally:
        doc.close()


def _slug(x: str) -> str:
    return re.sub(r"[^a-z0-9]", "", x.lower())


def match_one(text: str, cites: dict[str, dict],
              filename: str = "") -> tuple[str | None, str]:
    """Return (key, how) — how in {'doi', 'filename-doi', 'filename-title',
    'probable', ''}. The first three are safe to act on; 'probable' is
    reported only."""
    low = text.lower()
    by_doi = {v["doi"]: k for k, v in cites.items() if v.get("doi")}

    # 1. DOI printed in the text
    for d in {_norm_doi(d) for d in _DOI.findall(text)}:
        if d in by_doi:
            return by_doi[d], "doi"
        for cd, k in by_doi.items():   # trailing char lost / extra punctuation
            short, long_ = sorted((d, cd), key=len)
            if len(short) >= len(long_) - 2 and long_.startswith(short) \
                    and re.search(r"\d", short.split("/", 1)[-1]):
                return k, "doi"

    stem = Path(filename).stem if filename else ""
    if stem:
        # 2. DOI suffix in the filename: compare the slug of the stem with
        #    the slug of each DOI's part after the registrant prefix
        sslug = _slug(stem)
        if len(sslug) >= 5:
            for cd, k in by_doi.items():
                parts = cd.split("/")[1:]          # drop the 10.xxxx registrant
                cands = {_slug("/".join(parts))}   # whole suffix: "brain/awp284"
                if parts:
                    cands.add(_slug(parts[-1]))    # last segment: "awp284"
                if sslug in cands:
                    return k, "filename-doi"
        # 3. title prefix in the filename (>= 18 chars of the title)
        if len(sslug) >= 18:
            for k, v in cites.items():
                tslug = _slug(v["title"])
                if tslug and tslug.startswith(sslug[:min(len(sslug), 40)]):
                    return k, "filename-title"

    # 4. author block + year + title words, all near the top of page 1
    head = low[:600]
    best, best_score = None, 0.0
    for k, v in cites.items():
        if not v["author"] or not v["year"]:
            continue
        if v["author"] not in head or v["year"] not in low[:3000]:
            continue
        words = [w for w in re.findall(r"[a-z]{4,}", v["title"].lower())
                 if w not in _STOP]
        if len(words) < 3:
            continue
        hit = sum(1 for w in words if w in head) / len(words)
        if hit > best_score:
            best, best_score = k, hit
    if best and best_score >= 0.6:
        return best, "probable"
    return None, ""


def _cli(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--papers-dir", type=Path, default=ROOT / "papers")
    ap.add_argument("--citations", type=Path, default=ROOT / "citations.md")
    ap.add_argument("--execute", action="store_true", help="actually rename")
    ap.add_argument("--allow-probable", action="store_true",
                    help="with --execute: also rename author/year/title matches")
    args = ap.parse_args(argv)

    cites = read_citations(args.citations)
    keys_lower = {k.lstrip("@").lower(): k for k in cites}
    planned, unmatched, taken = [], [], []
    for f in sorted(args.papers_dir.iterdir()):
        if f.suffix.lower() not in (".pdf", ".txt") or f.name.startswith("."):
            continue
        stem = f.stem
        if stem.endswith("_annotated") or stem.lower() in keys_lower:
            continue   # already named, or an annotated copy
        try:
            text = first_pages_text(f)
        except Exception as e:  # noqa: BLE001
            unmatched.append((f.name, f"unreadable: {e}"))
            continue
        key, how = match_one(text, cites, filename=f.name)
        if not key:
            dois = sorted({_norm_doi(d) for d in _DOI.findall(text)})[:3]
            unmatched.append((f.name, f"no match; DOIs seen: {', '.join(dois) or 'none'}"))
            continue
        target = args.papers_dir / f"{key.lstrip('@')}{f.suffix.lower()}"
        if target.exists():
            taken.append((f.name, key, target.name))
            continue
        planned.append((f, target, how))

    for f, target, how in planned:
        tag = {"doi": "DOI", "filename-doi": "DOI in filename",
               "filename-title": "title in filename"}.get(how, "probable")
        do = args.execute and (how != "probable" or args.allow_probable)
        if do:
            f.rename(target)
        print(f"{'renamed' if do else 'would rename':12} {f.name}  →  {target.name}   [{tag}]")
    for name, key, tname in taken:
        print(f"{'duplicate':12} {name}  matches {key} but {tname} already exists — left alone")
    for name, why in unmatched:
        print(f"{'unmatched':12} {name}  ({why})")
    if planned and not args.execute:
        print("\nDry run. Add --execute to rename"
              + (" (and --allow-probable for the non-DOI matches)."
                 if any(h == "probable" for *_, h in planned) else "."))
    if not (planned or taken or unmatched):
        print("Every file in papers/ is already named after a citation key.")
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
