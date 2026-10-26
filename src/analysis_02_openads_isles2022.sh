#!/bin/bash
#SBATCH --job-name=openads_isles2022
#SBATCH --output=logs/%x_%A_%a.out
#SBATCH --error=logs/%x_%A_%a.err
#SBATCH --time=01:00:00
#SBATCH --mem=16G
#SBATCH --cpus-per-task=4

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
source /opt/neurodesktop/agent_bash_env.sh

PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "${PROJECT_DIR}"

COHORT_SIZE="${1:-n25}"
MANIFEST="reports/benchmarks/cohort_isles2022_${COHORT_SIZE}.tsv"
if [ -z "${SLURM_ARRAY_TASK_ID:-}" ]; then
    [ -z "${SLURM_JOB_ID:-}" ] || {
        echo "refusing nested sbatch: run this launcher with bash from the project root" >&2
        exit 1
    }
    case "${COHORT_SIZE}" in
        n25) EXPECTED=25 ;;
        n250) EXPECTED=250 ;;
        *) echo "usage: $0 {n25|n250}" >&2; exit 2 ;;
    esac
    [ -s "${MANIFEST}" ] || {
        echo "missing ${MANIFEST}; generate the selected cohort first" >&2
        exit 1
    }
    N_TASKS="$(wc -l < "${MANIFEST}")"
    [ "${N_TASKS}" -eq "${EXPECTED}" ] || {
        echo "${MANIFEST} has ${N_TASKS} rows, expected ${EXPECTED} for ${COHORT_SIZE}" >&2
        exit 1
    }
    mkdir -p logs
    exec sbatch --parsable --array="0-$((N_TASKS - 1))%4" "$0" "${COHORT_SIZE}"
fi

# Main-env python (has nibabel); resolve before module load changes PATH.
PYBIN="$(command -v python3)"

module load openadscpu/1.0.0

export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS="${SLURM_CPUS_PER_TASK:-4}"
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-4}"

IDX="${SLURM_ARRAY_TASK_ID:?not running as an array task}"
LINE="$(sed -n "$((IDX + 1))p" "${MANIFEST}")"
[ -n "${LINE}" ] || { echo "no manifest line for index ${IDX} — nothing to do"; exit 0; }
SUB="$(printf '%s' "${LINE}" | cut -f1)"
SES="$(printf '%s' "${LINE}" | cut -f2)"
SHORT="${SUB#sub-}"

DS="data/ISLES-2022"
SRC_DWI="${DS}/${SUB}/${SES}/dwi/${SUB}_${SES}_dwi.nii.gz"
SRC_ADC="${DS}/${SUB}/${SES}/dwi/${SUB}_${SES}_adc.nii.gz"
OUT_ROOT="derivatives/segmentation-benchmark/ISLES-2022/openads"
BIDS_DIR="${OUT_ROOT}/${SUB}/${SES}/dwi"
BIDS_MASK="${BIDS_DIR}/${SUB}_${SES}_space-DWI_desc-lesion_mask.nii.gz"

echo "[${IDX}] ${SUB} ${SES}"
[ -s "${SRC_DWI}" ] && [ -s "${SRC_ADC}" ] || { echo "input DWI/ADC missing"; exit 1; }

# Reuse only masks produced by the corrected, provenance-recorded runner.
if [ -e "${BIDS_MASK}" ]; then
    [ -s "${BIDS_MASK}" ] && [ -s "${BIDS_MASK}.prov.json" ] \
        && [ "$(head -c2 "${BIDS_MASK}" | od -An -tx1 | tr -d ' ')" = "1f8b" ] || {
        echo "legacy or incomplete OpenADS mask exists: ${BIDS_MASK}" >&2
        exit 1
    }
    echo "cached with provenance ✔ ${BIDS_MASK}"
    exit 0
fi

mkdir -p "derivatives/segmentation-benchmark/ISLES-2022" "${BIDS_DIR}"
ATTEMPT="$(mktemp -d "derivatives/segmentation-benchmark/ISLES-2022/.openads-${SUB}.attempt.XXXXXX")"
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
TMP_MASK="${ATTEMPT}/${SUB}_${SES}_space-DWI_desc-lesion_mask.nii.gz"
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
neurodesk-astra-provenance publish "${TMP_MASK}" "${BIDS_MASK}" \
    --output-id openads_masks --tool ads --script "$0"
echo "saved ✔ ${BIDS_MASK}"
