"""One place that knows where a participant's inputs and outputs live.

The notebook, the Slurm processing jobs and the review panels all used to
rebuild these paths independently. ``Study`` is now the single definition:

    study = Study(CONFIG, RAW_DATASET_DIR, PROJECT_DIR)
    study.dirs(entry)["linda"]        # derivatives/linda/sub-X/ses-Y/anat
    study.masks(entry)                # {"linda": {"T1w": path, "MNI": path}, ...}

An *entry* is one T1w image to process: ``{"subject", "session", "t1w"}``.
Nothing here runs a tool, downloads data or modifies an image.
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
}

# Generated filenames still use the historical "expert" token for manual masks
# (ExpertMask_in_MNI.nii.gz, *_expert.csv), so existing derivatives stay valid.
FILE_TOKENS = {"manual": "expert"}

SUB_RE = re.compile(r"(sub-[A-Za-z0-9]+)")
SES_RE = re.compile(r"(ses-[A-Za-z0-9]+)")


def file_token(source):
    """Filename token for a mask source ("manual" -> "expert")."""
    return FILE_TOKENS.get(source, source)


def derivative_dirs(dataset, config, entry):
    """BIDS-derivatives folder of every tool for one entry.

    ``<dataset>/<TOOL_SUBDIR>/sub-X[/ses-Y]/anat``
    """
    suffix = Path(entry["subject"]) / (entry.get("session") or "") / "anat"
    return {tool: Path(dataset) / config.get(key, f"derivatives/{tool}") / suffix
            for tool, key in DERIVATIVE_KEYS.items()}


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

    def lesion_native(self, entry):
        """LINDA's native-space lesion mask (the one to edit)."""
        return self.linda_dir(entry) / "Prediction3_native.nii.gz"

    def lesion_mni(self, entry):
        """LINDA's lesion mask in template space."""
        return self.linda_dir(entry) / "Lesion_in_MNI.nii.gz"

    def manual_mask_template(self, entry):
        template = self.config.get("MANUAL_MASK_PATH")
        if not template:
            return None
        return str(template).format(sub=entry["subject"], ses=entry.get("session") or "")

    def masks(self, entry):
        """Existing masks as ``{source: {space: path}}``; nothing is computed."""
        return cm.discover_masks(entry, self.linda_dir(entry), self.synthstroke_dir(entry),
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
        d = self.dirs(entry)
        return {"linda": d["linda"] / "Lesion_in_MNI.nii.gz",
                "manual": d["linda"] / "ExpertMask_in_MNI.nii.gz",
                "synthstroke": d["synthstroke"] / "SynthStroke_in_MNI.nii.gz"}[source]

    def qc_stages(self, entry):
        from . import qc as q
        brain = self.linda_dir(entry) / "BrainMask.nii.gz"
        if not cm.present(brain):
            brain = q.find_best_hdbet_mask(self.hdbet_dir(entry))
        return cm.qc_stages(self.masks(entry), brain_mask=brain,
                            mni_reference=self.linda_dir(entry) / "Subject_in_MNI.nii.gz")

    def label(self, entry):
        return f"{entry['subject']} {entry.get('session') or ''}".strip()

    def notebook_helpers(self):
        """Names older panels look up in the notebook namespace."""
        return {
            "deriv_path_for": self.linda_dir, "hdbet_path_for": self.hdbet_dir,
            "synthstroke_path_for": self.synthstroke_dir, "bcb_path_for": self.bcb_dir,
            "deepdisco_path_for": self.deepdisco_dir, "lesion_native_for": self.lesion_native,
            "lesion_mni_for": self.lesion_mni, "mask_inventory_for": self.masks,
            "available_mni_sources": self.mni_sources, "_mask_path_for": self.mni_mask,
            "qc_available_stages": self.qc_stages, "mask_file_token": file_token,
        }
