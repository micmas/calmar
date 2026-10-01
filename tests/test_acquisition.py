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

    def comparison_namespace(self):
        return dict(RUN_TEST=True, TEST_SUBJECT_IDX=0, Path=Path,
                    SUBJECTS=[dict(subject=self.sub, session=self.ses, t1w=self.t1)],
                    RAW_DATASET_DIR=self.root,
                    CONFIG=dict(MANUAL_MASK_PATH=None, OVERWRITE=False),
                    deriv_path_for=lambda e: self.root / "linda",
                    synthstroke_path_for=lambda e: self.root / "synth",
                    q=SimpleNamespace(coregister_t2_mask_to_t1=Mock(
                        side_effect=RuntimeError("registration reached"))),
                    importlib=SimpleNamespace(reload=lambda obj: obj),
                    HTML=lambda text: text, display=lambda *args: None)

    def test_comparison_fetches_discovered_mask_and_reference_before_registration(self):
        ns = self.comparison_namespace()
        with patch.dict("os.environ", {"RAW_DATASET_DIR": str(self.root)}), patch.object(
                acquisition.shutil, "which", return_value="datalad"), patch.object(
                acquisition.subprocess, "run", side_effect=self.fetch):
            with self.assertRaisesRegex(RuntimeError, "registration reached"):
                exec("".join(CELLS[29]["source"]), ns)
        self.assertEqual(self.calls, [self.mask, self.t2])
        args = ns["q"].coregister_t2_mask_to_t1.call_args.args
        self.assertEqual(args[:3], (self.t1, self.t2, self.mask))

    def test_comparison_reports_fetch_failure_without_registration(self):
        ns = self.comparison_namespace()
        output = io.StringIO()
        with patch.dict("os.environ", {"RAW_DATASET_DIR": str(self.root)}), patch.object(
                acquisition.shutil, "which", return_value="datalad"), patch.object(
                acquisition.subprocess, "run", return_value=SimpleNamespace(
                    returncode=1, stdout="", stderr="download failed")), contextlib.redirect_stdout(output):
            exec("".join(CELLS[29]["source"]), ns)
        ns["q"].coregister_t2_mask_to_t1.assert_not_called()
        self.assertIn("located but its content is unavailable", output.getvalue())
        self.assertIn("download failed", output.getvalue())

    def move_t1_to_other_session(self):
        self.t1.unlink()
        self.t1 = self.root / self.sub / "ses-t1only" / "anat" / f"{self.sub}_ses-t1only_T1w.nii.gz"
        self.t1.parent.mkdir(parents=True)
        nib.save(self.img, self.t1)
        # A T2 next to the T1 must not displace the annotation's actual source.
        nib.save(self.img, self.t1.with_name(f"{self.sub}_ses-t1only_T2w.nii.gz"))

    def test_comparison_uses_mask_source_session_when_t1_is_elsewhere(self):
        self.move_t1_to_other_session()
        ns = self.comparison_namespace()
        ns["SUBJECTS"][0]["session"] = "ses-t1only"
        with patch.dict("os.environ", {"RAW_DATASET_DIR": str(self.root)}), patch.object(
                acquisition.shutil, "which", return_value="datalad"), patch.object(
                acquisition.subprocess, "run", side_effect=self.fetch):
            with self.assertRaisesRegex(RuntimeError, "registration reached"):
                exec("".join(CELLS[29]["source"]), ns)
        self.assertEqual(self.calls, [self.mask, self.t2])
        self.assertEqual(ns["q"].coregister_t2_mask_to_t1.call_args.args[:3],
                         (self.t1, self.t2, self.mask))

    def test_batch_uses_mask_source_session_when_t1_is_elsewhere(self):
        self.move_t1_to_other_session()
        tree = ast.parse("".join(CELLS[47]["source"]))
        definitions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
        ns = dict(Path=Path, re=re, RAW_DATASET_DIR=self.root,
                  deriv_path_for=lambda e: self.root / "linda",
                  q=SimpleNamespace(mni_mask_matches_reference=lambda *a: False,
                      coregister_t2_mask_to_t1=Mock(side_effect=RuntimeError("registration reached"))),
                  ensure_nifti_content=acquisition.ensure_nifti_content)
        exec(compile(ast.Module(body=definitions, type_ignores=[]), "batch", "exec"), ns)
        with patch.object(acquisition.shutil, "which", return_value="datalad"), patch.object(
                acquisition.subprocess, "run", side_effect=self.fetch):
            with self.assertRaisesRegex(RuntimeError, "registration reached"):
                ns["_warp_manual_to_mni_batch"](
                    dict(subject=self.sub, session="ses-t1only", t1w=self.t1),
                    self.root / "derivatives" / "lesion_masks")
        self.assertEqual(self.calls, [self.mask, self.t2])
        self.assertEqual(ns["q"].coregister_t2_mask_to_t1.call_args.args[:3],
                         (self.t1, self.t2, self.mask))

    def test_batch_stops_on_unavailable_mask(self):
        tree = ast.parse("".join(CELLS[47]["source"]))
        definitions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
        ns = dict(Path=Path, RAW_DATASET_DIR=self.root,
                  deriv_path_for=lambda e: self.root / "linda",
                  q=SimpleNamespace(mni_mask_matches_reference=lambda *a: False),
                  ensure_nifti_content=Mock(return_value=False))
        exec(compile(ast.Module(body=definitions, type_ignores=[]), "batch", "exec"), ns)
        state, message = ns["_warp_manual_to_mni_batch"](
            dict(subject=self.sub, session=self.ses, t1w=self.t1),
            self.root / "derivatives" / "lesion_masks")
        self.assertEqual(state, "failed")
        self.assertIn("content unavailable", message)
        ns["ensure_nifti_content"].assert_called_once_with(self.mask, self.root)


if __name__ == "__main__":
    unittest.main()
