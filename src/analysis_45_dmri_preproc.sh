#!/bin/bash
#SBATCH --job-name=calmar_dmri_preproc
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=12:00:00
#SBATCH --mem=48G
#SBATCH --cpus-per-task=8
# Optional, lesion-aware preprocessing of gradient-bearing dMRI. The Python
# entry point builds a one-participant BIDS staging tree, places the reviewed
# native-T1 lesion mask at *_label-lesion_roi.nii.gz, runs QSIPrep, validates
# its DWI and HTML report, then publishes atomically with provenance.
set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "${PROJECT_DIR}"
export CALMAR_PYTHON="${CALMAR_PYTHON:-$(command -v python)}"
module load qsiprep/26.1.1
export CALMAR_EXECUTION_SCRIPT="$0"
export PYTHONPATH="${PROJECT_DIR}${PYTHONPATH:+:${PYTHONPATH}}"
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-8}"
export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS="${OMP_NUM_THREADS}"
export OPENBLAS_NUM_THREADS=1
for variable in OMP_NUM_THREADS ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS OPENBLAS_NUM_THREADS; do
    export "APPTAINERENV_${variable}=${!variable}"
    export "SINGULARITYENV_${variable}=${!variable}"
done
REQUEST="${1:?request JSON required}"
FINAL="${2:?result directory required}"
shift 2
for dependency in "$@"; do test -f "${dependency}/summary.json"; done
"${CALMAR_PYTHON}" -m calmar.dmri_pipeline dmri_preproc "${REQUEST}" "${FINAL}"
