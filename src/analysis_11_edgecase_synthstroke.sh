#!/bin/bash
#SBATCH --job-name=edge_synthstroke
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:45:00
#SBATCH --mem=8G
#SBATCH --cpus-per-task=4

# SynthStroke (T1w) across the whole edge-case battery — the fast tool
# (~15 s/subject), doubling as the worked example of an edge-case runner:
# a new tool's runner only needs to write
#   derivatives/<tool>/<sub>/{anat|dwi}/<sub>_space-{T1w|DWI}_desc-lesion_mask.nii.gz
# and analysis_12 will score it per category automatically.

set -euo pipefail

PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "${PROJECT_DIR}"

module load synthstroke/0.0.0

DS="data/synthetic_edgecases"
fail=0
while IFS=$'\t' read -r SUB _phase _cat _vox; do
    [ "${SUB}" = "participant_id" ] && continue
    T1="${DS}/${SUB}/anat/${SUB}_T1w.nii.gz"
    WORK="${DS}/derivatives/synthstroke/${SUB}/anat"
    BIDS_MASK="${WORK}/${SUB}_space-T1w_desc-lesion_mask.nii.gz"
    echo "── ${SUB}"
    [ -s "${T1}" ] || { echo "  T1w missing → FAIL"; fail=1; continue; }
    if [ -s "${BIDS_MASK}" ]; then echo "  cached ✔"; continue; fi
    mkdir -p "${WORK}"
    if ! synthstroke --input "${T1}" --outdir "${WORK}"; then
        echo "  synthstroke FAILED"; fail=1; continue
    fi
    PRED="${WORK}/prediction_lesion_mask.nii.gz"
    [ -s "${PRED}" ] || { echo "  expected output missing"; fail=1; continue; }
    cp "${PRED}" "${BIDS_MASK}.tmp.$$" && mv "${BIDS_MASK}.tmp.$$" "${BIDS_MASK}"
    echo "  saved ✔"
done < "${DS}/participants.tsv"
exit "${fail}"
