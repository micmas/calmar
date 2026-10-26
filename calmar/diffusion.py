"""Eligibility and report helpers for optional directional diffusion MRI.

CALMaR uses the word DWI in two different senses that must not be conflated:

* a three-dimensional trace-DWI plus ADC image can be used by OpenADS to
  segment an acute infarct;
* a four-dimensional diffusion acquisition with valid b-values and b-vectors
  can support tensor fitting and, with stronger assumptions, tractography.

This module performs metadata/sidecar checks only.  It deliberately does not
load the (often DataLad-annexed) NIfTI payload during participant discovery.
"""

from __future__ import annotations

from collections import defaultdict
from html import escape
import json
import math
from pathlib import Path

import pandas as pd

from .study import dataset_for_entry


MIN_TENSOR_DIRECTIONS = 6
MIN_REPORT_DIRECTIONS = 30
DMRI_SUBDIR = "derivatives/calmar-dmri"


def _numbers(path):
    """Read whitespace-separated floating-point values from a sidecar."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(path)
    return [float(value) for value in path.read_text(encoding="utf-8").split()]


def _bvecs(path, n):
    """Return b-vectors as ``n x 3`` rows, accepting both common layouts."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(path)
    rows = [[float(value) for value in line.split()]
            for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(rows) == 3 and all(len(row) == n for row in rows):
        return list(zip(*rows))
    if len(rows) == n and all(len(row) == 3 for row in rows):
        return rows
    raise ValueError(f"expected 3 x {n} or {n} x 3 values, found {[len(row) for row in rows]}")


def _metadata(path):
    path = Path(path)
    if not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def _shells(values, b0_threshold=100):
    """Readable shell centres; rounding avoids pretending scanner b-values are exact."""
    return sorted({0 if value < b0_threshold else int(round(value / 50.0) * 50)
                   for value in values})


def _unique_directions(bvals, vectors, b0_threshold=100, angular_tolerance_degrees=3.0):
    """Count antipodally equivalent gradient directions within each shell."""
    unique = defaultdict(list)
    threshold = math.cos(math.radians(angular_tolerance_degrees))
    for value, vector in zip(bvals, vectors):
        if value < b0_threshold:
            continue
        norm = math.sqrt(sum(component * component for component in vector))
        if norm == 0:
            continue
        direction = tuple(component / norm for component in vector)
        shell = int(round(value / 50.0) * 50)
        if not any(abs(sum(a * b for a, b in zip(direction, prior))) >= threshold
                   for prior in unique[shell]):
            unique[shell].append(direction)
    return sum(map(len, unique.values()))


def assess_dwi_series(item, *, min_report_directions=MIN_REPORT_DIRECTIONS,
                      b0_threshold=100):
    """Classify one discovered DWI series without reading its NIfTI payload.

    ``tensor_eligible`` is the mathematical minimum-sidecar check.  The more
    conservative ``report_eligible`` flag additionally requires at least 30
    diffusion-weighted volumes, so weak six-direction fits are not silently
    promoted into participant tract reports.
    """
    result = dict(item)
    result.update(tensor_eligible=False, report_eligible=False, b0_reference=False, n_volumes=None,
                  n_b0=0, n_dw_volumes=0, n_directions=0, shells=[], reasons=[], warnings=[])
    missing = [kind for kind in ("bval", "bvec", "json") if not item.get(kind)]
    if missing:
        result["reasons"].append("missing " + ", ".join(missing) + " sidecar" + ("s" if len(missing) > 1 else ""))
        return result
    try:
        bvals = _numbers(item["bval"])
        vectors = _bvecs(item["bvec"], len(bvals))
        metadata = _metadata(item["json"])
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        result["reasons"].append(f"unreadable gradient metadata: {exc}")
        return result
    n_b0 = sum(value < b0_threshold for value in bvals)
    nonzero = [i for i, value in enumerate(bvals) if value >= b0_threshold]
    invalid = []
    for i in nonzero:
        norm2 = sum(component * component for component in vectors[i])
        if not 0.25 <= norm2 <= 2.25:
            invalid.append(i)
    unique_directions = _unique_directions(bvals, vectors, b0_threshold)
    result.update(n_volumes=len(bvals), n_b0=n_b0, n_dw_volumes=len(nonzero),
                  n_directions=unique_directions,
                  shells=_shells(bvals, b0_threshold),
                  phase_encoding_direction=metadata.get("PhaseEncodingDirection"),
                  total_readout_time=metadata.get("TotalReadoutTime"))
    result["b0_reference"] = bool(n_b0 and metadata.get("PhaseEncodingDirection"))
    if not bvals:
        result["reasons"].append("empty b-value file")
    if n_b0 == 0:
        result["reasons"].append("no b=0 volume")
    if unique_directions < MIN_TENSOR_DIRECTIONS:
        result["reasons"].append(f"only {unique_directions} distinct diffusion directions")
    if invalid:
        result["reasons"].append(f"{len(invalid)} non-unit diffusion gradient vectors")
    if result["reasons"]:
        return result
    result["tensor_eligible"] = True
    if unique_directions < min_report_directions:
        result["warnings"].append(
            f"only {unique_directions} distinct diffusion directions; CALMaR requires "
            f"{min_report_directions} for reporting")
        return result
    result["report_eligible"] = True
    if not metadata.get("PhaseEncodingDirection"):
        result["warnings"].append("PhaseEncodingDirection is missing")
    if metadata.get("TotalReadoutTime") is None:
        result["warnings"].append("TotalReadoutTime is missing")
    return result


def _opposite_phase(a, b):
    return bool(a and b and a.rstrip("-") == b.rstrip("-") and a.endswith("-") != b.endswith("-"))


def assess_dwi_sessions(entry, *, min_report_directions=MIN_REPORT_DIRECTIONS):
    """Group a participant's series by session and rank report-ready options."""
    grouped = defaultdict(list)
    for item in entry.get("dwi_inventory", ()):
        grouped[item.get("session")].append(
            assess_dwi_series(item, min_report_directions=min_report_directions))
    sessions = []
    for session, series in grouped.items():
        eligible = [item for item in series if item["report_eligible"]]
        if not eligible:
            continue
        eligible.sort(key=lambda item: (-item["n_directions"], str(item.get("dwi") or "")))
        primary = eligible[0]
        reverse_candidates = [item for item in series if item is not primary and item["b0_reference"]
                              and _opposite_phase(primary.get("phase_encoding_direction"),
                                                  item.get("phase_encoding_direction"))]
        reverse_candidates.sort(key=lambda item: (-item["n_b0"], -item["n_directions"],
                                                   str(item.get("dwi") or "")))
        reverse = reverse_candidates[0] if reverse_candidates else None
        preprocessing_series = list(eligible)
        if reverse is not None and reverse not in preprocessing_series:
            preprocessing_series.append(reverse)
        warnings = list(dict.fromkeys(warning for item in preprocessing_series for warning in item["warnings"]))
        if reverse is None:
            warnings.append("no opposite phase-encoding DWI; susceptibility correction is limited")
        sessions.append({
            "subject": entry["subject"], "session": session,
            "same_session": session == entry.get("session"), "series": preprocessing_series,
            "primary": primary, "reverse": reverse,
            "n_directions": primary["n_directions"], "shells": primary["shells"],
            "has_reverse_phase": reverse is not None, "warnings": warnings,
        })
    return sorted(sessions, key=lambda item: (
        not item["same_session"], not item["has_reverse_phase"], -item["n_directions"], item["session"] or ""))


def direct_diffusion_dir(dataset, config, entry):
    """Standard location of normalized direct-dMRI outputs for a report entry."""
    selected = entry.get("dmri_analysis") or entry
    root = dataset_for_entry(dataset, selected)
    subject = selected["subject"]
    session = selected.get("session")
    return Path(root) / config.get("DMRI_SUBDIR", DMRI_SUBDIR) / subject / (session or "") / "dwi"


def tractometry_paths(dataset, config, entry):
    selected = entry.get("dmri_analysis") or entry
    stem = "_".join(filter(None, [selected["subject"], selected.get("session")]))
    folder = direct_diffusion_dir(dataset, config, entry) / "metrics"
    table = folder / f"{stem}_desc-direct_tractometry.tsv"
    return table, table.with_suffix(".json")


TRACTOMETRY_COLUMNS = {
    "tract", "hemisphere", "lesion_overlap_pct", "fa_median", "md_median_mm2_s", "valid_voxel_pct"
}


def load_tractometry(path):
    """Load CALMaR's normalized tractometry contract and reject ambiguous rows."""
    path = Path(path)
    table = pd.read_csv(path, sep="\t")
    missing = TRACTOMETRY_COLUMNS - set(table.columns)
    if missing:
        raise ValueError(f"tractometry table lacks: {', '.join(sorted(missing))}")
    if table.empty:
        raise ValueError("tractometry table is empty")
    numeric = sorted(TRACTOMETRY_COLUMNS - {"tract", "hemisphere"})
    for column in numeric:
        table[column] = pd.to_numeric(table[column], errors="raise")
    for column in ("lesion_overlap_pct", "valid_voxel_pct"):
        measured = table[column].dropna()
        if not measured.between(0, 100).all():
            raise ValueError(f"{column} must be between 0 and 100")
    if not table["fa_median"].dropna().between(0, 1).all():
        raise ValueError("fa_median must be between 0 and 1")
    md = table["md_median_mm2_s"].dropna()
    if not md.between(0, 0.01).all():
        raise ValueError("md_median_mm2_s must be in physical mm²/s units (0 to 0.01)")
    return table


def direct_diffusion_section(dataset, config, entry):
    """Render direct participant dMRI separately from normative disconnectomes.

    Returns ``None`` when direct dMRI was neither selected nor produced, so
    legacy reports remain unchanged.
    """
    table_path, metadata_path = tractometry_paths(dataset, config, entry)
    selected = bool(entry.get("dmri_analysis"))
    if not selected:
        return None
    if not table_path.is_file():
        return ("<p class='section-intro'>Directional diffusion MRI was selected for this participant, but no "
                "validated tractometry table is available yet. The normative BCB/DeepDisco section remains "
                "separate and is not replaced by a missing direct measurement.</p>")
    table = load_tractometry(table_path).sort_values(
        ["lesion_overlap_pct", "tract"], ascending=[False, True], kind="stable", na_position="last")
    metadata = {}
    if metadata_path.is_file():
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            metadata = {"warnings": ["the tractometry metadata sidecar could not be read"]}
    rows = []
    for _, row in table.iterrows():
        def measured(value, pattern):
            return pattern.format(value) if pd.notna(value) else "not calculated"
        rows.append(
            "<tr>" +
            f"<td>{escape(str(row['tract']))}</td><td>{escape(str(row['hemisphere']))}</td>" +
            f"<td>{measured(row['lesion_overlap_pct'], '{:.1f}%')}</td>" +
            f"<td>{measured(row['fa_median'], '{:.3f}')}</td>" +
            f"<td>{measured(row['md_median_mm2_s'], '{:.6g}')}</td>" +
            f"<td>{measured(row['valid_voxel_pct'], '{:.1f}%')}</td></tr>")
    warnings = list(metadata.get("warnings") or [])
    qc = metadata.get("qc_status")
    if qc and qc != "passed":
        warnings.insert(0, f"diffusion QC status: {str(qc).replace('_', ' ')}; values are provisional")
    warning_html = ("<p class='method-note'><strong>Review flags:</strong> " +
                    escape("; ".join(map(str, warnings))) + ".</p>") if warnings else ""
    acquisition = []
    if metadata.get("n_directions") is not None:
        acquisition.append(f"{metadata['n_directions']} diffusion-weighted volumes")
    if metadata.get("shells"):
        acquisition.append("shells " + "/".join(map(str, metadata["shells"])))
    if metadata.get("preprocessor"):
        acquisition.append(str(metadata["preprocessor"]))
    if metadata.get("session"):
        acquisition.append(f"diffusion session {metadata['session']}")
    if metadata.get("anatomical_session"):
        acquisition.append(f"lesion/anatomy session {metadata['anatomical_session']}")
    acquisition_text = escape(" · ".join(acquisition))
    return (
        "<p class='section-intro'>These are measurements from this participant&rsquo;s own directional diffusion "
        "acquisition. They complement, but do not validate or numerically combine with, the BCB/DeepDisco "
        "disconnectome predictions.</p>"
        "<p class='method-note'>FA and MD summarize diffusion within the successfully mapped portion of each "
        "tract; lesion overlap is reported separately when it can be mapped onto the same grid. In stroke, oedema, cavitation, crossing fibres, distortion "
        "and tracking failure can all change these values or prevent reconstruction. A low streamline count or "
        "missing tract must therefore not be read as proof of anatomical disconnection."
        + (f" Acquisition: {acquisition_text}." if acquisition_text else "") + "</p>" + warning_html +
        "<div class='table-wrap'><table><thead><tr><th>Tract</th><th>Side</th><th>Lesion overlap</th>"
        "<th>Median FA</th><th>Median MD (mm²/s)</th><th>Valid tract voxels</th></tr></thead><tbody>" +
        "".join(rows) + "</tbody></table></div>")
