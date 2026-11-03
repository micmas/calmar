"""Scheduler receipt checks without submitting jobs or launching tools."""
import asyncio
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from calmar.scheduled import (QC_VERSION, cached_step_results, previous_step_results,
                             run_step, usable_previous_step_results)


def test_cache_inspection_is_read_only_and_preserves_entry_order(tmp_path):
    entries = [{"subject": "sub-a", "t1w": "a.nii.gz"},
               {"subject": "sub-b", "t1w": "b.nii.gz"}]
    study = SimpleNamespace(dataset=tmp_path / "data", config={"SETTING": 1}, project=tmp_path)
    seen = []

    def cached(stage, payload, project):
        seen.append((stage, payload, project))
        subject = payload["entries"][0]["subject"]
        return {"subject": subject} if subject == "sub-a" else None

    with patch("calmar.scheduled._cached", side_effect=cached), \
         patch("calmar.scheduled._submit") as submit:
        results = cached_step_results("dmri_preproc", entries, study)
    assert results == [{"subject": "sub-a"}, None]
    assert [call[1]["entries"][0]["subject"] for call in seen] == ["sub-a", "sub-b"]
    assert all(call[0] == "dmri_preproc" and call[2] == tmp_path for call in seen)
    submit.assert_not_called()


def test_usable_prior_inspection_applies_scheduler_dependency_gate(tmp_path):
    entries = [{"subject": "sub-one", "t1w": "t1.nii.gz"}]
    study = SimpleNamespace(dataset=tmp_path / "data", config={}, project=tmp_path)
    prior = {"job": "91", "results": []}

    def dependency_check(stage, payload, project):
        assert stage == "dmri_recon" and project == tmp_path
        assert payload["config"]["DMRI_REUSE_PRIOR"] is True
        return dependency_check.accept

    with patch("calmar.scheduled._previous", return_value=prior), \
         patch("calmar.scheduled._prior_matches_dependencies", side_effect=dependency_check):
        dependency_check.accept = False
        assert usable_previous_step_results("dmri_recon", entries, study) == [None]
        dependency_check.accept = True
        assert usable_previous_step_results("dmri_recon", entries, study) == [prior]


def test_prior_with_incomplete_qc_is_never_offered_for_explicit_reuse(tmp_path):
    output = tmp_path / "result.nii.gz"
    output.write_bytes(b"result")
    entry = {"subject": "sub-one", "t1w": str(tmp_path / "t1.nii.gz")}
    study = SimpleNamespace(dataset=tmp_path, config={}, project=tmp_path)
    receipt = {"result": {
        "stage": "dmri_preproc", "qc_version": QC_VERSION,
        "results": [{"subject": "sub-one", "qc": {"complete": False},
                     "outputs": [{"path": str(output)}]}],
    }}

    with patch("calmar.scheduled._receipt", return_value=receipt):
        assert previous_step_results("dmri_preproc", [entry], study) == [None]


def test_route_overwrite_policy_overrides_global_and_is_not_receipt_identity():
    from calmar.scheduled import _identity_key, _reusable

    entry = {"subject": "sub-one", "t1w": "/data/t1.nii.gz"}
    for stage, key in (("openads", "OPENADS_OVERWRITE"),
                       ("dmri_preproc", "DMRI_OVERWRITE"),
                       ("brain_health_anatomy", "BRAIN_HEALTH_OVERWRITE")):
        payload = {"dataset": "/data", "entries": [entry],
                   "config": {"OVERWRITE": True, key: False}}
        assert _reusable(stage, payload) is True
        changed = {**payload, "config": {**payload["config"], "OVERWRITE": False, key: True}}
        assert _reusable(stage, changed) is False
        assert _identity_key(stage, payload) == _identity_key(stage, changed)

    unrelated = {"dataset": "/data", "entries": [entry],
                 "config": {"DEEPDISCO_OVERWRITE": True, "BCB_OVERWRITE": True}}
    assert _reusable("dmri_preproc", unrelated) is True
    assert _reusable("brain_health_anatomy", unrelated) is True
    assert _reusable("deepdisco", unrelated) is False
    assert _reusable("bcb", unrelated) is False


