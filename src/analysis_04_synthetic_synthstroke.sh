#!/bin/bash
#SBATCH --job-name=syn_synthstroke
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:30:00
#SBATCH --mem=8G
#SBATCH --cpus-per-task=4

# SynthStroke (T1w-only) on all synthetic subjects, both phases.
# ~15 s per subject, so a single job loops the whole 2x6 matrix.
# Replicates lesion-segmentation-benchmark.ipynb §9b:
#   synthstroke --input <T1w> --outdir <derivatives/synthstroke/<sub>/anat>
#   → prediction_lesion_mask.nii.gz, published to the BIDS mask path.
# Running the chronic-trained tool on the ACUTE phase is intentional — it is
# the cross-modality transfer baseline the synthetic datasets exist to probe.

set -euo pipefail

PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "${PROJECT_DIR}"

module load synthstroke/0.0.0

fail=0
for phase in acute chronic; do
  [ "${phase}" = acute ] && tag=synacu || tag=synchr
  DS="data/synthetic_${phase}"
  for i in 0 1 2 3 4 5; do
    SUB="sub-${tag}00${i}"
    T1="${DS}/${SUB}/anat/${SUB}_T1w.nii.gz"
    WORK="${DS}/derivatives/synthstroke/${SUB}/anat"
    BIDS_MASK="${WORK}/${SUB}_space-T1w_desc-lesion_mask.nii.gz"
    echo "── ${phase}/${SUB}"
    [ -s "${T1}" ] || { echo "  T1w missing → FAIL"; fail=1; continue; }
    if [ -s "${BIDS_MASK}" ]; then echo "  cached ✔"; continue; fi
    mkdir -p "${WORK}"
    if ! synthstroke --input "${T1}" --outdir "${WORK}"; then
        echo "  synthstroke FAILED"; fail=1; continue
    fi
    PRED="${WORK}/prediction_lesion_mask.nii.gz"
    [ -s "${PRED}" ] || { echo "  expected output missing"; fail=1; continue; }
    cp "${PRED}" "${BIDS_MASK}.tmp.$$" && mv "${BIDS_MASK}.tmp.$$" "${BIDS_MASK}"
    echo "  saved ✔ ${BIDS_MASK}"
  done
done
exit "${fail}"
