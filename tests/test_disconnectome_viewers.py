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
from calmar import colors
from calmar.widgets import set_volumes
from calmar.output import Output


ROOT = Path(__file__).resolve().parents[1]
CELLS = {int(c["id"].rsplit("-", 1)[1]) - 1: c for c in json.loads((ROOT / "lesion-interpretation-pipeline.ipynb").read_text())["cells"] if c["id"].startswith("calmar-step-")}


class Viewer(widgets.HTML):
    def __init__(self):
        super().__init__()
        self.opts = SimpleNamespace()
        self.loads = 0

    def load_volumes(self, volumes):
        self.volumes = [SimpleNamespace(**v) for v in volumes]

    @property
    def loaded(self):
        return [dict(path=v.path, colormap=v.colormap) for v in self.volumes]

    @property
    def volumes(self):
        return getattr(self, '_volumes', [])

    @volumes.setter
    def volumes(self, volumes):
        self._volumes = volumes
        self.loads += 1


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
                       cw=SimpleNamespace(fresh_viewer=viewer, vols=lambda x: x,
                                          set_volumes=set_volumes, Output=Output),
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

    def test_unified_viewer_updates_source_model_and_subject(self):
        self.run_cell(35)
        view = self.ns["_disconnectome_comparison"]
        for source, token in cd.SOURCE_TOKENS.items():
            view["source"].value = source
            view["model"].value = "commissural"
            self.assertTrue(any(f"{token}_commissural" in v["path"] for v in view["viewer"].loaded))
            self.assertFalse(view["lesion"].disabled)
            self.assertEqual(view["viewer"].loaded[1]["colormap"], colors.color(source))
            view["lesion"].value = False
            self.assertEqual(view["viewer"].volumes[1].opacity, 0)
            view["lesion"].value = True
            self.assertEqual(view["viewer"].volumes[1].opacity, .35)
        view["subject"].value = 1
        self.assertTrue(all("ses-2" in v["path"] for v in view["viewer"].loaded))
        view["subject"].value = 2
        self.assertEqual(view["viewer"].loaded, [])
        self.assertTrue(view["lesion"].disabled)

    def test_lesion_can_be_viewed_without_disconnectome_and_duplicate_is_removed(self):
        for folder in (self.folder(self.entries[0], "bcb"), self.folder(self.entries[0], "dd")):
            for path in folder.glob("*.nii.gz"):
                path.unlink()
        self.run_cell(35)
        view = self.ns["_disconnectome_comparison"]
        self.assertEqual(view["method"].value, "anatomy")
        self.assertEqual(len(view["viewer"].loaded), 2)
        self.assertFalse(view["lesion"].disabled)
        self.assertNotIn(36, CELLS)
        self.assertEqual(len(self.created), 1)

    def test_readability_controls_reuse_layers_and_handle_missing_methods(self):
        self.run_cell(35)
        comparison = self.ns["_disconnectome_comparison"]
        viewer = comparison["viewer"]
        anatomy, lesion, bcb, deepdisco = viewer.volumes
        loads = viewer.loads
        self.assertFalse(anatomy.colorbar_visible)
        self.assertEqual((bcb.opacity, deepdisco.opacity), (0.65, 0))
        self.assertEqual(viewer.opts.slice_type, 0)
        self.assertEqual(viewer.opts.crosshair_width, 0)
        comparison["method"].value = "deepdisco"
        self.assertEqual((bcb.opacity, deepdisco.opacity), (0, 0.65))
        self.assertFalse(bcb.colorbar_visible)
        self.assertTrue(deepdisco.colorbar_visible)
        comparison["method"].value = "both"
        comparison["opacity"].value = 0.4
        self.assertEqual((bcb.opacity, deepdisco.opacity), (0.4, 0.4))
        comparison["plane"].value = 3
        comparison["crosshair"].value = True
        self.assertEqual(viewer.opts.slice_type, 3)
        self.assertEqual(viewer.opts.crosshair_width, 1)
        comparison["method"].value = "anatomy"
        self.assertEqual((bcb.opacity, deepdisco.opacity), (0, 0))
        self.assertTrue(comparison["opacity"].disabled)
        self.assertEqual(viewer.loads, loads)
        self.assertEqual(anatomy.opacity, 1)
        comparison["method"].value = "bcbtoolkit"
        comparison["source"].value = "manual"  # Only DeepDisco exists.
        self.assertEqual(comparison["method"].value, "deepdisco")
        self.assertNotIn("bcbtoolkit", [v for _, v in comparison["method"].options])
        self.assertEqual(viewer.volumes[-1].opacity, 0.4)

    def test_custom_origin_colours_match_lesion_and_disconnectome_layers(self):
        colors.configure({'manual': 'yellow', 'synthstroke': 'cyan',
                          'bcbtoolkit': 'green', 'deepdisco': 'magenta'})
        self.addCleanup(colors.configure)
        self.run_cell(35)
        view = self.ns['_disconnectome_comparison']
        self.assertEqual(view['viewer'].loaded[2]['colormap'], 'green')
        self.assertEqual(view['viewer'].loaded[3]['colormap'], 'magenta')
        view['source'].value = 'manual'
        self.assertEqual(view['viewer'].loaded[1]['colormap'], 'yellow')

    def test_model_change_preserves_method_location_and_unchanged_layers(self):
        self.run_cell(35)
        view = self.ns['_disconnectome_comparison']
        viewer = view['viewer']
        anatomy, lesion, bcb, old_dd = viewer.volumes
        viewer.scene = SimpleNamespace(crosshair_pos=[.3, .4, .5])
        view['method'].value = 'deepdisco'
        view['model'].value = 'commissural'
        self.assertEqual(view['method'].value, 'deepdisco')
        self.assertEqual(viewer.scene.crosshair_pos, [.3, .4, .5])
        self.assertIs(viewer.volumes[0], anatomy)
        self.assertIs(viewer.volumes[1], lesion)
        self.assertIs(viewer.volumes[2], bcb)
        self.assertIsNot(viewer.volumes[3], old_dd)
        self.assertEqual(viewer.volumes[3].opacity, .65)
        self.assertEqual(bcb.opacity, 0)
        # No resampling/metric work occurs while its accordion is closed.
        self.assertFalse(list(self.root.rglob('_deepdisco_on_bcbgrid*')))
        view['method'].value = 'anatomy'
        self.assertEqual(lesion.opacity, .85)


if __name__ == "__main__":
    unittest.main()
