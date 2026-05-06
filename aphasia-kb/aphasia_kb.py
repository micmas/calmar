"""
aphasia_kb.py — load, validate, and query the markdown aphasia knowledge base.

Supports schema v2 (current) and v1 (legacy, read-only). Validation enforces
the v2 controlled vocabularies and required fields documented in `schema.md`.

Usage from the LINDA notebook:

    from aphasia_kb import KnowledgeBase
    kb = KnowledgeBase("aphasia-kb")             # default: only approved entries

    kb.regions / kb.impairments / kb.therapies   # DataFrames
    kb.findings                                  # long-format findings table

    kb.lookup_region("Broca's area")
    kb.interpret_overlap(overlap_df, atlas="HarvardOxford")

    # Include drafts when reviewing (DOES NOT affect interpret_overlap by default):
    kb_with_drafts = KnowledgeBase("aphasia-kb", include=["approved", "draft", "in_review"])

CLI:

    python aphasia_kb.py                         # summary
    python aphasia_kb.py --check drafts/         # validate v2 entries in drafts
    python aphasia_kb.py --lookup "Broca's area"
    python aphasia_kb.py --issues                # print all validation issues
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Sequence

import pandas as pd
import yaml


# ============================================================
# YAML frontmatter parsing
# ============================================================

_FRONTMATTER_RE = re.compile(
    r"^---\s*\n(?P<yaml>.*?)\n---\s*\n(?P<body>.*)$",
    re.DOTALL,
)

_QUOTE_MAP = str.maketrans({
    "\u2018": "'", "\u2019": "'",
    "\u201C": '"', "\u201D": '"',
    "\u2013": "-", "\u2014": "-",
})


def _normalize(s: str) -> str:
    """Normalize for alias lookup: lowercase, straight quotes, single spaces."""
    if s is None:
        return ""
    s = str(s).translate(_QUOTE_MAP).strip().lower()
    return re.sub(r"\s+", " ", s)


def parse_markdown(path: Path) -> tuple[dict, str]:
    """Return (frontmatter_dict, body_string) for a markdown file."""
    text = path.read_text(encoding="utf-8")
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    fm = yaml.safe_load(m.group("yaml")) or {}
    return fm, m.group("body")


# ============================================================
# Controlled vocabularies (mirror schema.md exactly)
# ============================================================

STATUS_VOCAB = {"draft", "in_review", "approved", "rejected", "legacy_v1"}
DIRECTION_VOCAB = {
    "likely", "unlikely",
    "likely_responder", "unlikely_responder",
    "no_effect", "mixed",
}
STRENGTH_VOCAB = {"weak", "moderate", "strong"}
EVIDENCE_VOCAB = {
    "case-study", "cohort", "RCT", "meta-analysis", "tentative",
}
CONFIDENCE_VOCAB = {"high", "medium", "low"}
TARGET_KIND_VOCAB = {"impairment", "therapy", "region", "prognosis", "predictor"}
REGION_KIND_VOCAB = {"atlas", "classical", "network", "tract"}
PREDICTOR_TYPE_VOCAB = {"behavioural", "demographic", "clinical", "imaging_metric"}
DIRECTION_OF_SEVERITY_VOCAB = {
    "higher_is_worse", "lower_is_worse", "nonmonotonic", "not_applicable",
}
METHOD_VOCAB = {
    "LSM", "VLSM", "VBCM", "MLPA", "MVPA",
    "fMRI_activation", "fMRI_FC", "rs_fMRI",
    "DTI", "NODDI", "tractography",
    "lesion_network_mapping", "disconnectome",
    "EEG", "MEG", "TMS", "tDCS",
    "behavioral_only", "clinical_RCT", "meta-analysis",
    "computational_model",
}
# Note: this set is intentionally extensible. New analytic methods may
# be added without a schema_version bump (see schema.md "Vocabulary
# extensibility" note). Structural changes to the schema (new fields,
# new bucket types, changed required-ness) DO require a version bump.
DESIGN_VOCAB = {
    "cross-sectional", "longitudinal", "RCT",
    "case-series", "single-case", "meta-analysis", "systematic-review",
}
IMAGING_VOCAB = {
    "T1", "T2", "FLAIR", "CT", "DWI",
    "fMRI", "multimodal", "none", "not_reported",
}
REGION_DEF_KIND_VOCAB = {
    "atlas", "manual_ROI", "peak_coord_sphere",
    "tract", "data_driven_cluster", "not_reported",
}

# v2.1 additions ---------------------------------------------------
SUPPORTS_VOCAB = {
    "claim", "method", "sample", "statistics", "confounders",
    "region_definition", "limitation", "imaging_details",
}
REFERENCE_SPACE_VOCAB = {
    "MNI152", "MNI305", "Talairach", "native", "other", "not_reported",
}

# v2.2 additions; extended 2026-05-01 with `treatment_response`
RELATIONSHIP_VOCAB = {
    "causal", "correlational", "recruitment", "responder",
    "treatment_response",
}

# Color hex per `supports` category — single source of truth shared
# between aphasia_kb.py (validation) and annotate_paper.py (rendering).
SUPPORTS_COLORS = {
    "claim":             "#a8c8ff",   # blue
    "sample":            "#a8e6a3",   # green
    "statistics":        "#ffcc99",   # orange
    "method":            "#fff4a3",   # yellow
    "region_definition": "#d9b3e6",   # purple
    "imaging_details":   "#d9b3e6",   # purple (same family as region)
    "limitation":        "#ffb3b3",   # red
    "confounders":       "#cccccc",   # grey
}

# Numeric weights for interpret_overlap()
_STRENGTH_WEIGHT = {"weak": 1.0, "moderate": 2.0, "strong": 3.0}
_EVIDENCE_WEIGHT = {
    "case-study":   0.5,
    "tentative":    0.5,
    "cohort":       1.0,
    "RCT":          1.5,
    "meta-analysis": 2.0,
}
_CONFIDENCE_WEIGHT = {"low": 0.5, "medium": 0.85, "high": 1.0}
_DIRECTION_SIGN = {
    "likely":              +1,
    "likely_responder":    +1,
    "unlikely":            -1,
    "unlikely_responder":  -1,
    "no_effect":           0,
    "mixed":               0,
}


# ============================================================
# Validation
# ============================================================

def _is_unset(v):
    return v is None or v == "" or v == "not_reported"


def _validate_v2_entry(entry: dict, src: str, issues: list[str]):
    """Validate a single v2 entry's frontmatter."""
    def err(msg):
        issues.append(f"{src}: {msg}")

    for f in ("id", "name", "kind", "status", "created_by", "created_on"):
        if not entry.get(f):
            err(f"missing required file-level field: {f}")
    sv = entry.get("schema_version")
    # Accept 2 (legacy v2.0), 2.1, 2.2, and 2.3 (current).
    # v2.1+ entries get the stricter source_passages + imaging_details checks.
    # v2.2+ entries get the relationship + multimodal-method checks.
    # v2.3+ entries can use the predictor bucket and target_kind=predictor.
    if sv not in (2, 2.1, 2.2, 2.3, "2", "2.1", "2.2", "2.3"):
        err(f"schema_version must be 2, 2.1, 2.2, or 2.3, got {sv!r}")
    is_v21 = sv in (2.1, 2.2, 2.3, "2.1", "2.2", "2.3")
    is_v22 = sv in (2.2, 2.3, "2.2", "2.3")
    is_v23 = sv in (2.3, "2.3")

    # v2.3 predictor entries: validate file-level predictor fields.
    # (We check kind=='predictor' regardless of bucket so any file that
    #  declares itself a predictor is held to the same contract.)
    if entry.get("kind") == "predictor":
        if not is_v23:
            err("predictor entries require schema_version 2.3 or higher")
        ptype = entry.get("predictor_type")
        if ptype not in PREDICTOR_TYPE_VOCAB:
            err(f"predictor_type={ptype!r} required; "
                f"allowed: {sorted(PREDICTOR_TYPE_VOCAB)}")
        if not entry.get("short_definition"):
            err("predictor entries require short_definition")
        if ptype in ("behavioural", "clinical"):
            assess = entry.get("assessment")
            if assess is None or not isinstance(assess, list) or not assess:
                err(f"predictor_type={ptype!r} requires assessment "
                    f"(non-empty list of test names)")
        dos = entry.get("direction_of_severity")
        if dos is not None and dos not in DIRECTION_OF_SEVERITY_VOCAB:
            err(f"direction_of_severity={dos!r} invalid; "
                f"allowed: {sorted(DIRECTION_OF_SEVERITY_VOCAB)}")
    if entry.get("status") not in STATUS_VOCAB:
        err(f"unknown status={entry.get('status')!r}; allowed: {sorted(STATUS_VOCAB)}")
    if entry.get("status") == "approved":
        if not entry.get("reviewer"):
            err("status=approved requires reviewer")
        if not entry.get("reviewed_on"):
            err("status=approved requires reviewed_on")

    findings = entry.get("findings") or []
    for i, f in enumerate(findings):
        prefix = f"finding[{i}] (id={f.get('id', '?')})"

        # Identity
        for req in ("id", "target", "target_kind", "claim", "direction", "citation"):
            if _is_unset(f.get(req)):
                err(f"{prefix}: missing {req}")
        if f.get("target_kind") not in TARGET_KIND_VOCAB:
            err(f"{prefix}: unknown target_kind={f.get('target_kind')!r}")
        if f.get("direction") not in DIRECTION_VOCAB:
            err(f"{prefix}: unknown direction={f.get('direction')!r}")

        # Method (v2.2: can be a list of strings; v2.0/2.1: string only)
        m = f.get("method")
        if isinstance(m, list):
            for mi in m:
                if mi not in METHOD_VOCAB:
                    err(f"{prefix}: unknown method[{mi!r}]; "
                        f"allowed: {sorted(METHOD_VOCAB)}")
        elif m not in METHOD_VOCAB:
            err(f"{prefix}: unknown method={m!r}; "
                f"allowed: {sorted(METHOD_VOCAB)}")
        if f.get("design") and f["design"] not in DESIGN_VOCAB:
            err(f"{prefix}: unknown design={f.get('design')!r}")

        # v2.2: relationship is required
        if is_v22:
            rel = f.get("relationship")
            if rel not in RELATIONSHIP_VOCAB:
                err(f"{prefix}: relationship={rel!r} required in v2.2; "
                    f"allowed: {sorted(RELATIONSHIP_VOCAB)}")

        # Sample
        sample = f.get("sample") or {}
        if "n" not in sample:
            err(f"{prefix}: sample.n missing")
        if not sample.get("population"):
            err(f"{prefix}: sample.population missing")

        # Statistics
        stats = f.get("statistics") or {}
        if not stats.get("threshold"):
            err(f"{prefix}: statistics.threshold missing")

        # Confounders (must be lists, even if empty)
        for ck in ("confounders_controlled", "confounders_not_controlled"):
            v = f.get(ck)
            if v is None:
                err(f"{prefix}: {ck} must be present (use [] if none)")
            elif not isinstance(v, list):
                err(f"{prefix}: {ck} must be a list")

        # Region definition
        rd = f.get("region_definition") or {}
        if rd.get("kind") not in REGION_DEF_KIND_VOCAB:
            err(f"{prefix}: region_definition.kind={rd.get('kind')!r} invalid")

        # author_limitations
        al = f.get("author_limitations")
        if al is None:
            err(f"{prefix}: author_limitations must be present (use [] if none)")
        elif not isinstance(al, list):
            err(f"{prefix}: author_limitations must be a list")

        # Extractor's assessment
        if f.get("evidence_quality") not in EVIDENCE_VOCAB:
            err(f"{prefix}: unknown evidence_quality={f.get('evidence_quality')!r}")
        if f.get("strength") not in STRENGTH_VOCAB:
            err(f"{prefix}: unknown strength={f.get('strength')!r}")

        # Provenance
        prov = f.get("provenance") or {}
        for pk in ("extracted_by", "extracted_on", "paper_section",
                   "confidence", "flags"):
            if pk not in prov:
                err(f"{prefix}: provenance.{pk} missing")
        if prov.get("confidence") not in CONFIDENCE_VOCAB:
            err(f"{prefix}: provenance.confidence={prov.get('confidence')!r} invalid")
        if not isinstance(prov.get("flags"), list):
            err(f"{prefix}: provenance.flags must be a list (use [] if none)")

        # v2.3 predictor-finding fields are an optional triplet:
        # if any of {instrument, score_band, interpretation} is set,
        # the others should be too (they're useless individually).
        if is_v23:
            triplet = ("instrument", "score_band", "interpretation")
            present = [k for k in triplet if f.get(k) not in (None, "")]
            if present and len(present) != len(triplet):
                missing = [k for k in triplet if k not in present]
                err(f"{prefix}: predictor triplet partially set "
                    f"(have {present}, missing {missing}); "
                    f"fill all three or none")
            for k in triplet:
                v = f.get(k)
                if v is not None and not isinstance(v, str):
                    err(f"{prefix}: {k} must be a string, got {type(v).__name__}")

        # v2.1: source_passages (required) + imaging_details (semi-required)
        if is_v21:
            sp = f.get("source_passages")
            if not sp or not isinstance(sp, list):
                err(f"{prefix}: source_passages must be a non-empty list in v2.1")
            else:
                for j, p in enumerate(sp):
                    pp = f"{prefix}.source_passages[{j}]"
                    if not isinstance(p, dict):
                        err(f"{pp}: must be an object, got {type(p).__name__}")
                        continue
                    for k in ("section", "page", "quote", "supports"):
                        if k not in p:
                            err(f"{pp}: missing {k}")
                    if p.get("supports") not in SUPPORTS_VOCAB:
                        err(f"{pp}: unknown supports={p.get('supports')!r}; "
                            f"allowed: {sorted(SUPPORTS_VOCAB)}")
                    if not (p.get("quote") or "").strip():
                        err(f"{pp}: quote is empty")

            img = f.get("imaging_details") or {}
            # reference_space + atlases_used are required when method
            # is anything imaging-based. behavioral_only / clinical_RCT
            # / meta-analysis findings can skip.
            non_imaging_methods = {
                "behavioral_only", "clinical_RCT",
                "meta-analysis", "computational_model",
            }
            method_value = f.get("method")
            if isinstance(method_value, list):
                # Multimodal: imaging required if ANY method is imaging-based
                needs_imaging = any(m not in non_imaging_methods
                                    for m in method_value)
            else:
                needs_imaging = method_value not in non_imaging_methods
            if needs_imaging:
                rs = img.get("reference_space")
                if rs not in REFERENCE_SPACE_VOCAB:
                    err(f"{prefix}: imaging_details.reference_space="
                        f"{rs!r} invalid (required for imaging method)")
                if "atlases_used" not in img:
                    err(f"{prefix}: imaging_details.atlases_used must be "
                        f"present (use [] if none)")
                elif not isinstance(img["atlases_used"], list):
                    err(f"{prefix}: imaging_details.atlases_used must be a list")
                # v2.2: if modalities is provided, check shape
                if "modalities" in img:
                    if not isinstance(img["modalities"], list):
                        err(f"{prefix}: imaging_details.modalities must be a list")
                    else:
                        for j, mod in enumerate(img["modalities"]):
                            if not isinstance(mod, dict):
                                err(f"{prefix}: imaging_details.modalities[{j}]"
                                    f" must be an object")
                            elif "modality" not in mod:
                                err(f"{prefix}: imaging_details.modalities[{j}]"
                                    f" missing 'modality' key")


