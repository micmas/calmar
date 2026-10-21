#!/usr/bin/env python3
"""
normalize_drafts.py — apply the extractor's save-time repairs to drafts
that already exist.

    python normalize_drafts.py             # dry run: what would change
    python normalize_drafts.py --execute   # rewrite the drafts

extract.py fixes a handful of omissions the local model makes on nearly
every draft as it saves them (`_normalize_findings`): a missing
`author_limitations` (→ [] + flag), a missing `sample.phase` (inferred
from time_post_onset), a `region_definition` without `kind` (→
not_reported), an imaging finding without `reference_space` (→
not_reported + flag) or `atlases_used` (→ []), and predictor entry
fields missing on a draft whose entry already exists canonically. Each
rule was added after a batch had already produced drafts without it, so
those drafts fail `auto_review.py`'s schema check for reasons that need
no judgement. This applies the current rules to every draft once.

Every change is a flagged default or a copy of a value the canonical
entry already holds — nothing is invented, and the flags keep the
draft in Tier B. Only drafts/ is touched; the canonical folders never.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from extract import _normalize_findings  # noqa: E402

BUCKETS = ("regions", "impairments", "therapies", "predictors", "reviews")


def _citation_of(content: str) -> str | None:
    m = re.search(r"^\s*citation:\s*['\"]?(@[\w\-]+)", content, re.M)
    return m.group(1) if m else None


def _cli(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--execute", action="store_true")
    ap.add_argument("--draft", type=Path, action="append", help="only these drafts")
    args = ap.parse_args(argv)

    drafts = list(args.draft or [])
    if not drafts:
        for b in BUCKETS:
            drafts += sorted((ROOT / "drafts" / b).glob("*.md"))
    n_changed = 0
    for d in drafts:
        bucket = d.parent.name
        content = d.read_text(encoding="utf-8")
        new, notes = _normalize_findings(content, bucket, _citation_of(content), ROOT)
        if new == content:
            continue
        n_changed += 1
        print(f"{'fixed' if args.execute else 'would fix':10} {d.relative_to(ROOT)}")
        for n in notes:
            print(f"             {n}")
        if args.execute:
            d.write_text(new, encoding="utf-8")
    print(f"\n{n_changed} of {len(drafts)} draft(s) "
          + ("rewritten." if args.execute else "would change. Add --execute to apply."))
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
