"""Lesion overlap and tensor profiles for selected AutoTrack reconstructions."""

from __future__ import annotations

import gzip
import json
from pathlib import Path
import re
import subprocess

import nibabel as nib
import numpy as np
import pandas as pd


BUNDLES = {
    "AssociationArcuateFasciculus": "Arcuate fasciculus",
    "AssociationFrontalAslantTract": "Frontal aslant tract",
    "AssociationInferiorFrontoOccipitalFasciculus": "Inferior fronto-occipital fasciculus",
}
ASLANT = "AssociationFrontalAslantTract"
SIDES = {"L": "Left", "R": "Right"}
SUPPORTED_RECON = {"ss3t_fod_autotrack", "dsi_studio_autotrack"}


class BundleQCUnavailable(ValueError):
    """A required input is unusable for supplemental bundle measurements."""


def profile_nodes(config):
    count = config.get("DMRI_PROFILE_NODES", 21)
    if isinstance(count, bool) or not isinstance(count, int) or not 5 <= count <= 101:
        raise ValueError("DMRI_PROFILE_NODES must be an integer between 5 and 101.")
    return count


def _unique(root, pattern):
    matches = sorted(root.rglob(pattern))
    if len(matches) != 1:
        raise BundleQCUnavailable(f"Expected one {pattern}, found {len(matches)}.")
    return matches[0]


def _same_grid(image, reference):
    return (image.shape == reference.shape and len(image.shape) == 3 and
            np.allclose(image.affine, reference.affine, atol=1e-3, rtol=0))


def _require_file(path):
    if not path.is_file():
        raise BundleQCUnavailable(f"Required bundle QC input is missing: {path.name}")
    return path


def _on_grid(path, reference):
    image = nib.load(_require_file(path))
    if not _same_grid(image, reference):
        raise BundleQCUnavailable(f"Image grids differ for {path.name} and its reference.")
    return image.get_fdata(dtype=np.float32)


