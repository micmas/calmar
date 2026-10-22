"""Annex discovery/fetch regressions using tiny images and mocked downloads."""

import ast
import contextlib
import io
import json
import re
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

import nibabel as nib
import numpy as np

from calmar import acquisition


ROOT = Path(__file__).resolve().parents[1]
CELLS = {int(c["id"].rsplit("-", 1)[1]) - 1: c for c in json.loads((ROOT / "lesion-interpretation-pipeline.ipynb").read_text())["cells"] if c["id"].startswith("calmar-step-")}


class AcquisitionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / ".datalad").mkdir()
        self.img = nib.Nifti1Image(np.ones((3, 3, 3), dtype=np.uint8), np.eye(4))
        self.sub, self.ses = "sub-M2035", "ses-4295"
        stem = f"{self.sub}_{self.ses}_acq-spc3_run-3_T2w"
        self.mask = self.root / "derivatives" / "lesion_masks" / self.sub / self.ses / "anat" / (stem + "_desc-lesion_mask.nii.gz")
        self.t2 = self.root / self.sub / self.ses / "anat" / (stem + ".nii.gz")
        for index, path in enumerate((self.mask, self.t2)):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.symlink_to(self.root / f"annex-object-{index}.nii.gz")
        self.t1 = self.t2.with_name(f"{self.sub}_{self.ses}_T1w.nii.gz")
        nib.save(self.img, self.t1)
        self.calls = []

    def fetch(self, command, **kwargs):
        self.assertEqual(command[:2], ["bash", str(ROOT / "src" / "analysis_18_fetch_nifti_content.sh")])
        self.assertEqual(command[2], str(self.root))
        relative = Path(command[3])
        self.assertFalse(relative.is_absolute())
        logical = self.root / relative
        self.assertIn(logical, (self.mask, self.t2))
        self.calls.append(logical)
        nib.save(self.img, logical.resolve())
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    def test_small_valid_image_needs_no_download(self):
        self.assertLess(self.t1.stat().st_size, 10_000)
        with patch.object(acquisition.subprocess, "run") as run:
            self.assertTrue(acquisition.ensure_nifti_content(self.t1))
        run.assert_not_called()

    def test_broken_annex_link_is_fetched_by_logical_dataset_path(self):
        self.assertFalse(self.mask.exists())
        with patch.object(acquisition.shutil, "which", return_value="datalad"), patch.object(
                acquisition.subprocess, "run", side_effect=self.fetch):
            self.assertTrue(acquisition.ensure_nifti_content(self.mask))
        self.assertTrue(self.mask.is_symlink())
        self.assertEqual(self.calls, [self.mask])

    def test_success_exit_without_valid_content_is_rejected(self):
        self.mask.resolve().write_text("annex pointer, not an image")
        with patch.object(acquisition.shutil, "which", return_value="datalad"), patch.object(
                acquisition.subprocess, "run", return_value=SimpleNamespace(
                    returncode=0, stdout="nothing fetched", stderr="")):
            self.assertFalse(acquisition.ensure_nifti_content(self.mask, self.root))

    def test_discovery_preserves_annotation_session(self):
        from calmar.processing import manual_inputs
        entry = dict(subject=self.sub, session="ses-other", t1w=self.t1)
        mask, reference, space = manual_inputs(dict(dataset=str(self.root), config={}), entry)
        self.assertEqual((mask, reference, space), (self.mask, self.t2, "other"))
        self.assertFalse(mask.exists())  # Discovery does not materialize content.

    def test_acquisition_failure_stops_before_registration(self):
        from calmar.processing import process
        request=dict(dataset=str(self.root),config={},entries=[dict(subject=self.sub,session=self.ses,t1w=str(self.t1))])
        with patch.dict("os.environ", {"SLURM_JOB_ID":"fixture"}), patch("calmar.processing.ensure_nifti_content",return_value=False), patch("calmar.qc.coregister_t2_mask_to_t1") as register:
            with self.assertRaisesRegex(RuntimeError,"Acquisition failed"):
                process("acquisition",request)
        register.assert_not_called()

    def test_acquisition_reports_dwi_in_same_and_other_sessions_without_fetching_it(self):
        from calmar.processing import process
        dwi = self.root / self.sub / "ses-dwi" / "dwi" / f"{self.sub}_ses-dwi_dwi.nii.gz"
        request = dict(dataset=str(self.root), config={"MANUAL_MASK_ROOT": str(self.root / "no-manual")}, entries=[dict(
            subject=self.sub, session=self.ses, t1w=str(self.t1),
            dwi_inventory=[dict(dwi=str(dwi), session="ses-dwi", same_session=False, openads_ready=False)])])
        with patch.dict("os.environ", {"SLURM_JOB_ID": "fixture"}), patch(
                "calmar.processing.ensure_nifti_content", return_value=True) as fetch:
            result = process("acquisition", request)[0]
        self.assertEqual(fetch.call_count, 1)  # selected T1 only; arbitrary DWI remains metadata-only
        self.assertEqual(result["qc"]["metrics"], {
            "dwi_series_available": 1, "dwi_sessions_available": "ses-dwi",
            "dwi_same_session": 0, "dwi_other_session": 1, "dwi_openads_ready": 0})


if __name__ == "__main__":
    unittest.main()
