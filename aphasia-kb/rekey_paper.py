#!/usr/bin/env python3
"""
rekey_paper.py — move everything extracted under one citation key to
another key.

    python rekey_paper.py --from @1-s2.0-S0010945208001330-main --to @Rapcsak2009
    python rekey_paper.py --from @1-s2.0-S0010945208001330-main --to @Rapcsak2009 --execute
    python rekey_paper.py --auto              # every draft key that is not in
                                              # citations.md, matched by the PDF's DOI
    python rekey_paper.py --auto --execute

For when a PDF was extracted before it had an entry in citations.md,
so its drafts, log lines and annotated copy carry a key made from the
download name. Renames and rewrites, in this order:

  papers/<old>.pdf                       → papers/<new>.pdf
  papers/<old>_annotated.pdf             → papers/<new>_annotated.pdf
  drafts/<bucket>/<id>__<old>.md         → drafts/<bucket>/<id>__<new>.md
      with `id:` and every `citation:` inside rewritten
  auto_review_log/<id>__<old>.yaml       → …__<new>.yaml (content rewritten)
  extraction_log.md                      lines mentioning @<old> rewritten
      and one REKEYED line appended

The target key must exist in citations.md (register_papers.py or a
hand-written block). Canonical entries are never touched: rekey a
draft before it is promoted. Dry run unless --execute.
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from match_papers import _DOI, _norm_doi, first_pages_text, read_citations  # noqa: E402

BUCKETS = ("regions", "impairments", "therapies", "predictors", "reviews")


def _bare(k: str) -> str:
    return k.lstrip("@")


def plan(old: str, new: str) -> list[tuple[str, Path, Path | None]]:
    """[(kind, src, dst)] — dst None means rewrite in place."""
    o, n = _bare(old), _bare(new)
    out: list[tuple[str, Path, Path | None]] = []
    papers = ROOT / "papers"
    for suffix in (".pdf", "_annotated.pdf", ".txt"):
        src = papers / f"{o}{suffix}"
        if src.exists():
            out.append(("file", src, papers / f"{n}{suffix}"))
    for b in BUCKETS:
        for src in sorted((ROOT / "drafts" / b).glob(f"*__{o}.md")):
            out.append(("draft", src, src.with_name(src.name[:-len(f"__{o}.md")] + f"__{n}.md")))
    for src in sorted((ROOT / "auto_review_log").glob(f"*__{o}.yaml")):
        out.append(("sidecar", src, src.with_name(src.name[:-len(f"__{o}.yaml")] + f"__{n}.yaml")))
    log = ROOT / "extraction_log.md"
    if log.exists() and f"@{o}" in log.read_text(encoding="utf-8"):
        out.append(("log", log, None))
    return out


def _rewrite(text: str, o: str, n: str) -> str:
    text = re.sub(rf"@{re.escape(o)}(?![\w\-])", f"@{n}", text)
    text = re.sub(rf"__{re.escape(o)}(?=\.md|\.yaml|\b|$)", f"__{n}", text)
    return text


def apply(old: str, new: str, execute: bool) -> int:
    o, n = _bare(old), _bare(new)
    steps = plan(old, new)
    if not steps:
        print(f"nothing carries @{o}")
        return 0
    verb = "" if execute else "would "
    for kind, src, dst in steps:
        if dst is None:
            print(f"  {verb}rewrite  {src.relative_to(ROOT)}  (@{o} → @{n})")
            continue
        if dst.exists():
            print(f"  ✗ {dst.relative_to(ROOT)} already exists — resolve by hand")
            return 1
        print(f"  {verb}rename   {src.relative_to(ROOT)}  →  {dst.name}")
    if not execute:
        return 0
    for kind, src, dst in steps:
        if kind in ("draft", "sidecar"):
            # rename first, then rewrite in place: works where deleting
            # is not allowed (sandboxed shells) and leaves no orphan
            src.rename(dst)
            dst.write_text(_rewrite(dst.read_text(encoding="utf-8"), o, n), encoding="utf-8")
        elif kind == "file":
            src.rename(dst)
        elif kind == "log":
            text = _rewrite(src.read_text(encoding="utf-8"), o, n)
            text = text.rstrip("\n") + (f"\n{date.today():%Y-%m-%d} | REKEYED | @{n} | "
                                        f"was extracted as @{o} (PDF had no citations.md entry)\n")
            src.write_text(text, encoding="utf-8")
    return 0


def auto_pairs() -> list[tuple[str, str]]:
    """(old, new) for every draft key absent from citations.md whose PDF's
    DOI identifies an entry that is there."""
    cites = read_citations(ROOT / "citations.md")
    by_doi = {v["doi"]: k for k, v in cites.items() if v.get("doi")}
    draft_keys = set()
    for b in BUCKETS:
        for p in (ROOT / "drafts" / b).glob("*__*.md"):
            draft_keys.add(p.stem.rsplit("__", 1)[1])
    pairs = []
    for k in sorted(draft_keys):
        if f"@{k}" in cites:
            continue
        pdf = ROOT / "papers" / f"{k}.pdf"
        if not pdf.exists():                      # match_papers may have renamed it already
            pdf = ROOT / "papers" / f"{k}_annotated.pdf"
        if not pdf.exists():
            print(f"  ? @{k}: no papers/{k}.pdf or _annotated.pdf to read a DOI from")
            continue
        text = first_pages_text(pdf)
        for d in (_norm_doi(x) for x in _DOI.findall(text)):
            if d in by_doi:
                pairs.append((f"@{k}", by_doi[d]))
                break
        else:
            print(f"  ? @{k}: no DOI in the PDF matches a citations.md entry — pass --from/--to")
    return pairs


def _cli(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--from", dest="old", help="key as extracted (with or without @)")
    ap.add_argument("--to", dest="new", help="correct key, present in citations.md")
    ap.add_argument("--auto", action="store_true",
                    help="find every draft key missing from citations.md and match by DOI")
    ap.add_argument("--execute", action="store_true")
    args = ap.parse_args(argv)

    cites = read_citations(ROOT / "citations.md")
    if args.auto:
        pairs = auto_pairs()
    elif args.old and args.new:
        pairs = [(args.old, args.new)]
    else:
        ap.error("--from X --to Y, or --auto")

    rc = 0
    for old, new in pairs:
        if f"@{_bare(new)}" not in cites:
            print(f"✗ @{_bare(new)} is not in citations.md — add it first")
            rc = 1
            continue
        print(f"\n@{_bare(old)}  →  @{_bare(new)}")
        rc |= apply(old, new, args.execute)
    if pairs and not args.execute:
        print("\nDry run. Add --execute to apply.")
    return rc


if __name__ == "__main__":
    sys.exit(_cli())
