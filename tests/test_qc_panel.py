"""QC interaction checks with temporary sidecars and no imaging execution."""
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import ipywidgets as w
from calmar.qc import QCRecord
from calmar.qc_panel import QCPanel
from calmar.execution import QCCheckpoint
from calmar.qc_decisions import report_qc_text


class Viewer(w.HTML):
    def load_volumes(self, volumes):
        self.volumes = volumes


class QCPanelTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.entries = [dict(subject=f"sub-{i}", session="ses-1") for i in range(2)]
        self.directory = lambda e: self.root / e["subject"] / e["session"]
        self.anchor = lambda e: self.directory(e) / "Lesion_in_MNI.nii.gz"
        shell = SimpleNamespace(input_transformers_post=[], kernel=SimpleNamespace(_abort_queues=Mock()))
        self.gate = QCCheckpoint(shell, self.entries, self.directory)
        self.addCleanup(self.gate.close)
        self.panel = QCPanel(self.entries, lambda e: ["skull_strip", "lesion", "expert_mni_warp"],
            self.anchor, lambda *args: [], Viewer(), self.gate)
        self.addCleanup(self.panel.close)

    def saved_panel(self, ratings):
        for i, stages in ratings.items():
            record = QCRecord.load(self.anchor(self.entries[i]))
            record.subject, record.session = self.entries[i]['subject'], self.entries[i]['session']
            record.reviewer, record.reviewed_on = 'Original reviewer', '2026-09-01'
            record.edits = [dict(operation='previous edit')]
            for stage, rating in stages.items():
                record.set_stage(stage, rating=rating, notes='Saved note')
            record.save()
        self.panel.deactivate()
        self.panel = QCPanel(self.entries, lambda e: ["skull_strip", "lesion", "expert_mni_warp"],
            self.anchor, lambda *args: [], Viewer(), self.gate)
        self.panel.navigation.request = Mock(return_value=True)
        self.addCleanup(self.panel.close)
        return self.panel

    def test_existing_choice_reuses_complete_qc_without_rewriting_ratings(self):
        stages = dict(skull_strip=1, lesion=2, expert_mni_warp=1)
        p = self.saved_panel({0: stages, 1: stages})
        before = {path: path.read_bytes() for path in self.root.rglob('*.qc.json')}
        self.assertIn('QC already exists', self.gate.message.value)
        self.assertIn('3/3 stages rated', p.existing_summary.value)
        self.assertIn('Original reviewer', p.existing_summary.value)
        self.assertTrue(self.gate.paused)
        p.use_existing.click()
        self.assertFalse(self.gate.paused)
        p.navigation.request.assert_called_once_with('after-qc', p._continue, prompt='')
        self.assertTrue(p.navigation.request.call_args.args[1]())
        self.assertEqual(p.stage.value, 'skull_strip')
        self.assertIn('All available stages', p.message.value)
        for entry in self.entries:
            self.assertIn('Existing QC reused', report_qc_text(self.directory(entry), entry))
        self.assertTrue(all(path.read_bytes() == data for path, data in before.items()))
        self.gate.skip_qc.click()
        self.assertFalse(p.use_existing.disabled)
        p.use_existing.click()
        self.assertIn('Existing QC reused', report_qc_text(self.directory(self.entries[0]), self.entries[0]))

    def test_reuse_mixed_cohort_goes_to_first_unrated_stage_and_keeps_scoped_choices(self):
        p = self.saved_panel({0: dict(skull_strip=1, lesion=2, expert_mni_warp=1),
                              1: dict(skull_strip=2)})
        self.assertTrue(p.reuse_saved())
        self.assertEqual((p.subject.value, p.stage.value), (1, 'lesion'))
        p.rating_buttons['lesion'].value = 1
        self.assertTrue(p.save_current())
        self.assertIn('Existing QC reused', report_qc_text(self.directory(self.entries[0]), self.entries[0]))
        self.assertIn('QC review selected', report_qc_text(self.directory(self.entries[1]), self.entries[1]))

    def test_unreviewed_participant_is_not_reported_as_reused(self):
        p = self.saved_panel({0: dict(skull_strip=1, lesion=1, expert_mni_warp=1)})
        p.use_existing.click()
        self.assertEqual((p.subject.value, p.stage.value), (1, 'skull_strip'))
        self.assertIn('QC review selected', report_qc_text(self.directory(self.entries[1]), self.entries[1]))
        self.assertFalse(QCRecord.load(self.anchor(self.entries[1])).path.exists())

    def test_redo_clears_drafts_only_and_saving_preserves_other_stages_and_edits(self):
        p = self.saved_panel({0: dict(skull_strip=1, lesion=2, expert_mni_warp=1)})
        path = QCRecord.load(self.anchor(self.entries[0])).path
        original = path.read_bytes()
        p.redo.click()
        self.assertEqual((p.subject.value, p.stage.value), (0, 'skull_strip'))
        self.assertTrue(all(b.value is None for b in p.rating_buttons.values()))
        self.assertEqual(p.notes.value, '')
        self.assertEqual(path.read_bytes(), original)
        p.subject.value = 1
        p.subject.value = 0
        self.assertTrue(all(b.value is None for b in p.rating_buttons.values()))
        self.assertFalse(p.save_participant())
        p.rating_buttons['skull_strip'].value = 2
        self.assertTrue(p.save_current())
        saved = QCRecord.load(self.anchor(self.entries[0]))
        self.assertEqual(saved.get_stage('skull_strip')['rating'], 2)
        self.assertEqual(saved.get_stage('lesion')['rating'], 2)
        self.assertEqual(saved.get_stage('lesion')['notes'], 'Saved note')
        self.assertEqual(saved.edits, [dict(operation='previous edit')])
        p.rating_buttons['lesion'].value = 1
        self.assertTrue(p.save_current())
        saved = QCRecord.load(self.anchor(self.entries[0]))
        self.assertEqual(saved.notes, '')
        self.assertEqual(saved.get_stage('lesion')['notes'], '')

    def test_empty_sidecar_does_not_offer_existing_qc(self):
        QCRecord(self.anchor(self.entries[0])).save()
        p = self.saved_panel({})
        self.assertEqual(p.existing_summary.value, '')
        self.assertNotIn('QC already exists', self.gate.message.value)

    def test_failed_reuse_decision_stays_paused_and_does_not_reset_drafts(self):
        p = self.saved_panel({0: dict(skull_strip=1)})
        p.rating_buttons['lesion'].value = 2
        with patch('calmar.execution.record_qc_choice', side_effect=OSError('disk unavailable')):
            self.assertFalse(p.reuse_saved())
        self.assertTrue(self.gate.paused)
        self.assertEqual(p.rating_buttons['lesion'].value, 2)
        p.navigation.request.assert_not_called()

    def test_reuse_and_continue_button_dispatch_to_same_step(self):
        p = self.saved_panel({0: dict(skull_strip=1, lesion=1, expert_mni_warp=1)})
        p.use_existing.click()
        saved_target = p.navigation.request.call_args.args
        p.navigation.request.reset_mock()
        p.continue_button.click()
        self.assertEqual(p.navigation.request.call_args.args, saved_target)
        self.assertEqual(saved_target[0], 'after-qc')
        p.navigation.request.reset_mock()
        p.deactivate()
        self.assertFalse(p.reuse_saved())
        self.assertFalse(p.continue_after_qc())
        p.navigation.request.assert_not_called()

    def test_save_advances_stage_and_unlocks_completed_reviews(self):
        p = self.panel
        p.rating_buttons["skull_strip"].value = 3
        self.assertTrue(p.repair.value)
        self.assertTrue(p.save_current())
        self.assertFalse(self.gate.paused)
        self.assertEqual(p.stage.value, "lesion")
        self.assertTrue(QCRecord.load(self.anchor(self.entries[0])).marked_for_rerun)
        self.assertFalse(self.gate.skip_qc.disabled)

    def test_save_all_keeps_notes_and_starts_next_subject_at_first_stage(self):
        p = self.panel
        p.rating_buttons["skull_strip"].value = 1
        p.notes.value = "brain reviewed"
        p.rating_buttons["lesion"].value = 2
        p.notes.value = "lesion reviewed"
        self.assertFalse(p.save_participant())
        self.assertFalse(self.anchor(self.entries[0]).with_suffix(".qc.json").exists())
        p.rating_buttons["expert_mni_warp"].value = 1
        self.assertTrue(p.save_participant())
        self.assertEqual(p.subject.value, 1)
        self.assertEqual(p.stage.value, "skull_strip")
        record = QCRecord.load(self.anchor(self.entries[0]))
        self.assertEqual(record.get_stage("skull_strip")["notes"], "brain reviewed")
        self.assertEqual(record.get_stage("lesion")["notes"], "lesion reviewed")
        self.assertEqual(record.get_stage("expert_mni_warp")["rating"], 1)
        self.assertIsNone(p.rating_buttons["skull_strip"].value)

    def test_switch_subject_preserves_drafts_without_writing(self):
        p = self.panel
        p.rating_buttons["lesion"].value = 2
        p.notes.value = "draft"
        p.subject.value = 1
        p.subject.value = 0
        self.assertEqual(p.rating_buttons["lesion"].value, 2)
        p.stage.value = "lesion"
        self.assertEqual(p.notes.value, "draft")
        self.assertFalse(list(self.root.rglob("*.qc.json")))

    def test_skip_remains_available_after_review_and_latest_choice_is_reported(self):
        for choice in ("review_requested", "skipped", "review_requested", "skipped"):
            self.assertTrue(self.gate.choose(choice))
        self.assertEqual(report_qc_text(self.directory(self.entries[0]), self.entries[0]),
                         "QC was skipped by the user.")

    def test_failed_save_preserves_previous_ratings(self):
        p = self.panel
        p.rating_buttons["skull_strip"].value = 1
        self.assertTrue(p.save_current())
        path = QCRecord.load(self.anchor(self.entries[0])).path
        before = path.read_bytes()
        p.rating_buttons["skull_strip"].value = 3
        with patch("calmar.qc.os.replace", side_effect=OSError("disk unavailable")):
            self.assertFalse(p.save_current())
        self.assertEqual(path.read_bytes(), before)
        self.assertFalse(list(path.parent.glob(".qc-*.tmp")))

    def test_repair_action_saves_draft_skull_rating_before_dispatch(self):
        self.panel.rating_buttons["skull_strip"].value = 3
        self.assertTrue(self.panel._prepare_repair())
        self.assertEqual(QCRecord.load(self.anchor(self.entries[0])).get_stage("skull_strip")["rating"], 3)

    def test_replaced_panel_cannot_resave_stale_ratings_after_repair(self):
        p = self.panel
        p.rating_buttons["skull_strip"].value = 1
        p.deactivate()
        self.assertTrue(p.save.disabled)
        self.assertFalse(p.save_current())
        self.assertFalse(p._prepare_repair())
        self.assertFalse(list(self.root.rglob("*.qc.json")))
