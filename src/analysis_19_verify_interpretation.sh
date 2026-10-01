#!/bin/bash
#SBATCH --job-name=calmar_interpretation_check
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:15:00
#SBATCH --mem=8G
#SBATCH --cpus-per-task=2
set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$PROJECT_DIR"
CALMAR_PYTHON="$(command -v python)"
module load fsl/6.0.7.22
DATASET="${1:?dataset required}"
ATLASES="${2:?atlas directory required}"
CACHE="${3:?Neurosynth cache required}"
FINAL="${4:?output directory required}"
mkdir -p "$(dirname "$FINAL")"
TMP="$(mktemp -d "${FINAL}.attempt.XXXXXX")"
trap 'rm -rf "$TMP"' EXIT
export MPLBACKEND=Agg
export OPENBLAS_NUM_THREADS=2
export PYTHONPATH="$PROJECT_DIR${PYTHONPATH:+:$PYTHONPATH}"
# These are the notebook's existing packages; no installation or downloads.
"$CALMAR_PYTHON" src/python/verify_interpretation.py "$DATASET" "$ATLASES" "$CACHE" "$TMP"
neurodesk-astra-provenance publish "$TMP" "$FINAL" \
    --output-id verification --tool "$CALMAR_PYTHON" --script "$0"
