"""Scheduler-only QSIPrep plus QSIRecon-or-DIPY direct-dMRI analysis."""

from __future__ import annotations

import argparse
import errno
import fcntl
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time
import tomllib
from uuid import uuid4

import pandas as pd

from .acquisition import ensure_nifti_content
from .diffusion import (DMRI_SUBDIR, bvalue_shells, dmri_method,
                        load_tensor_metrics, load_tractometry, tensor_metrics_paths,
                        tractometry_paths)
from .study import Study


def _require_slurm():
    if not os.environ.get("SLURM_JOB_ID"):
        raise RuntimeError("Diffusion tract-microstructure processing must be submitted with its retained Slurm script.")


def _entry(request):
    entries = request.get("entries") or []
    if len(entries) != 1:
        raise ValueError("A diffusion tract-microstructure job requires exactly one participant entry.")
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
            f"Diffusion tract-microstructure processing requires a native-T1 lesion mask from {source!r}; "
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


def _run(command, log, failure_dir=None):
    log = Path(log)
    with log.open("w", encoding="utf-8") as stream:
        completed = subprocess.run([str(value) for value in command], stdout=stream,
                                   stderr=subprocess.STDOUT, text=True, check=False)
    if completed.returncode:
        lines = log.read_text(encoding="utf-8", errors="replace").splitlines()
        retained = ""
        if failure_dir is not None:
            try:
                failure_dir = Path(failure_dir)
                if failure_dir.exists():
                    failure_dir = failure_dir.with_name(failure_dir.name + "." + uuid4().hex)
                failure_dir.mkdir(parents=True, exist_ok=False)
                shutil.copy2(log, failure_dir / log.name)
                crashes = (path for path in log.parent.rglob("crash-*") if path.is_file())
                for index, crash in enumerate(crashes, 1):
                    shutil.copy2(crash, failure_dir / f"{index:02d}-{crash.name}")
                retained = f" Full diagnostics retained in {failure_dir}."
            except OSError as exc:
                retained = f" Diagnostics could not be retained: {exc}."
        tail = "\n".join(lines[-40:]) or "(the tool wrote no diagnostic output)"
        raise RuntimeError(
            f"{Path(str(command[0])).name} failed with exit status {completed.returncode}. "
            f"Last {min(len(lines), 40)} log lines:{retained}\n{tail}")


def _retain_contract_failure(folder, failure_dir, missing, counts):
    """Atomically keep a successful tool attempt whose derivative contract is unmet."""
    folder, requested = Path(folder), Path(failure_dir)
    candidate = requested
    while True:
        if candidate.exists():
            candidate = requested.with_name(requested.name + "." + uuid4().hex)
            continue
        try:
            # Rename the whole attempt before diagnostics: even an inventory or
            # disk-space error must not let TemporaryDirectory delete the output.
            os.rename(folder, candidate)
            break
        except OSError as exc:
            if exc.errno in {errno.EEXIST, errno.ENOTEMPTY}:
                candidate = requested.with_name(requested.name + "." + uuid4().hex)
                continue
            raise
    diagnostic_error = None
    produced = candidate / "produced"
    try:
        files = sorted((
            {"path": str(path.relative_to(produced)), "bytes": path.stat().st_size}
            for path in produced.rglob("*") if path.is_file()
        ), key=lambda item: item["path"])
        (candidate / "artifact-inventory.json").write_text(json.dumps({
            "missing_required_artifacts": list(missing),
            "matched_artifact_counts": dict(counts),
            "files": files,
        }, indent=2) + "\n")
    except OSError as exc:
        diagnostic_error = f"; artifact inventory could not be written: {exc}"
    return candidate, diagnostic_error


def _retain_publish_failure(folder, failure_dir, error, counts):
    """Reassemble a publisher failure and retain the complete tool attempt."""
    folder = Path(folder)
    failed = getattr(error, "calmar_failed_path", None)
    produced = folder / "produced"
    if failed is not None and Path(failed).exists() and not produced.exists():
        os.replace(failed, produced)
        failed_sidecar = Path(str(failed) + ".prov.json")
        if failed_sidecar.exists():
            os.replace(failed_sidecar, folder / "failed-publication.prov.json")
    return _retain_contract_failure(
        folder, failure_dir, ["successful provenance publication"], counts)


def _hmc_method(config):
    method = config.get("DMRI_HMC_METHOD", "tortoise")
    if method not in {"tortoise", "eddy", "shoreline"}:
        raise ValueError("DMRI_HMC_METHOD must be tortoise, eddy or shoreline.")
    return method


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
        except Exception as exc:
            # Keep a failed publisher artifact recoverable even on a first
            # run, then restore any replaced result while the output lock
            # excludes CALMaR races.
            failed = final.with_name(final.name + ".publish-failed." +
                                     os.environ.get("SLURM_JOB_ID", "unknown") + "." + uuid4().hex)
            if final.exists():
                os.replace(final, failed)
                sidecar = Path(str(final) + ".prov.json")
                if sidecar.exists():
                    os.replace(sidecar, Path(str(failed) + ".prov.json"))
            elif Path(temporary).exists():
                os.replace(temporary, failed)
            for old, backup in reversed(preserved):
                os.replace(backup, old)
            try:
                exc.calmar_failed_path = failed if failed.exists() else None
            except (AttributeError, TypeError):
                pass
            if failed.exists() and hasattr(exc, "add_note"):
                exc.add_note(f"Failed publication artifact retained in {failed}.")
            raise


def _publish_result(output, stage, request, entry, derivative, started, qc, *,
                    status="computed", tracked_files=()):
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=output.name + ".attempt.", dir=output.parent) as folder:
        result = Path(folder) / "result"
        result.mkdir()
        listed = {"path": str(derivative), "status": status}
        tracked = {str(Path(path)): str(Path(path)) for path in tracked_files}
        if tracked:
            # The scheduler stamp code uses these relative names to detect any
            # in-place replacement of a published derivative member.
            listed["images"] = tracked
        summary = {
            "stage": stage, "request": request, "job": os.environ["SLURM_JOB_ID"],
            "results": [{"subject": entry["subject"], "session": entry.get("session"),
                         "seconds": time.monotonic() - started,
                         "outputs": [listed],
                         "qc": qc}], "qc_version": 7,
        }
        (result / "summary.json").write_text(json.dumps(summary, indent=2, default=str) + "\n")
        output_id = stage
        if dmri_method(request.get("config", {})) == "dipy_dti":
            output_id = {
                "dmri_recon": "dipy_dti_recon",
                "dmri_metrics": "dipy_dti_metrics",
            }.get(stage, stage)
        _publish(result, output, output_id, os.environ.get("CALMAR_PYTHON", "python"),
                 os.environ["CALMAR_EXECUTION_SCRIPT"])


