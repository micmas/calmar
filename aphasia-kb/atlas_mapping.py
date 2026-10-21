"""Curated mapping from atlas labels to knowledge-base regions (atlas_mapping/).

A lesion's overlap with atlas regions (one table per atlas, from the CALMaR
reporting job) is turned into damage per *anatomical unit* (units.yaml) and
hemisphere, then per *knowledge-base region* (kb_regions.yaml). Findings are
then matched by exact region name, never by guessing from label text. The
rules and every judgement call are documented in atlas_mapping/README.md;
atlas_mapping/MAPPING.md is the table generated from the YAML files
(``python atlas_mapping.py --write-table``).

Damage measures, per unit or region and side:
  lesion_pct   share of the whole lesion inside it (%); a region counts as
               damaged when this reaches the report's minimum (5 % by default)
  region_pct   share of the unit or region destroyed (%), or None when the
               overlap table predates per-hemisphere region sizes
"""
from __future__ import annotations

import argparse
import json
from functools import lru_cache
from pathlib import Path

import pandas as pd
import yaml

DIR = Path(__file__).resolve().parent / "atlas_mapping"
SIDES = ("left", "right")


@lru_cache(maxsize=4)
def load(directory: str = str(DIR)):
    """``(units, regions, unmapped)`` from the mapping files."""
    d = Path(directory)
    units = yaml.safe_load((d / "units.yaml").read_text())["units"]
    data = yaml.safe_load((d / "kb_regions.yaml").read_text())
    return units, data["regions"], data.get("unmapped") or {}


def load_gaps(directory: str = str(DIR)) -> dict:
    """Areas needing more evidence (evidence_gaps.yaml)."""
    path = Path(directory) / "evidence_gaps.yaml"
    return (yaml.safe_load(path.read_text()) or {}).get("gaps", {}) if path.exists() else {}


def citation_status(root: Path = DIR.parent) -> dict[str, str]:
    """``@Key -> status tag`` from citations.md (extracted, cited, seed, ...)."""
    import re
    text = (Path(root) / "citations.md").read_text(encoding="utf-8")
    return {f"@{k}": tag for k, tag in re.findall(r"^## @(\S+)\s+\[([^\]]+)\]", text, re.M)}


def atlas_labels(directory: str = str(DIR)) -> dict[str, list[str]]:
    data = json.loads((Path(directory) / "atlas_labels.json").read_text())
    return {k: v for k, v in data.items() if not k.startswith("_")}


def unit_labels(unit: dict, side: str) -> list[str]:
    """Atlas labels of a unit for one hemisphere (all labels when the side
    comes from the voxels)."""
    labels = unit["labels"]
    return list(labels) if isinstance(labels, list) else list(labels.get(side) or [])


def problems(directory: str = str(DIR)) -> list[str]:
    """Inconsistencies in the mapping files (empty list = valid)."""
    units, regions, unmapped = load(directory)
    known = atlas_labels(directory)
    out = []
    for uid, unit in units.items():
        for key in ("name", "kind", "atlas", "labels", "basis"):
            if key not in unit:
                out.append(f"unit {uid}: missing {key}")
        atlas = unit.get("atlas")
        if atlas not in known:
            out.append(f"unit {uid}: unknown atlas {atlas!r}")
            continue
        labels = unit.get("labels")
        if isinstance(labels, dict) and set(labels) - set(SIDES):
            out.append(f"unit {uid}: label sides must be left/right")
        for side in SIDES:
            for label in unit_labels(unit, side):
                if label not in known[atlas]:
                    out.append(f"unit {uid}: {label!r} is not a {atlas} label")
    for rid, region in regions.items():
        if region.get("side") not in ("left", "right", "both"):
            out.append(f"region {rid}: side must be left, right or both")
        if not region.get("units"):
            out.append(f"region {rid}: no units")
        for uid in region.get("units") or []:
            if uid not in units:
                out.append(f"region {rid}: unknown unit {uid!r}")
        if not region.get("basis"):
            out.append(f"region {rid}: missing basis")
    for rid in set(regions) & set(unmapped):
        out.append(f"region {rid}: both mapped and unmapped")
    known_papers = citation_status()
    for gid, gap in load_gaps(directory).items():
        if gap.get("kind") not in ("atlas_gap", "no_evidence", "thin", "contested"):
            out.append(f"gap {gid}: unknown kind {gap.get('kind')!r}")
        for area in gap.get("areas") or []:
            if area not in units and area not in regions and area not in unmapped:
                out.append(f"gap {gid}: unknown area {area!r}")
        for paper in gap.get("papers") or []:
            if paper not in known_papers:
                out.append(f"gap {gid}: {paper} is not in citations.md")
    return out


