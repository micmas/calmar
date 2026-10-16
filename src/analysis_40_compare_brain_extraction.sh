#!/bin/bash
#SBATCH --job-name=calmar_compare_brain_extraction
#SBATCH --output=logs/%x_%A_%a.out
#SBATCH --error=logs/%x_%A_%a.err
#SBATCH --time=01:30:00
#SBATCH --mem=16G
#SBATCH --cpus-per-task=4
# What this step does:
# Method comparison for the default brain extractor (one array task per
# participant with an expert lesion mask). For one T1w it writes the masks of:
#   hdbet1_accurate   hd-bet (hdbet/1.0.0) -mode accurate -device cpu -tta 0
#   hdbet2            hd-bet (hdbet/2.0.1) -device cpu (test-time augmentation on)
#   synthstrip_csf    mri_synthstrip (synthstrip/7.4.1), default: brain + CSF border
#   synthstrip_nocsf  mri_synthstrip --no-csf
#   hdbet1_fast_closed  existing hdbet/1.0.0 fast mask + calmar.brainmask.close_cavities (6 mm)
# and measures, against the expert lesion, how much lesion each mask excludes
# and how much it adds outside brain + lesion (python step, no tool).
# Usage: sbatch --array=0-40%10 src/analysis_40_compare_brain_extraction.sh <participants.json> <outdir>
set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$PROJECT_DIR"
CALMAR_PYTHON="${CALMAR_PYTHON:-$(command -v python)}"
LIST="${1:?participants.json}"; OUTROOT="${2:?output dir}"
read -r SUB SES T1 < <("$CALMAR_PYTHON" -c "import json,sys; r=json.load(open(sys.argv[1]))[int(sys.argv[2])]; print(r['subject'], r['session'], r['t1w'])" "$LIST" "${SLURM_ARRAY_TASK_ID:?array task}")
OUT="$OUTROOT/${SUB}_${SES}"
if [ -e "$OUT/metrics.json" ]; then echo "done already: $OUT"; exit 0; fi
mkdir -p "$OUTROOT"
TMP="$(mktemp -d "${OUT}.attempt.XXXXXX")"
trap 'rm -rf "$TMP"' EXIT
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-4}"
for v in OMP_NUM_THREADS; do export "APPTAINERENV_$v=$OMP_NUM_THREADS" "SINGULARITYENV_$v=$OMP_NUM_THREADS"; done
declare -A SECONDS_USED
time_it() { local name=$1; shift; local t0=$SECONDS; "$@"; SECONDS_USED[$name]=$((SECONDS - t0)); }

module purge; module load hdbet/1.0.0
time_it hdbet1_accurate hd-bet -i "$T1" -o "$TMP/hdbet1_accurate" -mode accurate -device cpu -tta 0
mv "$TMP/hdbet1_accurate_mask.nii.gz" "$TMP/hdbet1_accurate_mask.final.nii.gz"

module purge; module load hdbet/2.0.1
time_it hdbet2 hd-bet -i "$T1" -o "$TMP/hdbet2.nii.gz" -device cpu --save_bet_mask --no_bet_image
mv "$(ls "$TMP"/hdbet2*bet*.nii.gz | head -1)" "$TMP/hdbet2_mask.final.nii.gz"

module purge; module load synthstrip/7.4.1
time_it synthstrip_csf mri_synthstrip -i "$T1" -m "$TMP/synthstrip_csf_mask.final.nii.gz"
time_it synthstrip_nocsf mri_synthstrip -i "$T1" -m "$TMP/synthstrip_nocsf_mask.final.nii.gz" --no-csf

TIMES="{"; for k in "${!SECONDS_USED[@]}"; do TIMES+="\"$k\": ${SECONDS_USED[$k]},"; done; TIMES="${TIMES%,}}"
"$CALMAR_PYTHON" - "$LIST" "${SLURM_ARRAY_TASK_ID}" "$TMP" "$TIMES" <<'EOF'
import json, sys
sys.path.insert(0, '.')
import nibabel as nib, numpy as np
from nibabel.processing import resample_from_to
from calmar.brainmask import close_cavities, save_like
entry = json.load(open(sys.argv[1]))[int(sys.argv[2])]; d = sys.argv[3]
t1 = nib.load(entry['t1w']); vox = float(np.prod(t1.header.get_zooms()[:3])) / 1000
def on_t1(path):
    img = nib.load(path)
    if img.shape[:3] != t1.shape[:3] or not np.allclose(img.affine, t1.affine, atol=1e-3):
        img = resample_from_to(img, t1, order=0)
    return np.asarray(img.dataobj).reshape(t1.shape[:3]) > .5
expert = on_t1(entry['expert']); base = on_t1(entry['hdbet_fast'])
masks = {'hdbet1_fast': base}
closed = close_cavities(base, t1.header.get_zooms())
save_like(closed, t1, f'{d}/hdbet1_fast_closed_mask.final.nii.gz')
masks['hdbet1_fast_closed'] = closed
for name in ('hdbet1_accurate', 'hdbet2', 'synthstrip_csf', 'synthstrip_nocsf'):
    masks[name] = on_t1(f'{d}/{name}_mask.final.nii.gz')
out = {'subject': entry['subject'], 'session': entry['session'], 'expert_ml': round(expert.sum() * vox, 2),
       'seconds': json.loads(sys.argv[4]), 'masks': {}}
for name, m in masks.items():
    out['masks'][name] = {
        'volume_ml': round(m.sum() * vox, 1),
        'lesion_outside_frac': round(float((expert & ~m).sum() / max(expert.sum(), 1)), 4),
        'added_beyond_hdbet_and_lesion_ml': round(float((m & ~base & ~expert).sum() * vox), 1),
        'hdbet_brain_removed_ml': round(float((base & ~m & ~expert).sum() * vox), 1),
    }
json.dump(out, open(f'{d}/metrics.json', 'w'), indent=1)
print(json.dumps(out))
EOF
mkdir -p "$OUTROOT"; mv "$TMP" "$OUT"; trap - EXIT
echo "published $OUT"