def test_explicit_prior_reuse_is_labelled_and_rerun_remains_participant_specific(tmp_path):
    from calmar.scheduled import _MEMORY_CACHE, _split, _store, submit_step
    from calmar.step_summary import step_html
    from calmar.study import ENTRY_CONFIG, Study

    source = tmp_path / "dwi.nii.gz"
    output = tmp_path / "published"
    source.write_bytes(b"original")
    output.mkdir()
    product = output / "mask.nii.gz"
    product.write_bytes(b"mask-v1")
    base_entry = {"subject": "sub-one", "session": "ses-one", "t1w": str(source),
                  "dwi": str(source), "adc": str(source)}
    study = Study({"MODALITY": "dwi", "SEGMENTATION_METHODS": ["openads"]}, tmp_path, tmp_path)
    request = {"dataset": str(study.dataset), "config": study.config, "entries": [base_entry]}
    payload = _split("openads", request)[0]
    result = {"stage": "openads", "job": "77", "request": payload, "qc_version": QC_VERSION,
              "results": [{"subject": "sub-one", "session": "ses-one", "seconds": 1,
                           "outputs": [{"path": str(product), "status": "computed"}],
                           "qc": {"complete": True}}]}
    _store("openads", payload, tmp_path, result)
    source.write_bytes(b"changed")
    _MEMORY_CACHE.clear()

    assert cached_step_results("openads", [base_entry], study) == [None]
    assert previous_step_results("openads", [base_entry], study)[0]["job"] == "77"

    use_entry = {**base_entry, ENTRY_CONFIG: {"OPENADS_REUSE_PRIOR": True}}
    with patch("calmar.scheduled._submit") as submit:
        reused = submit_step("openads", [use_entry], study)
    submit.assert_not_called()
    assert reused["results"][0]["prior_result_from_job"] == "77"
    assert "explicit choice" in step_html(reused)

    # A path merely existing is insufficient: another run may have replaced
    # the files at that path with outputs from different inputs.
    product.write_bytes(b"mask-v2")
    _MEMORY_CACHE.clear()
    assert previous_step_results("openads", [base_entry], study) == [None]

    rerun_entry = {**base_entry, ENTRY_CONFIG: {"OPENADS_OVERWRITE": True}}
    from calmar.scheduled import _reusable
    rerun_payload = _split("openads", {
        "dataset": str(study.dataset), "config": study.config, "entries": [rerun_entry]})[0]
    assert not _reusable("openads", rerun_payload)
    rerun_result = {**result, "job": "88", "request": rerun_payload}
    _store("openads", rerun_payload, tmp_path, rerun_result)
    _MEMORY_CACHE.clear()
    assert cached_step_results("openads", [base_entry], study)[0]["job"] == "88"


def test_downstream_result_records_explicit_prior_dependency(tmp_path):
    from calmar.scheduled import _prior_dependencies
    payload = {"dataset": str(tmp_path), "config": {"DMRI_REUSE_PRIOR": True},
               "entries": [{"subject": "sub-one", "brain_health_components": []}]}
    prior = {"job": "91", "results": []}
    with patch("calmar.scheduled._cached", return_value=None), \
         patch("calmar.scheduled._previous", return_value=prior):
        markers = _prior_dependencies("dmri_recon", payload, tmp_path)
    assert markers == [{"stage": "dmri_preproc", "job": "91"}]


def test_downstream_prior_is_rejected_after_upstream_job_advances(tmp_path):
    from calmar.scheduled import _prior_matches_dependencies
    payload = {"dataset": str(tmp_path), "config": {"DMRI_REUSE_PRIOR": True},
               "entries": [{"subject": "sub-one"}]}
    metrics_receipt = {"stored_ns": 10, "result": {
        "job": "92", "upstream_jobs": {"dmri_preproc": "90", "dmri_recon": "91"}}}
    recon_receipt = {"stored_ns": 20, "result": {"job": "99"}}

    def receipt(stage, payload, project):
        return {"dmri_metrics": metrics_receipt, "dmri_recon": recon_receipt}.get(stage)

    def cached(stage, payload, project):
        return {"dmri_preproc": {"job": "90"}, "dmri_recon": {"job": "99"}}.get(stage)

    with patch("calmar.scheduled._receipt", side_effect=receipt), \
         patch("calmar.scheduled._cached", side_effect=cached):
        assert not _prior_matches_dependencies("dmri_metrics", payload, tmp_path)


