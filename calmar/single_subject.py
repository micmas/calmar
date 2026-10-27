"""Choose the single-subject test participant before any processing starts."""

import hashlib
from html import escape
import json
from pathlib import Path

import ipywidgets as w
from IPython import get_ipython
from IPython.display import display

from .execution import ExecutionCheckpoint
from .notebook_navigation import NotebookNavigation


OPTIONAL_ENTRY_FIELDS = (
    'subject', 'session', 'anatomical_session', 'dwi', 'adc', 'bval', 'bvec',
    'json', 'anatomical_t1w', 'flair', 'brain_health_components',
)


def optional_entry_key(entry):
    """Stable identity for one selected optional-analysis entry."""
    values = []
    for field in OPTIONAL_ENTRY_FIELDS:
        value = entry.get(field)
        if isinstance(value, (list, tuple, set)):
            value = tuple(sorted(map(str, value)))
        elif value is not None:
            value = str(value)
        values.append(value)
    return tuple(values)


def _anatomical_session(entry):
    """Linked anatomy session; an explicit ``None`` means sessionless anatomy."""
    return entry['anatomical_session'] if 'anatomical_session' in entry else entry.get('session')


def optional_entries_for_test(entries, test_entry):
    """Optional entries linked to the selected anatomical test session.

    Trace-DWI and directional-dMRI entries can use another imaging session;
    ``anatomical_session`` keeps them attached to the T1w session selected for
    the single-subject test.
    """
    subject = test_entry['subject']
    session = test_entry.get('session')
    return [entry for entry in (entries or ())
            if entry.get('subject') == subject
            and _anatomical_session(entry) == session]


def _path_stamp(path):
    try:
        path = Path(path)
        stat = path.stat()
        return [str(path.resolve()), stat.st_mtime_ns, stat.st_size]
    except (OSError, TypeError):
        return [str(path), None, None]


def optional_run_signature(route, entry, study):
    """Hash the selected entry, settings and upstream files for one optional route."""
    from .scheduled import _identity_key
    config = study.config_for(entry) if hasattr(study, 'config_for') else study.config
    dataset = study.dataset_for(entry) if hasattr(study, 'dataset_for') else study.dataset
    inputs = []
    for field in ('t1w', 'dwi', 'adc', 'bval', 'bvec', 'json', 'anatomical_t1w', 'flair'):
        if entry.get(field):
            inputs.append(entry[field])
    inputs.extend(entry.get('dwi_series') or ())
    if route in ('dmri', 'brain_health') and hasattr(study, 'masks'):
        source_key = 'DMRI_MASK_SOURCE' if route == 'dmri' else 'BRAIN_HEALTH_MASK_SOURCE'
        try:
            anatomical = {**entry, 'session': _anatomical_session(entry)}
            selected = study.masks(anatomical).get(config.get(source_key, 'manual'), {}).get('T1w')
            if selected is not None:
                inputs.append(selected)
        except (KeyError, TypeError, ValueError):
            pass
    stages = {
        'dwi': ('acquisition', 'openads'),
        'dmri': ('dmri_preproc', 'dmri_recon', 'dmri_metrics'),
        'brain_health': ('brain_health_anatomy', 'brain_health_wmh', 'brain_health_metrics'),
    }[route]
    request = {'dataset': str(dataset), 'config': config, 'entries': [entry]}
    payload = {
        'route': route, 'stage_identities': [_identity_key(stage, request) for stage in stages],
        'inputs': [_path_stamp(path) for path in inputs],
    }
    encoded = json.dumps(payload, default=str, sort_keys=True, separators=(',', ':')).encode()
    return hashlib.sha256(encoded).hexdigest()


def mark_optional_completed(state, route, entries, study, results):
    """Record successful single-test work with its settings and file stamps."""
    from .scheduled import _result_stamps
    try:
        watched = [{'result': result, 'stamps': _result_stamps(result)} for result in results]
        if any(item['stamps'] is None for item in watched):
            return False
        records = [(optional_entry_key(entry), optional_run_signature(route, entry, study))
                   for entry in entries]
    except Exception:
        return False
    bucket = state.setdefault(route, {})
    for key, signature in records:
        bucket[key] = {'signature': signature, 'watched': watched}
    return True


