#!/bin/bash
#SBATCH --job-name=calmar_notebook_environment
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:30:00
#SBATCH --mem=4G
#SBATCH --cpus-per-task=1
set -euo pipefail
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$PROJECT_DIR"
CALMAR_PYTHON="${CALMAR_PYTHON:-$(command -v python)}"

# Environment maintenance only: no imaging processing or dataset acquisition.
# Run from the project root, outside the notebook kernel. Restart that kernel
# after installation. Scientific processing continues to require Slurm.
# requirements.txt lists the notebook packages; constraints preserve the
# project's numerical stack and setuptools compatibility with PyTorch.
"$CALMAR_PYTHON" -m pip install -c constraints-neurodesk.txt -r requirements.txt 'setuptools<82'
"$CALMAR_PYTHON" -m pip check
"$CALMAR_PYTHON" -c 'import nilearn, ipylab, SimpleITK; print("Required notebook imports passed.")'