def test_downstream_prior_matches_current_or_explicit_prior_upstream_job(tmp_path):
    from calmar.scheduled import _prior_matches_dependencies
    payload = {"dataset": str(tmp_path), "config": {"DMRI_REUSE_PRIOR": True},
               "entries": [{"subject": "sub-one"}]}
    metrics = {"stored_ns": 20, "result": {"job": "92", "upstream_jobs": {
        "dmri_preproc": "90", "dmri_recon": "91"}}}

    def receipt(stage, payload, project):
        return metrics if stage == "dmri_metrics" else {"stored_ns": 10, "result": {}}

    upstream = {"dmri_preproc": {"job": "90"}, "dmri_recon": {"job": "91"}}
    with patch("calmar.scheduled._receipt", side_effect=receipt), \
         patch("calmar.scheduled._cached", side_effect=lambda stage, *_: upstream.get(stage)):
        assert _prior_matches_dependencies("dmri_metrics", payload, tmp_path)

    # A stale upstream is also safe only when the exact job used downstream is
    # the one that will now be retained.
    with patch("calmar.scheduled._receipt", side_effect=receipt), \
         patch("calmar.scheduled._cached", return_value=None), \
         patch("calmar.scheduled._previous",
               side_effect=lambda stage, *_: upstream.get(stage)):
        assert _prior_matches_dependencies("dmri_metrics", payload, tmp_path)
    changed = {**upstream, "dmri_recon": {"job": "99"}}
    with patch("calmar.scheduled._receipt", side_effect=receipt), \
         patch("calmar.scheduled._cached", return_value=None), \
         patch("calmar.scheduled._previous",
               side_effect=lambda stage, *_: changed.get(stage)):
        assert not _prior_matches_dependencies("dmri_metrics", payload, tmp_path)


def test_legacy_receipt_order_rejects_newer_upstream_and_accepts_older(tmp_path):
    from calmar.scheduled import _prior_matches_dependencies
    payload = {"dataset": str(tmp_path), "config": {"DMRI_REUSE_PRIOR": True},
               "entries": [{"subject": "sub-one"}]}
    legacy = {"result": {"job": "92"}}  # no upstream_jobs and no stored_ns
    current = {"job": "91"}

    def receipt(stage, payload, project):
        return legacy

    with patch("calmar.scheduled._receipt", side_effect=receipt), \
         patch("calmar.scheduled._cached", return_value=current), \
         patch("calmar.scheduled._receipt_time",
               side_effect=lambda stage, *_: 10 if stage == "dmri_recon" else 20):
        assert not _prior_matches_dependencies("dmri_recon", payload, tmp_path)
    with patch("calmar.scheduled._receipt", side_effect=receipt), \
         patch("calmar.scheduled._cached", return_value=current), \
         patch("calmar.scheduled._receipt_time",
               side_effect=lambda stage, *_: 10 if stage == "dmri_recon" else 5):
        assert _prior_matches_dependencies("dmri_recon", payload, tmp_path)


def test_receipt_token_rejects_reused_slurm_job_number(tmp_path):
    from calmar.scheduled import _prior_matches_dependencies
    payload = {"dataset": str(tmp_path), "config": {"DMRI_REUSE_PRIOR": True},
               "entries": [{"subject": "sub-one"}]}
    metrics = {"stored_ns": 30, "result": {
        "job": "91", "upstream_receipts": {
            "dmri_preproc": {"job": "90", "stored_ns": 10}}}}
    preproc = {"stored_ns": 20, "result": {"job": "90"}}

    with patch("calmar.scheduled._receipt",
               side_effect=lambda stage, *_: metrics if stage == "dmri_recon" else preproc), \
         patch("calmar.scheduled._cached", return_value={"job": "90"}):
        assert not _prior_matches_dependencies("dmri_recon", payload, tmp_path)


def test_normal_current_cache_is_not_reused_after_dependency_advances(tmp_path):
    from calmar.scheduled import _run_payloads
    payload = {"dataset": str(tmp_path), "config": {"MODALITY": "t1"},
               "entries": [{"subject": "sub-one", "t1w": str(tmp_path / "t1.nii.gz")}]}
    fresh = {"job": "99", "stage": "dmri_recon", "results": [{
        "subject": "sub-one", "outputs": [], "seconds": 1}]}
    job = {"job": "99", "folder": tmp_path, "output": tmp_path / "result",
           "payload": payload, "result": fresh, "upstream_receipts": {}}
    progress = SimpleNamespace(update=lambda *a, **k: None, refresh=lambda: None,
                               finish=lambda **k: None)
    with patch("calmar.scheduled._cached", return_value={"job": "91", "results": []}), \
         patch("calmar.scheduled._prior_matches_dependencies", return_value=False), \
         patch("calmar.scheduled._upstream_receipts", return_value={}), \
         patch("calmar.scheduled._attach_running", return_value=None), \
         patch("calmar.scheduled._submit", return_value=job) as submit, \
         patch("calmar.scheduled._poll", return_value=True), \
         patch("calmar.scheduled._prior_dependencies", return_value=[]), \
         patch("calmar.scheduled._store"), \
         patch("calmar.scheduled.JobProgress", return_value=progress):
        result = _run_payloads("dmri_recon", [payload], tmp_path, 10)
    submit.assert_called_once()
    assert result["job"] == "99"


