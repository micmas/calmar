#!/usr/bin/env python3
"""
audit_quotes.py — verify every `source_passages` quote in the CANONICAL
knowledge base against the paper it cites.

`auto_review.py` checks drafts; `compare_extraction.py` checks a sandbox
extraction. Nothing checked the approved entries until now, and the
2026-05 batch was approved largely without PDFs. This script is the
triage for GOVERNANCE.md §5: an entry whose quotes all locate can be
re-reviewed quickly; an entry with a missing quote goes to the top of
the pile.

    python audit_quotes.py                      # table, all buckets
    python audit_quotes.py --bucket therapies   # one bucket
    python audit_quotes.py --csv audit.csv      # one row per passage
    python audit_quotes.py --fail-on-missing    # exit 1 if any quote is absent

Matching uses annotate_paper's normaliser (ligatures, soft hyphens,
smart quotes, whitespace) and is case-insensitive, i.e. the same test
`auto_review.check_pdf_quote_match` applies to drafts, so a canonical
entry that passes here would pass the Tier A exact-match rule.

Three outcomes per passage:
    found     located in the PDF text layer
    absent    not located — fabricated, paraphrased, or a bad OCR layer
    no_pdf    the cited paper is not in papers/ (see kb_status.py
              --papers-needed)
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from aphasia_kb import parse_markdown  # noqa: E402

try:
    from annotate_paper import _normalize
except Exception:  # pragma: no cover
    import re

    def _normalize(s: str) -> str:
        return re.sub(r"\s+", " ", s).strip()

BUCKETS = ("regions", "impairments", "therapies", "predictors", "reviews")


def _pdf_text(path: Path) -> str:
    if path.suffix.lower() == ".txt":
        return path.read_text(encoding="utf-8", errors="ignore")
    import fitz  # pymupdf
    doc = fitz.open(str(path))
    text = "\n".join(page.get_text() for page in doc)
    doc.close()
    return text


def _find_paper(cite: str, papers_dir: Path) -> Path | None:
    key = cite.lstrip("@")
    for ext in (".pdf", ".txt"):
        p = papers_dir / f"{key}{ext}"
        if p.exists():
            return p
    return None


def audit(root: Path, papers_dir: Path, buckets=BUCKETS) -> list[dict]:
    rows: list[dict] = []
    cache: dict[str, str | None] = {}
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
                    paper = _find_paper(cite, papers_dir) if cite else None
                    try:
                        cache[cite] = (_normalize(_pdf_text(paper)).casefold()
                                       if paper else None)
                    except Exception as e:  # noqa: BLE001
                        cache[cite] = None
                        print(f"  ! could not read {paper}: {e}", file=sys.stderr)
                text = cache[cite]
                for sp in f.get("source_passages") or []:
                    q = (sp.get("quote") or "").strip()
                    if not q:
                        continue
                    if text is None:
                        status = "no_pdf"
                    else:
                        status = ("found" if _normalize(q).casefold() in text
                                  else "absent")
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
                              "reviewer": r["reviewer"],
                              "passages": 0, "found": 0, "absent": 0,
                              "no_pdf": 0})
        e["passages"] += 1
        e[r["status"]] += 1
    out = list(by.values())
    # worst first: absent quotes, then unverifiable, then clean
    out.sort(key=lambda e: (-e["absent"], -e["no_pdf"], e["bucket"], e["entry"]))
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
        with args.csv.open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else
                               ["bucket", "entry", "status"])
            w.writeheader()
            w.writerows(rows)
        print(f"wrote {args.csv} ({len(rows)} passages)")

    summ = summarise(rows)
    print(f"{'bucket':<12}{'entry':<48}{'quotes':>7}{'found':>7}"
          f"{'absent':>8}{'no pdf':>8}")
    for e in summ:
        print(f"{e['bucket']:<12}{e['entry'][:47]:<48}{e['passages']:>7}"
              f"{e['found']:>7}{e['absent']:>8}{e['no_pdf']:>8}")
    tot = {k: sum(e[k] for e in summ) for k in ("passages", "found", "absent", "no_pdf")}
    print(f"\n{len(summ)} entries · {tot['passages']} passages · "
          f"{tot['found']} found · {tot['absent']} absent · "
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
