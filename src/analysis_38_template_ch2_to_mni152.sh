#!/bin/bash
#SBATCH --job-name=calmar_template_ch2_to_mni152
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=02:00:00
#SBATCH --mem=16G
#SBATCH --cpus-per-task=8
# What this step does:
# LINDA 0.5.1 writes its "MNI" outputs on the ch2 (Colin27) template: one person's
# brain in MNI coordinates (181x217x181, 1 mm). The atlases, BCBToolkit tractograms
# and DeepDisco are defined on the FSL MNI152 template (MNI152NLin6Asym, 182x218x182).
# This step registers ch2 to MNI152 ONCE (brain to brain, ANTs SyN), so every
# native-space mask can be warped native -> Penn -> ch2 -> MNI152 in one resampling.
#   1. ch2 brain mask = LINDA's Penn template brain mask warped to ch2 with LINDA's
#      own templateToCh2 transforms (antsApplyTransforms, NearestNeighbor)
#   2. antsRegistrationSyN.sh -d 3 -t s -f MNI152_T1_1mm_brain -m ch2_brain
#   3. QC: warped ch2 vs MNI152 (correlation, brain-mask Dice) + PNG
# Outputs (published atomically): atlases/templates/ch2_to_MNI152NLin6Asym/
#   ch2_to_MNI152_0GenericAffine.mat, ch2_to_MNI152_1Warp.nii.gz (+ inverse),
#   MNI152NLin6Asym_T1_1mm.nii.gz (+ _brain, _brain_mask) reference grid,
#   ch2_in_MNI152.nii.gz, qc.json, qc.png
# Usage: sbatch src/analysis_38_template_ch2_to_mni152.sh
set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$PROJECT_DIR"
CALMAR_PYTHON="${CALMAR_PYTHON:-$(command -v python)}"
module load ants/2.6.5
export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS="${SLURM_CPUS_PER_TASK:-8}"
export APPTAINERENV_ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS="$ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS"
export SINGULARITYENV_ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS="$ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS"

PENN=/cvmfs/neurodesk.ardc.edu.au/containers/linda_0.5.1_20260508/linda_0.5.1_20260508.simg/usr/local/lib/R/site-library/LINDA/extdata/pennTemplate
FSL_STD=/cvmfs/neurodesk.ardc.edu.au/containers/fsl_6.0.7.22_20260416/fsl_6.0.7.22_20260416.simg/opt/fsl-6.0.7.22/data/standard
FINAL=atlases/templates/ch2_to_MNI152NLin6Asym
if [ -e "$FINAL" ]; then echo "Refusing to overwrite $FINAL; move it aside first." >&2; exit 1; fi
mkdir -p "$(dirname "$FINAL")"
TMP="$(mktemp -d "${FINAL}.attempt.XXXXXX")"
trap 'rm -rf "$TMP"' EXIT

cp "$FSL_STD/MNI152_T1_1mm.nii.gz" "$TMP/MNI152NLin6Asym_T1_1mm.nii.gz"
cp "$FSL_STD/MNI152_T1_1mm_brain.nii.gz" "$TMP/MNI152NLin6Asym_T1_1mm_brain.nii.gz"
cp "$FSL_STD/MNI152_T1_1mm_brain_mask.nii.gz" "$TMP/MNI152NLin6Asym_T1_1mm_brain_mask.nii.gz"
cp "$PENN/ch2.nii.gz" "$TMP/ch2.nii.gz"

# 1. ch2 brain mask from LINDA's Penn template mask and LINDA's Penn->ch2 transforms.
antsApplyTransforms -d 3 -i "$PENN/templateBrainMask.nii.gz" -r "$PENN/ch2.nii.gz" \
    -t "$PENN/templateToCh2_1Warp.nii.gz" -t "$PENN/templateToCh2_0GenericAffine.mat" \
    -n NearestNeighbor -o "$TMP/ch2_brain_mask.nii.gz"
"$CALMAR_PYTHON" - "$TMP" <<'EOF'
import sys, nibabel as nib, numpy as np
d = sys.argv[1]
t, m = nib.load(f'{d}/ch2.nii.gz'), nib.load(f'{d}/ch2_brain_mask.nii.gz')
brain = np.asarray(t.dataobj, dtype='float32') * (np.asarray(m.dataobj) > .5)
nib.save(nib.Nifti1Image(brain, t.affine, t.header), f'{d}/ch2_brain.nii.gz')
EOF

