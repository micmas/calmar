from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import nibabel as nib
import numpy as np
import pytest

from calmar.atlas_overlap import cached_overlap
from calmar.guided import source_cell
from calmar.timing import BatchTiming, install_timing, show_timings


def test_durations_outcomes_reruns_and_participant_totals():
    ns = {}
    entry = dict(subject='sub-test', session='ses-1')
    with patch('calmar.timing.display') as display, patch('calmar.timing.time.perf_counter', side_effect=[0, 1, 3, 4, 9, 10]):
        with BatchTiming(ns, 'Segmentation') as batch:
            with batch.participant(entry, 'HD-BET') as timing:
                timing['status'] = 'Cached'
            with pytest.raises(ValueError), batch.participant(entry, 'LINDA'):
                raise ValueError('failed computation')
    record = ns['BATCH_TIMINGS']['Segmentation']
    rows = list(record['participants'].values())
    assert [row['seconds'] for row in rows] == [2, 5]
    assert [row['status'] for row in rows] == ['Cached', 'Interrupted or failed']
    assert record['seconds'] == 10
    assert 'ses-1' in display.call_args.args[0].data
    with patch('calmar.timing.display') as display:
        show_timings(ns)
        assert '7.0 s' in display.call_args.args[0].data
        with BatchTiming(ns, 'Segmentation') as batch:
            with batch.participant(entry, 'LINDA') as timing:
                timing['status'] = 'Cached'
    assert len(ns['BATCH_TIMINGS']['Segmentation']['participants']) == 1


def test_batch_segmentation_records_cached_failed_and_new_participants(tmp_path):
    entries = [dict(subject=f'sub-{kind}', session='ses-1', t1w=tmp_path/f'{kind}_T1w.nii.gz')
               for kind in ('cached', 'failed', 'new')]
    directory = lambda e: tmp_path/e['subject']/'linda'
    brain_dir = lambda e: tmp_path/e['subject']/'hdbet'
    directory(entries[0]).mkdir(parents=True)
    (directory(entries[0])/'Lesion_in_MNI.nii.gz').write_bytes(b'existing-output')
    def extract(t1, output, **kw):
        if t1.name.startswith('failed'):
            return dict(returncode=1)
        (output/(t1.name.replace('.nii.gz','')+'_brain_mask.nii.gz')).write_bytes(b'mask')
        return dict(returncode=0)
    def segment(command, log, **kw):
        out = Path(command[command.index('--outdir')+1])
        (out/'Lesion_in_MNI.nii.gz').write_bytes(b'new-output')
        return SimpleNamespace(returncode=0)
    ns = dict(CONFIG=dict(RUN_SEGMENTATION=True), SUBJECTS=entries, Path=Path,
              deriv_path_for=directory, hdbet_path_for=brain_dir,
              q=SimpleNamespace(run_hd_bet=Mock(side_effect=extract)),
              importlib=SimpleNamespace(reload=lambda obj: obj))
    with patch('calmar.process_output.run_logged', side_effect=segment) as run, patch('calmar.timing.display'):
        exec(''.join(source_cell(42)['source']), ns)
    rows = list(ns['BATCH_TIMINGS']['Brain extraction and LINDA']['participants'].values())
    assert [(r['stage'], r['status']) for r in rows] == [
        ('HD-BET', 'Not needed (LINDA cached)'), ('LINDA', 'Cached'),
        ('HD-BET', 'Failed'), ('LINDA', 'Skipped (brain extraction failed)'),
        ('HD-BET', 'Completed'), ('LINDA', 'Completed')]
    assert run.call_count == 1
    assert (directory(entries[0])/'Lesion_in_MNI.nii.gz').read_bytes() == b'existing-output'


def test_atlas_timing_records_cached_zero_and_missing_masks(tmp_path):
    atlas = nib.Nifti1Image(np.ones((2, 2, 2), dtype=np.uint8), np.eye(4))
    path = tmp_path/'mask.nii.gz'
    nib.save(nib.Nifti1Image(np.zeros((2,2,2), dtype=np.uint8), np.eye(4)), path)
    entries = [dict(subject='sub-a', session=s) for s in ('ses-present','ses-missing')]
    resolver = lambda e: path if e['session']=='ses-present' else tmp_path/'missing.nii.gz'
    ns = {}
    for expected in ('Completed', 'Cached'):
        with patch('calmar.timing.display'), BatchTiming(ns, 'Atlas overlap') as batch:
            cached_overlap(tmp_path/'overlap.csv', entries, resolver, 'Atlas', atlas,
                           np.asarray(atlas.dataobj), ['Background','ROI'], participant_timer=batch.participant)
        assert [r['status'] for r in batch.record['participants'].values()] == [expected, 'Missing input']


def test_install_replaces_hooks_and_excludes_guided_wrapper():
    class Events:
        callbacks = {'pre_run_cell': [], 'post_run_cell': []}
        def register(self, event, callback): self.callbacks[event].append(callback)
        def unregister(self, event, callback): self.callbacks[event].remove(callback)
    shell = SimpleNamespace(events=Events())
    ns = {}
    install_timing(ns, shell); install_timing(ns, shell)
    assert all(len(callbacks)==1 for callbacks in shell.events.callbacks.values())
    before, after = shell._calmar_timing_hooks
    with patch('calmar.timing.time.perf_counter', side_effect=[1, 5, 6]):
        before(SimpleNamespace(raw_cell='# CALMAR_CELL_ID: calmar-step-42\npass'))
        after(None)
        before(SimpleNamespace(raw_cell='await run_cells([42, 44], globals())'))
        after(None)
    assert ns['STEP_TIMINGS'] == {'calmar-step-42': 4}


def test_process_log_retains_details_without_printing_success_debug(tmp_path, capsys):
    import sys
    from calmar.process_output import run_logged
    path = tmp_path/'logs'/'tool.log'
    result = run_logged([sys.executable, '-c', 'print("internal tool diagnostic")'], path)
    assert result.returncode == 0
    assert 'internal tool diagnostic' in path.read_text()
    assert 'internal tool diagnostic' not in capsys.readouterr().out
    result = run_logged([sys.executable, '-c', 'print("failure detail"); raise SystemExit(3)'], path)
    assert result.returncode == 3
    assert 'failure detail' in capsys.readouterr().out
