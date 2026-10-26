#!/bin/bash
#SBATCH --job-name=calmar_brain_health_metrics
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=02:00:00
#SBATCH --mem=16G
#SBATCH --cpus-per-task=4

set -euo pipefail

source /opt/neurodesktop/agent_bash_env.sh
if [[ "${1:-}" == "--version" || "${1:-}" == "-V" ]]; then
    module load ants/2.6.5
    observed="$(antsRegistration --version | head -n 1)"
    test -n "${observed}"
    echo "CALMaR brain-health metrics 1.0; ${observed}"
    exit 0
fi

PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "${PROJECT_DIR}"
module load ants/2.6.5
observed="$(antsRegistration --version | head -n 1)"
export CALMAR_ANTS_VERSION
CALMAR_ANTS_VERSION="$(sed -n 's/.*Version: *\([^ ]*\).*/\1/p' <<<"${observed}" | head -n 1)"
test -n "${CALMAR_ANTS_VERSION}"

REQUEST="${1:?usage: $0 <request.json> <output>}"
OUTPUT="${2:?usage: $0 <request.json> <output>}"
export CALMAR_EXECUTION_SCRIPT="$0"
export PYTHONPATH="${PROJECT_DIR}${PYTHONPATH:+:${PYTHONPATH}}"
"${CALMAR_PYTHON:-python}" -m calmar.brain_health_pipeline brain_health_metrics "${REQUEST}" "${OUTPUT}"
