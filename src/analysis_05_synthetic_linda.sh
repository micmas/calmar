#!/bin/bash
#SBATCH --job-name=syn_linda
#SBATCH --output=logs/%x_%A_%a.out
#SBATCH --error=logs/%x_%A_%a.err
#SBATCH --time=01:30:00
#SBATCH --mem=16G
#SBATCH --cpus-per-task=4
#SBATCH --array=0-11%4

# LINDA (chronic T1w tool) on all synthetic subjects, both phases — one array
# task per subject (index 0-5 = acute, 6-11 = chronic). Acute-phase runs are
# the deliberate transfer baseline (acute stroke is faint on T1w).
# Replicates lesion-segmentation-benchmark.ipynb §9a:
#   1. HD-BET skull-strip (mode from $1 / HDBET_MODE, default "fast")
#      → derivatives/hdbet/<sub>/anat/<sub>_T1w_brain_mask.nii.gz
#   2. analysis_17_linda_predict_with_mask.sh --t1 --mask --outdir (retained wrapper;
#      dispatches into the LINDA singularity container)
#   3. Prediction3_native.nii.gz published to the BIDS mask path.

if [ "${1:-}" = "--version" ]; then
    if [ "${CALMAR_PROVENANCE_COMPONENT:-linda}" = "hdbet" ]; then
        echo "hd-bet 1.0.0 (CALMaR benchmark workflow)"
    else
        echo "LINDA 0.5.1 (CALMaR benchmark workflow)"
    fi
    exit 0
fi

set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh

PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "${PROJECT_DIR}"
trap 'rm -rf "${BRAIN_ATTEMPT:-}" "${LINDA_ATTEMPT:-}"' EXIT

HDBET_MODE="${1:-${HDBET_MODE:-fast}}"
LINDA_SEED="${2:-historical_unseeded}"
case "${LINDA_SEED}" in
    historical_unseeded)
        SEED_TAG="unseeded"
        unset ANTS_RANDOM_SEED CALMAR_R_SEED \
            APPTAINERENV_ANTS_RANDOM_SEED APPTAINERENV_CALMAR_R_SEED \
            SINGULARITYENV_ANTS_RANDOM_SEED SINGULARITYENV_CALMAR_R_SEED \
            ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS OMP_NUM_THREADS \
            APPTAINERENV_ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS \
            APPTAINERENV_OMP_NUM_THREADS \
            SINGULARITYENV_ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS \
            SINGULARITYENV_OMP_NUM_THREADS
        ;;
    seed1729)
        SEED_TAG="seed1729"
        export ANTS_RANDOM_SEED=1729 CALMAR_R_SEED=1729
        export APPTAINERENV_ANTS_RANDOM_SEED=1729 APPTAINERENV_CALMAR_R_SEED=1729
        export SINGULARITYENV_ANTS_RANDOM_SEED=1729 SINGULARITYENV_CALMAR_R_SEED=1729
        export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=1 OMP_NUM_THREADS=1
        ;;
    *) echo "usage: $0 {fast|accurate} {historical_unseeded|seed1729}" >&2; exit 2 ;;
esac

PYBIN="$(command -v python3)"
PROVENANCE_TOOL="${PROJECT_DIR}/src/analysis_05_synthetic_linda.sh"
module load linda/0.5.1 hdbet/1.0.0

IDX="${SLURM_ARRAY_TASK_ID:?not running as an array task}"
if [ "${IDX}" -lt 6 ]; then phase=acute; tag=synacu; i=$((IDX));
else phase=chronic; tag=synchr; i=$((IDX - 6)); fi
SUB="sub-${tag}00${i}"
DS="data/synthetic_${phase}"
T1="${DS}/${SUB}/anat/${SUB}_T1w.nii.gz"

