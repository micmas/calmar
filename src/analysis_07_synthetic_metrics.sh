#!/bin/bash
#SBATCH --job-name=syn_metrics
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:20:00
#SBATCH --mem=8G
#SBATCH --cpus-per-task=2

# Cross-tool metrics on the synthetic datasets: every tool's mask (LINDA,
# SynthStroke, OpenADS) against the exact implanted ground truth, for both
# phases — the co-registered synthetic modalities make the three tools
# directly comparable per subject despite their different required inputs.
# Writes decision-qualified cross-tool metrics and a QC montage
# (one row per phase: GT contour + each tool's contour on the same subject).
# Metric definitions identical to analysis_03 / notebook §5/§10.

set -euo pipefail
source /opt/neurodesktop/agent_bash_env.sh

PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "${PROJECT_DIR}"

PROFILE="${1:-historical_baseline}"
HDBET_MODE="${2:-fast}"
LINDA_SEED="${3:-historical_unseeded}"
case "${PROFILE}" in
    historical_baseline) SYNTH_TAG="synthstroke-${PROFILE}" ;;
    calmar_current) SYNTH_TAG="synthstroke-${PROFILE}-hdbet-${HDBET_MODE}" ;;
    *) echo "invalid SynthStroke profile: ${PROFILE}" >&2; exit 2 ;;
esac
case "${LINDA_SEED}" in
    historical_unseeded) SEED_TAG="unseeded" ;;
    seed1729) SEED_TAG="seed1729" ;;
    *) echo "invalid LINDA seed: ${LINDA_SEED}" >&2; exit 2 ;;
esac
LINDA_TAG="linda-hdbet-${HDBET_MODE}-${SEED_TAG}"
RUN_TAG="${PROFILE}_hdbet-${HDBET_MODE}_${SEED_TAG}"
FINAL_CSV="reports/benchmarks/synthetic_crosstool_${RUN_TAG}_metrics.csv"
FINAL_PNG="reports/benchmarks/synthetic_crosstool_${RUN_TAG}_qc.png"
if [ -e "${FINAL_CSV}" ] && [ -e "${FINAL_PNG}" ]; then
    [ -s "${FINAL_CSV}" ] && [ -s "${FINAL_PNG}" ] && \
        [ -s "${FINAL_CSV}.prov.json" ] && [ -s "${FINAL_PNG}.prov.json" ] || {
        echo "completed metric set lacks data or provenance; preserve or remove it before retrying" >&2
        exit 1
    }
    echo "decision-specific metrics and QC already exist with provenance: ${RUN_TAG}"
    exit 0
fi
if [ -e "${FINAL_CSV}" ] || [ -e "${FINAL_PNG}" ]; then
    echo "only part of the final metric set exists; preserve or remove it before retrying" >&2
    exit 1
fi
mkdir -p reports/benchmarks
TMP_DIR="$(mktemp -d reports/benchmarks/.crosstool-metrics.attempt.XXXXXX)"
trap 'rm -rf "${TMP_DIR}"' EXIT
TMP_CSV="${TMP_DIR}/synthetic_crosstool_metrics.csv"
TMP_PNG="${TMP_DIR}/synthetic_crosstool_qc.png"

python3 - "${TMP_CSV}" "${TMP_PNG}" "${LINDA_TAG}" "${SYNTH_TAG}" <<'PY'
import sys
import numpy as np
import pandas as pd
import nibabel as nib
from pathlib import Path
from nilearn.image import resample_to_img
from scipy.ndimage import binary_erosion, distance_transform_edt

OUT_DIR = Path("reports/benchmarks")
CSV_OUT, PNG_OUT = map(Path, sys.argv[1:3])
TOOLS = {"linda":       (sys.argv[3], "anat", "T1w"),
         "synthstroke": (sys.argv[4], "anat", "T1w"),
         "openads":     ("openads", "dwi", "DWI")}


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


rows = []
for phase, tag in [("acute", "synacu"), ("chronic", "synchr")]:
    ds = Path(f"data/synthetic_{phase}")
    derivatives = Path(f"derivatives/segmentation-benchmark/synthetic_{phase}")
    for i in range(6):
        sub = f"sub-{tag}00{i}"
        ref_p = ds / "derivatives" / sub / f"{sub}_msk.nii.gz"
        if not ref_p.exists():
            continue
        ref_img = nib.load(ref_p)
        ref = binarise(ref_img)
        vv = float(np.prod(ref_img.header.get_zooms()[:3]))
        for tool, (tool_dir, mod, space) in TOOLS.items():
            pred_p = (derivatives / tool_dir / sub / mod
                      / f"{sub}_space-{space}_desc-lesion_mask.nii.gz")
            row = {"phase": phase, "subject": sub, "tool": tool,
                   "pred_exists": pred_p.exists(), "error": ""}
            if not pred_p.exists():
                row["error"] = "prediction missing"
                rows.append(row); continue
            pred = binarise(resample_to_img(nib.load(pred_p), ref_img,
                                            interpolation="nearest"))
            row["dice"], row["iou"] = dice_iou(ref, pred)
            row["ref_vol_ml"] = ref.sum() * vv / 1000.0
            row["pred_vol_ml"] = pred.sum() * vv / 1000.0
            row["vol_diff_ml"] = row["pred_vol_ml"] - row["ref_vol_ml"]
            row.update(surface_distances(ref, pred,
                                         ref_img.header.get_zooms()[:3]))
            rows.append(row)

