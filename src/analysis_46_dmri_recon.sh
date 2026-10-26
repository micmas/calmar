#!/bin/bash
#SBATCH --job-name=calmar_dmri_recon
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=12:00:00
#SBATCH --mem=48G
#SBATCH --cpus-per-task=8
# Experimental participant-specific tract reconstruction and tractometry from
# the published QSIPrep derivative. Reports must treat failed/missing bundles
# as tracking outcomes, never as proof of anatomical disconnection.
set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "${PROJECT_DIR}"
export CALMAR_PYTHON="${CALMAR_PYTHON:-$(command -v python)}"
module load qsirecon/26.0.1
export CALMAR_EXECUTION_SCRIPT="$0"
export PYTHONPATH="${PROJECT_DIR}${PYTHONPATH:+:${PYTHONPATH}}"
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-8}"
export OPENBLAS_NUM_THREADS=1
export FS_LICENSE="${FS_LICENSE:-/home/jovyan/license.txt}"
test -f "${FS_LICENSE}"
export APPTAINERENV_FS_LICENSE="${FS_LICENSE}"
export SINGULARITYENV_FS_LICENSE="${FS_LICENSE}"
for variable in OMP_NUM_THREADS OPENBLAS_NUM_THREADS; do
    export "APPTAINERENV_${variable}=${!variable}"
    export "SINGULARITYENV_${variable}=${!variable}"
done
REQUEST="${1:?request JSON required}"
FINAL="${2:?result directory required}"
shift 2
for dependency in "$@"; do test -f "${dependency}/summary.json"; done
"${CALMAR_PYTHON}" -m calmar.dmri_pipeline dmri_recon "${REQUEST}" "${FINAL}"