def area_evidence(findings: pd.DataFrame, directory: str = str(DIR)) -> dict[str, tuple[int, int]]:
    """``area -> (findings, papers)`` for every unit and KB region name: region
    findings directly, unit findings through every region mapped to the unit."""
    _, regions, _ = load(directory)
    loc = findings[(findings["source_kind"] == "region")
                   | ((findings["source_kind"] == "impairment") & (findings["target_kind"] == "region"))]
    if loc.empty:
        return {}
    names = loc.apply(lambda r: r["source_id"] if r["source_kind"] == "region" else r["target"], axis=1)
    cites: dict[str, list] = {}
    for name, citation in zip(names, loc["citation"]):
        cites.setdefault(name, []).append(citation)
        for unit in (regions.get(name) or {}).get("units", []):
            cites.setdefault(unit, []).append(citation)
    return {k: (len(v), len({c for c in v if isinstance(c, str)})) for k, v in cites.items()}


def gaps_markdown(findings: pd.DataFrame, directory: str = str(DIR)) -> str:
    """EVIDENCE_GAPS.md: each gap with its areas' current evidence and the
    suggested papers' extraction status."""
    evidence = area_evidence(findings, directory)
    status = citation_status()
    kinds = {"atlas_gap": "atlas gap: no atlas label, findings unreachable",
             "no_evidence": "no evidence: measured but no findings",
             "thin": "thin evidence", "contested": "contested in the literature"}
    lines = ["# Areas that need more evidence (generated)", "",
             "Generated from `evidence_gaps.yaml` and the current knowledge base by",
             "`python atlas_mapping.py --write-table`. Counts are findings / distinct papers (all statuses).",
             "Suggested papers are `[seed]` entries in `citations.md` until extracted.", ""]
    for gid, gap in load_gaps(directory).items():
        areas = ", ".join(f"`{a}` ({evidence.get(a, (0, 0))[0]} / {evidence.get(a, (0, 0))[1]})"
                          for a in gap.get("areas") or [])
        papers = ", ".join(f"{p} [{status.get(p, 'missing')}]" for p in gap.get("papers") or []) or "— (atlas change)"
        lines += [f"## {gid.replace('_', ' ')}", "", f"**Kind:** {kinds[gap['kind']]}  ", f"**Areas:** {areas}  ",
                  f"**Suggested papers:** {papers}", "", " ".join(str(gap.get('need', '')).split()), ""]
    return "\n".join(lines)


def _side_rows(rows: pd.DataFrame, labels: list[str], side: str, from_voxels: bool):
    """Overlap and region voxels of ``labels`` on one side."""
    hit = rows[rows["region"].isin(labels)]
    if hit.empty:
        return 0, None
    if from_voxels:
        overlap = int(hit[f"{side}_overlap_voxels"].sum()) if f"{side}_overlap_voxels" in hit else 0
        column = f"{side}_region_voxels"
        size = int(hit[column].sum()) if column in hit and hit[column].notna().all() else None
    else:
        overlap = int(hit["overlap_voxels"].sum())
        size = int(hit["total_region_voxels"].sum())
    return overlap, size


def unit_damage(rows_by_atlas: dict[str, pd.DataFrame], directory: str = str(DIR)) -> pd.DataFrame:
    """Damage per unit and side for one participant.

    ``rows_by_atlas``: the participant's rows of each atlas overlap table
    (columns region, overlap_voxels, total_region_voxels, total_lesion_voxels,
    left/right_overlap_voxels and, in newer tables, left/right_region_voxels).
    A unit whose atlas has no table is reported with ``measured`` False.
    """
    units, _, _ = load(directory)
    out = []
    for uid, unit in units.items():
        rows = rows_by_atlas.get(unit["atlas"])
        from_voxels = isinstance(unit["labels"], list)
        for side in SIDES:
            if rows is None:
                out.append(dict(unit=uid, side=side, atlas=unit["atlas"], measured=False,
                                overlap_voxels=0, lesion_pct=0.0, region_pct=None))
                continue
            total = int(rows["total_lesion_voxels"].iloc[0]) if len(rows) else 0
            overlap, size = _side_rows(rows, unit_labels(unit, side), side, from_voxels)
            out.append(dict(unit=uid, side=side, atlas=unit["atlas"], measured=True, overlap_voxels=overlap,
                            lesion_pct=100.0 * overlap / total if total else 0.0,
                            region_pct=(100.0 * overlap / size) if size else None))
    return pd.DataFrame(out)


