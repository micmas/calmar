#!/bin/bash
#SBATCH --job-name=openads_metrics
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:20:00
#SBATCH --mem=8G
#SBATCH --cpus-per-task=2

# Per-subject OpenADS-vs-expert metrics (Dice, IoU, volume difference, HD95,
# mean surface distance) on the ISLES-2022 cohort manifest, plus a QC montage
# PNG. Metric definitions match lesion-segmentation-benchmark.ipynb §5/§10:
# prediction is resampled to the expert-mask grid (nearest neighbour),
# binarised at >0, surface distances computed on eroded-boundary EDTs.
# Pure Python on main-env packages (nibabel/nilearn/scipy/pandas/matplotlib);
# no neuroimaging module required.

set -euo pipefail

PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "${PROJECT_DIR}"

python3 - <<'PY'
import numpy as np
import pandas as pd
import nibabel as nib
from pathlib import Path
from nilearn.image import resample_to_img
from scipy.ndimage import binary_erosion, distance_transform_edt

DS = Path("data/ISLES-2022")
OUT_DIR = Path("reports/benchmarks")
MANIFEST = OUT_DIR / "cohort_isles2022.tsv"


def binarise(img):
    return (img.get_fdata() > 0).astype(np.uint8)


def dice_iou(a, b):
    a = a.astype(bool); b = b.astype(bool)
    inter = int((a & b).sum()); s = int(a.sum()) + int(b.sum())
    union = s - inter
    return ((2 * inter / s) if s else float("nan"),
            (inter / union) if union else float("nan"))


def surface_distances(a, b, zooms):
    out = {"hd95_mm": float("nan"), "mean_surf_mm": float("nan")}
    if a.sum() == 0 or b.sum() == 0:
        return out
    def boundary(m):
        return m & ~binary_erosion(m, iterations=1)
    ba = boundary(a.astype(bool)); bb = boundary(b.astype(bool))
    if ba.sum() == 0 or bb.sum() == 0:
        return out
    dt_b = distance_transform_edt(~bb, sampling=zooms)
    dt_a = distance_transform_edt(~ba, sampling=zooms)
    d = np.concatenate([dt_b[ba], dt_a[bb]])
    return {"hd95_mm": float(np.percentile(d, 95)),
            "mean_surf_mm": float(d.mean())}


rows, panels = [], []
for line in MANIFEST.read_text().splitlines():
    sub, ses = line.split("\t")
    ref_p = DS / "derivatives" / sub / ses / f"{sub}_{ses}_msk.nii.gz"
    pred_p = (DS / "derivatives" / "openads" / sub / ses / "dwi"
              / f"{sub}_{ses}_space-DWI_desc-lesion_mask.nii.gz")
    row = {"subject": sub, "session": ses, "tool": "openads",
           "pred_exists": pred_p.exists(), "error": ""}
    if not pred_p.exists():
        row["error"] = "prediction missing"
        rows.append(row); continue
    ref_img, pred_img = nib.load(ref_p), nib.load(pred_p)
    pred_rs = resample_to_img(pred_img, ref_img, interpolation="nearest")
    ref, pred = binarise(ref_img), binarise(pred_rs)
    vv = float(np.prod(ref_img.header.get_zooms()[:3]))
    row["dice"], row["iou"] = dice_iou(ref, pred)
    row["ref_vol_ml"] = ref.sum() * vv / 1000.0
    row["pred_vol_ml"] = pred.sum() * vv / 1000.0
    row["vol_diff_ml"] = row["pred_vol_ml"] - row["ref_vol_ml"]
    row.update(surface_distances(ref, pred, ref_img.header.get_zooms()[:3]))
    rows.append(row)
    panels.append((sub, ref_p, pred_p))

df = pd.DataFrame(rows)
tmp = OUT_DIR / "openads_isles2022_metrics.csv.tmp"
df.to_csv(tmp, index=False)
tmp.rename(OUT_DIR / "openads_isles2022_metrics.csv")

done = df[df.pred_exists]
print(f"{len(done)}/{len(df)} subjects with predictions")
if len(done):
    print(done[["dice", "iou", "vol_diff_ml", "hd95_mm"]]
          .describe().loc[["mean", "std", "50%", "min", "max"]].round(3))

# ── QC montage: worst / median / best Dice subjects, expert vs prediction ──
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

scored = done.dropna(subset=["dice"]).sort_values("dice")
if len(scored):
    idx = sorted({0, len(scored) // 2, len(scored) - 1})
    sel = scored.iloc[idx]
    fig, axes = plt.subplots(1, len(sel), figsize=(5 * len(sel), 5))
    axes = np.atleast_1d(axes)
    for ax, (_, r) in zip(axes, sel.iterrows()):
        sub, ses = r.subject, r.session
        dwi = nib.load(DS / sub / ses / "dwi" / f"{sub}_{ses}_dwi.nii.gz")
        ref_img = nib.load(DS / "derivatives" / sub / ses / f"{sub}_{ses}_msk.nii.gz")
        pred_img = nib.load(DS / "derivatives" / "openads" / sub / ses / "dwi"
                            / f"{sub}_{ses}_space-DWI_desc-lesion_mask.nii.gz")
        ref = binarise(ref_img)
        pred = binarise(resample_to_img(pred_img, ref_img, interpolation="nearest"))
        dwi_rs = resample_to_img(dwi, ref_img, force_resample=True,
                                 copy_header=True).get_fdata()
        if dwi_rs.ndim == 4:
            dwi_rs = dwi_rs[..., 0]
        z = int(np.argmax(ref.sum(axis=(0, 1)))) if ref.any() \
            else int(np.argmax(pred.sum(axis=(0, 1)))) if pred.any() \
            else ref.shape[2] // 2
        ax.imshow(dwi_rs[:, :, z].T, cmap="gray", origin="lower")
        ax.contour(ref[:, :, z].T, levels=[0.5], colors="lime", linewidths=1.2)
        if pred[:, :, z].any():
            ax.contour(pred[:, :, z].T, levels=[0.5], colors="red", linewidths=1.2)
        ax.set_title(f"{sub}\nDice {r.dice:.2f}  (green=expert, red=OpenADS)",
                     fontsize=9)
        ax.axis("off")
    fig.suptitle("OpenADS on ISLES-2022 — worst / median / best Dice", fontsize=11)
    fig.tight_layout()
    tmp_png = OUT_DIR / "openads_isles2022_qc.png.tmp.png"
    fig.savefig(tmp_png, dpi=130, bbox_inches="tight")
    tmp_png.rename(OUT_DIR / "openads_isles2022_qc.png")
    print(f"QC montage → {OUT_DIR / 'openads_isles2022_qc.png'}")
PY