def test_running_job_with_different_upstream_receipt_is_not_attached(tmp_path):
    from calmar.scheduled import _attach_running
    payload = {"dataset": str(tmp_path), "config": {"MODALITY": "t1"},
               "entries": [{"subject": "sub-one", "t1w": "/data/t1.nii.gz"}]}
    folder = tmp_path / "reports/jobs/active"
    folder.mkdir(parents=True)
    (folder / "request.json").write_text(json.dumps(payload))
    (folder / "submission.json").write_text(json.dumps({
        "job_id": "77", "stage": "dmri_recon",
        "upstream_receipts": {"dmri_preproc": {"job": "70", "stored_ns": 1}}}))
    current = {"dmri_preproc": {"job": "71", "stored_ns": 2}}
    with patch("calmar.scheduled.subprocess.run", return_value=SimpleNamespace(stdout="77\n")):
        with pytest.raises(RuntimeError, match="older upstream"):
            _attach_running("dmri_recon", payload, tmp_path, current)


def test_reporting_job_reattaches_after_notebook_disconnect(tmp_path):
    from calmar.scheduled import _attach_running
    payload = {"function": "build_report", "args": [], "kwargs": {}}
    folder = tmp_path / "reports/jobs/reporting-active"
    folder.mkdir(parents=True)
    (folder / "request.json").write_text(json.dumps(payload))
    (folder / "submission.json").write_text(json.dumps({
        "job_id": "78", "stage": "reporting", "upstream_receipts": {}}))
    with patch("calmar.scheduled.subprocess.run", return_value=SimpleNamespace(stdout="78\n")):
        job = _attach_running("reporting", payload, tmp_path, {})
    assert job["job"] == "78"
    assert job["upstream_receipts"] == {}


def test_disk_receipt_replaces_stale_process_memory(tmp_path):
    import hashlib
    from calmar.scheduled import _MEMORY_CACHE, _identity_key, _receipt
    payload = {"dataset": str(tmp_path), "config": {},
               "entries": [{"subject": "sub-one", "t1w": "/data/t1.nii.gz"}]}
    key = _identity_key("brain", payload)
    _MEMORY_CACHE[key] = {"stored_ns": 1, "result": {"job": "old"}}
    path = tmp_path / "reports/step-cache" / (hashlib.sha256(str(key).encode()).hexdigest() + ".json")
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({"stored_ns": 2, "result": {"job": "new"}}))
    assert _receipt("brain", payload, tmp_path)["result"]["job"] == "new"


def test_step_summary_keeps_derived_from_prior_warning_visible():
    from calmar.step_summary import step_html
    result = {"stage": "dmri_metrics", "results": [{
        "subject": "sub-one", "seconds": 1, "outputs": [],
        "derived_from_prior": [{"stage": "dmri_preproc", "job": "91"}],
    }]}
    html = step_html(result)
    assert "computed from explicitly retained prior result" in html
    assert "dmri_preproc (job 91)" in html


def test_brain_health_report_link_does_not_change_t1_stage_identity():
    from calmar.scheduled import _identity_key
    base = {"dataset": "/data", "config": {"MODALITY": "t1"},
            "entries": [{"subject": "sub-one", "t1w": "/data/T1w.nii.gz"}]}
    linked = {**base, "entries": [{**base["entries"][0], "brain_health_analysis": {
        "components": ["atrophy"], "_calmar_config": {"BRAIN_HEALTH_OVERWRITE": True}}}]}
    for stage in ("brain", "linda", "registration", "brain_health_anatomy"):
        assert _identity_key(stage, base) == _identity_key(stage, linked)



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


def test_mixed_result_restores_entry_metadata_for_step_viewers(tmp_path):
    from calmar.scheduled import submit_step
    from calmar.study import ENTRY_CONFIG, ENTRY_DATASET, Study
    t1 = tmp_path / 'acute' / 'sub-a_dwi.nii.gz'; t1.parent.mkdir(); t1.write_bytes(b'dwi')
    entry = {'subject': 'sub-a', 'session': 'ses-1', 't1w': str(t1), 'dwi': str(t1),
             ENTRY_DATASET: str(t1.parent),
             ENTRY_CONFIG: {'MODALITY': 't1', 'SEGMENTATION_METHODS': ['linda']}}
    submissions = []
    with patch('calmar.scheduled.subprocess.run', side_effect=_fake_scheduler(tmp_path, submissions)), \
            patch('IPython.display.display'):
        result = submit_step('brain', [entry], Study({}, tmp_path, tmp_path))
    restored = result['request']['entries'][0]
    assert restored[ENTRY_DATASET] == str(t1.parent)
    assert restored[ENTRY_CONFIG]['MODALITY'] == 't1'


