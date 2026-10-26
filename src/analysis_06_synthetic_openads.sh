#!/bin/bash
#SBATCH --job-name=syn_openads
#SBATCH --output=logs/%x_%A_%a.out
#SBATCH --error=logs/%x_%A_%a.err
#SBATCH --time=01:00:00
#SBATCH --mem=16G
#SBATCH --cpus-per-task=4
#SBATCH --array=0-11%4

# OpenADS (DWI+ADC acute tool) on all synthetic subjects, both phases — one
# array task per subject (index 0-5 = acute, 6-11 = chronic). The chronic
# runs are the reverse transfer baseline (DWI pseudonormalized, ADC elevated:
# no restricted-diffusion signature for the tool to find).
# Same two-pass runner as src/analysis_02_openads_isles2022.sh, adapted to the
# session-less synthetic BIDS layout.

set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh

PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "${PROJECT_DIR}"

PYBIN="$(command -v python3)"

module load openadscpu/1.0.0

export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS="${SLURM_CPUS_PER_TASK:-4}"
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-4}"

IDX="${SLURM_ARRAY_TASK_ID:?not running as an array task}"
if [ "${IDX}" -lt 6 ]; then phase=acute; tag=synacu; i=$((IDX));
else phase=chronic; tag=synchr; i=$((IDX - 6)); fi
SUB="sub-${tag}00${i}"
SHORT="${SUB#sub-}"
DS="data/synthetic_${phase}"

SRC_DWI="${DS}/${SUB}/dwi/${SUB}_dwi.nii.gz"
SRC_ADC="${DS}/${SUB}/dwi/${SUB}_adc.nii.gz"
DERIV="derivatives/segmentation-benchmark/synthetic_${phase}"
OUT_ROOT="${DERIV}/openads"
BIDS_DIR="${OUT_ROOT}/${SUB}/dwi"
BIDS_MASK="${BIDS_DIR}/${SUB}_space-DWI_desc-lesion_mask.nii.gz"

echo "[${IDX}] ${phase}/${SUB}"
[ -s "${SRC_DWI}" ] && [ -s "${SRC_ADC}" ] || { echo "input DWI/ADC missing"; exit 1; }
if [ -e "${BIDS_MASK}" ]; then
    [ -s "${BIDS_MASK}" ] && [ -s "${BIDS_MASK}.prov.json" ] || {
        echo "legacy or incomplete OpenADS mask exists: ${BIDS_MASK}" >&2
        exit 1
    }
    echo "cached with provenance ✔ ${BIDS_MASK}"; exit 0
fi

mkdir -p "${DERIV}" "${BIDS_DIR}"
ATTEMPT="$(mktemp -d "${DERIV}/.openads-${SUB}.attempt.XXXXXX")"
trap 'rm -rf "${ATTEMPT}"' EXIT
STAGING="${ATTEMPT}/staging"
ADS_OUT="${ATTEMPT}/openads"
mkdir -p "${STAGING}" "${ADS_OUT}"
ln -sfn "$(readlink -f "${SRC_DWI}")" "${STAGING}/${SHORT}_DWI.nii.gz"
ln -sfn "$(readlink -f "${SRC_ADC}")" "${STAGING}/${SHORT}_ADC.nii.gz"

SEG="${ADS_OUT}/${SUB}/DWI/segment/${SUB}_stroke-mask.nii.gz"
ads dwi --subject-path "${STAGING}" --output-root "${ADS_OUT}" \
    --stages prepdata,gen_mask,skull_strip

PRE="${ADS_OUT}/${SUB}/DWI/preprocess"
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

ads dwi --subject-path "${STAGING}" --output-root "${ADS_OUT}" \
    --stages registration,inference,report
[ -s "${SEG}" ] || { echo "FAILED: ${SEG} was not produced"; exit 1; }

# nibabel infers format from the extension, so the temp name must end .nii.gz
TMP_MASK="${ATTEMPT}/${SUB}_space-DWI_desc-lesion_mask.nii.gz"
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
n = int((data > 0).sum())
assert n < 0.5 * data.size, f"implausible lesion voxel count {n}"
if n == 0:
    print("warning: empty prediction (no lesion voxels)")
nib.save(nib.Nifti1Image(data.astype(np.uint8), seg.affine), out_p)
print(f"lesion voxels: {n}")
PY
neurodesk-astra-provenance publish "${TMP_MASK}" "${BIDS_MASK}" \
    --output-id openads_masks --tool ads --script "$0"
echo "saved ✔ ${BIDS_MASK}"
