"""
promote.py — review and promote draft KB entries.

Usage:
    python promote.py --list                 # show pending drafts
    python promote.py --show drafts/regions/ho-cort_44__Fridriksson2018.md
    python promote.py --diff drafts/regions/ho-cort_44__Fridriksson2018.md
    python promote.py --approve drafts/regions/ho-cort_44__Fridriksson2018.md \
                      --reviewer "michele"
    python promote.py --reject  drafts/regions/ho-cort_44__Fridriksson2018.md \
                      --reviewer "michele" --reason "sample too small"

Approve does the following, atomically:
  1. Validates the draft against v2 schema. Refuses if invalid.
  2. Sets status: approved, reviewer:, reviewed_on:.
  3. If a file with the same id already exists in the canonical folder,
     merges the draft's findings into it (giving them fresh f-ids).
     Otherwise, moves the draft to the canonical folder.
  4. Removes the draft file.
  5. Appends a line to extraction_log.md.

This script is the *only* way an entry is supposed to leave drafts/.
"""

from __future__ import annotations

import argparse
import datetime as dt
import difflib
import re
import shutil
import sys
from pathlib import Path

import yaml

# Reuse the validator from the loader
sys.path.insert(0, str(Path(__file__).parent))
from aphasia_kb import (
    parse_markdown, _validate_v2_entry,
    KnowledgeBase,
)

ROOT = Path(__file__).parent
LOG = ROOT / "extraction_log.md"


# ============================================================
# Helpers
# ============================================================
def _read(path: Path) -> tuple[dict, str, str]:
    """Return (frontmatter_dict, body_string, full_text)."""
    text = path.read_text(encoding="utf-8")
    fm, body = parse_markdown(path)
    return fm, body, text


def _write(path: Path, fm: dict, body: str):
    """Serialize frontmatter + body back to markdown."""
    yaml_text = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True,
                               default_flow_style=False)
    path.write_text(f"---\n{yaml_text}---\n{body}", encoding="utf-8")


def _bucket_for(draft_path: Path) -> str:
    """Return regions/impairments/therapies for a draft path."""
    parts = draft_path.parts
    if "drafts" not in parts:
        raise ValueError(f"Not a drafts path: {draft_path}")
    i = parts.index("drafts")
    return parts[i + 1]


def _canonical_path_for(fm: dict, bucket: str) -> Path:
    """Where the entry should live once approved."""
    return ROOT / bucket / f"{fm['id']}.md"


def _next_finding_id(existing_ids: set[str], wanted: str) -> str:
    """If `wanted` is taken, return the next free f<n> id."""
    if wanted not in existing_ids:
        return wanted
    n = 1
    while f"f{n}" in existing_ids:
        n += 1
    return f"f{n}"


# ============================================================
# Commands
# ============================================================
def cmd_list(args):
    kb = KnowledgeBase(ROOT, include=["draft", "in_review"])
    if kb.drafts.empty:
        print("No pending drafts.")
        return
    print(f"{len(kb.drafts)} pending draft(s):\n")
    for r in kb.drafts.itertuples():
        print(f"  [{r.status:<10s}] {r.path}  ({r.n_findings} findings)")
        print(f"               id={r.id}  by={r.created_by}  on={r.created_on}")


def cmd_show(args):
    p = Path(args.show)
    print(p.read_text(encoding="utf-8"))


def cmd_diff(args):
    """Show what would change in the canonical file if this draft were approved."""
    draft = Path(args.diff)
    fm_d, body_d, text_d = _read(draft)
    canonical = _canonical_path_for(fm_d, _bucket_for(draft))
    if not canonical.exists():
        print(f"(no existing canonical file at {canonical} — draft becomes a new entry)")
        print(text_d)
        return
    text_c = canonical.read_text(encoding="utf-8")
    diff = difflib.unified_diff(
        text_c.splitlines(keepends=True),
        text_d.splitlines(keepends=True),
        fromfile=str(canonical), tofile=str(draft),
    )
    sys.stdout.writelines(diff)


