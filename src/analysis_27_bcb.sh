#!/bin/bash
#SBATCH --job-name=calmar_bcb
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=01:00:00
#SBATCH --mem=12G
#SBATCH --cpus-per-task=4
# What this step does:
# BCBToolkit disconnectome for each selected template-space lesion mask. The mask
# is first placed on the FSL MNI152 1 mm grid by world coordinates, then:
#   run_disco.sh -l <input dir> -o <output dir>
# and the map is resampled back to the mask grid.
# Implementation: calmar.processing.step_bcb.
# Usage (submitted by calmar.scheduled.submit_step, one job per participant):
#   sbatch src/analysis_27_bcb.sh <request.json> <result-dir>
# QC: the job also writes reports/qc/steps/<step>/<sub>_<ses>.png and metrics.
set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$PROJECT_DIR"
export CALMAR_PYTHON="${CALMAR_PYTHON:-$(command -v python)}"
module load bcbtoolkit/0.0.0 fsl/6.0.7.22
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
"$CALMAR_PYTHON" -m calmar.processing bcb "$REQUEST" "$FINAL"
