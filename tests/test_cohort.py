"""Selection uses T1 sessions; manual annotation sessions are independent."""
import contextlib
import io
from pathlib import Path
import re
import tempfile
import unittest
from calmar.cohort import sample_t1_participants
from calmar.guided import normalize_selection, source_cell


class CohortTests(unittest.TestCase):
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
            ns = dict(Path=Path, re=re, RAW_DATASET_DIR=root, CONFIG=config)
            # Execute real discovery and sampling, stopping before acquisition.
            source = "".join(source_cell(19)["source"]).split("# ---- Lazy datalad get:")[0]
            with contextlib.redirect_stdout(io.StringIO()):
                exec(source, ns)
            self.assertEqual({e["subject"] for e in ns["SUBJECTS"]}, {"sub-1", "sub-2", "sub-3"})
            self.assertEqual(len(ns["SUBJECTS"]), 3)
            self.assertTrue(all(e["session"] in ("ses-t1a", "ses-t1b") for e in ns["SUBJECTS"]))
