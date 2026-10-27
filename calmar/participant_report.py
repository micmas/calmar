"""Participant interpretation report: assemble, save and show one HTML report.

The notebook's report cells call two functions:

* :func:`generate_participant_report` — for ONE participant and ONE MNI-space
  lesion mask: prepares the atlas-overlap tables (Slurm), queries the aphasia
  knowledge base (KB), renders the HTML sections, saves
  ``reports/interpretation_<sub>_<ses>_<source>.html`` and returns a
  :class:`ParticipantReportResult` holding the on-screen panel.
* :func:`decode_into_report` — optional Neurosynth decoding of the same mask
  (Slurm), appended to that report.

How the numbers are computed
----------------------------
* Damaged regions: rows of the display-atlas overlap table with
  ``lesion_in_roi_percent`` (= % of lesion voxels inside the ROI) at or above
  ``ReportSettings.min_overlap_pct``, or ``roi_coverage_percent`` (= % of ROI
  voxels lesioned) at or above ``min_region_pct`` — the same rule the KB
  interpretation uses; at most ``max_rois`` rows.
* Lesion location (calmar.report_evidence.location_section): damage per KB
  region through the curated atlas mapping (stroke-aphasia-kb/atlas_mapping/; share of
  the lesion and share of the region destroyed, per hemisphere), the findings
  about each damaged region with their direction, and the impairments they
  point to (:meth:`KnowledgeBase.location_findings` / ``interpret_damage``).
* Measures (calmar.report_evidence.measures_section): WAB-AQ, age at stroke,
  education, days to WAB, sex (``participants.tsv``), optional brain-health
  measurements, and lesion volume (mL; voxels > 0 in the selected MNI mask x
  voxel volume). Values without KB evidence remain visible as context.
* Domain context: user-entered none/mild/moderate/severe levels across language
  and cognitive domains. When a WAB/WAB-R aphasia type is present, its published
  +/- profile seeds fluency, comprehension and repetition conservatively
  (impaired -> a mild profile floor; relatively preserved -> severity not
  assigned). User entries take precedence, and every other missing domain
  remains ``not_assessed``.
* Therapies: :meth:`KnowledgeBase.interpret_therapies` from the impairments
  the lesion location points to, gated by impairments implied by the WAB type.
* Provenance: mask QC rating from the participant's ``*.qc.json`` sidecar and
  how the mask was made (calmar.mask_method).

The clinical rules (WAB type profile, recovery stage, display-signal bins) live in
``stroke-aphasia-kb/scripts/aphasia_rules.py`` and are shown by :func:`rules_html`.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from html import escape
from pathlib import Path
import base64
import itertools
import re

import pandas as pd

from .kb_location import kb_git_state
from .kb_paths import load_kb_modules

from . import colors as cc
from .masks import MASK_LABELS

#: Atlases the KB lookup uses by default.
DEFAULT_KB_ATLASES = ("AAL", "HarvardOxford", "Destrieux", "Schaefer400", "JHU", "XTRACT")

#: QC stages (calmar.qc) whose rating describes each mask source.
QC_STAGES_FOR_SOURCE = {
    "linda": ("lesion",),
    "synthstroke": ("synthstroke_lesion",),
    "manual": ("manual_lesion", "expert_mni_warp"),
    "openads": ("openads_lesion", "openads_mni_warp"),
}

TEMPLATE_CAVEAT = (
    "Lesion masks are on the FSL MNI152 template (MNI152NLin6Asym, 1 mm); the registration used for this "
    "mask is named above. Atlases are resampled to the lesion by world coordinates. Overlaps still depend "
    "on how well this individual brain was registered to MNI152, which matters most for small or thin regions.")


# KB entry statuses a report may draw on, by evidence level (report form "Evidence").
EVIDENCE_LEVELS = {"approved": ("approved",),
                   "in_review": ("approved", "in_review"),
                   "all": ("approved", "in_review", "draft")}
EVIDENCE_LABELS = {"approved": "Approved entries only",
                   "in_review": "Approved + in review",
                   "all": "All, including unreviewed drafts"}

DOMAIN_LEVELS = ("not_assessed", "none", "mild", "moderate", "severe")
DOMAIN_LEVEL_LABELS = {
    "not_assessed": "Not assessed", "none": "None observed", "mild": "Mild",
    "moderate": "Moderate", "severe": "Severe",
}
DOMAIN_LABELS = {
    "naming": "Naming / word finding", "comprehension": "Spoken comprehension",
    "repetition": "Repetition", "fluency": "Speech fluency", "reading": "Reading",
    "writing": "Writing", "speech_motor": "Speech motor / articulation",
    "semantics": "Semantic processing", "syntax": "Syntactic processing",
    "executive_function": "Executive function", "attention": "Attention", "memory": "Memory",
    "praxis": "Praxis", "visuospatial_attention": "Visuospatial attention",
}


@dataclass
class ReportSettings:
    """User decisions for the interpretation report (set in the settings cell)."""
    kb_atlases: tuple = DEFAULT_KB_ATLASES   # atlases used to query the KB
    display_atlas: str = "HarvardOxford"     # atlas for the damaged-regions table
    high_conf_only: bool = False             # only KB findings with confidence "high"
    include_drafts: bool = True              # older setting: True = evidence "all", False = "approved"
    evidence: str | None = None              # "approved", "in_review" (approved + in review) or "all" (+ drafts)
    min_overlap_pct: float = 5.0             # an ROI counts as damaged if it holds >= this % of the lesion
    min_region_pct: float = 25.0             # ... or if >= this % of the ROI is destroyed (small regions, thin tracts)
    disconnectome: str = "bcb"               # map for tract disconnection: "bcb", "deepdisco" or "none"
    min_disconnected_pct: float = 50.0       # a tract counts as disconnected if >= this % of it has p > 0.5
    top_n: int = 5                           # rows per prediction / therapy table
    max_rois: int = 15                       # rows in the damaged-regions table
    max_evidence_regions: int = 8            # main region disclosures before the additional-region fold
    min_summary_citations: int = 2           # primary symptom summary: distinct citation keys
    min_summary_anatomies: int = 2           # primary symptom summary: distinct mapped anatomical units
    threshold: float = 0.5                   # mask threshold for Dice between masks

    @property
    def include(self):
        level = self.evidence or ("all" if self.include_drafts else "approved")
        if level not in EVIDENCE_LEVELS:
            raise ValueError(f"evidence must be one of {list(EVIDENCE_LEVELS)}, not {level!r}")
        return EVIDENCE_LEVELS[level]


@dataclass
class ParticipantReportResult:
    """What the report cell keeps: the panel, the saved file and its selection."""
    entry: dict
    source: str
    path: Path
    panel: object
    messages: list = field(default_factory=list)

    @property
    def selection(self):
        return (self.entry["subject"], self.entry.get("session") or "", self.source)


# ============================================================
# Knowledge base and rules
# ============================================================

def _kb_modules(kb_root):
    """Freshly import ``aphasia_kb`` and ``aphasia_rules`` from one root."""
    return load_kb_modules(kb_root, "aphasia_kb", "aphasia_rules")


def load_kb(kb_root, settings, aphasia_kb=None):
    """KnowledgeBase from ``kb_root``. Raises if the root holds no KB entries."""
    if aphasia_kb is None:
        aphasia_kb, _ = _kb_modules(kb_root)
    kb = aphasia_kb.KnowledgeBase(Path(kb_root), include=settings.include)
    if not len(kb.regions) and not len(kb.impairments):
        # A wrong root does not error inside KnowledgeBase; it loads nothing.
        raise FileNotFoundError(f"No aphasia knowledge base entries under {kb_root}")
    return kb




def kb_version(kb_root, kb, location=None):
    """The KB checkout and content scope used for this report."""
    root = Path(kb_root).expanduser().resolve()
    state = kb_git_state(root)
    findings = kb.findings
    reviewed = (findings["review_kind"] == "human").sum() if "review_kind" in findings else 0
    return {
        **state,
        "root": str(root),
        "location": location or "configured KB root",
        "papers": int(findings["citation"].dropna().nunique()) if "citation" in findings else 0,
        "findings": len(findings),
        "findings_reviewed": int(reviewed),
        "entries": {b: len(getattr(kb, b)) for b in ("regions", "impairments", "therapies", "predictors")},
        "statuses": list(kb.include),
    }


def kb_version_text(version):
    """One line for the report, e.g. "version 059bcd5 (2026-10-19) · 36 papers · ..."."""
    if version["commit"]:
        text = f"version {version['commit']} ({version['date']})"
        if version["uncommitted"] is True:
            text += " with uncommitted changes"
        elif version.get("uncommitted") is None:
            text += "; working-tree status unknown"
    else:
        text = "version unknown (not under git version control)"
        if version.get("uncommitted") is None:
            text += "; working-tree status unknown"
    text += f" · KB root: {version.get('location', 'configured KB root')} ({version.get('root', 'unknown')})"
    entries = version["entries"]
    return (f"{text} · {version['papers']} papers · {version['findings']} extracted findings "
            f"({version['findings_reviewed']} approved by a named reviewer) in "
            f"{sum(entries.values())} entries ({entries['regions']} regions, {entries['impairments']} impairments, "
            f"{entries['therapies']} therapies, {entries['predictors']} predictors) · "
            f"statuses used: {', '.join(version['statuses'])}")


def rules_html(kb_root):
    """The fixed clinical/display rules as small HTML tables (for the notebook)."""
    _, rules = _kb_modules(kb_root)
    parts = []
    for title, table in rules.rules_tables().items():
        parts.append(f"<h4 style='margin:10px 0 4px'>{escape(title)}</h4>"
                     + table.to_html(index=False, border=0, escape=True))
    return ("<div style='font-size:12px'>" + "".join(parts) +
            "<p style='font-size:11px'>Defined in <code>stroke-aphasia-kb/scripts/aphasia_rules.py</code> "
            "(sources and caveats in its docstrings).</p></div>")


# ============================================================
# Inputs: overlap tables, participants.tsv, lesion volume
# ============================================================

def _participant_rows(df, entry):
    return df[(df["subject"] == entry["subject"]) &
              (df["session"].fillna("") == (entry.get("session") or ""))]


def overlap_csv(atlas, source, overlap_paths, reports_dir):
    """CSV prepared for this report, else the historical shared CSV."""
    from .study import file_token
    key = f"{atlas}_{source}"
    if key in (overlap_paths or {}):
        return Path(overlap_paths[key])
    return Path(reports_dir) / f"lesion_atlas_overlap_{atlas}_{file_token(source)}.csv"


def _days(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def lesion_damage(entry, source, settings, overlap_paths, reports_dir):
    """Damage per knowledge-base region (stroke-aphasia-kb/atlas_mapping) from the
    participant's rows of each atlas overlap table in ``settings.kb_atlases``.
    Returns ``(region damage, {atlas: rows})``."""
    import atlas_mapping
    rows_by_atlas = {}
    for atlas in settings.kb_atlases:
        csv = overlap_csv(atlas, source, overlap_paths, reports_dir)
        if not csv.exists():
            continue
        rows = _participant_rows(pd.read_csv(csv), entry)
        if not rows.empty:
            rows_by_atlas[atlas] = rows
    units = atlas_mapping.unit_damage(rows_by_atlas)
    return atlas_mapping.region_damage(units), rows_by_atlas


def imaging_interpretation(kb, rules, entry, source, settings, overlap_paths, reports_dir):
    """KB predictions from lesion location, through the curated atlas mapping.

    Returns (DataFrame, [(atlas, rows)]); the DataFrame has target,
    target_kind, score, n_findings, citations, contributing_regions, direction.
    """
    damage, rows_by_atlas = lesion_damage(entry, source, settings, overlap_paths, reports_dir)
    per_atlas = [(atlas, len(rows)) for atlas, rows in rows_by_atlas.items()]
    found = kb.interpret_damage(damage, min_overlap=settings.min_overlap_pct, min_region=settings.min_region_pct,
                                min_confidence=("high" if settings.high_conf_only else None))
    if found is None or found.empty:
        return pd.DataFrame(), per_atlas
    found["direction"] = found["score"].apply(rules.evidence_direction)
    return found, per_atlas


def damaged_regions(entry, source, settings, overlap_paths, reports_dir):
    """Display-atlas rows holding >= min_overlap_pct of the lesion or with >= min_region_pct of the ROI lesioned."""
    csv = overlap_csv(settings.display_atlas, source, overlap_paths, reports_dir)
    if not csv.exists():
        return pd.DataFrame()
    rows = _participant_rows(pd.read_csv(csv), entry)
    damaged = ((rows["lesion_in_roi_percent"] >= settings.min_overlap_pct)
               | (rows["roi_coverage_percent"] >= settings.min_region_pct))
    return rows[damaged].sort_values("lesion_in_roi_percent", ascending=False).head(settings.max_rois)


def participant_row(dataset_dir, subject):
    """The participant's ``participants.tsv`` row as a dict ('n/a' -> None)."""
    path = Path(dataset_dir) / "participants.tsv"
    if not path.exists():
        return {}
    df = pd.read_csv(path, sep="\t", dtype=str)
    rows = df[df["participant_id"] == subject]
    if rows.empty:
        return {}
    return {k: (None if pd.isna(v) or v == "n/a" else v) for k, v in rows.iloc[0].items()}


