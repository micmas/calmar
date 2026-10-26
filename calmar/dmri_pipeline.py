"""Scheduler-only QSIPrep/QSIRecon orchestration for optional direct dMRI."""

from __future__ import annotations

import argparse
import fcntl
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time
from uuid import uuid4

import pandas as pd

from .acquisition import ensure_nifti_content
from .diffusion import DMRI_SUBDIR, tractometry_paths
from .study import Study


def _require_slurm():
    if not os.environ.get("SLURM_JOB_ID"):
        raise RuntimeError("Direct dMRI processing must be submitted with its retained Slurm script.")


def _entry(request):
    entries = request.get("entries") or []
    if len(entries) != 1:
        raise ValueError("A direct dMRI job requires exactly one participant entry.")
    return entries[0]


def _subject_parts(entry):
    return entry["subject"], entry.get("session"), entry["subject"].removeprefix("sub-")


def _final_dir(request, entry, stage):
    subject, session, _ = _subject_parts(entry)
    return (Path(request["dataset"]) / request["config"].get("DMRI_SUBDIR", DMRI_SUBDIR) /
            subject / (session or "") / stage)


def _link(source, target):
    source, target = Path(source), Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.link(source.resolve(), target)
    except OSError:
        shutil.copy2(source, target)


def _materialize(path, dataset):
    path = Path(path)
    if path.is_file():
        return path
    if path.name.endswith((".nii", ".nii.gz")) and ensure_nifti_content(path, dataset):
        return path
    try:
        # Do not resolve a missing DataLad annex symlink into .git/annex; get
        # expects the dataset-relative user-facing path.
        relative = path.absolute().relative_to(Path(dataset).resolve())
    except ValueError:
        relative = None
    if relative is not None:
        subprocess.run(["datalad", "-C", str(dataset), "get", str(relative)], check=True)
    if not path.is_file():
        raise FileNotFoundError(f"Required direct-dMRI input is unavailable: {path}")
    return path


def _anatomical_entry(entry):
    return {**entry, "session": entry.get("anatomical_session"),
            "t1w": entry.get("anatomical_t1w") or entry.get("t1w")}


def _lesion_mask(request, entry):
    source = request["config"].get("DMRI_MASK_SOURCE", "manual")
    if source not in {"manual", "linda", "synthstroke"}:
        raise ValueError("DMRI_MASK_SOURCE must be manual, linda or synthstroke in native T1 space.")
    anatomical = _anatomical_entry(entry)
    study = Study(request["config"], request["dataset"], request["config"].get("PROJECT_DIR", "."))
    masks = study.masks(anatomical)
    mask = (masks.get(source) or {}).get("T1w")
    if mask is None:
        raise FileNotFoundError(
            f"Direct dMRI requires a native-T1 lesion mask from {source!r}; "
            f"none exists for {anatomical['subject']} {anatomical.get('session') or ''}.")
    return Path(mask), source


