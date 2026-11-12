#!/bin/bash
#SBATCH --job-name=calmar_update_kb
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:10:00
#SBATCH --mem=1G
#SBATCH --cpus-per-task=1

set -euo pipefail
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "${PROJECT_DIR}"

# Share notebook Setup's safe update policy, overriding an offline preference.
CALMAR_KB_UPDATE=latest python - <<'PY'
from calmar.kb_location import resolve_kb_root, update_kb_to_latest

root, reason = resolve_kb_root()
print(f"Selected knowledge base: {root} ({reason})", flush=True)
print(update_kb_to_latest(root, reason), flush=True)
PY
