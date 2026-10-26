#!/bin/bash
#SBATCH --job-name=calmar_dmri_metrics
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:20:00
#SBATCH --mem=8G
#SBATCH --cpus-per-task=1
# Normalize QSIRecon bundle DTI summaries into CALMaR's explicit tractometry
# contract. Metrics that have not yet been computed (currently lesion overlap
# and valid-voxel coverage) remain missing and are labelled as such in reports.
set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "${PROJECT_DIR}"
export CALMAR_PYTHON="${CALMAR_PYTHON:-$(command -v python)}"
export CALMAR_EXECUTION_SCRIPT="$0"
export PYTHONPATH="${PROJECT_DIR}${PYTHONPATH:+:${PYTHONPATH}}"
REQUEST="${1:?request JSON required}"
FINAL="${2:?result directory required}"
shift 2
for dependency in "$@"; do test -f "${dependency}/summary.json"; done
"${CALMAR_PYTHON}" -m calmar.dmri_pipeline dmri_metrics "${REQUEST}" "${FINAL}"
