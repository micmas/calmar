"""Eligibility, output contracts and reporting for optional brain-health MRI.

The analysis deliberately separates two measurements:

* T1w SynthSeg volumetry provides atrophy-sensitive *descriptive* markers.
  A single scan without age-adjusted norms cannot diagnose atrophy, and a
  chronic stroke cavity can lower apparent tissue fraction.
* FLAIR DeepWMH segmentation provides a white-matter-hyperintensity candidate
  burden.  Stroke-lesion signal is excluded after registration, but the
  remaining signal is still not assigned a vascular aetiology automatically.
"""

from __future__ import annotations

from html import escape
import json
from pathlib import Path

from .study import config_for_entry, dataset_for_entry, modality


BRAIN_HEALTH_SUBDIR = "derivatives/calmar-brain-health"

# Stable report-facing measurements.  Every selected measurement is emitted,
# including an explicit missing value, so absence is never mistaken for zero.
BRAIN_HEALTH_REPORT_MEASURES = {
    "atrophy": (
        ("intracranial_volume_ml", "Intracranial segmented volume", "mL", "anatomy"),
        ("brain_tissue_volume_ml", "Brain tissue volume", "mL", "anatomy"),
        ("brain_parenchymal_fraction", "Brain parenchymal fraction", "fraction", "anatomy"),
        ("lesion_cavity_ml", "Stroke cavity used for adjustment", "mL", "anatomy"),
        ("lesion_adjusted_brain_parenchymal_fraction",
         "Stroke-cavity-adjusted brain parenchymal fraction", "fraction", "anatomy_adjusted"),
        ("lateral_ventricle_fraction", "Lateral-ventricle fraction (raw)", "fraction", "anatomy"),
        ("lesion_masked_lateral_ventricle_fraction",
         "Lateral-ventricle fraction outside lesion", "fraction", "anatomy_adjusted"),
        ("lesion_ventricle_overlap_ml", "Lesion overlap with ventricle labels", "mL", "anatomy_adjusted"),
        ("left_lateral_ventricle_ml", "Left lateral-ventricle volume", "mL", "anatomy"),
        ("right_lateral_ventricle_ml", "Right lateral-ventricle volume", "mL", "anatomy"),
    ),
    "wmh": (
        ("total_flair_hyperintensity_ml", "Total segmented FLAIR hyperintensity", "mL", "wmh_raw"),
        ("wmh_candidate_ml", "Non-stroke WMH candidate burden", "mL", "wmh_adjusted"),
        ("stroke_excluded_hyperintensity_ml", "Hyperintensity removed in stroke exclusion zone", "mL",
         "wmh_adjusted"),
        ("wmh_fraction_icv", "WMH candidate / intracranial volume", "fraction", "wmh_adjusted"),
    ),
}


def _same_session_flairs(entry):
    """Return same-session BIDS FLAIR paths, without fetching payloads."""
    value = entry.get("t1w") or entry.get("dwi")
    if not value:
        return []
    native = Path(value)
    anat = native.parent if native.parent.name == "anat" else native.parent.parent / "anat"
    matches = sorted(anat.glob("*_FLAIR.nii.gz")) + sorted(anat.glob("*_FLAIR.nii"))
    return matches


def brain_health_inventory(config, dataset, entry):
    """Describe same-session inputs available for one participant.

    T1 volumetry is restricted to genuine T1-route entries.  Although
    SynthSeg can accept other contrasts, low-resolution acute FLAIR is not
    promoted into an atrophy estimate here.
    """
    effective = config_for_entry(config, entry)
    route = modality(effective)
    t1w = Path(entry["t1w"]) if route == "t1" and entry.get("t1w") else None
    flairs = _same_session_flairs(entry)
    flair = flairs[0] if flairs else None
    return {
        "subject": entry["subject"], "session": entry.get("session"),
        "dataset": str(dataset_for_entry(dataset, entry)),
        "t1w": str(t1w) if t1w is not None else None,
        "flair": str(flair) if flair is not None else None,
        "flair_candidates": [str(path) for path in flairs],
        "atrophy_available": t1w is not None,
        "wmh_available": flair is not None,
        "route": route,
    }


def output_root(dataset, config, entry):
    subject, session = entry["subject"], entry.get("session")
    return (Path(dataset) / config.get("BRAIN_HEALTH_SUBDIR", BRAIN_HEALTH_SUBDIR) /
            subject / (session or "") / "anat")


def output_paths(dataset, config, entry):
    root = output_root(dataset, config, entry)
    source = str(config.get("BRAIN_HEALTH_MASK_SOURCE", "manual"))
    mode = str(config.get("BRAIN_HEALTH_SYNTHSEG_MODE", "robust"))
    margin = float(config.get("BRAIN_HEALTH_LESION_EXCLUSION_MM", 3.0))
    margin_label = f"{margin:g}".replace(".", "p")
    components = (entry.get("brain_health_components") or
                  (entry.get("brain_health_analysis") or {}).get("components") or ())
    component_label = "-".join(sorted(components)) or "none"
    metric_dir = root / f"metrics_{component_label}_source-{source}_margin-{margin_label}mm"
    return {
        "anatomy": root / f"synthseg_mode-{mode}_source-{source}",
        "wmh": root / "deepwmh",
        "metrics": metric_dir,
        "metrics_json": metric_dir / "brain_health.json",
        "metrics_tsv": metric_dir / "brain_health.tsv",
        "qc_png": metric_dir / "brain_health_qc.png",
    }


