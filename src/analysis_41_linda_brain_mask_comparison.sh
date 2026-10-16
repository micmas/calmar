#!/bin/bash
#SBATCH --job-name=calmar_linda_mask_compare
#SBATCH --output=logs/%x_%A_%a.out
#SBATCH --error=logs/%x_%A_%a.err
#SBATCH --time=04:00:00
#SBATCH --mem=16G
#SBATCH --cpus-per-task=1
# What this step does:
# Method comparison for the default brain mask given to LINDA. One array task =
# one (session, brain mask) pair from <tasks.json>; LINDA 0.5.1 runs with that
# mask, a fixed ANTs/R seed and one thread (bit-reproducible), into
# <outdir>/<sub>_<ses>_<mask_name>/. Scoring against the expert lesion is a
# separate python step. Nothing in derivatives/ is touched.
# Usage: sbatch --array=0-15 src/analysis_41_linda_brain_mask_comparison.sh <tasks.json> <outdir> <seed>
set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$PROJECT_DIR"
CALMAR_PYTHON="${CALMAR_PYTHON:-$(command -v python)}"
LIST="${1:?tasks.json}"; OUTROOT="${2:?output dir}"; SEED="${3:?seed}"
read -r SUB SES NAME T1 MASK < <("$CALMAR_PYTHON" -c "import json,sys; r=json.load(open(sys.argv[1]))[int(sys.argv[2])]; print(r['subject'], r['session'], r['mask_name'], r['t1w'], r['mask'])" "$LIST" "${SLURM_ARRAY_TASK_ID:?array task}")
OUT="$OUTROOT/${SUB}_${SES}_${NAME}"
if [ -e "$OUT/Prediction3_native.nii.gz" ]; then echo "done already: $OUT"; exit 0; fi
mkdir -p "$OUTROOT"
TMP="$(mktemp -d "${OUT}.attempt.XXXXXX")"
trap 'rm -rf "$TMP"' EXIT
module load linda/0.5.1
# Same determinism settings as the pipeline's LINDA step (processing.step_linda).
for v in ANTS_RANDOM_SEED CALMAR_R_SEED; do
    export "$v=$SEED" "APPTAINERENV_$v=$SEED" "SINGULARITYENV_$v=$SEED"
done
# OPENBLAS too: unset, R's BLAS picks its own thread count and the result differs
# from the pipeline's LINDA step (sub-M2051: Dice 0.87 with identical inputs).
for v in OMP_NUM_THREADS OPENBLAS_NUM_THREADS ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS; do
    export "$v=1" "APPTAINERENV_$v=1" "SINGULARITYENV_$v=1"
done
bash src/analysis_17_linda_predict_with_mask.sh --t1 "$T1" --mask "$MASK" --outdir "$TMP"
test -s "$TMP/Prediction3_native.nii.gz"
rm -rf "$OUT"; mv "$TMP" "$OUT"; trap - EXIT
echo "published $OUT"