def stage_bids(request, entry, destination):
    """Build a one-participant BIDS input without modifying the source dataset."""
    destination = Path(destination)
    destination.mkdir(parents=True)
    subject, session, _ = _subject_parts(entry)
    stem = "_".join(filter(None, [subject, session]))
    dataset = request["dataset"]
    (destination / "dataset_description.json").write_text(json.dumps({
        "Name": "CALMaR selected stroke dMRI", "BIDSVersion": "1.10.0",
        "DatasetType": "raw",
    }, indent=2) + "\n")
    series = list(entry.get("dmri_assessment", {}).get("series") or [])
    if not series:
        series = [{key: entry.get(key) for key in ("dwi", "bval", "bvec", "json")}]
    for item in series:
        dwi = _materialize(item["dwi"], dataset)
        target = destination / subject / (session or "") / "dwi" / dwi.name
        _link(dwi, target)
        base = str(dwi).removesuffix(".nii.gz").removesuffix(".nii")
        for kind, suffix in (("bval", ".bval"), ("bvec", ".bvec"), ("json", ".json")):
            source = item.get(kind) or base + suffix
            source = _materialize(source, dataset)
            _link(source, target.with_name(target.name.removesuffix(".nii.gz").removesuffix(".nii") + suffix))
    anatomical = _anatomical_entry(entry)
    t1w = _materialize(anatomical["t1w"], dataset)
    lesion, source = _lesion_mask(request, entry)
    lesion = _materialize(lesion, dataset)
    anat_dir = destination / subject / (session or "") / "anat"
    def nifti_extension(path):
        return ".nii.gz" if str(path).endswith(".nii.gz") else ".nii"
    _link(t1w, anat_dir / f"{stem}_T1w{nifti_extension(t1w)}")
    _link(lesion, anat_dir / f"{stem}_label-lesion_roi{nifti_extension(lesion)}")
    provenance = {
        "subject": subject, "diffusion_session": session,
        "anatomical_session": anatomical.get("session"),
        "anatomical_t1w": str(t1w), "lesion_mask": str(lesion), "lesion_mask_source": source,
        "cross_session_anatomy": anatomical.get("session") != session,
    }
    (destination / "calmar-selection.json").write_text(json.dumps(provenance, indent=2) + "\n")
    return provenance


def _run(command, log):
    with Path(log).open("w", encoding="utf-8") as stream:
        subprocess.run([str(value) for value in command], stdout=stream, stderr=subprocess.STDOUT,
                       text=True, check=True)


def _preserve_or_refuse(final, overwrite):
    final = Path(final)
    if not final.exists():
        return []
    if not overwrite:
        raise FileExistsError(f"Direct-dMRI output already exists and is preserved: {final}")
    backup = final.with_name(final.name + ".previous." + uuid4().hex)
    os.replace(final, backup)
    preserved = [(final, backup)]
    sidecar = Path(str(final) + ".prov.json")
    if sidecar.exists():
        backup_sidecar = Path(str(backup) + ".prov.json")
        os.replace(sidecar, backup_sidecar)
        preserved.append((sidecar, backup_sidecar))
    return preserved


def _publish(temporary, final, output_id, tool, script, overwrite=False):
    final = Path(final)
    final.parent.mkdir(parents=True, exist_ok=True)
    lock_path = final.with_name("." + final.name + ".lock")
    with lock_path.open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        preserved = _preserve_or_refuse(final, overwrite)
        try:
            subprocess.run(["neurodesk-astra-provenance", "publish", str(temporary), str(final),
                            "--output-id", output_id, "--tool", tool, "--script", script], check=True)
        except Exception:
            # Keep a failed publisher artifact recoverable and restore any
            # replaced result while the per-output lock excludes CALMaR races.
            if preserved:
                failed = final.with_name(final.name + ".failed." +
                                         os.environ.get("SLURM_JOB_ID", "unknown") + "." + uuid4().hex)
                if final.exists():
                    os.replace(final, failed)
                sidecar = Path(str(final) + ".prov.json")
                if sidecar.exists():
                    os.replace(sidecar, Path(str(failed) + ".prov.json"))
                for old, backup in reversed(preserved):
                    os.replace(backup, old)
            raise


def _publish_result(output, stage, request, entry, derivative, started, qc):
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=output.name + ".attempt.", dir=output.parent) as folder:
        result = Path(folder) / "result"
        result.mkdir()
        summary = {
            "stage": stage, "request": request, "job": os.environ["SLURM_JOB_ID"],
            "results": [{"subject": entry["subject"], "session": entry.get("session"),
                         "seconds": time.monotonic() - started,
                         "outputs": [{"path": str(derivative), "status": "computed"}],
                         "qc": qc}], "qc_version": 7,
        }
        (result / "summary.json").write_text(json.dumps(summary, indent=2, default=str) + "\n")
        _publish(result, output, stage, os.environ.get("CALMAR_PYTHON", "python"),
                 os.environ["CALMAR_EXECUTION_SCRIPT"])


