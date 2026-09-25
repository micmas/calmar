"""Discover existing CALMaR lesion masks without running a segmentation tool.

Only known output conventions or explicitly configured manual masks are used.
Native T1w and MNI outputs are kept separate; finding a file does not establish
registration quality. Discovery never downloads or modifies image data.
"""

from pathlib import Path


MASK_LABELS = {"linda": "LINDA", "synthstroke": "SynthStroke", "manual": "Manual"}


def present(path):
    """Exclude missing content (including unfetched annex links) and empty files."""
    if path is None:
        return False
    try:
        p = Path(path)
        return p.is_file() and p.stat().st_size > 0
    except OSError:
        return False


def discover_masks(entry, linda_dir, synthstroke_dir, *, manual_path=None,
                   manual_space="t1"):
    """Return {source: {space: path}} for locally present, known lesion outputs.

Spaces are ``T1w`` and ``MNI``. A configured manual mask in another space is
not treated as T1w: its registered output must exist before it is offered.
Directories are already scoped to a single subject/session by the caller.
"""
    linda, synth = Path(linda_dir), Path(synthstroke_dir)
    stem = "_".join(x for x in (entry["subject"], entry.get("session")) if x)
    candidates = {
        "linda": {
            "T1w": [linda / "Prediction3_native.nii.gz",
                    linda / f"{stem}_space-T1w_desc-lesion_mask.nii.gz"],
            "MNI": [linda / "Lesion_in_MNI.nii.gz"],
        },
        "synthstroke": {
            "T1w": [synth / "prediction_lesion_mask.nii.gz"],
            "MNI": [synth / "SynthStroke_in_MNI.nii.gz"],
        },
        "manual": {
            "T1w": [linda / "_manual_mask_compare" / "ManualLesion_in_T1_sitk.nii.gz",
                    linda / "_manual_mask_compare" / "ManualLesion_in_T1.nii.gz"],
            "MNI": [linda / "ExpertMask_in_MNI.nii.gz"],
        },
    }
    if manual_path is not None and manual_space in ("t1", "mni"):
        space = "T1w" if manual_space == "t1" else "MNI"
        candidates["manual"][space].insert(0, Path(manual_path))
    found = {}
    for source, spaces in candidates.items():
        for space, paths in spaces.items():
            path = next((p for p in paths if present(p)), None)
            if path is not None:
                found.setdefault(source, {})[space] = path
    return found


def qc_stages(masks, *, brain_mask=None, mni_reference=None):
    """Available stages, without using LINDA completion as a prerequisite."""
    stages = []
    if present(brain_mask):
        stages.append("skull_strip")
    for source, stage in (("linda", "lesion"),
                          ("synthstroke", "synthstroke_lesion"),
                          ("manual", "manual_lesion")):
        if "T1w" in masks.get(source, {}):
            stages.append(stage)
    if "MNI" in masks.get("manual", {}) and present(mni_reference):
        stages.append("expert_mni_warp")
    return stages
