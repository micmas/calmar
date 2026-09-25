"""Check moved resource dispatch without running R or neuroimaging tools."""

import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from calmar import qc


class ScriptPathTests(unittest.TestCase):
    def test_warp_dispatch_preserves_arguments_and_finds_resources_outside_repo(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for name in ("native.nii.gz", "Subject_in_MNI.nii.gz",
                         "Reg3_sub_to_template_warp.nii.gz",
                         "Reg3_sub_to_template_affine.mat"):
                (root / name).touch()
            previous = Path.cwd()
            try:
                os.chdir(root)
                with patch.object(qc.subprocess, "run", return_value=SimpleNamespace(returncode=1)) as run:
                    self.assertEqual(qc.warp_native_mask_to_mni(
                        root, root / "native.nii.gz", root / "output.nii.gz"), 1)
            finally:
                os.chdir(previous)
            args, kwargs = run.call_args
            command = args[0]
            self.assertTrue(Path(command[1]).is_file())
            self.assertEqual(Path(command[1]).name, "analysis_15_warp_native_to_mni.sh")
            self.assertEqual(command[command.index("--reference") + 1], str(root / "Subject_in_MNI.nii.gz"))
            source = Path(kwargs["env"]["CALMAR_SOURCE_DIR"])
            self.assertTrue((source / "r" / "warp_native_mask_to_ch2.R").is_file())

    def test_linda_fallback_keeps_options_and_finds_moved_r_stub(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            with patch("shutil.which", return_value=None), patch.object(
                    qc.subprocess, "run", return_value=SimpleNamespace(returncode=1)) as run:
                rc = qc.run_linda_with_mask(root / "T1.nii.gz", root / "mask.nii.gz",
                                            root / "linda", verbose=False, cache=False)
            self.assertEqual(rc, 1)
            args, kwargs = run.call_args
            command = args[0]
            self.assertEqual(Path(command[1]).name, "analysis_17_linda_predict_with_mask.sh")
            self.assertTrue(Path(command[1]).is_file())
            self.assertEqual(command[-2:], ["--quiet", "--no-cache"])
            self.assertEqual(command[command.index("--mask") + 1], str(root / "mask.nii.gz"))
            self.assertTrue(qc._LINDA_R_STUB.is_file())
            self.assertEqual(qc._LINDA_R_STUB,
                             Path(kwargs["env"]["CALMAR_SOURCE_DIR"]) / "r" / "linda_predict_with_mask.R")


if __name__ == "__main__":
    unittest.main()
