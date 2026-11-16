#!/bin/bash
#SBATCH --job-name=calmar_demo_site
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:30:00
#SBATCH --mem=4G
#SBATCH --cpus-per-task=1
set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$PROJECT_DIR"
# Static export only; imaging has already completed in the prerequisite job.
"${CALMAR_PYTHON:-python}" src/python/package_demo_site.py "$@"
