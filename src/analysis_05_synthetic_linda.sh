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

set -euo pipefail

PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "${PROJECT_DIR}"

HDBET_MODE="${1:-${HDBET_MODE:-fast}}"

module load linda/0.5.1 hdbet/1.0.0

IDX="${SLURM_ARRAY_TASK_ID:?not running as an array task}"
if [ "${IDX}" -lt 6 ]; then phase=acute; tag=synacu; i=$((IDX));
else phase=chronic; tag=synchr; i=$((IDX - 6)); fi
SUB="sub-${tag}00${i}"
DS="data/synthetic_${phase}"
T1="${DS}/${SUB}/anat/${SUB}_T1w.nii.gz"

WORK="${DS}/derivatives/linda/${SUB}/anat"
BIDS_MASK="${WORK}/${SUB}_space-T1w_desc-lesion_mask.nii.gz"
NATIVE_PRED="${WORK}/Prediction3_native.nii.gz"
HDBET_DIR="${DS}/derivatives/hdbet/${SUB}/anat"
BRAIN_MASK="${HDBET_DIR}/${SUB}_T1w_brain_mask.nii.gz"

echo "[${IDX}] ${phase}/${SUB} (hd-bet mode: ${HDBET_MODE})"
[ -s "${T1}" ] || { echo "T1w missing"; exit 1; }
if [ -s "${BIDS_MASK}" ]; then echo "cached ✔"; exit 0; fi

if [ ! -s "${BRAIN_MASK}" ]; then
    mkdir -p "${HDBET_DIR}"
    hd-bet -i "${T1}" -o "${HDBET_DIR}/${SUB}_T1w_brain.nii.gz" \
        -mode "${HDBET_MODE}" -device cpu -tta 0
    [ -s "${BRAIN_MASK}" ] || { echo "HD-BET produced no brain mask"; exit 1; }
fi

mkdir -p "${WORK}"
if [ ! -s "${NATIVE_PRED}" ]; then
    bash src/analysis_17_linda_predict_with_mask.sh \
        --t1 "${T1}" --mask "${BRAIN_MASK}" --outdir "${WORK}"
fi
[ -s "${NATIVE_PRED}" ] || { echo "FAILED: ${NATIVE_PRED} not produced"; exit 1; }

cp "${NATIVE_PRED}" "${BIDS_MASK}.tmp.${SLURM_JOB_ID:-$$}"
mv "${BIDS_MASK}.tmp.${SLURM_JOB_ID:-$$}" "${BIDS_MASK}"
echo "saved ✔ ${BIDS_MASK}"
