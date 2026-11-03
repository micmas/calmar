#!/bin/bash
#SBATCH --job-name=calmar-guided-sync-tests
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:10:00
#SBATCH --mem=4G
#SBATCH --cpus-per-task=2

set -euo pipefail

# Pure Python notebook/UI validation: no neuroimaging module is required.
CALMAR_REPO_DIR="${SLURM_SUBMIT_DIR:?Submit this script from the CALMaR repository root}"
cd "$CALMAR_REPO_DIR"

python -m compileall -q calmar
if ! command -v node >/dev/null; then
  echo "Node.js is required for the notebook-navigation frontend regression." >&2
  exit 1
fi

python -m pytest -q -ra \
  tests/test_guided_workflow.py \
  tests/test_notebook_syntax.py \
  tests/test_cohort.py \
  tests/test_analysis_choice.py \
  tests/test_dwi_route.py \
  tests/test_diffusion.py \
  tests/test_brain_health.py \
  tests/test_execution_checkpoint.py \
  tests/test_notebook_navigation.py
