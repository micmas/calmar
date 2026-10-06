#!/bin/bash
#SBATCH --job-name=edge_metrics
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:20:00
#SBATCH --mem=8G
#SBATCH --cpus-per-task=2

# Score every tool found under data/synthetic_edgecases/derivatives/ against
# the battery's ground truth, per category. Tools are discovered
# automatically (any derivatives/<tool>/ dir holding *_desc-lesion_mask
# files) — adding a new tool requires no change here.
# Beyond Dice, reports the edge-case-relevant quantities:
#   detection    — any voxel overlap with GT (per subject)
#   fp_vol_ml    — predicted volume on lesion-NEGATIVE subjects
#   distractor_overlap_ml — predicted volume inside the mixed-chronology
#                  chronic distractor (should be 0 for an acute DWI tool)
# Writes reports/benchmarks/edgecase_metrics.csv + per-category summary.

set -euo pipefail

PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "${PROJECT_DIR}"

python3 - <<'PY'
import numpy as np
import pandas as pd
import nibabel as nib
from pathlib import Path
from nilearn.image import resample_to_img

DS = Path("data/synthetic_edgecases")
OUT = Path("reports/benchmarks")

manifest = pd.read_csv(DS / "participants.tsv", sep="\t")
tools = sorted(p.name for p in (DS / "derivatives").iterdir()
               if p.is_dir() and not p.name.startswith("sub-")
               and any(p.rglob("*_desc-lesion_mask.nii.gz")))
print(f"tools found: {tools}")

rows = []
for _, r in manifest.iterrows():
    sub, phase, cat = r.participant_id, r.phase, r.category
    ref_img = nib.load(DS / "derivatives" / sub / f"{sub}_msk.nii.gz")
    ref = ref_img.get_fdata() > 0
    vv = float(np.prod(ref_img.header.get_zooms()[:3]))
    dis_p = DS / "derivatives" / sub / f"{sub}_desc-distractorchronic_msk.nii.gz"
    dis = nib.load(dis_p).get_fdata() > 0 if dis_p.exists() else None
    for tool in tools:
        hits = list((DS / "derivatives" / tool / sub).rglob(
            "*_desc-lesion_mask.nii.gz"))
        row = {"subject": sub, "phase": phase, "category": cat, "tool": tool,
               "pred_exists": bool(hits)}
        if hits:
            pred = resample_to_img(nib.load(hits[0]), ref_img,
                                   interpolation="nearest").get_fdata() > 0
            inter = int((pred & ref).sum())
            s = int(pred.sum()) + int(ref.sum())
            row["dice"] = 2 * inter / s if s else np.nan   # NaN: both empty
            row["ref_vol_ml"] = ref.sum() * vv / 1000
            row["pred_vol_ml"] = pred.sum() * vv / 1000
            row["detection"] = bool(inter) if ref.any() else np.nan
            row["fp_vol_ml"] = (pred.sum() * vv / 1000
                                if not ref.any() else np.nan)
            row["distractor_overlap_ml"] = ((pred & dis).sum() * vv / 1000
                                            if dis is not None else np.nan)
        rows.append(row)

df = pd.DataFrame(rows)
tmp = OUT / "edgecase_metrics.csv.tmp"
df.to_csv(tmp, index=False)
tmp.rename(OUT / "edgecase_metrics.csv")
print(f"→ {OUT / 'edgecase_metrics.csv'}  ({len(df)} rows)")

done = df[df.pred_exists]
if len(done):
    summary = (done.groupby(["category", "tool"])
               .agg(n=("subject", "count"),
                    dice_mean=("dice", "mean"),
                    detect_rate=("detection", "mean"),
                    fp_vol_ml=("fp_vol_ml", "mean"),
                    distractor_ml=("distractor_overlap_ml", "mean"))
               .round(3))
    print(summary.to_string())
PY
