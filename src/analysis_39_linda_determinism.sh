#!/bin/bash
#SBATCH --job-name=calmar_linda_determinism
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=03:00:00
#SBATCH --mem=24G
#SBATCH --cpus-per-task=4
# What this step does:
# Reproducibility check: runs LINDA (with the HD-BET mask) on one T1w with a fixed
# ANTs/R seed into a fresh folder. Run it twice and compare the two
# Prediction3_native.nii.gz files; identical outputs mean the seed makes LINDA
# deterministic. Nothing in derivatives/ is touched.
# Usage: sbatch src/analysis_39_linda_determinism.sh <T1w> <brain_mask> <outdir> <seed>
set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$PROJECT_DIR"
module load linda/0.5.1
T1="${1:?T1w}"; MASK="${2:?brain mask}"; OUT="${3:?output dir}"; SEED="${4:?seed}"
if [ -e "$OUT" ]; then echo "Refusing to reuse $OUT" >&2; exit 1; fi
mkdir -p "$OUT"
for v in ANTS_RANDOM_SEED CALMAR_R_SEED; do
    export "$v=$SEED" "APPTAINERENV_$v=$SEED" "SINGULARITYENV_$v=$SEED"
done
for v in OMP_NUM_THREADS OPENBLAS_NUM_THREADS ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS; do
    export "$v=${SLURM_CPUS_PER_TASK:-4}" "APPTAINERENV_$v=${SLURM_CPUS_PER_TASK:-4}" "SINGULARITYENV_$v=${SLURM_CPUS_PER_TASK:-4}"
done
echo "threads inside the container: ${SLURM_CPUS_PER_TASK:-4} (sbatch --cpus-per-task=1 for the single-thread test)"
bash src/analysis_17_linda_predict_with_mask.sh --t1 "$T1" --mask "$MASK" --outdir "$OUT"
