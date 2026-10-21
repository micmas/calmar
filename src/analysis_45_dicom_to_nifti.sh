#!/bin/bash
#SBATCH --job-name=calmar_dicom_import
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:30:00
#SBATCH --mem=4G
#SBATCH --cpus-per-task=1
# What this step does (local data, before participant selection):
# dcm2niix (v1.0.20260724) converts one DICOM folder to gzipped NIfTI with BIDS
# JSON sidecars, one file per series, named <series number>_<protocol>. The job
# lists every series with a guessed role (T1w, FLAIR, DWI, ADC); the notebook
# shows the list, the user confirms the roles, and only then are the chosen
# series copied into the local BIDS dataset (calmar.local_import.import_images).
# Implementation: calmar.dicom_import. A few seconds to a minute per study.
# Usage (submitted by calmar.local_import.convert_dicom):
#   sbatch src/analysis_45_dicom_to_nifti.sh <request.json> <result-dir>
set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$PROJECT_DIR"
CALMAR_PYTHON="${CALMAR_PYTHON:-$(command -v python)}"
module load dcm2niix/v1.0.20260724
export CALMAR_EXECUTION_SCRIPT="$0"
export PYTHONPATH="$PROJECT_DIR${PYTHONPATH:+:$PYTHONPATH}"
"$CALMAR_PYTHON" -m calmar.dicom_import "${1:?request JSON required}" "${2:?output directory required}"
