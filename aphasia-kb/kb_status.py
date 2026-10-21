#!/usr/bin/env python3
"""
kb_status.py — what is in the knowledge base, who approved it, and what
what a lesion can actually reach through the atlas mapping.

    python kb_status.py                 # human-readable summary
    python kb_status.py --json          # the same as JSON (for figures/CI)
    python kb_status.py --papers-needed # citation keys + DOIs the canonical
                                        # KB depends on, for re-downloading
                                        # into papers/
    python kb_status.py --tag-legacy    # stamp `review_tier: legacy` on
                                        # approved entries that were not
                                        # approved by a named person
                                        # (GOVERNANCE.md §5); idempotent

Sections of the summary
-----------------------
* entries and findings per bucket
* review provenance: human / model / legacy / none, per bucket
* relationship types and strength ratings across findings
* atlas reachability: which KB region entries the curated mapping
  (atlas_mapping/) lets a lesion reach, and which cannot be reached and why
* papers: cited keys, which have a DOI in citations.md, and which have a
  PDF in papers/

Nothing here calls a model or the network.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from aphasia_kb import parse_markdown, reviewer_kind  # noqa: E402
from phase import finding_phase  # noqa: E402

BUCKETS = ("regions", "impairments", "therapies", "predictors",
           "reviews", "ingredients")


def _entries(root: Path) -> list[tuple[str, Path, dict, str]]:
    out = []
    for b in BUCKETS:
        d = root / b
        if not d.is_dir():
            continue
        for p in sorted(d.glob("*.md")):
            fm, body = parse_markdown(p)
            if fm:
                out.append((b, p, fm, body))
    return out


def _citation_dois(root: Path) -> dict[str, dict]:
    """@Key -> {doi, title, status} from citations.md."""
    cites: dict[str, dict] = {}
    path = root / "citations.md"
    if not path.exists():
        return cites
    cur = None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^##\s+(@\S+)\s*(\[(.*?)\])?", line)
        if m:
            cur = m.group(1)
            cites[cur] = {"doi": None, "title": None,
                          "status": m.group(3)}
            continue
        if cur is None:
            continue
        if cites[cur]["title"] is None and line.strip() and \
                not line.startswith((">", "*", "doi", "#")) and \
                not re.match(r"^[A-Z][^.]*\.$", line.strip()) is None:
            pass
        md = re.search(r"doi:\s*(10\.\S+)", line, re.I)
        if md and cites[cur]["doi"] is None:
            cites[cur]["doi"] = md.group(1).rstrip(".,;")
    return cites


def _decoder_map(root: Path) -> dict[str, str]:
    """HO_LABEL_TO_KB_REGION from decode_lesion.py, read from the source
    text so this script does not need nibabel/nilearn installed."""
    src = root / "decode_lesion.py"
    if not src.exists():
        return {}
    text = src.read_text(encoding="utf-8")
    m = re.search(r"HO_LABEL_TO_KB_REGION\s*=\s*\{(.*?)\n\}", text, re.S)
    if not m:
        return {}
    return dict(re.findall(r'"([^"]+)"\s*:\s*"([^"]+)"', m.group(1)))


def collect(root: Path) -> dict:
    entries = _entries(root)
    per_bucket = {b: {"entries": 0, "findings": 0,
                      "review": collections.Counter()} for b in BUCKETS}
    rel = collections.Counter()
    strength = collections.Counter()
    methods = collections.Counter()
    phase = collections.Counter()
    phase_stated = 0
    cited: dict[str, set] = collections.defaultdict(set)
    region_findings: dict[str, int] = {}
    legacy_candidates: list[Path] = []

    for b, p, fm, _ in entries:
        pb = per_bucket[b]
        pb["entries"] += 1
        fs = [f for f in (fm.get("findings") or []) if isinstance(f, dict)]
        pb["findings"] += len(fs)
        kind = reviewer_kind(fm.get("reviewer"), fm.get("review_tier"))
        pb["review"][kind] += 1
        if fm.get("status") == "approved" and kind in ("legacy",) \
                and fm.get("review_tier") != "legacy":
            legacy_candidates.append(p)
        if b == "regions":
            region_findings[fm.get("id")] = len(fs)
        for f in fs:
            rel[str(f.get("relationship"))] += 1
            strength[str(f.get("strength"))] += 1
            ph, src = finding_phase(f)
            phase[ph] += 1
            phase_stated += src == "stated"
            m = f.get("method")
            for mm in (m if isinstance(m, list) else [m]):
                methods[str(mm)] += 1
            c = f.get("citation")
            if c:
                cited[str(c)].add(f"{b}/{p.name}")

    # Atlas reachability: which region findings a report can reach from lesion
    # location, through the curated mapping (atlas_mapping/; README there).
    import atlas_mapping
    _, mapped, unmapped = atlas_mapping.load()
    reachable = {rid: {"units": mapped[rid]["units"], "side": mapped[rid]["side"],
                       "findings": n, "review": bool(mapped[rid].get("review"))}
                 for rid, n in region_findings.items() if rid in mapped}
    unreachable = {rid: {"findings": n, "reason": unmapped.get(rid, "missing from atlas_mapping/kb_regions.yaml")}
                   for rid, n in region_findings.items() if rid not in mapped}

    dois = _citation_dois(root)
    papers_dir = root / "papers"
    papers = {}
    for key, users in sorted(cited.items()):
        k = key.lstrip("@")
        pdf = any((papers_dir / f"{k}{ext}").exists() for ext in (".pdf", ".txt"))
        papers[key] = {"doi": (dois.get(key) or {}).get("doi"),
                       "pdf_present": pdf,
                       "used_by": sorted(users)}

    # files in papers/ that no cited key claims — usually a naming slip
    unmatched: list[str] = []
    if papers_dir.is_dir():
        # any key in citations.md counts, not only those canonical
        # entries cite — drafts and not-yet-extracted papers live there too
        keys = {k.lstrip("@") for k in cited} | {k.lstrip("@") for k in dois}
        for f in sorted(papers_dir.iterdir()):
            if f.suffix.lower() not in (".pdf", ".txt") or f.name.startswith("."):
                continue
            stem = f.stem
            if stem.endswith("_annotated"):
                continue
            if stem not in keys:
                unmatched.append(f.name)

    total_review = collections.Counter()
    for b in BUCKETS:
        total_review.update(per_bucket[b]["review"])
        per_bucket[b]["review"] = dict(per_bucket[b]["review"])

    return {
        "as_of": dt.date.today().isoformat(),
        "entries": sum(v["entries"] for v in per_bucket.values()),
        "findings": sum(v["findings"] for v in per_bucket.values()),
        "papers_cited": len(cited),
        "per_bucket": per_bucket,
        "review_total": dict(total_review),
        "relationship": dict(rel),
        "strength": dict(strength),
        "phase": dict(phase.most_common()),
        "phase_stated": phase_stated,
        "methods": dict(methods.most_common()),
        "atlas_mapping": {"reachable": reachable, "unreachable": unreachable},
        "papers": papers,
        "papers_unmatched": unmatched,
        "_legacy_candidates": [str(p.relative_to(root)) for p in legacy_candidates],
    }


def print_summary(st: dict) -> None:
    print(f"Aphasia KB status — {st['as_of']}")
    print(f"  {st['entries']} entries · {st['findings']} findings · "
          f"{st['papers_cited']} papers cited\n")
    print(f"  {'bucket':<13}{'entries':>8}{'findings':>10}   review provenance")
    for b, v in st["per_bucket"].items():
        rv = ", ".join(f"{k} {n}" for k, n in sorted(v["review"].items()))
        print(f"  {b:<13}{v['entries']:>8}{v['findings']:>10}   {rv}")
    rt = st["review_total"]
    print(f"\n  Approved by a named person: {rt.get('human', 0)} · "
          f"model: {rt.get('model', 0)} · pre-policy (legacy): "
          f"{rt.get('legacy', 0)} · no reviewer: {rt.get('none', 0)}")
    if st["_legacy_candidates"]:
        print(f"  {len(st['_legacy_candidates'])} entries lack the "
              f"`review_tier: legacy` stamp — run --tag-legacy")

    if st.get("phase"):
        print("\n  Findings by recovery phase (v2.6; inferred from time_post_onset "
              f"where not stated — {st.get('phase_stated', 0)} stated): "
              + ", ".join(f"{k} {v}" for k, v in st["phase"].items()))
    print("\n  Findings by relationship: " +
          ", ".join(f"{k} {v}" for k, v in
                    sorted(st["relationship"].items(), key=lambda x: -x[1])))
    print("  Findings by strength:     " +
          ", ".join(f"{k} {v}" for k, v in
                    sorted(st["strength"].items(), key=lambda x: -x[1])))
    print("  Methods (top 6):          " +
          ", ".join(f"{k} {v}" for k, v in list(st["methods"].items())[:6]))

    d = st["atlas_mapping"]
    n_reach = sum(v["findings"] for v in d["reachable"].values())
    n_not = sum(v["findings"] for v in d["unreachable"].values())
    print(f"\n  Atlas reachability (curated mapping, atlas_mapping/): region entries with "
          f"{n_reach} findings reachable, {n_not} not")
    if d["unreachable"]:
        print("  Region entries a lesion cannot reach:")
        for rid, info in sorted(d["unreachable"].items(), key=lambda x: -x[1]["findings"]):
            print(f"    {rid:<40} {info['findings']:>3} findings  ({info['reason'][:70]})")

    missing = [k for k, v in st["papers"].items() if not v["pdf_present"]]
    print(f"\n  Papers: {len(st['papers'])} cited, "
          f"{len(st['papers']) - len(missing)} with a PDF in papers/, "
          f"{len(missing)} missing  (--papers-needed lists them with DOIs)")
    if st.get("papers_unmatched"):
        print(f"  {len(st['papers_unmatched'])} file(s) in papers/ match no "
              f"cited key (rename to <Key>.pdf): "
              + ", ".join(st["papers_unmatched"][:6])
              + (" …" if len(st["papers_unmatched"]) > 6 else ""))


def print_papers_needed(st: dict) -> None:
    print("# Papers the canonical KB depends on and that are not in papers/")
    print("# key | doi | used by")
    for key, v in st["papers"].items():
        if v["pdf_present"]:
            continue
        doi = v["doi"] or "(no DOI in citations.md)"
        print(f"{key} | {doi} | {'; '.join(v['used_by'])}")


def tag_legacy(root: Path, dry_run: bool = False) -> int:
    """Stamp `review_tier: legacy` on approved entries whose reviewer is
    not a named person (GOVERNANCE.md §5).

    The stamp is inserted as one line after `status:` in the frontmatter
    — the file is NOT re-serialised, so the diff is exactly one added
    line per entry. Entries with no reviewer at all (currently the RTSS
    ingredients) are reported, not tagged: they fail validation already
    and need a reviewer, not a tier.
    """
    n = 0
    no_reviewer: list[str] = []
    for b, p, fm, _ in _entries(root):
        if fm.get("status") != "approved" or fm.get("review_tier") == "legacy":
            continue
        kind = reviewer_kind(fm.get("reviewer"), fm.get("review_tier"))
        if kind == "human":
            continue
        if kind == "none":
            no_reviewer.append(f"{b}/{p.name}")
            continue
        n += 1
        print(f"  legacy: {b}/{p.name}  (reviewer: {fm.get('reviewer')!r})")
        if dry_run:
            continue
        text = p.read_text(encoding="utf-8")
        head, sep, rest = text.partition("\n---")
        if not text.startswith("---") or not sep:
            print(f"  ! {p.name}: no frontmatter; skipped", file=sys.stderr)
            n -= 1
            continue
        lines = head.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("status:"):
                lines.insert(i + 1, "review_tier: legacy")
                break
        else:
            lines.append("review_tier: legacy")
        p.write_text("\n".join(lines) + sep + rest, encoding="utf-8")
    if no_reviewer:
        print(f"  {len(no_reviewer)} approved entries have no reviewer at "
              f"all (fix with a reviewer, not a tier): "
              f"{', '.join(no_reviewer[:4])}{' …' if len(no_reviewer) > 4 else ''}")
    if not dry_run and n:
        log = root / "extraction_log.md"
        with log.open("a", encoding="utf-8") as fh:
            fh.write(f"{dt.date.today().isoformat()} | LEGACY-TAGGED | — | "
                     f"{n} entries | review_tier: legacy stamped per "
                     f"GOVERNANCE.md §5\n")
    return n


def _cli(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--papers-needed", action="store_true")
    ap.add_argument("--tag-legacy", action="store_true")
    ap.add_argument("--dry-run", action="store_true",
                    help="with --tag-legacy: list, do not write")
    args = ap.parse_args(argv)

    if args.tag_legacy:
        n = tag_legacy(args.root, dry_run=args.dry_run)
        print(f"{'would tag' if args.dry_run else 'tagged'} {n} entries")
        return 0
    st = collect(args.root)
    if args.json:
        st.pop("_legacy_candidates", None)
        print(json.dumps(st, indent=2))
    elif args.papers_needed:
        print_papers_needed(st)
    else:
        print_summary(st)
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
