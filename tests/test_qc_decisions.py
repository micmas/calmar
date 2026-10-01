"""QC choices persist without altering ratings and reach the saved report."""

import ast
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from calmar.execution import QCCheckpoint
from calmar.qc_decisions import record_qc_choice, report_qc_notice


ROOT = Path(__file__).resolve().parents[1]


class QCDecisionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.entry = {"subject": "sub-test", "session": "ses-1"}
        self.directory = self.root / "linda" / "sub-test" / "ses-1" / "anat"
        self.directory.mkdir(parents=True)
        self.ratings = self.directory / "Lesion_in_MNI.qc.json"
        self.ratings.write_text('{"stages":{"lesion":{"rating":2}},"edits":[{"operation":"manual"}]}')
        self.original_ratings = self.ratings.read_bytes()

    def test_skip_persists_and_is_scoped_to_subject_session(self):
        path = record_qc_choice(self.directory, self.entry, "skipped", "checkpoint-1")
        record_qc_choice(self.directory, self.entry, "skipped", "checkpoint-1")
        data = json.loads(path.read_text())
        self.assertEqual(len(data["events"]), 1)
        self.assertEqual(data["events"][0]["chosen_by"], "user")
        self.assertTrue(data["events"][0]["timestamp"])
        self.assertIn("QC was skipped by the user", report_qc_notice(self.directory, self.entry))
        other = {"subject": "sub-test", "session": "ses-2"}
        self.assertNotIn("QC was skipped", report_qc_notice(self.root / "other", other))
        with self.assertRaises(ValueError):
            report_qc_notice(self.directory, other)
        self.assertEqual(self.ratings.read_bytes(), self.original_ratings)

    def test_review_request_keeps_history_without_claiming_completion(self):
        record_qc_choice(self.directory, self.entry, "skipped", "checkpoint-1")
        path = record_qc_choice(self.directory, self.entry, "review_requested", "checkpoint-2")
        self.assertEqual([event["choice"] for event in json.loads(path.read_text())["events"]],
                         ["skipped", "review_requested"])
        notice = report_qc_notice(self.directory, self.entry)
        self.assertNotIn("QC was skipped", notice)
        self.assertIn("does not confirm completion", notice)
        self.assertEqual(self.ratings.read_bytes(), self.original_ratings)

    def test_reused_qc_replaces_skip_notice_without_claiming_new_review(self):
        from calmar.qc_decisions import report_qc_text
        record_qc_choice(self.directory, self.entry, "skipped", "skip")
        record_qc_choice(self.directory, self.entry, "existing_reused", "reuse")
        notice = report_qc_notice(self.directory, self.entry)
        self.assertIn("Existing QC was reused by the user", notice)
        self.assertNotIn("QC was skipped", notice)
        self.assertIn("stage coverage", report_qc_text(self.directory, self.entry))
        self.assertEqual(self.ratings.read_bytes(), self.original_ratings)

    def test_failed_write_preserves_prior_decision_and_removes_temporary_file(self):
        path = record_qc_choice(self.directory, self.entry, "skipped", "checkpoint-1")
        before = path.read_bytes()
        with patch("calmar.qc_decisions.os.replace", side_effect=OSError("disk error")):
            with self.assertRaises(OSError):
                record_qc_choice(self.directory, self.entry, "review_requested", "checkpoint-2")
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(list(self.directory.glob(".QC_decision.*.tmp")), [])

    def test_checkpoint_does_not_unlock_if_choice_cannot_be_recorded(self):
        shell = SimpleNamespace(input_transformers_post=[], kernel=SimpleNamespace(_abort_queues=Mock()))
        gate = QCCheckpoint(shell, [self.entry], lambda e: self.directory)
        self.addCleanup(gate.close)
        with patch("calmar.execution.record_qc_choice", side_effect=OSError("disk full")):
            gate.skip_qc.click()
        self.assertTrue(gate.paused)
        self.assertIn(gate.guard, shell.input_transformers_post)
        self.assertFalse(gate.skip_qc.disabled)
        self.assertIn("disk full", gate.message.value)
        gate.skip_qc.click()
        self.assertFalse(gate.paused)
        self.assertNotIn(gate.guard, shell.input_transformers_post)
        self.assertFalse(gate.do_qc.disabled)
        self.assertTrue(gate.skip_qc.disabled)

    def test_skip_notice_is_in_exported_pdf(self):
        import datetime
        import fitz
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_pdf import PdfPages
        import pandas as pd
        from calmar.qc_decisions import report_qc_text
        record_qc_choice(self.directory, self.entry, "skipped", "pdf-choice")
        notebook = json.loads((ROOT / "lesion-interpretation-pipeline.ipynb").read_text())
        tree = ast.parse("".join(next(c for c in notebook["cells"] if c["id"] == "calmar-step-75")["source"]))
        function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "write_pdf")
        ns = dict(_pdf_dir=self.root, plt=plt, PdfPages=PdfPages, datetime=datetime.datetime,
                  deriv_path_for=lambda e:self.directory, report_qc_text=report_qc_text)
        exec(compile(ast.Module(body=[function],type_ignores=[]),'pdf-function','exec'),ns)
        frame = pd.DataFrame([dict(subject='sub-test',session='ses-1',region='fixture',
            lesion_in_roi_percent=100.,roi_coverage_percent=2.,overlap_voxels=3,total_lesion_voxels=3)])
        path = ns['write_pdf']('sub-test','ses-1',frame,'fixture')
        with fitz.open(path) as document:
            self.assertIn('QC was skipped by the user.', document[0].get_text())

    def test_skip_note_is_in_actual_report_export_and_inline_title(self):
        record_qc_choice(self.directory, self.entry, "skipped", "checkpoint-1")
        notebook = json.loads((ROOT / "lesion-interpretation-pipeline.ipynb").read_text())
        tree = ast.parse("".join(next(c for c in notebook["cells"] if c["id"] == "calmar-step-81")["source"]))
        report_branch = next(node.orelse for node in tree.body
                             if isinstance(node, ast.If) and node.orelse
                             and any(isinstance(n, ast.ImportFrom) and n.module == "calmar.qc_decisions"
                                     for n in node.orelse))
        start = next(i for i, node in enumerate(report_branch)
                     if isinstance(node, ast.ImportFrom) and node.module == "calmar.qc_decisions")
        end = next(i for i, node in enumerate(report_branch[start:], start)
                   if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
                   and isinstance(node.value.func, ast.Attribute) and node.value.func.attr == "write_text")
        displayed = []
        namespace = dict(INTERP_MASK_SOURCE="manual", e=self.entry, deriv_path_for=lambda e: self.directory,
                         _title_card="<h1>Test report</h1>", html_body="<p>Results</p>",
                         _lesion_overlay_img_tag=lambda: "", REPORTS_DIR=self.root / "reports",
                         display=displayed.append, HTML=lambda text: text)
        exec(compile(ast.Module(body=report_branch[start:end+1], type_ignores=[]), "report-export", "exec"), namespace)
        html = namespace["_rpt_path"].read_text()
        self.assertIn("QC was skipped by the user", html)
        self.assertIn("QC was skipped by the user", namespace["html"])
        self.assertIn('<div role="note"', html)
        # The note is in the report body, not the no-print toolbar.
        self.assertIn(namespace["_qc_notice"], namespace["html"])


if __name__ == "__main__":
    unittest.main()