def row_to_predictors(row):
    """KB predictor values from a participants.tsv row (unparseable values skipped)."""
    out = {}
    if not row:
        return out
    def number(key):
        try:
            return float(row[key]) if row.get(key) not in (None, "") else None
        except ValueError:
            return None
    if number("wab_aq") is not None:
        out["severity_metric"] = {"instrument": "WAB-AQ", "value": number("wab_aq")}
    if number("age_at_stroke") is not None:
        out["age"] = number("age_at_stroke")
    if number("wab_days") is not None:
        out["time_post_onset"] = number("wab_days")
    if row.get("sex"):
        out["sex"] = row["sex"]
    return out


def education_measure(row):
    """Return education exactly as supplied, without guessing across fields."""
    row = row or {}
    for key in ("education_years", "years_of_education"):
        value = row.get(key)
        if value not in (None, ""):
            try:
                value = float(value)
            except (TypeError, ValueError):
                return {"value": value, "units": "not recorded", "label": "Education", "kb_id": "education"}
            return {"value": value, "units": "years", "label": "Education", "kb_id": "education"}
    if row.get("education") not in (None, ""):
        return {"value": row["education"], "units": "as recorded", "label": "Education", "kb_id": "education"}
    return {"value": None, "units": "not recorded", "label": "Education", "kb_id": "education",
            "missing_reason": "participants.tsv has no education value"}


def normalise_domain_levels(values):
    """Validate the report-only domain context without inferring missing levels."""
    supplied = values or {}
    unknown = sorted(set(supplied) - set(DOMAIN_LABELS))
    if unknown:
        raise ValueError("Unknown impairment domains: " + ", ".join(unknown))
    out = {}
    for domain in DOMAIN_LABELS:
        level = supplied.get(domain, "not_assessed")
        if level not in DOMAIN_LEVELS:
            raise ValueError(f"Invalid level {level!r} for {domain}; choose one of {DOMAIN_LEVELS}")
        out[domain] = level
    return out


def wab_profile_domain_levels(rules, wab_type):
    """Domain defaults from the Kertesz WAB/WAB-R +/- type profile.

    The qualitative type profile does not measure domain severity. CALMaR uses
    the least non-zero impairment category for ``-``. A ``+`` is only relative
    preservation within that type's range, so its severity remains unassessed.
    Only the three axes encoded by the WAB taxonomy receive source annotations;
    an unknown or missing type populates nothing.
    """
    levels = normalise_domain_levels(None)
    sources = {}
    profile = rules.decompose_aphasia(wab_type)
    if not profile:
        return levels, sources
    for domain, status in zip(rules.WAB_AXES, profile):
        if status == "-":
            levels[domain] = "mild"
            sources[domain] = "wab_profile_impaired"
        else:
            sources[domain] = "wab_profile_preserved"
    return levels, sources


def domain_levels_html(values, sources=None):
    """Participant-context table of entered and WAB-profile-derived levels."""
    levels = normalise_domain_levels(values)
    sources = sources or {}
    source_label = {
        "wab_profile_impaired": "WAB/WAB-R profile: impaired (−); mild is a profile floor",
        "wab_profile_preserved": "WAB/WAB-R profile: relatively preserved (+); severity not assigned",
        "entered": "Entered for this report",
    }
    def source_for(domain, level):
        fallback = "Entered for this report" if level != "not_assessed" else "—"
        return source_label.get(sources.get(domain), fallback)
    rows = "".join(
        f"<tr><td><b>{escape(DOMAIN_LABELS[domain])}</b></td>"
        f"<td>{escape(DOMAIN_LEVEL_LABELS[level])}</td>"
        f"<td>{escape(source_for(domain, level))}</td></tr>"
        for domain, level in levels.items())
    seeded = any(str(value).startswith("wab_profile_") for value in sources.values())
    intro = (
        "The participant's recorded aphasia type was not displayed as a clinical measure. Instead, its "
        "Kertesz WAB/WAB-R profile informed only the rows identified in the Source column: <b>− impaired → mild "
        "profile floor</b>; <b>+ relatively preserved → severity not assigned</b>. These are not measured domain "
        "severities; replace them with assessed levels when available."
        if seeded else
        "Domain levels were entered directly for this report. They are not inferred from WAB-AQ, language, or "
        "lesion location."
    )
    return (f"<p class='section-intro'>{intro} <b>Not assessed</b> is not normal performance.</p>"
            "<table class='behaviour-table'><thead><tr><th>Domain</th><th>Level</th><th>Source</th></tr></thead>"
            "<tbody>" + rows + "</tbody></table>")


def lesion_volume_ml(mask_path):
    """Volume (mL) of voxels > 0, using the diagonal voxel size as before."""
    import nibabel as nib
    import numpy as np
    img = nib.load(str(mask_path))
    voxel_mm3 = abs(img.affine[0, 0] * img.affine[1, 1] * img.affine[2, 2])
    return float((np.asanyarray(img.dataobj) > 0).sum() * voxel_mm3 / 1000.0)


# ============================================================
# Provenance: mask QC and agreement between masks
# ============================================================

def mask_qc_summary(anchor_mask, mask_path, source):
    """QC rating(s) and edit count for the selected mask, from ``*.qc.json``.

    ``anchor_mask`` is the participant's QC anchor (``Study.qc_anchor``),
    whose sidecar holds every stage rating; ``mask_path``'s own sidecar holds
    that mask's edit history. Returns {"ratings": [(stage, label, reviewer,
    date)], "edits": n, "poor": bool}.
    """
    from . import qc as q
    ratings, poor = [], False
    try:
        record = q.QCRecord.load(Path(anchor_mask))
        for stage in QC_STAGES_FOR_SOURCE.get(source, ()):
            rating = record.get_stage(stage).get("rating")
            if rating is not None:
                ratings.append((stage, q.RATING_VOCAB.get(rating, str(rating)),
                                record.reviewer, record.reviewed_on))
                poor = poor or rating == 3
    except (OSError, ValueError):
        pass
    edits = 0
    try:
        edits = len(q.QCRecord.load(Path(mask_path)).edits)
    except (OSError, ValueError):
        pass
    return {"ratings": ratings, "edits": edits, "poor": poor}


def mask_agreement(masks, threshold=0.5):
    """Dice and volumes for every pair of masks ``{source: path}``.

    Masks are binarised at ``> threshold``; a mask on a different grid is
    resampled (nearest neighbour) onto the first mask's grid. Returns
    (volumes {source: mL}, [(a, b, dice)]).
    """
    import nibabel as nib
    import numpy as np
    from nibabel.processing import resample_from_to
    loaded = {s: nib.load(str(p)) for s, p in masks.items() if Path(p).exists()}
    if not loaded:
        return {}, []
    ref = next(iter(loaded.values()))
    data, volumes = {}, {}
    for source, img in loaded.items():
        if img.shape != ref.shape or not np.allclose(img.affine, ref.affine):
            img = resample_from_to(img, ref, order=0)
        data[source] = np.asanyarray(img.dataobj) > threshold
        volumes[source] = float(data[source].sum() * abs(np.linalg.det(ref.affine[:3, :3])) / 1000.0)
    pairs = []
    for a, b in itertools.combinations(data, 2):
        total = data[a].sum() + data[b].sum()
        pairs.append((a, b, float(2 * (data[a] & data[b]).sum() / total) if total else float("nan")))
    return volumes, pairs


