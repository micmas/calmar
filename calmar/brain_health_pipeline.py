"""Slurm-only processing for optional atrophy and WMH candidate features."""

from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time

import nibabel as nib
from nibabel.processing import resample_from_to
import numpy as np
from scipy.ndimage import distance_transform_edt

from .brain_health import output_paths
from .dmri_pipeline import _materialize, _publish
from .study import Study, modality


CSF_LABELS = {4, 5, 14, 15, 24, 43, 44, 72}
LATERAL_VENTRICLE_LABELS = {4, 5, 43, 44}
LEFT_LATERAL_VENTRICLE_LABELS = {4, 5}
RIGHT_LATERAL_VENTRICLE_LABELS = {43, 44}


def _require_slurm():
    if not os.environ.get("SLURM_JOB_ID"):
        raise RuntimeError("Brain-health processing must run through its retained Slurm scripts.")


def _entry(request):
    entries = request.get("entries") or []
    if len(entries) != 1:
        raise ValueError("A brain-health job requires exactly one participant entry.")
    return entries[0]


def _components(entry):
    return set(entry.get("brain_health_components") or ())


def _run(command, log):
    with Path(log).open("w", encoding="utf-8") as stream:
        subprocess.run([str(item) for item in command], stdout=stream, stderr=subprocess.STDOUT,
                       text=True, check=True)


def _save_like(data, image, path, dtype=np.uint8):
    header = image.header.copy()
    header.set_data_dtype(dtype)
    nib.save(nib.Nifti1Image(np.asarray(data, dtype=dtype), image.affine, header), str(path))


def _wmh_measurements(raw, exclusion, voxel_ml, intracranial_volume_ml=None):
    """Volume contract; without a stroke exclusion only the raw total is valid."""
    values = {"total_flair_hyperintensity_ml": float(np.asarray(raw, bool).sum() * voxel_ml)}
    if exclusion is None:
        values.update(wmh_candidate_ml=None, stroke_excluded_hyperintensity_ml=None,
                      wmh_fraction_icv=None)
        return values
    raw, exclusion = np.asarray(raw, bool), np.asarray(exclusion, bool)
    candidate = raw & ~exclusion
    values.update(
        wmh_candidate_ml=float(candidate.sum() * voxel_ml),
        stroke_excluded_hyperintensity_ml=float((raw & exclusion).sum() * voxel_ml),
        wmh_fraction_icv=(float(candidate.sum() * voxel_ml) / intracranial_volume_ml
                          if intracranial_volume_ml else None),
    )
    return values


def _same_grid(left, right):
    return left.shape[:3] == right.shape[:3] and np.allclose(left.affine, right.affine, atol=1e-3)


def _native_lesion(request, entry):
    config = request["config"]
    source = config.get("BRAIN_HEALTH_MASK_SOURCE", "manual")
    allowed = {"manual", "linda", "synthstroke", "openads"}
    if source not in allowed:
        raise ValueError(f"BRAIN_HEALTH_MASK_SOURCE must be one of {sorted(allowed)}, not {source!r}")
    study = Study(config, request["dataset"], config.get("PROJECT_DIR", "."))
    mask = (study.masks(entry).get(source) or {}).get("T1w")
    route = modality(config)
    if source == "openads":
        dwi_entry = entry.get("dwi_analysis") or entry
        reference = dwi_entry.get("dwi") or (dwi_entry.get("t1w") if route == "dwi" else None)
        if dwi_entry.get("session") != entry.get("session"):
            raise ValueError("OpenADS lesion and brain-health FLAIR must come from the same session.")
    else:
        reference = entry.get("dwi") if route == "dwi" else (entry.get("anatomical_t1w") or entry.get("t1w"))
    if mask is None:
        return None, source, Path(reference) if reference else None
    return Path(mask), source, Path(reference) if reference else None