def preprocess(request, output):
    _require_slurm()
    started = time.monotonic()
    entry = _entry(request)
    config = request["config"]
    final = _final_dir(request, entry, "qsiprep")
    overwrite = bool(config.get("DMRI_OVERWRITE", False))
    final.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="qsiprep.attempt.", dir=final.parent) as folder:
        folder = Path(folder)
        bids = folder / "bids"
        provenance = stage_bids(request, entry, bids)
        produced = folder / "produced"
        work = folder / "work"
        _, _, label = _subject_parts(entry)
        threads = int(os.environ.get("SLURM_CPUS_PER_TASK", "8"))
        memory = max(1024, int(float(os.environ.get("SLURM_MEM_PER_NODE", "32768")) * 0.9))
        command = [
            "qsiprep", bids, produced, "participant", "--participant-label", label,
            "--output-resolution", str(config.get("DMRI_OUTPUT_RESOLUTION", 2.0)),
            "--anat-modality", "T1w", "--hmc-method", "eddy",
            "--nprocs", threads, "--omp-nthreads", min(threads, 4), "--mem", memory,
            "--skip-bids-validation", "--stop-on-first-crash", "--notrack", "-w", work,
        ]
        _run(command, folder / "qsiprep.log")
        preprocessed = list(produced.rglob("*desc-preproc_dwi.nii*"))
        reports = list(produced.rglob("*.html"))
        if not preprocessed or not reports:
            raise RuntimeError("QSIPrep completed without a preprocessed DWI and HTML report.")
        (produced / "calmar-selection.json").write_text(json.dumps(provenance, indent=2) + "\n")
        shutil.copy2(folder / "qsiprep.log", produced / "calmar-qsiprep.log")
        _publish(produced, final, "dmri_preproc", "qsiprep", os.environ["CALMAR_EXECUTION_SCRIPT"], overwrite)
    qc = {"png": None, "metrics": {"preprocessed_dwi": len(preprocessed),
                                     "reports": len(reports),
                                     "cross_session_anatomy": provenance["cross_session_anatomy"]},
          "flags": (["cross-session anatomy/lesion mask"] if provenance["cross_session_anatomy"] else []),
          "complete": True}
    _publish_result(output, "dmri_preproc", request, entry, final, started, qc)


def reconstruct(request, output):
    _require_slurm()
    started = time.monotonic()
    entry = _entry(request)
    config = request["config"]
    preprocessed = _final_dir(request, entry, "qsiprep")
    if not preprocessed.is_dir():
        raise FileNotFoundError(f"Run the dmri_preproc stage first: {preprocessed}")
    final = _final_dir(request, entry, "qsirecon")
    overwrite = bool(config.get("DMRI_OVERWRITE", False))
    final.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="qsirecon.attempt.", dir=final.parent) as folder:
        folder = Path(folder)
        produced, work = folder / "produced", folder / "work"
        _, _, label = _subject_parts(entry)
        threads = int(os.environ.get("SLURM_CPUS_PER_TASK", "8"))
        memory = max(1024, int(float(os.environ.get("SLURM_MEM_PER_NODE", "32768")) * 0.9))
        spec = config.get("DMRI_RECON_SPEC", "ss3t_fod_autotrack")
        license_file = Path(config.get("FS_LICENSE") or os.environ.get("FS_LICENSE") or "/home/jovyan/license.txt")
        if not license_file.is_file():
            raise FileNotFoundError(
                "QSIRecon requires a FreeSurfer license; set CONFIG['FS_LICENSE'] or the FS_LICENSE environment variable.")
        command = [
            "qsirecon", preprocessed, produced, "participant", "--participant-label", label,
            "--recon-spec", spec, "--nprocs", threads, "--omp-nthreads", min(threads, 4),
            "--mem", memory, "--fs-license-file", license_file,
            "--stop-on-first-crash", "--notrack", "-w", work,
        ]
        _run(command, folder / "qsirecon.log")
        scalarstats = [*produced.rglob("*scalarstats.csv"), *produced.rglob("*scalarstats.tsv")]
        bundles = [*produced.rglob("*_streamlines.tck.gz"), *produced.rglob("*.tck")]
        reports = list(produced.rglob("*.html"))
        if not scalarstats or not bundles or not reports:
            raise RuntimeError(
                "QSIRecon did not produce all required tractometry, bundle and HTML-report artifacts.")
        shutil.copy2(folder / "qsirecon.log", produced / "calmar-qsirecon.log")
        (produced / "calmar-reconstruction.json").write_text(json.dumps({
            "recon_spec": spec, "scalarstats": [str(path.relative_to(produced)) for path in scalarstats],
            "bundles": len(bundles), "report_count": len(reports),
            "interpretation": "experimental patient-specific tractography; absence is not disconnection",
        }, indent=2) + "\n")
        _publish(produced, final, "dmri_recon", "qsirecon", os.environ["CALMAR_EXECUTION_SCRIPT"], overwrite)
    qc = {"png": None, "metrics": {"scalarstats": len(scalarstats), "bundles": len(bundles),
                                     "reports": len(reports), "recon_spec": spec},
          "flags": ["patient-specific stroke tractography requires visual QC"], "complete": True}
    _publish_result(output, "dmri_recon", request, entry, final, started, qc)


