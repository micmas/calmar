"""Bring a site's own MRIs into a local BIDS dataset that the workflow reads.

Images end up as ``<dataset>/sub-<id>/ses-<id>/anat/sub-<id>_ses-<id>_T1w.nii.gz``
(and ``_FLAIR``), or ``dwi/..._dwi.nii.gz`` + ``_adc.nii.gz`` for the acute route,
so participant discovery (:func:`calmar.study.discover_t1w` / ``discover_dwi``)
and every later step need no change. Set ``DATASET_SOURCE = "local"`` and
``LOCAL_DATASET`` to that folder.

* **NIfTI** files are checked (readable, 3-D) and copied; ``.nii`` is gzipped;
  a JSON sidecar beside the file is copied too.
* **DICOM** folders are converted by dcm2niix in a Slurm job
  (``src/analysis_45_dicom_to_nifti.sh``, :mod:`calmar.dicom_import`). Each
  converted series is listed with a guessed role (T1w, FLAIR, DWI, ADC) from its
  series description and image type; the user confirms the roles, then the
  chosen series are imported as NIfTI.

An existing image is never replaced unless ``overwrite=True``; files are
written to a temporary name and renamed into place.
"""
from __future__ import annotations

import gzip
from html import escape
import json
import os
from pathlib import Path
import shutil
import tempfile
from uuid import uuid4

from .participant_data import participant_id

#: Role → (BIDS folder, suffix).
ROLES = {"T1w": ("anat", "T1w"), "FLAIR": ("anat", "FLAIR"), "dwi": ("dwi", "dwi"), "adc": ("dwi", "adc")}
ROLE_LABELS = {"T1w": "T1-weighted", "FLAIR": "FLAIR", "dwi": "DWI (b1000 trace)", "adc": "ADC map"}


def session_id(label):
    """``"1"`` / ``"ses-1"`` → ``"ses-1"``; None or blank → None (no session level)."""
    if label is None or not str(label).strip():
        return None
    import re
    text = str(label).strip()
    text = text[4:] if text.lower().startswith("ses-") else text
    text = re.sub(r"[^A-Za-z0-9]", "", text)
    if not text:
        raise ValueError(f"Not a usable session ID: {label!r}")
    return f"ses-{text}"


def bids_path(dataset, subject, session, role):
    """Where an image of ``role`` goes in the dataset."""
    if role not in ROLES:
        raise ValueError(f"Unknown image role {role!r}; choose one of {list(ROLES)}")
    folder, suffix = ROLES[role]
    sub, ses = participant_id(subject), session_id(session)
    stem = "_".join(filter(None, [sub, ses, suffix]))
    return Path(dataset) / sub / (ses or "") / folder / f"{stem}.nii.gz"


def ensure_dataset_description(dataset):
    """Write a minimal BIDS ``dataset_description.json`` if there is none."""
    path = Path(dataset) / "dataset_description.json"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"Name": Path(dataset).name, "BIDSVersion": "1.9.0",
                                    "DatasetType": "raw",
                                    "GeneratedBy": [{"Name": "CALMaR local import"}]}, indent=2) + "\n")
    return path


def check_image(path):
    """Shape and voxel size of a readable 3-D NIfTI; ValueError otherwise."""
    import nibabel as nib
    try:
        image = nib.load(str(path))
    except Exception as error:
        raise ValueError(f"{path} is not a readable NIfTI image: {error}") from None
    shape = tuple(int(n) for n in image.shape)
    if len(shape) == 4 and shape[3] == 1:
        shape = shape[:3]
    if len(shape) != 3:
        raise ValueError(f"{Path(path).name} has shape {shape}; a 3-D image is needed "
                         "(for diffusion, the b1000 trace image and the ADC map, not the raw 4-D series)")
    return {"shape": shape, "voxel_mm": tuple(round(float(z), 3) for z in image.header.get_zooms()[:3])}


def _sidecar_of(path):
    path = Path(path)
    name = path.name[:-7] if path.name.endswith(".nii.gz") else path.stem
    candidate = path.with_name(name + ".json")
    return candidate if candidate.exists() else None


