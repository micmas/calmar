#!/bin/bash
#SBATCH --job-name=calmar_dmri_status_tests
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:10:00
#SBATCH --mem=3G
#SBATCH --cpus-per-task=1

set -euo pipefail

PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$PROJECT_DIR"

# Read-only cache/status and notebook UI tests; no neuroimaging command runs.
python -m compileall -q calmar/dmri_choice.py calmar/scheduled.py
python -m pytest -q \
    tests/test_diffusion.py \
    tests/test_scheduled.py \
    tests/test_notebook_navigation.py \
    tests/test_notebook_syntax.py