def _reconstruction_artifacts(produced):
    """Return the QSIRecon artifacts required by CALMaR's direct-dMRI route.

    QSIRecon 26.0.1's SS3T AutoTrack workflow writes a long
    ``*_bundlestats.csv`` table.  Some other reconstruction specs and older
    releases write wide ``*scalarstats`` tables instead, so both documented
    layouts are accepted while retaining the exact source files in provenance.
    """
    produced = Path(produced)
    tables = [
        *produced.rglob("*scalarstats.csv"), *produced.rglob("*scalarstats.tsv"),
        *produced.rglob("*bundlestats.csv"), *produced.rglob("*bundlestats.tsv"),
    ]
    bundles = [*produced.rglob("*_streamlines.tck.gz"), *produced.rglob("*.tck")]
    reports = list(produced.rglob("*.html"))
    groups = {
        "tractometry statistics": tables,
        "bundle streamlines": bundles,
        "HTML report": reports,
    }
    return tables, bundles, reports, groups


def _write_reconstruction_record(produced, spec, tables, bundles, reports, **extra):
    record = {
        "recon_spec": spec,
        "tractometry_tables": [str(path.relative_to(produced)) for path in tables],
        # Retain the old key for consumers of derivatives published before the
        # long QSIRecon bundle-statistics layout was observed in production.
        "scalarstats": [str(path.relative_to(produced)) for path in tables
                        if "scalarstats" in path.name],
        "bundles": len(bundles), "report_count": len(reports),
        "interpretation": "experimental patient-specific tractography; absence is not disconnection",
        **extra,
    }
    (Path(produced) / "calmar-reconstruction.json").write_text(
        json.dumps(record, indent=2) + "\n")


def _generated_versions(derivative):
    """Read tool versions recorded by the derivative that was actually produced."""
    versions = {}
    for description in Path(derivative).rglob("dataset_description.json"):
        try:
            generated = json.loads(description.read_text(encoding="utf-8")).get("GeneratedBy", [])
        except (OSError, json.JSONDecodeError, AttributeError):
            continue
        for item in generated:
            if not isinstance(item, dict):
                continue
            name = str(item.get("Name", "")).lower()
            version = item.get("Version")
            if name in {"qsiprep", "qsirecon"} and version:
                previous = versions.setdefault(name, str(version))
                if previous != str(version):
                    raise RuntimeError(
                        f"Derivative records conflicting {name} versions: {previous} and {version}.")
    return versions


def _observed_reconstruction(produced, entry):
    """Verify identity, method and version from QSIRecon's own retained records."""
    produced = Path(produced)
    subject, session, label = _subject_parts(entry)
    configs = list(produced.glob(f"{subject}/log/*/qsirecon.toml"))
    if not configs:
        raise RuntimeError(f"Retained QSIRecon attempt has no {subject}/log/*/qsirecon.toml.")
    observed = set()
    for config_path in configs:
        try:
            config = tomllib.loads(config_path.read_text(encoding="utf-8"))
            spec = config["workflow"]["recon_spec"]
            version = config["environment"]["version"]
            participants = tuple(config["execution"]["participant_label"])
            processing = tuple(config["execution"].get("processing_list", ()))
        except (OSError, tomllib.TOMLDecodeError, KeyError, TypeError) as exc:
            raise RuntimeError(f"Could not read retained QSIRecon provenance: {config_path}: {exc}") from exc
        if label not in participants:
            raise RuntimeError(
                f"Retained QSIRecon attempt is for {participants}, not participant {label}.")
        if not processing:
            raise RuntimeError("Retained QSIRecon provenance has no processing_list identity.")
        session_token = f"/{session}/" if session else f"/{subject}/"
        if not any(session_token in f"/{item}" for item in processing):
            raise RuntimeError(
                f"Retained QSIRecon attempt does not record requested session {session or '(none)'}.")
        if session is None and any(re.search(r"/ses-[^/]+/", f"/{item}") for item in processing):
            raise RuntimeError(
                "Retained QSIRecon attempt is sessioned, but the request has no session.")
        observed.add((str(spec), str(version)))
    if len(observed) != 1:
        raise RuntimeError(f"Retained QSIRecon attempt has conflicting run provenance: {sorted(observed)}")
    spec, version = observed.pop()
    versions = _generated_versions(produced)
    if versions.get("qsirecon") and versions["qsirecon"] != version:
        raise RuntimeError(
            f"QSIRecon TOML records {version}, but dataset metadata records {versions['qsirecon']}.")
    subject_dirs = list(produced.glob(f"derivatives/*/{subject}"))
    matching_dirs = ([path / session for path in subject_dirs if (path / session).is_dir()]
                     if session else [path for path in subject_dirs
                                      if not any(path.glob("ses-*"))])
    if not matching_dirs:
        raise RuntimeError(
            f"Retained QSIRecon attempt has no derivative directory for {subject} {session or ''}.")
    return {"recon_spec": spec, "qsirecon_version": version,
            "qsiprep_version": versions.get("qsiprep")}