def load_metrics(path):
    """Load and minimally validate the stable report contract."""
    path = Path(path)
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not isinstance(value.get("measurements"), dict):
        raise ValueError(f"Invalid brain-health metrics: {path}")
    measurements = value["measurements"]
    bounds = {
        "brain_parenchymal_fraction": (0.0, 1.0),
        "lesion_adjusted_brain_parenchymal_fraction": (0.0, 1.0),
        "lateral_ventricle_fraction": (0.0, 1.0),
        "wmh_candidate_ml": (0.0, None),
        "total_flair_hyperintensity_ml": (0.0, None),
    }
    for key, (lower, upper) in bounds.items():
        number = measurements.get(key)
        if number is None:
            continue
        number = float(number)
        if number < lower or (upper is not None and number > upper):
            raise ValueError(f"Implausible {key}={number} in {path}")
    return value


def _method_text(result, kind):
    methods = result.get("methods") or {}
    if kind.startswith("anatomy"):
        method = methods.get("anatomy") or {}
        text = method.get("tool") or "SynthSeg"
        version = method.get("version")
        text += f" {version}" if version else " (version not recorded)"
        mode = result.get("synthseg_mode")
        if mode:
            text += f", {mode} mode"
        if kind == "anatomy_adjusted":
            text += "; CALMaR lesion-mask adjustment"
        return text
    method = methods.get("wmh") or {}
    text = method.get("tool") or "DeepWMH"
    version = method.get("version")
    text += f" {version}" if version else " (version not recorded)"
    if kind == "wmh_adjusted":
        registration = methods.get("lesion_to_flair_registration") or {}
        reg_tool = registration.get("tool") or "ANTs"
        reg_version = registration.get("version")
        text += f"; stroke exclusion registered with {reg_tool}"
        text += f" {reg_version}" if reg_version else " (version not recorded)"
    return text