def provenance_html(source, mask_path, qc, *, kb_scope, method=None, generated=None, kb=None):
    """Research-use caveat, the lesion mask (QC and how it was made), template caveat,
    knowledge base. ``method``: HTML list of the steps that made the mask
    (calmar.mask_method). Agreement with the manual mask is shown in the report
    form before generating, not in the report."""
    label = MASK_LABELS.get(source, source)
    if qc["ratings"]:
        rated = "; ".join(f"{escape(stage)}: <b>{escape(lbl)}</b>"
                          + (f" ({escape(str(who))}" + (f", {escape(str(when))}" if when else "") + ")" if who else "")
                          for stage, lbl, who, when in qc["ratings"])
    else:
        rated = "not rated in the QC checkpoint"
    warn = (" <b class='provenance-warning'>Rated poor — interpret this report with caution.</b>"
            if qc["poor"] else "")
    edits = f" Edits recorded on this mask: {qc['edits']}." if qc["edits"] else ""
    generated = generated or datetime.now()
    return (
        "<div class='calmar-provenance' role='note'>"
        "<b>Research use only — not a diagnosis.</b> This report combines automated lesion "
        "segmentation with literature associations from the aphasia knowledge base. It does not "
        "diagnose aphasia, predict an individual's outcome or prescribe therapy; any clinical use "
        "requires review by a qualified clinician."
        "<ul style='margin:6px 0 0 18px;padding:0'>"
        f"<li><b>Lesion mask:</b> {escape(label)} (MNI) <code>{escape(Path(mask_path).name)}</code>. "
        f"QC: {rated}.{edits}{warn}</li>"
        + (f"<li><b>How this lesion mask was made:</b>{method}</li>" if method else "") +
        f"<li><b>Template space:</b> {escape(TEMPLATE_CAVEAT)}</li>"
        + (f"<li><b>Knowledge base:</b> {escape(kb)}</li>" if kb else "") +
        f"<li><b>Generated:</b> {generated:%Y-%m-%d %H:%M} · KB scope: {escape(kb_scope)}</li>"
        "</ul></div>")


# ============================================================
# HTML rendering of the KB results
# ============================================================

def _badge(direction):
    colour = {"likely": "#28a745", "unlikely": "#dc3545"}.get(direction, "#6c757d")
    text = {"likely": "LIKELY", "unlikely": "UNLIKELY"}.get(direction, "AMBIGUOUS")
    return (f'<span style="background:{colour};color:white;'
            f'padding:1px 6px;border-radius:3px;font-size:11px">{text}</span>')


def _stars_html(rules, score):
    stars, label = rules.evidence_strength(score)
    glyphs = "&#9733;" * stars if stars else "&mdash;"
    return (f"<span class='display-signal' title='Project display heuristic; raw score = {score:+.2f}'>"
            f"<span class='display-stars' aria-hidden='true'>{glyphs}</span>"
            f"<span class='display-stars-print'>{stars}/4 stars</span>"
            f"<span class='display-label' aria-hidden='true'>{escape(label)}</span>"
            f"<span class='visually-hidden'>Project-specific display heuristic: {stars} of 4 stars; "
            f"{escape(label)}.</span></span>")


_TABLE_HEAD = ("<table style='border-collapse:collapse;font-size:13px;width:100%'>"
               "<tr style='background:#52489c;color:white'>"
               "<th style='padding:4px 4px'></th>"
               "<th style='text-align:left;padding:4px 8px'>{what}</th>"
               "<th style='padding:4px 8px;text-align:left'>Project display signal</th>"
               "<th style='padding:4px 4px'>N findings</th>"
               "<th style='text-align:left;padding:4px 4px'>Citations</th></tr>")


def interp_table(kb, rules, df, kind, top_n):
    """Predicted findings of one target kind (e.g. 'impairment')."""
    if df is None or df.empty:
        return f"<p style='color:#666'><em>No {kind} predictions.</em></p>"
    sub = df[df["target_kind"] == kind].head(top_n)
    if sub.empty:
        return f"<p style='color:#666'><em>No {kind} predictions.</em></p>"
    rows = []
    for _, r in sub.iterrows():
        name = kb.label_for(r["target"])
        id_note = (f" <small style='color:#5a5a66;font-size:10px'>({r['target']})</small>"
                   if name != r["target"] else "")
        rows.append(f"<tr><td style='padding:4px 2px'>{_badge(r['direction'])}</td>"
                    f"<td style='padding:4px 8px'><b>{name}</b>{id_note}</td>"
                    f"<td style='padding:4px 8px'>{_stars_html(rules, r['score'])}</td>"
                    f"<td style='text-align:center;padding:4px 4px'>{r['n_findings']}</td>"
                    f"<td style='font-size:11px;color:#666;padding:4px 4px'>{', '.join(r.get('citations') or [])}</td></tr>")
    return _TABLE_HEAD.format(what="Predicted finding") + "".join(rows) + "</table>"


def interp_table_all(kb, rules, df, top_n):
    """Predictor-driven outcome predictions of every kind."""
    if df is None or df.empty:
        return "<p style='color:#666'><em>No outcome predictions.</em></p>"
    rows = []
    for _, r in df.head(top_n).iterrows():
        name = kb.label_for(r["target"])
        id_note = (f" <small style='color:#5a5a66;font-size:10px'>({r['target']})</small>"
                   if name != r["target"] else "")
        kind = f"<small style='color:#888;font-size:10px'>[{r.get('target_kind', '')}]</small> "
        rows.append(f"<tr><td style='padding:4px 2px'>{_badge(r['direction'])}</td>"
                    f"<td style='padding:4px 8px'>{kind}<b>{name}</b>{id_note}</td>"
                    f"<td style='padding:4px 8px'>{_stars_html(rules, r['score'])}</td>"
                    f"<td style='text-align:center;padding:4px 4px'>{r['n_findings']}</td>"
                    f"<td style='font-size:11px;color:#666;padding:4px 4px'>{', '.join(r.get('citations') or [])}</td></tr>")
    return _TABLE_HEAD.format(what="Predicted outcome") + "".join(rows) + "</table>"


_INGREDIENT_COLOURS = {"procedure": ("#4062bb", "#fff"),
                       "dose_parameter": ("#f45b69", "#2b2b3a"),
                       "technology": ("#1f7f7f", "#fff")}


def _ingredient_badges(summary):
    if not summary:
        return "<em style='color:#5a5a66'>—</em>"
    badges = []
    for item in summary:
        label, cat = (item.rsplit(" (", 1) if " (" in item and item.endswith(")") else (item, ""))
        cat = cat.rstrip(")")
        background, ink = _INGREDIENT_COLOURS.get(cat, ("#bdbdbd", "#2b2b3a"))
        if cat == "dose_parameter":
            background = "rgba(244,91,105,.12)"
        border = "#f45b69" if cat == "dose_parameter" else background
        badges.append(f"<span style='display:inline-block;margin:1px 2px;padding:1px 6px;"
                      f"border:1px solid {border};border-radius:3px;font-size:10px;color:{ink};"
                      f"background:{background}'>{label}</span>")
    return " ".join(badges)


def therapy_table(kb, df, stage_id, stage_label, therapy_stages):
    """Matched therapies; mark evidence from another recovery stage."""
    if df is None or df.empty:
        return ("<p style='color:#666'><em>No therapy recommendations matched. "
                "Add more impairment-targeted therapy KB entries to populate this section.</em></p>")
    rows = []
    for _, r in df.iterrows():
        beh = ", ".join(kb.label_for(i) for i in (r.get("behavioral_matched") or []))
        les = ", ".join(kb.label_for(i) for i in (r.get("lesion_matched") or []))
        parts = ([f"<b>{beh}</b> <small style='color:#1f7f7f'>(behavioural)</small>"] if beh else []) + \
                ([f"{les} <small style='color:#5a5a66'>(lesion)</small>"] if les else [])
        desc = str(r.get("short_description") or "")
        desc = (desc[:120] + "&#8230;") if len(desc) > 120 else desc
        evidence = therapy_stages.get(str(r.get("therapy_id") or r.get("id") or ""), set())
        warn = ""
        if stage_id and evidence and stage_id not in evidence:
            warning = (f"Evidence for this therapy comes from {' / '.join(sorted(evidence))} patients; "
                       f"current patient is {stage_label}.")
            warn = (" <details class='stage-warning'><summary>Stage mismatch</summary>"
                    f"<span class='stage-warning-detail'>{escape(warning)}</span></details>"
                    f"<span class='print-only stage-warning-print'>{escape(warning)}</span>")
        rows.append(
            "<tr>"
            "<td data-label='Therapy' style='padding:6px 8px;font-weight:bold;word-break:break-word;vertical-align:top;min-width:130px'>"
            f"<span class='cell-value'>{r['therapy_name']}{warn}</span></td>"
            f"<td data-label='Addresses impairment(s)' style='padding:6px 8px;font-size:12px;color:#444;vertical-align:top'>{'; '.join(parts) or '—'}</td>"
            "<td data-label='Active ingredients (RTSS)' style='padding:6px 8px;font-size:11px;vertical-align:top;overflow-wrap:break-word'>"
            f"{_ingredient_badges(r.get('rtss_summary') or [])}</td>"
            f"<td data-label='Brief description' style='padding:6px 8px;font-size:11px;color:#666;vertical-align:top'>{desc}</td>"
            f"<td data-label='Citations' style='padding:6px 4px;font-size:11px;color:#777;vertical-align:top'>{', '.join(r.get('citations') or [])}</td>"
            "</tr>")
    legend = ("<p style='font-size:10px;color:#5a5a66;margin:4px 0 0 0'>"
              "<span style='background:#4062bb;color:white;padding:1px 5px;border-radius:3px'>procedure</span>&nbsp;"
              "<span style='background:rgba(244,91,105,.12);color:#2b2b3a;border:1px solid #f45b69;"
              "padding:1px 5px;border-radius:3px'>dose parameter</span>&nbsp;"
              "<span style='background:#1f7f7f;color:white;padding:1px 5px;border-radius:3px'>technology</span></p>")
    return ("<div class='table-scroll' role='region' aria-label='Therapy recommendations' tabindex='0'>"
            "<table class='data-table therapy-table' style='table-layout:fixed'>"
            "<colgroup><col style='width:22%'><col style='width:24%'>"
            "<col style='width:18%'><col style='width:25%'><col style='width:11%'></colgroup>"
            "<thead><tr>"
            "<th style='text-align:left;padding:4px 8px'>Therapy</th>"
            "<th style='text-align:left;padding:4px 8px'>Addresses impairment(s)</th>"
            "<th style='text-align:left;padding:4px 8px'>Active ingredients (RTSS)</th>"
            "<th style='text-align:left;padding:4px 8px'>Brief description</th>"
            "<th style='text-align:left;padding:4px 4px'>Citations</th></tr></thead><tbody>"
            + "".join(rows) + "</tbody></table></div>" + legend)


