#!/bin/bash
#SBATCH --job-name=calmar_linda
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=08:00:00
#SBATCH --mem=12G
#SBATCH --cpus-per-task=1
# What this step does:
# LINDA lesion segmentation using the HD-BET brain mask (skips LINDA's skull strip):
#   bash src/analysis_17_linda_predict_with_mask.sh --t1 <T1w> --mask <HD-BET mask> --outdir <dir>
# Outputs: Prediction3_native.nii.gz; Lesion_in_MNI / Subject_in_MNI on FSL MNI152 (native -> Penn -> ch2 -> MNI152,
# one resampling, via analysis_15 + the analysis_38 template transform); LINDA's own ch2 outputs as *_in_ch2
# Reproducibility: one thread plus a fixed ANTs/R seed (CONFIG REGISTRATION_SEED)
# makes LINDA bit-identical between runs (tested 2026-10-12, src/analysis_39); with
# 4 threads the same seed still gave Dice 0.96 between runs. One thread takes
# 1.5-3.7 h per participant, almost all of it LINDA's 3rd-round SyNCC registration;
# participants run as separate jobs in parallel. CONFIG LINDA_THREADS > 1 trades
# reproducibility for speed: submit_step then passes --cpus-per-task=LINDA_THREADS.
# Memory: ~5.3 GB resident seen (sub-M2051, 2026-10-13); 12G leaves headroom.
# Implementation: calmar.processing.step_linda.
# Usage (submitted by calmar.scheduled.submit_step, one job per participant):
#   sbatch src/analysis_24_linda.sh <request.json> <result-dir>
# QC: the job also writes reports/qc/steps/<step>/<sub>_<ses>.png and metrics.
set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$PROJECT_DIR"
CALMAR_PYTHON="${CALMAR_PYTHON:-$(command -v python)}"
module load linda/0.5.1
export CALMAR_EXECUTION_SCRIPT="$0"
export PYTHONPATH="$PROJECT_DIR${PYTHONPATH:+:$PYTHONPATH}"
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-1}"  # CONFIG LINDA_THREADS; 1 = deterministic (see header)
export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS="$OMP_NUM_THREADS"
export OPENBLAS_NUM_THREADS="$OMP_NUM_THREADS"
export MPLBACKEND=Agg
# Neurodesk containers use --cleanenv; explicitly pass allocation limits inside.
for thread_variable in OMP_NUM_THREADS OPENBLAS_NUM_THREADS ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS; do
    export "APPTAINERENV_${thread_variable}=${!thread_variable}"
    export "SINGULARITYENV_${thread_variable}=${!thread_variable}"
done
REQUEST="${1:?request JSON required}"
FINAL="${2:?output directory required}"
shift 2
for dependency in "$@"; do test -f "$dependency/summary.json"; done
"$CALMAR_PYTHON" -m calmar.processing linda "$REQUEST" "$FINAL"
