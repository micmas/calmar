"""Choose the single-subject test participant before any processing starts."""

from html import escape
from pathlib import Path

import ipywidgets as w
from IPython import get_ipython
from IPython.display import display

from .execution import ExecutionCheckpoint
from .notebook_navigation import NotebookNavigation


def processing_status(entry, namespace):
    linda = Path(namespace['deriv_path_for'](entry))
    synth = Path(namespace['synthstroke_path_for'](entry))
    brain = Path(namespace['hdbet_path_for'](entry))
    present = lambda p: p.is_file() and p.stat().st_size > 0
    from calmar.study import segmentation_methods
    wanted = {'linda': linda/'Lesion_in_MNI.nii.gz', 'synthstroke': synth/'SynthStroke_in_MNI.nii.gz'}
    if all(present(wanted[m]) for m in segmentation_methods(namespace.get('CONFIG', {}))):
        return 'Segmentations available'
    if any(present(p) for folder in (linda, synth, brain) for p in folder.glob('*.nii.gz')):
        return 'Partly processed'
    return 'Not processed'


class SingleSubjectInputs:
    def __init__(self, namespace, shell=None):
        self.ns = namespace
        self.entries = [dict(e) for e in namespace['SUBJECTS']]
        if not self.entries:
            raise ValueError('Run participant discovery before choosing a test participant.')
        statuses = [processing_status(e, namespace) for e in self.entries]
        pairs = [(e['subject'], e.get('session') or '') for e in self.entries]
        previous = namespace.get('_CALMAR_TEST_SELECTION')
        index = (pairs.index(previous) if previous in pairs else
                 next((i for i, status in enumerate(statuses) if status == 'Not processed'),
                      next((i for i, status in enumerate(statuses) if status == 'Partly processed'), 0)))
        self.subject = w.Dropdown(options=[
            (f"{e['subject']} {e.get('session') or ''} — {statuses[i]}", i)
            for i, e in enumerate(self.entries)], value=index, description='Test participant:',
            style={'description_width': 'initial'}, layout=w.Layout(width='620px', max_width='100%'))
        self.message = w.HTML()
        self.gate = ExecutionCheckpoint(shell, 'Choose the test participant and click Run single-subject test.') if shell else None
        self.navigation = NotebookNavigation(self.message,
            on_cell_order=self.gate._update_cell_order if self.gate else None)
        self.start = w.Button(description='Run single-subject test', button_style='primary',
                              layout=w.Layout(width='230px'))
        self.start.on_click(lambda _: self.navigation.request('single-test-start', self.approve))
        self.subject.observe(self.apply, names='value')
        self.widget = w.VBox([w.HTML('<h3>Choose the single-subject test participant</h3>'
            'The default is a participant without processing outputs, when available. '
            'This selection applies to all single-subject processing and viewers below.'),
            self.subject, self.start, self.message, self.navigation])
        if self.gate:
            self.gate.controls = [self.widget, self.navigation]
        self.apply()

    def apply(self, *_):
        index = self.subject.value
        entry = self.entries[index]
        self.ns['TEST_SUBJECT_IDX'] = self.ns['CONFIG']['TEST_SUBJECT_IDX'] = index
        self.ns['_CALMAR_TEST_SELECTION'] = (entry['subject'], entry.get('session') or '')
        self.ns['DIAG_SUBJECT_IDX'] = self.ns['CMP_SUBJECT_IDX'] = None
        self.message.value = f"Selected <b>{escape(entry['subject'])} {escape(entry.get('session') or '')}</b>. Click Run single-subject test to begin."

    def approve(self):
        self.apply()
        # A fresh test selection supersedes older downstream in-memory gates.
        if self.gate:
            for name in ('_calmar_batch_checkpoint', '_calmar_qc_checkpoint', '_calmar_report_checkpoint'):
                previous = getattr(self.gate.shell, name, None)
                if previous:
                    previous.close()
            self.gate.release()
        self.message.value = 'Starting the selected single-subject test…'
        return True

    def close(self):
        if self.gate:
            self.gate.close()
        else:
            self.navigation.close()
            self.widget.close()


def show_single_subject_inputs(namespace):
    previous = namespace.get('_single_subject_inputs')
    if previous:
        previous.close()
    panel = SingleSubjectInputs(namespace, get_ipython())
    namespace['_single_subject_inputs'] = panel
    display(panel.widget)
    if panel.gate:
        panel.gate._cancel_queued()
    return panel
