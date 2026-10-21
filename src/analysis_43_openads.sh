#!/bin/bash
#SBATCH --job-name=calmar_openads
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=02:00:00
#SBATCH --mem=16G
#SBATCH --cpus-per-task=4
# What this step does (acute route, CONFIG["MODALITY"] = "dwi"):
# OpenADS (openadscpu/1.0.0; Liu et al., acute stroke detection and segmentation)
# segments the acute lesion on the diffusion-weighted image (DWI, b1000 trace)
# with its ADC map, and registers the DWI to MNI152 (affine + SyN against its JHU
# ADC template). The native lesion is then warped to FSL MNI152 with those
# transforms (src/analysis_44_apply_openads_registration.sh, nearest neighbour),
# and the DWI itself (linear) as the template-space background.
#   ads dwi --stages prepdata,gen_mask,skull_strip      then
#   ads dwi --stages registration,inference,report
# Between the two passes the brain-extracted DWI and ADC are regenerated as raw x
# brain mask: OpenADS 1.0.0 names every stripped image <sub>_stroke.nii.gz when the
# subject id contains "stroke" (ISLES ids do), so ADC would overwrite DWI.
# Implementation: calmar.processing.step_openads. About 30 min per participant on CPU.
# Usage (submitted by calmar.scheduled.submit_step, one job per participant):
#   sbatch src/analysis_43_openads.sh <request.json> <result-dir>
# QC: the job also writes reports/qc/steps/<step>/<sub>_<ses>.png and metrics.
set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$PROJECT_DIR"
CALMAR_PYTHON="${CALMAR_PYTHON:-$(command -v python)}"
module load openadscpu/1.0.0
export CALMAR_EXECUTION_SCRIPT="$0"
export PYTHONPATH="$PROJECT_DIR${PYTHONPATH:+:$PYTHONPATH}"
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-4}"
export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS="$OMP_NUM_THREADS"
export OPENBLAS_NUM_THREADS=1
export MPLBACKEND=Agg
for thread_variable in OMP_NUM_THREADS ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS; do
    export "APPTAINERENV_${thread_variable}=${SLURM_CPUS_PER_TASK:-4}"
    export "SINGULARITYENV_${thread_variable}=${SLURM_CPUS_PER_TASK:-4}"
done
REQUEST="${1:?request JSON required}"
FINAL="${2:?output directory required}"
shift 2
for dependency in "$@"; do test -f "$dependency/summary.json"; done
"$CALMAR_PYTHON" -m calmar.processing openads "$REQUEST" "$FINAL"
