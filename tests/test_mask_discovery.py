"""Regression checks using temporary file stubs; no imaging jobs or downloads."""

import datetime
import importlib
import importlib.metadata
import json
from pathlib import Path
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import ipywidgets as widgets
from IPython.display import HTML
import packaging

from calmar import masks as cm
from calmar import qc as q


ROOT = Path(__file__).resolve().parents[1]
CELLS = {int(c["id"].rsplit("-", 1)[1]) - 1: c for c in json.loads((ROOT / "lesion-interpretation-pipeline.ipynb").read_text())["cells"] if c["id"].startswith("calmar-step-")}


def cell(number):
    return "".join(CELLS[number - 1]["source"])


class Viewer(widgets.HTML):
    def load_volumes(self, volumes):
        self.loaded = volumes


class MaskDiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.entries = [dict(subject="sub-test", session=s, t1w=self.root / f"{s}_T1w.nii.gz")
                        for s in ("ses-1", "ses-2", "ses-3")]
        for e in self.entries:
            self.touch(e["t1w"])

    def touch(self, p):
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"nonempty test fixture")
        return p

    def linda(self, e):
        return self.root / "linda" / e["subject"] / e["session"] / "anat"

    def synth(self, e):
        return self.root / "synthstroke" / e["subject"] / e["session"] / "anat"

    def inventory(self, e):
        return cm.discover_masks(e, self.linda(e), self.synth(e))

    def stages(self, e):
        return cm.qc_stages(self.inventory(e),
                            brain_mask=self.linda(e) / "BrainMask.nii.gz",
                            mni_reference=self.linda(e) / "Subject_in_MNI.nii.gz")

    def test_synthstroke_only_and_sessions(self):
        e = self.entries[0]
        native = self.touch(self.synth(e) / "prediction_lesion_mask.nii.gz")
        self.assertEqual(self.inventory(e), {"synthstroke": {"T1w": native}})
        self.assertEqual(self.stages(e), ["synthstroke_lesion"])
        self.assertFalse(self.linda(e).exists())
        self.assertEqual(self.inventory(self.entries[1]), {})
        mni = self.touch(self.synth(e) / "SynthStroke_in_MNI.nii.gz")
        self.assertEqual(self.inventory(e)["synthstroke"]["MNI"], mni)

    def test_missing_empty_and_unfetched_masks(self):
        e = self.entries[0]
        self.synth(e).mkdir(parents=True)
        (self.synth(e) / "prediction_lesion_mask.nii.gz").touch()
        (self.synth(e) / "SynthStroke_in_MNI.nii.gz").symlink_to(self.root / "unfetched")
        self.assertEqual(self.inventory(e), {})

    def test_manual_space_is_explicit(self):
        e = self.entries[0]
        manual = self.touch(self.root / "manual.nii.gz")
        for declared, expected in (("t1", "T1w"), ("mni", "MNI")):
            found = cm.discover_masks(e, self.linda(e), self.synth(e),
                                     manual_path=manual, manual_space=declared)
            self.assertEqual(found, {"manual": {expected: manual}})
        self.assertEqual(cm.discover_masks(e, self.linda(e), self.synth(e),
                                          manual_path=manual, manual_space="other"), {})

    def test_legacy_precedence_and_bids_fallback(self):
        e = self.entries[0]
        bids = self.touch(self.linda(e) / "sub-test_ses-1_space-T1w_desc-lesion_mask.nii.gz")
        self.assertEqual(self.inventory(e)["linda"]["T1w"], bids)
        legacy = self.touch(self.linda(e) / "Prediction3_native.nii.gz")
        self.assertEqual(self.inventory(e)["linda"]["T1w"], legacy)

    def test_qc_sidecar_survives_later_linda_output(self):
        e = self.entries[0]
        anchor = self.linda(e) / "Lesion_in_MNI.nii.gz"
        rec = q.QCRecord.load(anchor)
        rec.subject, rec.session = e["subject"], e["session"]
        rec.set_stage("synthstroke_lesion", rating=1, notes="reviewed")
        rec.set_stage("manual_lesion", rating=2)
        rec.save()
        self.assertFalse(anchor.exists())
        self.touch(anchor)
        reloaded = q.QCRecord.load(anchor)
        self.assertEqual(reloaded.get_stage("synthstroke_lesion")["notes"], "reviewed")
        self.assertEqual(reloaded.get_stage("manual_lesion")["rating"], 2)

    def test_qc_widget_selects_available_stages_and_saves_without_linda(self):
        first, second, _ = self.entries
        self.touch(self.synth(first) / "prediction_lesion_mask.nii.gz")
        self.touch(self.linda(second) / "_manual_mask_compare" / "ManualLesion_in_T1.nii.gz")
        self.touch(self.linda(second) / "ExpertMask_in_MNI.nii.gz")
        self.touch(self.linda(second) / "Subject_in_MNI.nii.gz")
        viewer = Viewer()
        self.addCleanup(viewer.close)
        class Widgets:
            fresh_viewer = staticmethod(lambda *a, **kw: viewer)
            vols = staticmethod(lambda v: v)
        class StopExecution(Exception):
            pass
        ns = dict(importlib=importlib, q=q, cm=cm, SUBJECTS=self.entries,
                  mask_inventory_for=self.inventory, qc_available_stages=self.stages,
                  lesion_mni_for=lambda e: self.linda(e) / "Lesion_in_MNI.nii.gz",
                  deriv_path_for=self.linda, synthstroke_path_for=self.synth,
                  _mask_path_for=lambda e, s: self.inventory(e).get(s, {}).get("MNI", self.root / "absent"),
                  Path=Path, widgets=widgets, HTML=HTML, cw=Widgets, _dt=datetime,
                  display=lambda *a: None, clear_output=lambda **kw: None,
                  StopExecution=StopExecution)
        with patch.object(importlib, "reload", lambda x: x), patch.object(q, "ensure_lesion_boundary", lambda p, **kw: p), patch("calmar.execution.pause_for_qc") as pause:
            pause.return_value = SimpleNamespace(message=widgets.HTML(), do_qc=widgets.Button(),
                skip_qc=widgets.Button(), choose=lambda choice: True, choice=None,
                _update_cell_order=lambda *args: None)
            with self.assertRaises(StopExecution):
                exec(cell(51), ns)
            pause.assert_called_once_with(self.entries, self.linda, display_controls=False)
            self.assertEqual(len(ns["qc_pool"]), 2)
            panel = ns["_qc_panel"]
            self.addCleanup(panel.close)
            self.assertEqual(panel.stage.value, "synthstroke_lesion")
            panel.rating_buttons["synthstroke_lesion"].value = 1
            self.assertTrue(panel.save_participant())
            self.assertEqual(panel.subject.value, 1)
            self.assertEqual(panel.stage.value, "expert_mni_warp")
            self.assertNotIn("manual_lesion", panel.rating_buttons)
            panel.rating_buttons["expert_mni_warp"].value = 2
            self.assertTrue(panel.save_current())
            saved = q.QCRecord.load(self.linda(second) / "Lesion_in_MNI.nii.gz")
            self.assertEqual(saved.get_stage("expert_mni_warp")["rating"], 2)

    def test_report_selector_filters_masks_and_handles_no_mni(self):
        first, second, third = self.entries
        self.touch(self.synth(first) / "SynthStroke_in_MNI.nii.gz")
        self.touch(self.linda(second) / "ExpertMask_in_MNI.nii.gz")
        self.touch(self.synth(third) / "prediction_lesion_mask.nii.gz")
        class StopExecution(Exception):
            pass
        ns = dict(SUBJECTS=self.entries, INTERP_SUBJECT_IDX=0, INTERP_MASK_SOURCE="linda",
                  INTERP_MASK_LABELS=cm.MASK_LABELS, widgets=widgets, HTML=HTML,
                  available_mni_sources=lambda e: [s for s, spaces in self.inventory(e).items() if "MNI" in spaces],
                  display=lambda *a: None, clear_output=lambda **kw: None,
                  StopExecution=StopExecution)
        with self.assertRaises(StopExecution):
            exec(cell(79), ns)
        self.addCleanup(ns["_report_inputs"].close)
        self.assertEqual(ns["INTERP_MASK_SOURCE"], "synthstroke")
        ns["_rp_subj"].value = 1
        self.assertEqual(ns["INTERP_MASK_SOURCE"], "manual")
        ns["_rp_subj"].value = 2
        self.assertIsNone(ns["INTERP_MASK_SOURCE"])
        self.assertTrue(ns["_rp_mask"].disabled)