def _validate_mask(path, reference, *, allow_empty=False):
    image, ref = nib.load(str(path)), nib.load(str(reference))
    if not _same_grid(image, ref):
        raise RuntimeError(f"Output grid does not match its source image: {path}")
    data = np.asarray(image.dataobj)
    if not np.isfinite(data).all():
        raise RuntimeError(f"Non-finite mask: {path}")
    if not allow_empty and not np.any(data > 0):
        raise RuntimeError(f"Empty mask: {path}")
    return image, data


def _publish_summary(output, stage, request, entry, final, started, files, qc):
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=output.name + ".attempt.", dir=output.parent) as folder:
        result = Path(folder) / "result"
        result.mkdir()
        listed = [{"path": str(final), "status": "computed",
                   "images": {Path(path).name: Path(path).name for path in files
                              if str(path).lower().endswith((".png", ".gif"))}}]
        listed.extend({"path": str(path), "status": "computed"} for path in files)
        summary = {
            "stage": stage, "request": request, "job": os.environ["SLURM_JOB_ID"],
            "results": [{"subject": entry["subject"], "session": entry.get("session"),
                         "seconds": time.monotonic() - started, "outputs": listed, "qc": qc}],
            "qc_version": 7,
        }
        (result / "summary.json").write_text(json.dumps(summary, indent=2, default=str) + "\n")
        _publish(result, output, stage, os.environ["CALMAR_EXECUTION_SCRIPT"],
                 os.environ["CALMAR_EXECUTION_SCRIPT"])


