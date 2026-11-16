#!/bin/bash
#SBATCH --job-name=calmar_demo_publish
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=01:00:00
#SBATCH --mem=4G
#SBATCH --cpus-per-task=1
set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$PROJECT_DIR"
# Submit only after the completed-run packaging job. The repository's existing
# GitHub Pages workflow performs deployment; no hosting or DNS settings change.
exec "${CALMAR_PYTHON:-python}" src/python/publish_demo_site.py "$@"