def damaged_regions_html(df, display_atlas, atlas_dir):
    if df is None or df.empty:
        return "<p style='color:#666'><em>No damaged regions above threshold.</em></p>"
    from .anatomy_labels import label_table
    df = label_table(df, display_atlas, atlas_dir)
    rows = [f"<tr><td data-label='{escape(display_atlas)} region'>{escape(r['region'])}</td>"
            f"<td data-label='Lesion side' class='numeric'>{escape(r['lesion_hemisphere'])}</td>"
            f"<td data-label='% of lesion in ROI' class='numeric'>{r['lesion_in_roi_percent']:.1f}%</td>"
            f"<td data-label='% of ROI lesioned' class='numeric'>{r['roi_coverage_percent']:.1f}%</td>"
            f"<td data-label='Overlap voxels' class='numeric secondary'>"
            f"{int(r.get('overlap_voxels', 0)):,} vox</td></tr>" for _, r in df.iterrows()]
    return ("<div class='table-scroll' role='region' aria-label='Damaged regions' tabindex='0'>"
            "<table class='data-table damaged-table'><thead><tr>"
            f"<th style='text-align:left;padding:4px 8px'>{display_atlas} region</th>"
            "<th class='numeric'>Lesion side</th>"
            "<th class='numeric'>% of lesion in ROI</th>"
            "<th class='numeric'>% of ROI lesioned</th><th class='numeric'>Overlap voxels</th></tr></thead><tbody>"
            + "".join(rows) + "</tbody></table></div><p class='method-note'>"
            "Lesion side is measured from the actual mask overlap; bilateral entries show left/right counts.</p>")


def behaviour_html(rules, row, predictors, volume_ml):
    if not row and volume_ml is None:
        return "<p style='color:#888'><em>No participants.tsv entry.</em></p>"
    row = row or {}
    education = education_measure(row)
    education_value = education.get("value")
    if education_value is not None and education.get("units") == "years":
        education_value = f"{education_value:g} years"
    items = [("WAB-AQ", row.get("wab_aq")),
             ("Age at stroke", row.get("age_at_stroke")),
             ("Education", education_value),
             ("Sex", row.get("sex")),
             ("Days to WAB", row.get("wab_days")),
             ("Lesion volume", f"{volume_ml:.1f} mL" if volume_ml is not None else "&#8212;")]
    rows = "".join(f"<tr><td style='padding:2px 8px'><b>{k}</b></td>"
                   f"<td style='padding:2px 8px'>{v or '&#8212;'}</td></tr>" for k, v in items)
    used = (f"<div style='font-size:11px;color:#888;margin-top:6px'>"
            f"Mapped to KB predictors: {', '.join(predictors.keys()) or '&#8212;'}</div>") if predictors else ""
    return "<table class='behaviour-table'>" + rows + "</table>" + used


STAGE_COLOURS = {"acute": ("#f45b69", "rgba(244,91,105,.10)"),
                 "subacute": ("#52489c", "rgba(82,72,156,.10)"),
                 "chronic": ("#4062bb", "rgba(64,98,187,.10)"),
                 None: ("#d6d6d6", "#f7f7f7")}


def stage_badge(stage_id, label):
    border, bg = STAGE_COLOURS.get(stage_id, STAGE_COLOURS[None])
    return (f"<span style='display:inline-block;white-space:nowrap;background:{bg};color:#2b2b3a;border:1px solid {border};"
            f"padding:1px 8px;border-radius:3px;font-size:11px;font-weight:bold'>{label}</span>")


LEGEND_HTML = '''
      <div class="legend">
        <p><b>Display signal</b> is CALMaR&rsquo;s project-specific ordering heuristic, not a formal evidence
        grade or participant-level prediction. Its basis is explained beside the outcome summaries.</p>
        <p><b>Relationship</b> is what a study reported between the region or measure and the outcome:
        association, inverse association, no association or mixed results. <b>Evidence strength</b> is
        the extractor&rsquo;s reading of the finding. <b>Extraction confidence</b> is confidence that the
        paper was transcribed and interpreted correctly. These are distinct.</p>
        <p>Finding counts are descriptive. They do not measure certainty, and findings do not necessarily
        represent independent studies or independent cohorts. Group associations do not predict this participant&rsquo;s outcome.</p>
        <p>An &ldquo;atlas match includes a documented judgement call&rdquo; note links a knowledge-base region to
        atlas units using a curated decision recorded in <code>stroke-aphasia-kb/atlas_mapping/README.md</code>.</p>
        <b>WAB/WAB-R profile conversion</b>: where a recorded type informed the domain table,
        + relatively preserved kept severity unassigned and &#8722; impaired became a &ldquo;mild profile floor&rdquo;.
        Neither is a measured domain severity.<br>
        <b>Stage badge</b>:
        Acute &lt;7 d &middot; Subacute 7 d–6 mo &middot; Chronic &gt;6 mo. A therapy-stage warning identifies
        evidence from a different recovery stage; open it for detail.
        Rules and their sources: <code>stroke-aphasia-kb/scripts/aphasia_rules.py</code>.
      </div>'''


def report_section(title, content, *, open=False):
    """One accessible major report disclosure with parser-safe markers."""
    opened = " open" if open else ""
    section_id = "section-" + re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return (f"<!-- calmar-section:{escape(title)} -->"
            f"<details class='report-section' id='{section_id}' data-print-open{opened}><summary>"
            f"<h2 class='section-title'><span>{title}</span>"
            "<span class='section-action' aria-hidden='true'><span class='when-closed'>Open section</span>"
            "<span class='when-open'>Close section</span></span></h2></summary>"
            f"<!-- calmar-section-content --><div class='report-section-body'>{content}</div>"
            "</details><!-- calmar-section-end -->")


