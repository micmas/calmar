import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import Mock

import ipywidgets as w
import pandas as pd

from calmar.atlas_ui import OverlapSelection, overlap_table
from calmar.report_ui import ParticipantReport, ReportInputs, report_sections
from calmar.participant_report import report_section
from calmar import colors


class ReportInterfaceTests(unittest.TestCase):
    def test_marked_section_titles_are_plain_accessible_text(self):
        body = "<main>" + report_section("This participant’s measures: what the evidence says", "<p>Body</p>") + "</main>"
        sections = report_sections(body)
        self.assertEqual(sections[0][0], "This participant’s measures: what the evidence says")

    def test_report_viewer_uses_the_selected_mask_origin_colour(self):
        colors.configure({'manual': 'cyan'})
        self.addCleanup(colors.configure)
        with TemporaryDirectory() as temp:
            root = Path(temp)
            brain, lesion = root/'brain.nii.gz', root/'mask.nii.gz'
            brain.touch(); lesion.touch()
            viewer = w.HTML()
            viewer.opts, viewer.volumes = SimpleNamespace(), []
            self.addCleanup(viewer.close)
            helpers = SimpleNamespace(fresh_viewer=Mock(return_value=viewer), set_volumes=Mock())
            report = ParticipantReport('Report', '', [('Results', '<p>Fixture</p>')], root/'report.html', '<body></body>',
                                       brain, lesion, helpers, source='manual')
            self.addCleanup(report.widget.close)
            self.addCleanup(report.navigation.close)
            report.show_brain({'new': 1})
            self.assertEqual(helpers.set_volumes.call_args.args[1][1]['colormap'], 'cyan')
            controls = report.brain_box.children[0]                       # same controls as the step viewers
            self.assertEqual([r['label'] for r in controls.roles], ['Manual lesion'])

    def test_table_title_tracks_atlas_mask_and_counts_full_overlap(self):
        rows = [dict(subject='sub-ui', session='', region=f'ROI {i}', overlap_voxels=1,
                     lesion_in_roi_percent=1., roi_coverage_percent=2., total_lesion_voxels=100)
                for i in range(25)]
        df = pd.DataFrame(rows)
        html = overlap_table(df, 'sub-ui', '', 'Atlas B', 'manual', limit=20)
        self.assertIn('Atlas B — Manual mask — sub-ui', html)
        self.assertIn('Regions overlapped:</b> 25', html)
        self.assertIn('Showing 20 of 25', html)
        self.assertNotIn('ROI 24</td>', html)

    def test_default_prefers_synthstroke_but_manual_and_linda_are_selectable(self):
        table = pd.DataFrame([dict(subject='sub-ui', session='')])
        selection = OverlapSelection({f'A_{s}': table for s in ('linda','synthstroke','manual')})
        self.assertEqual(selection.source.value, 'synthstroke')
        selection.source.value = 'linda'
        self.assertEqual(selection.source.value, 'linda')
        selection.source.value = 'manual'
        self.assertEqual(selection.source.value, 'manual')

    def test_generation_uses_form_choice_and_releases_checkpoint_only_on_approval(self):
        shell = SimpleNamespace(input_transformers_post=[], kernel=SimpleNamespace(_abort_queues=Mock()))
        ns = dict(SUBJECTS=[dict(subject='sub-ui',session=None)],
                  INTERP_KB_ATLASES=['Atlas A','Atlas B'], available_mni_sources=lambda e:['manual','synthstroke'])
        panel = ReportInputs(ns, shell)
        self.addCleanup(panel.close)
        self.assertEqual(panel.source.value, 'synthstroke')
        self.assertEqual(panel.evidence.value, 'all')                      # default: drafts included
        panel.source.value, panel.atlas.value, panel.decode.value = 'manual', 'Atlas B', True
        panel.evidence.value = 'approved'
        panel.domains['naming'].value = 'moderate'
        self.assertIn('evidence: Approved entries only', panel.summary.value)
        self.assertTrue(panel.gate.paused)
        panel.navigation.request = Mock()
        panel.generate.click()
        args = panel.navigation.request.call_args.args
        self.assertEqual(args[0], 'report-start')
        self.assertTrue(panel.gate.paused)
        self.assertTrue(args[1]())
        self.assertFalse(panel.gate.paused)
        self.assertEqual((ns['INTERP_MASK_SOURCE'], ns['INTERP_DISPLAY_ATLAS'], ns['INTERP_RUN_DECODING'],
                          ns['INTERP_EVIDENCE']), ('manual','Atlas B',True,'approved'))
        self.assertEqual(ns['INTERP_DOMAIN_LEVELS']['naming'], 'moderate')
        self.assertEqual(ns['INTERP_DOMAIN_LEVELS']['reading'], 'not_assessed')

    def test_domain_levels_are_kept_separate_when_switching_participants(self):
        shell = SimpleNamespace(input_transformers_post=[], kernel=SimpleNamespace(_abort_queues=Mock()))
        ns = dict(SUBJECTS=[dict(subject='sub-a', session='ses-1'), dict(subject='sub-b', session='ses-2')],
                  INTERP_KB_ATLASES=['Atlas A'], available_mni_sources=lambda entry: ['manual'])
        panel = ReportInputs(ns, shell)
        self.addCleanup(panel.close)
        panel.domains['naming'].value = 'mild'
        panel.subject.value = 1
        self.assertEqual(panel.domains['naming'].value, 'not_assessed')
        panel.domains['naming'].value = 'severe'
        panel.subject.value = 0
        self.assertEqual(panel.domains['naming'].value, 'mild')
        self.assertEqual(ns['INTERP_DOMAIN_LEVELS_BY_PARTICIPANT']['sub-b|ses-2']['naming'], 'severe')

    def test_report_keeps_evidence_and_qc_notice_and_adds_decoding_once(self):
        body = '<main><h4>Regions (Atlas A)</h4><table><tr><td>ROI</td></tr></table><h4>Outcomes</h4><p>Citation X</p><hr><div class="legend"><h5>How to read the evidence</h5><p>Legend</p></div></main>'
        sections = report_sections(body)
        self.assertEqual([x[0] for x in sections], ['Regions (Atlas A)','Outcomes','Legend and evidence notes'])
        self.assertIn('Citation X', sections[1][1])
        self.assertEqual(sum('How to read the evidence' in content for _, content in sections), 1)
        self.assertTrue(sections[-1][1].rstrip().endswith('</div>'))
        with TemporaryDirectory() as temp:
            path = Path(temp)/'report.html'
            full = '<html><head><style>.report-header{color:red}</style></head><body>QC was skipped by the user.' + body + '</body></html>'
            path.write_text(full)
            report = ParticipantReport('Participant report', 'QC was skipped by the user.', sections,
                path, full, Path(temp)/'missing-brain.nii.gz', Path(temp)/'mask.nii.gz', SimpleNamespace(), decode=True)
            self.addCleanup(report.widget.close)
            self.addCleanup(report.navigation.close)
            self.assertIn('QC was skipped by the user.', report.widget.children[0].value)
            self.assertIn('.report-header{color:red}', report.widget.children[0].value)
            self.assertIn('class="calmar-report"', report.widget.children[0].value)
            report.add_decoding('<p>first result</p>')
            report.add_decoding('<p>second result</p>')
            saved = path.read_text()
            self.assertNotIn('first result', saved)
            self.assertEqual(saved.count('Optional Neurosynth decoding'), 1)
            self.assertIn('Citation X', saved)
            self.assertIn('QC was skipped by the user.', saved)
            self.assertIn('second result', report.decode_html.value)

    def test_notebooks_have_unique_report_targets_and_no_stray_sections(self):
        root = Path(__file__).resolve().parents[1]
        for name in ('lesion-interpretation-pipeline.ipynb', 'calmar-guided.ipynb'):
            notebook = json.loads((root/name).read_text())
            roles = [c['metadata'].get('calmar', {}).get('role') for c in notebook['cells']]
            self.assertEqual(roles.count('report-selection'), 1)
            self.assertEqual(roles.count('report-start'), 1)
            self.assertFalse(any('Lesion viewer (now integrated above)' in ''.join(c['source']) for c in notebook['cells']))
        self.assertFalse(any('## Lesion segmentation' in ''.join(c['source']).splitlines() for c in json.loads((root/'lesion-interpretation-pipeline.ipynb').read_text())['cells']))


if __name__ == '__main__':
    unittest.main()
