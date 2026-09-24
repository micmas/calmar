"""Regression tests for sparse overlays, coordinate-space caches and run config."""
import ast
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import ipywidgets as widgets
import nibabel as nib
import numpy as np
from ipyniivue import NiiVue

from calmar_overlay import mask_comparison
import linda_qc as q


class Viewer(widgets.HTML):
    def load_volumes(self, specs):
        self.loaded = specs


class AlignmentDisplayTests(unittest.TestCase):
    def test_comparison_cell_prepares_manual_mni_for_disconnectome_cells(self):
        root = Path(__file__).resolve().parents[1]
        cells = json.loads((root / "lesion-interpretation-pipeline.ipynb").read_text())["cells"]
        with tempfile.TemporaryDirectory() as td:
            folder = Path(td)
            t1, manual = folder / "T1w.nii.gz", folder / "manual.nii.gz"
            img = nib.Nifti1Image(np.ones((3, 3, 3), dtype=np.uint8), np.eye(4))
            nib.save(img, t1); nib.save(img, manual)
            calls = []
            def warp(linda_dir, native, output, **kwargs):
                calls.append((linda_dir, native, output))
                nib.save(nib.load(native), output)
                return 0
            ns = dict(RUN_TEST=True, TEST_SUBJECT_IDX=0, Path=Path, nib=nib, np=np,
                      SUBJECTS=[dict(subject="sub-test", session="ses-1", t1w=t1)],
                      CONFIG=dict(MANUAL_MASK_PATH=str(manual), MANUAL_MASK_SPACE="t1",
                                  OVERWRITE=False),
                      deriv_path_for=lambda e: folder,
                      synthstroke_path_for=lambda e: folder / "synth",
                      q=SimpleNamespace(warp_native_mask_to_mni=warp),
                      importlib=SimpleNamespace(reload=lambda obj: obj),
                      image=SimpleNamespace(resample_to_img=lambda a, b, **kw: a),
                      HTML=lambda text: text, display=lambda *args: None, cw=None)
            with patch("shutil.which", return_value=None), patch("calmar_overlay.mask_comparison"):
                exec("".join(cells[29]["source"]), ns)
            self.assertEqual(len(calls), 1)
            self.assertEqual(calls[0][2], folder / "ExpertMask_in_MNI.nii.gz")
            self.assertTrue(calls[0][2].exists())

    def test_sparse_overlays_have_binary_ranges_and_independent_controls(self):
        viewer = NiiVue()
        self.addCleanup(viewer.close)
        cw = SimpleNamespace(fresh_viewer=lambda *a, **kw: viewer, vols=lambda x: x)
        data = nib.Nifti1Image(np.ones((3, 3, 3), dtype=np.uint8), np.eye(4)).to_bytes()
        ui = mask_comparison(cw, "test", [
            {"data": data, "name": "T1"},
            {"data": data, "name": "Manual", "colormap": "blue", "opacity": .5},
            {"data": data, "name": "SynthStroke", "colormap": "green", "opacity": .85},
        ])
        self.addCleanup(ui.close)
        original = list(viewer.volumes)
        self.assertEqual(len(original), 3)
        for volume in original[1:]:
            self.assertEqual((volume.cal_min, volume.cal_max), (.5, 1.0))
        ui.children[0].children[1].value = False
        self.assertEqual([v.opacity for v in viewer.volumes], [1.0, .5, 0.0])
        ui.children[0].children[0].value = False
        self.assertEqual([v.opacity for v in viewer.volumes], [1.0, 0.0, 0.0])
        ui.children[0].children[1].value = True
        self.assertEqual([v.opacity for v in viewer.volumes], [1.0, 0.0, .85])
        self.assertTrue(all(a is b for a, b in zip(original, viewer.volumes)))

    def test_penn_grid_is_rejected_as_mni_even_when_filename_says_mni(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            shape = (3, 4, 5)
            nib.save(nib.Nifti1Image(np.zeros(shape), np.eye(4)), root / "Subject_in_MNI.nii.gz")
            path = root / "ExpertMask_in_MNI.nii.gz"
            wrong_affine = np.eye(4); wrong_affine[1, 3] = 13
            nib.save(nib.Nifti1Image(np.zeros(shape), wrong_affine), path)
            self.assertFalse(q.mni_mask_matches_reference(root, path))
            nib.save(nib.Nifti1Image(np.zeros(shape), np.eye(4)), path)
            self.assertTrue(q.mni_mask_matches_reference(root, path))
            path.unlink()
            self.assertFalse(q.mni_mask_matches_reference(root, path))

    def test_new_subject_and_all_mask_settings(self):
        root = Path(__file__).resolve().parents[1]
        n = json.loads((root / "lesion-interpretation-pipeline.ipynb").read_text())
        source = "".join(n["cells"][11]["source"])
        assignment = next(node for node in ast.parse(source).body
                          if isinstance(node, ast.Assign) and any(
                              isinstance(t, ast.Name) and t.id == "CONFIG" for t in node.targets))
        ns = {"Path": Path}
        exec(compile(ast.Module(body=[assignment], type_ignores=[]), "config", "exec"), ns)
        config = ns["CONFIG"]
        self.assertEqual(config["SUBJECT_FILTER"], ["sub-M2018", "sub-M2034"])
        self.assertEqual(config["SESSION_FILTER"], ["ses-341", "ses-1568"])
        self.assertEqual(config["MAX_SUBJECTS"], 2)
        self.assertEqual(config["BCB_MASKS"], "all")
        self.assertEqual(config["DEEPDISCO_MASK_SOURCE"], "all")
        self.assertTrue(config["DEEPDISCO_RUN_ALL"])
        self.assertFalse(config["OVERWRITE"])


if __name__ == "__main__":
    unittest.main()