def standalone_html(title, body):
    """Wrap report markup in a printable standalone page."""
    return f'''<!DOCTYPE html>
<html class="calmar-report-page" lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
.calmar-report{{
  --calmar-grape:#52489c;--calmar-blue:#4062bb;--calmar-cyan:#59c3c3;
  --calmar-platinum:#ebebeb;--calmar-pink:#f45b69;--calmar-ink:#2b2b3a;
  --calmar-ink-2:#5a5a66;--calmar-cyan-ink:#1f7f7f;--calmar-panel:#f7f7f7;
  --calmar-line:#ebebeb;--calmar-line-strong:#d6d6d6;
}}
.calmar-report,.calmar-report *{{box-sizing:border-box}}
html.calmar-report-page{{background:#f7f7f7}}
.calmar-report{{font-family:Arial,Helvetica,sans-serif;background:#fff;color:var(--calmar-ink);
  font-size:17px;line-height:1.55;overflow-wrap:break-word}}
body.calmar-report{{width:min(94vw,88rem);margin:2.5rem auto;padding:0 1.5rem 4rem}}
.calmar-report h1,.calmar-report h2,.calmar-report h3,.calmar-report h4,.calmar-report h5,.calmar-report h6{{color:var(--calmar-grape);line-height:1.25}}
.calmar-report p{{max-width:100%}}
.calmar-report code{{font-size:.86em;overflow-wrap:anywhere}}
.calmar-report a{{color:var(--calmar-blue)}}
.calmar-report button{{font:inherit}}
.report-header{{border:1px solid var(--calmar-line-strong);border-top:5px solid var(--calmar-grape);
  border-radius:5px;padding:1.25rem 1.4rem;background:#fff;color:var(--calmar-ink)}}
.report-header h1{{font-size:1.45rem;margin:0 0 .45rem}}
.report-meta{{color:var(--calmar-ink-2);font-size:.88rem;line-height:1.6}}
.calmar-provenance{{border:1px solid var(--calmar-line-strong);border-left:5px solid var(--calmar-grape);
  background:rgba(82,72,156,.08);padding:1rem 1.25rem;margin:1rem 0;font-size:.9rem;break-inside:avoid}}
.calmar-provenance ul{{margin:.55rem 0 0 1.2rem;padding:0}}
.calmar-provenance li+li{{margin-top:.3rem}}
.provenance-warning{{display:block;border-left:4px solid var(--calmar-pink);padding-left:.5rem;margin-top:.35rem}}
.report-content{{border:1px solid var(--calmar-line-strong);border-radius:5px;padding:1.4rem;background:#fff}}
.report-section{{border-top:1px solid var(--calmar-line)}}
.report-section:first-child{{border-top:0}}
.report-section>summary{{display:flex;justify-content:space-between;align-items:baseline;gap:1rem;cursor:pointer;
  padding:1.15rem .15rem;color:var(--calmar-grape);font-size:1.35rem;font-weight:700;line-height:1.25}}
.report-section .section-title{{display:flex;justify-content:space-between;align-items:baseline;gap:1rem;
  width:100%;font:inherit;color:inherit;margin:0}}
.report-section>summary::marker{{color:var(--calmar-grape)}}
.report-section-body{{padding:.1rem .25rem 2.1rem}}
.section-action{{color:var(--calmar-blue);font-size:.75rem;font-weight:600;white-space:nowrap}}
.section-action .when-open{{display:none}}
.report-section[open] .section-action .when-closed{{display:none}}
.report-section[open] .section-action .when-open{{display:inline}}
.section-intro{{font-size:1.02rem;margin:.2rem 0 .8rem;color:var(--calmar-ink);max-width:100%}}
.method-note{{font-size:.88rem;color:var(--calmar-ink-2);margin:.35rem 0 .9rem;max-width:100%}}
.outcome-cards{{margin:1.25rem 0 2.25rem}}
.outcome-card{{padding:1.25rem 0 1.45rem;border-top:1px solid var(--calmar-line);break-inside:avoid}}
.outcome-card:last-child{{border-bottom:1px solid var(--calmar-line)}}
.outcome-card header{{display:flex;gap:1rem;align-items:flex-start;justify-content:space-between}}
.outcome-card h3{{font-size:1.18rem;margin:.08rem 0 .35rem}}
.outcome-kind{{margin:0;color:var(--calmar-ink-2);font-size:.76rem;text-transform:uppercase;letter-spacing:.05em}}
.display-signal{{display:inline-flex;flex-direction:column;align-items:flex-end;line-height:1.15;white-space:nowrap}}
.display-stars{{color:var(--calmar-grape);font-family:"DejaVu Sans",Arial,Helvetica,sans-serif;
  font-size:1rem;letter-spacing:.05em}}
.display-stars-print{{display:none;color:var(--calmar-grape);font-size:.78rem}}
.display-label{{color:#777784;font-size:.69rem;font-weight:400;margin-top:.12rem}}
.display-signal-note{{border-left:4px solid var(--calmar-blue);padding:.55rem .8rem;margin:1rem 0;background:rgba(64,98,187,.06)}}
.display-signal-note summary,.source-list summary,.region-list summary,.citation-detail summary,.finding-more summary,
.measure-findings summary{{color:var(--calmar-blue);font-weight:600;cursor:pointer}}
.calmar-report summary:focus-visible,.calmar-report button:focus-visible,.calmar-report [tabindex]:focus-visible{{outline:3px solid var(--calmar-cyan-ink);outline-offset:3px}}
.visually-hidden{{position:absolute!important;width:1px!important;height:1px!important;padding:0!important;margin:-1px!important;
  overflow:hidden!important;clip:rect(0,0,0,0)!important;white-space:nowrap!important;border:0!important}}
.matched-findings,.relevance-basis{{font-size:.88rem;color:var(--calmar-ink-2);margin:.35rem 0 .45rem}}
.finding-counts{{display:flex;flex-wrap:wrap;gap:.25rem 1.2rem;margin:.45rem 0 .65rem;font-size:.86rem;color:var(--calmar-ink-2)}}
.finding-counts span{{white-space:nowrap}}
.finding-counts strong{{color:var(--calmar-ink);font-weight:650}}
.finding-indicators{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.5rem;margin:.85rem 0}}
.finding-indicators div{{border-left:3px solid var(--calmar-line-strong);padding:.15rem .55rem}}
.finding-indicators dt{{font-size:.73rem;text-transform:uppercase;letter-spacing:.035em;color:var(--calmar-ink-2)}}
.finding-indicators dd{{margin:0;font-weight:700}}
.region-preview{{font-size:.9rem;color:var(--calmar-ink-2);margin:.75rem 0 .2rem}}
.region-list,.source-list,.citation-detail{{font-size:.86rem;margin:.35rem 0}}
.source-list>div{{margin:.4rem 0 .2rem .75rem}}
.source-list .citation-detail{{margin:.25rem 0}}
.citation-detail p{{margin:.35rem 0 .6rem;padding-left:.75rem;border-left:2px solid var(--calmar-line-strong)}}
.subsection-heading{{margin:2rem 0 .75rem}}
.subsection-heading h3{{font-size:1.25rem;margin:0 0 .25rem}}
.subsection-heading p{{font-size:.9rem;color:var(--calmar-ink-2);margin:0}}
.additional-regions,.additional-outcomes{{margin-top:.9rem;border:1px solid var(--calmar-line-strong);border-radius:3px;padding:.65rem .8rem}}
.additional-regions>summary,.additional-outcomes>summary{{color:var(--calmar-blue);font-weight:600;cursor:pointer}}
.additional-regions-body{{margin-top:.45rem}}
.additional-outcomes>.outcome-cards{{margin:.5rem 0 0}}
.tract-direction{{display:flex;flex-wrap:wrap;gap:.15rem .8rem;font-size:.82rem;color:var(--calmar-ink-2)}}
.tract-direction span{{white-space:nowrap}}
.shared-symptoms{{grid-column:1/-1;font-size:.82rem;color:var(--calmar-ink-2)}}
.shared-symptom-detail{{margin:.25rem 0 1rem;padding:.5rem .8rem;border-left:3px solid var(--calmar-line-strong)}}
.shared-symptom-detail p{{margin:.2rem 0}}
.shared-symptom-detail ul{{margin:.4rem 0 .4rem 1.25rem;padding:0}}
.shared-symptom-detail li+li{{margin-top:.2rem}}
.region-evidence{{border-top:1px solid var(--calmar-line)}}
.region-evidence:last-of-type{{border-bottom:1px solid var(--calmar-line)}}
.region-evidence>summary{{display:grid;grid-template-columns:minmax(15rem,1.2fr) minmax(16rem,1fr);gap:.3rem 1rem;
  cursor:pointer;padding:.95rem .25rem;align-items:start}}
.region-title{{font-weight:700;color:var(--calmar-grape)}}
.region-title span{{font-weight:400;color:var(--calmar-ink-2)}}
.region-facts{{font-size:.88rem;color:var(--calmar-ink-2)}}
.region-notes{{grid-column:1/-1;display:flex;gap:.5rem;flex-wrap:wrap;font-size:.78rem}}
.region-action{{grid-column:1/-1;color:var(--calmar-blue);font-size:.8rem;font-weight:600}}
.region-action .when-open{{display:none}}
.region-evidence[open] .region-action .when-closed{{display:none}}
.region-evidence[open] .region-action .when-open{{display:inline}}
.mapping-note,.thin-evidence,.phase-summary,.laterality-note{{border-left:3px solid var(--calmar-pink);padding-left:.45rem;color:var(--calmar-ink)}}
.region-body{{padding:.25rem 0 1.25rem 1rem}}
.region-alias{{font-size:.84rem;color:var(--calmar-ink-2);margin:.2rem 0 .8rem}}
.outcome-findings{{margin:1rem 0 1.65rem}}
.outcome-findings h4{{font-size:1.05rem;margin:0 0 .35rem}}
.outcome-findings h4 span{{font-size:.78rem;font-weight:400;color:var(--calmar-ink-2)}}
.finding{{padding:1rem 0;border-top:1px solid var(--calmar-line);break-inside:avoid-page}}
.finding-claim{{font-size:1rem;margin:0 0 .35rem;max-width:100%}}
.finding-source,.finding-governance{{font-size:.82rem;color:var(--calmar-ink-2);margin:.25rem 0;max-width:100%}}
.citation-key{{font-weight:700;color:var(--calmar-blue)}}
.finding-indicators{{grid-template-columns:repeat(3,minmax(0,1fr));max-width:48rem}}
.finding-indicators dd{{font-size:.88rem;font-weight:600;text-transform:capitalize}}
.finding-more{{margin:.5rem 0;font-size:.87rem}}
.finding-more-body{{margin:.6rem 0;padding:.75rem 1rem;background:var(--calmar-panel);border-left:3px solid var(--calmar-line-strong)}}
.detail-heading{{font-weight:700;color:var(--calmar-grape);margin:.8rem 0 .25rem}}
.detail-list{{display:grid;grid-template-columns:minmax(8rem,max-content) 1fr;gap:.2rem .8rem;margin:.25rem 0}}
.detail-list dt{{font-weight:700;color:var(--calmar-ink-2)}}
.detail-list dd{{margin:0}}
.calmar-report blockquote{{margin:.7rem 0;padding:.1rem 0 .1rem 1rem;border-left:3px solid var(--calmar-line-strong)}}
.calmar-report blockquote p{{margin:.2rem 0}}
.calmar-report blockquote footer{{font-size:.78rem;color:var(--calmar-ink-2)}}
.measure-cards{{border-top:1px solid var(--calmar-line)}}
.measure-card{{padding:1.2rem 0;border-bottom:1px solid var(--calmar-line);break-inside:avoid}}
.measure-card header{{display:grid;grid-template-columns:minmax(12rem,.7fr) minmax(15rem,1.3fr);gap:1rem}}
.measure-card h3,.measure-card header p{{margin:0}}
.measure-card .secondary,.secondary{{color:var(--calmar-ink-2)}}
.stage-warning{{display:inline-block;margin:.25rem 0;font-size:.75rem;font-weight:400}}
.stage-warning summary{{color:var(--calmar-ink);font-weight:700;text-decoration:underline;text-decoration-color:var(--calmar-pink);
  text-decoration-thickness:2px;cursor:pointer}}
.stage-warning-detail{{display:block;max-width:32rem;padding:.35rem .5rem;border-left:3px solid var(--calmar-pink);
  color:var(--calmar-ink-2);font-weight:400}}
.table-scroll{{max-width:100%;overflow-x:auto;border:1px solid var(--calmar-line);border-radius:3px}}
.data-table,.behaviour-table{{border-collapse:collapse;width:100%;font-size:.88rem}}
.data-table th{{background:var(--calmar-grape);color:#fff}}
.data-table th,.data-table td{{padding:.45rem .55rem;text-align:left;vertical-align:top;border-bottom:1px solid var(--calmar-line)}}
.data-table td{{overflow-wrap:anywhere}}
.damaged-table th:first-child,.damaged-table td:first-child{{text-align:left}}
.damaged-table .numeric{{text-align:center}}
.evidence-path{{margin:.85rem 0 1.35rem;padding:.55rem .8rem;border-left:4px solid var(--calmar-blue);
  background:rgba(64,98,187,.06);break-inside:avoid-page}}
.evidence-path ol{{margin:.45rem 0 .45rem 1.25rem;padding:0}}
.evidence-path>summary{{color:var(--calmar-blue);font-weight:600;cursor:pointer}}
.evidence-path>div{{margin-top:.55rem}}
.evidence-path li+li{{margin-top:.25rem}}
.evidence-path p{{margin:.45rem 0 0;font-size:.88rem;color:var(--calmar-ink-2)}}
.data-table .cell-value{{min-width:0}}
.behaviour-table{{width:auto}}
.legend{{font-size:.86rem;color:var(--calmar-ink-2);line-height:1.55}}
.legend h5{{font-size:1.25rem}}
.legend p{{margin:.45rem 0}}
.print-only{{display:none}}
.calmar-report img{{max-width:100%;height:auto}}
@media screen and (max-width:700px){{
  body.calmar-report{{margin:0;padding:1rem .75rem 3rem;font-size:16px}}
  .report-header,.report-content{{padding:1rem}}
  .report-section>summary{{font-size:1.18rem;align-items:flex-start}}
  .outcome-card header,.measure-card header{{display:block}}
  .display-signal{{white-space:normal;margin-top:.35rem}}
  .finding-counts{{gap:.2rem .8rem}}
  .finding-indicators{{grid-template-columns:1fr}}
  .region-evidence>summary{{grid-template-columns:1fr}}
  .region-notes{{grid-column:1}}
  .region-body{{padding-left:.35rem}}
  .detail-list{{grid-template-columns:1fr}}
  .detail-list dd{{margin:0 0 .35rem}}
  .table-scroll{{overflow:visible;border:0}}
  .data-table,.data-table tbody,.data-table tr,.data-table td{{display:block;width:100%}}
  .data-table colgroup,.data-table thead{{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;
    clip:rect(0,0,0,0);white-space:nowrap;border:0}}
  .data-table tr{{padding:.55rem 0;border-top:1px solid var(--calmar-line)}}
  .data-table td{{display:grid;grid-template-columns:minmax(8rem,40%) minmax(0,1fr);gap:.65rem;text-align:left!important;
    border:0;padding:.28rem .15rem!important;min-width:0!important}}
  .data-table td::before{{content:attr(data-label);font-weight:700;color:var(--calmar-ink-2);font-size:.78rem}}
}}
@media print{{
  @page{{margin:14mm}}
  html.calmar-report-page,body.calmar-report{{background:#fff}}
  body.calmar-report{{max-width:none;margin:0;padding:0;font-size:10pt;line-height:1.42}}
  .no-print{{display:none!important}}
  .report-header,.report-content,.calmar-provenance{{border-color:var(--calmar-line-strong);box-shadow:none}}
  .outcome-card,.measure-card,.finding{{break-inside:avoid-page}}
  .region-evidence{{break-inside:auto}}
  .region-evidence>summary{{display:block}}
  .region-title,.region-facts,.region-notes,.tract-direction,.shared-symptoms{{display:block}}
  .region-facts{{margin-top:.15rem}}
  .region-action{{display:none}}
  .screen-only{{display:none!important}}
  .print-only{{display:block}}
  .stage-warning{{display:none}}
  .stage-warning-print{{font-size:8pt;border-left:2px solid var(--calmar-pink);padding-left:.35rem}}
  .calmar-report details>summary{{break-after:avoid-page}}
  .calmar-report details:not([data-print-open]){{display:none!important}}
  .calmar-report details[data-print-open]>*:not(summary){{display:block!important}}
  .display-stars{{display:none}}
  .display-stars-print{{display:inline}}
  .report-section{{border-top:0}}
  .report-section>summary{{font-size:15pt;padding:1.2rem 0 .35rem}}
  .section-action{{display:none}}
  .report-section-body{{padding:0 0 .6rem}}
  .table-scroll{{overflow:visible}}
  .calmar-report table{{break-inside:avoid-page}}
  .finding-more-body{{background:#fff}}
}}
</style></head><body class="calmar-report">
<div class="no-print" style="margin-bottom:16px">
  <button onclick="window.print()" style="padding:8px 18px;background:#4062bb;color:white;border:none;border-radius:4px;cursor:pointer">
    Save / Print PDF</button>
  <span style="color:#5a5a66;font-size:.82rem;margin-left:10px">Use your browser's PDF option when printing</span>
</div>
{body}
<script>
function revealReportTarget(id){{
  const target=id && document.getElementById(id);
  if(target){{
    if(target.tagName==='DETAILS') target.open=true;
    let ancestor=target.parentElement && target.parentElement.closest('details');
    while(ancestor){{
      ancestor.open=true;
      ancestor=ancestor.parentElement && ancestor.parentElement.closest('details');
    }}
    target.scrollIntoView({{block:'start'}});
  }}
}}
document.addEventListener('DOMContentLoaded',()=>{{
  revealReportTarget(location.hash.slice(1));
  document.addEventListener('click',(event)=>{{
    const link=event.target.closest('a[href^="#"]');
    if(link) revealReportTarget(link.getAttribute('href').slice(1));
  }});
}});
window.addEventListener('hashchange',()=>revealReportTarget(location.hash.slice(1)));
let calmarPrintState=[];
window.addEventListener('beforeprint',()=>{{
  const printable=[...document.querySelectorAll('details[data-print-open]')];
  calmarPrintState=printable.map(item=>item.open);
  printable.forEach(item=>{{item.open=true}});
}});
window.addEventListener('afterprint',()=>{{
  document.querySelectorAll('details[data-print-open]').forEach(
    (item,index)=>{{item.open=calmarPrintState[index]}});
  calmarPrintState=[];
}});
</script>
</body></html>'''


