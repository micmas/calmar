#!/bin/bash
#SBATCH --job-name=calmar_recover_dmri_recon
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:20:00
#SBATCH --mem=4G
#SBATCH --cpus-per-task=1

# Validate and publish a complete retained QSIRecon attempt after CALMaR's
# artifact contract has been corrected. This does not run QSIRecon. Once the
# artifacts, subject/session, method and producing version all match, recovery
# adds CALMaR provenance to produced/ and atomically publishes that directory;
# the retained work directory and original QSIRecon log remain in place.
set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "${PROJECT_DIR}"
export CALMAR_PYTHON="${CALMAR_PYTHON:-$(command -v python)}"
# The provenance publisher queries the producing tool's version even though
# this recovery job does not execute QSIRecon itself.
module load qsirecon/26.0.1
export CALMAR_EXECUTION_SCRIPT="$0"
export PYTHONPATH="${PROJECT_DIR}${PYTHONPATH:+:${PYTHONPATH}}"

REQUEST="${1:?request JSON required}"
RETAINED="${2:?retained QSIRecon attempt required}"
FINAL="${3:?result directory required}"

test -f "${REQUEST}"
test -d "${RETAINED}/produced"
test -f "${RETAINED}/qsirecon.log"
"${CALMAR_PYTHON}" -m calmar.dmri_pipeline \
    dmri_recon_recover "${REQUEST}" "${FINAL}" --retained "${RETAINED}"