def pending_optional_entries(entries, completed, *, route=None, study=None):
    """Selected entries not safely reusable from this kernel's single test."""
    from .scheduled import _result_stamps
    pending = []
    for entry in entries or ():
        try:
            record = completed.get(optional_entry_key(entry)) if isinstance(completed, dict) else None
            reusable = bool(record and route and study and
                            record.get('signature') == optional_run_signature(route, entry, study))
            if reusable:
                for watched in record.get('watched', ()):
                    if (watched.get('stamps') is None or
                            watched['stamps'] != _result_stamps(watched['result'])):
                        reusable = False
                        break
        except Exception:
            reusable = False
        if not reusable:
            pending.append(entry)
    return pending


def processing_status(entry, namespace):
    linda = Path(namespace['deriv_path_for'](entry))
    synth = Path(namespace['synthstroke_path_for'](entry))
    brain = Path(namespace['hdbet_path_for'](entry))
    present = lambda p: p.is_file() and p.stat().st_size > 0
    from calmar.study import config_for_entry, segmentation_methods
    wanted = {'linda': linda/'Lesion_in_MNI.nii.gz', 'synthstroke': synth/'SynthStroke_in_MNI.nii.gz'}
    if 'openads_path_for' in namespace:          # acute (DWI) route
        wanted['openads'] = Path(namespace['openads_path_for'](entry))/'OpenADS_in_MNI.nii.gz'
    config = config_for_entry(namespace.get('CONFIG', {}), entry)
    if all(m in wanted and present(wanted[m]) for m in segmentation_methods(config)):
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
        self.skip = w.Button(description='Skip single-subject test', button_style='warning',
                             layout=w.Layout(width='230px'))
        self.skip.on_click(lambda _: self.navigation.request(
            'batch-start', self.skip_test,
            prompt='Skip the single-subject test and start batch processing now?'))
        from .method_choice import MethodChoice
        self.methods = MethodChoice(namespace['CONFIG'], on_change=self._methods_changed)
        self.subject.observe(self.apply, names='value')
        self.widget = w.VBox([w.HTML('<h3>Choose the single-subject test participant</h3>'
            'The default is a participant without processing outputs, when available. '
            'This selection applies to all single-subject processing and viewers below. '
            'To process the whole cohort without a test run, choose <b>Skip single-subject test</b>.'),
            self.subject, self.methods.widget, w.HBox([self.start, self.skip]),
            self.message, self.navigation])
        if self.gate:
            self.gate.controls = [self.widget, self.navigation]
        self.apply()

    def apply(self, *_):
        index = self.subject.value
        entry = self.entries[index]
        self.ns['TEST_SUBJECT_IDX'] = self.ns['CONFIG']['TEST_SUBJECT_IDX'] = index
        self.ns['_CALMAR_TEST_SELECTION'] = (entry['subject'], entry.get('session') or '')
        self.ns['DIAG_SUBJECT_IDX'] = self.ns['CMP_SUBJECT_IDX'] = None
        self.message.value = (f"Selected <b>{escape(entry['subject'])} "
                              f"{escape(entry.get('session') or '')}</b>. Run the single-subject test "
                              "or skip it and start the batch.")

    def _methods_changed(self, valid):
        self.start.disabled = self.skip.disabled = not valid

    def _release_for_processing(self):
        """Release this gate and discard stale downstream checkpoints."""
        if self.gate:
            for name in ('_calmar_batch_checkpoint', '_calmar_qc_checkpoint', '_calmar_report_checkpoint'):
                previous = getattr(self.gate.shell, name, None)
                if previous:
                    previous.close()
            self.gate.release()
        self.methods.disable()
        self.start.disabled = self.skip.disabled = True

    def approve(self):
        if not self.methods.valid:
            self.message.value = 'Choose at least one lesion segmentation.'
            return False
        self.apply()
        # Skip affects only the current continuation. Re-entering this panel
        # must always make the explicit test choice available again.
        self.ns['RUN_TEST'] = True
        # A fresh test selection supersedes older downstream in-memory gates.
        self._release_for_processing()
        self.message.value = f'Starting the selected single-subject test ({self.methods.summary()})…'
        return True

    def skip_test(self):
        """Skip the test cells and continue at the cohort batch entry point."""
        if not self.methods.valid:
            self.message.value = 'Choose at least one lesion segmentation.'
            return False
        self.apply()
        self.ns['RUN_TEST'] = False
        self._release_for_processing()
        self.message.value = (f'Skipping the single-subject test; starting batch processing '
                              f'({self.methods.summary()})…')
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
