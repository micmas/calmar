"""Scheduler receipt checks without submitting jobs or launching tools."""
import asyncio
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from calmar.scheduled import run_step, QC_VERSION


@pytest.mark.parametrize('receipt_job,logs,success', [('123',True,True),('122',True,False),('123',False,False)])
def test_only_fresh_matching_job_with_inspected_logs_is_accepted(tmp_path, receipt_job, logs, success):
    calls=[]
    def command(args, **kwargs):
        calls.append(args)
        if args[0]=='sbatch':
            assert kwargs['env']['CALMAR_PYTHON'] == sys.executable
            output=Path(args[-1]); output.mkdir()
            (output/'summary.json').write_text(json.dumps({'job':receipt_job,'stage':'brain','results':[]}))
            Path(str(output)+'.prov.json').write_text(json.dumps({'slurm_job_id':receipt_job,'output_id':'brain'}))
            if logs:
                for flag in ('--output','--error'):
                    Path(args[args.index(flag)+1]).write_text('')
            return SimpleNamespace(stdout='123\n')
        if args[0]=='squeue':
            return SimpleNamespace(stdout='')  # nothing already running
        assert args[0]=='sacct'
        return SimpleNamespace(stdout='123|COMPLETED|0:0\n')
    namespace={'PROJECT_DIR':tmp_path,'RAW_DATASET_DIR':tmp_path/'data','SUBJECTS':[],'CONFIG':{}}
    with patch('calmar.scheduled.subprocess.run',side_effect=command),patch('IPython.display.display'):
        if success:
            assert asyncio.run(run_step('brain',namespace))['job']=='123'
            assert list(tmp_path.rglob('log-review.json'))
        else:
            with pytest.raises(RuntimeError): asyncio.run(run_step('brain',namespace))
    assert list(tmp_path.rglob('submission.json'))  # Recovery ID survives failures.
    sbatch = next(c for c in calls if c[0] == 'sbatch')
    assert '--output' in sbatch and '--error' in sbatch
    assert '--export=ALL' in sbatch


def test_completed_step_reuses_receipt_across_namespaces_until_input_changes(tmp_path):
    from calmar.scheduled import run_step_sync
    t1 = tmp_path/'T1.nii.gz'; t1.write_bytes(b'original source')
    mask = tmp_path/'mask.nii.gz'; mask.write_bytes(b'published output')
    request = {'dataset': str(tmp_path), 'config': {},
               'entries': [{'subject':'sub-one', 't1w': str(t1)}]}
    result = {'job':'123', 'stage':'brain', 'request':request, 'qc_version':QC_VERSION, 'results':[
        {'subject':'sub-one', 'seconds':1, 'outputs':[{'path':str(mask), 'status':'computed'}]}]}
    submissions = []
    def command(args, **kwargs):
        if args[0] == 'sbatch':
            submissions.append(args)
            out = Path(args[-1]); out.mkdir()
            (out/'summary.json').write_text(json.dumps(result))
            Path(str(out)+'.prov.json').write_text(json.dumps({'slurm_job_id':'123', 'output_id':'brain'}))
            for flag in ('--output','--error'): Path(args[args.index(flag)+1]).write_text('')
            return SimpleNamespace(stdout='123\n')
        return SimpleNamespace(stdout='123|COMPLETED|0:0\n')
    def namespace():
        return dict(PROJECT_DIR=tmp_path, RAW_DATASET_DIR=tmp_path, SUBJECTS=request['entries'], CONFIG={})
    with patch('calmar.scheduled.subprocess.run', side_effect=command), patch('IPython.display.display'):
        run_step_sync('brain', namespace())
        run_step_sync('brain', namespace())
        assert len(submissions) == 1
        t1.write_bytes(b'changed source')
        run_step_sync('brain', namespace())
        assert len(submissions) == 2


