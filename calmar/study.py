"""One place that knows where a participant's inputs and outputs live.

The notebook, the Slurm processing jobs and the review panels all used to
rebuild these paths independently. ``Study`` is now the single definition:

    study = Study(CONFIG, RAW_DATASET_DIR, PROJECT_DIR)
    study.dirs(entry)["linda"]        # derivatives/linda/sub-X/ses-Y/anat
    study.masks(entry)                # {"linda": {"T1w": path, "MNI": path}, ...}

An *entry* is one image to process: ``{"subject", "session", "t1w"}``.
``t1w`` is the native image every native-space output lies on: the T1w in the
chronic (T1) route, the diffusion-weighted image in the acute (DWI) route
(``CONFIG["MODALITY"] = "dwi"``), whose entries also carry ``dwi``, ``adc``
and ``modality``. Nothing here runs a tool, downloads data or modifies an image.
"""
from pathlib import Path
import re

from . import masks as cm
from .cohort import sample_t1_participants

# Config key holding each tool's derivatives folder (relative to the dataset).
DERIVATIVE_KEYS = {
    "hdbet": "HDBET_SUBDIR",
    "linda": "DERIVATIVES_SUBDIR",
    "synthstroke": "SYNTHSTROKE_SUBDIR",
    "bcbtoolkit": "BCB_SUBDIR",
    "deepdisco": "DEEPDISCO_SUBDIR",
    "registration": "REGISTRATION_SUBDIR",
    "openads": "OPENADS_SUBDIR",
}

# Automatic lesion segmentations the workflow can run (CONFIG["SEGMENTATION_METHODS"]),
# per imaging route (CONFIG["MODALITY"]): chronic T1w, or acute diffusion (DWI + ADC).
ROUTE_METHODS = {"t1": ("linda", "synthstroke"), "dwi": ("openads",)}
SEGMENTATION_METHODS = ROUTE_METHODS["t1"] + ROUTE_METHODS["dwi"]
# Steps of the T1 route that the DWI route does not run, and the reverse.
T1_ONLY_STAGES = ("brain", "linda", "synthstroke", "registration")
DWI_ONLY_STAGES = ("openads",)


def modality(config):
    """"t1" (chronic route, default) or "dwi" (acute route: OpenADS on DWI + ADC)."""
    value = config.get("MODALITY") or "t1"
    if value not in ROUTE_METHODS:
        raise ValueError(f"MODALITY must be one of {list(ROUTE_METHODS)}, not {value!r}")
    return value

# Generated filenames still use the historical "expert" token for manual masks
# (ExpertMask_in_MNI.nii.gz, *_expert.csv), so existing derivatives stay valid.
FILE_TOKENS = {"manual": "expert"}

SUB_RE = re.compile(r"(sub-[A-Za-z0-9]+)")
SES_RE = re.compile(r"(ses-[A-Za-z0-9]+)")


def file_token(source):
    """Filename token for a mask source ("manual" -> "expert")."""
    return FILE_TOKENS.get(source, source)


def segmentation_methods(config):
    """The automatic segmentations selected in CONFIG (default: both)."""
    allowed = ROUTE_METHODS[modality(config)]
    methods = config.get("SEGMENTATION_METHODS")
    methods = tuple(allowed if methods is None else methods)
    if modality(config) == "dwi":
        methods = allowed                       # the acute route has one segmentation
    unknown = [m for m in methods if m not in allowed]
    if unknown or not methods:
        raise ValueError(f"SEGMENTATION_METHODS must list one or more of {allowed}, not {list(methods)}")
    return methods


def template_source(config):
    """Who registers each brain to the template: "linda" (its own registration,
    reused for every mask), "ants" (the registration step, T1 route without
    LINDA) or "openads" (OpenADS's DWI registration, acute route)."""
    if modality(config) == "dwi":
        return "openads"
    return "linda" if "linda" in segmentation_methods(config) else "ants"


def stage_selected(stage, config):
    """False for a step the selected methods (and imaging route) do not need."""
    route = modality(config)
    if (route == "dwi" and stage in T1_ONLY_STAGES) or (route == "t1" and stage in DWI_ONLY_STAGES):
        return False
    if stage in SEGMENTATION_METHODS:
        return stage in segmentation_methods(config)
    if stage == "registration":
        return template_source(config) == "ants"
    return True


def mni_masks(dirs):
    """Template-space lesion mask of each source (whether or not it exists).

    Masks warped with LINDA's registration live with their tool (and the manual
    mask in LINDA's folder); masks warped by the registration step (LINDA not
    run) live in its folder, so the two registrations never share a file.
    """
    own = dirs["template"] == dirs["linda"]
    masks = {"linda": dirs["linda"] / "Lesion_in_MNI.nii.gz",
             "manual": dirs["template"] / "ExpertMask_in_MNI.nii.gz",
             "synthstroke": (dirs["synthstroke"] if own else dirs["template"]) / "SynthStroke_in_MNI.nii.gz"}
    if "openads" in dirs:
        masks["openads"] = dirs["openads"] / "OpenADS_in_MNI.nii.gz"
    return masks


