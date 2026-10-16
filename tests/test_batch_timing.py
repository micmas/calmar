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


def test_batch_runs_retained_stages_and_stops_after_failure():
    ns = dict(SUBJECTS=[], study=None, BATCH_TIMINGS={})
    with patch("calmar.scheduled.submit_step",side_effect=RuntimeError("brain extraction failed")) as run:
        with pytest.raises(RuntimeError,match="brain extraction failed"):
            exec("".join(source_cell(42)["source"]),ns)
    assert [call.args[0] for call in run.call_args_list] == ["brain"]


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


def test_temporary_tool_logs_survive_timeout_and_staging_cleanup(tmp_path, monkeypatch):
    import shutil
    import subprocess
    from calmar.process_output import run_logged
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv('SLURM_JOB_ID', 'fixture')
    staging = tmp_path/'map.attempt.fixture'; staging.mkdir()
    (staging/'nested.log').write_text('full nested diagnostic')
    def timeout(command, stdout, **kwargs):
        stdout.write('partial progress')
        raise subprocess.TimeoutExpired(command, 1)
    with patch('calmar.process_output.subprocess.run', side_effect=timeout):
        with pytest.raises(subprocess.TimeoutExpired):
            run_logged(['tool'], staging/'processing.log', timeout=1)
    shutil.rmtree(staging)
    retained = list((tmp_path/'logs/processing_attempts/fixture').glob('*'))
    assert len(retained) == 1
    assert (retained[0]/'processing.log').read_text() == 'partial progress'
    assert (retained[0]/'nested.log').read_text() == 'full nested diagnostic'