def _validate_v1_entry(entry: dict, src: str, issues: list[str]):
    """Light validation for legacy v1 entries — they keep the thin schema."""
    def err(msg):
        issues.append(f"{src}: {msg}")
    for req in ("id", "name", "kind"):
        if not entry.get(req):
            err(f"v1: missing required field {req}")


# ============================================================
# Loader
# ============================================================

@dataclass
class KnowledgeBase:
    """
    Load a knowledge base directory.

    Parameters
    ----------
    root : str | Path
        Directory containing regions/, impairments/, therapies/, drafts/,
        _legacy_v1/, and citations.md.
    include : sequence of statuses to load. Default loads only `approved`
        from the canonical folders. Pass e.g. ['approved', 'draft'] to
        also include drafts.
    """
    root: Path
    include: tuple = ("approved",)

    regions: pd.DataFrame = field(init=False)
    impairments: pd.DataFrame = field(init=False)
    therapies: pd.DataFrame = field(init=False)
    predictors: pd.DataFrame = field(init=False)
    findings: pd.DataFrame = field(init=False)
    bodies: dict[str, str] = field(init=False)
    issues: list[str] = field(init=False)
    drafts: pd.DataFrame = field(init=False)

    def __init__(self, root: str | Path,
                 include: Sequence[str] = ("approved",)):
        self.root = Path(root)
        self.include = tuple(include)
        self.bodies = {}
        self.issues = []
        self._load()

    # --------------------------------------------------------
    # Load
    # --------------------------------------------------------
    def _walk(self, base: Path) -> dict[str, list[dict]]:
        out = {"regions": [], "impairments": [], "therapies": [], "predictors": []}
        for sub in out:
            d = base / sub
            if not d.is_dir():
                continue
            for path in sorted(d.glob("*.md")):
                fm, body = parse_markdown(path)
                if not fm:
                    self.issues.append(f"{path}: no frontmatter")
                    continue
                fm["_path"] = str(path.relative_to(self.root))
                fm["_kind_bucket"] = sub
                self.bodies[fm.get("id", path.stem)] = body
                out[sub].append(fm)
        return out

    def _load(self):
        # Approved (canonical) folders
        approved = self._walk(self.root)
        # Drafts
        drafts = self._walk(self.root / "drafts")
        for sub in drafts:
            for e in drafts[sub]:
                e["_origin"] = "draft"
        # Legacy v1
        legacy = self._walk(self.root / "_legacy_v1")
        for sub in legacy:
            for e in legacy[sub]:
                e["status"] = "legacy_v1"
                e["_origin"] = "legacy_v1"
                e.setdefault("schema_version", 1)

        # Validate everything we touched
        for bucket_entries in (approved, drafts, legacy):
            for sub, entries in bucket_entries.items():
                for e in entries:
                    src = e["_path"]
                    sv = e.get("schema_version")
                    if sv in (2, 2.1, 2.2, 2.3, "2", "2.1", "2.2", "2.3"):
                        _validate_v2_entry(e, src, self.issues)
                    else:
                        _validate_v1_entry(e, src, self.issues)

        # Filter by status
        def keep(entry: dict) -> bool:
            return entry.get("status") in self.include

        regions = [e for e in approved["regions"] if keep(e)]
        impairs = [e for e in approved["impairments"] if keep(e)]
        theras  = [e for e in approved["therapies"] if keep(e)]
        preds   = [e for e in approved["predictors"] if keep(e)]
        # Drafts are admitted only if their status is in `include` AND the
        # caller asked for drafts (typical use: include=['approved', 'draft'])
        for sub_entries, dest in (
            (drafts["regions"], regions),
            (drafts["impairments"], impairs),
            (drafts["therapies"], theras),
            (drafts["predictors"], preds),
        ):
            for e in sub_entries:
                if keep(e):
                    dest.append(e)
        # Legacy v1 admitted only if 'legacy_v1' in include
        for sub_entries, dest in (
            (legacy["regions"], regions),
            (legacy["impairments"], impairs),
            (legacy["therapies"], theras),
            (legacy["predictors"], preds),
        ):
            for e in sub_entries:
                if keep(e):
                    dest.append(e)

        self.regions     = pd.DataFrame(regions)
        self.impairments = pd.DataFrame(impairs)
        self.therapies   = pd.DataFrame(theras)
        self.predictors  = pd.DataFrame(preds)

        # Long-format findings table
        rows = []
        for sub_entries, sub in (
            (regions, "region"),
            (impairs, "impairment"),
            (theras,  "therapy"),
            (preds,   "predictor"),
        ):
            for e in sub_entries:
                for f in e.get("findings") or []:
                    rows.append({
                        "source_id":   e.get("id"),
                        "source_kind": sub,
                        "source_status": e.get("status"),
                        **{k: v for k, v in f.items()
                           if k in (
                               "id", "target", "target_kind", "claim", "direction",
                               "citation", "method", "design", "evidence_quality",
                               "strength",
                           )},
                        "sample_n": (f.get("sample") or {}).get("n"),
                        "stat_threshold": (f.get("statistics") or {}).get("threshold"),
                        "stat_effect_size": (f.get("statistics") or {}).get("effect_size"),
                        "confidence":  (f.get("provenance") or {}).get("confidence"),
                        "flags":       (f.get("provenance") or {}).get("flags") or [],
                        "schema_version": e.get("schema_version", 1),
                    })
        self.findings = pd.DataFrame(rows)

        # Convenience: a separate drafts dataframe for review tooling
        draft_rows = []
        for sub in ("regions", "impairments", "therapies", "predictors"):
            for e in drafts[sub]:
                draft_rows.append({
                    "bucket":   sub,
                    "id":       e.get("id"),
                    "name":     e.get("name"),
                    "status":   e.get("status"),
                    "path":     e["_path"],
                    "n_findings": len(e.get("findings") or []),
                    "created_by": e.get("created_by"),
                    "created_on": e.get("created_on"),
                })
        self.drafts = pd.DataFrame(draft_rows)

        # Build alias index
        self._alias_to_id: dict[str, str] = {}
        for entry in regions + impairs + theras + preds:
            ids = {entry.get("id"), entry.get("name")}
            for a in (entry.get("aliases") or []):
                ids.add(a)
            for x in list(ids):
                if x and "(" in str(x):
                    ids.add(re.sub(r"\s*\(.*?\)\s*", "", str(x)).strip())
            for x in ids:
                if x:
                    self._alias_to_id[_normalize(x)] = entry["id"]

    # --------------------------------------------------------
    # Lookup
    # --------------------------------------------------------
    def lookup_region(self, name_or_id: str) -> dict | None:
        rid = self._alias_to_id.get(_normalize(name_or_id))
        if not rid or self.regions.empty:
            return None
        sub = self.regions[self.regions["id"] == rid]
        return sub.iloc[0].to_dict() if not sub.empty else None

    def lookup_predictor(self, name_or_id: str) -> dict | None:
        """Look up a predictor by id, name, or alias."""
        pid = self._alias_to_id.get(_normalize(name_or_id))
        if not pid or self.predictors.empty:
            return None
        sub = self.predictors[self.predictors["id"] == pid]
        return sub.iloc[0].to_dict() if not sub.empty else None

    def resolve_aliases(self, names: Iterable[str]) -> dict[str, str | None]:
        out = {}
        for n in names:
            if n is None:
                continue
            out[n] = self._alias_to_id.get(_normalize(n))
        return out

    # --------------------------------------------------------
    # Interpretation
    # --------------------------------------------------------
    def interpret_overlap(
        self,
        overlap_df: pd.DataFrame,
        atlas: str | None = None,
        region_col: str = "region",
        weight_col: str = "lesion_in_roi_percent",
        min_overlap: float = 1.0,
        min_confidence: str | None = None,
    ) -> pd.DataFrame:
        """
        Aggregate KB findings against a per-region overlap table and return
        a ranked DataFrame of likely / unlikely findings with citations.

        For v2 entries, each contribution is multiplied by the extractor's
        confidence weight as well as strength × evidence × overlap × sign.
        """
        if overlap_df is None or overlap_df.empty or self.findings.empty:
            return pd.DataFrame()

        sub = overlap_df.copy()
        if atlas and "atlas" in sub.columns:
            sub = sub[sub["atlas"] == atlas]
        sub = sub[sub[weight_col] >= min_overlap]

        sub["_kb_id"] = sub[region_col].map(
            lambda x: self._alias_to_id.get(_normalize(x))
        )
        matched = sub.dropna(subset=["_kb_id"])
        if matched.empty:
            return pd.DataFrame()

        f = self.findings[self.findings["source_kind"] == "region"]
        if min_confidence:
            order = {"low": 0, "medium": 1, "high": 2}
            min_rank = order.get(min_confidence, 0)
            f = f[f["confidence"].map(lambda c: order.get(c, 0) >= min_rank)]
        joined = matched.merge(
            f, left_on="_kb_id", right_on="source_id", how="inner",
            suffixes=("", "_f"),
        )

        joined["weight"] = joined[weight_col] / 100.0
        joined["strength_w"] = joined["strength"].map(_STRENGTH_WEIGHT).fillna(1.0)
        joined["evidence_w"] = joined["evidence_quality"].map(_EVIDENCE_WEIGHT).fillna(1.0)
        joined["sign"]       = joined["direction"].map(_DIRECTION_SIGN).fillna(0)
        joined["confidence_w"] = joined["confidence"].map(_CONFIDENCE_WEIGHT).fillna(1.0)
        joined["contribution"] = (
            joined["weight"] * joined["strength_w"] * joined["evidence_w"]
            * joined["confidence_w"] * joined["sign"]
        )

        agg = (joined
               .groupby(["target", "target_kind"], as_index=False)
               .agg(score=("contribution", "sum"),
                    n_findings=("contribution", "size"),
                    citations=("citation", lambda s: sorted(set(s))),
                    contributing_regions=("region", lambda s: sorted(set(s)))))
        agg["direction"] = agg["score"].apply(
            lambda s: "likely" if s > 0 else ("unlikely" if s < 0 else "ambiguous")
        )
        agg = agg.sort_values("score", key=lambda s: s.abs(), ascending=False)
        return agg.reset_index(drop=True)

    def interpret_predictors(
        self,
        scores: dict,
        instrument_match_bonus: float = 1.5,
        min_confidence: str | None = None,
    ) -> pd.DataFrame:
        """
        Aggregate findings carried by predictor entries against a patient's
        measured behavioural / demographic / clinical / imaging scalars.

        Parameters
        ----------
        scores : dict
            Mapping from predictor id (or alias / name) to either:
              * a bare numeric value (e.g. `{"age": 64}`), or
              * a dict with `instrument` and `value` keys
                (e.g. `{"severity_metric": {"instrument": "WAB-AQ",
                "value": 65}}`).
            When `instrument` is supplied, findings whose
            `instrument` matches exactly receive a weighting bonus,
            and findings with no `instrument` field receive the
            normal weight. Findings with a different instrument
            still contribute, but at base weight (no penalty), so
            cross-instrument evidence remains visible.
        instrument_match_bonus : float, default 1.5
            Multiplier applied to findings whose `instrument` exactly
            matches the patient's reported instrument. Set to 1.0 to
            disable instrument-aware weighting.

        Returns
        -------
        pd.DataFrame with one row per (target, target_kind) aggregating
        evidence from all matched predictor findings, with citations,
        contributing predictors, and (when instrument was supplied)
        the set of instruments that matched.
        """
        if not scores or self.findings.empty:
            return pd.DataFrame()

        # Resolve user-supplied keys to canonical predictor ids,
        # and capture a per-id "expected instrument" if supplied.
        resolved: dict[str, str | None] = {}  # pid -> expected_instrument or None
        for key, raw in scores.items():
            pid = self._alias_to_id.get(_normalize(key))
            if pid is None:
                continue
            if isinstance(raw, dict):
                inst = raw.get("instrument")
            else:
                inst = None
            resolved[pid] = inst

        if not resolved:
            return pd.DataFrame()

        f = self.findings[
            (self.findings["source_kind"] == "predictor")
            & (self.findings["source_id"].isin(resolved.keys()))
        ].copy()
        if min_confidence:
            order = {"low": 0, "medium": 1, "high": 2}
            min_rank = order.get(min_confidence, 0)
            f = f[f["confidence"].map(lambda c: order.get(c, 0) >= min_rank)]
        if f.empty:
            return pd.DataFrame()

        f["strength_w"]   = f["strength"].map(_STRENGTH_WEIGHT).fillna(1.0)
        f["evidence_w"]   = f["evidence_quality"].map(_EVIDENCE_WEIGHT).fillna(1.0)
        f["confidence_w"] = f["confidence"].map(_CONFIDENCE_WEIGHT).fillna(1.0)
        f["sign"]         = f["direction"].map(_DIRECTION_SIGN).fillna(0)

        # Instrument-aware weighting: bonus when the finding's instrument
        # matches the patient's instrument for that predictor; base weight
        # otherwise (so cross-instrument evidence is still visible).
        # `instrument` is only present in the long-format findings table
        # when the schema rolls it in — re-read it from the raw frontmatter
        # via a lookup keyed on (source_id, finding id).
        per_finding_instrument = self._build_finding_instrument_index()

        def _instrument_w(row):
            expected = resolved.get(row["source_id"])
            if not expected:
                return 1.0
            actual = per_finding_instrument.get(
                (row["source_id"], row["id"]))
            if actual and _normalize(actual) == _normalize(expected):
                return instrument_match_bonus
            return 1.0

        f["instrument"] = f.apply(
            lambda r: per_finding_instrument.get((r["source_id"], r["id"])),
            axis=1,
        )
        f["instrument_w"] = f.apply(_instrument_w, axis=1)
        f["weight"]       = 1.0  # patient-value weighting reserved for future
        f["contribution"] = (
            f["weight"] * f["strength_w"] * f["evidence_w"]
            * f["confidence_w"] * f["instrument_w"] * f["sign"]
        )

        agg = (f
               .groupby(["target", "target_kind"], as_index=False)
               .agg(score=("contribution", "sum"),
                    n_findings=("contribution", "size"),
                    citations=("citation", lambda s: sorted(set(s))),
                    contributing_predictors=("source_id",
                                             lambda s: sorted(set(s))),
                    instruments=("instrument",
                                 lambda s: sorted({x for x in s if x}))))
        agg["direction"] = agg["score"].apply(
            lambda s: "likely" if s > 0 else ("unlikely" if s < 0 else "ambiguous")
        )
        agg = agg.sort_values("score", key=lambda s: s.abs(), ascending=False)
        return agg.reset_index(drop=True)

    def _build_finding_instrument_index(self) -> dict[tuple, str | None]:
        """Map (source_id, finding_id) -> the finding's `instrument` field
        (or None). Used by interpret_predictors() to route around the
        long-format findings table, which doesn't carry the v2.3
        predictor-triplet fields by default."""
        idx: dict[tuple, str | None] = {}
        for df, kind in (
            (self.predictors, "predictor"),
            (self.regions, "region"),
            (self.impairments, "impairment"),
            (self.therapies, "therapy"),
        ):
            if df is None or df.empty:
                continue
            for _, row in df.iterrows():
                src_id = row.get("id")
                for fnd in (row.get("findings") or []):
                    if isinstance(fnd, dict):
                        idx[(src_id, fnd.get("id"))] = fnd.get("instrument")
        return idx

    # --------------------------------------------------------
    # Convenience
    # --------------------------------------------------------
    def summary(self) -> str:
        return (
            f"Knowledge base @ {self.root}\n"
            f"  include:     {list(self.include)}\n"
            f"  regions:     {len(self.regions)}\n"
            f"  impairments: {len(self.impairments)}\n"
            f"  therapies:   {len(self.therapies)}\n"
            f"  predictors:  {len(self.predictors)}\n"
            f"  findings:    {len(self.findings)}\n"
            f"  drafts:      {len(self.drafts)} pending\n"
            f"  issues:      {len(self.issues)}"
        )