def import_image(dataset, subject, session, role, source, *, overwrite=False):
    """Copy one NIfTI into the dataset as ``role``; returns the new path.

    Refuses to replace an existing image unless ``overwrite``.
    """
    source = Path(source).expanduser().resolve()
    info = check_image(source)
    target = bids_path(dataset, subject, session, role)
    if target.exists() and not overwrite:
        raise FileExistsError(f"{target} already exists; pass overwrite=True to replace it")
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(f".{target.name}.{uuid4().hex}.tmp")
    try:
        if source.name.endswith(".gz"):
            shutil.copyfile(source, temporary)
        else:
            with open(source, "rb") as raw, gzip.open(temporary, "wb") as packed:
                shutil.copyfileobj(raw, packed)
        os.replace(temporary, target)
    finally:
        temporary.unlink(missing_ok=True)
    sidecar = _sidecar_of(source)
    if sidecar is not None:
        shutil.copyfile(sidecar, target.with_name(target.name[:-7] + ".json"))
    ensure_dataset_description(dataset)
    return {"role": role, "path": target, **info}


def import_images(dataset, subject, session, files, *, overwrite=False):
    """Import ``{role: path}`` for one participant/session; checks the set first.

    A DWI needs its ADC map (and the reverse); at least a T1w or a DWI is needed.
    Nothing is written when a check fails.
    """
    files = {role: path for role, path in files.items() if path}
    if not files:
        raise ValueError("No images given.")
    if ("dwi" in files) != ("adc" in files):
        raise ValueError("The acute (DWI) route needs both the DWI (b1000 trace) and its ADC map.")
    if "T1w" not in files and "dwi" not in files:
        raise ValueError("Give at least a T1w image (chronic route) or a DWI + ADC pair (acute route).")
    for role, path in files.items():
        check_image(Path(path).expanduser())
        target = bids_path(dataset, subject, session, role)
        if target.exists() and not overwrite:
            raise FileExistsError(f"{target} already exists; tick Overwrite to replace it")
    return [import_image(dataset, subject, session, role, path, overwrite=overwrite)
            for role, path in files.items()]


# ── DICOM ────────────────────────────────────────────────────────────────────

def guess_role(series):
    """T1w / FLAIR / dwi / adc from a converted series' metadata, or None."""
    description = " ".join(str(series.get(k) or "") for k in ("SeriesDescription", "ProtocolName")).lower()
    image_type = " ".join(map(str, series.get("ImageType") or [])).upper()
    if "ADC" in image_type or "adc" in description or "apparent diffusion" in description:
        return "adc"
    if "TRACEW" in image_type or "trace" in description or (
            any(k in description for k in ("dwi", "diff", "dw_")) and not series.get("bvec")):
        return "dwi"
    if "flair" in description:
        return "FLAIR"
    if any(k in description for k in ("t1", "mprage", "mp-rage", "spgr", "bravo", "tfl", "fspgr")):
        return "T1w"
    return None


def convert_dicom(dicom_dir, project_dir, *, timeout=3600):
    """Convert a DICOM folder with dcm2niix in Slurm and list its series.

    Returns one dict per converted image: ``nifti`` (path in the job's result
    folder under reports/jobs/), ``json``, ``SeriesDescription``, ``ImageType``,
    ``shape``, ``guess`` (a role or None). Nothing is added to the dataset.
    """
    from .scheduled import _run_payloads
    dicom_dir = Path(dicom_dir).expanduser().resolve()
    if not dicom_dir.is_dir():
        raise ValueError(f"Not a folder: {dicom_dir}")
    # A fresh conversion each time: the request names a new attempt.
    payload = {"dicom_dir": str(dicom_dir), "attempt": uuid4().hex}
    result = _run_payloads("dicom_import", [payload], Path(project_dir), timeout)
    return result.get("value") or []


# ── Notebook panel ───────────────────────────────────────────────────────────

