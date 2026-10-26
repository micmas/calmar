#!/usr/bin/env python3
"""Export the knowledge base for the CALMaR webapp (neurodesk/webapps, apps/calmar).

The webapp has no Python: it loads one JSON asset and re-implements, in
JavaScript, the parts of the participant report that turn a lesion into
cited findings (``atlas_mapping.unit_damage`` / ``region_damage``,
``KnowledgeBase.location_findings`` / ``interpret_damage`` /
``interpret_therapies`` and the display rules of ``aphasia_rules``). This
script writes everything that logic needs:

* the entries (regions, impairments, therapies, predictors, ingredients) in
  the statuses selected, with the names the report shows;
* every finding, flat (as ``KnowledgeBase.findings``) plus the nested blocks
  the report's disclosure panels show (sample, statistics, author
  limitations, source passages, review provenance);
* the curated atlas mapping (``atlas_mapping/units.yaml``, ``kb_regions.yaml``)
  and the disconnectome bundle mapping (``atlas_mapping/disconnectome.yaml``);
* the rule tables of ``aphasia_rules`` (score weights, display bins, aphasia
  type ids, recovery stages of each therapy's evidence);
* the bibliography (``citations.md``), keyed by ``@Key``.

``--fixtures DIR`` also writes parity fixtures: synthetic overlap tables with
the outputs the Python code produces for them, which the webapp's Node tests
replay against the JavaScript port.

    python aphasia-kb/export_webapp.py --out ../webapps/apps/calmar/web/models/annotations/aphasia-kb.json
    python aphasia-kb/export_webapp.py --include approved,in_review --out kb.json
    python aphasia-kb/export_webapp.py --fixtures ../webapps/apps/calmar/tests/fixtures/kb-parity
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import aphasia_kb  # noqa: E402
import aphasia_rules  # noqa: E402
import atlas_mapping  # noqa: E402

SCHEMA_VERSION = 1
ENTRY_FIELDS = ("id", "name", "kind", "aliases", "short_description", "status", "reviewer", "review_tier",
                "targets_impairments", "rtss_ingredients", "rtss_category", "direction_of_severity", "units",
                "predictor_type")
FINDING_RAW_FIELDS = ("relationship", "design", "sample", "statistics", "author_limitations", "source_passages",
                      "region_definition", "primary_papers_cited", "instrument")
# Columns of KnowledgeBase.findings the webapp reads (the rest are tooling).
FINDING_FLAT_FIELDS = ("source_id", "source_kind", "source_status", "source_path", "id", "target", "target_kind",
                       "claim", "direction", "citation", "method", "design", "evidence_quality", "strength",
                       "sample_n", "population", "time_post_onset", "phase", "phase_source", "stat_threshold",
                       "stat_effect_size", "confidence", "flags", "reviewer", "review_tier", "review_kind",
                       # v2.7 (lesion_mapping.py): how a lesion-mapping finding was obtained, and its cohort group
                       "lm_analysis", "lm_n", "lm_volume_correction", "lm_correction", "lm_source", "lm_orientation",
                       "design_cautions", "cohort", "cohort_source", "cohort_group")
SAMPLE_PHASE_STAGES = {"hyperacute": "acute", "acute": "acute", "early_subacute": "subacute",
                       "late_subacute": "subacute", "chronic": "chronic"}


def _clean(value):
    """JSON-safe copy: NaN -> None, numpy scalars -> Python, tuples -> lists."""
    if isinstance(value, dict):
        return {str(k): _clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_clean(v) for v in value]
    if isinstance(value, float) and math.isnan(value):
        return None
    if hasattr(value, "item") and not isinstance(value, (str, bytes)):
        try:
            return _clean(value.item())
        except (ValueError, AttributeError):
            pass
    if isinstance(value, (date, pd.Timestamp)):
        return value.isoformat()
    return value


def _rel(path, root):
    try:
        return str(Path(path).resolve().relative_to(Path(root).resolve()))
    except ValueError:
        return str(path)


def citations(root: Path) -> dict[str, str]:
    """``@Key -> full citation text`` from citations.md (report_evidence._evidence_context)."""
    return {key: text for key, (text, _) in _citation_blocks(root).items()}


def citation_links(root: Path) -> dict[str, str]:
    """``@Key -> https://doi.org/...`` for every entry whose block carries a ``doi:`` line (or a URL)."""
    return {key: link for key, (_, link) in _citation_blocks(root).items() if link}


_DOI = re.compile(r"^(?:doi:\s*|https?://(?:dx\.)?doi\.org/)(10\.\S+)$", re.I)
_URL = re.compile(r"^(https?://\S+)$", re.I)


