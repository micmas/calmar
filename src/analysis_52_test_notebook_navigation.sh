#!/bin/bash
#SBATCH --job-name=calmar_nav_tests
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:10:00
#SBATCH --mem=4G
#SBATCH --cpus-per-task=2

set -euo pipefail

# These are UI and isolated-kernel tests. They do not run neuroimaging tools,
# so no Neurodesk module is required.
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "${PROJECT_DIR}"

python -m compileall -q \
    calmar/notebook_navigation.py \
    calmar/execution.py \
    calmar/dwi_choice.py \
    calmar/dmri_choice.py \
    calmar/brain_health_choice.py \
    calmar/single_subject.py \
    calmar/qc_panel.py \
    calmar/report_ui.py \
    calmar/guided.py

python -m pytest -q \
    tests/test_notebook_navigation.py \
    tests/test_guided_workflow.py \
    tests/test_execution_checkpoint.py