def derivative_dirs(dataset, config, entry):
    """BIDS-derivatives folder of every tool for one entry.

    ``<dataset>/<TOOL_SUBDIR>/sub-X[/ses-Y]/anat``. ``template`` is the folder
    holding the participant's template registration (``Subject_in_MNI``) and the
    manual mask's products: LINDA's folder when LINDA runs, otherwise the
    registration step's.
    """
    suffix = Path(entry["subject"]) / (entry.get("session") or "") / "anat"
    dirs = {tool: Path(dataset) / config.get(key, f"derivatives/{tool}") / suffix
            for tool, key in DERIVATIVE_KEYS.items()}
    dirs["template"] = dirs[{"linda": "linda", "ants": "registration", "openads": "openads"}[template_source(config)]]
    return dirs


# ── Participant discovery ────────────────────────────────────────────────────

def matches_filter(value, flt):
    """CONFIG filter: None (everything), a list, an exact string or a regex."""
    if flt is None:
        return True
    if isinstance(flt, (list, tuple, set)):
        return value in flt
    if isinstance(flt, str):
        if any(c in flt for c in ".*+?[](){}|^$\\"):
            return re.search(flt, value) is not None
        return value == flt
    return True


def discover_t1w(root, sub_filter=None, ses_filter=None, selection="first"):
    """List T1w images under ``root`` as entries.

    Works for ``sub-*/ses-*/anat``, ``sub-*/anat`` and flat folders. IDs come
    from path components first, then from the filename. ``derivatives``,
    ``.git`` and ``.datalad`` are skipped. With ``selection="first"`` only the
    first T1w (sorted by path) of each subject/session is kept.
    """
    root = Path(root)
    found = []
    for t1 in sorted(root.rglob("*_T1w.nii.gz")):
        parts = t1.relative_to(root).parts
        if any(part in ("derivatives", ".git", ".datalad") for part in parts):
            continue
        sub = next((p for p in parts if p.startswith("sub-")), None)
        ses = next((p for p in parts if p.startswith("ses-")), None)
        if sub is None:
            m = SUB_RE.search(t1.name)
            sub = m.group(1) if m else f"sub-{t1.name.removesuffix('.nii.gz')}"
        if ses is None:
            m = SES_RE.search(t1.name)
            ses = m.group(1) if m else None
        if not matches_filter(sub, sub_filter):
            continue
        if ses is not None and not matches_filter(ses, ses_filter):
            continue
        found.append({"subject": sub, "session": ses, "t1w": t1})
    if selection == "first":
        seen = {}
        for entry in found:
            seen.setdefault((entry["subject"], entry["session"]), entry)
        found = list(seen.values())
    return found


def discover_dwi(root, sub_filter=None, ses_filter=None):
    """List diffusion images with their ADC under ``root`` as entries (acute route).

    Looks for ``sub-*/[ses-*/]dwi/*_dwi.nii.gz`` with an ``*_adc.nii.gz``
    beside it (the ISLES-2022 layout: trace DWI, b1000, and its ADC map);
    ``derivatives`` is skipped. ``t1w`` is set to the DWI, the native image.
    """
    root = Path(root)
    found = []
    for dwi in sorted(root.rglob("*_dwi.nii.gz")):
        parts = dwi.relative_to(root).parts
        if any(part in ("derivatives", ".git", ".datalad") for part in parts):
            continue
        adc = dwi.with_name(dwi.name.replace("_dwi.nii.gz", "_adc.nii.gz"))
        if not adc.exists() and not adc.is_symlink():
            continue
        sub = next((p for p in parts if p.startswith("sub-")), None)
        ses = next((p for p in parts if p.startswith("ses-")), None)
        if sub is None or not matches_filter(sub, sub_filter):
            continue
        if ses is not None and not matches_filter(ses, ses_filter):
            continue
        found.append({"subject": sub, "session": ses, "t1w": dwi, "dwi": dwi, "adc": adc, "modality": "dwi"})
    return found


def select_participants(config, dataset_dir):
    """Apply DATASET_SOURCE, filters and MAX_SUBJECTS/RANDOM_SAMPLE.

    Returns ``(entries, note)``; ``note`` describes any sampling applied.
    """
    source = config["DATASET_SOURCE"]
    if source == "single":
        t1 = Path(config["SINGLE_T1W"]).expanduser().resolve()
        sub, ses = SUB_RE.search(str(t1)), SES_RE.search(str(t1))
        return [{"subject": sub.group(1) if sub else "sub-single",
                 "session": ses.group(1) if ses else None, "t1w": t1}], ""
    if modality(config) == "dwi":
        entries = discover_dwi(dataset_dir, config.get("SUBJECT_FILTER"), config.get("SESSION_FILTER"))
    else:
        entries = discover_t1w(dataset_dir, config.get("SUBJECT_FILTER"),
                               config.get("SESSION_FILTER"), config.get("T1W_SELECTION", "first"))
    n = config.get("MAX_SUBJECTS")
    if config.get("RANDOM_SAMPLE"):
        before = len({e["subject"] for e in entries})
        seed = config.get("RANDOM_SEED", 42)
        entries = sample_t1_participants(entries, n, seed=seed)
        return entries, (f"Random sample of {len(entries)}/{before} participants "
                         f"(MAX_SUBJECTS={n}, seed={seed}), one T1w session each.")
    if n and 0 < n < len(entries):
        before = len(entries)
        return entries[:n], f"First {n}/{before} T1w images (MAX_SUBJECTS={n})."
    return entries, ""