def _inputs(preproc, recon, output):
    selection = json.loads(_require_file(preproc / "calmar-selection.json").read_text())
    if not selection.get("lesion_mask") or not selection.get("anatomical_t1w"):
        raise BundleQCUnavailable("QSIPrep does not record the native lesion and T1 inputs.")
    lesion, t1 = (Path(selection[key]) for key in ("lesion_mask", "anatomical_t1w"))
    reference_path = _unique(preproc, "*_space-ACPC_desc-preproc_dwiref.nii.gz")
    reference = nib.load(reference_path)
    if len(reference.shape) != 3 or not np.isfinite(reference.affine).all():
        raise BundleQCUnavailable("QSIPrep diffusion reference must have a finite three-dimensional grid.")
    background = reference.get_fdata(dtype=np.float32)
    if not (np.isfinite(background) & (background > 0)).any():
        raise BundleQCUnavailable("The QSIPrep diffusion reference has no usable intensities for visual QC.")
    mask_path = reference_path.with_name(reference_path.name.replace("desc-preproc_dwiref", "desc-brain_mask"))
    source_lesion = _on_grid(lesion, nib.load(_require_file(t1)))
    if not np.isfinite(source_lesion).all() or not np.isin(source_lesion, [0, 1]).all():
        raise BundleQCUnavailable("The selected lesion must be a finite binary mask on the native T1 grid.")
    if not source_lesion.any():
        raise BundleQCUnavailable("The selected native T1 lesion mask is empty.")
    anat_to_acpc = _unique(preproc, "*_from-anat_to-ACPC_mode-image_xfm.mat")
    orig_to_anat = _unique(preproc, "*_from-orig_to-anat_mode-image_xfm.txt")
    aligned = output / "lesion_on_diffusion_grid.nii.gz"
    ants_version = subprocess.run(["antsRegistration", "--version"], check=True,
                                  capture_output=True, text=True).stdout.strip()
    subprocess.run([
        "antsApplyTransforms", "-d", "3", "-i", str(lesion), "-r", str(reference_path),
        "-o", str(aligned), "-n", "NearestNeighbor",
        "-t", str(anat_to_acpc), "-t", str(orig_to_anat),
    ], check=True)
    lesion_mask = _on_grid(aligned, reference) > 0
    brain = _on_grid(mask_path, reference) > 0
    if not (lesion_mask & brain).any():
        raise BundleQCUnavailable(
            "The resampled lesion has no voxels in the diffusion brain mask. Review alignment and voxel size.")
    fa_path = _unique(recon, "*_space-ACPC_model-tensor_param-fa_dwimap.nii.gz")
    md_path = _unique(recon, "*_space-ACPC_model-tensor_param-md_dwimap.nii.gz")
    fa = _on_grid(fa_path, reference)
    md = _on_grid(md_path, reference)
    md_sidecar = md_path.with_name(md_path.name.removesuffix(".nii.gz") + ".json")
    units = json.loads(_require_file(md_sidecar).read_text()).get("Units")
    normalized = str(units).translate(str.maketrans({"µ": "μ", "²": "2", "^": "", " ": ""}))
    scale = {"μm2/ms": 0.001, "um2/ms": 0.001, "mm2/s": 1.0}.get(normalized)
    if scale is None:
        raise BundleQCUnavailable(f"Missing or unsupported tensor MD units ({units!r}).")
    md *= scale
    positive_md = md[brain & np.isfinite(md) & (md > 0)]
    if not positive_md.size or not 0.00005 <= np.median(positive_md) <= 0.005:
        raise BundleQCUnavailable(f"Tensor MD map values disagree with the documented units {units!r}.")
    valid = brain & np.isfinite(fa) & np.isfinite(md) & (fa >= 0) & (fa <= 1) & (md > 0) & (md <= 0.01)
    provenance = {
        "native_lesion": str(lesion), "native_t1": str(t1), "diffusion_reference": str(reference_path),
        "diffusion_brain_mask": str(mask_path), "lesion_transform_chain": [str(orig_to_anat), str(anat_to_acpc)],
        "fa_map": str(fa_path), "md_map": str(md_path), "md_source_units": units, "md_scale": scale,
        "md_sidecar": str(md_sidecar),
        "ants_version": ants_version,
        "lesion_voxels_on_grid": int(lesion_mask.sum()),
        "lesion_voxels_in_brain_mask": int((lesion_mask & brain).sum()),
    }
    return reference, lesion_mask, fa, md, valid, provenance


def _voxels(points, inverse, shape):
    indices = np.floor(nib.affines.apply_affine(inverse, points) + 0.5).astype(int)
    inside = ((indices >= 0) & (indices < shape)).all(axis=1)
    return indices[inside], inside


def _sample_bundle(path, reference, nodes, *, superior_first=False):
    """Sample occupancy densely in voxel space and profiles uniformly by arc length."""
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rb") as source:
        streamlines = nib.streamlines.TckFile.load(source).streamlines
    inverse = np.linalg.inv(reference.affine)
    occupied = set()
    profile = [set() for _ in range(nodes)]
    out_of_grid = 0
    skipped = 0
    # In RAS, start the aslant tract at its superior end. For other bundles
    # start posteriorly. The other axes break equal-coordinate ties.
    order = [2, 1, 0] if superior_first else [1, 2, 0]
    for line in streamlines:
        if len(line) < 2 or not np.isfinite(line).all():
            skipped += 1
            continue
        start, end = tuple(line[0, order]), tuple(line[-1, order])
        if (start < end if superior_first else start > end):
            line = line[::-1]
        lengths = np.linalg.norm(np.diff(line, axis=0), axis=1)
        distinct = np.r_[True, lengths > 0]
        if distinct.sum() < 2:
            skipped += 1
            continue
        line = line[distinct]
        distance = np.r_[0, np.cumsum(lengths[lengths > 0], dtype=float)]
        deltas = np.diff(nib.affines.apply_affine(inverse, line), axis=0)
        steps = np.maximum(1, np.ceil(2 * np.linalg.norm(deltas, axis=1))).astype(int)
        starts = np.cumsum(steps) - steps
        offsets = np.arange(steps.sum()) - np.repeat(starts, steps)
        dense = np.r_[np.repeat(distance[:-1], steps) +
                      offsets * np.repeat(np.diff(distance) / steps, steps), distance[-1]]

        def sample(at):
            points = np.column_stack([np.interp(at, distance, axis) for axis in line.T])
            return _voxels(points, inverse, reference.shape)

        voxels, inside = sample(dense)
        occupied.update(map(tuple, voxels))
        out_of_grid += int((~inside).sum())
        voxels, inside = sample(np.linspace(0, distance[-1], nodes))
        for node, voxel in zip(np.flatnonzero(inside), voxels):
            profile[node].add(tuple(voxel))
    return occupied, profile, len(streamlines), out_of_grid, skipped


