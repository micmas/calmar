#!/bin/bash
#SBATCH --job-name=calmar_validation
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:25:00
#SBATCH --mem=8G
#SBATCH --cpus-per-task=2
set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$PROJECT_DIR"
CALMAR_PYTHON="${CALMAR_PYTHON:-$(command -v python)}"
# Dependencies are pinned/restored by analysis_20_restore_environment.sh.
export OPENBLAS_NUM_THREADS="$SLURM_CPUS_PER_TASK"
export MPLBACKEND=Agg
ARTIFACTS="${1:?unique artifacts directory required}"
mkdir -p "$ARTIFACTS"
"$CALMAR_PYTHON" -m pytest -q tests > "$ARTIFACTS/unit-tests.log" 2>&1
"$CALMAR_PYTHON" tests/browser_suite.py --artifacts "$ARTIFACTS/browser"
