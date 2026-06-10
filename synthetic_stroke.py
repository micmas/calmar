"""
synthetic_stroke.py — controlled stroke DWI + ADC + T1w phantom generator.

Open datasets with native-space DWI **and** ADC plus lesion masks are scarce
(ISLES 2022 is essentially the only auto-downloadable one; the gold-standard
Faria/ICPSR set is access-gated). This module synthesises controlled stand-ins
so the benchmark's tools can be exercised against a perfect ground truth.

Each subject is a brain-shaped volume (from the MNI152 template) with 1-3
implanted ellipsoidal lesions. Three co-registered modalities are written —
T1w, DWI, ADC — plus the binary mask. Because they share one grid, every
modality is perfectly co-registered to the ground truth (Dice/HD95 are exact).

Two phases (choose per dataset), reflecting stroke-imaging physiology:
  * "acute"  (<~1 wk): cytotoxic edema -> restricted diffusion.
        DWI HYPER-intense, ADC HYPO-intense (~350, below the ~620 ischemic-core
        threshold), T1w only subtly hypointense (acute stroke is faint on T1 —
        which is exactly why chronic T1 tools struggle; a realistic transfer
        baseline). Targets OpenADS (DWI+ADC).
  * "chronic"(>~6 mo): encephalomalacia / gliosis.
        T1w DARK cavity (CSF-like), ADC ELEVATED (free water), DWI
        pseudonormalized (no longer bright). Targets LINDA / SynthStroke (T1w).

ADC value choices follow the acute-stroke literature: normal parenchyma
~800e-6 mm2/s, ischemic-core threshold ~<=620, severe/irreversible <550, free
water (CSF / chronic cavity) ~3000.

CAVEAT: synthetic lesions are cleaner and more separable than real stroke, and
the modalities here are perfectly co-registered (no acquisition/registration
error). Treat this as a controlled pipeline + gross-detectability sanity
benchmark, not a measure of real-world accuracy.

Output layout (mirrors the ISLES BIDS layout discover()/OpenADS expect):
    <target>/<sub>/anat/<sub>_T1w.nii.gz
    <target>/<sub>/dwi/<sub>_dwi.nii.gz
    <target>/<sub>/dwi/<sub>_adc.nii.gz
    <target>/derivatives/<sub>/<sub>_msk.nii.gz

Run `python synthetic_stroke.py` for an offline self-test (no nilearn/network).
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import nibabel as nib


def _gen_one_synthetic(sub: str, target: Path, rng: "np.random.RandomState",
                       mni_img: "nib.Nifti1Image", brain_mask: "np.ndarray",
                       phase: str = "acute") -> dict:
    """Generate one synthetic subject's T1w, DWI, ADC and ground-truth mask.

    Args:
        sub:        subject id, e.g. "sub-synacu000"
        target:     dataset root to write into
        rng:        seeded numpy RandomState (reproducibility)
        mni_img:    anatomical scaffold (nibabel image; T1-like intensities)
        brain_mask: boolean ndarray, same grid as mni_img
        phase:      "acute" or "chronic" — sets the per-modality lesion signature

    Returns a dict of the written paths and the lesion voxel count.
    """
    from scipy.ndimage import gaussian_filter

    target = Path(target)
    aff = mni_img.affine
    t1 = mni_img.get_fdata().astype(np.float32)
    bm = np.asarray(brain_mask, dtype=bool)

    # Normalise the template within brain to [0, 1].
    t = np.zeros_like(t1)
    if bm.any():
        v = t1[bm]
        lo, hi = np.percentile(v, [2, 98])
        t[bm] = np.clip((t1[bm] - lo) / (hi - lo + 1e-6), 0, 1)
    csf = bm & (t < 0.25)                        # ventricles/CSF: dark on T1

    # ── Modality bases (healthy brain; lesion added afterward, per phase) ──
    # DWI: tissue moderate, CSF dark (suppressed at high b).
    dwi = np.zeros_like(t); dwi[bm] = 600 + 250 * t[bm]; dwi[csf] = 120
    # ADC: tissue moderate, CSF very bright (free water).
    adc = np.zeros_like(t); adc[bm] = 800 + 100 * (1 - t[bm]); adc[csf] = 3000
    # T1w: the MNI template is itself T1-weighted; rescale to a clean range.
    t1max = np.percentile(t1[bm], 98) if bm.any() else (float(t1.max()) or 1.0)
    t1w = np.clip(t1 / (t1max + 1e-6), 0, 1.5) * 700.0      # tissue ~0-1050

    # Implant 1-3 ellipsoidal lesions in deep tissue (WM/GM).
    mask = np.zeros(t.shape, np.uint8)
    wm_idx = np.argwhere(bm & (t > 0.45) & (t < 0.9))
    if len(wm_idx) == 0:                          # degenerate scaffold safeguard
        wm_idx = np.argwhere(bm)
    zz, yy, xx = np.ogrid[:t.shape[0], :t.shape[1], :t.shape[2]]
    for _ in range(int(rng.randint(1, 4))):
        c = wm_idx[rng.randint(len(wm_idx))]
        r = rng.uniform(4, 9, size=3)            # voxel radii (~8-18 mm at 2 mm)
        ell = (((zz - c[0]) / r[0])**2 + ((yy - c[1]) / r[1])**2
               + ((xx - c[2]) / r[2])**2) <= 1.0
        mask[ell & bm] = 1
    les = mask > 0

    # ── Phase-dependent lesion signature ──
    if phase == "chronic":
        t1w[les] = 60.0            # dark cavity (encephalomalacia, CSF-like)
        adc[les] = 2200.0          # elevated (free water / gliosis)
        dwi[les] = 500.0           # pseudonormalized — no longer bright
    else:                          # "acute"
        dwi[les] = 1400.0          # hyperintense (restricted diffusion)
        adc[les] = 350.0           # hypointense (restricted, below ~620 core)
        t1w[les] = t1w[les] * 0.85  # subtle hypointensity (near-isointense)

    # Smooth + brain-limited noise for realism.
    dwi = np.clip(gaussian_filter(dwi, 0.8) + rng.normal(0, 15, t.shape) * bm,
                  0, None).astype(np.float32)
    adc = np.clip(gaussian_filter(adc, 0.8) + rng.normal(0, 20, t.shape) * bm,
                  0, None).astype(np.float32)
    head = t1 > 0
    t1w = np.clip(gaussian_filter(t1w, 0.6) + rng.normal(0, 12, t1.shape) * head,
                  0, None).astype(np.float32)

    # Write: T1w (anat/), DWI + ADC siblings (dwi/), mask (derivatives/).
    anat_dir = target / sub / "anat"; anat_dir.mkdir(parents=True, exist_ok=True)
    t1w_path = anat_dir / f"{sub}_T1w.nii.gz"
    nib.save(nib.Nifti1Image(t1w, aff), str(t1w_path))

    dwi_dir = target / sub / "dwi"; dwi_dir.mkdir(parents=True, exist_ok=True)
    dwi_path = dwi_dir / f"{sub}_dwi.nii.gz"
    adc_path = dwi_dir / f"{sub}_adc.nii.gz"
    nib.save(nib.Nifti1Image(dwi, aff), str(dwi_path))
    nib.save(nib.Nifti1Image(adc, aff), str(adc_path))

    mdir = target / "derivatives" / sub; mdir.mkdir(parents=True, exist_ok=True)
    msk_path = mdir / f"{sub}_msk.nii.gz"
    nib.save(nib.Nifti1Image(mask, aff), str(msk_path))

    return {"t1w": t1w_path, "dwi": dwi_path, "adc": adc_path, "mask": msk_path,
            "lesion_voxels": int(les.sum()), "phase": phase}


def synthetic_install(target, *, n_subjects: int = 6, seed: int = 7,
                      phase: str = "acute", prefix: str | None = None) -> bool:
    """Generate a synthetic stroke dataset of the given phase if not present.

    Idempotent: skips when at least n_subjects subjects (with T1w) already exist.
    `prefix` defaults to a phase-specific subject prefix so acute and chronic
    cohorts never collide on subject id. Returns True on success.
    """
    from nilearn import datasets as _nlds

    target = Path(target)
    if prefix is None:
        prefix = "sub-synacu" if phase == "acute" else "sub-synchr"

    # Key idempotency off the T1w so older datasets (pre-T1w / wrong phase)
    # are regenerated rather than skipped.
    existing = (sorted(target.glob(f"{prefix}*/anat/*_T1w.nii.gz"))
                if target.exists() else [])
    if len(existing) >= n_subjects:
        print(f"  ✔  synthetic {phase} dataset present ({len(existing)} subjects)")
        return True

    print(f"  generating {n_subjects} synthetic {phase.upper()} subjects "
          f"(T1w+DWI+ADC) → {target} …")
    mni = _nlds.load_mni152_template(resolution=2)
    # Brain mask (fall back to a template threshold if loader/grid differs).
    try:
        bm_img = _nlds.load_mni152_brain_mask(resolution=2)
        bm = bm_img.get_fdata() > 0
        if bm.shape != mni.shape:
            raise ValueError("grid mismatch")
    except Exception:
        d = mni.get_fdata()
        bm = d > (0.15 * d.max())

    for i in range(n_subjects):
        sub = f"{prefix}{i:03d}"
        info = _gen_one_synthetic(sub, target,
                                  np.random.RandomState(seed * 1000 + i), mni, bm,
                                  phase=phase)
        print(f"    ✔ {sub}  ({info['lesion_voxels']:,} lesion voxels)")

    try:
        (target / "dataset_description.json").write_text(
            '{"Name": "Synthetic %s stroke (T1w+DWI+ADC phantom)", '
            '"BIDSVersion": "1.9.0"}' % phase)
    except Exception:
        pass
    print(f"  ✔  synthetic {phase} dataset ready ({n_subjects} subjects)")
    return True


def _make_fake_template(grid: int = 60, seed: int = 0):
    """Build a brain-like scaffold (no nilearn/network) for offline testing."""
    zz, yy, xx = np.ogrid[:grid, :grid, :grid]
    c = grid / 2
    brain = (((zz - c) / 22)**2 + ((yy - c) / 26)**2 + ((xx - c) / 20)**2) <= 1
    t1 = np.zeros((grid, grid, grid), np.float32)
    t1[brain] = np.random.RandomState(seed).uniform(0.3, 1.0, size=int(brain.sum()))
    vent = (((zz - c) / 6)**2 + ((yy - c) / 6)**2 + ((xx - c) / 6)**2) <= 1
    t1[vent] = 0.1
    img = nib.Nifti1Image(t1, np.eye(4))
    return img, (t1 > 0.001)


def _self_test() -> int:
    """Offline smoke test: generate an acute and a chronic subject from a fake
    template and verify the per-phase modality signatures and on-disk layout."""
    import tempfile, shutil

    tmp = Path(tempfile.mkdtemp(prefix="synth_stroke_test_"))
    mni, bm = _make_fake_template()
    ok = True
    for phase, sub in (("acute", "sub-synacu000"), ("chronic", "sub-synchr000")):
        info = _gen_one_synthetic(sub, tmp, np.random.RandomState(7), mni, bm,
                                  phase=phase)
        for p in (tmp / sub / "anat" / f"{sub}_T1w.nii.gz",
                  tmp / sub / "dwi" / f"{sub}_dwi.nii.gz",
                  tmp / sub / "dwi" / f"{sub}_adc.nii.gz",
                  tmp / "derivatives" / sub / f"{sub}_msk.nii.gz"):
            if not p.exists():
                print(f"  ✘ missing output: {p}"); ok = False

        t1w = nib.load(str(info["t1w"])).get_fdata()
        dwi = nib.load(str(info["dwi"])).get_fdata()
        adc = nib.load(str(info["adc"])).get_fdata()
        msk = nib.load(str(info["mask"])).get_fdata() > 0
        brain = (mni.get_fdata() > 0.001) & ~msk

        if phase == "acute":
            checks = {
                "mask non-empty":      msk.sum() > 0,
                "DWI lesion brighter": dwi[msk].mean() > dwi[brain].mean(),
                "ADC lesion darker":   adc[msk].mean() < adc[brain].mean(),
            }
        else:
            checks = {
                "mask non-empty":      msk.sum() > 0,
                "T1w lesion darker":   t1w[msk].mean() < t1w[brain].mean(),
                "ADC lesion elevated": adc[msk].mean() > adc[brain].mean(),
                "DWI not hyperbright": dwi[msk].mean() <= dwi[brain].mean() * 1.1,
            }
        for name, passed in checks.items():
            print(f"  {'✔' if passed else '✘'} {phase}/{sub}: {name}")
            ok &= bool(passed)
        print(f"    T1w lesion={t1w[msk].mean():.0f} brain={t1w[brain].mean():.0f} | "
              f"DWI lesion={dwi[msk].mean():.0f} brain={dwi[brain].mean():.0f} | "
              f"ADC lesion={adc[msk].mean():.0f} brain={adc[brain].mean():.0f}")

    shutil.rmtree(tmp, ignore_errors=True)
    print("SELF-TEST:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    import sys
    sys.exit(_self_test())
