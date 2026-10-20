#!/usr/bin/env python3
"""
verify_dois.py — check that every DOI in citations.md resolves to the
paper the entry describes.

    python verify_dois.py                   # every entry
    python verify_dois.py --status wanted   # only [wanted] entries
    python verify_dois.py --key @Bates2003  # one entry

For each entry the DOI is looked up at Crossref (api.crossref.org,
no key needed) and the registered title and first author are compared
with the entry's own. Output per entry:

    ok          title matches (similarity >= 0.85) and first author matches
    title?      DOI resolves, but the title differs — read the two lines
    author?     title matches, first author does not (often just a
                diacritic or a consortium author; check)
    not found   Crossref has no record for this DOI — a typo, or a
                DOI that was never registered
    no doi      the entry has no `doi:` line

Nothing is written. `match_papers.py` keys on these DOIs, so a wrong
one means a downloaded PDF is simply not recognised — this is how to
find that before it happens. Needs network; run it on the machine, not
in a sandbox.
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from match_papers import read_citations  # noqa: E402

CROSSREF = "https://api.crossref.org/works/"
UA = "calmar-aphasia-kb/1.0 (mailto:m.massontrottier@uq.edu.au)"


def _fold(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9 ]", " ", s.lower()).strip()


def _statuses(path: Path) -> dict[str, str]:
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^##\s+(@\S+)\s*(?:\[([\w\-]+)\])?", line)
        if m:
            out[m.group(1)] = (m.group(2) or "").lower()
    return out


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


def check(entry: dict, rec: dict | None) -> tuple[str, str]:
    if rec is None:
        return "not found", ""
    title = " ".join(rec.get("title") or [""])
    sim = difflib.SequenceMatcher(None, _fold(entry["title"]), _fold(title)).ratio()
    authors = rec.get("author") or []
    first = _fold(authors[0].get("family", "")) if authors else ""
    detail = f"crossref: {title[:90]}{'…' if len(title) > 90 else ''}"
    if sim < 0.85:
        return "title?", detail
    if entry["author"] and first and entry["author"] not in first and first not in entry["author"]:
        return "author?", f"crossref first author: {authors[0].get('family')}"
    return "ok", ""


def _cli(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--citations", type=Path, default=ROOT / "citations.md")
    ap.add_argument("--status", help="only entries with this status tag (e.g. wanted)")
    ap.add_argument("--key", action="append", help="only this @Key (repeatable)")
    args = ap.parse_args(argv)

    cites = read_citations(args.citations)
    statuses = _statuses(args.citations)
    keys = [k for k in cites
            if (not args.status or statuses.get(k) == args.status.lower())
            and (not args.key or k in args.key)]

    counts: dict[str, int] = {}
    for k in keys:
        e = cites[k]
        if not e["doi"]:
            verdict, detail = "no doi", ""
        else:
            try:
                verdict, detail = check(e, lookup(e["doi"]))
            except Exception as ex:  # noqa: BLE001
                verdict, detail = "error", str(ex)[:80]
            time.sleep(0.2)   # polite to Crossref
        counts[verdict] = counts.get(verdict, 0) + 1
        mark = "  " if verdict == "ok" else "! "
        print(f"{mark}{verdict:<10} {k:<24} {e['doi'] or ''}")
        if detail:
            print(f"             entry:    {e['title'][:90]}")
            print(f"             {detail}")
    print("\n" + " · ".join(f"{v} {n}" for v, n in sorted(counts.items())))
    return 1 if any(v not in ("ok",) for v in counts) else 0


if __name__ == "__main__":
    sys.exit(_cli())
