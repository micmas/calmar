#!/bin/bash
#SBATCH --job-name=calmar_fetch_nifti
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:15:00
#SBATCH --mem=1G
#SBATCH --cpus-per-task=1

set -euo pipefail
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "${PROJECT_DIR}"

DATASET="${1:?usage: $0 <dataset-root> <dataset-relative-file>}"
RELATIVE_PATH="${2:?usage: $0 <dataset-root> <dataset-relative-file>}"

# DataLad manages the annex object and its original BIDS symlink. Do not
# dereference the symlink or replace it with a separately downloaded copy.
datalad -C "${DATASET}" get -- "${RELATIVE_PATH}"