def _citation_blocks(root: Path) -> dict[str, tuple[str, str | None]]:
    out = {}
    text = (root / "citations.md").read_text(encoding="utf-8")
    for block in re.split(r"^## (?=@)", text, flags=re.M)[1:]:
        heading, _, body = block.partition("\n")
        key = heading.split()[0]
        lines = []
        link = None
        for line in body.splitlines():
            line = line.strip()
            if line.startswith((">", "#", "---")):
                if lines:
                    break
                continue
            if not line:
                continue
            doi = _DOI.match(line)
            if doi and link is None:
                link = f"https://doi.org/{doi.group(1).rstrip('.')}"
            elif _URL.match(line) and link is None:
                link = _URL.match(line).group(1)
            lines.append(re.sub(r"\*([^*]+)\*", r"\1", line))
        out[key] = (" ".join(lines), link)
    return out


def entries(kb) -> dict:
    out = {}
    for table in (kb.regions, kb.impairments, kb.therapies, kb.predictors, kb.ingredients):
        if table is None or table.empty:
            continue
        for _, row in table.iterrows():
            entry = {k: _clean(row.get(k)) for k in ENTRY_FIELDS if k in row and _present(row.get(k))}
            entry["bucket"] = str(row.get("_kind_bucket") or "")
            out[str(row["id"])] = entry
    return out


def _present(value):
    if value is None:
        return False
    if isinstance(value, (list, tuple, set, dict, str)):
        return bool(value)
    try:
        return not pd.isna(value)
    except (TypeError, ValueError):
        return True


def findings(kb, root: Path) -> list:
    """Flat rows merged with the nested blocks of the raw finding."""
    raw = {}
    for table in (kb.regions, kb.impairments, kb.therapies, kb.predictors):
        if table is None or table.empty:
            continue
        for _, entry in table.iterrows():
            for finding in entry.get("findings") or []:
                raw[(str(entry.get("_path") or ""), finding.get("id"))] = finding
    out = []
    for _, row in kb.findings.iterrows():
        item = {k: _clean(row.get(k)) for k in FINDING_FLAT_FIELDS if k in row}
        item["source_path"] = _rel(item.get("source_path") or "", root)
        nested = raw.get((str(row.get("source_path") or ""), row.get("id")), {})
        for key in FINDING_RAW_FIELDS:
            if _present(nested.get(key)):
                item[key] = _clean(nested[key])
        review = nested.get("review") or {}
        if review:
            item["review"] = _clean(review)
        item["stages"] = sorted(finding_stages(item))
        out.append(item)
    return out


def finding_stages(item) -> set:
    """report_evidence.finding_phases for one exported finding."""
    stage = SAMPLE_PHASE_STAGES.get(item.get("phase"))
    if stage:
        return {stage}
    text = " ".join(str(item.get(k) or "") for k in ("population", "time_post_onset"))
    return aphasia_rules.stages_in_population(text)


def rules(kb_root: Path) -> dict:
    return {
        "strengthWeight": aphasia_kb._STRENGTH_WEIGHT,
        "evidenceWeight": aphasia_kb._EVIDENCE_WEIGHT,
        "confidenceWeight": aphasia_kb._CONFIDENCE_WEIGHT,
        "directionSign": aphasia_kb._DIRECTION_SIGN,
        # v2.7: lesion-mapping findings whose design leaves the result less trustworthy
        # (Moore et al. 2026) are graded down: each of these multiplies the weight.
        "designPenalty": getattr(aphasia_kb, "DESIGN_PENALTY", 0.8),
        "designStrongVolumeControl": ["direct", "covariate"],
        "designWeakCorrection": ["uncorrected", "not_reported"],
        "evidenceStrengthBins": [[upper, stars, label] for upper, stars, label in aphasia_rules.EVIDENCE_STRENGTH_BINS],
        "aphasiaTypes": sorted(aphasia_rules.APHASIA_COMPONENTS),
        "aphasiaLabels": dict(aphasia_rules.APHASIA_LABELS),
        "recoveryStages": [[sid, label, lo, hi] for sid, label, lo, hi in aphasia_rules.RECOVERY_STAGES],
        "stagePatterns": [[sid, pattern.pattern] for sid, pattern in aphasia_rules.THERAPY_STAGE_PATTERNS],
        "samplePhaseStages": SAMPLE_PHASE_STAGES,
        "therapyEvidenceStages": {k: sorted(v) for k, v in aphasia_rules.therapy_evidence_stages(kb_root).items()},
        "defaults": {"minOverlapPct": 5.0, "minRegionPct": 25.0, "minDisconnectedPct": 50.0, "topN": 5,
                     "maxEvidenceRegions": 8, "minSummaryCitations": 2, "minSummaryAnatomies": 2,
                     "thinStudies": 2},
    }


