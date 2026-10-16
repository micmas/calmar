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
  ``ReportSettings.min_overlap_pct``; at most ``max_rois`` rows.
* Predicted impairments: :meth:`KnowledgeBase.interpret_overlap` per KB atlas,
  weighting each region by ``lesion_in_roi_percent``; scores of the same
  target from different atlases are summed. Direction and star rating follow
  ``aphasia_rules.evidence_direction`` / ``evidence_strength``.
* Outcome predictions: :meth:`KnowledgeBase.interpret_predictors` on WAB-AQ,
  age at stroke, days to WAB, sex (``participants.tsv``) and lesion volume
  (mL; voxels > 0 in the selected MNI mask × voxel volume).
* Therapies: :meth:`KnowledgeBase.interpret_therapies` from the predicted
  impairments, gated by impairments implied by the WAB type.
* Provenance: mask QC rating from the participant's ``*.qc.json`` sidecar;
  Dice between every pair of available MNI masks (> ``threshold``), resampled
  to a common grid when needed.

The clinical rules (WAB type profile, recovery stage, evidence stars) live in
``aphasia-kb/aphasia_rules.py`` and are shown by :func:`rules_html`.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from html import escape
from pathlib import Path
import base64
import itertools
import sys

import pandas as pd

from . import colors as cc
from .masks import MASK_LABELS

#: Atlases the KB lookup uses by default.
DEFAULT_KB_ATLASES = ("AAL", "HarvardOxford", "Destrieux", "Schaefer400", "JHU")

#: QC stages (calmar.qc) whose rating describes each mask source.
QC_STAGES_FOR_SOURCE = {
    "linda": ("lesion",),
    "synthstroke": ("synthstroke_lesion",),
    "manual": ("manual_lesion", "expert_mni_warp"),
}

TEMPLATE_CAVEAT = (
    "Lesion masks are on the FSL MNI152 template (MNI152NLin6Asym): LINDA's ch2 (Colin27) "
    "registration continued ch2 -> MNI152 in one resampling. Atlases are resampled to the lesion by "
    "world coordinates. Overlaps still depend on how well this individual brain was registered to "
    "MNI152, which matters most for small or thin regions.")


@dataclass
class ReportSettings:
    """User decisions for the interpretation report (set in the settings cell)."""
    kb_atlases: tuple = DEFAULT_KB_ATLASES   # atlases used to query the KB
    display_atlas: str = "HarvardOxford"     # atlas for the damaged-regions table
    high_conf_only: bool = False             # only KB findings with confidence "high"
    include_drafts: bool = True              # also use draft / in-review KB entries
    min_overlap_pct: float = 5.0             # min % of lesion in an ROI to count it
    top_n: int = 5                           # rows per prediction / therapy table
    max_rois: int = 15                       # rows in the damaged-regions table
    threshold: float = 0.5                   # mask threshold for Dice between masks

    @property
    def include(self):
        return ("approved", "in_review", "draft") if self.include_drafts else ("approved",)


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
    """Import ``aphasia_kb`` and ``aphasia_rules`` from ``kb_root`` (no reload)."""
    root = str(Path(kb_root).resolve())
    if root not in sys.path:
        sys.path.insert(0, root)
    import aphasia_kb
    import aphasia_rules
    return aphasia_kb, aphasia_rules


def load_kb(kb_root, settings):
    """KnowledgeBase from ``kb_root``. Raises if the root holds no KB entries."""
    aphasia_kb, _ = _kb_modules(kb_root)
    kb = aphasia_kb.KnowledgeBase(Path(kb_root), include=settings.include)
    if not len(kb.regions) and not len(kb.impairments):
        # A wrong root does not error inside KnowledgeBase; it loads nothing.
        raise FileNotFoundError(f"No aphasia knowledge base entries under {kb_root}")
    return kb


