#!/bin/bash
#SBATCH --job-name=calmar_web_dependencies
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:10:00
#SBATCH --mem=2G
#SBATCH --cpus-per-task=1
set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh
cd "${SLURM_SUBMIT_DIR:-$PWD}"
# Browser renderer and test runner only; no imaging or dataset downloads.
mkdir -p analyses/unattended-demo/web-tools
cp src/web/demo/package.json src/web/demo/package-lock.json analyses/unattended-demo/web-tools/
npm ci --prefix analyses/unattended-demo/web-tools --no-audit --no-fund
node analyses/unattended-demo/web-tools/node_modules/playwright/cli.js install chromium