def mapping() -> dict:
    units, regions, unmapped = atlas_mapping.load()
    disco = yaml.safe_load((atlas_mapping.DIR / "disconnectome.yaml").read_text()) or {}
    return {
        "units": units,
        "regions": regions,
        "unmapped": unmapped,
        "atlasLabels": atlas_mapping.atlas_labels(),
        "disconnectome": {
            "atlas": disco.get("atlas", "ENIGMA"),
            "units": disco.get("units") or {},
            "extraUnits": disco.get("extra_units") or {},
            "extraRegions": disco.get("extra_regions") or {},
        },
    }


def version(root: Path, kb) -> dict:
    """KB commit (if under git) and a content digest of what the export read."""
    def git(*args):
        try:
            done = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, timeout=20)
        except (OSError, subprocess.TimeoutExpired):
            return None
        return done.stdout.strip() if done.returncode == 0 else None
    commit = git("log", "-1", "--format=%h %cs", "--", *[str(root / p) for p in (
        "regions", "impairments", "therapies", "predictors", "reviews", "ingredients", "citations.md",
        "atlas_mapping", "aphasia_kb.py", "aphasia_rules.py")])
    digest = hashlib.sha256()
    for path in sorted(root.glob("*/*.md")) + sorted((root / "atlas_mapping").glob("*.yaml")) + [root / "citations.md"]:
        if path.parent.name in ("drafts", "examples", "_legacy_v1"):
            continue
        digest.update(path.name.encode() + path.read_bytes())
    findings = kb.findings
    return {
        "commit": commit.split()[0] if commit else None,
        "date": commit.split()[1] if commit else None,
        "contentDigest": digest.hexdigest()[:16],
        "exportedOn": date.today().isoformat(),
        "papers": int(findings["citation"].dropna().nunique()) if "citation" in findings else 0,
        "findings": int(len(findings)),
        "findingsReviewed": int((findings["review_kind"] == "human").sum()) if "review_kind" in findings else 0,
        "entries": {b: int(len(getattr(kb, b))) for b in ("regions", "impairments", "therapies", "predictors")},
        "statuses": list(kb.include),
    }


def export(root: Path, include) -> dict:
    kb = aphasia_kb.KnowledgeBase(root, include=include)
    if not len(kb.regions) and not len(kb.impairments):
        raise FileNotFoundError(f"No aphasia knowledge base entries under {root}")
    return {
        "schemaVersion": SCHEMA_VERSION,
        "_comment": ("Aphasia knowledge base exported for the CALMaR webapp by aphasia-kb/export_webapp.py. "
                     "Regenerate with that script; do not edit by hand. Findings are group-level literature "
                     "associations with their citations and review provenance, not clinical predictions."),
        "version": version(root, kb),
        "entries": entries(kb),
        "findings": findings(kb, root),
        "mapping": mapping(),
        "rules": rules(root),
        "citations": citations(root),
        "citationLinks": citation_links(root),
    }


# ---------------------------------------------------------------------------
# Parity fixtures: what the Python code answers for synthetic overlap tables.
# ---------------------------------------------------------------------------

def _rows(atlas, rows, total):
    df = pd.DataFrame(rows)
    df["total_lesion_voxels"] = total
    df["atlas"] = atlas
    return df


def _ho(region, overlap, size, left_frac=1.0, left_size=None):
    left = int(round(overlap * left_frac))
    left_size = size // 2 if left_size is None else left_size
    return dict(region=region, overlap_voxels=overlap, total_region_voxels=size,
                left_overlap_voxels=left, right_overlap_voxels=overlap - left,
                left_region_voxels=left_size, right_region_voxels=size - left_size)


def _sided(region, overlap, size):
    return dict(region=region, overlap_voxels=overlap, total_region_voxels=size,
                left_overlap_voxels=overlap if region.endswith(("_L", " L")) else 0,
                right_overlap_voxels=overlap if region.endswith(("_R", " R")) else 0,
                left_region_voxels=size if region.endswith(("_L", " L")) else 0,
                right_region_voxels=size if region.endswith(("_R", " R")) else 0)