def preprocess(request, output):
    _require_slurm()
    started = time.monotonic()
    entry = _entry(request)
    config = request["config"]
    final = _final_dir(request, entry, "qsiprep")
    overwrite = bool(config.get("DMRI_OVERWRITE", config.get("OVERWRITE", False)))
    hmc_method = _hmc_method(config)
    final.parent.mkdir(parents=True, exist_ok=True)
    if final.exists() and not overwrite:
        raise FileExistsError(
            f"QSIPrep derivative already exists and is preserved: {final}. Reuse its scheduler receipt when "
            "available, or set DMRI_OVERWRITE=True to preserve it as a backup and recompute.")
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
            "--anat-modality", "T1w", "--hmc-method", hmc_method,
            "--nprocs", threads, "--omp-nthreads", min(threads, 4), "--mem", memory,
            "--skip-bids-validation", "--stop-on-first-crash", "--notrack", "-w", work,
        ]
        failure_dir = final.parent / f"qsiprep.failed.{os.environ['SLURM_JOB_ID']}"
        _run(command, folder / "qsiprep.log", failure_dir=failure_dir)
        preprocessed = list(produced.rglob("*desc-preproc_dwi.nii*"))
        reports = list(produced.rglob("*.html"))
        artifact_groups = {"preprocessed DWI": preprocessed, "HTML report": reports}
        missing = [name for name, paths in artifact_groups.items() if not paths]
        if missing:
            retained, diagnostic_error = _retain_contract_failure(
                folder, failure_dir, missing,
                {name: len(paths) for name, paths in artifact_groups.items()})
            raise RuntimeError(
                f"QSIPrep completed but CALMaR could not find the required {', '.join(missing)}. "
                f"The complete attempt was retained in {retained}{diagnostic_error or ''}.")
        try:
            provenance["hmc_method"] = hmc_method
            (produced / "calmar-selection.json").write_text(json.dumps(provenance, indent=2) + "\n")
            shutil.copy2(folder / "qsiprep.log", produced / "calmar-qsiprep.log")
        except Exception as exc:
            retained, diagnostic_error = _retain_contract_failure(
                folder, failure_dir, ["complete CALMaR selection provenance"],
                {name: len(paths) for name, paths in artifact_groups.items()})
            raise RuntimeError(
                f"QSIPrep artifacts are complete, but CALMaR could not finalize their provenance: {exc}. "
                f"The complete attempt was retained in {retained}{diagnostic_error or ''}.") from exc
        try:
            _publish(produced, final, "dmri_preproc", "qsiprep",
                     os.environ["CALMAR_EXECUTION_SCRIPT"], overwrite)
        except Exception as exc:
            retained, diagnostic_error = _retain_publish_failure(
                folder, failure_dir, exc,
                {name: len(paths) for name, paths in artifact_groups.items()})
            raise RuntimeError(
                f"QSIPrep completed, but provenance publication failed: {exc}. "
                f"The complete attempt was retained in {retained}{diagnostic_error or ''}.") from exc
    qc = {"png": None, "metrics": {"preprocessed_dwi": len(preprocessed),
                                     "reports": len(reports),
                                     "hmc_method": hmc_method,
                                     "cross_session_anatomy": provenance["cross_session_anatomy"]},
          "flags": (["cross-session anatomy/lesion mask"] if provenance["cross_session_anatomy"] else []),
          "complete": True}
    _publish_result(output, "dmri_preproc", request, entry, final, started, qc)


def _dipy_inputs(request, entry):
    """Resolve one QSIPrep-preprocessed series and its matching gradients/mask."""
    preprocessed = _final_dir(request, entry, "qsiprep")
    dwi_files = sorted(preprocessed.rglob("*desc-preproc_dwi.nii.gz"))
    if len(dwi_files) != 1:
        raise RuntimeError(
            f"DIPY DTI requires exactly one QSIPrep preprocessed DWI; found {len(dwi_files)} in {preprocessed}.")
    dwi = dwi_files[0]
    base = Path(str(dwi).removesuffix(".nii.gz"))
    bval, bvec = Path(str(base) + ".bval"), Path(str(base) + ".bvec")
    mask = dwi.with_name(dwi.name.replace("_desc-preproc_dwi.nii.gz", "_desc-brain_mask.nii.gz"))
    missing = [path for path in (bval, bvec, mask) if not path.is_file()]
    if missing:
        raise FileNotFoundError("QSIPrep DIPY inputs are incomplete: " + ", ".join(map(str, missing)))
    return dwi, bval, bvec, mask


def _dipy_version():
    completed = subprocess.run(
        ["dipy_fit_dti", "--version"], capture_output=True, text=True, check=True)
    match = re.search(r"\bDIPY\s+([0-9][^\s]*)", completed.stdout + completed.stderr)
    if not match:
        raise RuntimeError("dipy_fit_dti did not report a parseable version")
    version = match.group(1)
    expected = os.environ.get("CALMAR_DIPY_VERSION", "1.12.1")
    if version != expected:
        raise RuntimeError(f"DIPY version {version} is installed; CALMaR requires the pinned {expected}")
    return version


def _dipy_acquisition_shells(bval_path):
    """Return rounded nonzero shells and reject unvalidated multi-shell DTI."""
    import numpy as np
    bvals = np.loadtxt(bval_path, ndmin=1)
    shells = [value for value in bvalue_shells(bvals) if value >= 100]
    if len(shells) != 1:
        shown = "/".join(map(str, shells)) or "none"
        raise RuntimeError(
            "DIPY DTI is validated only for a single nonzero shell; "
            f"found b={shown}. Select QSIRecon or a single-shell diffusion session.")
    return shells