class LocalImportPanel:
    """Import one participant/session: NIfTI paths, or a DICOM folder converted in Slurm."""

    def __init__(self, dataset, project_dir):
        import ipywidgets as w
        self.dataset, self.project = Path(dataset), Path(project_dir)
        style, wide = {"description_width": "170px"}, w.Layout(width="640px", max_width="100%")
        self.subject = w.Text(description="Participant ID:", placeholder="sub-01", style=style)
        self.session = w.Text(description="Session (optional):", placeholder="ses-01", style=style)
        self.paths = {role: w.Text(description=ROLE_LABELS[role] + ":", placeholder="/path/to/image.nii.gz",
                                   style=style, layout=wide) for role in ROLES}
        self.dicom = w.Text(description="DICOM folder:", placeholder="/path/to/dicom/study", style=style,
                            layout=wide)
        self.convert = w.Button(description="Convert DICOM (Slurm)", layout=w.Layout(width="210px"))
        self.series_box = w.VBox()
        self.overwrite = w.Checkbox(description="Overwrite existing images", indent=False)
        self.run = w.Button(description="Import", button_style="primary")
        self.message = w.HTML()
        self.series, self.role_choices = [], []
        self.convert.on_click(lambda _: self.convert_dicom())
        self.run.on_click(lambda _: self.submit())
        self.widget = w.VBox([
            w.HTML(f"<b>Import images</b> → <code>{escape(str(self.dataset))}</code> (BIDS)"),
            self.subject, self.session,
            w.HTML("<b>NIfTI files</b> — a T1w (chronic route) and/or a DWI + ADC pair (acute route):"),
            *self.paths.values(),
            w.HTML("<b>or DICOM</b> — convert, then check the role of each series:"),
            w.HBox([self.dicom, self.convert]), self.series_box,
            self.overwrite, self.run, self.message])

    def convert_dicom(self):
        import ipywidgets as w
        self.message.value = "Converting in Slurm…"
        try:
            self.series = convert_dicom(self.dicom.value, self.project)
        except Exception as error:
            self.message.value = f"<span style='color:#a00'>Conversion failed: {escape(str(error))}</span>"
            return
        options = [("ignore", None), *[(label, role) for role, label in ROLE_LABELS.items()]]
        self.role_choices = [w.Dropdown(options=options, value=s.get("guess"), layout=w.Layout(width="200px"),
                                        disabled=not s.get("shape")) for s in self.series]
        self.series_box.children = [
            w.HBox([choice, w.HTML(f"{escape(str(s.get('SeriesDescription') or Path(s['nifti']).name))} "
                                   + (f"<small>{'×'.join(map(str, s['shape']))}</small>" if s.get("shape")
                                      else "<small style='color:#a00'>not 3-D: cannot be imported</small>"))])
            for choice, s in zip(self.role_choices, self.series)]
        self.message.value = (f"{len(self.series)} series converted. Check the roles, then Import."
                              if self.series else "dcm2niix found no images in that folder.")

    def files(self):
        chosen = {role: box.value.strip() for role, box in self.paths.items() if box.value.strip()}
        for choice, s in zip(self.role_choices, self.series):
            if choice.value:
                if choice.value in chosen:
                    raise ValueError(f"Two images were given as {ROLE_LABELS[choice.value]}.")
                chosen[choice.value] = s["nifti"]
        return chosen

    def submit(self):
        """Import the chosen images; returns the imported records, or None on error."""
        try:
            done = import_images(self.dataset, self.subject.value, self.session.value or None,
                                 self.files(), overwrite=self.overwrite.value)
        except Exception as error:
            self.message.value = f"<span style='color:#a00'>Not imported: {escape(str(error))}</span>"
            return None
        self.message.value = ("Imported:<br>" + "<br>".join(
            f"{escape(ROLE_LABELS[d['role']])}: <code>{escape(str(d['path']))}</code> "
            f"({'×'.join(map(str, d['shape']))}, {'×'.join(f'{z:g}' for z in d['voxel_mm'])} mm)" for d in done)
            + "<br>Rerun participant selection to include them.")
        return done


def show_local_import(dataset, project_dir):
    from IPython.display import display
    panel = LocalImportPanel(dataset, project_dir)
    display(panel.widget)
    return panel