DERIV="derivatives/segmentation-benchmark/synthetic_${phase}"
WORK="${DERIV}/linda-hdbet-${HDBET_MODE}-${SEED_TAG}/${SUB}/anat"
BIDS_MASK="${WORK}/${SUB}_space-T1w_desc-lesion_mask.nii.gz"
HDBET_DIR="${WORK}/preproc-hdbet-${HDBET_MODE}"
BRAIN_MASK="${HDBET_DIR}/${SUB}_T1w_brain_mask.nii.gz"

echo "[${IDX}] ${phase}/${SUB} (hd-bet=${HDBET_MODE}; LINDA=${LINDA_SEED})"
[ -s "${T1}" ] || { echo "T1w missing"; exit 1; }
if [ -e "${BIDS_MASK}" ]; then
    [ -s "${BIDS_MASK}" ] && [ -s "${BIDS_MASK}.prov.json" ] || {
        echo "legacy or incomplete LINDA mask exists without usable provenance: ${BIDS_MASK}" >&2
        exit 1
    }
    echo "cached with provenance ✔ ${BIDS_MASK}"; exit 0
fi

if [ -e "${BRAIN_MASK}" ] && [ ! -s "${BRAIN_MASK}.prov.json" ]; then
    echo "legacy HD-BET mask exists without provenance: ${BRAIN_MASK}" >&2
    exit 1
fi
if [ ! -s "${BRAIN_MASK}" ]; then
    mkdir -p "${HDBET_DIR}" "${DERIV}"
    BRAIN_ATTEMPT="$(mktemp -d "${DERIV}/.hdbet-${SUB}.attempt.XXXXXX")"
    hd-bet -i "${T1}" -o "${BRAIN_ATTEMPT}/${SUB}_T1w_brain.nii.gz" \
        -mode "${HDBET_MODE}" -device cpu -tta 0
    BRAIN_TMP="${BRAIN_ATTEMPT}/${SUB}_T1w_brain_mask.nii.gz"
    [ -s "${BRAIN_TMP}" ] || { echo "HD-BET produced no brain mask"; exit 1; }
    "${PYBIN}" - "${BRAIN_TMP}" <<'PY'
import sys
import nibabel as nib
import numpy as np
data = np.asarray(nib.load(sys.argv[1]).dataobj)
assert data.ndim == 3 and np.isfinite(data).all()
assert 0 < int((data > 0).sum()) < data.size
PY
    CALMAR_PROVENANCE_COMPONENT=hdbet \
        neurodesk-astra-provenance publish "${BRAIN_TMP}" "${BRAIN_MASK}" \
            --output-id linda_brain_masks \
            --tool "${PROVENANCE_TOOL}" --script "$0"
    rm -rf "${BRAIN_ATTEMPT}"
fi

mkdir -p "${WORK}" "${DERIV}"
LINDA_ATTEMPT="$(mktemp -d "${DERIV}/.linda-${SUB}.attempt.XXXXXX")"
bash src/analysis_17_linda_predict_with_mask.sh \
    --t1 "${T1}" --mask "${BRAIN_MASK}" --outdir "${LINDA_ATTEMPT}"
NATIVE_PRED="${LINDA_ATTEMPT}/Prediction3_native.nii.gz"
[ -s "${NATIVE_PRED}" ] || { echo "FAILED: ${NATIVE_PRED} not produced"; exit 1; }
"${PYBIN}" - "${NATIVE_PRED}" <<'PY'
import sys
import nibabel as nib
import numpy as np
data = np.asarray(nib.load(sys.argv[1]).dataobj)
assert data.ndim == 3 and np.isfinite(data).all()
assert int((data > 0).sum()) < data.size // 2
PY

neurodesk-astra-provenance publish "${NATIVE_PRED}" "${BIDS_MASK}" \
    --output-id linda_masks \
    --tool "${PROVENANCE_TOOL}" --script "$0"
rm -rf "${LINDA_ATTEMPT}"
echo "saved ✔ ${BIDS_MASK}"
