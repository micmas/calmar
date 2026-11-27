#!/bin/bash
#SBATCH --job-name=calmar_demo_tests
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:05:00
#SBATCH --mem=2G
#SBATCH --cpus-per-task=1
set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$PROJECT_DIR"
# Python-only controller tests; fake kernels perform no imaging computation.
"${CALMAR_PYTHON:-python}" -m pytest -q tests/test_unattended_demo.py tests/test_demo_publication.py
# Check the publication account from the same scheduler environment without
# logging authentication secrets or changing repository state.
gh api repos/micmas/calmar/pages --jq '{cname,build_type}'
gh api -i user | sed -n '/^[Xx]-[Oo][Aa][Uu][Tt][Hh]-[Ss][Cc][Oo][Pp][Ee][Ss]:/p'
