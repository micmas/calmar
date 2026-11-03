#!/bin/bash
#SBATCH --job-name=calmar_optional_actions_tests
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:12:00
#SBATCH --mem=3G
#SBATCH --cpus-per-task=1

set -euo pipefail

PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$PROJECT_DIR"

# Pure Python workflow/UI tests; no neuroimaging command runs.
python -m compileall -q \
    calmar/analysis_choice.py calmar/dwi_choice.py calmar/dmri_choice.py \
    calmar/brain_health_choice.py calmar/scheduled.py calmar/processing.py
python -m pytest -q \
    tests/test_analysis_choice.py \
    tests/test_dwi_route.py \
    tests/test_diffusion.py \
    tests/test_brain_health.py \
    tests/test_scheduled.py \
    tests/test_notebook_syntax.py
