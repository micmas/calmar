"""Slurm side of the DICOM import (src/analysis_45_dicom_to_nifti.sh).

Runs dcm2niix (loaded by the script) on the requested DICOM folder and
publishes the NIfTI images, their JSON sidecars and a summary listing every
series with a guessed role (:func:`calmar.local_import.guess_role`) to the job's
result folder. The dataset itself is not touched; the notebook imports the
series the user chose (:func:`calmar.local_import.import_images`).
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from .processing import publish


def convert(dicom_dir, out_dir):
    """dcm2niix → gzipped NIfTI + BIDS sidecars named <series number>_<protocol>."""
    command = ["dcm2niix", "-z", "y", "-b", "y", "-ba", "y", "-f", "%3s_%p", "-o", str(out_dir), str(dicom_dir)]
    done = subprocess.run(command, capture_output=True, text=True)
    (Path(out_dir) / "dcm2niix.log").write_text(" ".join(command) + "\n\n" + done.stdout + done.stderr)
    if done.returncode not in (0, 2):        # 2 = no DICOM found; reported as an empty list
        raise RuntimeError(f"dcm2niix failed ({done.returncode}): {done.stderr[-2000:]}")


def series(out_dir, final_dir):
    """One record per converted image, with paths as they will be after publishing."""
    from .local_import import check_image, guess_role
    records = []
    for nifti in sorted(Path(out_dir).glob("*.nii.gz")):
        sidecar = nifti.with_name(nifti.name[:-7] + ".json")
        meta = json.loads(sidecar.read_text()) if sidecar.exists() else {}
        meta["bvec"] = nifti.with_name(nifti.name[:-7] + ".bvec").exists()
        try:
            shape = list(check_image(nifti)["shape"])
        except ValueError:
            shape = None                      # e.g. a raw 4-D diffusion series: listed, not importable
        records.append({"nifti": str(Path(final_dir) / nifti.name),
                        "json": str(Path(final_dir) / sidecar.name) if sidecar.exists() else None,
                        "SeriesDescription": meta.get("SeriesDescription"), "ProtocolName": meta.get("ProtocolName"),
                        "ImageType": meta.get("ImageType"), "shape": shape,
                        "guess": guess_role(meta) if shape else None})
    return records


def main():
    request_path, output = map(Path, sys.argv[1:])
    if output.exists():
        raise FileExistsError(output)
    request = json.loads(request_path.read_text())
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=output.name + ".attempt.", dir=output.parent) as d:
        tmp = Path(d) / "receipt"
        images = tmp / "images"
        images.mkdir(parents=True)
        convert(request["dicom_dir"], images)
        value = series(images, output / "images")
        (tmp / "summary.json").write_text(json.dumps({"request": request, "value": value, "results": [],
                                                      "job": os.environ.get("SLURM_JOB_ID"),
                                                      "stage": "dicom_import"}, indent=2))
        publish(tmp, output, "dicom_import")


if __name__ == "__main__":
    main()