def _fake_scheduler(tmp_path, submissions, qc_version=QC_VERSION):
    counter = iter(range(200, 300))
    def command(args, **kwargs):
        if args[0] == 'sbatch':
            job = str(next(counter))
            submissions.append(args)
            payload = json.loads(Path(args[-2]).read_text())
            out = Path(args[-1]); out.mkdir()
            results = [{'subject': e['subject'], 'seconds': 1, 'outputs': [{'path': e['t1w'], 'status': 'cached'}]}
                       for e in payload['entries']]
            summary = {'job': job, 'stage': 'brain', 'request': payload, 'results': results}
            if qc_version: summary['qc_version'] = qc_version
            (out/'summary.json').write_text(json.dumps(summary))
            Path(str(out)+'.prov.json').write_text(json.dumps({'slurm_job_id': job, 'output_id': 'brain'}))
            for flag in ('--output', '--error'): Path(args[args.index(flag)+1]).write_text('')
            return SimpleNamespace(stdout=job+'\n')
        if args[0] == 'sacct':
            return SimpleNamespace(stdout=f'{args[2]}|COMPLETED|0:0\n')
        return SimpleNamespace(stdout='')
    return command


def test_one_job_per_participant_and_per_participant_reuse(tmp_path):
    from calmar.scheduled import submit_step
    from calmar.study import Study
    entries = []
    for name in ('sub-a', 'sub-b'):
        t1 = tmp_path/f'{name}_T1w.nii.gz'; t1.write_bytes(name.encode())
        entries.append({'subject': name, 'session': None, 't1w': str(t1)})
    study = Study({}, tmp_path, tmp_path)
    submissions = []
    with patch('calmar.scheduled.subprocess.run', side_effect=_fake_scheduler(tmp_path, submissions)), \
            patch('IPython.display.display'):
        result = submit_step('brain', entries, study, timings={})
        assert len(submissions) == 2
        assert [r['subject'] for r in result['results']] == ['sub-a', 'sub-b']
        assert 'participant result' in repr(result)  # never dumps the raw request
        Path(entries[1]['t1w']).write_bytes(b'changed')
        submit_step('brain', entries, study)
        assert len(submissions) == 3  # only the changed participant is resubmitted
        assert 'sub-b' in submissions[-1][3]


def test_receipt_without_saved_qc_evidence_is_refreshed(tmp_path):
    from calmar.scheduled import submit_step
    from calmar.study import Study
    t1 = tmp_path/'T1w.nii.gz'; t1.write_bytes(b'x')
    entries = [{'subject': 'sub-a', 'session': None, 't1w': str(t1)}]
    submissions = []
    with patch('calmar.scheduled.subprocess.run', side_effect=_fake_scheduler(tmp_path, submissions, qc_version=None)), \
            patch('IPython.display.display'):
        submit_step('brain', entries, Study({}, tmp_path, tmp_path))
        submit_step('brain', entries, Study({}, tmp_path, tmp_path))
    assert len(submissions) == 2


def test_receipt_with_failed_qc_figure_is_retried(tmp_path):
    from calmar.scheduled import _cached, _store, _identity_key
    t1 = tmp_path/'T1w.nii.gz'; t1.write_bytes(b'x')
    payload = {'dataset': str(tmp_path), 'config': {}, 'entries': [{'subject': 'sub-a', 't1w': str(t1)}]}
    result = {'stage': 'linda', 'qc_version': QC_VERSION, 'request': payload,
              'results': [{'subject': 'sub-a', 'outputs': [{'path': str(t1), 'status': 'cached'}],
                           'qc': {'png': None, 'complete': False}}]}
    _store('linda', payload, tmp_path, result)
    assert _cached('linda', payload, tmp_path) is None
    result['results'][0]['qc'] = {'png': None, 'complete': True}
    _store('linda', payload, tmp_path, result)
    assert _cached('linda', payload, tmp_path) is not None


