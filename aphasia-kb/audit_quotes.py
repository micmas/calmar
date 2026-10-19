#!/usr/bin/env python3
"""
audit_quotes.py — verify every `source_passages` quote in the CANONICAL
knowledge base against the paper it cites.

`auto_review.py` checks drafts; `compare_extraction.py` checks a sandbox
extraction. Nothing checked the approved entries until v2.5, and the
2026-05 batch was approved largely without PDFs. This script is the
triage for GOVERNANCE.md §5: an entry whose quotes all locate can be
re-reviewed quickly; an entry with an absent quote goes to the top of
the pile.

    python audit_quotes.py                      # table, all buckets
    python audit_quotes.py --bucket therapies   # one bucket
    python audit_quotes.py --csv _compare/audit.csv   # one row per passage
    python audit_quotes.py --show-absent        # list the absent quotes
    python audit_quotes.py --fail-on-missing    # exit 1 if any quote is absent

Grades come from the shared `quote_check.py`, so the same quote gets
the same grade here, in `auto_review.py` and in `compare_extraction.py`:
    found     verbatim in the text layer
    elided    `[...]`/`…` in the quote and every fragment is verbatim
    table     table cells quoted in row form (`a | b | 0.60`); verbatim
              content, but not a span the annotator can highlight
    anchored  opening 60 chars match, then a glyph the PDF font encodes
              oddly (`<` as `5`, `=` as `¼`) was silently corrected
    near      the same passage with a lost space, or a paraphrase
    absent    nothing similar anywhere — the fabrication signal
    no_pdf    the cited paper is not in papers/ (see kb_status.py
              --papers-needed)

found + elided + table are "verified". anchored and near are for a
person to confirm against the annotated PDF. absent is re-review first.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from aphasia_kb import parse_markdown  # noqa: E402
from quote_check import PaperText, find_paper, grade_quote  # noqa: E402

BUCKETS = ("regions", "impairments", "therapies", "predictors", "reviews")
GRADES = ("found", "elided", "table", "anchored", "near", "absent", "no_pdf")


def audit(root: Path, papers_dir: Path, buckets=BUCKETS) -> list[dict]:
    rows: list[dict] = []
    cache: dict[str, PaperText | None] = {}
    for b in buckets:
        d = root / b
        if not d.is_dir():
            continue
        for p in sorted(d.glob("*.md")):
            fm, _ = parse_markdown(p)
            if not fm:
                continue
            for f in fm.get("findings") or []:
                if not isinstance(f, dict):
                    continue
                cite = str(f.get("citation") or "")
                if cite not in cache:
                    paper = find_paper(cite, papers_dir)
                    try:
                        cache[cite] = PaperText.from_pdf(paper) if paper else None
                    except Exception as e:  # noqa: BLE001
                        cache[cite] = None
                        print(f"  ! could not read {paper}: {e}", file=sys.stderr)
                paper_text = cache[cite]
                for sp in f.get("source_passages") or []:
                    q = (sp.get("quote") or "").strip()
                    if not q:
                        continue
                    if paper_text is None:
                        status = "no_pdf"
                    else:
                        status = grade_quote(q, paper_text)
                        if status == "exact":
                            status = "found"
                    rows.append({
                        "bucket": b, "entry": p.name, "entry_id": fm.get("id"),
                        "reviewer": fm.get("reviewer"),
                        "review_tier": fm.get("review_tier"),
                        "finding": f.get("id"), "citation": cite,
                        "supports": sp.get("supports"), "page": sp.get("page"),
                        "status": status, "quote": q[:120],
                    })
    return rows


def summarise(rows: list[dict]) -> list[dict]:
    by: dict[tuple, dict] = {}
    for r in rows:
        k = (r["bucket"], r["entry"])
        e = by.setdefault(k, {"bucket": r["bucket"], "entry": r["entry"],
                              "reviewer": r["reviewer"], "passages": 0,
                              **{g: 0 for g in GRADES}})
        e["passages"] += 1
        e[r["status"]] += 1
    out = list(by.values())
    # worst first: absent, then the ones a person must eyeball, then clean
    out.sort(key=lambda e: (-e["absent"], -(e["near"] + e["anchored"]),
                            -e["no_pdf"], e["bucket"], e["entry"]))
    return out


def _cli(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--papers-dir", type=Path, default=ROOT / "papers")
    ap.add_argument("--bucket", choices=BUCKETS, action="append")
    ap.add_argument("--csv", type=Path, help="write one row per passage")
    ap.add_argument("--fail-on-missing", action="store_true")
    ap.add_argument("--show-absent", action="store_true",
                    help="print every absent quote (first 120 chars)")
    args = ap.parse_args(argv)

    rows = audit(args.root, args.papers_dir, tuple(args.bucket or BUCKETS))
    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        with args.csv.open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else
                               ["bucket", "entry", "status"])
            w.writeheader()
            w.writerows(rows)
        print(f"wrote {args.csv} ({len(rows)} passages)")

    summ = summarise(rows)
    print(f"{'bucket':<12}{'entry':<44}{'quotes':>7}{'found':>6}{'elided':>7}"
          f"{'table':>6}{'anchor':>7}{'near':>5}{'absent':>7}{'no pdf':>7}")
    for e in summ:
        print(f"{e['bucket']:<12}{e['entry'][:43]:<44}{e['passages']:>7}"
              f"{e['found']:>6}{e['elided']:>7}{e['table']:>6}{e['anchored']:>7}"
              f"{e['near']:>5}{e['absent']:>7}{e['no_pdf']:>7}")
    tot = {g: sum(e[g] for e in summ) for g in GRADES}
    tot["passages"] = sum(e["passages"] for e in summ)
    verified = tot["found"] + tot["elided"] + tot["table"]
    print(f"\n{len(summ)} entries · {tot['passages']} passages · "
          f"{verified} verified (found {tot['found']}, elided {tot['elided']}, "
          f"table {tot['table']}) · {tot['anchored']} anchored · "
          f"{tot['near']} near · {tot['absent']} absent · "
          f"{tot['no_pdf']} without a PDF")
    if args.show_absent:
        for r in rows:
            if r["status"] == "absent":
                print(f"  ABSENT {r['bucket']}/{r['entry']} {r['finding']} "
                      f"[{r['supports']}] p.{r['page']}: {r['quote']}")
    if args.fail_on_missing and tot["absent"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