def reconstruct_dipy(request, output):
    """Fit a single-shell-compatible DIPY tensor model after shared QSIPrep."""
    _require_slurm()
    started = time.monotonic()
    entry = _entry(request)
    config = request["config"]
    dwi, bval, bvec, mask = _dipy_inputs(request, entry)
    final = _final_dir(request, entry, "dipy_dti")
    overwrite = bool(config.get("DMRI_OVERWRITE", config.get("OVERWRITE", False)))
    if final.exists() and not overwrite:
        raise FileExistsError(
            f"DIPY DTI derivative already exists and is preserved: {final}. Reuse its scheduler receipt "
            "or select Rerun from the start.")
    final.parent.mkdir(parents=True, exist_ok=True)
    version = _dipy_version()
    fitted_shells = _dipy_acquisition_shells(bval)
    with tempfile.TemporaryDirectory(prefix="dipy_dti.attempt.", dir=final.parent) as folder:
        folder = Path(folder)
        produced = folder / "produced"
        produced.mkdir()
        subject, session, _ = _subject_parts(entry)
        stem = "_".join(filter(None, [subject, session]))
        names = {
            "FA": f"{stem}_space-ACPC_model-DIPYDTI_param-FA_dwimap.nii.gz",
            "MD": f"{stem}_space-ACPC_model-DIPYDTI_param-MD_dwimap.nii.gz",
            "AD": f"{stem}_space-ACPC_model-DIPYDTI_param-AD_dwimap.nii.gz",
            "RD": f"{stem}_space-ACPC_model-DIPYDTI_param-RD_dwimap.nii.gz",
        }
        command = [
            "dipy_fit_dti", dwi, bval, bvec, mask,
            "--fit_method", "WLS", "--b0_threshold", "100",
            "--save_metrics", "fa", "md", "ad", "rd",
            "--out_dir", produced,
            "--out_fa", names["FA"], "--out_md", names["MD"],
            "--out_ad", names["AD"], "--out_rd", names["RD"],
        ]
        failure_dir = final.parent / f"dipy_dti.failed.{os.environ['SLURM_JOB_ID']}"
        _run(command, folder / "dipy-dti.log", failure_dir=failure_dir)
        try:
            import nibabel as nib
            reference = nib.load(mask)
            for metric, name in names.items():
                path = produced / name
                if not path.is_file():
                    raise RuntimeError(f"DIPY did not produce its {metric} map: {path}")
                image = nib.load(path)
                if (image.shape[:3] != reference.shape[:3] or
                        not _affines_close(image.affine, reference.affine)):
                    raise RuntimeError(f"DIPY {metric} map does not match the QSIPrep brain-mask grid")
            # The workflow writes a PAM peaks object even when only tensor
            # scalars were requested. It is outside this DTI contract and adds
            # about 25 MB per participant, so remove it only after validating
            # the requested maps.
            for unrequested in produced.glob("*.pam5"):
                unrequested.unlink()
            record = {
                "method": "dipy_dti", "fit_method": "WLS", "dipy_version": version,
                "b0_threshold": 100, "fitted_shells": fitted_shells,
                "source_preprocessed_dwi": str(dwi),
                "source_bval": str(bval), "source_bvec": str(bvec), "source_mask": str(mask),
                "maps": names,
                "interpretation": "voxelwise tensor model; not bundle tractometry or evidence of disconnection",
            }
            (produced / "calmar-dipy-dti.json").write_text(json.dumps(record, indent=2) + "\n")
            shutil.copy2(folder / "dipy-dti.log", produced / "calmar-dipy-dti.log")
        except Exception as exc:
            retained, diagnostic_error = _retain_contract_failure(
                folder, failure_dir, ["four same-grid DIPY tensor maps and provenance"],
                {"tensor maps": len(list(produced.glob("*param-*_dwimap.nii.gz")))})
            raise RuntimeError(
                f"DIPY completed, but its derivative contract failed: {exc}. "
                f"The complete attempt was retained in {retained}{diagnostic_error or ''}.") from exc
        try:
            _publish(produced, final, "dipy_dti_recon", "dipy_fit_dti",
                     os.environ["CALMAR_EXECUTION_SCRIPT"], overwrite)
        except Exception as exc:
            retained, diagnostic_error = _retain_publish_failure(
                folder, failure_dir, exc, {"tensor maps": len(names)})
            raise RuntimeError(
                f"DIPY completed, but provenance publication failed: {exc}. "
                f"The complete attempt was retained in {retained}{diagnostic_error or ''}.") from exc
    qc = {
        "png": None,
        "metrics": {"method": "DIPY DTI", "fit": "WLS", "maps": 4,
                    "dipy_version": version, "fitted_shells": fitted_shells},
        "flags": ["voxelwise tensor maps require visual QC; this method does not reconstruct bundles"],
        "complete": True,
    }
    _publish_result(output, "dmri_recon", request, entry, final, started, qc,
                    tracked_files=names.values())


def _affines_close(first, second):
    import numpy as np
    return bool(np.allclose(first, second, rtol=1e-5, atol=1e-4))


