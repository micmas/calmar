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

from calmar.overlay import mask_comparison
from calmar import qc as q


class Viewer(widgets.HTML):
    def load_volumes(self, specs):
        self.loaded = specs


class AlignmentDisplayTests(unittest.TestCase):
    def test_comparison_is_read_only_and_manual_processing_precedes_it(self):
        from calmar.guided import source_cell
        from unittest.mock import Mock
        namespace = {"RUN_TEST": True, "SUBJECTS": [{"subject": "sub-a"}], "TEST_SUBJECT_IDX": 0,
                     "study": None, "BATCH_TIMINGS": {}}
        # Manual-mask processing is its own step after SynthStroke; its viewer and
        # summary replace the separate registration/mask review cell.
        from calmar.guided import notebook_cells
        ids = [c.get("id") for c in notebook_cells()]
        self.assertLess(ids.index("calmar-step-27"), ids.index("calmar-manual"))
        self.assertNotIn("calmar-step-30", ids)
        run = Mock()
        namespace.update(submit_step=run, show_step=Mock())
        if True:
            exec("".join(source_cell(27)["source"]), namespace)
            exec("".join(next(c for c in notebook_cells() if c.get("id") == "calmar-manual")["source"]), namespace)
        self.assertEqual([c.args[0] for c in run.call_args_list], ["synthstroke", "manual"])

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
        source = "".join(next(c for c in n["cells"] if c.get("id") == "calmar-step-12")["source"])
        assignment = next(node for node in ast.parse(source).body
                          if isinstance(node, ast.Assign) and any(
                              isinstance(t, ast.Name) and t.id == "CONFIG" for t in node.targets))
        ns = {"Path": Path}
        exec(compile(ast.Module(body=[assignment], type_ignores=[]), "config", "exec"), ns)
        config = ns["CONFIG"]
        self.assertCountEqual(config["SUBJECT_FILTER"], ["sub-M2234", "sub-M2173", "sub-M2030"])
        self.assertCountEqual(config["SESSION_FILTER"], ["ses-715", "ses-590", "ses-1454"])
        self.assertEqual(config["MAX_SUBJECTS"], 3)
        self.assertEqual(config["BCB_MASKS"], "all")
        self.assertEqual(config["DEEPDISCO_MASK_SOURCE"], "all")
        self.assertTrue(config["DEEPDISCO_RUN_ALL"])
        self.assertFalse(config["OVERWRITE"])


if __name__ == "__main__":
    unittest.main()