def rules_html(kb_root):
    """The fixed clinical/display rules as small HTML tables (for the notebook)."""
    _, rules = _kb_modules(kb_root)
    parts = []
    for title, table in rules.rules_tables().items():
        parts.append(f"<h4 style='margin:10px 0 4px'>{escape(title)}</h4>"
                     + table.to_html(index=False, border=0, escape=True))
    return ("<div style='font-size:12px'>" + "".join(parts) +
            "<p style='font-size:11px'>Defined in <code>aphasia-kb/aphasia_rules.py</code> "
            "(sources and caveats in its docstrings).</p></div>")


def decompose_html(rules, name, color="#666"):
    """WAB flu/comp/rep annotation for a type name ('' if not a WAB type)."""
    pattern = rules.decompose_aphasia(name)
    if not pattern:
        return ""
    def sym(v):
        if v == "+":
            return "<span style='color:#2e7d32'>+</span>"
        if v == "-":
            return "<span style='color:#c62828'>&#8722;</span>"
        return "<span style='color:#888'>~</span>"
    f, c, r = pattern
    return (f" <small style='color:{color};font-family:monospace'>"
            f"[flu {sym(f)} &middot; comp {sym(c)} &middot; rep {sym(r)}]</small>")


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


def imaging_interpretation(kb, rules, entry, source, settings, overlap_paths, reports_dir):
    """KB predictions from lesion location, merged across ``settings.kb_atlases``.

    Returns (DataFrame, [(atlas, rows)]); the DataFrame has target,
    target_kind, score, n_findings, citations, source_atlases, direction.
    """
    per_atlas, chunks = [], []
    for atlas in settings.kb_atlases:
        csv = overlap_csv(atlas, source, overlap_paths, reports_dir)
        if not csv.exists():
            continue
        rows = _participant_rows(pd.read_csv(csv), entry)
        if rows.empty:
            continue
        found = kb.interpret_overlap(
            rows, atlas=atlas, region_col="region", weight_col="lesion_in_roi_percent",
            min_overlap=settings.min_overlap_pct,
            min_confidence=("high" if settings.high_conf_only else None))
        if found is None or found.empty:
            per_atlas.append((atlas, 0))
            continue
        chunks.append(found.copy().assign(_atlas=atlas))
        per_atlas.append((atlas, len(found)))
    if not chunks:
        return pd.DataFrame(), per_atlas
    merged = (pd.concat(chunks, ignore_index=True)
              .groupby(["target", "target_kind"], as_index=False)
              .agg(score=("score", "sum"), n_findings=("n_findings", "sum"),
                   citations=("citations", lambda s: sorted({c for lst in s for c in lst})),
                   source_atlases=("_atlas", lambda s: sorted(set(s)))))
    merged["direction"] = merged["score"].apply(rules.evidence_direction)
    merged = merged.sort_values("score", key=lambda s: s.abs(), ascending=False).reset_index(drop=True)
    return merged, per_atlas


def damaged_regions(entry, source, settings, overlap_paths, reports_dir):
    """Display-atlas rows with lesion_in_roi_percent >= min_overlap_pct."""
    csv = overlap_csv(settings.display_atlas, source, overlap_paths, reports_dir)
    if not csv.exists():
        return pd.DataFrame()
    rows = _participant_rows(pd.read_csv(csv), entry)
    return (rows[rows["lesion_in_roi_percent"] >= settings.min_overlap_pct]
            .sort_values("lesion_in_roi_percent", ascending=False).head(settings.max_rois))


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

    ``anchor_mask`` is the participant's QC anchor (LINDA's Lesion_in_MNI),
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