def _dipy_qc_png(dwi_path, bval_path, mask_path, maps, output):
    """Make a compact FA/MD montage from the exact published-grid inputs."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import nibabel as nib
    import numpy as np

    mask = np.asanyarray(nib.load(mask_path).dataobj) > 0
    bvals = np.loadtxt(bval_path, ndmin=1)
    b0 = np.flatnonzero(bvals < 100)
    if not len(b0):
        raise RuntimeError("DIPY QC could not find a b=0 volume")
    dwi = nib.load(dwi_path)
    background = np.asarray(dwi.dataobj[..., int(b0[0])], dtype=np.float32)
    fa = np.asarray(nib.load(maps["FA"]).dataobj, dtype=np.float32)
    md = np.asarray(nib.load(maps["MD"]).dataobj, dtype=np.float32)
    z_used = np.where(mask)[2]
    if not len(z_used):
        raise RuntimeError("QSIPrep brain mask is empty")
    slices = np.quantile(z_used, [0.3, 0.5, 0.7]).round().astype(int)
    vmax = float(np.nanpercentile(background[mask], 99))
    fig, axes = plt.subplots(2, 3, figsize=(10.5, 6.2), constrained_layout=True)
    for column, z in enumerate(slices):
        bg = np.rot90(background[:, :, z])
        valid = np.rot90(mask[:, :, z])
        axes[0, column].imshow(bg, cmap="gray", vmin=0, vmax=vmax)
        axes[0, column].imshow(np.ma.masked_where(~valid, np.rot90(fa[:, :, z])),
                               cmap="viridis", vmin=0, vmax=1, alpha=.78)
        axes[0, column].set_title(f"FA · axial slice {z}")
        axes[1, column].imshow(bg, cmap="gray", vmin=0, vmax=vmax)
        axes[1, column].imshow(np.ma.masked_where(~valid, np.rot90(md[:, :, z])),
                               cmap="magma", vmin=0, vmax=.002, alpha=.78)
        axes[1, column].set_title(f"MD (mm²/s) · axial slice {z}")
        for row in range(2):
            axes[row, column].axis("off")
    fig.suptitle("DIPY weighted-least-squares tensor fit · review alignment and artefacts")
    fig.savefig(output, dpi=140, facecolor="white")
    plt.close(fig)
    from PIL import Image
    try:
        with Image.open(output) as checked_image:
            if checked_image.format != "PNG":
                raise RuntimeError(f"DIPY QC has format {checked_image.format!r}, expected PNG")
            checked_image.verify()
    except (OSError, SyntaxError) as exc:
        raise RuntimeError(f"DIPY QC is not a readable PNG: {exc}") from exc
    # Neurodesk provides ImageMagick and uses it as an independent format
    # check. Portable test runners may not, so Pillow remains the required
    # validation and identify is an additional check when installed.
    identify = shutil.which("identify")
    if identify:
        checked = subprocess.run(
            [identify, "-format", "%m %w %h", str(output)],
            capture_output=True, text=True, check=True)
        if not checked.stdout.startswith("PNG "):
            raise RuntimeError(f"DIPY QC is not a valid PNG: {checked.stdout!r}")


def normalize_dipy_metrics(request, output):
    """Validate DIPY maps and publish explicit whole-brain tensor summaries."""
    _require_slurm()
    started = time.monotonic()
    entry = _entry(request)
    recon = _final_dir(request, entry, "dipy_dti")
    record_path = recon / "calmar-dipy-dti.json"
    if not record_path.is_file():
        raise FileNotFoundError(f"Run the DIPY DTI reconstruction first: {record_path}")
    record = json.loads(record_path.read_text(encoding="utf-8"))
    if record.get("method") != "dipy_dti" or record.get("fit_method") != "WLS":
        raise RuntimeError("Published DIPY reconstruction does not record the expected WLS tensor method")
    import nibabel as nib
    import numpy as np
    mask_path = Path(record["source_mask"])
    mask = np.asanyarray(nib.load(mask_path).dataobj) > 0
    rows, warnings, maps = [], [], {}
    ranges = {"FA": (0., 1., "unitless"), "MD": (0., .01, "mm²/s"),
              "AD": (0., .01, "mm²/s"), "RD": (0., .01, "mm²/s")}
    for metric, name in record["maps"].items():
        path = recon / name
        maps[metric] = path
        values = np.asarray(nib.load(path).dataobj, dtype=np.float64)[mask]
        lower, upper, units = ranges[metric]
        valid = np.isfinite(values) & (values >= lower) & (values <= upper)
        if not valid.any():
            raise RuntimeError(f"DIPY {metric} map has no finite physical values inside the brain mask")
        fraction = float(valid.mean() * 100.)
        if fraction < 98.:
            warnings.append(f"{metric}: only {fraction:.1f}% of brain-mask voxels are in the physical range")
        measured = values[valid]
        rows.append({
            "metric": metric, "median": float(np.median(measured)),
            "p05": float(np.percentile(measured, 5)), "p95": float(np.percentile(measured, 95)),
            "valid_voxels": int(valid.sum()), "valid_brain_pct": fraction,
            "physical_units": units,
        })
    table = pd.DataFrame(rows).sort_values("metric", kind="stable")
    table_path, metadata_path = tensor_metrics_paths(request["dataset"], request["config"], entry)
    metrics_dir = table_path.parent
    metrics_dir.parent.mkdir(parents=True, exist_ok=True)
    overwrite = bool(request["config"].get(
        "DMRI_OVERWRITE", request["config"].get("OVERWRITE", False)))
    assessment = entry.get("dmri_assessment") or {}
    metadata = {
        "subject": entry["subject"], "session": entry.get("session"),
        "anatomical_session": entry.get("anatomical_session"),
        "method": "dipy_dti", "fit_method": "WLS",
        "software": f"DIPY {record['dipy_version']}",
        "preprocessor": "QSIPrep-preprocessed DWI", "b0_threshold": record["b0_threshold"],
        "n_directions": assessment.get("n_directions"),
        "source_shells": assessment.get("shells"),
        "fitted_shells": record.get("fitted_shells"),
        "qc_status": "requires_visual_review",
        "warnings": [
            *warnings,
            "whole-brain tensor summaries are descriptive and are not bundle tractometry",
            "stroke, crossing fibres and residual distortion can bias DTI measures",
        ],
        "source_maps": {key: str(value) for key, value in maps.items()},
    }
    with tempfile.TemporaryDirectory(prefix="dipy_metrics.attempt.", dir=metrics_dir.parent) as folder:
        temporary = Path(folder) / "dipy_metrics"
        temporary.mkdir()
        temporary_table = temporary / table_path.name
        temporary_metadata = temporary / metadata_path.name
        table.to_csv(temporary_table, sep="\t", index=False)
        load_tensor_metrics(temporary_table)
        temporary_metadata.write_text(json.dumps(metadata, indent=2, default=str) + "\n")
        qc_name = table_path.name.replace("_metrics.tsv", "_qc.png")
        _dipy_qc_png(record["source_preprocessed_dwi"], record["source_bval"],
                     mask_path, maps, temporary / qc_name)
        _publish(temporary, metrics_dir, "dipy_dti_metrics",
                 os.environ.get("CALMAR_PYTHON", "python"),
                 os.environ["CALMAR_EXECUTION_SCRIPT"], overwrite)
    qc_path = metrics_dir / qc_name
    qc = {
        "png": str(qc_path),
        "metrics": {row["metric"]: row["median"] for row in rows},
        "flags": metadata["warnings"], "complete": True,
    }
    _publish_result(output, "dmri_metrics", request, entry, metrics_dir, started, qc,
                    tracked_files=(table_path.name, metadata_path.name, qc_name))


def reconstruct(request, output):
    _require_slurm()
    if dmri_method(request["config"]) == "dipy_dti":
        return reconstruct_dipy(request, output)
    started = time.monotonic()
    entry = _entry(request)
    config = request["config"]
    preprocessed = _final_dir(request, entry, "qsiprep")
    if not preprocessed.is_dir():
        raise FileNotFoundError(f"Run the dmri_preproc stage first: {preprocessed}")
    final = _final_dir(request, entry, "qsirecon")
    overwrite = bool(config.get("DMRI_OVERWRITE", config.get("OVERWRITE", False)))
    final.parent.mkdir(parents=True, exist_ok=True)
    if final.exists() and not overwrite:
        raise FileExistsError(
            f"QSIRecon derivative already exists and is preserved: {final}. Reuse its scheduler receipt when "
            "available, or set DMRI_OVERWRITE=True to preserve it as a backup and recompute.")
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
        failure_dir = final.parent / f"qsirecon.failed.{os.environ['SLURM_JOB_ID']}"
        _run(command, folder / "qsirecon.log", failure_dir=failure_dir)
        tables, bundles, reports, artifact_groups = _reconstruction_artifacts(produced)
        missing = [name for name, paths in artifact_groups.items() if not paths]
        if missing:
            retained, diagnostic_error = _retain_contract_failure(
                folder, failure_dir, missing,
                {name: len(paths) for name, paths in artifact_groups.items()})
            raise RuntimeError(
                f"QSIRecon completed but CALMaR could not find the required "
                f"{', '.join(missing)}. The complete attempt was retained in "
                f"{retained}{diagnostic_error or ''}.")
        try:
            shutil.copy2(folder / "qsirecon.log", produced / "calmar-qsirecon.log")
            observed = _observed_reconstruction(produced, entry)
            if observed["recon_spec"] != spec:
                raise RuntimeError(
                    f"QSIRecon recorded recon spec {observed['recon_spec']!r}, expected {spec!r}.")
            _write_reconstruction_record(
                produced, spec, tables, bundles, reports,
                qsirecon_version=observed["qsirecon_version"],
                qsiprep_version=observed.get("qsiprep_version"))
        except Exception as exc:
            retained, diagnostic_error = _retain_contract_failure(
                folder, failure_dir, ["consistent reconstruction provenance"],
                {name: len(paths) for name, paths in artifact_groups.items()})
            raise RuntimeError(
                f"QSIRecon artifacts are complete, but CALMaR could not finalize their provenance: {exc}. "
                f"The complete attempt was retained in {retained}{diagnostic_error or ''}.") from exc
        try:
            _publish(produced, final, "dmri_recon", "qsirecon",
                     os.environ["CALMAR_EXECUTION_SCRIPT"], overwrite)
        except Exception as exc:
            retained, diagnostic_error = _retain_publish_failure(
                folder, failure_dir, exc,
                {name: len(paths) for name, paths in artifact_groups.items()})
            raise RuntimeError(
                f"QSIRecon completed, but provenance publication failed: {exc}. "
                f"The complete attempt was retained in {retained}{diagnostic_error or ''}.") from exc
    qc = {"png": None, "metrics": {"tractometry_tables": len(tables), "bundles": len(bundles),
                                     "reports": len(reports), "recon_spec": spec},
          "flags": ["patient-specific stroke tractography requires visual QC"], "complete": True}
    _publish_result(output, "dmri_recon", request, entry, final, started, qc)


def recover_reconstruction(request, retained, output):
    """Publish a complete retained QSIRecon attempt after a contract correction.

    This never resumes or reruns QSIRecon.  It is deliberately an explicit
    Slurm-only operation whose retained-attempt path is recorded in the
    derivative, so an incomplete or unrelated folder cannot be adopted
    silently by the notebook scheduler.
    """
    _require_slurm()
    started = time.monotonic()
    entry = _entry(request)
    retained = Path(retained).resolve()
    produced = retained / "produced"
    log = retained / "qsirecon.log"
    if not produced.is_dir() or not log.is_file():
        raise FileNotFoundError(
            f"Retained QSIRecon attempt must contain produced/ and qsirecon.log: {retained}")
    expected_parent = _final_dir(request, entry, "qsirecon").parent.resolve()
    if retained.parent != expected_parent:
        raise RuntimeError(
            f"Retained QSIRecon attempt is under {retained.parent}, expected {expected_parent}.")
    match = re.fullmatch(r"qsirecon\.failed\.(\d+)(?:\..+)?", retained.name)
    if not match:
        raise RuntimeError(
            f"Retained QSIRecon folder must be named qsirecon.failed.<job>[.<suffix>]: {retained}")
    source_job = match.group(1)
    tables, bundles, reports, groups = _reconstruction_artifacts(produced)
    missing = [name for name, paths in groups.items() if not paths]
    if missing:
        raise RuntimeError(
            f"Refusing to publish retained QSIRecon attempt; missing {', '.join(missing)}: {retained}")
    config = request["config"]
    final = _final_dir(request, entry, "qsirecon")
    overwrite = bool(config.get("DMRI_OVERWRITE", config.get("OVERWRITE", False)))
    if final.exists() and not overwrite:
        raise FileExistsError(
            f"QSIRecon derivative already exists and is preserved: {final}. Set DMRI_OVERWRITE=True "
            "to preserve it as a backup before recovering this retained attempt.")
    observed = _observed_reconstruction(produced, entry)
    requested_spec = config.get("DMRI_RECON_SPEC")
    if requested_spec and requested_spec != observed["recon_spec"]:
        raise RuntimeError(
            f"Retained QSIRecon used {observed['recon_spec']!r}, but the request records "
            f"{requested_spec!r}.")
    version_check = subprocess.run(
        ["qsirecon", "--version"], capture_output=True, text=True, check=True)
    loaded_version = (version_check.stdout + "\n" + version_check.stderr).strip()
    loaded_versions = set(re.findall(
        r"(?<!\d)(\d+\.\d+\.\d+(?:[A-Za-z0-9.+-]*))", loaded_version))
    if observed["qsirecon_version"] not in loaded_versions:
        raise RuntimeError(
            f"Retained QSIRecon used {observed['qsirecon_version']}, but the recovery environment "
            f"reports {loaded_version!r}.")
    spec = observed["recon_spec"]
    # Publish a hard-linked staging tree so a publisher error never dismantles
    # the retained attempt. All paths are on the same derivative filesystem;
    # _link falls back to a copy only if hard links are unavailable.
    with tempfile.TemporaryDirectory(prefix="qsirecon.recovery.", dir=final.parent) as folder:
        staged = Path(folder) / "produced"
        shutil.copytree(produced, staged, copy_function=_link)
        for generated in (staged / "calmar-qsirecon.log",
                          staged / "calmar-reconstruction.json"):
            # Never overwrite a hard link to the retained attempt.
            generated.unlink(missing_ok=True)
        shutil.copy2(log, staged / "calmar-qsirecon.log")
        staged_tables, staged_bundles, staged_reports, _ = _reconstruction_artifacts(staged)
        _write_reconstruction_record(
            staged, spec, staged_tables, staged_bundles, staged_reports,
            recovered_from=str(retained), compute_job=source_job,
            recovery_job=os.environ["SLURM_JOB_ID"],
            qsirecon_version=observed["qsirecon_version"],
            qsiprep_version=observed.get("qsiprep_version"))
        _publish(staged, final, "dmri_recon", "qsirecon",
                 os.environ["CALMAR_EXECUTION_SCRIPT"], overwrite)
    qc = {
        "png": None,
        "metrics": {"tractometry_tables": len(tables), "bundles": len(bundles),
                    "reports": len(reports), "recon_spec": spec,
                    "compute_job": source_job},
        "flags": [
            f"complete QSIRecon output recovered from compute job {source_job} after a CALMaR contract correction",
            "patient-specific stroke tractography requires visual QC",
        ],
        "complete": True,
    }
    _publish_result(output, "dmri_recon", request, entry, final, started, qc, status="recovered")


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


def _derivative_methods(request, entry):
    """Read method choices from published derivatives, never current defaults."""
    records = []
    for stage, name in (("qsiprep", "calmar-selection.json"),
                        ("qsirecon", "calmar-reconstruction.json")):
        path = _final_dir(request, entry, stage) / name
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Direct-dMRI method provenance is unavailable: {path}: {exc}") from exc
        if not isinstance(record, dict):
            raise RuntimeError(f"Direct-dMRI method provenance is not an object: {path}")
        records.append(record)
    hmc_method = records[0].get("hmc_method")
    if not hmc_method:
        # Compatibility with derivatives published before CALMaR copied this
        # field into calmar-selection.json.  QSIPrep records the effective CLI
        # choice in its retained log, so this remains observed provenance and
        # never falls back to today's configuration default.
        log_path = _final_dir(request, entry, "qsiprep") / "calmar-qsiprep.log"
        try:
            log = log_path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            raise RuntimeError(
                f"Direct-dMRI HMC provenance is unavailable: {log_path}: {exc}") from exc
        match = re.search(r"--hmc-method\s+(tortoise|eddy|shoreline)\b", log)
        if match:
            hmc_method = match.group(1)
    recon_spec = records[1].get("recon_spec")
    if not hmc_method or not recon_spec:
        raise RuntimeError("Published direct-dMRI derivatives do not record hmc_method and recon_spec.")
    return hmc_method, recon_spec


def _derivative_versions(request, entry):
    """Read producing software versions from published derivative metadata."""
    versions = {}
    for stage in ("qsiprep", "qsirecon"):
        for name, version in _generated_versions(_final_dir(request, entry, stage)).items():
            previous = versions.setdefault(name, version)
            if previous != version:
                raise RuntimeError(
                    f"Published derivatives disagree on {name} version: {previous} and {version}.")
    if not {"qsiprep", "qsirecon"}.issubset(versions):
        raise RuntimeError(
            "Published direct-dMRI derivatives do not record both QSIPrep and QSIRecon versions.")
    return versions


def _scalar_rows(recon):
    """Read QSIRecon bundle statistics into CALMaR's narrow contract."""
    recon = Path(recon)
    wide_sources = [*recon.rglob("*scalarstats.tsv"), *recon.rglob("*scalarstats.csv")]
    long_sources = [*recon.rglob("*bundlestats.tsv"), *recon.rglob("*bundlestats.csv")]
    if wide_sources and long_sources:
        raise RuntimeError(
            "QSIRecon output contains both wide scalarstats and long bundlestats tables; "
            "select one reconstruction derivative explicitly.")
    sources = wide_sources or long_sources
    values = {}
    used = []
    md_conversions = []

    def md_scale(values_to_classify, source):
        units = set()
        for raw in values_to_classify:
            if pd.isna(raw) or float(raw) == 0:
                continue
            value = float(raw)
            if 0.05 <= value <= 5:
                units.add("µm²/ms")
            elif 1e-5 <= value <= 0.01:
                units.add("mm²/s")
            else:
                raise RuntimeError(
                    f"QSIRecon MD value {value!r} has ambiguous or implausible units in {source}; "
                    "expected 0.05–5 µm²/ms or 0.00001–0.01 mm²/s.")
        if not units:
            raise RuntimeError(f"QSIRecon MD values are all zero or missing in {source}; units are unknowable.")
        if len(units) != 1:
            raise RuntimeError(f"QSIRecon MD values mix units within one table: {source}.")
        source_units = units.pop()
        scale = 1e-3 if source_units == "µm²/ms" else 1.0
        conversion = {"source": str(source), "source_units": source_units, "scale": scale}
        md_conversions.append(conversion)
        return scale
    pattern = re.compile(
        r"^bundle_(?P<bundle>.+?)_(?P<model>dti|tensor)_(?P<scalar>fa|md)_(?P<stat>median|mean)$",
        re.IGNORECASE)
    for source in sources:
        frame = pd.read_csv(source, sep="\t" if source.suffix == ".tsv" else ",")
        if frame.empty:
            continue
        if {"bundle_name", "dti_fa", "md"}.issubset(frame.columns):
            # DSI Studio's long AutoTrack table reports bundle means. Normalize
            # MD to physical mm²/s after an explicit magnitude/unit check.
            scale = md_scale(frame["md"], source)
            for _, row in frame.iterrows():
                bundle = str(row["bundle_name"])
                if bundle in values:
                    raise RuntimeError(
                        f"Duplicate QSIRecon bundle {bundle} across tractometry tables; "
                        "select one reconstruction output explicitly.")
                md = row["md"] if pd.isna(row["md"]) else float(row["md"]) * scale
                values[bundle] = {
                    ("fa", "mean"): row["dti_fa"],
                    ("md", "mean"): md,
                }
            used.append(source)
            continue
        if len(frame) != 1:
            raise RuntimeError(f"Expected one participant row in QSIRecon scalar table: {source}")
        md_columns = [column for column in frame.columns
                      if (match := pattern.match(str(column)))
                      and match.group("scalar").lower() == "md"]
        scale = md_scale((frame.iloc[0][column] for column in md_columns), source) if md_columns else None
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
            value = frame.iloc[0][column]
            if scalar_key[0] == "md":
                value = value if pd.isna(value) else float(value) * scale
            existing[scalar_key] = value
        if matched:
            used.append(source)
    rows = []
    for bundle, scalars in sorted(values.items()):
        fa_stats = {stat for scalar, stat in scalars if scalar == "fa"}
        md_stats = {stat for scalar, stat in scalars if scalar == "md"}
        common = fa_stats & md_stats
        if fa_stats and md_stats and not common:
            raise RuntimeError(
                f"QSIRecon bundle {bundle} has FA statistics {sorted(fa_stats)} and MD statistics "
                f"{sorted(md_stats)}, with no common summary statistic.")
        available = common or fa_stats or md_stats
        statistic = next((name for name in ("median", "mean") if name in available), None)
        fa = scalars.get(("fa", statistic)) if statistic else None
        md = scalars.get(("md", statistic)) if statistic else None
        if pd.isna(fa) and pd.isna(md):
            continue
        rows.append({"tract": bundle, "hemisphere": _bundle_side(bundle),
                     "lesion_overlap_pct": float("nan"),
                     "fa": fa, "md_mm2_s": md, "summary_statistic": statistic,
                     "valid_voxel_pct": float("nan")})
    if not rows:
        raise RuntimeError(
            "No QSIRecon bundle DTI FA/MD values matched either the long "
            "bundlestats or wide scalarstats schema.")
    table = pd.DataFrame(rows)
    table.attrs["md_unit_conversions"] = md_conversions
    return table, used