df = pd.DataFrame(rows)
df.to_csv(CSV_OUT, index=False)

done = df[df.pred_exists & df.dice.notna()] if "dice" in df else df.iloc[0:0]
print(f"{int(df.pred_exists.sum())}/{len(df)} tool×subject pairs with predictions")
if len(done):
    print(done.groupby(["phase", "tool"])["dice"]
          .agg(["count", "mean", "std", "median"]).round(3))

# ── QC montage: per phase, one subject (median OpenADS-Dice if available),
#    T1w background, GT + all three tool contours ──
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

COLORS = {"gt": "lime", "linda": "red", "synthstroke": "orange",
          "openads": "cyan"}
fig, axes = plt.subplots(1, 2, figsize=(11, 5.5))
for ax, (phase, tag) in zip(axes, [("acute", "synacu"), ("chronic", "synchr")]):
    ds = Path(f"data/synthetic_{phase}")
    derivatives = Path(f"derivatives/segmentation-benchmark/synthetic_{phase}")
    ph = done[done.phase == phase]
    if len(ph):
        med = ph.groupby("subject")["dice"].mean().sort_values()
        sub = med.index[len(med) // 2]
    else:
        sub = f"sub-{tag}000"
    ref_img = nib.load(ds / "derivatives" / sub / f"{sub}_msk.nii.gz")
    ref = binarise(ref_img)
    t1 = resample_to_img(nib.load(ds / sub / "anat" / f"{sub}_T1w.nii.gz"),
                         ref_img, force_resample=True, copy_header=True).get_fdata()
    z = int(np.argmax(ref.sum(axis=(0, 1)))) if ref.any() else ref.shape[2] // 2
    ax.imshow(t1[:, :, z].T, cmap="gray", origin="lower")
    ax.contour(ref[:, :, z].T, levels=[0.5], colors=COLORS["gt"], linewidths=1.6)
    handles = [plt.Line2D([], [], color=COLORS["gt"], label="ground truth")]
    for tool, (tool_dir, mod, space) in TOOLS.items():
        p = (derivatives / tool_dir / sub / mod
             / f"{sub}_space-{space}_desc-lesion_mask.nii.gz")
        if not p.exists():
            continue
        pred = binarise(resample_to_img(nib.load(p), ref_img,
                                        interpolation="nearest"))
        if pred[:, :, z].any():
            ax.contour(pred[:, :, z].T, levels=[0.5],
                       colors=COLORS[tool], linewidths=1.1)
        d = done[(done.subject == sub) & (done.tool == tool)]["dice"]
        lbl = f"{tool} (Dice {float(d.iloc[0]):.2f})" if len(d) else tool
        handles.append(plt.Line2D([], [], color=COLORS[tool], label=lbl))
    ax.legend(handles=handles, fontsize=7, loc="lower right")
    ax.set_title(f"{phase}: {sub} (T1w background)", fontsize=10)
    ax.axis("off")
fig.suptitle("Synthetic cross-tool benchmark — all tools vs exact ground truth",
             fontsize=11)
fig.tight_layout()
fig.savefig(PNG_OUT, dpi=130, bbox_inches="tight")
print(f"QC montage prepared → {PNG_OUT}")
PY
[ "$(wc -l < "${TMP_CSV}")" -gt 1 ] || { echo "metrics table has no data rows" >&2; exit 1; }
identify "${TMP_PNG}"
neurodesk-astra-provenance publish "${TMP_CSV}" "${FINAL_CSV}" \
    --output-id crosstool_metrics --tool python3 --script "$0"
if ! neurodesk-astra-provenance publish "${TMP_PNG}" "${FINAL_PNG}" \
    --output-id crosstool_qc --tool python3 --script "$0"; then
    mv "${FINAL_CSV}" "${TMP_DIR}/rollback_metrics.csv"
    mv "${FINAL_CSV}.prov.json" "${TMP_DIR}/rollback_metrics.prov.json"
    exit 1
fi