def save_report(entry, source, reports_dir, title_card, qc_notice, provenance, overlay, body):
    """Write ``interpretation_<sub>_<ses>_<source>.html``; return (path, page html, inline html).

    Order in the saved page: title, QC checkpoint notice, provenance/caveats,
    static lesion overlay, report body.
    """
    inline = title_card + qc_notice + provenance + overlay + body
    path = Path(reports_dir) / f"interpretation_{entry['subject']}_{entry.get('session') or 'nosession'}_{source}.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    page = standalone_html(f"Lesion interpretation — {entry['subject']} {entry.get('session') or ''}", inline)
    path.write_text(page, encoding="utf-8")
    return path, page, inline


def _overlay_img(namespace, entry, mask, background, source):
    """Static lesion overlay (rendered in Slurm) embedded in the saved report.

    The live NiiVue viewer is not serialised into the HTML file, so the saved
    report and its printed PDF carry this PNG instead.
    """
    from . import reporting
    label = MASK_LABELS.get(source, source)
    if not Path(mask).exists():
        return ("<p style='font-size:12px;color:#888;font-family:sans-serif'>"
                f"No MNI-space lesion mask found ({Path(mask).name}) &mdash; run the warp cells first.</p>")
    try:
        png = reporting.run_reporting_task(namespace, "report_overlay", mask=str(mask),
                                           background=str(background), source=source)
        data = base64.b64encode(Path(png).read_bytes()).decode("ascii")
        return ("<div style='margin:4px 0 12px;font-family:sans-serif'>"
                "<div style='font-size:12px;color:#555;margin-bottom:4px'>"
                f"<b>Lesion viewer</b> &mdash; {entry['subject']} {entry.get('session') or ''} "
                f"(MNI space) &nbsp;{cc.legend([source])} {label} lesion</div>"
                "<img alt='Lesion overlay (MNI space)' style='width:100%;max-width:920px;border-radius:6px;"
                f"background:#000;display:block' src='data:image/png;base64,{data}'></div>")
    except Exception as exc:
        return ("<p style='font-size:12px;color:#c62828;font-family:sans-serif'>"
                f"Could not render lesion overlay: {escape(str(exc))}</p>")


# ============================================================
# Main entry points
# ============================================================