def normalize_metrics(request, output):
    _require_slurm()
    if dmri_method(request["config"]) == "dipy_dti":
        return normalize_dipy_metrics(request, output)
    started = time.monotonic()
    entry = _entry(request)
    recon = _final_dir(request, entry, "qsirecon")
    if not recon.is_dir():
        raise FileNotFoundError(f"Run the dmri_recon stage first: {recon}")
    table, sources = _scalar_rows(recon)
    table_path, metadata_path = tractometry_paths(request["dataset"], request["config"], entry)
    metrics_dir = table_path.parent
    metrics_dir.parent.mkdir(parents=True, exist_ok=True)
    overwrite = bool(request["config"].get(
        "DMRI_OVERWRITE", request["config"].get("OVERWRITE", False)))
    assessment = entry.get("dmri_assessment") or {}
    hmc_method, recon_spec = _derivative_methods(request, entry)
    bundle_qc = bool(request["config"].get("DMRI_BUNDLE_QC"))
    if bundle_qc:
        from .bundle_qc import BundleQCUnavailable, SUPPORTED_RECON, measure_bundles, profile_nodes

        nodes = profile_nodes(request["config"])
    versions = _derivative_versions(request, entry)
    metadata = {
        "subject": entry["subject"], "session": entry.get("session"),
        "anatomical_session": entry.get("anatomical_session"),
        "cross_session_anatomy": entry.get("anatomical_session") != entry.get("session"),
        "preprocessor": f"QSIPrep {versions['qsiprep']} + QSIRecon {versions['qsirecon']}",
        "software_versions": versions,
        "hmc_method": hmc_method,
        "recon_spec": recon_spec,
        "n_directions": assessment.get("n_directions"), "shells": assessment.get("shells"),
        "qc_status": "requires_visual_review",
        "warnings": list(dict.fromkeys([
            *(assessment.get("warnings") or []),
            *(["diffusion and anatomical lesion mask come from different sessions"]
              if entry.get("anatomical_session") != entry.get("session") else []),
            *([] if bundle_qc else ["lesion-to-bundle overlap and valid-voxel coverage were not requested"]),
            "patient-specific bundle absence is not evidence of anatomical disconnection",
        ])),
        "source_tractometry_tables": [str(path) for path in sources],
        "md_unit_conversions": table.attrs.get("md_unit_conversions", []),
    }
    with tempfile.TemporaryDirectory(prefix="dmri_metrics.attempt.", dir=metrics_dir.parent) as folder:
        folder = Path(folder)
        temporary_metrics = folder / "metrics"
        temporary_metrics.mkdir()
        temporary_table = temporary_metrics / table_path.name
        temporary_metadata = temporary_metrics / metadata_path.name
        if bundle_qc:
            try:
                if recon_spec not in SUPPORTED_RECON:
                    raise BundleQCUnavailable(f"Bundle lesion QC requires AutoTrack. This run used {recon_spec}.")
                # An unavailable supplement must leave the validated QSIRecon
                # summary untouched and must never publish half-written QC.
                supplemental = folder / "bundle-qc"
                supplemental.mkdir()
                enriched = table.copy()
                metadata["bundle_qc"] = measure_bundles(
                    _final_dir(request, entry, "qsiprep"), recon, enriched, supplemental, nodes)
            except BundleQCUnavailable as exc:
                metadata["bundle_qc"] = {"status": "unavailable", "reason": str(exc)}
            else:
                for artifact in supplemental.iterdir():
                    artifact.rename(temporary_metrics / artifact.name)
                table = enriched
        table.to_csv(temporary_table, sep="\t", index=False, na_rep="n/a")
        # Validate the serialized artifact, not only the in-memory frame, before
        # a scheduler receipt can call it complete.
        load_tractometry(temporary_table)
        temporary_metadata.write_text(json.dumps(metadata, indent=2, default=str) + "\n")
        _publish(temporary_metrics, metrics_dir, "dmri_metrics", os.environ.get("CALMAR_PYTHON", "python"),
                 os.environ["CALMAR_EXECUTION_SCRIPT"], overwrite)
    bundle_metadata = metadata.get("bundle_qc", {})
    png = bundle_metadata.get("qc_png")
    geometry = bundle_metadata.get("sources", {})
    qc_inputs = [str(path) for path in sources]
    if geometry:
        qc_inputs.extend(geometry[key] for key in (
            "native_lesion", "native_t1", "diffusion_reference", "diffusion_brain_mask",
            "fa_map", "md_map", "md_sidecar"))
        qc_inputs.extend(geometry["lesion_transform_chain"])
        qc_inputs.extend(bundle["source"] for bundle in bundle_metadata["bundles"] if "source" in bundle)
    tracked = [table_path, metadata_path]
    tracked.extend(metrics_dir / bundle_metadata[key]
                   for key in ("qc_png", "profile_png", "profile_tsv", "aligned_lesion")
                   if bundle_metadata.get(key))
    qc = {"png": str(metrics_dir / png) if png else None,
          "metrics": {"tracts": len(table), "source_tables": len(sources)},
          "flags": metadata["warnings"], "input_files": qc_inputs, "complete": True}
    if bundle_metadata.get("reason"):
        qc["flags"] = [*qc["flags"], bundle_metadata["reason"]]
    _publish_result(output, "dmri_metrics", request, entry, metrics_dir, started, qc, tracked_files=tracked)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=(
        "dmri_preproc", "dmri_recon", "dmri_recon_recover", "dmri_metrics"))
    parser.add_argument("request", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--retained", type=Path)
    args = parser.parse_args()
    request = json.loads(args.request.read_text(encoding="utf-8"))
    if os.environ.get("CALMAR_DMRI_HMC_METHOD"):
        request["config"]["DMRI_HMC_METHOD"] = os.environ["CALMAR_DMRI_HMC_METHOD"]
    if os.environ.get("CALMAR_DMRI_RECON_SPEC"):
        request["config"]["DMRI_RECON_SPEC"] = os.environ["CALMAR_DMRI_RECON_SPEC"]
    if os.environ.get("CALMAR_DMRI_METHOD"):
        request["config"]["DMRI_METHOD"] = os.environ["CALMAR_DMRI_METHOD"]
    if os.environ.get("CALMAR_DMRI_BUNDLE_QC"):
        request["config"]["DMRI_BUNDLE_QC"] = os.environ["CALMAR_DMRI_BUNDLE_QC"] == "on"
    if os.environ.get("CALMAR_DMRI_PROFILE_NODES"):
        request["config"]["DMRI_PROFILE_NODES"] = int(os.environ["CALMAR_DMRI_PROFILE_NODES"].removeprefix("nodes_"))
    if args.output.exists():
        raise FileExistsError(args.output)
    if args.stage == "dmri_recon_recover":
        if args.retained is None:
            parser.error("dmri_recon_recover requires --retained")
        recover_reconstruction(request, args.retained, args.output)
    else:
        if args.retained is not None:
            parser.error("--retained is only valid with dmri_recon_recover")
        {"dmri_preproc": preprocess, "dmri_recon": reconstruct,
         "dmri_metrics": normalize_metrics}[args.stage](request, args.output)


if __name__ == "__main__":
    main()
