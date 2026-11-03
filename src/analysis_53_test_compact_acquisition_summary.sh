#!/bin/bash
#SBATCH --job-name=calmar_acq_summary_tests
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:10:00
#SBATCH --mem=2G
#SBATCH --cpus-per-task=1

set -euo pipefail

PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$PROJECT_DIR"

# Pure Python notebook/UI regression tests; no neuroimaging executable is used.
python -m compileall -q calmar/step_summary.py tests/test_step_summary.py
python -m pytest -q \
    tests/test_step_summary.py \
    tests/test_step_viewer.py \
    tests/test_scheduled.py \
    tests/test_guided_workflow.py \
    tests/test_cohort.py \
    tests/test_notebook_syntax.py \
    tests/test_batch_timing.py