def test_primary_cache_key_ignores_additional_cohort_selection():
    from calmar.scheduled import _identity_key
    request = {'dataset': '/data/chronic', 'entries': [{'subject': 'sub-a', 't1w': '/data/a.nii.gz'}],
               'config': {'MODALITY': 't1', 'ADDITIONAL_COHORTS': [{'SUBJECT_FILTER': ['sub-acute-a']}]}}
    changed = {**request, 'config': {**request['config'],
               'ADDITIONAL_COHORTS': [{'SUBJECT_FILTER': ['sub-acute-b']}]}}
    assert _identity_key('brain', request) == _identity_key('brain', changed)


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


def test_direct_dmri_settings_are_scoped_to_direct_dmri_stages():
    from calmar.scheduled import _identity_key, _reusable
    entry = {'subject': 'sub-one', 'session': 'ses-dwi', 't1w': '/data/T1w.nii.gz',
             'dwi': '/data/DWI.nii.gz', 'bval': '/data/DWI.bval',
             'bvec': '/data/DWI.bvec', 'json': '/data/DWI.json'}
    base = {'dataset': '/data', 'entries': [entry],
            'config': {'MODALITY': 't1', 'DMRI_RECON_SPEC': 'ss3t_fod_autotrack'}}
    changed = {**base, 'config': {**base['config'], 'DMRI_RECON_SPEC': 'dsi_studio_autotrack'}}
    assert _identity_key('brain', base) == _identity_key('brain', changed)
    assert _identity_key('dmri_recon', base) != _identity_key('dmri_recon', changed)
    overwrite = {**base, 'config': {**base['config'], 'DMRI_OVERWRITE': True}}
    assert _reusable('brain', overwrite)
    assert not _reusable('dmri_preproc', overwrite)


def test_dmri_report_link_does_not_change_processing_cache_identity():
    from calmar.scheduled import _identity_key
    base = {'dataset': '/data', 'config': {'MODALITY': 't1'},
            'entries': [{'subject': 'sub-one', 'session': 'ses-dwi', 't1w': '/data/T1w.nii.gz',
                         'dwi': '/data/DWI.nii.gz', 'bval': '/data/DWI.bval',
                         'bvec': '/data/DWI.bvec', 'json': '/data/DWI.json'}]}
    linked = {**base, 'entries': [{**base['entries'][0], 'dmri_analysis': {
        'subject': 'sub-one', 'session': 'ses-old', 'dwi': '/data/OLD_DWI.nii.gz'}}]}
    for stage in ('brain', 'linda', 'dmri_preproc', 'dmri_recon', 'dmri_metrics'):
        assert _identity_key(stage, base) == _identity_key(stage, linked)


def test_brain_health_settings_are_scoped_to_the_stage_that_uses_them():
    from calmar.scheduled import _identity_key, _reusable
    entry = {'subject': 'sub-one', 'session': 'ses-one', 't1w': '/data/T1w.nii.gz',
             'flair': '/data/FLAIR.nii.gz', 'anatomical_t1w': '/data/T1w.nii.gz',
             'brain_health_components': ['atrophy', 'wmh']}
    base = {'dataset': '/data', 'entries': [entry],
            'config': {'MODALITY': 't1', 'BRAIN_HEALTH_MASK_SOURCE': 'manual',
                       'BRAIN_HEALTH_SYNTHSEG_MODE': 'robust',
                       'BRAIN_HEALTH_LESION_EXCLUSION_MM': 3.0}}
    margin = {**base, 'config': {**base['config'], 'BRAIN_HEALTH_LESION_EXCLUSION_MM': 5.0}}
    assert _identity_key('brain', base) == _identity_key('brain', margin)
    assert _identity_key('brain_health_anatomy', base) == _identity_key('brain_health_anatomy', margin)
    assert _identity_key('brain_health_wmh', base) == _identity_key('brain_health_wmh', margin)
    assert _identity_key('brain_health_metrics', base) != _identity_key('brain_health_metrics', margin)
    overwrite = {**base, 'config': {**base['config'], 'BRAIN_HEALTH_OVERWRITE': True}}
    assert _reusable('brain', overwrite)
    assert not _reusable('brain_health_metrics', overwrite)


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
