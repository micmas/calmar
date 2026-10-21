"""Exercise the actual notebook panels together using tiny synthetic fixtures."""

import json
from pathlib import Path
import tempfile
import textwrap
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch
from datetime import datetime
from matplotlib.backends.backend_pdf import PdfPages

import ipywidgets as widgets
from IPython.display import HTML
from ipyniivue import NiiVue
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
import pandas as pd

from calmar.atlas_ui import OverlapSelection
from calmar import widgets as cw


CELLS = {int(c["id"].rsplit("-", 1)[1]) - 1: c for c in json.loads((Path(__file__).resolve().parents[1] /
                    "lesion-interpretation-pipeline.ipynb").read_text())["cells"] if c["id"].startswith("calmar-step-")}


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
                       widgets=widgets, HTML=HTML, display=Mock(), datetime=datetime, PdfPages=PdfPages,
                       clear_output=lambda **kw: None, Path=Path, nib=nib, np=np,
                       plt=plt, textwrap=textwrap, DERIV_DIR=self.root,
                       REPORTS_DIR=self.root, ATLAS_DIR=self.root,
                       deriv_path_for=lambda e: self.root,
                       mask_inventory_for=lambda e: self.masks,
                       cw=SimpleNamespace(fresh_viewer=fresh, vols=lambda s: s, set_volumes=cw.set_volumes, Output=cw.Output))
        # Cells use study.linda_dir / study.masks; follow later namespace overrides.
        self.ns["study"] = SimpleNamespace(linda_dir=lambda e: self.ns["deriv_path_for"](e),
                                           template_dir=lambda e: self.ns["deriv_path_for"](e),
                                           masks=lambda e: self.ns["mask_inventory_for"](e))
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

    def test_cohort_menu_keeps_participants_without_positive_overlap(self):
        cohort = [('sub-test', ''), ('sub-zero', ''), ('sub-missing', 'ses-2')]
        sel = OverlapSelection(self.tables, 'Atlas_A', cohort)
        self.assertEqual([v for _, v in sel.subject.options], cohort)
        sel.subject.value = cohort[1]
        sel.atlas.value = 'Atlas_B'
        self.assertEqual(sel.subject.value, cohort[1])
        self.assertEqual([v for _, v in sel.subject.options], cohort)

    def test_empty_table_preserves_columns_and_cohort(self):
        empty = self.tables['Atlas_B_manual'].iloc[:0]
        sel = OverlapSelection({'Atlas_B_manual': empty}, 'Atlas_B', [('sub-zero', '')])
        self.assertEqual(sel.subject.value, ('sub-zero', ''))
        self.assertIn('subject', sel.current()[0])

    def test_one_preview_shares_selection_and_loads_brain_only_on_its_tab(self):
        self.run_cell(74)
        report = self.ns["_subject_report_panel"]
        for name in ("atlas_dd", "subj_dd", "src_dd", "_refresh_subjects", "_dirty"):
            self.ns[name] = None
        self.assertEqual(report["subject"].value, ("sub-test", ""))
        self.assertEqual(len(report["viewer"].volumes), 0)
        self.assertIn("Atlas_A", report["report"].value)
        self.assertIn("Manual mask", report["report"].value)
        report["tabs"].selected_index = 1
        self.assertEqual(len(report["viewer"].volumes), 3)
        brain = report["viewer"].volumes[0]
        self.assertEqual(Path(report["viewer"].volumes[0].path).name, "Subject_in_MNI.nii.gz")
        report["source"].value = "manual"
        self.assertEqual(Path(report["viewer"].volumes[-1].path).name, "manual.nii.gz")
        self.assertEqual(report["viewer"].volumes[-1].cal_min, .5)
        report["atlas"].value = "Atlas_B"
        self.assertEqual(report["viewer"].volumes[1].name, "Atlas_B_atlas.nii.gz")
        self.assertIs(report["viewer"].volumes[0], brain)
        self.assertTrue((self.root / "Atlas_B_atlas.nii.gz").exists())
        self.assertIn('Atlas_B', report['report'].value)
        self.assertIsNone(report['group'].selected_index)
        self.assertIsNone(report['state']['group_panel'])
        self.assertFalse(report['chart'].outputs)
        self.ns['display'].assert_called_once_with(report['widget'])
        self.assertEqual(len(self.viewers), 1)

    def test_report_explains_missing_brain_instead_of_showing_mask_as_background(self):
        (self.root / "Subject_in_MNI.nii.gz").unlink()
        self.run_cell(74)
        report = self.ns["_subject_report_panel"]
        report["tabs"].selected_index = 1
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
        self.run_cell(74)
        report = self.ns['_subject_report_panel']
        report['source'].value = 'manual'
        report['group_tabs'].selected_index = 1
        self.assertIsNone(report['state']['group_panel'])
        report['group'].selected_index = 0
        panel = report['state']['group_panel']
        self.assertIs(panel['source'], report['source'])
        self.assertFalse(list(self.root.glob("group_lesion_frequency*")))
        self.assertIsNone(panel['state']['viewer'])
        with patch('calmar.reporting.run_reporting_task', return_value={
                'map': str(moved), 'background': str(self.root/'Subject_in_MNI.nii.gz'), 'used': 2}) as submit:
            panel["compute"]()
        self.assertEqual(submit.call_args.args[1], 'group')
        self.assertIn(str(moved), submit.call_args.kwargs['masks'])
        viewer = panel['state']['viewer']
        self.assertEqual(len(viewer.volumes), 2)
        self.assertEqual(Path(viewer.volumes[-1].path).name,
                         "manual_moved.nii.gz")
        self.assertIsNone(viewer.volumes[0].cal_min)
        panel["source"].value = "linda"
        self.assertFalse(viewer.volumes)

    def test_optional_charts_stay_lazy_and_refresh_from_shared_mask_selection(self):
        self.tables['Schaefer400_manual'] = self.tables['Atlas_B_manual'].assign(region='LH_Vis_1')
        self.run_cell(74)
        panel = self.ns['_subject_report_panel']
        self.assertFalse(panel['chart'].outputs)
        self.assertFalse(panel['heatmap'].outputs)
        self.assertFalse(panel['networks'].outputs)
        panel['tabs'].selected_index = 2
        self.assertTrue(panel['chart'].outputs)
        panel['group'].selected_index = 0
        self.assertTrue(panel['heatmap'].outputs)
        panel['group_tabs'].selected_index = 2
        self.assertTrue(panel['networks'].outputs)
        panel['source'].value = 'linda'
        self.assertIn('unavailable', panel['networks'].outputs[0]['text'])
        self.assertIsNone(panel['state']['group_panel'])
        self.assertEqual(len(self.viewers), 1)

    def test_export_is_inside_preview_and_uses_current_selection(self):
        self.run_cell(74)
        self.run_cell(75)
        panel = self.ns['_subject_report_panel']
        self.assertEqual(len(panel['export'].children), 2)
        self.ns['display'].assert_called_once_with(panel['widget'])
        panel['atlas'].value = 'Atlas_B'
        panel['export'].children[0].click()
        path = self.root/'pdfs/sub-test_no-ses_Atlas_B_manual.pdf'
        self.assertTrue(path.read_bytes().startswith(b'%PDF'))

    def test_obsolete_panels_are_removed_from_both_workflows(self):
        for number in (67, 71, 72):
            self.assertNotIn(number-1, CELLS)
        from calmar.guided import source_cell
        self.assertIn('build_results_panel', ''.join(source_cell(74)['source']))

    def test_group_heatmap_distinguishes_zero_overlap_from_missing_results(self):
        from calmar.atlas_results import cohort_matrix
        df = self.tables['Atlas_B_manual'].fillna({'session': ''})
        df.attrs['overlap_status'] = {json.dumps(['sub-zero', '']): {'status': 'complete'}}
        matrix = cohort_matrix(df, [('sub-test', ''), ('sub-zero', ''), ('sub-missing', '')],
                               'lesion_in_roi_percent', 20)
        self.assertEqual(list(matrix.columns), ['sub-test', 'sub-zero', 'sub-missing'])
        self.assertEqual(matrix['sub-zero'].iloc[0], 0)
        self.assertTrue(np.isnan(matrix['sub-missing'].iloc[0]))

    def test_rerunning_preview_deactivates_the_old_panel(self):
        self.run_cell(74)
        old = self.ns['_subject_report_panel']
        old['group_tabs'].selected_index = 1
        old['group'].selected_index = 0
        self.run_cell(74)
        self.assertFalse(old['state']['active'])
        self.assertTrue(old['state']['group_panel']['build'].disabled)
        self.assertTrue(self.ns['_subject_report_panel']['state']['active'])


if __name__ == "__main__":
    unittest.main()
