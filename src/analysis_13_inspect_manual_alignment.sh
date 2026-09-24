#!/bin/bash
#SBATCH --job-name=calmar_alignment_qc
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:15:00
#SBATCH --mem=8G
#SBATCH --cpus-per-task=4
set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$PROJECT_DIR"
module load linda/0.5.1
INPUT="${1:?dataset root required}"
FINAL="${2:?output directory required}"
mkdir -p "$(dirname "$FINAL")"
TMP="$(mktemp -d "${FINAL}.attempt.XXXXXX")"
trap 'rm -rf "$TMP"' EXIT
export MPLBACKEND=Agg
export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS="$SLURM_CPUS_PER_TASK"
python src/inspect_alignment.py "$INPUT" "$TMP"
neurodesk-astra-provenance publish "$TMP" "$FINAL" \
    --output-id alignment_qc --tool python --script "$0"