def _bundle_side(name):
    """Extract only a terminal anatomical L/R marker, not tracking direction."""
    cleaned = re.sub(r"[-_](lr|rl)$", "", name, flags=re.IGNORECASE)
    midline = ("corpuscallosum", "anteriorcommissure", "posteriorcommissure", "fornix")
    compact = re.sub(r"[^a-z0-9]", "", cleaned.lower())
    if any(term in compact for term in midline):
        return "bilateral/unspecified"
    # QSIRecon AutoTrack names are commonly concatenated (ExtremeCapsuleL,
    # SuperiorLongitudinalFasciculus1R), so the terminal marker is sufficient.
    match = re.search(r"[a-z0-9]([LR])$", cleaned)
    if match:
        return "left" if match.group(1).lower() == "l" else "right"
    return "bilateral/unspecified"


def _scalar_rows(recon):
    """Read QSIRecon wide bundle scalar tables into CALMaR's narrow contract."""
    sources = [*Path(recon).rglob("*scalarstats.tsv"), *Path(recon).rglob("*scalarstats.csv")]
    values = {}
    used = []
    pattern = re.compile(
        r"^bundle_(?P<bundle>.+?)_(?P<model>dti|tensor)_(?P<scalar>fa|md)_(?P<stat>median|mean)$",
        re.IGNORECASE)
    for source in sources:
        frame = pd.read_csv(source, sep="\t" if source.suffix == ".tsv" else ",")
        if frame.empty:
            continue
        if len(frame) != 1:
            raise RuntimeError(f"Expected one participant row in QSIRecon scalar table: {source}")
        matched = False
        for column in frame.columns:
            match = pattern.match(str(column))
            if not match:
                continue
            matched = True
            key = match.group("bundle")
            scalar_key = (match.group("scalar").lower(), match.group("stat").lower())
            existing = values.setdefault(key, {})
            if scalar_key in existing:
                raise RuntimeError(
                    f"Duplicate QSIRecon value for {key} {scalar_key} across scalar-stat tables; "
                    "select one reconstruction output explicitly.")
            existing[scalar_key] = frame.iloc[0][column]
        if matched:
            used.append(source)
    rows = []
    for bundle, scalars in sorted(values.items()):
        # The report contract names these fields as medians. Do not silently
        # substitute a mean if a future QSIRecon schema omits the median.
        fa = scalars.get(("fa", "median"))
        md = scalars.get(("md", "median"))
        if pd.isna(fa) and pd.isna(md):
            continue
        rows.append({"tract": bundle, "hemisphere": _bundle_side(bundle),
                     "lesion_overlap_pct": float("nan"),
                     "fa_median": fa, "md_median_mm2_s": md,
                     "valid_voxel_pct": float("nan")})
    if not rows:
        raise RuntimeError(
            "No QSIRecon bundle DTI FA/MD columns matched the expected "
            "bundle_<name>_(DTI|tensor)_(fa|md)_(mean|median) schema.")
    return pd.DataFrame(rows), used