def test_reused_participants_are_labelled_with_their_original_job(tmp_path):
    from calmar.scheduled import submit_step
    from calmar.step_summary import step_html
    from calmar.study import Study
    t1 = tmp_path/'T1w.nii.gz'; t1.write_bytes(b'x')
    entries = [{'subject': 'sub-a', 'session': None, 't1w': str(t1)}]
    submissions = []
    with patch('calmar.scheduled.subprocess.run', side_effect=_fake_scheduler(tmp_path, submissions)), \
            patch('IPython.display.display'):
        first = submit_step('brain', entries, Study({}, tmp_path, tmp_path))
        again = submit_step('brain', entries, Study({}, tmp_path, tmp_path))
    assert 'reused_from_job' not in first['results'][0]
    assert again['results'][0]['reused_from_job'] == first['job']
    assert f"unchanged since Slurm job {first['job']}" in step_html(again)


def test_rerun_waits_for_the_job_already_running_for_the_same_request(tmp_path):
    from calmar.scheduled import _attach_running
    payload = {'dataset': str(tmp_path), 'config': {'LINDA_THREADS': 1},
               'entries': [{'subject': 'sub-one', 't1w': str(tmp_path/'T1.nii.gz')}]}
    folder = tmp_path/'reports'/'jobs'/'abc'; folder.mkdir(parents=True)
    (folder/'request.json').write_text(json.dumps(payload))
    (folder/'submission.json').write_text(json.dumps({'job_id': '77', 'stage': 'linda'}))
    def queue(running):
        return lambda args, **kwargs: SimpleNamespace(stdout=running)
    with patch('calmar.scheduled.subprocess.run', side_effect=queue('77\n')) as run:
        job = _attach_running('linda', payload, tmp_path)
    assert job['job'] == '77' and job['output'] == folder/'result'
    assert '--name=calmar_linda_sub-one' in run.call_args.args[0]
    with patch('calmar.scheduled.subprocess.run', side_effect=queue('')):
        assert _attach_running('linda', payload, tmp_path) is None          # finished
    changed = {**payload, 'config': {'LINDA_THREADS': 4}}
    with patch('calmar.scheduled.subprocess.run', side_effect=queue('77\n')):
        assert _attach_running('linda', changed, tmp_path) is None          # other settings


def test_dwi_inventory_only_changes_acquisition_cache_identity():
    from calmar.scheduled import _identity_key
    base = {'dataset': '/data', 'config': {},
            'entries': [{'subject': 'sub-one', 'session': 'ses-one', 't1w': '/data/T1w.nii.gz'}]}
    inventoried = {**base, 'entries': [{**base['entries'][0], 'dwi_inventory': [
        {'dwi': '/data/DWI.nii.gz', 'session': 'ses-two', 'same_session': False,
         'openads_ready': False, 'bval': '/data/DWI.bval'}]}]}
    assert _identity_key('brain', base) == _identity_key('brain', inventoried)
    assert _identity_key('acquisition', base) != _identity_key('acquisition', inventoried)


def test_optional_dwi_selection_only_changes_downstream_disconnectome_identity():
    from calmar.scheduled import _identity_key
    base = {'dataset': '/data', 'config': {'MODALITY': 't1'},
            'entries': [{'subject': 'sub-one', 'session': 'ses-t1', 't1w': '/data/T1w.nii.gz'}]}
    selected = {**base, 'entries': [{**base['entries'][0], 'dwi_analysis': {
        'subject': 'sub-one', 'session': 'ses-dwi', 'dwi': '/data/DWI.nii.gz',
        'adc': '/data/ADC.nii.gz', 't1w': '/data/DWI.nii.gz'}}]}
    assert _identity_key('brain', base) == _identity_key('brain', selected)
    assert _identity_key('bcb', base) != _identity_key('bcb', selected)
    toggled = {**base, 'config': {**base['config'], 'ANALYSE_DWI': True,
                                  '_DWI_ANALYSIS_SELECTED': True}}
    assert _identity_key('brain', base) == _identity_key('brain', toggled)


