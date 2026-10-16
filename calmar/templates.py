"""Template space used for every "MNI" output: FSL MNI152 (MNI152NLin6Asym, 1 mm).

LINDA registers each brain to its ch2 (Colin27) template. ``analysis_38`` registers
ch2 to MNI152 once; these files let every warp go native -> Penn -> ch2 -> MNI152
in a single resampling. The atlases, BCBToolkit tractograms and DeepDisco models
are all defined on this MNI152 template.
"""
from pathlib import Path

NAME = "MNI152NLin6Asym"
DIR = Path(__file__).resolve().parents[1] / "atlases" / "templates" / "ch2_to_MNI152NLin6Asym"
WARP = DIR / "ch2_to_MNI152_1Warp.nii.gz"
AFFINE = DIR / "ch2_to_MNI152_0GenericAffine.mat"
T1 = DIR / "MNI152NLin6Asym_T1_1mm.nii.gz"
T1_BRAIN = DIR / "MNI152NLin6Asym_T1_1mm_brain.nii.gz"
BRAIN_MASK = DIR / "MNI152NLin6Asym_T1_1mm_brain_mask.nii.gz"
SHAPE = (182, 218, 182)


def require():
    """The ch2 -> MNI152 transform files, or a clear error saying how to make them."""
    missing = [p for p in (WARP, AFFINE, T1, BRAIN_MASK) if not p.is_file()]
    if missing:
        raise FileNotFoundError(
            "ch2 -> MNI152 template transforms are missing (" + ", ".join(p.name for p in missing) + "). "
            "Run once: sbatch src/analysis_38_template_ch2_to_mni152.sh")
    return WARP, AFFINE


def inputs():
    """Files that define the template space (part of every MNI product's cache identity)."""
    return [WARP, AFFINE, T1]
