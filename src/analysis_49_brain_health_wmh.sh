#!/bin/bash
#SBATCH --job-name=calmar_brain_health_wmh
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=03:00:00
#SBATCH --mem=24G
#SBATCH --cpus-per-task=4

set -euo pipefail

source /opt/neurodesktop/agent_bash_env.sh
if [[ "${1:-}" == "--version" || "${1:-}" == "-V" ]]; then
    module load deepwmh/1.0.1
    observed="$(deepwmh --version 2>&1 || true)"
    tool_version="$(sed -n 's/.*Version \([0-9][0-9.]*\).*/\1/p' <<<"${observed}" | head -n 1)"
    package_path="$(readlink -f "$(command -v deepwmh)")"
    package_version="$(sed -n 's#.*deepwmh_\([0-9][0-9.]*\)_.*#\1#p' <<<"${package_path}" | head -n 1)"
    test -n "${tool_version}" && test -n "${package_version}"
    echo "CALMaR brain-health WMH 1.0; DeepWMH tool ${tool_version}; Neurodesk package ${package_version}"
    exit 0
fi

PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "${PROJECT_DIR}"
module load deepwmh/1.0.1
observed="$(deepwmh --version 2>&1 || true)"
export CALMAR_DEEPWMH_VERSION
CALMAR_DEEPWMH_VERSION="$(sed -n 's/.*Version \([0-9][0-9.]*\).*/\1/p' <<<"${observed}" | head -n 1)"
test -n "${CALMAR_DEEPWMH_VERSION}"

REQUEST="${1:?usage: $0 <request.json> <output>}"
OUTPUT="${2:?usage: $0 <request.json> <output>}"
export CALMAR_EXECUTION_SCRIPT="$0"
export PYTHONPATH="${PROJECT_DIR}${PYTHONPATH:+:${PYTHONPATH}}"
"${CALMAR_PYTHON:-python}" -m calmar.brain_health_pipeline brain_health_wmh "${REQUEST}" "${OUTPUT}"
