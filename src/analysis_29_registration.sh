#!/bin/bash
#SBATCH --job-name=calmar_registration
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=03:00:00
#SBATCH --mem=12G
#SBATCH --cpus-per-task=4
# What this step does (only when LINDA is not among SEGMENTATION_METHODS; with
# LINDA, its own registration is reused):
# registers the brain-extracted T1w to the FSL MNI152 brain (MNI152NLin6Asym, 1 mm)
# with ANTs, excluding the SynthStroke lesion (dilated 2 voxels) from the cost
# function so it does not pull the warp. ANTs' documented reproducible route:
#   1. antsRegistrationSyN.sh -t a -n 1 -e <seed>   (affine; Mattes MI, single thread)
#   2. antsRegistrationSyN.sh -t so -i <affine> -e <seed> -n <threads>   (SyN, CC metric)
# then warps the whole-head T1w (Subject_in_MNI, linear) and the SynthStroke mask
# (SynthStroke_in_MNI, nearest neighbour, src/analysis_42_apply_template_registration.sh).
# Implementation: calmar.processing.step_registration.
# Usage (submitted by calmar.scheduled.submit_step, one job per participant):
#   sbatch src/analysis_29_registration.sh <request.json> <result-dir>
# QC: the job also writes reports/qc/steps/<step>/<sub>_<ses>.png and metrics.
set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$PROJECT_DIR"
CALMAR_PYTHON="${CALMAR_PYTHON:-$(command -v python)}"
module load ants/2.6.5
export CALMAR_EXECUTION_SCRIPT="$0"
export PYTHONPATH="$PROJECT_DIR${PYTHONPATH:+:$PYTHONPATH}"
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-4}"
export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS="$OMP_NUM_THREADS"
export OPENBLAS_NUM_THREADS=1
export MPLBACKEND=Agg
# Neurodesk containers use --cleanenv; explicitly pass allocation limits inside.
for thread_variable in OMP_NUM_THREADS ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS; do
    export "APPTAINERENV_${thread_variable}=${SLURM_CPUS_PER_TASK:-4}"
    export "SINGULARITYENV_${thread_variable}=${SLURM_CPUS_PER_TASK:-4}"
done
REQUEST="${1:?request JSON required}"
FINAL="${2:?output directory required}"
shift 2
for dependency in "$@"; do test -f "$dependency/summary.json"; done
"$CALMAR_PYTHON" -m calmar.processing registration "$REQUEST" "$FINAL"