FIXTURE_CASES = {
    "left_perisylvian": {
        "total": 20000,
        "HarvardOxford": [
            _ho("Inferior Frontal Gyrus, pars opercularis", 3000, 7000, 1.0, 3500),
            _ho("Precentral Gyrus", 2000, 40000, 1.0, 20000),
            _ho("Insular Cortex", 2500, 9000, 1.0, 4500),
            _ho("Superior Temporal Gyrus, posterior division", 600, 8000, 1.0, 4000),
            _ho("Planum Temporale", 1500, 4000, 1.0, 1800),
        ],
        "AAL": [_sided("Putamen_L", 1200, 7000), _sided("Frontal_Inf_Orb_L", 100, 6000)],
        "JHU": [_sided("Superior longitudinal fasciculus L", 1900, 2000)],
        "XTRACT": [_sided("Arcuate Fasciculus L", 1500, 3000)],
    },
    "right_small": {
        "total": 800,
        "HarvardOxford": [_ho("Inferior Frontal Gyrus, pars triangularis", 600, 6000, 0.0, 3000),
                          _ho("Middle Frontal Gyrus", 200, 50000, 0.0, 25000)],
        "AAL": [],
        "JHU": [],
    },
    "no_atlas_hit": {"total": 100, "HarvardOxford": [_ho("Occipital Pole", 100, 10000)], "AAL": []},
}

DISCONNECTOME_CASES = {
    "arcuate_cut": {"Association_ArcuateFasciculusL": 0.83, "Association_SuperiorLongitudinalFasciculusL_3": 0.62,
                    "Association_SuperiorLongitudinalFasciculusL_2": 0.1, "Association_ExtremeCapsuleL": 0.55,
                    "Association_UncinateFasciculusL": 0.04, "Association_ArcuateFasciculusR": 0.0,
                    "Commissure_CorpusCallosum_ForcepsMinor": 0.3, "ProjectionBasalGanglia_OpticRadiationL": float("nan")},
}


def fixtures(root: Path, include) -> dict:
    kb = aphasia_kb.KnowledgeBase(root, include=include)
    out = {"_comment": "Generated by aphasia-kb/export_webapp.py --fixtures; the Python answers the JS port must match.",
           "include": list(include), "cases": {}, "disconnectome": {}}
    for name, case in FIXTURE_CASES.items():
        rows_by_atlas = {atlas: _rows(atlas, rows, case["total"]) for atlas, rows in case.items()
                         if atlas != "total" and rows}
        units = atlas_mapping.unit_damage(rows_by_atlas)
        damage = atlas_mapping.region_damage(units)
        location = kb.location_findings(damage, min_overlap=5.0, min_region=25.0)
        imaging = kb.interpret_damage(damage, min_overlap=5.0, min_region=25.0)
        impairments = []
        if not imaging.empty:
            symptom = imaging.apply(lambda r: _is_symptom(r["target"], r["target_kind"]), axis=1)
            impairments = list(imaging[symptom]["target"].head(10))
        therapies = kb.interpret_therapies(impairments, max_results=5)
        location_columns = ["region", "side", "lesion_pct", "region_pct", "predicts", "predicts_kind",
                            "finding_id", "source_id", "citation", "direction", "contribution"]
        if "design_w" in location.columns:
            location_columns += ["design_w", "cohort_group"]
        out["cases"][name] = {
            "input": {atlas: _clean(rows.to_dict("records")) for atlas, rows in rows_by_atlas.items()},
            "unitDamage": _clean(units.to_dict("records")),
            "regionDamage": _clean(damage.to_dict("records")),
            "locationFindings": _clean(location[location_columns].to_dict("records")) if not location.empty else [],
            "interpretDamage": _clean(imaging.to_dict("records")) if not imaging.empty else [],
            "symptomImpairments": impairments,
            "therapies": _clean(therapies.to_dict("records")) if not therapies.empty else [],
        }
    # The measures section for the one measure the webapp has: lesion volume.
    out["measures"] = {}
    f = kb.findings[kb.findings["source_kind"] == "predictor"]
    for pid in ("lesion_volume",):
        g = f[(f["source_id"] == pid) & (f["target"] != pid)]
        shown = g.drop_duplicates(subset=["claim", "citation"])
        out["measures"][pid] = {
            "findings": _clean(g[["finding_id" if "finding_id" in g.columns else "id", "target", "target_kind", "direction", "citation"]]
                               .rename(columns={"id": "finding_id"}).to_dict("records")),
            "distinct": int(len(shown)),
            "directionCounts": _clean(shown["direction"].fillna("not reported").value_counts().to_dict()),
            "directionOfSeverity": next((str(p["direction_of_severity"]) for _, p in kb.predictors.iterrows()
                                         if p["id"] == pid and isinstance(p.get("direction_of_severity"), str)), None),
        }
    for name, fractions in DISCONNECTOME_CASES.items():
        disco = disconnection_from_fractions(fractions)
        rows = kb.location_findings(disco, min_overlap=101.0, min_region=50.0)
        out["disconnectome"][name] = {
            "fractions": {k: (None if isinstance(v, float) and math.isnan(v) else v) for k, v in fractions.items()},
            "regionDisconnection": _clean(disco.to_dict("records")),
            "findings": _clean(rows[["region", "side", "region_pct", "predicts", "finding_id", "source_id", "citation"]]
                               .to_dict("records")) if not rows.empty else [],
        }
    return out


