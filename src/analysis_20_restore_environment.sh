#!/bin/bash
#SBATCH --job-name=calmar_environment
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:30:00
#SBATCH --mem=8G
#SBATCH --cpus-per-task=2
set -euo pipefail
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$PROJECT_DIR"
python -m pip install -c constraints-neurodesk.txt -r requirements.txt -r tests/requirements.txt -r tests/requirements-browser.txt nbstripout setuptools
python -m pip check
python -m playwright install chromium
python -m pip freeze > "logs/environment_${SLURM_JOB_ID:-local}.txt"