# 2. Brain-to-brain SyN registration (fixed = MNI152, moving = ch2).
antsRegistrationSyN.sh -d 3 -t s -n "$ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS" \
    -f "$TMP/MNI152NLin6Asym_T1_1mm_brain.nii.gz" -m "$TMP/ch2_brain.nii.gz" \
    -o "$TMP/ch2_to_MNI152_"
# Whole-head ch2 through the same transforms (background for checks).
antsApplyTransforms -d 3 -i "$TMP/ch2.nii.gz" -r "$TMP/MNI152NLin6Asym_T1_1mm.nii.gz" \
    -t "$TMP/ch2_to_MNI152_1Warp.nii.gz" -t "$TMP/ch2_to_MNI152_0GenericAffine.mat" \
    -n Linear -o "$TMP/ch2_in_MNI152.nii.gz"
antsApplyTransforms -d 3 -i "$TMP/ch2_brain_mask.nii.gz" -r "$TMP/MNI152NLin6Asym_T1_1mm.nii.gz" \
    -t "$TMP/ch2_to_MNI152_1Warp.nii.gz" -t "$TMP/ch2_to_MNI152_0GenericAffine.mat" \
    -n NearestNeighbor -o "$TMP/ch2_brain_mask_in_MNI152.nii.gz"

# 3. QC: agreement before and after registration, and a figure.
"$CALMAR_PYTHON" - "$TMP" <<'EOF'
import json, sys
sys.path.insert(0, '.')
import nibabel as nib, numpy as np
from nibabel.processing import resample_from_to
from calmar import step_qc
d = sys.argv[1]
ref = nib.load(f'{d}/MNI152NLin6Asym_T1_1mm_brain.nii.gz')
mask = np.asarray(nib.load(f'{d}/MNI152NLin6Asym_T1_1mm_brain_mask.nii.gz').dataobj) > .5
mni = np.asarray(ref.dataobj, dtype='float32')
def stats(img, brainmask):
    data = np.asarray(img.dataobj, dtype='float32')
    return {'r_in_mni152_brain': round(float(np.corrcoef(data[mask], mni[mask])[0, 1]), 3),
            'brain_mask_dice': round(step_qc.dice(np.asarray(brainmask.dataobj, dtype='float32'), mask.astype('float32')), 3)}
before = stats(resample_from_to(nib.load(f'{d}/ch2_brain.nii.gz'), ref, order=1),
               resample_from_to(nib.load(f'{d}/ch2_brain_mask.nii.gz'), ref, order=0))
after = stats(nib.load(f'{d}/ch2_to_MNI152_Warped.nii.gz'), nib.load(f'{d}/ch2_brain_mask_in_MNI152.nii.gz'))
qc = {'before_registration (ch2 placed by MNI coordinates)': before, 'after_registration': after}
json.dump(qc, open(f'{d}/qc.json', 'w'), indent=2)
print(json.dumps(qc, indent=2))
anat = step_qc._load(f'{d}/ch2_to_MNI152_Warped.nii.gz')
outline = step_qc._data(step_qc._load(f'{d}/MNI152NLin6Asym_T1_1mm_brain_mask.nii.gz', anat))
raw = step_qc._load(resample_from_to(nib.load(f'{d}/ch2_brain.nii.gz'), ref, order=1))
step_qc.figure([dict(bg=step_qc._data(raw), overlays=[(outline, 'cyan')], focus=outline,
                     label=f"ch2 placed by coordinates only · MNI152 brain outline = cyan · r={before['r_in_mni152_brain']}"),
                dict(bg=step_qc._data(anat), overlays=[(outline, 'cyan')], focus=outline,
                     label=f"ch2 after SyN registration · MNI152 brain outline = cyan · r={after['r_in_mni152_brain']}")],
               'ch2 (Colin27) -> MNI152NLin6Asym template registration', f'{d}/qc.png')
EOF
for f in ch2_to_MNI152_0GenericAffine.mat ch2_to_MNI152_1Warp.nii.gz ch2_to_MNI152_1InverseWarp.nii.gz qc.png; do
    test -s "$TMP/$f"
done
neurodesk-astra-provenance publish "$TMP" "$FINAL" --output-id template_ch2_to_mni152 \
    --tool antsRegistration --script "$0"
echo "Published $FINAL"
