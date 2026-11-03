"""Selection uses T1 sessions; manual annotation sessions are independent."""
import contextlib
import io
from pathlib import Path
import re
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch
from calmar.cohort import sample_t1_participants
from calmar.guided import (SOURCE_OPTIONS, initial_input_route, normalize_selection, set_route_source_options,
                           source_cell, validate_isles_input)


class CohortTests(unittest.TestCase):
    def test_route_change_preserves_local_source_and_replaces_t1_only_sources(self):
        import ipywidgets as widgets
        source = widgets.Dropdown(options=[("OpenNeuro", "openneuro"), ("Local BIDS", "local"),
                                           ("Single T1", "single")], value="local")
        set_route_source_options(source, "dwi")
        self.assertEqual(source.value, "local")
        set_route_source_options(source, "t1")
        source.value = "single"
        set_route_source_options(source, "dwi")
        self.assertEqual(source.value, "local")

    def test_dwi_guided_selection_uses_openads_not_t1_methods(self):
        values = normalize_selection(dict(DATASET_SOURCE="local", MODALITY="dwi", SUBJECT_FILTER="sub-1",
            SESSION_FILTER="", MAX_SUBJECTS=1, RANDOM_SAMPLE=False,
            _method_linda=True, _method_synthstroke=True))
        self.assertEqual(values["SEGMENTATION_METHODS"], ["openads"])
        self.assertNotIn("_method_linda", values)

    def test_guided_selection_always_asks_about_optional_analyses(self):
        values = normalize_selection(dict(
            DATASET_SOURCE="local", MODALITY="t1", SUBJECT_FILTER="sub-1",
            SESSION_FILTER="", MAX_SUBJECTS=1, RANDOM_SAMPLE=False,
            ANALYSE_DWI=False, ANALYSE_TRACT_DWI=True, ANALYSE_BRAIN_HEALTH=False))
        self.assertIsNone(values["ANALYSE_DWI"])
        self.assertIsNone(values["ANALYSE_TRACT_DWI"])
        self.assertIsNone(values["ANALYSE_BRAIN_HEALTH"])

    def test_isles_guided_source_is_explicit_and_forces_the_compatible_route(self):
        self.assertIn(("ISLES 2022 (local)", "isles2022"), SOURCE_OPTIONS["dwi"])
        self.assertEqual(initial_input_route({"DATASET_SOURCE": "isles2022", "MODALITY": "t1"}), "dwi")
        values = normalize_selection(dict(
            DATASET_SOURCE="isles2022", MODALITY="t1", SUBJECT_FILTER="",
            SESSION_FILTER="", MAX_SUBJECTS=0, RANDOM_SAMPLE=False,
            _method_linda=True, _method_synthstroke=True))
        self.assertEqual(values["MODALITY"], "dwi")
        self.assertEqual(values["SEGMENTATION_METHODS"], ["openads"])

    def test_isles_validation_distinguishes_bad_filters_from_a_bad_root(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            folder = root/'sub-strokecase0001'/'ses-0001'/'dwi'
            folder.mkdir(parents=True)
            (root/'derivatives').mkdir()
            for suffix in ('dwi', 'adc'):
                (folder/f'sub-strokecase0001_ses-0001_{suffix}.nii.gz').write_bytes(b'x')
            self.assertEqual(len(validate_isles_input(root)), 1)
            with self.assertRaisesRegex(ValueError, '1 ISLES DWI\\+ADC pairs.*filters'):
                validate_isles_input(root, ['sub-not-in-isles'])

    def test_isles_validation_reports_a_nested_extraction_root(self):
        with tempfile.TemporaryDirectory() as temporary:
            outer = Path(temporary)
            root = outer/'ISLES-2022'
            folder = root/'sub-strokecase0001'/'ses-0001'/'dwi'
            folder.mkdir(parents=True)
            (root/'derivatives').mkdir()
            for suffix in ('dwi', 'adc'):
                (folder/f'sub-strokecase0001_ses-0001_{suffix}.nii.gz').write_bytes(b'x')
            with self.assertRaisesRegex(ValueError, f'Choose {re.escape(str(root))}'):
                validate_isles_input(outer)

    def test_empty_openneuro_filters_enable_random_sampling(self):
        values = normalize_selection(dict(DATASET_SOURCE="openneuro", SUBJECT_FILTER=" , ",
            SESSION_FILTER="", MAX_SUBJECTS=3, RANDOM_SAMPLE=False))
        self.assertIsNone(values["SUBJECT_FILTER"])
        self.assertIsNone(values["SESSION_FILTER"])
        self.assertTrue(values["RANDOM_SAMPLE"])
        self.assertEqual(values["MAX_SUBJECTS"], 3)

    def test_explicit_filter_preserves_sampling_choice(self):
        for subjects, sessions in (("sub-1", ""), ("", "ses-2")):
            values = normalize_selection(dict(DATASET_SOURCE="openneuro", SUBJECT_FILTER=subjects,
                SESSION_FILTER=sessions, MAX_SUBJECTS=3, RANDOM_SAMPLE=False))
            self.assertFalse(values["RANDOM_SAMPLE"])

    def test_multisession_subjects_do_not_fill_multiple_participant_slots(self):
        entries = [dict(subject=f"sub-{i}", session=f"ses-{j}", t1w=f"{i}/{j}/T1.nii.gz")
                   for i in range(6) for j in range(1 if i else 12)]
        picked = sample_t1_participants(entries, 3, seed=67)
        self.assertEqual(len(picked), 3)
        self.assertEqual(len({e["subject"] for e in picked}), 3)
        self.assertTrue(all(e in entries for e in picked))
        self.assertEqual(picked, sample_t1_participants(list(reversed(entries)), 3, seed=67))
        self.assertEqual(len(sample_t1_participants(entries, None, seed=67)), 6)
        self.assertEqual(sample_t1_participants([], 3), [])

    def test_notebook_discovery_selects_t1_sessions_independently_of_annotations(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for subject in ("sub-1", "sub-2", "sub-3", "sub-maskonly"):
                mask = root / "derivatives" / "lesion_masks" / subject / "ses-annotation" / "anat" / f"{subject}_ses-annotation_T2w_desc-lesion_mask.nii.gz"
                mask.parent.mkdir(parents=True)
                mask.symlink_to(root / "unfetched-mask")
                if subject == "sub-maskonly":
                    continue
                for session in ("ses-t1a", "ses-t1b"):
                    t1 = root / subject / session / "anat" / f"{subject}_{session}_T1w.nii.gz"
                    t1.parent.mkdir(parents=True)
                    t1.symlink_to(root / "unfetched-t1")
            config = normalize_selection(dict(DATASET_SOURCE="openneuro", SUBJECT_FILTER="",
                SESSION_FILTER="", MAX_SUBJECTS=3, RANDOM_SAMPLE=False, T1W_SELECTION="first"))
            ns = dict(Path=Path, re=re, RAW_DATASET_DIR=root, PROJECT_DIR=root, CONFIG=config,
                      BATCH_TIMINGS={})
            # Execute the combined selection/acquisition cell with external work mocked.
            source = "".join(source_cell(19)["source"])
            result = {"stage": "acquisition", "results": []}
            with patch("calmar.scheduled.submit_step", return_value=result) as submit, \
                 patch("calmar.step_summary.show_step") as show, \
                 patch("calmar.step_summary.show_mask_inventory") as inventory, \
                 contextlib.redirect_stdout(io.StringIO()):
                exec(source, ns)
            self.assertEqual({e["subject"] for e in ns["SUBJECTS"]}, {"sub-1", "sub-2", "sub-3"})
            self.assertEqual(len(ns["SUBJECTS"]), 3)
            self.assertTrue(all(e["session"] in ("ses-t1a", "ses-t1b") for e in ns["SUBJECTS"]))
            submit.assert_called_once_with("acquisition", ns["SUBJECTS"], ns["study"],
                                           timings=ns["BATCH_TIMINGS"])
            show.assert_called_once_with(result, title="Selected inputs and DWI availability")
            inventory.assert_called_once_with(ns["study"], ns["SUBJECTS"])

    def test_combined_cell_names_every_selected_entry_when_acquisition_fails(self):
        entries = [
            {"subject": "sub-one", "session": "ses-a", "t1w": "one.nii.gz"},
            {"subject": "sub-two", "session": "ses-b", "t1w": "two.nii.gz"},
        ]
        study = SimpleNamespace(
            notebook_helpers=lambda: {},
            label=lambda entry: f"{entry['subject']} {entry['session']}",
        )
        source = "".join(source_cell(19)["source"])
        output = io.StringIO()
        with patch("calmar.study.select_cohorts", return_value=(entries, "fixture")), \
             patch("calmar.study.Study", return_value=study), \
             patch("calmar.study.config_for_entry", return_value={"MODALITY": "t1"}), \
             patch("calmar.scheduled.submit_step", side_effect=RuntimeError("fetch failed")), \
             patch("calmar.step_summary.show_step") as show, \
             patch("calmar.step_summary.show_mask_inventory") as inventory, \
             contextlib.redirect_stdout(output), \
             self.assertRaisesRegex(RuntimeError, "fetch failed"):
            exec(source, {"CONFIG": {}, "RAW_DATASET_DIR": Path("data"),
                          "PROJECT_DIR": Path("project"), "BATCH_TIMINGS": {}})
        self.assertIn("Acquisition failed for selected entries:", output.getvalue())
        self.assertIn("sub-one ses-a", output.getvalue())
        self.assertIn("sub-two ses-b", output.getvalue())
        show.assert_not_called()
        inventory.assert_not_called()