def brain_health_measure_records(dataset, config, entry):
    """Return report measure records for the explicitly selected components.

    The records are deliberately complete: selected measurements whose output
    or value is unavailable are returned with ``value=None`` and missing
    method/QC metadata rather than being omitted or inferred.
    """
    selected = entry.get("brain_health_analysis")
    if not selected:
        return []
    components = tuple(selected.get("components") or ())
    path = output_paths(dataset, config, entry)["metrics_json"]
    result, error = {}, None
    if path.is_file():
        try:
            result = load_metrics(path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            error = f"metrics could not be validated: {exc}"
    else:
        error = "validated metrics file is missing"
    measurements = result.get("measurements") or {}
    qc_status = result.get("qc_status") or "missing"
    records = []
    for component in components:
        for key, label, units, method_kind in BRAIN_HEALTH_REPORT_MEASURES.get(component, ()):
            value = measurements.get(key)
            records.append({
                "id": key, "kb_id": key, "label": label, "value": value,
                "units": units,
                "method": _method_text(result, method_kind) if result else "missing",
                "qc_status": qc_status,
                "missing_reason": error if value is None else None,
                "brain_health": True,
            })
    return records


def brain_health_measure_note(dataset, config, entry, *, stroke_phase=None):
    """Plain-language interpretation boundary shown above brain-health cards."""
    selected = entry.get("brain_health_analysis")
    if not selected:
        return ""
    path = output_paths(dataset, config, entry)["metrics_json"]
    result = {}
    if path.is_file():
        try:
            result = load_metrics(path)
        except (OSError, ValueError, json.JSONDecodeError):
            pass
    warnings = list(result.get("warnings") or ())
    phase = stroke_phase or result.get("stroke_phase")
    components = set(selected.get("components") or ())
    if "wmh" in components and phase in {"acute", "subacute"}:
        warnings.append(f"{phase} FLAIR: infarct-related oedema may extend beyond the exclusion zone")
    elif "wmh" in components and phase == "chronic":
        warnings.append("chronic FLAIR: perilesional gliosis can extend beyond the exclusion zone")
    warning_html = ("<br><b>Review flags:</b> " + escape("; ".join(dict.fromkeys(map(str, warnings)))) + "."
                    if warnings else "")
    return (
        "<p class='method-note'><b>Brain-health interpretation boundary:</b> A single scan without an age- and "
        "acquisition-matched reference cannot establish atrophy. Stroke cavities can mimic tissue loss; the "
        "lesion adjustment is not a reconstruction of pre-stroke anatomy. FLAIR hyperintensity outside the "
        "stroke-exclusion zone is a WMH candidate, not an automatic diagnosis of small-vessel disease, and no "
        "Fazekas grade is inferred." + warning_html + "</p>")


def _number(value, digits=1, suffix=""):
    if value is None:
        return "not calculated"
    return f"{float(value):.{digits}f}{suffix}"


def brain_health_section(dataset, config, entry, *, stroke_phase=None):
    """Render selected brain-health measurements for the participant report."""
    selected = entry.get("brain_health_analysis")
    if not selected:
        return None
    path = output_paths(dataset, config, entry)["metrics_json"]
    if not path.is_file():
        components = ", ".join(selected.get("components") or ()) or "brain health"
        return ("<p class='section-intro'>Brain-health analysis was selected " +
                f"({escape(components)}), but no validated metrics are available yet.</p>")
    try:
        result = load_metrics(path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return ("<p class='section-intro'>Brain-health outputs exist, but their metrics could not be "
                f"validated: {escape(str(exc))}.</p>")
    m = result["measurements"]
    expected = {
        "components": sorted(selected.get("components") or ()),
        "lesion_mask_source": config.get("BRAIN_HEALTH_MASK_SOURCE", "manual"),
        "lesion_exclusion_mm": (float(config.get("BRAIN_HEALTH_LESION_EXCLUSION_MM", 3.0))
                                if "wmh" in (selected.get("components") or ()) else None),
    }
    if "atrophy" in (selected.get("components") or ()):
        expected["synthseg_mode"] = config.get("BRAIN_HEALTH_SYNTHSEG_MODE", "robust")
    stale = []
    for key, value in expected.items():
        actual = sorted(result.get(key) or ()) if key == "components" else result.get(key)
        if actual != value:
            stale.append(f"{key} is {actual!r}, current selection is {value!r}")
    rows = []
    if result.get("anatomy"):
        rows.extend([
            ("Intracranial segmented volume", _number(m.get("intracranial_volume_ml"), 1, " mL")),
            ("Brain parenchymal fraction", _number(m.get("brain_parenchymal_fraction"), 3)),
            ("Stroke-cavity-adjusted parenchymal fraction", _number(
                m.get("lesion_adjusted_brain_parenchymal_fraction"), 3)),
            ("Lateral-ventricle fraction (raw)", _number(m.get("lateral_ventricle_fraction"), 4)),
            ("Lateral-ventricle fraction outside lesion", _number(
                m.get("lesion_masked_lateral_ventricle_fraction"), 4)),
            ("Lesion overlap with ventricle labels", _number(
                m.get("lesion_ventricle_overlap_ml"), 1, " mL")),
            ("Left / right lateral ventricle", " / ".join([
                _number(m.get("left_lateral_ventricle_ml"), 1, " mL"),
                _number(m.get("right_lateral_ventricle_ml"), 1, " mL")]))])
    if result.get("wmh"):
        rows.extend([
            ("Total segmented FLAIR hyperintensity", _number(
                m.get("total_flair_hyperintensity_ml"), 1, " mL")),
            ("Non-stroke WMH candidate burden", _number(m.get("wmh_candidate_ml"), 1, " mL")),
            ("Removed within stroke exclusion zone", _number(
                m.get("stroke_excluded_hyperintensity_ml"), 1, " mL")),
            ("WMH candidate / intracranial volume", _number(m.get("wmh_fraction_icv"), 5)),
        ])
    table = "".join(f"<tr><td>{escape(label)}</td><td>{escape(value)}</td></tr>" for label, value in rows)
    warnings = list(result.get("warnings") or ())
    warnings.extend("stale brain-health result: " + item for item in stale)
    effective_phase = stroke_phase or result.get("stroke_phase")
    if effective_phase in {"acute", "subacute"}:
        warnings.append(f"{effective_phase} FLAIR: infarct-related oedema may extend beyond the exclusion zone")
    elif effective_phase == "chronic" and result.get("wmh"):
        warnings.append("chronic FLAIR: perilesional gliosis can extend beyond the exclusion zone")
    if result.get("qc_status") != "passed":
        warnings.insert(0, "visual QC has not been marked as passed; values are provisional")
    warning_html = ("<p class='method-note'><strong>Review flags:</strong> " +
                    escape("; ".join(dict.fromkeys(map(str, warnings)))) + ".</p>") if warnings else ""
    phases = []
    if effective_phase:
        phases.append(f"stroke phase: {effective_phase}")
    if result.get("flair"):
        phases.append(f"FLAIR: {Path(result['flair']).name}")
    context = escape(" · ".join(phases))
    return (
        "<p class='section-intro'>These measurements describe background structural brain health separately "
        "from the focal stroke lesion. They are imaging features for interpretation, not diagnostic labels.</p>"
        "<p class='method-note'>A single scan without an age- and acquisition-matched reference cannot establish "
        "atrophy. Stroke cavities can mimic tissue loss, so both raw and lesion-adjusted parenchymal fractions are "
        "shown; the adjustment is not a reconstruction of pre-stroke anatomy. FLAIR hyperintensity outside the "
        "registered stroke-exclusion zone is labelled a WMH candidate: it "
        "is not automatically small-vessel disease, and acute oedema or other pathology may remain. No automated "
        "Fazekas grade is inferred." + (f" {context}." if context else "") + "</p>" + warning_html +
        "<div class='table-wrap'><table><thead><tr><th>Brain-health feature</th><th>Value</th></tr></thead>"
        f"<tbody>{table}</tbody></table></div>")
