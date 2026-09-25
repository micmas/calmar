#!/bin/bash
#SBATCH --job-name=calmar_corrected_disconnectomes
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:30:00
#SBATCH --mem=16G
#SBATCH --cpus-per-task=4
set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$PROJECT_DIR"
module load deepdisco/20251008
DATASET="${1:?dataset root required}"
CORRECTED="${2:?inspected correction directory required}"
FINAL="${3:?completion report directory required}"
TMP="$(mktemp -d "${FINAL}.attempt.XXXXXX")"
trap 'rm -rf "$TMP"' EXIT
export OMP_NUM_THREADS="$SLURM_CPUS_PER_TASK"
export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS="$SLURM_CPUS_PER_TASK"
export MPLBACKEND=Agg
python src/python/refresh_corrected_disconnectomes.py "$DATASET" "$CORRECTED" "$TMP"
neurodesk-astra-provenance publish "$TMP" "$FINAL" \
    --output-id corrected_disconnectomes --tool python --script "$0"