def provenance_html(source, mask_path, qc, volumes, pairs, *, threshold, kb_scope, generated=None):
    """Research-use caveat, mask source and QC, method agreement, template caveat."""
    label = MASK_LABELS.get(source, source)
    if qc["ratings"]:
        rated = "; ".join(f"{escape(stage)}: <b>{escape(lbl)}</b>"
                          + (f" ({escape(str(who))}" + (f", {escape(str(when))}" if when else "") + ")" if who else "")
                          for stage, lbl, who, when in qc["ratings"])
    else:
        rated = "not rated in the QC checkpoint"
    warn = (" <b style='color:#c62828'>Rated poor — interpret this report with caution.</b>"
            if qc["poor"] else "")
    edits = f" Edits recorded on this mask: {qc['edits']}." if qc["edits"] else ""
    if pairs:
        rows = "".join(
            f"<tr><td style='padding:1px 8px'>{escape(MASK_LABELS.get(a, a))} vs {escape(MASK_LABELS.get(b, b))}</td>"
            f"<td style='padding:1px 8px;text-align:right'>{d:.2f}</td></tr>" for a, b, d in pairs)
        vols = ", ".join(f"{escape(MASK_LABELS.get(s, s))} {v:.1f} mL" for s, v in volumes.items())
        agreement = (f"Dice between available MNI masks (voxels &gt; {threshold:g}); "
                     "1 = identical; lower values mean the methods disagree on lesion extent:"
                     f"<table style='font-size:12px;margin:2px 0'>{rows}</table>Volumes: {vols}.")
    else:
        agreement = "Only one MNI mask is available, so agreement between methods was not computed."
    generated = generated or datetime.now()
    return (
        "<div class='calmar-provenance' role='note' style='border:1px solid #90a4ae;background:#eef3f6;"
        "color:#1a1a1a;padding:10px 14px;margin:12px 0;font-family:sans-serif;font-size:12px;"
        "break-inside:avoid'>"
        "<b>Research use only — not a diagnosis.</b> This report combines automated lesion "
        "segmentation with literature associations from the aphasia knowledge base. It does not "
        "diagnose aphasia, predict an individual's outcome or prescribe therapy; any clinical use "
        "requires review by a qualified clinician."
        "<ul style='margin:6px 0 0 18px;padding:0'>"
        f"<li><b>Lesion mask:</b> {escape(label)} (MNI) <code>{escape(Path(mask_path).name)}</code>. "
        f"QC: {rated}.{edits}{warn}</li>"
        f"<li><b>Method agreement:</b> {agreement}</li>"
        f"<li><b>Template space:</b> {escape(TEMPLATE_CAVEAT)}</li>"
        f"<li><b>Generated:</b> {generated:%Y-%m-%d %H:%M} · KB scope: {escape(kb_scope)}</li>"
        "</ul></div>")


# ============================================================
# HTML rendering of the KB results (unchanged presentation)
# ============================================================

def _badge(direction):
    colour = {"likely": "#28a745", "unlikely": "#dc3545"}.get(direction, "#6c757d")
    text = {"likely": "LIKELY", "unlikely": "UNLIKELY"}.get(direction, "AMBIGUOUS")
    return (f'<span style="background:{colour};color:white;'
            f'padding:1px 6px;border-radius:3px;font-size:11px">{text}</span>')


def _stars_html(rules, score):
    stars, label = rules.evidence_strength(score)
    symbols = "&#9733;" * stars if stars else "&#8212;"
    return (f"<span title='raw score = {score:+.2f}'"
            f" style='color:#f0a500;font-size:14px;letter-spacing:1px'>"
            f"{symbols}</span> <small style='color:#666'>{label}</small>")