# ── Per-participant paths ────────────────────────────────────────────────────

class Study:
    """Paths and existing masks for each participant of one dataset."""

    def __init__(self, config, dataset_dir, project_dir):
        self.config = config
        self.dataset = Path(dataset_dir)
        self.project = Path(project_dir)

    def dirs(self, entry):
        return derivative_dirs(self.dataset, self.config, entry)

    # Short accessors kept for the review panels and older cells.
    def hdbet_dir(self, entry): return self.dirs(entry)["hdbet"]
    def linda_dir(self, entry): return self.dirs(entry)["linda"]
    def synthstroke_dir(self, entry): return self.dirs(entry)["synthstroke"]
    def bcb_dir(self, entry): return self.dirs(entry)["bcbtoolkit"]
    def deepdisco_dir(self, entry): return self.dirs(entry)["deepdisco"]
    def template_dir(self, entry): return self.dirs(entry)["template"]

    def lesion_native(self, entry):
        """LINDA's native-space lesion mask (the one to edit)."""
        return self.linda_dir(entry) / "Prediction3_native.nii.gz"

    def lesion_mni(self, entry):
        """LINDA's lesion mask in template space."""
        return self.linda_dir(entry) / "Lesion_in_MNI.nii.gz"

    def qc_anchor(self, entry):
        """The mask whose ``*.qc.json`` sidecar holds every QC stage rating:
        LINDA's MNI lesion in the T1 route (also when LINDA did not run), the
        OpenADS MNI lesion in the acute (DWI) route."""
        if modality(self.config) == "dwi":
            return self.dirs(entry)["openads"] / "OpenADS_in_MNI.nii.gz"
        return self.lesion_mni(entry)

    def qc_dir(self, entry):
        """Folder of the QC sidecar and the Do / Skip QC decision (``QC_decision.json``)."""
        return self.qc_anchor(entry).parent

    def manual_mask_template(self, entry):
        template = self.config.get("MANUAL_MASK_PATH")
        if not template:
            return None
        return str(template).format(sub=entry["subject"], ses=entry.get("session") or "")

    def masks(self, entry):
        """Existing masks as ``{source: {space: path}}``; nothing is computed."""
        return cm.discover_masks(entry, self.linda_dir(entry), self.synthstroke_dir(entry),
                                 template_dir=self.template_dir(entry), openads_dir=self.dirs(entry)["openads"],
                                 manual_path=self.manual_mask_template(entry),
                                 manual_space=self.config.get("MANUAL_MASK_SPACE", "t1"))

    def mni_sources(self, entry):
        return [source for source, spaces in self.masks(entry).items() if "MNI" in spaces]

    def mni_mask(self, entry, source):
        """Existing MNI mask for a source, or its expected path when missing."""
        if source not in cm.MASK_LABELS:
            raise ValueError(f"Unknown mask source: {source!r}")
        found = self.masks(entry).get(source, {}).get("MNI")
        if found is not None:
            return found
        return mni_masks(self.dirs(entry))[source]

    def qc_stages(self, entry):
        from . import qc as q
        brain = self.linda_dir(entry) / "BrainMask.nii.gz"
        if modality(self.config) == "dwi":
            brain = None                # OpenADS's brain mask is not rated: its lesion is confined to it
        elif not cm.present(brain):
            brain = q.find_best_hdbet_mask(self.hdbet_dir(entry))
        return cm.qc_stages(self.masks(entry), brain_mask=brain,
                            mni_reference=self.template_dir(entry) / "Subject_in_MNI.nii.gz")

    def label(self, entry):
        return f"{entry['subject']} {entry.get('session') or ''}".strip()

    def notebook_helpers(self):
        """Names older panels look up in the notebook namespace."""
        return {
            "deriv_path_for": self.linda_dir, "hdbet_path_for": self.hdbet_dir,
            "synthstroke_path_for": self.synthstroke_dir, "bcb_path_for": self.bcb_dir,
            "deepdisco_path_for": self.deepdisco_dir, "template_path_for": self.template_dir,
            "lesion_native_for": self.lesion_native,
            "lesion_mni_for": self.lesion_mni, "mask_inventory_for": self.masks,
            "available_mni_sources": self.mni_sources, "_mask_path_for": self.mni_mask,
            "qc_available_stages": self.qc_stages, "mask_file_token": file_token,
            "qc_dir_for": self.qc_dir,
            "openads_path_for": lambda entry: self.dirs(entry)["openads"],
        }