def generate_participant_report(entry, source, settings, *, study, namespace, reports_dir,
                                dataset_dir, atlas_dir, kb_root, helpers, run_decoding=False,
                                kb_reason=None):
    """Build, save and return the interpretation report for one participant + mask.

    ``study`` (calmar.study.Study) locates masks and derivatives. ``namespace``
    is the notebook namespace; it is used only by the Slurm helpers that still
    require one (``atlas_overlap.prepare_report_overlap`` needs ALL_ATLASES,
    CONFIG, _mask_path_for and PROJECT_DIR; ``reporting.run_reporting_task``
    needs PROJECT_DIR) and to read the OVERLAP_PATHS they publish.
    """
    from .atlas_overlap import prepare_report_overlap
    from .qc_decisions import report_qc_notice
    from .report_evidence import (MAP_LABELS, disconnection_section, disconnectome_map, is_symptom_target,
                                  location_coverage, location_section, measures_section, tract_atlases)
    from .report_ui import ParticipantReport, report_sections

    messages = []
    note = messages.append
    if kb_reason is None:
        from .kb_location import resolve_kb_root
        try:
            selected_root, selected_reason = resolve_kb_root(namespace.get("PROJECT_DIR"))
        except FileNotFoundError:
            selected_root, selected_reason = None, "explicit report root"
        kb_reason = (selected_reason if selected_root == Path(kb_root).expanduser().resolve()
                     else "explicit report root")
    aphasia_kb, rules = _kb_modules(kb_root)
    kb = load_kb(kb_root, settings, aphasia_kb=aphasia_kb)
    note(kb.summary())
    kb_line = kb_version_text(kb_version(kb_root, kb, location=kb_reason))
    note(f"Knowledge base {kb_line}")

    if source not in study.mni_sources(entry):
        raise ValueError(f"No existing MNI mask for {source!r}, {entry['subject']} "
                         f"{entry.get('session') or ''}. Choose an available mask in the report selector.")
    mask = Path(study.mni_mask(entry, source))
    brain = (Path(study.dirs(entry)["openads"]) / "Subject_in_MNI.nii.gz"
             if source == "openads" else Path(study.template_dir(entry)) / "Subject_in_MNI.nii.gz")
    # prepare_report_overlap reads the atlas list from INTERP_KB_ATLASES; give it ours.
    view = dict(namespace, INTERP_KB_ATLASES=list(settings.kb_atlases))
    prepare_report_overlap(view, entry, source)
    for key in ("OVERLAP_PATHS", "OVERLAP_DFS"):
        if key in view:
            namespace.setdefault(key, {}).update(view[key])
    overlap_paths = namespace.get("OVERLAP_PATHS", {})
    note(f"\nInterpreting: {entry['subject']} {entry.get('session') or ''} ({source} mask)")

    # 1. Lesion location -> KB predictions
    imaging, per_atlas = imaging_interpretation(kb, rules, entry, source, settings, overlap_paths, reports_dir)
    damage, _ = lesion_damage(entry, source, settings, overlap_paths, reports_dir)
    location_rows = kb.location_findings(damage, min_overlap=settings.min_overlap_pct, min_region=settings.min_region_pct,
                                         min_confidence=("high" if settings.high_conf_only else None))
    # Tracts disconnected by the lesion, from its BCBToolkit or DeepDisco map.
    map_path = disconnectome_map(study, entry, source, settings.disconnectome)
    disconnection, disconnection_rows, map_label = None, None, None
    atlases = tract_atlases(namespace.get("ALL_ATLASES"))
    if map_path is not None and atlases:
        import atlas_mapping
        disconnection = atlas_mapping.region_disconnection(atlas_mapping.tract_disconnection(map_path, atlases))
        disconnection_rows = kb.location_findings(
            disconnection, min_overlap=101.0, min_region=settings.min_disconnected_pct,
            min_confidence=("high" if settings.high_conf_only else None))
        map_label = MAP_LABELS[settings.disconnectome]
        note(f"  Tract disconnection from {map_path.name}: {0 if disconnection_rows is None else len(disconnection_rows)} findings")
    damaged = damaged_regions(entry, source, settings, overlap_paths, reports_dir)
    note("  Overlap rows by atlas (matched to KB regions through stroke-aphasia-kb/atlas_mapping):")
    for atlas, n in per_atlas:
        note(f"    . {atlas:14s} {n:3d} regions overlapped")

    # 2. Clinical data -> KB predictor predictions, recovery stage
    dataset_for = getattr(study, "dataset_for", lambda entry: dataset_dir)
    dataset_dir = dataset_for(entry)
    row = participant_row(dataset_dir, entry["subject"])
    predictors = row_to_predictors(row)
    predictors["education"] = education_measure(row)
    stage_id, stage_label = rules.classify_stage((row or {}).get("wab_days"))
    # STROKE_PHASE overrides; without onset data the acute (DWI) route is acute.
    from .study import modality
    config_for = getattr(study, "config_for", lambda entry: getattr(study, "config", {}) or {})
    entry_config = config_for(entry)
    configured = entry_config.get("STROKE_PHASE")
    if configured in ("acute", "subacute", "chronic"):
        stage_id = configured
        stage_label = {s: label for s, label, *_ in rules.RECOVERY_STAGES}[configured]
    elif stage_id is None and modality(entry_config) == "dwi":
        stage_id, stage_label = "acute", {s: label for s, label, *_ in rules.RECOVERY_STAGES}["acute"]
    try:
        therapy_stages = rules.therapy_evidence_stages(kb_root)
    except Exception:
        therapy_stages = {}  # non-critical: stage warnings are omitted
    volume = None
    try:
        volume = lesion_volume_ml(mask)
        predictors["lesion_volume"] = volume
    except Exception as exc:
        note(f"  lesion_volume not computed: {exc}")
    predicted = (kb.interpret_predictors(predictors, min_confidence=("high" if settings.high_conf_only else None))
                 if predictors else pd.DataFrame())

    # 3. Therapies for predicted + WAB-implied impairments
    impairments = []
    if not imaging.empty:
        symptom_rows = imaging.apply(
            lambda row: is_symptom_target(rules, row["target"], row["target_kind"]), axis=1)
        impairments += list(imaging[symptom_rows]["target"].head(settings.top_n * 2))
    if not predicted.empty:
        impairments += list(predicted[predicted["target_kind"] == "impairment"]["target"].head(settings.top_n))
    impairments = list(dict.fromkeys(impairments))
    wab_type = (row or {}).get("wab_type") or ""
    behavioural = kb.wab_to_impairments(wab_type)
    note(f"  Recorded behavioural profile -> KB therapy-gating impairments: {behavioural}")
    therapies = kb.interpret_therapies(impairments, behavioral_impairment_ids=behavioural,
                                       max_results=settings.top_n)

    # 4. HTML
    n_pred = 0 if predicted.empty else len(predicted)
    n_therapy = 0 if therapies.empty else len(therapies)
    conf_note = ("(high-confidence findings only)" if settings.high_conf_only
                 else "(all confidence levels included)")
    kb_scope = f"{', '.join(settings.include)} {conf_note}"
    days = (row or {}).get("wab_days")
    try:
        days_text = f"{int(float(days))} days post-onset"
    except (TypeError, ValueError):
        days_text = "onset date unknown"
    label = MASK_LABELS.get(source, source)
    title_card = f'''
    <header class="report-header">
      <h1>Clinical interpretation &mdash;
        {entry['subject']} {entry.get('session') or ''}
        &nbsp; {stage_badge(stage_id, stage_label)}
        <small style="font-weight:normal;color:#5a5a66;font-size:.8rem">&nbsp; {days_text}</small>
      </h1>
      <div class="report-meta">
        Lesion mask: <b>{label}</b> &middot; recovery stage: <b>{stage_label}</b> &middot;
        research use only, not a diagnosis
        <br>
        Selected evidence scope: <b>{', '.join(settings.include)}</b> &middot; {conf_note} &middot;
        atlas (lookup): {', '.join(settings.kb_atlases)} &middot;
        atlas (display): {settings.display_atlas}
      </div>
    </header>
    '''
    domain_key = f"{entry['subject']}|{entry.get('session') or ''}"
    levels_by_participant = namespace.get("INTERP_DOMAIN_LEVELS_BY_PARTICIPANT") or {}
    sources_by_participant = namespace.get("INTERP_DOMAIN_LEVEL_SOURCES_BY_PARTICIPANT") or {}
    if domain_key in levels_by_participant:
        domain_levels = normalise_domain_levels(levels_by_participant[domain_key])
        domain_sources = dict(sources_by_participant.get(domain_key) or {})
    elif levels_by_participant:
        # Another participant's current UI values must never leak into this report.
        domain_levels, domain_sources = wab_profile_domain_levels(rules, (row or {}).get("wab_type"))
    elif "INTERP_DOMAIN_LEVELS" in namespace:
        domain_levels = normalise_domain_levels(namespace.get("INTERP_DOMAIN_LEVELS"))
        domain_sources = dict(namespace.get("INTERP_DOMAIN_LEVEL_SOURCES") or {})
    else:
        domain_levels, domain_sources = wab_profile_domain_levels(rules, (row or {}).get("wab_type"))
    context = f'''
      <h3>Behavioural / clinical data</h3>
      <p class="section-intro">These participant measures provide context before the lesion description. Missing
        raw measures remain missing; any qualitative WAB-profile conversion is identified separately below.</p>
      {behaviour_html(rules, row, predictors, volume)}
      <h3>Domain-level impairment context</h3>
      {domain_levels_html(domain_levels, domain_sources)}
      <h3>Damaged regions ({settings.display_atlas}, &ge;{settings.min_overlap_pct}%)</h3>
      <p class="section-intro">This table locates the lesion in the selected display atlas. It is an anatomical
        overview; the literature interpretation follows below.</p>
      {damaged_regions_html(damaged, settings.display_atlas, atlas_dir)}'''
    location = location_section(
        kb, rules, location_rows, damage, location_coverage(kb, location_rows, damage), settings, phase=stage_id,
        lesion_volume_ml=volume)
    white_matter = disconnection_section(
        kb, rules, disconnection_rows, disconnection, damage, settings, map_label, phase=stage_id,
        map_name=map_path.name if map_path is not None else None, mask_label=label,
        lesion_rows=location_rows)
    from .diffusion import direct_diffusion_section
    direct_diffusion = direct_diffusion_section(dataset_dir, entry_config, entry)
    from .brain_health import brain_health_measure_note, brain_health_measure_records
    brain_health_records = brain_health_measure_records(dataset_dir, entry_config, entry)
    for record in brain_health_records:
        predictors[record["id"]] = record
    brain_health_note = brain_health_measure_note(dataset_dir, entry_config, entry, stroke_phase=stage_id)
    measures = f'''
      <p class="section-intro">Findings about measures such as lesion volume or aphasia severity report
        associations in study groups (for example, larger lesions with more severe aphasia), not predictions for
        one person.</p>
      {brain_health_note}
      {measures_section(kb, predictors, _days(days), "high" if settings.high_conf_only else None, phase=stage_id)}'''
    therapy = f'''
      <p class="section-intro">These are therapies with evidence targeting impairments represented above. They are
        research associations, not prescriptions; recovery-stage mismatches remain marked for clinical review.
        Therapy gating uses the KB mapping from the recorded WAB profile, not the report-only domain-level table.</p>
      {therapy_table(kb, therapies, stage_id, stage_label, therapy_stages)}'''
    body = ("<main class='report-content'>"
            + report_section("Participant context and lesion overview", context, open=True)
            # Non-lesion predictors (age, education, severity, lesion volume)
            # come before location: they carry most of the prognostic weight
            # (Brain Communications 2024 commentary, fcae364; Huygelier 2025).
            + report_section("This participant’s measures: what the evidence says", measures, open=True)
            + report_section("Lesion location: what the evidence says", location, open=True)
            + report_section("White-matter disconnection: normative lesion-based models", white_matter)
            + (report_section("Direct diffusion measurements: participant dMRI", direct_diffusion)
               if direct_diffusion is not None else "")
            + report_section(f"Therapy recommendations ({n_therapy} matched)", therapy)
            + report_section("How to read the evidence", LEGEND_HTML)
            + "</main>")

    # 5. Provenance, QC notice, overlay; save
    from .mask_method import mask_method_html
    try:
        method = mask_method_html(study, entry, source)
    except Exception as exc:          # the report is still useful without it
        method = None
        note(f"  mask method not described: {exc}")
    try:
        qc_anchor = study.qc_anchor(entry, source)
        qc_directory = study.qc_dir(entry, source)
    except TypeError:  # compatibility with lightweight third-party Study adapters
        qc_anchor = study.qc_anchor(entry)
        qc_directory = study.qc_dir(entry)
    qc = mask_qc_summary(qc_anchor, mask, source)
    provenance = provenance_html(source, mask, qc, kb_scope=kb_scope, method=method, kb=kb_line)
    qc_notice = report_qc_notice(Path(qc_directory), entry)
    overlay = _overlay_img(namespace, entry, mask, brain, source)
    path, page, _ = save_report(entry, source, reports_dir, title_card, qc_notice, provenance, overlay, body)
    note(f"  Report saved → {path}")

    sections = [("Provenance and caveats", provenance)] + report_sections(body)
    sections.append(("Generation details", "<pre>" + escape("\n".join(messages)) + "</pre>"))
    panel = ParticipantReport(title_card, qc_notice, sections, path, page, brain, mask, helpers,
                              decode=run_decoding, source=source)
    return ParticipantReportResult(dict(entry), source, path, panel, messages)


