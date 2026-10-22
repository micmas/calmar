#!/usr/bin/env python3
"""
reextract.py — extract chosen papers again with the current extractor.

    python reextract.py Breier2008 Hope2013              # dry run: the plan
    python reextract.py Breier2008 Hope2013 --execute    # do it
    python reextract.py --preset selective-retry --execute
    python reextract.py --preset placeholder --into-drafts --execute

`extract.py --batch` never re-extracts a paper that already has findings,
which is right for routine runs and wrong when an earlier extraction is
known to be weak (made with thinking on and cut to 8 findings by the
overflow retry; or written in May without the paper). This does it on
purpose, without losing anything:

  * paper has DRAFTS only → its drafts and their review sidecars are
    moved to _compare/superseded/<date>/ (git-ignored; git history keeps
    the committed copies), the old annotated PDF likewise, and the paper
    is extracted afresh into drafts/. A RE-EXTRACTED line goes to the log.
  * paper has CANONICAL findings (approved, by a person or a model) →
    extracted into the sandbox _compare/rerun/ instead, so nothing
    approved is duplicated; compare with
        python compare_extraction.py --citation @Key --candidate-dir _compare/rerun
    and promote by hand what the old entry lacks.
    --into-drafts overrides this (for the placeholder therapy findings,
    which must be replaced, not compared): fresh drafts are written next
    to the canonical findings, and the placeholder findings are removed
    from the canonical entry at review.

Presets name the groups identified on 2026-10-22:
  placeholder      five therapy papers whose May findings quote "clinical
                   knowledge" instead of the paper
  selective-retry  fifteen papers whose 2026-10-20/21 extraction overflowed
                   (thinking on) and was retried with "at most 8 findings"
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUCKETS = ("regions", "impairments", "therapies", "predictors", "reviews")
CANON = BUCKETS + ("ingredients",)

PRESETS = {
    "placeholder": ["Maher2006", "Pulvermuller2001", "Schlaug2008", "Stahl2013",
                    "vanderMeulen2012"],
    "selective-retry": ["Breier2008", "Schwartz2012", "Karnath2018", "Alyahya2020",
                        "Bates2003", "Benghanem2019", "Billot2022", "Bonilha2016",
                        "Breitenstein2017", "Catani2008", "Fridriksson2013",
                        "Griffis2017", "Halai2017", "Henseler2014", "Hope2013"],
}


def canonical_files(key: str) -> list[Path]:
    rx = re.compile(rf"^\s*citation:\s*['\"]?@{re.escape(key)}['\"]?\s*$", re.M)
    out = []
    for b in CANON:
        for p in sorted((ROOT / b).glob("*.md")):
            if rx.search(p.read_text(encoding="utf-8")):
                out.append(p)
    return out


def draft_files(key: str) -> list[Path]:
    return [p for b in BUCKETS for p in sorted((ROOT / "drafts" / b).glob(f"*__{key}.md"))]


def sidecars(key: str) -> list[Path]:
    return sorted((ROOT / "auto_review_log").glob(f"*__{key}.yaml"))


def _move(src: Path, dest_root: Path, execute: bool) -> str:
    rel = src.relative_to(ROOT)
    dst = dest_root / rel
    if execute:
        dst.parent.mkdir(parents=True, exist_ok=True)
        n = 1
        while dst.exists():
            dst = dst.with_name(f"{dst.stem}.{n}{dst.suffix}")
            n += 1
        shutil.move(str(src), str(dst))
    return str(rel)


def _cli(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("keys", nargs="*", help="citation keys, with or without @")
    ap.add_argument("--preset", choices=sorted(PRESETS), action="append")
    ap.add_argument("--into-drafts", action="store_true",
                    help="extract into drafts/ even when the paper has canonical findings")
    ap.add_argument("--papers-dir", type=Path, default=ROOT / "papers")
    ap.add_argument("--execute", action="store_true")
    args = ap.parse_args(argv)

    keys = [k.lstrip("@") for k in args.keys]
    for p in args.preset or []:
        keys += [k for k in PRESETS[p] if k not in keys]
    if not keys:
        ap.error("give citation keys or --preset")

    today = dt.date.today().isoformat()
    superseded = ROOT / "_compare" / "superseded" / today
    to_drafts, to_sandbox, missing = [], [], []

    for k in keys:
        pdf = args.papers_dir / f"{k}.pdf"
        if not pdf.exists():
            missing.append(k)
            print(f"✗ {k}: no {pdf.name} in papers/ — skipped")
            continue
        canon = canonical_files(k)
        drafts = draft_files(k)
        if canon and not args.into_drafts:
            to_sandbox.append(pdf)
            print(f"⊙ {k}: {len(canon)} canonical entr{'y' if len(canon) == 1 else 'ies'} "
                  f"cite it → sandbox _compare/rerun/ (drafts left as they are: {len(drafts)})")
            continue
        verb = "moved" if args.execute else "would move"
        print(f"↻ {k}: {len(drafts)} draft(s) {verb} to _compare/superseded/{today}/ → "
              f"fresh drafts" + (f"  ({len(canon)} canonical entr{'y' if len(canon) == 1 else 'ies'} "
                                 f"also cite it — remove the old findings at review)" if canon else ""))
        for f in drafts + sidecars(k):
            _move(f, superseded, args.execute)
        ann = args.papers_dir / f"{k}_annotated.pdf"
        if ann.exists() and args.execute:
            dst = superseded / "papers" / ann.name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(ann), str(dst))
        to_drafts.append(pdf)

    print(f"\n{len(to_drafts)} to drafts, {len(to_sandbox)} to the sandbox, "
          f"{len(missing)} without a PDF.")
    if not args.execute:
        print("Dry run. Add --execute to move the old drafts and extract.")
        return 0

    rc = 0
    if to_drafts:
        log = ROOT / "extraction_log.md"
        with log.open("a", encoding="utf-8") as fh:
            for pdf in to_drafts:
                fh.write(f"{today} | RE-EXTRACTED | @{pdf.stem} | previous drafts moved to "
                         f"_compare/superseded/{today}/ | current extractor (thinking off)\n")
        rc |= subprocess.call([sys.executable, str(ROOT / "extract.py"), "--pdf",
                               *map(str, to_drafts)], cwd=str(ROOT.parent))
    if to_sandbox:
        rc |= subprocess.call([sys.executable, str(ROOT / "extract.py"), "--pdf",
                               *map(str, to_sandbox), "--out-dir",
                               str(ROOT / "_compare" / "rerun")], cwd=str(ROOT.parent))
        print("\nCompare each sandbox paper with what is approved:")
        for pdf in to_sandbox:
            print(f"  python aphasia-kb/compare_extraction.py --citation @{pdf.stem} "
                  f"--candidate-dir aphasia-kb/_compare/rerun")
    return rc


if __name__ == "__main__":
    sys.exit(_cli())
