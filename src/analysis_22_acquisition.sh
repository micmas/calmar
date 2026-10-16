#!/bin/bash
#SBATCH --job-name=calmar_acquisition
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:30:00
#SBATCH --mem=4G
#SBATCH --cpus-per-task=1
# What this step does:
# Fetch image content (datalad get) for each requested T1w and, when present,
# the publisher's manual lesion mask and the scan it was drawn on.
# Implementation: calmar.processing.step_acquisition.
# Usage (submitted by calmar.scheduled.submit_step, one job per participant):
#   sbatch src/analysis_22_acquisition.sh <request.json> <result-dir>
# QC: the job also writes reports/qc/steps/<step>/<sub>_<ses>.png and metrics.
set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$PROJECT_DIR"
CALMAR_PYTHON="${CALMAR_PYTHON:-$(command -v python)}"

export CALMAR_EXECUTION_SCRIPT="$0"
export PYTHONPATH="$PROJECT_DIR${PYTHONPATH:+:$PYTHONPATH}"
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-1}"
export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS="$OMP_NUM_THREADS"
export OPENBLAS_NUM_THREADS="$OMP_NUM_THREADS"
export MPLBACKEND=Agg
REQUEST="${1:?request JSON required}"
FINAL="${2:?output directory required}"
shift 2
for dependency in "$@"; do test -f "$dependency/summary.json"; done
"$CALMAR_PYTHON" -m calmar.processing acquisition "$REQUEST" "$FINAL"
