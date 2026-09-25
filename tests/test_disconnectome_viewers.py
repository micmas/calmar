"""Exercise notebook callbacks with tiny local fixtures, without inference."""

import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest

import ipywidgets as widgets
from IPython.display import HTML
import nibabel as nib
import numpy as np

from calmar import disconnectomes as cd
from calmar import masks as cm


ROOT = Path(__file__).resolve().parents[1]
CELLS = json.loads((ROOT / "lesion-interpretation-pipeline.ipynb").read_text())["cells"]


class Viewer(widgets.HTML):
    def load_volumes(self, volumes):
        self.loaded = volumes


class DisconnectomeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.entries = [dict(subject="sub-test", session=s) for s in ("ses-1", "ses-2", "ses-empty")]
        self.shown = []
        self.created = []
        def viewer(*args, **kwargs):
            v = Viewer()
            self.created.append(v)
            self.addCleanup(v.close)
            return v
        self.ns = dict(SUBJECTS=self.entries, TEST_SUBJECT_IDX=0, DIAG_SUBJECT_IDX=None,
                       RUN_TEST=True, Path=Path, widgets=widgets, HTML=HTML,
                       display=lambda *args: self.shown.extend(args), clear_output=lambda **kw: None,
                       np=np, nib=nib,
                       image=SimpleNamespace(resample_to_img=lambda a, b, **kw: a),
                       cw=SimpleNamespace(fresh_viewer=viewer, vols=lambda x: x),
                       deriv_path_for=lambda e: self.folder(e, "linda"),
                       synthstroke_path_for=lambda e: self.folder(e, "synthstroke"),
                       bcb_path_for=lambda e: self.folder(e, "bcb"),
                       deepdisco_path_for=lambda e: self.folder(e, "dd"),
                       mask_inventory_for=lambda e: cm.discover_masks(
                           e, self.folder(e, "linda"), self.folder(e, "synthstroke")))
        for e in self.entries[:2]:
            self.write(self.folder(e, "linda") / "Subject_in_MNI.nii.gz")
            self.write(self.folder(e, "linda") / "Lesion_in_MNI.nii.gz")
            self.write(self.folder(e, "linda") / "ExpertMask_in_MNI.nii.gz")
            self.write(self.folder(e, "synthstroke") / "SynthStroke_in_MNI.nii.gz")
            self.write(self.folder(e, "bcb") / "Disconnectome_linda.nii.gz")
            for token in cd.SOURCE_TOKENS.values():
                for model in cd.MODEL_NAMES:
                    self.write(self.folder(e, "dd") / f"DeepDisco_{token}_{model}.nii.gz")

    def folder(self, entry, tool):
        return self.root / tool / entry["subject"] / entry["session"] / "anat"

    def write(self, path):
        path.parent.mkdir(parents=True, exist_ok=True)
        nib.save(nib.Nifti1Image(np.arange(8, dtype=np.float32).reshape(2, 2, 2) / 8,
                                np.eye(4)), path)
        return path

    def run_cell(self, number):
        exec("".join(CELLS[number - 1]["source"]), self.ns)

    def test_discovery_distinguishes_missing_bcb_from_existing_deepdisco(self):
        e = self.entries[0]
        found = cd.discover(self.folder(e, "bcb"), self.folder(e, "dd"))
        self.assertEqual(len(cd.available_sources(found)), 3)
        self.assertIsNone(found["manual"]["bcb"])
        self.assertEqual(len(found["manual"]["deepdisco"]), 4)
        self.assertEqual(len(cd.map_options(found, "linda")), 5)
        self.assertEqual(len(cd.map_options(found, "synthstroke")), 4)
        p = found["manual"]["deepdisco"]["projection"]
        p.write_bytes(b"")
        found["manual"]["deepdisco"]["commissural"].unlink()
        found["manual"]["deepdisco"]["commissural"].symlink_to(self.root / "unfetched")
        self.write(self.folder(e, "dd") / "_deepdisco_on_bcbgrid_expert.nii.gz")
        self.assertEqual(len(cd.discover(self.folder(e, "bcb"), self.folder(e, "dd"))
                             ["manual"]["deepdisco"]), 2)

    def test_viewers_keep_independent_state_across_cells_and_subjects(self):
        self.run_cell(35)
        comparison = self.ns["_disconnectome_comparison"]
        self.assertEqual(len(comparison["source"].options), 3)
        self.run_cell(37)
        view = self.ns["_disconnectome_view"]
        # These globals were reused by downstream cells in the broken notebook.
        for name in ("_src_dd", "_ddir", "_bdir", "_tag", "_bg", "_nv", "_c_e",
                     "_map_dd", "_map_options", "_DD_LABELS", "_SRC_TOKEN"):
            self.ns[name] = None
        for src, token in cd.SOURCE_TOKENS.items():
            view["source"].value = src
            self.assertEqual(len(view["map"].options), 5 if src == "linda" else 4)
            self.assertNotIn("No disconnectome", view["header"].value)
            comparison["source"].value = src
            self.assertEqual(len(comparison["model"].options), 4)
            comparison["model"].value = "commissural"
            self.assertTrue(any(f"{token}_commissural" in v["path"]
                                for v in comparison["viewer"].loaded))
        comparison["subject"].value = 1
        view["subject"].value = 1
        self.assertIn("ses-2", view["header"].value)
        for state in (view, comparison):
            self.assertTrue(all("ses-2" in v["path"] for v in state["viewer"].loaded))
        view["subject"].value = 2
        comparison["subject"].value = 2
        self.assertEqual(view["viewer"].loaded, [])
        self.assertEqual(comparison["viewer"].loaded, [])

    def test_refresh_discovers_new_maps_and_bcb_only_source(self):
        self.run_cell(37)
        view = self.ns["_disconnectome_view"]
        view["source"].value = "manual"
        p = self.write(self.folder(self.entries[0], "bcb") / "Disconnectome_expert.nii.gz")
        view["refresh"].click()
        self.assertIn(("BCBToolkit", p), view["map"].options)
        self.assertIn("BCBToolkit: available", view["files"].value)
        for p in self.folder(self.entries[0], "dd").glob("DeepDisco_expert_*.nii.gz"):
            p.unlink()
        view["refresh"].click()
        self.assertEqual(len(view["map"].options), 1)
        self.run_cell(35)
        comparison = self.ns["_disconnectome_comparison"]
        comparison["source"].value = "manual"
        self.assertTrue(comparison["model"].disabled)
        self.assertTrue(any("Disconnectome_expert" in v["path"]
                            for v in comparison["viewer"].loaded))


if __name__ == "__main__":
    unittest.main()
