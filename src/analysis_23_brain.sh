#!/bin/bash
#SBATCH --job-name=calmar_brain
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:45:00
#SBATCH --mem=12G
#SBATCH --cpus-per-task=4
# What this step does:
# Brain mask of the whole-head T1w (CONFIG["BRAIN_MASK"], default "hdbet"):
#   hd-bet -i <T1w> -o <prefix> -device cpu -mode fast -tta 0     (brain tissue)
# With BRAIN_MASK="hdbet+synthstrip" also
#   mri_synthstrip -i <T1w> -o <brain> -m <mask>                   (brain + CSF)
#   brain mask = HD-BET OR SynthStrip, so CSF-filled lesion cavities stay inside
# Outputs: derivatives/hdbet/<sub>/<ses>/anat/<stem>_brain_mask.nii.gz (used by later
# steps), _brain.nii.gz, the component _desc-hdbet_brain_mask.nii.gz and, for the
# union, _desc-synthstrip_brain_mask.nii.gz
# Implementation: calmar.processing.step_brain.
# Usage (submitted by calmar.scheduled.submit_step, one job per participant):
#   sbatch src/analysis_23_brain.sh <request.json> <result-dir>
# QC: the job also writes reports/qc/steps/<step>/<sub>_<ses>.png and metrics.
set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$PROJECT_DIR"
CALMAR_PYTHON="${CALMAR_PYTHON:-$(command -v python)}"
module load hdbet/1.0.0 synthstrip/7.4.1
export CALMAR_EXECUTION_SCRIPT="$0"
export PYTHONPATH="$PROJECT_DIR${PYTHONPATH:+:$PYTHONPATH}"
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-4}"
export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS="$OMP_NUM_THREADS"
export OPENBLAS_NUM_THREADS="$OMP_NUM_THREADS"
export MPLBACKEND=Agg
# Neurodesk containers use --cleanenv; explicitly pass allocation limits inside.
for thread_variable in OMP_NUM_THREADS OPENBLAS_NUM_THREADS ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS; do
    export "APPTAINERENV_${thread_variable}=${SLURM_CPUS_PER_TASK:-4}"
    export "SINGULARITYENV_${thread_variable}=${SLURM_CPUS_PER_TASK:-4}"
done
REQUEST="${1:?request JSON required}"
FINAL="${2:?output directory required}"
shift 2
for dependency in "$@"; do test -f "$dependency/summary.json"; done
"$CALMAR_PYTHON" -m calmar.processing brain "$REQUEST" "$FINAL"