# ============================================================
# Optional Neurosynth decoding
# ============================================================

_TERM_COLOR, _REG_COLOR, _IMP_COLOR, _WARN_COLOR = "#1a6b3a", "#1a3a6b", "#7b3f00", "#856404"
#: Terms shown: top N with correlation above MIN_R (display choice, not a significance test).
DECODE_TOP_TERMS, DECODE_MIN_R = 10, 0.05


def _pill(text, color):
    return (f'<span style="display:inline-block;padding:2px 7px;border-radius:4px;'
            f'background:{color};color:#fff;font-size:0.82em;margin:1px">{text}</span>')


def render_decode(label, path, space, dec):
    """HTML sections ('header', 'atlas', 'neurosynth', 'impairments', 'therapy') for one decode."""
    sections = {}
    hdr = [f'<h3 style="margin-bottom:2px;color:#1a1a1a">{label}</h3>',
           f'<p style="color:#555;font-size:0.85em;margin-top:2px;background:#fff;padding:4px 6px;border-radius:4px">'
           f'<code>{path}</code><br>Space: {space} &nbsp;·&nbsp; '
           f'Lesion size: <b>{dec["lesion_voxels"]}</b> voxels (after resample to MNI 2 mm)</p>']
    hdr += [f'<p style="color:{_WARN_COLOR}">⚠ {w}</p>' for w in dec.get("warnings", [])]
    sections["header"] = "\n".join(hdr)

    th = '<th style="padding:5px 8px;text-align:left;border-bottom:2px solid #ccc">{}</th>'
    td = '<td style="padding:4px 8px{style}">{value}</td>'
    tr = '<tr style="border-bottom:1px solid #eee;background:#ffffff;color:#1a1a1a">{}</tr>'
    head = ('<table style="border-collapse:collapse;width:100%;font-size:0.88em">'
            '<tr style="background:#f0f0f0;color:#1a1a1a">{}</tr>')

    reg = dec["region_overlap"]
    atl = ['<h4 style="margin:0 0 6px 0;color:#1a1a1a">HarvardOxford cortical atlas overlap</h4>']
    if reg.empty:
        atl.append('<p style="color:#1a1a1a"><em>No atlas regions overlap the lesion (&ge;3 voxels).</em></p>')
    else:
        atl.append(head.format("".join(th.format(c) for c in
                                       ["Region", "Hemi", "Overlap (vox)", "Overlap (%)", "KB region"])))
        for _, row in reg.iterrows():
            kb_rid = row.get("kb_region_id", "")
            hemi = "#c62828" if row["hemisphere"] == "left" else "#1565c0"
            atl.append(tr.format(
                td.format(style="", value=row["ho_label"])
                + td.format(style=f";color:{hemi}", value=row["hemisphere"])
                + td.format(style=";text-align:right", value=row["overlap_voxels"])
                + td.format(style=";text-align:right", value=f'{row["overlap_pct"]}%')
                + td.format(style="", value=_pill(kb_rid, _REG_COLOR) if kb_rid else '<span style="color:#999">—</span>')))
        atl.append("</table>")
    sections["atlas"] = "\n".join(atl)

    nsy = [f'<h4 style="margin:0 0 6px 0;color:#1a1a1a">Neurosynth term decoding '
           f'(top {DECODE_TOP_TERMS}, r &gt; {DECODE_MIN_R:g})</h4>']
    terms = dec["term_decoding"]
    if dec.get("neurosynth_available", False):
        nsy.append(f"<p>Decoding completed: {len(terms)} terms tested. "
                   f"Only correlations above {DECODE_MIN_R:g} are shown below.</p>")
    if terms.empty:
        nsy.append('<p style="color:#1a1a1a"><em>Neurosynth decoding unavailable.</em></p>')
    else:
        top = terms[terms["r"] > DECODE_MIN_R].head(DECODE_TOP_TERMS)
        if top.empty:
            nsy.append(f'<p style="color:#1a1a1a"><em>No terms with r &gt; {DECODE_MIN_R:g}.</em></p>')
        else:
            nsy.append(head.format("".join(th.format(c) for c in ["Term", "r", "KB impairment", "Bar"])))
            max_r = top["r"].max() or 1
            for _, t in top.iterrows():
                imp = t.get("impairment", "")
                r_col = "#1a6b3a" if t["r"] > 0.2 else ("#7b3f00" if t["r"] > 0.1 else "#555")
                bar = (f'<div style="width:{int(t["r"] / max_r * 120)}px;height:10px;'
                       f'background:{_TERM_COLOR};border-radius:2px"></div>')
                nsy.append(tr.format(
                    td.format(style="", value=t["term"])
                    + td.format(style=f";color:{r_col}", value=f'<b>{t["r"]:.4f}</b>')
                    + td.format(style="", value=_pill(imp, _IMP_COLOR) if imp else '<span style="color:#999">—</span>')
                    + td.format(style="", value=bar)))
            nsy.append("</table>")
    sections["neurosynth"] = "\n".join(nsy)

    imps = dec.get("impairment_hits", [])
    sections["impairments"] = ('<h4 style="margin:0 0 6px 0;color:#1a1a1a">Inferred impairments</h4>\n'
                               + ('<p style="color:#1a1a1a">' + " ".join(_pill(i, _IMP_COLOR) for i in imps) + "</p>"
                                  if imps else '<p style="color:#1a1a1a"><em>No impairments inferred.</em></p>'))

    trecs = dec.get("therapy_recs", None)
    ther = ['<h4 style="margin:0 0 6px 0;color:#1a1a1a">Therapy recommendations (lesion-informed)</h4>']
    if trecs is None or (hasattr(trecs, "empty") and trecs.empty):
        ther.append('<p style="color:#1a1a1a"><em>No therapy recommendations generated.</em></p>')
    else:
        ther.append(head.format("".join(th.format(c) for c in
                                        ["Therapy", "Score", "Matched impairments", "Evidence level"])))
        for _, t in trecs.head(8).iterrows():
            matched = t.get("matched_impairments", [])
            matched = (" ".join(_pill(m, _IMP_COLOR) for m in matched[:4]) if isinstance(matched, list)
                       else str(matched))
            ther.append(tr.format(
                td.format(style="", value=f"<b>{t.get('therapy_name', t.get('therapy_id', '?'))}</b>")
                + td.format(style=";text-align:right", value=t.get("score", ""))
                + td.format(style="", value=matched)
                + td.format(style="", value=t.get("evidence_level", ""))))
        ther.append("</table>")
    sections["therapy"] = "\n".join(ther)
    return sections


def decode_into_report(report, entry, source, *, kb_root, dataset_dir, project_dir, form=None):
    """Decode the report's mask with Neurosynth (Slurm) and add it to ``report``.

    ``report`` is the :class:`ParticipantReportResult` from
    :func:`generate_participant_report`; ``entry``/``source`` are the current
    form selection and must match it. ``form`` (the report-inputs panel) gets a
    status message. Returns True when Neurosynth decoding completed.
    """
    from . import reporting
    if report is None:
        raise RuntimeError("Generate the participant report before running decoding.")
    if report.selection != (entry["subject"], entry.get("session") or "", source):
        raise RuntimeError("Report inputs changed. Generate the new report before decoding.")
    panel = report.panel
    ok = True
    with panel.decode_log:
        label = f"{MASK_LABELS.get(source, source)} (MNI-space mask)"
        mask = report.panel.lesion
        print(f"[decode] subject = {entry['subject']} {entry.get('session') or ''} — 1 mask(s) to decode")
        print(f"[decode] {label}: {mask}")
        try:
            dec = reporting.run_reporting_task({"PROJECT_DIR": project_dir}, "decode", mask=str(mask),
                                               kb_root=str(kb_root), dataset=str(dataset_dir))
            ok = bool(dec.get("neurosynth_available", False))
            parts = render_decode(label, mask, "MNI152", dec)
        except Exception as exc:
            ok = False
            parts = {k: f'<p style="color:#c00">Decoding <b>{label}</b> failed: '
                        f'<code>{type(exc).__name__}: {escape(str(exc))}</code></p>'
                     for k in ("header", "atlas", "neurosynth", "impairments", "therapy")}
            print(f"[decode] ERROR on {label}: {type(exc).__name__}: {exc}")
        extra = ("<details><summary>Additional decoding evidence</summary>"
                 + parts["atlas"] + parts["impairments"] + parts["therapy"] + "</details>"
                 if len(set(parts.values())) > 1 else "")
        panel.add_decoding(parts["header"] + parts["neurosynth"] + extra)
    if form is not None:
        form.message.value = ("Participant report ready. See the Neurosynth tab for decoding results." if ok else
                              "Participant report generated, but Neurosynth decoding is incomplete. "
                              "See its tab and decoding log.")
    return ok


# ============================================================
# Small notebook helpers
# ============================================================

def selected_entry(entries, index):
    """``entries[index]`` with a readable error for a missing form choice."""
    if index is None or not 0 <= index < len(entries):
        raise ValueError("Choose a participant in the report form first.")
    return entries[index]


def outputs_inventory_html(entries, inventory_for, reports_dir, latest_report=None):
    """Counts of MNI masks per source, saved group maps and the latest report link.

    Presence only: a file being listed does not mean its QC was completed.
    """
    from .report_ui import file_link
    rows = "".join(
        f"<tr><td>{escape(MASK_LABELS[s])}</td>"
        f"<td>{sum('MNI' in inventory_for(e).get(s, {}) for e in entries)} / {len(entries)}</td></tr>"
        for s in MASK_LABELS)
    groups = sorted(Path(reports_dir).glob("group_lesion_frequency*.nii.gz"))
    links = " · ".join(file_link(p, p.name) for p in groups) or "None saved"
    report = (file_link(latest_report, "Most recently generated participant report")
              if latest_report and Path(latest_report).exists()
              else "No participant report generated in this kernel.")
    return (f"<h3>Available outputs</h3><p>{len(entries)} participant/session entries in this cohort.</p>"
            "<table><tr><th>MNI mask source</th><th>Available in cohort</th></tr>" + rows + "</table>"
            f"<p><b>Saved group maps:</b> {links}</p><p>{report}</p>")