def _plot(output, reference, lesion, overlays, profiles):
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.figure import Figure

    reference = nib.as_closest_canonical(reference)
    background = reference.get_fdata()
    vmax = np.percentile(background[np.isfinite(background) & (background > 0)], 99)
    lesion = lesion.astype(np.uint8)
    figure = Figure(figsize=(9.6, 2.1 * len(overlays)))
    FigureCanvasAgg(figure)
    for row, (label, tract) in enumerate(overlays):
        overlap = tract & lesion
        anchor = overlap if overlap.any() else tract
        if not anchor.any():
            anchor = lesion
        anchor = np.argwhere(anchor).mean(axis=0).round().astype(int)
        for axis, plane in enumerate(("Sagittal", "Coronal", "Axial")):
            ax = figure.add_subplot(len(overlays), 3, row * 3 + axis + 1)
            ax.imshow(np.take(background, anchor[axis], axis=axis).T, cmap="gray",
                      origin="lower", vmin=0, vmax=vmax, interpolation="nearest")
            for data, color in ((tract, "deepskyblue"), (lesion, "tomato")):
                layer = np.take(data, anchor[axis], axis=axis).T
                if layer.any():
                    ax.contour(layer, levels=[0.5], colors=[color], linewidths=0.9)
            ax.set_title(f"{label}\n{plane}" if axis == 0 else plane, fontsize=9)
            ax.set_axis_off()
    figure.suptitle("Diffusion-space QC | blue: reconstructed bundle · red: registered lesion")
    figure.tight_layout()
    figure.savefig(output / "bundle_lesion_qc.png", dpi=130)

    if profiles.empty:
        return
    figure = Figure(figsize=(10, 7))
    FigureCanvasAgg(figure)
    axes = figure.subplots(3, 2, sharex=True)
    for (row_axes, label) in zip(axes, BUNDLES.values()):
        bundle = profiles[profiles["bundle"] == label]
        for side, color in zip(SIDES.values(), ("#026e89", "#bb4e23")):
            subset = bundle[bundle["hemisphere"] == side]
            row_axes[0].plot(subset["distance_pct"], subset["fa_median"], label=side, color=color)
            row_axes[1].plot(subset["distance_pct"], subset["md_median_mm2_s"], label=side, color=color)
        row_axes[0].set_ylabel(f"{label}\nFA", fontsize=9)
        row_axes[0].set_ylim(0, 1)
        row_axes[1].set_ylabel("MD (mm²/s)", fontsize=9)
    axes[0, 1].legend(loc="upper right")
    for ax in axes[-1]:
        ax.set_xlabel("Normalized streamline distance (%)")
    figure.suptitle("Median tensor values along reconstructed bundles")
    figure.tight_layout()
    figure.savefig(output / "bundle_profiles.png", dpi=130)


def _on_plot_grid(data, reference):
    return np.asarray(nib.as_closest_canonical(
        nib.Nifti1Image(data.astype(np.uint8), reference.affine)).dataobj)