def region_damage(units_df: pd.DataFrame, directory: str = str(DIR)) -> pd.DataFrame:
    """Damage per knowledge-base region, on its side (both sides for ``side: both``).

    Within one atlas the region's units do not overlap, so their shares are
    added. Labels of different atlases can overlap (XTRACT's arcuate and JHU's
    SLF), so across atlases the larger value is taken, never the sum.
    """
    _, regions, _ = load(directory)
    by_key = {(r.unit, r.side): r for r in units_df.itertuples()}
    out = []
    for rid, region in regions.items():
        sides = SIDES if region["side"] == "both" else (region["side"],)
        parts = [by_key[(u, s)] for u in region["units"] for s in sides if (u, s) in by_key]
        per_atlas = []
        for atlas in dict.fromkeys(p.atlas for p in parts):
            own = [p for p in parts if p.atlas == atlas]
            hit = [p for p in own if p.overlap_voxels]
            sizes = [p.overlap_voxels / (p.region_pct / 100.0) for p in own if p.region_pct]
            complete = all(p.region_pct is not None or not p.overlap_voxels for p in own)
            per_atlas.append(dict(
                lesion_pct=sum(p.lesion_pct for p in own),
                region_pct=(100.0 * sum(p.overlap_voxels for p in hit) / sum(sizes)) if hit and sizes and complete else None,
                measured=any(p.measured for p in own)))
        best = max(per_atlas, key=lambda d: (d["region_pct"] or 0, d["lesion_pct"]), default=None)
        out.append(dict(
            region=rid, side=region["side"], measured=any(d["measured"] for d in per_atlas),
            lesion_pct=best["lesion_pct"] if best else 0.0, region_pct=best["region_pct"] if best else None,
            units_hit=[p.unit for p in parts if p.overlap_voxels], review=bool(region.get("review"))))
    return pd.DataFrame(out)


def coverage(findings: pd.DataFrame, directory: str = str(DIR)) -> dict:
    """How much location evidence the mapping can reach.

    Counts findings anchored on a region entry, or naming a region as the
    target of an impairment finding: mapped / listed as unmappable / missing
    from the mapping (``missing`` should be empty).
    """
    _, regions, unmapped = load(directory)
    loc = findings[(findings["source_kind"] == "region")
                   | ((findings["source_kind"] == "impairment") & (findings["target_kind"] == "region"))]
    names = loc.apply(lambda r: r["source_id"] if r["source_kind"] == "region" else r["target"], axis=1)
    counts = names.value_counts().to_dict() if len(loc) else {}
    return {"findings": int(len(loc)),
            "mapped": int(sum(n for k, n in counts.items() if k in regions)),
            "unmappable": {k: n for k, n in counts.items() if k in unmapped},
            "missing": {k: n for k, n in counts.items() if k not in regions and k not in unmapped}}


def markdown_table(directory: str = str(DIR)) -> str:
    """MAPPING.md: every unit and region with its labels, basis and review flag."""
    units, regions, unmapped = load(directory)
    lines = ["# Atlas → knowledge-base mapping (generated)", "",
             "Generated from `units.yaml` and `kb_regions.yaml` by `python atlas_mapping.py --write-table`;",
             "do not edit by hand. Rules and decisions: [README.md](README.md). ⚑ = judgement call to review.", "",
             "## Anatomical units", "", "| Unit | Atlas | Labels | Basis |", "|---|---|---|---|"]
    for uid, u in units.items():
        labels = u["labels"]
        text = ("; ".join(labels) + " (side from voxels)" if isinstance(labels, list)
                else " / ".join(f"{s}: {', '.join(labels.get(s) or [])}" for s in SIDES))
        lines.append(f"| {'⚑ ' if u.get('review') else ''}`{uid}` {u['name']} | {u['atlas']} | {text} | {u['basis']} |")
    lines += ["", "## Knowledge-base regions", "", "| Region | Side | Units | Basis |", "|---|---|---|---|"]
    for rid, r in sorted(regions.items()):
        lines.append(f"| {'⚑ ' if r.get('review') else ''}`{rid}` | {r['side']} | "
                     f"{', '.join(f'`{u}`' for u in r['units'])} | {r['basis']} |")
    lines += ["", "## Not mappable", "", "| Region | Reason |", "|---|---|"]
    lines += [f"| `{rid}` | {reason} |" for rid, reason in sorted(unmapped.items())]
    return "\n".join(lines) + "\n"


def _cli():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write-table", action="store_true", help="regenerate atlas_mapping/MAPPING.md")
    parser.add_argument("--coverage", action="store_true", help="location findings reachable through the mapping")
    args = parser.parse_args()
    found = problems()
    print("\n".join(found) if found else "Mapping files are consistent.")
    kb = None
    if args.write_table or args.coverage:
        from aphasia_kb import KnowledgeBase
        kb = KnowledgeBase(Path(__file__).parent, include=("approved", "in_review", "draft"))
    if args.write_table:
        (DIR / "MAPPING.md").write_text(markdown_table())
        (DIR / "EVIDENCE_GAPS.md").write_text(gaps_markdown(kb.findings))
        print(f"Wrote {DIR / 'MAPPING.md'} and {DIR / 'EVIDENCE_GAPS.md'}")
    if args.coverage:
        c = coverage(kb.findings)
        print(f"{c['mapped']}/{c['findings']} location findings name a mapped region; "
              f"{sum(c['unmappable'].values())} name an unmappable one; missing from the mapping: {c['missing'] or 'none'}")


if __name__ == "__main__":
    _cli()
