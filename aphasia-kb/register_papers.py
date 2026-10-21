#!/usr/bin/env python3
"""
register_papers.py — give every PDF in papers/ a citation entry.

A PDF that matches no `@Key` in citations.md cannot be renamed by
match_papers.py, and extract.py --batch refuses it (a paper must be in
the bibliography before anything is extracted from it — otherwise
drafts, log lines and annotated PDFs end up keyed on a download name
like `1-s2.0-S0010945208001330-main`). This script closes that gap:

    python register_papers.py             # dry run: shows the entries it would add
    python register_papers.py --execute   # append them to citations.md

For each unmatched PDF it finds the DOI (printed in the first pages, or
in the filename), asks Crossref for the bibliographic record, builds a
citations.md block in the house format with the tag `[seed]`, and
appends it under "## Registered automatically". The key is
<FirstAuthorSurname><Year>, as the existing keys are; on a collision
with a different paper, the first content word of the title is added
(`Fridriksson2010Preservation`).

Without a DOI, or when Crossref cannot be reached, the PDF is listed
with what could be read from its first page and left for a block
written by hand — nothing is guessed into the bibliography.

Every automatic entry carries a note saying so and the date, so a
person can see at a glance which blocks have not been checked. The
intake (intake_papers.py) runs this before matching, so the normal
flow is: drop the PDF in papers/, run the intake, done.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from match_papers import (_DOI, _norm_doi, _slug, first_pages_text,  # noqa: E402
                          match_one, read_citations)

CROSSREF = "https://api.crossref.org/works/"
UA = "calmar-aphasia-kb/1.0 (mailto:m.massontrottier@uq.edu.au)"
SECTION = "## Registered automatically"
_STOP = {"the", "a", "an", "of", "in", "on", "for", "and", "to", "with", "by",
         "from", "after", "is", "are", "its", "at", "as", "into", "versus"}


def _ascii(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    return "".join(ch for ch in s if not unicodedata.combining(ch))


def lookup(doi: str) -> dict | None:
    req = urllib.request.Request(CROSSREF + urllib.parse.quote(doi, safe=""),
                                 headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.load(r)["message"]
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def _author_line(rec: dict) -> tuple[str, str]:
    """('Baldo JV, Schwartz S, …', 'Baldo') in the house format."""
    out, first = [], ""
    for a in rec.get("author") or []:
        fam = a.get("family")
        if not fam:                       # consortium author
            if a.get("name"):
                out.append(a["name"])
            continue
        initials = "".join(p[0] for p in re.split(r"[\s\-.]+", a.get("given", "")) if p)
        out.append(f"{fam} {initials}".strip())
        first = first or fam
    if len(out) > 12:
        out = out[:12] + ["et al."]
    return ", ".join(out) + ("." if out and not out[-1].endswith(".") else ""), first


def _year(rec: dict) -> str:
    for k in ("published-print", "published-online", "issued", "created"):
        parts = (rec.get(k) or {}).get("date-parts") or [[None]]
        if parts and parts[0] and parts[0][0]:
            return str(parts[0][0])
    return ""


def make_key(first_author: str, year: str, title: str, existing: dict[str, dict], doi: str) -> str:
    base = re.sub(r"[^A-Za-z]", "", _ascii(first_author)) + year
    if not base:
        return ""
    for k, v in existing.items():
        if k.lstrip("@") == base and v.get("doi") == doi:
            return base                   # already registered under this key
    if f"@{base}" not in existing:
        return base
    for w in re.findall(r"[A-Za-z]{4,}", title):
        if w.lower() in _STOP:
            continue
        cand = base + w.capitalize()
        if f"@{cand}" not in existing:
            return cand
    return base + "b"


def build_block(rec: dict, key: str, doi: str, pdf_name: str) -> str:
    authors, _ = _author_line(rec)
    title = " ".join(rec.get("title") or [""]).strip().rstrip(".")
    journal = " ".join(rec.get("short-container-title") or rec.get("container-title") or [""])
    year = _year(rec)
    vol, issue, page = rec.get("volume", ""), rec.get("issue", ""), rec.get("page", "")
    ref = f"*{journal}*. {year}" if journal else year
    if vol:
        ref += f";{vol}"
        if issue:
            ref += f"({issue})"
        if page:
            ref += f":{page}"
    ref += "."
    return (f"## @{key}  [seed]\n{authors}\n{title}.\n{ref}\ndoi:{doi}\n\n"
            f"> Registered automatically from the PDF's DOI via Crossref on "
            f"{date.today().isoformat()} (file: {pdf_name}). Check the entry; "
            f"add a note on why the paper is in the KB.\n")


def _dois_of(text: str, filename: str, known: dict[str, str]) -> list[str]:
    """Candidate DOIs, best first. A DOI broken over a line ends up in
    the text twice, once truncated ("10.1136/jnnp-2012-") and once
    whole; the truncated form is dropped when a longer candidate starts
    with it. Otherwise the order on the page is kept (the article's own
    DOI is usually printed first, cited ones later)."""
    seen: list[str] = []
    for d in (_norm_doi(x) for x in _DOI.findall(text)):
        if re.search(r"/.*\d", d) and len(d.split("/", 1)[1]) >= 4 and d not in seen:
            seen.append(d)
    seen = [d for d in seen if not any(o != d and o.startswith(d) for o in seen)]
    stem = _slug(Path(filename).stem)
    for cd in known.values():
        parts = cd.split("/")[1:]
        if parts and _slug(parts[-1]) == stem and cd not in seen:
            seen.insert(0, cd)
    return seen


def _doi_of(text: str, filename: str, known: dict[str, str]) -> str | None:
    cands = _dois_of(text, filename, known)
    return cands[0] if cands else None
    # (kept for callers that want a single value; register() tries them all)
    seen = [_norm_doi(d) for d in _DOI.findall(text)]
    for d in seen:
        if re.search(r"/.*\d", d) and len(d.split("/", 1)[1]) >= 4:
            return d
    stem = _slug(Path(filename).stem)
    for cd in known.values():
        parts = cd.split("/")[1:]
        if parts and _slug(parts[-1]) == stem:
            return cd
    return None


def _page1_hint(text: str) -> str:
    return " ".join(text.split())[:160]


def register(papers_dir: Path, citations: Path, execute: bool) -> int:
    cites = read_citations(citations)
    known = {k: v["doi"] for k, v in cites.items() if v.get("doi")}
    keys_lower = {k.lstrip("@").lower() for k in cites}
    new_blocks: list[str] = []
    manual: list[tuple[str, str]] = []
    offline = False

    for f in sorted(papers_dir.glob("*.pdf")):
        if f.stem.endswith("_annotated") or f.stem.lower() in keys_lower:
            continue
        try:
            text = first_pages_text(f)
        except Exception as e:  # noqa: BLE001
            manual.append((f.name, f"unreadable: {e}"))
            continue
        key, how = match_one(text, cites, filename=f.name)
        if key and how != "probable":
            continue                       # match_papers will rename it
        cands = _dois_of(text, f.name, known)
        if not cands:
            manual.append((f.name, "no DOI in the first pages or filename — "
                                   f"page 1: {_page1_hint(text)}"))
            continue
        if any(c in known.values() for c in cands):
            continue                       # key exists; match_papers handles it
        if offline:
            manual.append((f.name, f"DOI {cands[0]} — Crossref unreachable"))
            continue
        rec, doi = None, cands[0]
        try:
            for doi in cands[:3]:          # first resolvable candidate wins
                rec = lookup(doi)
                if rec is not None:
                    break
        except Exception as e:  # noqa: BLE001
            offline = True
            manual.append((f.name, f"DOI {doi} — Crossref unreachable ({str(e)[:60]})"))
            continue
        if rec is None:
            manual.append((f.name, f"DOI(s) {', '.join(cands[:3])} not found at Crossref — "
                                   f"page 1: {_page1_hint(text)}"))
            continue
        _, first = _author_line(rec)
        title = " ".join(rec.get("title") or [""])
        key = make_key(first, _year(rec), title, cites, doi)
        if not key:
            manual.append((f.name, f"DOI {doi} — Crossref record has no author/year"))
            continue
        block = build_block(rec, key, doi, f.name)
        new_blocks.append(block)
        cites[f"@{key}"] = {"doi": doi, "title": title, "author": first.lower(), "year": _year(rec)}
        known[f"@{key}"] = doi
        print(f"{'registered' if execute else 'would register':16} {f.name}  →  @{key}")
        print("    " + block.splitlines()[2][:100])

    for name, why in manual:
        print(f"{'needs a block':16} {name}  ({why})")

    if new_blocks and execute:
        text = citations.read_text(encoding="utf-8").rstrip("\n") + "\n"
        if SECTION not in text:
            text += (f"\n---\n\n{SECTION}\n\n> Entries written by register_papers.py from the "
                     f"PDF's DOI. Each says when; none has been checked by a person "
                     f"until its note is replaced.\n\n")
        else:
            text += "\n"
        text += "\n".join(new_blocks)
        citations.write_text(text, encoding="utf-8")
        print(f"\n{len(new_blocks)} entr{'y' if len(new_blocks) == 1 else 'ies'} appended to {citations.name}")
    elif new_blocks:
        print(f"\nDry run: {len(new_blocks)} entr{'y' if len(new_blocks) == 1 else 'ies'} would be appended. Add --execute.")
    elif not manual:
        print("Every PDF in papers/ has a citation entry.")
    return 1 if manual else 0


def _cli(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--papers-dir", type=Path, default=ROOT / "papers")
    ap.add_argument("--citations", type=Path, default=ROOT / "citations.md")
    ap.add_argument("--execute", action="store_true", help="append the entries")
    args = ap.parse_args(argv)
    return register(args.papers_dir, args.citations, args.execute)


if __name__ == "__main__":
    sys.exit(_cli())
