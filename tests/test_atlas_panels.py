"""Exercise the actual notebook panels together using tiny synthetic fixtures."""

import json
from pathlib import Path
import tempfile
import textwrap
from types import SimpleNamespace
import unittest
from unittest.mock import Mock

import ipywidgets as widgets
from IPython.display import HTML
from ipyniivue import NiiVue
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
import pandas as pd

from calmar_atlas_ui import OverlapSelection


CELLS = json.loads((Path(__file__).resolve().parents[1] /
                    "lesion-interpretation-pipeline.ipynb").read_text())["cells"]


class AtlasPanelTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.entry = dict(subject="sub-test", session=None)
        row = dict(subject="sub-test", session=np.nan, region="Example ROI",
                   lesion_in_roi_percent=20., roi_coverage_percent=5.,
                   overlap_voxels=2, total_lesion_voxels=10)
        self.tables = {key: pd.DataFrame([row]) for key in
                       ("Atlas_A_linda", "Atlas_A_manual", "Atlas_B_manual")}
        # Historical cached rows should never select an unavailable current subject.
        self.tables["Atlas_A_linda"] = pd.DataFrame([
            dict(row, subject="sub-historical"), row])
        self.img = nib.Nifti1Image(np.ones((3, 3, 3), dtype=np.uint8), np.eye(4))
        self.masks = {}
        for source in ("linda", "manual", "synthstroke"):
            path = self.root / f"{source}.nii.gz"
            nib.save(self.img, path)
            self.masks[source] = {"MNI": path}
        nib.save(self.img, self.root / "Subject_in_MNI.nii.gz")
        nib.save(self.img, self.root / "mni152_t1_2mm.nii.gz")
        nib.save(self.img, self.root / "Atlas_A_atlas.nii.gz")
        self.viewers = []
        def fresh(*args, **kwargs):
            nv = NiiVue(height=kwargs.get("height", 300))
            self.viewers.append(nv)
            self.addCleanup(nv.close)
            return nv
        self.ns = dict(OVERLAP_DFS=self.tables, SUBJECTS=[self.entry],
                       CONFIG={"DEFAULT_ATLAS": "Atlas_A", "LESION_THRESHOLD": .5},
                       ALL_ATLASES={"Atlas_B": SimpleNamespace(maps=self.img)},
                       widgets=widgets, HTML=HTML, display=lambda *a: None,
                       clear_output=lambda **kw: None, Path=Path, nib=nib, np=np,
                       plt=plt, textwrap=textwrap, DERIV_DIR=self.root,
                       REPORTS_DIR=self.root, ATLAS_DIR=self.root,
                       deriv_path_for=lambda e: self.root,
                       mask_inventory_for=lambda e: self.masks,
                       cw=SimpleNamespace(fresh_viewer=fresh, vols=lambda s: s))
        self.addCleanup(lambda: plt.close("all"))

    def run_cell(self, number):
        exec("".join(CELLS[number - 1]["source"]), self.ns)

    def test_valid_combinations_and_session_normalization(self):
        sel = OverlapSelection(self.tables, "Atlas_A")
        seen = []
        sel.observe(lambda **kw: seen.append(sel.current()))
        sel.atlas.value = "Atlas_B"
        self.assertEqual(sel.source.value, "manual")
        self.assertEqual(sel.subject.value, ("sub-test", ""))
        self.assertEqual(len(seen), 1)
        self.assertEqual(seen[0][0]["session"].iloc[0], "")
        self.assertEqual(sel.source.options, (("Manual", "manual"),))
        self.assertTrue(pd.isna(self.tables["Atlas_B_manual"]["session"].iloc[0]))

    def test_later_report_keeps_earlier_controls_independent_and_loads_brain(self):
        self.run_cell(71)
        earlier = self.ns["_atlas_overlap_panel"]
        self.run_cell(74)
        report = self.ns["_subject_report_panel"]
        for name in ("atlas_dd", "subj_dd", "src_dd", "_refresh_subjects", "_dirty"):
            self.ns[name] = None
        self.assertEqual(report["subject"].value, ("sub-test", ""))
        self.assertEqual(len(report["viewer"].volumes), 3)
        self.assertEqual(Path(report["viewer"].volumes[0].path).name, "Subject_in_MNI.nii.gz")
        report["source"].value = "manual"
        self.assertEqual(Path(report["viewer"].volumes[-1].path).name, "manual.nii.gz")
        self.assertEqual(report["viewer"].volumes[-1].cal_min, .5)
        report["atlas"].value = "Atlas_B"
        self.assertEqual(report["viewer"].volumes[1].name, "Atlas_B.nii")
        self.assertTrue(report["viewer"].volumes[1].data)
        self.assertEqual(earlier["atlas"].value, "Atlas_A")
        earlier["atlas"].value = "Atlas_B"
        self.assertEqual(earlier["source"].value, "manual")
        self.assertEqual(earlier["current"]()[0]["session"].iloc[0], "")
        self.assertEqual(len(self.viewers), 1)

    def test_report_explains_missing_brain_instead_of_showing_mask_as_background(self):
        (self.root / "Subject_in_MNI.nii.gz").unlink()
        self.run_cell(74)
        report = self.ns["_subject_report_panel"]
        self.assertFalse(report["viewer"].volumes)
        self.assertIn("Brain viewer needs Subject_in_MNI", report["message"].value)

    def test_group_source_selection_defers_computation_and_checks_affines(self):
        second = dict(subject="sub-other", session=None)
        moved = self.root / "manual_moved.nii.gz"
        affine = np.eye(4); affine[0, 3] = 1
        nib.save(nib.Nifti1Image(np.ones((3, 3, 3), dtype=np.uint8), affine), moved)
        resample = Mock(return_value=self.img)
        self.ns.update(SUBJECTS=[self.entry, second],
                       image=SimpleNamespace(resample_to_img=resample),
                       mask_inventory_for=lambda e: self.masks if e == self.entry else
                       {"manual": {"MNI": moved}})
        self.run_cell(67)
        panel = self.ns["_group_overlap_panel"]
        panel["source"].value = "manual"
        self.assertFalse(list(self.root.glob("group_lesion_frequency*")))
        panel["compute"]()
        resample.assert_called_once()
        self.assertEqual(len(panel["viewer"].volumes), 2)
        self.assertEqual(Path(panel["viewer"].volumes[-1].path).name,
                         "group_lesion_frequency_manual.nii.gz")
        self.assertIsNone(panel["viewer"].volumes[0].cal_min)
        panel["source"].value = "linda"
        self.assertFalse(panel["viewer"].volumes)


if __name__ == "__main__":
    unittest.main()
