#!/bin/bash
#SBATCH --job-name=calmar_demo
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=96:00:00
#SBATCH --signal=B:USR1@600
#SBATCH --mem=10G
#SBATCH --cpus-per-task=1
set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$PROJECT_DIR"
# This allocation runs the notebook controller. Each imaging cell submits the
# existing version-pinned analysis_22..50 scripts in separate Slurm allocations.
# Notebook dependencies: Python 3.13.15, nbclient 0.11.0, nbformat 5.11.1,
# nbconvert 7.17.1 plus the project's requirements/constraints (already installed).
export CALMAR_PYTHON="${CALMAR_PYTHON:-$(command -v python)}"
export PYTHONPATH="$PROJECT_DIR${PYTHONPATH:+:$PYTHONPATH}"
export MPLBACKEND=Agg
export CALMAR_KB_UPDATE=off
export CALMAR_DEMO_SCRIPT="$PROJECT_DIR/src/analysis_58_unattended_demo.sh"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
exec "$CALMAR_PYTHON" src/python/unattended_demo.py "$@"