def cmd_approve(args):
    draft = Path(args.approve)
    fm, body, _ = _read(draft)
    bucket = _bucket_for(draft)

    # 1. Validate
    issues = []
    _validate_v2_entry(fm, str(draft), issues)
    if issues:
        print(f"❌ Cannot approve — {len(issues)} validation issue(s):")
        for i in issues:
            print(f"  {i}")
        sys.exit(1)

    # 2. Stamp approval
    fm["status"]      = "approved"
    fm["reviewer"]    = args.reviewer
    fm["reviewed_on"] = dt.date.today().isoformat()

    # 3. Merge or move
    canonical = _canonical_path_for(fm, bucket)
    if canonical.exists():
        fm_c, body_c, _ = _read(canonical)
        existing_ids = {f.get("id") for f in (fm_c.get("findings") or [])}
        merged = list(fm_c.get("findings") or [])
        added  = []
        for f in fm.get("findings") or []:
            new_id = _next_finding_id(existing_ids, f.get("id", "f1"))
            f = dict(f)
            f["id"] = new_id
            existing_ids.add(new_id)
            merged.append(f)
            added.append(new_id)
        fm_c["findings"] = merged
        fm_c["last_reviewed"] = fm["reviewed_on"]
        _write(canonical, fm_c, body_c)
        print(f"✓ Merged {len(added)} new finding(s) ({', '.join(added)}) "
              f"into {canonical.relative_to(ROOT)}")
    else:
        canonical.parent.mkdir(parents=True, exist_ok=True)
        _write(canonical, fm, body)
        print(f"✓ Promoted {draft.name} → {canonical.relative_to(ROOT)}")

    # 4. Remove draft
    draft.unlink()

    # 5. Append log entry
    cite = "?"
    for f in fm.get("findings") or []:
        if f.get("citation"):
            cite = f["citation"]; break
    LOG.parent.mkdir(parents=True, exist_ok=True)
    line = (f"{dt.date.today().isoformat()} | APPROVED | {cite} | "
            f"{fm.get('id')} | reviewer: {args.reviewer}\n")
    with LOG.open("a") as fh:
        fh.write(line)
    print(f"  logged: {line.strip()}")


def cmd_reject(args):
    draft = Path(args.reject)
    fm, body, _ = _read(draft)
    fm["status"]   = "rejected"
    fm["reviewer"] = args.reviewer
    fm["reviewed_on"] = dt.date.today().isoformat()
    fm.setdefault("notes", "")
    fm["notes"] = (str(fm.get("notes") or "")
                   + f"\n\nRejected {dt.date.today().isoformat()} by {args.reviewer}: "
                   + (args.reason or "(no reason given)"))
    _write(draft, fm, body)
    print(f"✗ Marked rejected: {draft}")
    cite = "?"
    for f in fm.get("findings") or []:
        if f.get("citation"):
            cite = f["citation"]; break
    line = (f"{dt.date.today().isoformat()} | REJECTED | {cite} | "
            f"{fm.get('id')} | reviewer: {args.reviewer} | reason: "
            f"{args.reason or '(none)'}\n")
    with LOG.open("a") as fh:
        fh.write(line)
    print(f"  logged: {line.strip()}")


# ============================================================
# Main
# ============================================================
def main(argv=None):
    p = argparse.ArgumentParser(description="Review/promote draft KB entries")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--list",    action="store_true", help="list pending drafts")
    g.add_argument("--show",    metavar="PATH",      help="print one draft")
    g.add_argument("--diff",    metavar="PATH",      help="diff against canonical")
    g.add_argument("--approve", metavar="PATH",      help="approve a draft")
    g.add_argument("--reject",  metavar="PATH",      help="reject a draft")
    p.add_argument("--reviewer", help="your name (required for approve/reject)")
    p.add_argument("--reason",   help="reason for rejection")
    args = p.parse_args(argv)

    if args.approve and not args.reviewer:
        p.error("--approve requires --reviewer")
    if args.reject and not args.reviewer:
        p.error("--reject requires --reviewer")

    if args.list:    cmd_list(args)
    if args.show:    cmd_show(args)
    if args.diff:    cmd_diff(args)
    if args.approve: cmd_approve(args)
    if args.reject:  cmd_reject(args)


if __name__ == "__main__":
    main()