def _qc_overlay(image_path, masks, output, title):
    """Write a simple orthogonal PNG; scientific acceptance remains visual."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    image = nib.as_closest_canonical(nib.load(str(image_path)))
    data = np.asarray(image.dataobj, dtype=np.float32)
    finite = data[np.isfinite(data)]
    low, high = np.percentile(finite, [2, 98]) if finite.size else (0, 1)
    mask_data = []
    for path, color, label in masks:
        mask = nib.as_closest_canonical(nib.load(str(path)))
        if not _same_grid(mask, image):
            mask = resample_from_to(mask, image, order=0)
        mask_data.append((np.asarray(mask.dataobj) > 0, color, label))
    combined = np.zeros(data.shape, dtype=bool)
    for mask, _, _ in mask_data:
        combined |= mask
    if combined.any():
        centre = tuple(int(round(value)) for value in np.argwhere(combined).mean(axis=0))
    else:
        centre = tuple(size // 2 for size in data.shape)
    planes = [(data[centre[0], :, :].T, 0), (data[:, centre[1], :].T, 1), (data[:, :, centre[2]].T, 2)]
    fig, axes = plt.subplots(1, 3, figsize=(12, 4), constrained_layout=True)
    for ax, (background, axis) in zip(axes, planes):
        ax.imshow(background, cmap="gray", origin="lower", vmin=low, vmax=high)
        for mask, color, label in mask_data:
            plane = ({0: mask[centre[0], :, :].T,
                      1: mask[:, centre[1], :].T,
                      2: mask[:, :, centre[2]].T}[axis])
            if plane.any():
                ax.contour(plane.astype(float), levels=[0.5], colors=[color], linewidths=1.1)
        ax.axis("off")
    fig.suptitle(title + " · " + " · ".join(label for _, _, label in mask_data))
    fig.savefig(output, dpi=130)
    plt.close(fig)
    if Path(output).read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
        raise RuntimeError(f"QC output is not a PNG: {output}")


def anatomy(request, output):
    _require_slurm()
    started, entry = time.monotonic(), _entry(request)
    if "atrophy" not in _components(entry):
        raise ValueError("brain_health_anatomy requested for an entry without T1 volumetry selected")
    t1w = _materialize(entry.get("anatomical_t1w") or entry.get("t1w"), request["dataset"])
    final = output_paths(request["dataset"], request["config"], entry)["anatomy"]
    final.parent.mkdir(parents=True, exist_ok=True)
    overwrite = bool(request["config"].get("BRAIN_HEALTH_OVERWRITE", False))
    if final.exists() and not overwrite:
        files = [final / name for name in ("segmentation.nii.gz", "volumes.csv", "synthseg_qc.csv",
                                           "anatomy_metrics.json", "anatomy_qc.png")]
        if any(not path.is_file() for path in files):
            raise RuntimeError(f"Existing brain-health anatomy output is incomplete: {final}")
        previous = json.loads((final / "anatomy_metrics.json").read_text())
        _publish_summary(output, "brain_health_anatomy", request, entry, final, started, files,
                         {"png": str(final / "anatomy_qc.png"),
                          "metrics": previous.get("measurements", {}),
                          "flags": previous.get("warnings", []), "complete": True})
        return
    with tempfile.TemporaryDirectory(prefix="brain_health_anatomy.attempt.", dir=final.parent) as folder:
        folder = Path(folder)
        produced = folder / "produced"
        produced.mkdir()
        segmentation = produced / "segmentation.nii.gz"
        synthseg_mode = request["config"].get("BRAIN_HEALTH_SYNTHSEG_MODE", "robust")
        if synthseg_mode not in {"standard", "robust"}:
            raise ValueError("BRAIN_HEALTH_SYNTHSEG_MODE must be 'standard' or 'robust'")
        command = ["mri_synthseg", "--i", t1w, "--o", segmentation, "--parc",
                   "--keepgeom", "--vol", produced / "volumes.csv", "--qc", produced / "synthseg_qc.csv",
                   "--cpu", "--threads", os.environ.get("SLURM_CPUS_PER_TASK", "8")]
        if synthseg_mode == "robust":
            command.append("--robust")
        _run(command, folder / "synthseg.log")
        _, seg = _validate_mask(segmentation, t1w)
        t1 = nib.load(str(t1w))
        voxel_ml = abs(np.linalg.det(t1.affine[:3, :3])) / 1000.0
        seg = np.rint(seg).astype(np.int32)
        intracranial = seg > 0
        tissue = intracranial & ~np.isin(seg, tuple(CSF_LABELS))
        lesion, lesion_source, _ = _native_lesion(request, entry)
        if lesion_source == "openads":
            raise ValueError("OpenADS is DWI-space and cannot adjust T1 SynthSeg anatomy metrics.")
        lesion_cavity = np.zeros(seg.shape, dtype=bool)
        warnings = []
        if lesion is not None:
            lesion = _materialize(lesion, request["dataset"])
            lesion_image = nib.load(str(lesion))
            if not _same_grid(lesion_image, t1):
                lesion_image = resample_from_to(lesion_image, t1, order=0)
            lesion_data = np.asarray(lesion_image.dataobj) > 0
            lesion_cavity = lesion_data & (~intracranial | np.isin(seg, tuple(CSF_LABELS)))
        else:
            warnings.append(f"native {lesion_source} lesion mask unavailable; cavity adjustment not calculated")
        icv_ml = float(intracranial.sum() * voxel_ml)
        tissue_ml = float(tissue.sum() * voxel_ml)
        lesion_cavity_ml = float(lesion_cavity.sum() * voxel_ml) if lesion is not None else None
        adjusted_denominator = icv_ml + (float((lesion_cavity & ~intracranial).sum() * voxel_ml)
                                         if lesion is not None else 0.0)
        adjusted_fraction = ((tissue_ml + lesion_cavity_ml) / adjusted_denominator
                             if lesion is not None and adjusted_denominator else None)
        lateral = np.isin(seg, tuple(LATERAL_VENTRICLE_LABELS))
        lesion_overlap = lesion_data & lateral if lesion is not None else np.zeros(seg.shape, dtype=bool)
        lateral_outside_lesion = lateral & ~lesion_overlap
        if lesion is not None and lesion_overlap.any():
            warnings.append("stroke lesion overlaps SynthSeg lateral-ventricle labels; raw ventricle volumes may reflect the cavity")
        measures = {
            "intracranial_volume_ml": icv_ml, "brain_tissue_volume_ml": tissue_ml,
            "brain_parenchymal_fraction": tissue_ml / icv_ml if icv_ml else None,
            "lesion_cavity_ml": lesion_cavity_ml,
            "lesion_adjusted_brain_parenchymal_fraction": adjusted_fraction,
            "lateral_ventricle_fraction": float(lateral.sum() * voxel_ml / icv_ml) if icv_ml else None,
            "lesion_masked_lateral_ventricle_fraction": float(lateral_outside_lesion.sum() * voxel_ml / icv_ml)
                                                         if icv_ml and lesion is not None else None,
            "lesion_ventricle_overlap_ml": float(lesion_overlap.sum() * voxel_ml) if lesion is not None else None,
            "left_lateral_ventricle_ml": float(np.isin(seg, tuple(LEFT_LATERAL_VENTRICLE_LABELS)).sum() * voxel_ml),
            "right_lateral_ventricle_ml": float(np.isin(seg, tuple(RIGHT_LATERAL_VENTRICLE_LABELS)).sum() * voxel_ml),
        }
        metadata = {"measurements": measures, "warnings": warnings,
                    "lesion_mask_source": lesion_source, "synthseg_mode": synthseg_mode,
                    "method": {"tool": "SynthSeg", "version": os.environ.get("CALMAR_SYNTHSEG_VERSION")},
                    "qc_status": "requires_visual_review"}
        (produced / "anatomy_metrics.json").write_text(json.dumps(metadata, indent=2) + "\n")
        shutil.copy2(folder / "synthseg.log", produced / "synthseg.log")
        _qc_overlay(t1w, [(segmentation, "cyan", "SynthSeg boundary")],
                    produced / "anatomy_qc.png", f"{entry['subject']} anatomy")
        _publish(produced, final, "brain_health_anatomy", os.environ["CALMAR_EXECUTION_SCRIPT"],
                 os.environ["CALMAR_EXECUTION_SCRIPT"], overwrite)
    files = [final / name for name in ("segmentation.nii.gz", "volumes.csv", "synthseg_qc.csv",
                                       "anatomy_metrics.json", "anatomy_qc.png")]
    if any(not path.is_file() for path in files):
        raise RuntimeError(f"Incomplete SynthSeg publication: {final}")
    _publish_summary(output, "brain_health_anatomy", request, entry, final, started, files,
                     {"png": str(final / "anatomy_qc.png"), "metrics": measures,
                      "flags": warnings, "complete": True})


def wmh(request, output):
    _require_slurm()
    started, entry = time.monotonic(), _entry(request)
    if "wmh" not in _components(entry):
        raise ValueError("brain_health_wmh requested for an entry without FLAIR analysis selected")
    flair = _materialize(entry["flair"], request["dataset"])
    final = output_paths(request["dataset"], request["config"], entry)["wmh"]
    final.parent.mkdir(parents=True, exist_ok=True)
    overwrite = bool(request["config"].get("BRAIN_HEALTH_OVERWRITE", False))
    if final.exists() and not overwrite:
        files = [final / name for name in ("wmh_raw_mask.nii.gz", "wmh_raw_qc.png", "deepwmh.log")]
        if any(not path.is_file() for path in files):
            raise RuntimeError(f"Existing brain-health WMH output is incomplete: {final}")
        _publish_summary(output, "brain_health_wmh", request, entry, final, started, files,
                         {"png": str(final / "wmh_raw_qc.png"), "flags": [], "complete": True})
        return
    with tempfile.TemporaryDirectory(prefix="brain_health_wmh.attempt.", dir=final.parent) as folder:
        folder = Path(folder)
        raw = folder / "raw"
        case = (entry["subject"] + "_" + (entry.get("session") or "noses")).replace("_to_", "_")
        _run(["deepwmh", "-i", flair, "-n", case, "-o", raw, "-g", "-1"], folder / "deepwmh.log")
        candidates = sorted((raw / "002_Segmentations" / "003_postproc_fov").glob("*.nii*"))
        if len(candidates) != 1:
            raise RuntimeError(f"Expected one final DeepWMH mask, found {len(candidates)} in {raw}")
        produced = folder / "produced"
        produced.mkdir()
        mask = produced / "wmh_raw_mask.nii.gz"
        image = nib.load(str(candidates[0]))
        _save_like(np.asarray(image.dataobj) > 0, image, mask)
        _validate_mask(mask, flair, allow_empty=True)
        shutil.copy2(folder / "deepwmh.log", produced / "deepwmh.log")
        (produced / "wmh_metrics.json").write_text(json.dumps({
            "method": {"tool": "DeepWMH", "version": os.environ.get("CALMAR_DEEPWMH_VERSION")},
            "qc_status": "requires_visual_review",
        }, indent=2) + "\n")
        _qc_overlay(flair, [(mask, "yellow", "raw FLAIR hyperintensity")],
                    produced / "wmh_raw_qc.png", f"{entry['subject']} DeepWMH")
        _publish(produced, final, "brain_health_wmh", os.environ["CALMAR_EXECUTION_SCRIPT"],
                 os.environ["CALMAR_EXECUTION_SCRIPT"], overwrite)
    files = [final / name for name in ("wmh_raw_mask.nii.gz", "wmh_raw_qc.png", "deepwmh.log")]
    if any(not path.is_file() for path in files):
        raise RuntimeError(f"Incomplete DeepWMH publication: {final}")
    _publish_summary(output, "brain_health_wmh", request, entry, final, started, files,
                     {"png": str(final / "wmh_raw_qc.png"), "flags": [], "complete": True})


def _register_lesion(request, entry, flair, destination, log):
    lesion, source, moving = _native_lesion(request, entry)
    if lesion is None:
        return None, source, "native lesion mask unavailable; stroke signal could not be excluded"
    lesion = _materialize(lesion, request["dataset"])
    if moving is None:
        raise ValueError(f"No native reference image is recorded for the {source} lesion mask.")
    moving = _materialize(moving, request["dataset"])
    fixed_image, moving_image = nib.load(str(flair)), nib.load(str(moving))
    lesion_image = nib.load(str(lesion))
    if not _same_grid(lesion_image, moving_image):
        raise RuntimeError(
            f"The {source} lesion is not on its declared native reference grid; refusing a potentially "
            f"misregistered FLAIR exclusion ({lesion} vs {moving}).")
    if _same_grid(fixed_image, moving_image):
        transformed = resample_from_to(lesion_image, fixed_image, order=0)
        _save_like(np.asarray(transformed.dataobj) > 0, fixed_image, destination)
        if not np.any(np.asarray(transformed.dataobj) > 0):
            return None, source, "registered stroke lesion is empty; stroke signal could not be excluded"
        return destination, source, None
    prefix = destination.parent / "lesion_to_flair_"
    threads = os.environ.get("SLURM_CPUS_PER_TASK", "4")
    seed = str(request["config"].get("BRAIN_HEALTH_REGISTRATION_SEED", 1729))
    _run(["antsRegistrationSyNQuick.sh", "-d", 3, "-f", flair, "-m", moving,
          "-o", prefix, "-t", "a", "-n", threads, "-y", 1, "-e", seed], log)
    _run(["antsApplyTransforms", "-d", 3, "-i", lesion, "-r", flair,
          "-t", str(prefix) + "0GenericAffine.mat", "-n", "NearestNeighbor", "-o", destination], log)
    _, data = _validate_mask(destination, flair, allow_empty=True)
    if not np.any(data > 0):
        return None, source, "registered stroke lesion is empty; stroke signal could not be excluded"
    return destination, source, None


def metrics(request, output):
    _require_slurm()
    started, entry = time.monotonic(), _entry(request)
    components = _components(entry)
    if not components:
        raise ValueError("No brain-health component was selected")
    paths = output_paths(request["dataset"], request["config"], entry)
    final = paths["metrics"]
    final.parent.mkdir(parents=True, exist_ok=True)
    overwrite = bool(request["config"].get("BRAIN_HEALTH_OVERWRITE", False))
    if final.exists() and not overwrite:
        files = [final / name for name in ("brain_health.json", "brain_health.tsv", "brain_health_qc.png")]
        if any(not path.is_file() for path in files):
            raise RuntimeError(f"Existing brain-health metrics output is incomplete: {final}")
        previous = json.loads((final / "brain_health.json").read_text())
        _publish_summary(output, "brain_health_metrics", request, entry, final, started, files,
                         {"png": str(final / "brain_health_qc.png"),
                          "metrics": previous.get("measurements", {}),
                          "flags": previous.get("warnings", []), "complete": True})
        return
    measurements, warnings = {}, []
    anatomy_metadata = None
    if "atrophy" in components:
        source = paths["anatomy"] / "anatomy_metrics.json"
        if not source.is_file():
            raise FileNotFoundError(f"Run brain_health_anatomy first: {source}")
        anatomy_metadata = json.loads(source.read_text())
        expected_source = request["config"].get("BRAIN_HEALTH_MASK_SOURCE", "manual")
        expected_mode = request["config"].get("BRAIN_HEALTH_SYNTHSEG_MODE", "robust")
        if anatomy_metadata.get("lesion_mask_source") != expected_source:
            raise RuntimeError("SynthSeg metrics used a different lesion source; rerun brain_health_anatomy.")
        if anatomy_metadata.get("synthseg_mode") != expected_mode:
            raise RuntimeError("SynthSeg metrics used a different inference mode; rerun brain_health_anatomy.")
        measurements.update(anatomy_metadata["measurements"])
        warnings.extend(anatomy_metadata.get("warnings") or ())
    with tempfile.TemporaryDirectory(prefix="brain_health_metrics.attempt.", dir=final.parent) as folder:
        folder = Path(folder)
        produced = folder / "produced"
        produced.mkdir()
        qc_image = entry.get("anatomical_t1w") or entry.get("t1w")
        overlays = []
        lesion_source = request["config"].get("BRAIN_HEALTH_MASK_SOURCE", "manual")
        if "wmh" in components:
            flair = _materialize(entry["flair"], request["dataset"])
            raw_path = paths["wmh"] / "wmh_raw_mask.nii.gz"
            if not raw_path.is_file():
                raise FileNotFoundError(f"Run brain_health_wmh first: {raw_path}")
            raw_image, raw = _validate_mask(raw_path, flair, allow_empty=True)
            raw = raw > 0
            lesion_path, lesion_source, registration_warning = _register_lesion(
                request, entry, flair, produced / "stroke_lesion_in_flair.nii.gz", folder / "registration.log")
            if registration_warning:
                warnings.append(registration_warning)
                exclusion = None
            else:
                lesion_data = np.asarray(nib.load(str(lesion_path)).dataobj) > 0
                margin = float(request["config"].get("BRAIN_HEALTH_LESION_EXCLUSION_MM", 3.0))
                distance = distance_transform_edt(~lesion_data, sampling=raw_image.header.get_zooms()[:3])
                exclusion = distance <= margin
                _save_like(exclusion, raw_image, produced / "stroke_exclusion_zone.nii.gz")
            voxel_ml = abs(np.linalg.det(raw_image.affine[:3, :3])) / 1000.0
            icv = measurements.get("intracranial_volume_ml")
            measurements.update(_wmh_measurements(raw, exclusion, voxel_ml, icv))
            if exclusion is None:
                overlays = [(raw_path, "yellow", "raw FLAIR hyperintensity")]
            else:
                candidate = raw & ~exclusion
                _save_like(candidate, raw_image, produced / "wmh_candidate_mask.nii.gz")
                overlays = [(produced / "wmh_candidate_mask.nii.gz", "yellow", "WMH candidate")]
            if modality(request["config"]) == "dwi":
                warnings.append("acute FLAIR: infarct-related oedema may extend beyond the exclusion zone")
            qc_image = flair
            if lesion_path is not None:
                overlays.append((lesion_path, "red", "registered stroke lesion"))
        else:
            overlays = [(paths["anatomy"] / "segmentation.nii.gz", "cyan", "SynthSeg boundary")]
        metadata = {
            "subject": entry["subject"], "session": entry.get("session"),
            "components": sorted(components), "anatomy": "atrophy" in components,
            "wmh": "wmh" in components, "flair": entry.get("flair"),
            "stroke_phase": request["config"].get("STROKE_PHASE"),
            "lesion_mask_source": lesion_source,
            "anatomy_lesion_mask_source": (anatomy_metadata.get("lesion_mask_source")
                                            if anatomy_metadata else None),
            "synthseg_mode": (anatomy_metadata.get("synthseg_mode") if anatomy_metadata else None),
            "lesion_exclusion_mm": (float(request["config"].get("BRAIN_HEALTH_LESION_EXCLUSION_MM", 3.0))
                                    if "wmh" in components else None),
            "methods": {
                "anatomy": ((anatomy_metadata.get("method") or
                             {"tool": "SynthSeg", "version": None})
                            if "atrophy" in components else None),
                "wmh": ((json.loads((paths["wmh"] / "wmh_metrics.json").read_text()).get("method")
                         if (paths["wmh"] / "wmh_metrics.json").is_file() else
                         {"tool": "DeepWMH", "version": None})
                        if "wmh" in components else None),
                "lesion_to_flair_registration": (
                    {"tool": "ANTs", "version": os.environ.get("CALMAR_ANTS_VERSION")}
                    if "wmh" in components else None),
            },
            "qc_status": "requires_visual_review", "warnings": list(dict.fromkeys(warnings)),
            "measurements": measurements,
        }
        (produced / "brain_health.json").write_text(json.dumps(metadata, indent=2, default=str) + "\n")
        with (produced / "brain_health.tsv").open("w", newline="", encoding="utf-8") as stream:
            writer = csv.writer(stream, delimiter="\t")
            writer.writerow(["measurement", "value"])
            writer.writerows((key, "n/a" if value is None else value) for key, value in measurements.items())
        _qc_overlay(qc_image, overlays, produced / "brain_health_qc.png", f"{entry['subject']} brain health")
        if (folder / "registration.log").is_file():
            shutil.copy2(folder / "registration.log", produced / "registration.log")
        _publish(produced, final, "brain_health_metrics", os.environ["CALMAR_EXECUTION_SCRIPT"],
                 os.environ["CALMAR_EXECUTION_SCRIPT"], overwrite)
    files = [final / name for name in ("brain_health.json", "brain_health.tsv", "brain_health_qc.png")]
    if any(not path.is_file() for path in files):
        raise RuntimeError(f"Incomplete brain-health metric publication: {final}")
    _publish_summary(output, "brain_health_metrics", request, entry, final, started, files,
                     {"png": str(final / "brain_health_qc.png"), "metrics": measurements,
                      "flags": warnings, "complete": True})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("brain_health_anatomy", "brain_health_wmh", "brain_health_metrics"))
    parser.add_argument("request", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    request = json.loads(args.request.read_text(encoding="utf-8"))
    def margin_value(value):
        value = str(value)
        if value.startswith("margin_") and value.endswith("mm"):
            value = value[len("margin_"):-len("mm")]
        return float(value)
    overrides = {
        "CALMAR_BRAIN_HEALTH_SYNTHSEG_MODE": ("BRAIN_HEALTH_SYNTHSEG_MODE", str),
        "CALMAR_BRAIN_HEALTH_MASK_SOURCE": ("BRAIN_HEALTH_MASK_SOURCE", str),
        "CALMAR_BRAIN_HEALTH_LESION_EXCLUSION_MM": ("BRAIN_HEALTH_LESION_EXCLUSION_MM", margin_value),
    }
    for environment, (key, convert) in overrides.items():
        if environment in os.environ:
            request["config"][key] = convert(os.environ[environment])
    if args.output.exists():
        raise FileExistsError(args.output)
    {"brain_health_anatomy": anatomy, "brain_health_wmh": wmh,
     "brain_health_metrics": metrics}[args.stage](request, args.output)


if __name__ == "__main__":
    main()
