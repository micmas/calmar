#!/bin/bash
#SBATCH --job-name=openads_isles2022
#SBATCH --output=logs/%x_%A_%a.out
#SBATCH --error=logs/%x_%A_%a.err
#SBATCH --time=01:00:00
#SBATCH --mem=16G
#SBATCH --cpus-per-task=4
#SBATCH --array=0-24%4

# OpenADS acute-stroke segmentation on the ISLES-2022 cohort manifest.
# One array task per subject; replicates the two-pass runner from
# lesion-segmentation-benchmark.ipynb §9c (verified against the completed
# sub-strokecase0004 run):
#   pass 1: prepdata,gen_mask,skull_strip
#   between passes: regenerate *_DWI_brain/*_ADC_brain from the raw images
#           and the SynthStrip mask (see the quirk note below — the stage's
#           own naming is unreliable for "stroke*" subject ids)
#   pass 2: registration,inference,report
# The native-space mask is published atomically to the BIDS derivatives
# path with OpenADS's own RAS+ affine (correct world coordinates; see the
# note at the publish step).

set -euo pipefail

PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "${PROJECT_DIR}"

# Main-env python (has nibabel); resolve before module load changes PATH.
PYBIN="$(command -v python3)"

module load openadscpu/1.0.0

export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS="${SLURM_CPUS_PER_TASK:-4}"
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-4}"

MANIFEST="reports/benchmarks/cohort_isles2022.tsv"
IDX="${SLURM_ARRAY_TASK_ID:?not running as an array task}"
LINE="$(sed -n "$((IDX + 1))p" "${MANIFEST}")"
[ -n "${LINE}" ] || { echo "no manifest line for index ${IDX} — nothing to do"; exit 0; }
SUB="$(printf '%s' "${LINE}" | cut -f1)"
SES="$(printf '%s' "${LINE}" | cut -f2)"
SHORT="${SUB#sub-}"

DS="data/ISLES-2022"
SRC_DWI="${DS}/${SUB}/${SES}/dwi/${SUB}_${SES}_dwi.nii.gz"
SRC_ADC="${DS}/${SUB}/${SES}/dwi/${SUB}_${SES}_adc.nii.gz"
OUT_ROOT="${DS}/derivatives/openads"
BIDS_DIR="${OUT_ROOT}/${SUB}/${SES}/dwi"
BIDS_MASK="${BIDS_DIR}/${SUB}_${SES}_space-DWI_desc-lesion_mask.nii.gz"

echo "[${IDX}] ${SUB} ${SES}"
[ -s "${SRC_DWI}" ] && [ -s "${SRC_ADC}" ] || { echo "input DWI/ADC missing"; exit 1; }

# Idempotent: keep an existing published mask (e.g. the earlier n=2 run).
if [ -s "${BIDS_MASK}" ] && [ "$(head -c2 "${BIDS_MASK}" | od -An -tx1 | tr -d ' ')" = "1f8b" ]; then
    echo "cached ✔ ${BIDS_MASK}"
    exit 0
fi

# Isolate any partial internal outputs from a previous failed attempt.
if [ -d "${OUT_ROOT}/${SUB}/DWI" ] && [ ! -s "${OUT_ROOT}/${SUB}/DWI/segment/${SUB}_stroke-mask.nii.gz" ]; then
    echo "removing incomplete previous attempt ${OUT_ROOT}/${SUB}/DWI"
    rm -rf "${OUT_ROOT}/${SUB}/DWI"
fi

STAGING="${DS}/derivatives/openads_staging/${SUB}"
mkdir -p "${STAGING}" "${OUT_ROOT}"
ln -sfn "$(readlink -f "${SRC_DWI}")" "${STAGING}/${SHORT}_DWI.nii.gz"
ln -sfn "$(readlink -f "${SRC_ADC}")" "${STAGING}/${SHORT}_ADC.nii.gz"

SEG="${OUT_ROOT}/${SUB}/DWI/segment/${SUB}_stroke-mask.nii.gz"
if [ ! -s "${SEG}" ]; then
    ads dwi --subject-path "${STAGING}" --output-root "${OUT_ROOT}" \
        --stages prepdata,gen_mask,skull_strip

    PRE="${OUT_ROOT}/${SUB}/DWI/preprocess"
    # OpenADS 1.0.0 quirk: when the subject id contains "stroke" (e.g. ISLES
    # "sub-strokecase…"), skull_strip renames EVERY stripped image to
    # <sub>_stroke.nii.gz — the stripped ADC overwrites the stripped DWI and
    # the model then receives ADC as its DWI input (it segments CSF).
    # Regenerate both brain files deterministically (raw image x brain mask)
    # instead of trusting the stage's output naming.
    "${PYBIN}" - "${PRE}" "${SUB}" <<'BRAINPY'
import sys
from pathlib import Path
import nibabel as nib
import numpy as np

pre, sub = Path(sys.argv[1]), sys.argv[2]
m = nib.load(pre / f"{sub}_DWIbrain-mask.nii.gz").get_fdata() > 0
for mod in ("DWI", "ADC"):
    img = nib.load(pre / f"{sub}_{mod}.nii.gz")
    dst = pre / f"{sub}_{mod}_brain.nii.gz"
    if dst.is_symlink() or dst.exists():
        dst.unlink()
    nib.save(nib.Nifti1Image((img.get_fdata() * m).astype(np.float32),
                             img.affine), dst)
    print(f"regenerated {dst.name}")
BRAINPY

    ads dwi --subject-path "${STAGING}" --output-root "${OUT_ROOT}" \
        --stages registration,inference,report
fi
[ -s "${SEG}" ] || { echo "FAILED: ${SEG} was not produced"; exit 1; }

mkdir -p "${BIDS_DIR}"
# nibabel infers format from the extension, so the temp name must end .nii.gz
rm -f "${BIDS_MASK%.nii.gz}"_tmp*.nii.gz "${BIDS_MASK}".tmp.*
TMP_MASK="${BIDS_MASK%.nii.gz}_tmp${SLURM_JOB_ID:-$$}.nii.gz"
"${PYBIN}" - "${SRC_DWI}" "${SEG}" "${TMP_MASK}" <<'PY'
import sys
import nibabel as nib
import numpy as np

dwi_p, seg_p, out_p = sys.argv[1:4]
dwi = nib.load(dwi_p)
seg = nib.load(seg_p)
data = seg.get_fdata()
assert data.shape == dwi.shape[:3], f"grid mismatch {data.shape} vs {dwi.shape}"
# Keep OpenADS's own output affine: this container version reorients the
# volume to RAS+ properly (data AND affine), so the segment mask's world
# coordinates are already correct. Re-attaching the source DWI affine (the
# old notebook workaround) mirror-flips masks on non-RAS native grids.
# An empty prediction is a valid benchmark result (Dice 0); a full-volume
# mask is not.
n = int((data > 0).sum())
assert n < 0.5 * data.size, f"implausible lesion voxel count {n}"
if n == 0:
    print("warning: empty prediction (no lesion voxels)")
nib.save(nib.Nifti1Image(data.astype(np.uint8), seg.affine), out_p)
print(f"lesion voxels: {n}")
PY
mv "${TMP_MASK}" "${BIDS_MASK}"
echo "saved ✔ ${BIDS_MASK}"
