#!/bin/bash
#SBATCH --job-name=calmar_tool_versions
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:15:00
#SBATCH --mem=4G
#SBATCH --cpus-per-task=1
# What this step does:
# Asks each imaging tool for its own version (as neurodesk-astra-provenance would),
# with a short timeout, so provenance sidecars can name the producing tool rather
# than the orchestrating Python. Nothing is processed.
set -uo pipefail
source /opt/neurodesktop/agent_bash_env.sh
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$PROJECT_DIR"
probe() {  # module, command
    echo "### $1 :: $2"
    module purge >/dev/null 2>&1; module load "$1" || { echo "module load failed"; return; }
    echo "path: $(command -v "$2")"
    for flag in --version -version -V; do
        echo "--- $2 $flag"
        timeout 30 "$2" "$flag" </dev/null 2>&1 | head -5
        echo "exit: ${PIPESTATUS[0]}"
    done
}
probe hdbet/1.0.0 hd-bet
probe linda/0.5.1 linda_predict.sh
probe linda/0.5.1 Rscript
probe linda/0.5.1 antsApplyTransforms
probe synthstroke/0.0.0 synthstroke
probe bcbtoolkit/0.0.0 run_disco.sh
probe deepdisco/20251008 deepdisco-cli
