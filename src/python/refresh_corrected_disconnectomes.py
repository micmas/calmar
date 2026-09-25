"""Preserve superseded files, publish inspected masks, and refresh dependents."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
from nibabel.processing import resample_from_to

dataset, corrected, report = map(lambda p: Path(p).resolve(), sys.argv[1:])
backup = corrected.parent / ("alignment-repair-backup-job" + os.environ["SLURM_JOB_ID"])
backup.mkdir(exist_ok=False)
affine = np.array([[-2, 0, 0, 90], [0, 2, 0, -126], [0, 0, 2, -72], [0, 0, 0, 1]], dtype=float)
metrics = {}
inspected = json.loads((corrected / "metrics.json").read_text())


def preserve(path):
    if path.exists():
        dst = backup / path.relative_to(dataset)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dst)


def publish(tmp, final, output_id):
    subprocess.run(["neurodesk-astra-provenance", "publish", str(tmp), str(final),
                    "--output-id", output_id, "--tool", "python", "--script", __file__,
                    "--replace"], check=True)


for subject in inspected:
    sub, ses = subject.split("/")
    assert inspected[subject]["linda"]["before_after_dice"] == 1.0
    linda = dataset / "derivatives/linda" / sub / ses / "anat"
    synth = dataset / "derivatives/synthstroke" / sub / ses / "anat"
    dd = dataset / "derivatives/deepdisco" / sub / ses / "anat"
    for token, target in [("expert", linda / "ExpertMask_in_MNI.nii.gz"),
                          ("synthstroke", synth / "SynthStroke_in_MNI.nii.gz")]:
        source = corrected / sub / ses / target.name
        ref = nib.load(linda / "Subject_in_MNI.nii.gz")
        image = nib.load(source)
        assert image.shape == ref.shape and np.allclose(image.affine, ref.affine)
        preserve(target)
        for sidecar in [target.with_name(target.name + ".prov.json"),
                        target.with_name(target.name.replace(".nii.gz", ".qc.json"))]:
            preserve(sidecar)
        # Remove only dependents of the changed mask, after preserving originals.
        for path in sorted(dd.glob(f"*_{token}*")):
            if path.is_file():
                preserve(path)
                path.unlink()
        for path in target.parent.glob(target.name.replace(".nii.gz", "") + "_boundary*.nii.gz"):
            preserve(path)
            path.unlink()
        with tempfile.TemporaryDirectory(prefix=target.name + ".attempt.", dir=target.parent) as td:
            tmp = Path(td) / target.name
            # Re-serialize so the file timestamp invalidates caches of the old mask.
            nib.save(image, tmp)
            publish(tmp, target, "corrected_mni_masks")
        mask2 = resample_from_to(image, ((91, 109, 91), affine), order=0)
        input2 = dd / f"_deepdisco_input_{token}.nii.gz"
        nib.save(nib.Nifti1Image((mask2.get_fdata() > .5).astype(np.uint8), affine), input2)
        for model, code in [("association", "ASS"), ("projection", "PRO"),
                            ("commissural", "COM"), ("whole_brain", "WHO")]:
            final = dd / f"DeepDisco_{token}_{model}.nii.gz"
            with tempfile.TemporaryDirectory(prefix=final.name + ".attempt.", dir=dd) as td:
                tmp = Path(td) / final.name
                subprocess.run(["deepdisco-cli", "--input", str(input2), "--model", code,
                                "--output", str(tmp)], check=True, timeout=300)
                im = nib.load(tmp); values = im.get_fdata(dtype=np.float32)
                assert values.shape == (91, 109, 91) and np.isfinite(values).all()
                assert float(values.min()) >= 0 and float(values.max()) <= 1.00001
                key = f"{subject}/{token}/{model}"
                metrics[key] = {"min": float(values.min()), "max": float(values.max()),
                                "nonzero": int(np.count_nonzero(values))}
                publish(tmp, final, "refreshed_deepdisco_maps")
                if model == "whole_brain":
                    fig, axes = plt.subplots(1, 3, figsize=(10, 3))
                    bg = resample_from_to(ref, im, order=1).get_fdata(dtype=np.float32)
                    for axis, ax in enumerate(axes):
                        cut = values.shape[axis] // 2
                        ax.imshow(np.take(bg, cut, axis=axis).T, origin="lower", cmap="gray")
                        plane = np.take(values, cut, axis=axis).T
                        ax.imshow(np.ma.masked_where(plane <= .1, plane), origin="lower",
                                  cmap="hot", alpha=.65, vmin=.1, vmax=1)
                        ax.axis("off")
                    fig.suptitle(f"{sub} {ses} {token}: corrected-input DeepDisco whole brain")
                    fig.tight_layout()
                    fig.savefig(report / f"{sub}_{ses}_{token}_deepdisco.png", dpi=110)
                    plt.close(fig)
                print(key, metrics[key], flush=True)
(report / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n")
(report / "backup_path.txt").write_text(str(backup) + "\n")