def _is_symptom(target, kind):
    if kind != "impairment":
        return False
    normalized = re.sub(r"[^a-z0-9]+", "_", str(target).lower()).strip("_")
    return not (aphasia_rules.canonical_aphasia_type(target) is not None or normalized == "aphasia"
                or normalized.endswith("_aphasia"))


def disconnection_from_fractions(fractions: dict) -> pd.DataFrame:
    """The webapp's disconnection table from ENIGMA streamline fractions, in
    the columns of ``atlas_mapping.region_disconnection`` (the reference the
    JavaScript port is checked against). A unit's score is the largest
    fraction of its bundles; side comes from the bundle name, or (midline
    bundles) is reported on both sides; regions take their most disconnected
    unit on their side."""
    disco = mapping()["disconnectome"]
    units = {**{k: {"labels": v["labels"]} for k, v in disco["units"].items()},
             **{k: {"labels": v["labels"]} for k, v in disco["extraUnits"].items()}}
    _, regions, _ = atlas_mapping.load()
    regions = {**regions, **disco["extraRegions"]}
    unit_rows = {}
    for uid, unit in units.items():
        labels = unit["labels"]
        for side in atlas_mapping.SIDES:
            names = list(labels) if isinstance(labels, list) else list(labels.get(side) or [])
            values = [fractions[n] for n in names if n in fractions and not (isinstance(fractions[n], float) and math.isnan(fractions[n]))]
            unit_rows[(uid, side)] = max(values) * 100.0 if values else None
    out = []
    for rid, region in regions.items():
        if not any(u in units for u in region["units"]):
            continue
        sides = atlas_mapping.SIDES if region["side"] == "both" else (region["side"],)
        parts = [(u, s, unit_rows[(u, s)]) for u in region["units"] for s in sides
                 if (u, s) in unit_rows and unit_rows[(u, s)] is not None]
        if not parts:
            continue
        best = max(parts, key=lambda p: p[2])
        out.append(dict(region=rid, side=region["side"], measured=True, lesion_pct=0.0, region_pct=best[2],
                        units_hit=[best[0]], review=bool(region.get("review"))))
    return pd.DataFrame(out)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--root", default=str(ROOT), help="knowledge-base root (default: this folder)")
    parser.add_argument("--include", default="approved",
                        help="comma-separated entry statuses to export (default: approved)")
    parser.add_argument("--out", help="write the webapp JSON here")
    parser.add_argument("--fixtures", help="write parity fixtures (kb-parity.json) into this directory")
    parser.add_argument("--indent", type=int, default=None, help="pretty-print the JSON (default: compact)")
    args = parser.parse_args(argv)
    root = Path(args.root)
    include = tuple(s.strip() for s in args.include.split(",") if s.strip())
    if args.out:
        data = export(root, include)
        path = Path(args.out)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=args.indent, sort_keys=True) + "\n", encoding="utf-8")
        v = data["version"]
        print(f"{path}: {len(data['findings'])} findings, {len(data['entries'])} entries, "
              f"{len(data['citations'])} citations, {path.stat().st_size / 1024:.0f} KB "
              f"(KB {v['commit'] or 'uncommitted'} · digest {v['contentDigest']} · statuses {', '.join(include)})")
    if args.fixtures:
        folder = Path(args.fixtures)
        folder.mkdir(parents=True, exist_ok=True)
        data = fixtures(root, include)
        (folder / "kb-parity.json").write_text(json.dumps(data, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                                               encoding="utf-8")
        print(f"{folder / 'kb-parity.json'}: {len(data['cases'])} damage cases, {len(data['disconnectome'])} disconnectome cases")
    if not args.out and not args.fixtures:
        parser.error("nothing to do: pass --out and/or --fixtures")


if __name__ == "__main__":
    main()