def measure_bundles(preproc, recon, table, output, nodes):
    """Write exploratory profile and QC artifacts, and enrich matching tract rows."""
    try:
        reference, lesion, fa, md, valid, provenance = _inputs(preproc, recon, output)
    except (json.JSONDecodeError, nib.filebasedimages.ImageFileError) as exc:
        raise BundleQCUnavailable("A diffusion-space image or metadata file could not be decoded.") from exc
    tracks = {}
    for path in recon.rglob("*_space-ACPC_*_streamlines.tck*"):
        match = re.search(r"_bundle-([^_]+)_streamlines\.tck(?:\.gz)?$", path.name)
        if match:
            tracks.setdefault(match[1], []).append(path)
    if not any(bundle + side in tracks for bundle in BUNDLES for side in SIDES):
        raise BundleQCUnavailable(
            "None of the six expected AutoTrack streamlines match the derivative filenames.")
    table_keys = table["tract"].str.replace(r"[^A-Za-z0-9]", "", regex=True).str.lower()
    overlays, rows, statuses = [], [], []
    for bundle, name in BUNDLES.items():
        for suffix, side in SIDES.items():
            key = bundle + suffix
            status = {"bundle": name, "hemisphere": side, "status": "no streamline file"}
            statuses.append(status)
            files = tracks.get(key, [])
            if not files:
                continue
            if len(files) != 1:
                status["status"] = "multiple streamline files"
                continue
            try:
                occupied, profile, count, outside, skipped = _sample_bundle(
                    files[0], reference, nodes, superior_first=bundle == ASLANT)
            except (OSError, EOFError, nib.streamlines.tractogram_file.DataError,
                    nib.streamlines.tractogram_file.HeaderError):
                status.update(status="unreadable streamline file", source=str(files[0]))
                continue
            status.update(source=str(files[0]), streamline_count=count, outside_grid_samples=outside,
                          unusable_streamlines=skipped,
                          profile_start="superior" if bundle == ASLANT else "posterior")
            if not occupied:
                status["status"] = "no usable voxels in diffusion grid"
                continue
            tract = np.zeros(reference.shape, dtype=bool)
            tract[tuple(np.array(sorted(occupied)).T)] = True
            label = f"{side} {name.lower()}"
            overlays.append((label, _on_plot_grid(tract, reference)))
            overlap = int((tract & lesion).sum())
            covered = int((tract & valid).sum())
            status.update(status="measured", occupied_voxels=len(occupied), overlap_voxels=overlap,
                          valid_voxels=covered)
            indices = table_keys.index[table_keys == key.lower()]
            if len(indices) > 1:
                raise BundleQCUnavailable(f"Multiple QSIRecon summary rows match {key}.")
            index = indices[0] if len(indices) else len(table)
            if not len(indices):
                table.loc[index] = {"tract": key, "hemisphere": side.lower()}
            table.loc[index, "lesion_overlap_pct"] = 100 * overlap / len(occupied)
            table.loc[index, "valid_voxel_pct"] = 100 * covered / len(occupied)
            for point, voxels in enumerate(profile):
                positions = tuple(np.array(sorted(voxels), dtype=int).reshape(-1, 3).T)
                usable = valid[positions]
                rows.append({
                    "bundle": name, "hemisphere": side, "node": point + 1,
                    "distance_pct": 100 * point / (nodes - 1),
                    "sampled_voxels": len(voxels), "valid_voxels": int(usable.sum()),
                    "lesion_voxels": int(lesion[positions].sum()),
                    "fa_median": np.median(fa[positions][usable]) if usable.any() else np.nan,
                    "md_median_mm2_s": np.median(md[positions][usable]) if usable.any() else np.nan,
                })
    profiles = pd.DataFrame(rows)
    if not profiles.empty:
        profiles.to_csv(output / "bundle_profiles.tsv", sep="\t", index=False, na_rep="n/a")
    plot_lesion = _on_plot_grid(lesion, reference)
    if not overlays:
        overlays = [("No selected bundles measured", np.zeros_like(plot_lesion))]
    _plot(output, reference, plot_lesion, overlays, profiles)
    return {
        "status": "computed", "profile_nodes": nodes, "bundles": statuses, "sources": provenance,
        "qc_png": "bundle_lesion_qc.png", "aligned_lesion": "lesion_on_diffusion_grid.nii.gz",
        "profile_tsv": "bundle_profiles.tsv" if rows else None,
        "profile_png": "bundle_profiles.png" if rows else None,
    }