class SetupTests(unittest.TestCase):
    def test_install_skipped_when_packages_present(self):
        with patch("subprocess.run") as run:
            exec(cell(5), {})
            run.assert_not_called()

    def test_missing_package_reports_terminal_command_without_installing(self):
        actual_version = importlib.metadata.version
        def version(name):
            if name == "SimpleITK":
                raise importlib.metadata.PackageNotFoundError(name)
            return actual_version(name)
        with patch("importlib.metadata.version", version), patch("subprocess.run") as run:
            with self.assertRaisesRegex(RuntimeError, "Restart Kernel"):
                exec(cell(5), {})
            run.assert_not_called()

    def test_missing_widget_dependency_is_checked(self):
        actual_version = importlib.metadata.version
        def version(name):
            if name == "ipyniivue":
                raise importlib.metadata.PackageNotFoundError(name)
            return actual_version(name)
        ns = {"_CALMAR_SETUP_READY": True}
        with patch("importlib.metadata.version", version), patch("subprocess.run") as run:
            with self.assertRaisesRegex(RuntimeError, "pip install ipyniivue"):
                exec(cell(5), ns)
            run.assert_not_called()
        self.assertFalse(ns["_CALMAR_SETUP_READY"])

    def test_stale_packaging_has_actionable_error(self):
        with patch.object(packaging, "__version__", "stale-test"):
            with self.assertRaisesRegex(RuntimeError, "Restart the kernel"):
                exec(cell(8), {})

    def test_full_import_cell(self):
        ns = {}
        exec(cell(8), ns)
        self.assertTrue(ns["_CALMAR_SETUP_READY"])
        self.assertTrue(all(name in ns for name in ("sys", "importlib", "image", "widgets", "cm")))

    def test_decode_stops_after_failed_setup(self):
        with self.assertRaisesRegex(RuntimeError, "Setup imports did not complete"):
            exec(cell(85), {"INTERP_RUN_DECODING": True})

    def test_optional_decode_does_nothing_when_not_requested(self):
        exec(cell(85), {"INTERP_RUN_DECODING": False})


if __name__ == "__main__":
    unittest.main()
