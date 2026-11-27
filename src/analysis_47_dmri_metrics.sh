#!/bin/bash
#SBATCH --job-name=calmar_dmri_metrics
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:20:00
#SBATCH --mem=8G
#SBATCH --cpus-per-task=1
# Normalize diffusion summaries and optionally apply the published QSIPrep
# transforms to measure reconstructed-bundle overlap in diffusion space.
set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "${PROJECT_DIR}"
export CALMAR_PYTHON="${CALMAR_PYTHON:-$(command -v python)}"
export CALMAR_EXECUTION_SCRIPT="$0"
export PYTHONPATH="${PROJECT_DIR}${PYTHONPATH:+:${PYTHONPATH}}"
REQUEST="${1:?request JSON required}"
FINAL="${2:?result directory required}"
shift 2
for dependency in "$@"; do test -f "${dependency}/summary.json"; done
if "${CALMAR_PYTHON}" - "${REQUEST}" <<'PY'
import json
import os
import sys

with open(sys.argv[1]) as request:
    config = json.load(request)["config"]
method = os.environ.get("CALMAR_DMRI_METHOD") or config.get("DMRI_METHOD", "qsirecon")
override = os.environ.get("CALMAR_DMRI_BUNDLE_QC")
enabled = override == "on" if override else config.get("DMRI_BUNDLE_QC", False)
sys.exit(0 if method == "qsirecon" and enabled else 1)
PY
then
    module load ants/2.6.5
fi
"${CALMAR_PYTHON}" -m calmar.dmri_pipeline dmri_metrics "${REQUEST}" "${FINAL}"