_TABLE_HEAD = ("<table style='border-collapse:collapse;font-size:13px;width:100%'>"
               "<tr style='background:#2c3e50;color:white'>"
               "<th style='padding:4px 4px'></th>"
               "<th style='text-align:left;padding:4px 8px'>{what}</th>"
               "<th style='padding:4px 8px;text-align:left'>Evidence strength</th>"
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
        decomp = decompose_html(rules, r["target"]) if kind == "impairment" else ""
        id_note = (f" <small style='color:#aaa;font-size:10px'>({r['target']})</small>"
                   if name != r["target"] else "")
        rows.append(f"<tr><td style='padding:4px 2px'>{_badge(r['direction'])}</td>"
                    f"<td style='padding:4px 8px'><b>{name}</b>{id_note}{decomp}</td>"
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
        id_note = (f" <small style='color:#aaa;font-size:10px'>({r['target']})</small>"
                   if name != r["target"] else "")
        kind = f"<small style='color:#888;font-size:10px'>[{r.get('target_kind', '')}]</small> "
        rows.append(f"<tr><td style='padding:4px 2px'>{_badge(r['direction'])}</td>"
                    f"<td style='padding:4px 8px'>{kind}<b>{name}</b>{id_note}</td>"
                    f"<td style='padding:4px 8px'>{_stars_html(rules, r['score'])}</td>"
                    f"<td style='text-align:center;padding:4px 4px'>{r['n_findings']}</td>"
                    f"<td style='font-size:11px;color:#666;padding:4px 4px'>{', '.join(r.get('citations') or [])}</td></tr>")
    return _TABLE_HEAD.format(what="Predicted outcome") + "".join(rows) + "</table>"


_INGREDIENT_COLOURS = {"procedure": "#1a6b3a", "dose_parameter": "#7b3f00", "technology": "#1a3a6b"}


def _ingredient_badges(summary):
    if not summary:
        return "<em style='color:#aaa'>—</em>"
    badges = []
    for item in summary:
        label, cat = (item.rsplit(" (", 1) if " (" in item and item.endswith(")") else (item, ""))
        cat = cat.rstrip(")")
        badges.append(f"<span style='display:inline-block;margin:1px 2px;padding:1px 6px;"
                      f"border-radius:3px;font-size:10px;color:white;"
                      f"background:{_INGREDIENT_COLOURS.get(cat, '#555')}'>{label}</span>")
    return " ".join(badges)


def therapy_table(kb, df, stage_id, stage_label, therapy_stages):
    """Matched therapies; ⚠ when their evidence comes from another recovery stage."""
    if df is None or df.empty:
        return ("<p style='color:#666'><em>No therapy recommendations matched. "
                "Add more impairment-targeted therapy KB entries to populate this section.</em></p>")
    rows = []
    for _, r in df.iterrows():
        beh = ", ".join(kb.label_for(i) for i in (r.get("behavioral_matched") or []))
        les = ", ".join(kb.label_for(i) for i in (r.get("lesion_matched") or []))
        parts = ([f"<b>{beh}</b> <small style='color:#28a745'>(behavioural)</small>"] if beh else []) + \
                ([f"{les} <small style='color:#888'>(lesion)</small>"] if les else [])
        desc = str(r.get("short_description") or "")
        desc = (desc[:120] + "&#8230;") if len(desc) > 120 else desc
        evidence = therapy_stages.get(str(r.get("therapy_id") or r.get("id") or ""), set())
        warn = ""
        if stage_id and evidence and stage_id not in evidence:
            warn = (f" <span title='Evidence for this therapy comes from {' / '.join(sorted(evidence))} "
                    f"patients; current patient is {stage_label}.'"
                    f" style='cursor:help;color:#e65100;font-size:13px'>&#9888;</span>")
        rows.append(
            "<tr>"
            "<td style='padding:6px 8px;font-weight:bold;word-break:break-word;vertical-align:top;min-width:130px'>"
            f"  {r['therapy_name']}{warn}</td>"
            f"<td style='padding:6px 8px;font-size:12px;color:#444;vertical-align:top'>{'; '.join(parts) or '—'}</td>"
            "<td style='padding:6px 8px;font-size:11px;vertical-align:top;overflow-wrap:break-word'>"
            f"{_ingredient_badges(r.get('rtss_summary') or [])}</td>"
            f"<td style='padding:6px 8px;font-size:11px;color:#666;vertical-align:top'>{desc}</td>"
            f"<td style='padding:6px 4px;font-size:11px;color:#777;vertical-align:top'>{', '.join(r.get('citations') or [])}</td>"
            "</tr>")
    legend = ("<p style='font-size:10px;color:#777;margin:4px 0 0 0'>"
              "<span style='background:#1a6b3a;color:white;padding:1px 5px;border-radius:3px'>procedure</span>&nbsp;"
              "<span style='background:#7b3f00;color:white;padding:1px 5px;border-radius:3px'>dose parameter</span>&nbsp;"
              "<span style='background:#1a3a6b;color:white;padding:1px 5px;border-radius:3px'>technology</span></p>")
    return ("<table style='border-collapse:collapse;font-size:13px;width:100%;table-layout:fixed'>"
            "<colgroup><col style='width:22%'><col style='width:24%'>"
            "<col style='width:18%'><col style='width:25%'><col style='width:11%'></colgroup>"
            "<tr style='background:#2c3e50;color:white'>"
            "<th style='text-align:left;padding:4px 8px'>Therapy</th>"
            "<th style='text-align:left;padding:4px 8px'>Addresses impairment(s)</th>"
            "<th style='text-align:left;padding:4px 8px'>Active ingredients (RTSS)</th>"
            "<th style='text-align:left;padding:4px 8px'>Brief description</th>"
            "<th style='text-align:left;padding:4px 4px'>Citations</th></tr>"
            + "".join(rows) + "</table>" + legend)


def damaged_regions_html(df, display_atlas, atlas_dir):
    if df is None or df.empty:
        return "<p style='color:#666'><em>No damaged regions above threshold.</em></p>"
    from .anatomy_labels import label_table
    df = label_table(df, display_atlas, atlas_dir)
    rows = [f"<tr><td style='padding:3px 8px'>{escape(r['region'])}</td>"
            f"<td style='padding:3px 8px'>{escape(r['lesion_hemisphere'])}</td>"
            f"<td style='text-align:right;padding:3px 8px'>{r['lesion_in_roi_percent']:.1f}%</td>"
            f"<td style='text-align:right;font-size:11px;color:#666;padding:3px 4px'>"
            f"{int(r.get('overlap_voxels', 0)):,} vox</td></tr>" for _, r in df.iterrows()]
    return ("<table style='border-collapse:collapse;font-size:13px'>"
            "<tr style='background:#2c3e50;color:white'>"
            f"<th style='text-align:left;padding:4px 8px'>{display_atlas} region</th>"
            "<th style='padding:4px 8px'>Lesion side</th>"
            "<th style='padding:4px 8px'>% in ROI</th><th></th></tr>"
            + "".join(rows) + "</table><p>"
            "Lesion side is measured from the actual mask overlap; bilateral entries show left/right counts.</p>")


def behaviour_html(rules, row, predictors, volume_ml):
    if not row and volume_ml is None:
        return "<p style='color:#888'><em>No participants.tsv entry.</em></p>"
    row = row or {}
    wab_type = row.get("wab_type")
    items = [("WAB-AQ", row.get("wab_aq")),
             ("WAB type", (str(wab_type) + decompose_html(rules, wab_type)) if wab_type else None),
             ("Age at stroke", row.get("age_at_stroke")),
             ("Sex", row.get("sex")),
             ("Days to WAB", row.get("wab_days")),
             ("Lesion volume", f"{volume_ml:.1f} mL" if volume_ml is not None else "&#8212;")]
    rows = "".join(f"<tr><td style='padding:2px 8px'><b>{k}</b></td>"
                   f"<td style='padding:2px 8px'>{v or '&#8212;'}</td></tr>" for k, v in items)
    used = (f"<div style='font-size:11px;color:#888;margin-top:6px'>"
            f"Mapped to KB predictors: {', '.join(predictors.keys()) or '&#8212;'}</div>") if predictors else ""
    return "<table style='border-collapse:collapse;font-size:13px'>" + rows + "</table>" + used


STAGE_COLOURS = {"acute": ("#d32f2f", "#ffebee"), "subacute": ("#e65100", "#fff3e0"),
                 "chronic": ("#1565c0", "#e3f2fd"), None: ("#555555", "#f5f5f5")}


def stage_badge(stage_id, label):
    fg, bg = STAGE_COLOURS.get(stage_id, STAGE_COLOURS[None])
    return (f"<span style='background:{bg};color:{fg};border:1px solid {fg};"
            f"padding:1px 8px;border-radius:3px;font-size:11px;font-weight:bold'>{label}</span>")


LEGEND_HTML = '''
      <hr style="margin-top:18px">
      <div style="font-size:11px;color:#666;line-height:1.6">
        <b>Legend.</b><br>
        <b>Evidence strength</b>: &#9733; weak &middot; &#9733;&#9733; moderate &middot;
        &#9733;&#9733;&#9733; strong &middot; &#9733;&#9733;&#9733;&#9733; very strong.
        Hover stars for raw score (bins are a project display heuristic, not an evidence grading).<br>
        <b>Direction badge</b>: <span style="color:#28a745">LIKELY</span> /
        <span style="color:#dc3545">UNLIKELY</span> /
        <span style="color:#6c757d">AMBIGUOUS</span>.<br>
        <b>WAB decomposition</b>: flu = fluency, comp = comprehension, rep = repetition.
        <span style="color:#2e7d32">+</span> preserved,
        <span style="color:#c62828">&#8722;</span> impaired (WAB type taxonomy).<br>
        <b>Stage badge</b>:
        <span style="background:#ffebee;color:#d32f2f;border:1px solid #d32f2f;padding:0 5px;border-radius:3px;font-size:10px">Acute &lt;2 wk</span>
        <span style="background:#fff3e0;color:#e65100;border:1px solid #e65100;padding:0 5px;border-radius:3px;font-size:10px">Subacute 2 wk–6 mo</span>
        <span style="background:#e3f2fd;color:#1565c0;border:1px solid #1565c0;padding:0 5px;border-radius:3px;font-size:10px">Chronic &gt;6 mo</span> &nbsp;
        &#9888; = therapy evidence from a different recovery stage (hover for detail).
        Rules and their sources: <code>aphasia-kb/aphasia_rules.py</code>.
      </div>'''


def standalone_html(title, body):
    """Wrap report markup in a printable standalone page."""
    return f'''<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>{title}</title>
<style>
body{{font-family:Arial,sans-serif;max-width:960px;margin:40px auto;font-size:13px}}
@media print{{
  .no-print{{display:none}}
  body{{margin:10px;font-size:11px}}
  table{{page-break-inside:avoid}}
}}
</style></head><body>
<div class="no-print" style="margin-bottom:16px">
  <button onclick="window.print()" style="padding:6px 18px;background:#1565c0;color:white;border:none;border-radius:4px;cursor:pointer;font-size:13px">
    &#128438; Save / Print PDF</button>
  <span style="color:#888;font-size:11px;margin-left:10px">Use your browser's PDF option when printing</span>
</div>
{body}
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
                                dataset_dir, atlas_dir, kb_root, helpers, run_decoding=False):
    """Build, save and return the interpretation report for one participant + mask.

    ``study`` (calmar.study.Study) locates masks and derivatives. ``namespace``
    is the notebook namespace; it is used only by the Slurm helpers that still
    require one (``atlas_overlap.prepare_report_overlap`` needs ALL_ATLASES,
    CONFIG, _mask_path_for and PROJECT_DIR; ``reporting.run_reporting_task``
    needs PROJECT_DIR) and to read the OVERLAP_PATHS they publish.
    """
    from .atlas_overlap import prepare_report_overlap
    from .qc_decisions import report_qc_notice
    from .report_ui import ParticipantReport, report_sections

    messages = []
    note = messages.append
    _, rules = _kb_modules(kb_root)
    kb = load_kb(kb_root, settings)
    note(kb.summary())

    if source not in study.mni_sources(entry):
        raise ValueError(f"No existing MNI mask for {source!r}, {entry['subject']} "
                         f"{entry.get('session') or ''}. Choose an available mask in the report selector.")
    mask = Path(study.mni_mask(entry, source))
    linda_dir = Path(study.linda_dir(entry))
    brain = linda_dir / "Subject_in_MNI.nii.gz"
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
    damaged = damaged_regions(entry, source, settings, overlap_paths, reports_dir)
    note("  KB findings by atlas:")
    for atlas, n in per_atlas:
        note(f"    . {atlas:14s} {n:3d} (target,target_kind) rows")

    # 2. Clinical data -> KB predictor predictions, recovery stage
    row = participant_row(dataset_dir, entry["subject"])
    predictors = row_to_predictors(row)
    stage_id, stage_label = rules.classify_stage((row or {}).get("wab_days"))
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
        impairments += list(imaging[imaging["target_kind"] == "impairment"]["target"].head(settings.top_n * 2))
    if not predicted.empty:
        impairments += list(predicted[predicted["target_kind"] == "impairment"]["target"].head(settings.top_n))
    impairments = list(dict.fromkeys(impairments))
    wab_type = (row or {}).get("wab_type") or ""
    behavioural = kb.wab_to_impairments(wab_type)
    note(f"  WAB type: {wab_type!r} -> behavioral impairments: {behavioural}")
    therapies = kb.interpret_therapies(impairments, behavioral_impairment_ids=behavioural,
                                       max_results=settings.top_n)

    # 4. HTML
    n_imaging = int((imaging["target_kind"] == "impairment").sum()) if not imaging.empty else 0
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
    <div style="border:1px solid #ddd;border-radius:6px;padding:16px 16px 10px;
                background:#fafafa;font-family:sans-serif;color:#1a1a1a">
      <h3 style="margin-top:0;margin-bottom:4px">Clinical interpretation &mdash;
        {entry['subject']} {entry.get('session') or ''}
        &nbsp; {stage_badge(stage_id, stage_label)}
        <small style="font-weight:normal;color:#888;font-size:12px">&nbsp; {days_text}</small>
      </h3>
      <div style="font-size:11px;color:#888">
        Lesion mask: <b style="color:#c62828">{label}</b> &middot; research use only, not a diagnosis
        <br>
        KB scope: {', '.join(settings.include)} &middot; {conf_note} &middot;
        atlas (lookup): {', '.join(settings.kb_atlases)} &middot;
        atlas (display): {settings.display_atlas}
      </div>
    </div>
    '''
    body = f'''
    <div style="border:1px solid #ddd;border-radius:6px;padding:16px;
                background:#fafafa;font-family:sans-serif;color:#1a1a1a">

      <h4 style="margin-top:0">Damaged regions ({settings.display_atlas},
        &ge;{settings.min_overlap_pct}%)</h4>
      {damaged_regions_html(damaged, settings.display_atlas, atlas_dir)}

      <h4 style="margin-top:18px">Behavioural / clinical data</h4>
      {behaviour_html(rules, row, predictors, volume)}

      <h4 style="margin-top:18px">Predictor-driven outcome predictions
        ({n_pred} total findings)</h4>
      <p style="font-size:12px;color:#555;margin:4px 0 8px 0">
        Based on WAB-AQ, age, lesion volume, and other clinical scalars.
        Findings are weighted by the severity of the patient&rsquo;s values.
      </p>
      {interp_table_all(kb, rules, predicted, settings.top_n)}

      <h4 style="margin-top:18px">Predicted impairments from lesion location
        ({n_imaging} total findings)</h4>
      <p style="font-size:12px;color:#555;margin:4px 0 8px 0">
        Based on which brain regions are damaged and what language functions
        those regions support (lesion-symptom mapping studies).
      </p>
      {interp_table(kb, rules, imaging, 'impairment', settings.top_n)}

      <h4 style="margin-top:18px">Therapy recommendations ({n_therapy} matched)</h4>
      <p style="font-size:12px;color:#555;margin:4px 0 8px 0">
        Therapies with evidence targeting the predicted impairments above.
      </p>
      {therapy_table(kb, therapies, stage_id, stage_label, therapy_stages)}
{LEGEND_HTML}
    </div>
    '''

    # 5. Provenance, QC notice, overlay; save
    masks = {s: study.mni_mask(entry, s) for s in study.mni_sources(entry)}
    try:
        volumes, pairs = mask_agreement(masks, settings.threshold)
    except Exception as exc:
        volumes, pairs = {}, []
        note(f"  mask agreement not computed: {exc}")
    qc = mask_qc_summary(study.lesion_mni(entry), mask, source)
    provenance = provenance_html(source, mask, qc, volumes, pairs,
                                 threshold=settings.threshold, kb_scope=kb_scope)
    qc_notice = report_qc_notice(linda_dir, entry)
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
