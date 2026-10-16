#!/bin/bash
#SBATCH --job-name=calmar_acceptance_qc
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:20:00
#SBATCH --mem=8G
#SBATCH --cpus-per-task=2
set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$PROJECT_DIR"
CALMAR_PYTHON="${CALMAR_PYTHON:-$(command -v python)}"
module load fsl/6.0.7.22
export PYTHONPATH="$PROJECT_DIR${PYTHONPATH:+:$PYTHONPATH}"
export MPLBACKEND=Agg
export OPENBLAS_NUM_THREADS="${SLURM_CPUS_PER_TASK:-2}"
REQUEST="${1:?cohort request JSON required}"
FINAL="${2:?output directory required}"
shift 2
for dependency in "$@"; do test -f "$dependency/summary.json"; done
test ! -e "$FINAL"
mkdir -p "$(dirname "$FINAL")"
TMP="$(mktemp -d "${FINAL}.attempt.XXXXXX")"
trap 'status=$?; if (( status )); then printf "Inspection diagnostics retained: %s\n" "$TMP"; else rm -rf "$TMP"; fi' EXIT
"$CALMAR_PYTHON" src/python/inspect_acceptance.py "$REQUEST" "$TMP"
neurodesk-astra-provenance publish "$TMP" "$FINAL" \
    --output-id inspection --tool "$CALMAR_PYTHON" --script "$0"