# ============================================================
# CLI
# ============================================================
def _cli(argv=None):
    import argparse
    p = argparse.ArgumentParser(description="Inspect / validate the aphasia KB")
    p.add_argument("--root", default=Path(__file__).parent,
                   help="Path to the aphasia-kb folder")
    p.add_argument("--check", metavar="DIR",
                   help="Validate v2 entries in DIR (e.g. drafts/) and exit.")
    p.add_argument("--include", nargs="+",
                   default=["approved", "draft", "in_review", "legacy_v1"],
                   help="Statuses to load (default: everything).")
    p.add_argument("--lookup", help="Look up a region by id/name/alias")
    p.add_argument("--issues", action="store_true",
                   help="Print all validation issues and exit")
    p.add_argument("--drafts", action="store_true",
                   help="List pending drafts and exit")
    args = p.parse_args(argv)

    kb = KnowledgeBase(args.root, include=args.include)
    print(kb.summary())

    if args.check:
        # Re-validate only the requested directory
        sub_issues = [i for i in kb.issues if args.check in i]
        for i in sub_issues:
            print(" ", i)
        sys.exit(0 if not sub_issues else 1)

    if args.issues:
        for i in kb.issues:
            print(" ", i)
        sys.exit(0)

    if args.drafts:
        if kb.drafts.empty:
            print("\nNo pending drafts.")
        else:
            print("\nPending drafts:")
            print(kb.drafts.to_string(index=False))
        sys.exit(0)

    if args.lookup:
        r = kb.lookup_region(args.lookup)
        if r is None:
            print(f"  no region matched {args.lookup!r}")
        else:
            print(f"\nMatch for {args.lookup!r}:")
            for k, v in r.items():
                if k.startswith("_"):
                    continue
                print(f"  {k}: {v}")


if __name__ == "__main__":
    _cli()
