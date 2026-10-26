#!/bin/bash
#SBATCH --job-name=calmar_brain_health_anatomy
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=04:00:00
#SBATCH --mem=32G
#SBATCH --cpus-per-task=8

set -euo pipefail

source /opt/neurodesktop/agent_bash_env.sh
if [[ "${1:-}" == "--version" || "${1:-}" == "-V" ]]; then
    module load synthseg/8.2.1
    mri_synthseg --help >/dev/null
    tool_path="$(readlink -f "$(command -v mri_synthseg)")"
    tool_version="$(sed -n 's#.*synthseg_\([0-9][0-9.]*\)_.*#\1#p' <<<"${tool_path}" | head -n 1)"
    test -n "${tool_version}"
    echo "CALMaR brain-health anatomy 1.0; installed mri_synthseg package ${tool_version}"
    exit 0
fi

PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "${PROJECT_DIR}"
module load synthseg/8.2.1
tool_path="$(readlink -f "$(command -v mri_synthseg)")"
export CALMAR_SYNTHSEG_VERSION
CALMAR_SYNTHSEG_VERSION="$(sed -n 's#.*synthseg_\([0-9][0-9.]*\)_.*#\1#p' <<<"${tool_path}" | head -n 1)"
test -n "${CALMAR_SYNTHSEG_VERSION}"

REQUEST="${1:?usage: $0 <request.json> <output>}"
OUTPUT="${2:?usage: $0 <request.json> <output>}"
export CALMAR_EXECUTION_SCRIPT="$0"
export PYTHONPATH="${PROJECT_DIR}${PYTHONPATH:+:${PYTHONPATH}}"
"${CALMAR_PYTHON:-python}" -m calmar.brain_health_pipeline brain_health_anatomy "${REQUEST}" "${OUTPUT}"
