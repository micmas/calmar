"""Exercise notebook callbacks with tiny local fixtures, without inference."""

import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import ipywidgets as widgets
from IPython.display import HTML
import nibabel as nib
import numpy as np

from calmar import disconnectomes as cd
from calmar import disconnectome_compare as dc
from calmar import widgets as calmar_widgets
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


class FakeStudy:
    """The parts of calmar.study.Study the comparison panel uses."""
    def __init__(self, folder):
        self.folder, self.project = folder, folder(dict(subject="x", session="x"), "project")

    def dirs(self, entry):
        return {"linda": self.folder(entry, "linda"), "template": self.folder(entry, "linda"),
                "synthstroke": self.folder(entry, "synthstroke"),
                "bcbtoolkit": self.folder(entry, "bcb"), "deepdisco": self.folder(entry, "dd")}

    def masks(self, entry):
        return cm.discover_masks(entry, self.folder(entry, "linda"), self.folder(entry, "synthstroke"))


class DisconnectomeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.entries = [dict(subject="sub-test", session=s, t1w="T1w.nii.gz") for s in ("ses-1", "ses-2", "ses-empty")]
        self.loads = []
        self.shown = []
        self.created = []
        def viewer(*args, **kwargs):
            v = Viewer()
            self.created.append(v)
            self.addCleanup(v.close)
            return v
        # The cell calls calmar.disconnectome_compare, which uses calmar.widgets
        # for its viewer and IPython's display; replace both with local fakes.
        def set_volumes(nv, specs):
            self.loads.append(specs)
            nv.volumes = [widgets.HTML() for _ in specs]                  # widgets with model ids
        from calmar import step_viewer
        for patcher in (patch.object(calmar_widgets, "fresh_viewer", viewer),
                        patch.object(calmar_widgets, "set_volumes", set_volumes),
                        patch.object(step_viewer, "display", lambda *args: None),
                        patch.object(dc, "display", lambda *args: self.shown.extend(args))):
            patcher.start()
            self.addCleanup(patcher.stop)
        self.ns = dict(SUBJECTS=self.entries, TEST_SUBJECT_IDX=0, RUN_TEST=True,
                       study=FakeStudy(self.folder))
        for e in self.entries[:2]:
            self.write(self.folder(e, "linda") / "Subject_in_MNI.nii.gz")
            self.write(self.folder(e, "linda") / "Lesion_in_MNI.nii.gz")
            self.write(self.folder(e, "linda") / "ExpertMask_in_MNI.nii.gz")
            self.write(self.folder(e, "synthstroke") / "SynthStroke_in_MNI.nii.gz")
            self.write(self.folder(e, "bcb") / "Disconnectome_linda.nii.gz")
            for token in ("linda", "synthstroke", "expert"):              # the T1-route sources
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

    def specs(self):
        return self.loads[-1]

    def visible(self, view):
        """Paths of the layers the browser controls show (same rule as the JS)."""
        c = view["controls"]
        return [Path(l["path"]).name for l, layer in zip(self.specs()[1:], c.layers) if c.visible(layer)]

    def test_comparison_uses_the_step_controls(self):
        self.run_cell(35)
        view = self.ns["_disconnectome_comparison"]
        c = view["controls"]
        self.assertEqual([k for _, k in c.groups], ["linda", "synthstroke", "manual"])
        self.assertEqual([k for _, k in c.variants], list(cd.MODEL_NAMES))
        self.assertEqual([r["label"] for r in c.roles], ["Lesion", "BCBToolkit map", "DeepDisco map"])
        self.assertEqual(self.visible(view), ["Lesion_in_MNI.nii.gz", "Disconnectome_linda.nii.gz"])
        c.roles = [{**r, "shown": True} for r in c.roles]                 # tick DeepDisco
        c.variant = "commissural"
        self.assertEqual(self.visible(view), ["Lesion_in_MNI.nii.gz", "Disconnectome_linda.nii.gz",
                                              "DeepDisco_linda_commissural.nii.gz"])
        c.group = "manual"                                                  # no BCBToolkit map
        self.assertEqual(self.visible(view), ["ExpertMask_in_MNI.nii.gz", "DeepDisco_expert_commissural.nii.gz"])
        self.assertEqual(len(self.created), 1)

    def test_participant_menu_reloads_and_keeps_choices(self):
        self.run_cell(35)
        view = self.ns["_disconnectome_comparison"]
        view["controls"].group = "synthstroke"
        view["participant"].value = 1
        self.assertTrue(all("ses-2" in l["path"] for l in self.specs()))
        self.assertEqual(view["controls"].group, "synthstroke")
        view["participant"].value = 2                                       # nothing processed yet
        self.assertIn("No image", view["status"].value)

    def test_lesion_alone_when_no_maps_exist(self):
        for folder in (self.folder(self.entries[0], "bcb"), self.folder(self.entries[0], "dd")):
            for path in folder.glob("*.nii.gz"):
                path.unlink()
        self.run_cell(35)
        view = self.ns["_disconnectome_comparison"]
        self.assertEqual(self.visible(view), ["Lesion_in_MNI.nii.gz"])
        self.assertEqual(view["controls"].variants, [])
        self.assertNotIn(36, CELLS)

    def test_custom_origin_colours_match_lesion_and_disconnectome_layers(self):
        colors.configure({'manual': 'yellow', 'synthstroke': 'cyan',
                          'bcbtoolkit': 'green', 'deepdisco': 'magenta'})
        self.addCleanup(colors.configure)
        self.run_cell(35)
        by_name = {Path(l['path']).name: l['colormap'] for l in self.specs()}
        self.assertEqual(by_name['Disconnectome_linda.nii.gz'], 'green')
        self.assertEqual(by_name['DeepDisco_linda_whole_brain.nii.gz'], 'magenta')
        self.ns["_disconnectome_comparison"]["controls"].group = "manual"
        by_name = {Path(l['path']).name: l['colormap'] for l in self.specs()}
        self.assertEqual(by_name['ExpertMask_in_MNI.nii.gz'], 'yellow')

    def test_initial_source_and_model_are_honoured(self):
        view = dc.show_disconnectome_comparison(self.ns["study"], self.entries[1],
                                                mask_source="synthstroke", model="projection",
                                                entries=self.entries)
        self.assertEqual(view["participant"].value, 1)
        self.assertEqual((view["controls"].group, view["controls"].variant), ("synthstroke", "projection"))

    def test_metrics_cache_by_mtime_and_table_explains_metrics(self):
        bcb, dd = dc.comparison_paths(self.ns["study"], self.entries[0], "linda", "whole_brain")
        result = dict(r=.8, dice=.4, thr=.5, n_bcb=10, n_dd=5, png="x.png")
        with patch("calmar.reporting.run_reporting_task", return_value=result) as task:
            dc._METRICS_CACHE.clear()
            self.assertIs(dc.agreement_metrics(bcb, dd, self.root), result)
            dc.agreement_metrics(bcb, dd, self.root)
            self.assertEqual(task.call_count, 1)
            self.assertEqual(task.call_args.kwargs["threshold"], dc.DICE_THRESHOLD)
            self.write(dd)  # New file -> new mtime -> recomputed.
            import os
            os.utime(dd, ns=(1, 1))
            dc.agreement_metrics(bcb, dd, self.root)
            self.assertEqual(task.call_count, 2)
        html = dc.metrics_table_html(result, "t")
        self.assertIn("Pearson r", html)
        self.assertIn("2·|A∩B| / (|A|+|B|)", html)
        self.assertIn("0.800", html)

    def test_opening_metrics_section_shows_table_with_definitions(self):
        self.run_cell(35)
        view = self.ns["_disconnectome_comparison"]
        result = dict(r=.8, dice=.4, thr=.5, n_bcb=10, n_dd=5, png="x.png")
        with patch.object(dc, "agreement_metrics", return_value=result) as metrics:
            view["details"].selected_index = 0
            metrics.assert_called_once()
            self.assertIn("Dice", self.shown[-1].data)
            self.assertIn("Pearson r", self.shown[-1].data)
            view["controls"].variant = "projection"                         # chosen in the browser
            self.assertTrue(str(metrics.call_args.args[1]).endswith("DeepDisco_linda_projection.nii.gz"))

    def test_lesion_centre_is_inside_a_non_convex_lesion(self):
        data = np.zeros((9, 9, 3), np.uint8)
        data[0:9, 0, 1] = 1; data[0, 0:9, 1] = 1  # L shape; centroid lies outside it.
        affine = np.diag([2., 2., 2., 1.]); affine[:3, 3] = [-10, -20, -30]
        path = self.root / "lesion.nii.gz"
        nib.save(nib.Nifti1Image(data, affine), path)
        mm = dc.lesion_centre_mm(path)
        voxel = np.round(nib.affines.apply_affine(np.linalg.inv(affine), mm)).astype(int)
        self.assertEqual(data[tuple(voxel)], 1)
        nib.save(nib.Nifti1Image(np.zeros_like(data), affine), path)
        self.assertIsNone(dc.lesion_centre_mm(path))

if __name__ == "__main__":
    unittest.main()