def normalize_metrics(request, output):
    _require_slurm()
    started = time.monotonic()
    entry = _entry(request)
    recon = _final_dir(request, entry, "qsirecon")
    if not recon.is_dir():
        raise FileNotFoundError(f"Run the dmri_recon stage first: {recon}")
    table, sources = _scalar_rows(recon)
    table_path, metadata_path = tractometry_paths(request["dataset"], request["config"], entry)
    metrics_dir = table_path.parent
    metrics_dir.parent.mkdir(parents=True, exist_ok=True)
    overwrite = bool(request["config"].get("DMRI_OVERWRITE", False))
    assessment = entry.get("dmri_assessment") or {}
    metadata = {
        "subject": entry["subject"], "session": entry.get("session"),
        "anatomical_session": entry.get("anatomical_session"),
        "cross_session_anatomy": entry.get("anatomical_session") != entry.get("session"),
        "preprocessor": "QSIPrep 26.1.1 + QSIRecon 26.0.1",
        "recon_spec": request["config"].get("DMRI_RECON_SPEC", "ss3t_fod_autotrack"),
        "n_directions": assessment.get("n_directions"), "shells": assessment.get("shells"),
        "qc_status": "requires_visual_review",
        "warnings": list(dict.fromkeys([
            *(assessment.get("warnings") or []),
            *(["diffusion and anatomical lesion mask come from different sessions"]
              if entry.get("anatomical_session") != entry.get("session") else []),
            "lesion-to-bundle overlap and valid-voxel coverage are not yet calculated",
            "patient-specific bundle absence is not evidence of anatomical disconnection",
        ])),
        "source_scalarstats": [str(path) for path in sources],
    }
    with tempfile.TemporaryDirectory(prefix="dmri_metrics.attempt.", dir=metrics_dir.parent) as folder:
        folder = Path(folder)
        temporary_metrics = folder / "metrics"
        temporary_metrics.mkdir()
        temporary_table = temporary_metrics / table_path.name
        temporary_metadata = temporary_metrics / metadata_path.name
        table.to_csv(temporary_table, sep="\t", index=False, na_rep="n/a")
        temporary_metadata.write_text(json.dumps(metadata, indent=2, default=str) + "\n")
        _publish(temporary_metrics, metrics_dir, "dmri_metrics", os.environ.get("CALMAR_PYTHON", "python"),
                 os.environ["CALMAR_EXECUTION_SCRIPT"], overwrite)
    qc = {"png": None, "metrics": {"tracts": len(table), "source_tables": len(sources)},
          "flags": metadata["warnings"], "complete": True}
    _publish_result(output, "dmri_metrics", request, entry, metrics_dir, started, qc)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("dmri_preproc", "dmri_recon", "dmri_metrics"))
    parser.add_argument("request", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    request = json.loads(args.request.read_text(encoding="utf-8"))
    if os.environ.get("CALMAR_DMRI_RECON_SPEC"):
        request["config"]["DMRI_RECON_SPEC"] = os.environ["CALMAR_DMRI_RECON_SPEC"]
    if args.output.exists():
        raise FileExistsError(args.output)
    {"dmri_preproc": preprocess, "dmri_recon": reconstruct,
     "dmri_metrics": normalize_metrics}[args.stage](request, args.output)


if __name__ == "__main__":
    main()