def test_inventory_does_not_hide_a_pre_inventory_running_job(tmp_path):
    from calmar.scheduled import _attach_running
    old = {'dataset': str(tmp_path), 'config': {},
           'entries': [{'subject': 'sub-one', 't1w': str(tmp_path/'T1.nii.gz')}]}
    current = {**old, 'entries': [{**old['entries'][0], 'dwi_inventory': [
        {'dwi': str(tmp_path/'DWI.nii.gz'), 'session': 'ses-two'}]}]}
    folder = tmp_path/'reports'/'jobs'/'pre-inventory'; folder.mkdir(parents=True)
    (folder/'request.json').write_text(json.dumps(old))
    (folder/'submission.json').write_text(json.dumps({'job_id': '88', 'stage': 'linda'}))
    with patch('calmar.scheduled.subprocess.run', return_value=SimpleNamespace(stdout='88\n')):
        assert _attach_running('linda', current, tmp_path)['job'] == '88'


def test_linda_cpus_follow_linda_threads():
    from calmar.scheduled import _resources
    assert _resources('linda', {'config': {}}) == ['--cpus-per-task=1']
    assert _resources('linda', {'config': {'LINDA_THREADS': 4}}) == ['--cpus-per-task=4']
    assert _resources('brain', {'config': {'LINDA_THREADS': 4}}) == []
    with pytest.raises(ValueError):
        _resources('linda', {'config': {'LINDA_THREADS': 0}})


def test_progress_reads_linda_steps(tmp_path, capsys):
    from calmar.job_progress import JobProgress, latest_step
    log = """03:50 Starting LINDA v0.5.1
03:52 1st round of prediction...
03:52     Running registration: SyN
 2DIAGNOSTIC,     5, -3.8e-01
04:06 3rd round of prediction...
04:06     Running registration: SyNCC
"""
    assert latest_step(log) == 'round 3/3: SyNCC registration since 04:06 (slowest step, 1-3.5 h)'
    assert latest_step('03:52 1st round of prediction...') == '1st round of prediction since 03:52'
    assert latest_step('plain line\nlast line') == 'last line'
    entry = {'subject': 'sub-one', 'session': 'ses-1'}
    attempt = tmp_path/'derivatives/linda/sub-one/ses-1/anat.attempt.x/anat'; attempt.mkdir(parents=True)
    (attempt/'processing.log').write_text(log)
    job = {'job': '9', 'started': 0, 'payload': {'dataset': str(tmp_path), 'config': {}, 'entries': [entry]}}
    progress = JobProgress('linda', [job])                                   # not live: prints changes
    progress.update(job, 'PENDING'); progress.update(job, 'PENDING'); progress.update(job, 'RUNNING')
    lines = capsys.readouterr().out.splitlines()
    assert lines == ['linda · sub-one ses-1 · Slurm job 9: queued',
                     'linda · sub-one ses-1 · Slurm job 9: running · ' + latest_step(log)]
    assert progress.line().startswith('linda · sub-one ses-1 · Slurm job 9 · running ')
    assert progress.line().endswith(latest_step(log))


def test_live_progress_rewrites_one_line(capsys, monkeypatch):
    from calmar import job_progress
    monkeypatch.setattr(job_progress, '_live', lambda: True)
    jobs = [{'job': str(n), 'started': 0, 'payload': {'entries': [{'subject': f'sub-{n}'}]}} for n in (1, 2)]
    progress = job_progress.JobProgress('acquisition', jobs)
    progress.update(jobs[0], 'COMPLETED'); progress.update(jobs[1], 'RUNNING', '')
    progress.refresh(); progress.finish()
    out = capsys.readouterr().out
    assert out.count('\n') == 1 and out.endswith('\n')                    # one line in the notebook
    assert '\racquisition · 2 jobs · 1 done, 1 running · ' in out
    assert out.rstrip('\n').split('\r')[-1].startswith('acquisition · 2 jobs done in ')
