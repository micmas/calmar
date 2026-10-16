#!/bin/bash
#SBATCH --job-name=calmar_launch_probe
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:01:00
#SBATCH --mem=12G
#SBATCH --cpus-per-task=4
set -euo pipefail
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$PROJECT_DIR"
printf 'Batch script started: job=%s host=%s\n' "$SLURM_JOB_ID" "$(hostname)"
/usr/bin/id
/bin/true
