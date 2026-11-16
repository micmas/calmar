#!/bin/bash
#SBATCH --job-name=calmar_reader_verify
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:15:00
#SBATCH --mem=6G
#SBATCH --cpus-per-task=2
set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh
cd "${SLURM_SUBMIT_DIR:-$PWD}"
# Browser-only validation; no imaging computation. Dependencies pinned in step 62.
python -m pytest -q tests/test_demo_publication.py tests/test_demo_reader.py
node src/web/demo/verify_reader.cjs "${1:?bundle}" "${2:?verification output}"
