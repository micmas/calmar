from pathlib import Path
from unittest.mock import patch
import nibabel as nib
import numpy as np
import pytest
from calmar.qc_operation import execute
from calmar.scheduled import encode,decode,scheduled_operation


def test_qc_failure_preserves_original_files_and_ratings(tmp_path,monkeypatch):
    monkeypatch.setenv('SLURM_JOB_ID','fixture')
    final=tmp_path/'brain';final.mkdir()
    (final/'ratings.json').write_text('existing ratings')
    def fail(t1w_path,out_dir):
        (out_dir/'ratings.json').write_text('changed staging only')
        return {'returncode':1}
    with patch('calmar.qc.run_hd_bet',new=fail),pytest.raises(RuntimeError,match='failed'):
        execute({'function':'run_hd_bet','args':encode([tmp_path/'T1.nii.gz',final]),'kwargs':{}})
    assert (final/'ratings.json').read_text()=='existing ratings'
    assert not list(tmp_path.glob('brain.attempt.*'))


def test_qc_success_publishes_validated_copy_and_preserves_backup(tmp_path,monkeypatch):
    monkeypatch.setenv('SLURM_JOB_ID','fixture')
    final=tmp_path/'brain';final.mkdir()
    (final/'ratings.json').write_text('existing ratings')
    def success(t1w_path,out_dir):
        path=out_dir/'mask.nii.gz'
        nib.save(nib.Nifti1Image(np.ones((3,3,3),dtype='uint8'),np.eye(4)),path)
        return {'returncode':0,'mask':path}
    with patch('calmar.qc.run_hd_bet',new=success),patch('calmar.qc_operation.publish',side_effect=lambda a,b,c:a.rename(b)):
        result=execute({'function':'run_hd_bet','args':encode([tmp_path/'T1.nii.gz',final]),'kwargs':{}})
    assert result['mask']==final/'mask.nii.gz'
    assert (final/'ratings.json').read_text()=='existing ratings'
    assert (tmp_path/'brain.previous.fixture'/'ratings.json').read_text()=='existing ratings'


def test_interactive_processing_routes_to_scheduler(monkeypatch):
    monkeypatch.delenv('SLURM_JOB_ID',raising=False)
    @scheduled_operation
    def operation(path): pytest.fail('must not process interactively')
    with patch('calmar.scheduled.run_step_sync',return_value={'value':encode(Path('/output'))}) as run:
        assert operation(Path('/input'))==Path('/output')
    assert run.call_args.args[0]=='qc_operation'


def test_relative_string_and_symlink_writes_cannot_escape_staging(tmp_path,monkeypatch):
    monkeypatch.setenv('SLURM_JOB_ID','fixture')
    monkeypatch.chdir(tmp_path)
    final=tmp_path/'brain'; final.mkdir()
    original=tmp_path/'original.txt'; original.write_text('preserved')
    (final/'linked.txt').symlink_to(original)
    def fail(t1w_path,out_dir):
        assert Path(out_dir) != final
        (Path(out_dir)/'linked.txt').write_text('staged change')
        raise RuntimeError('repair interrupted')
    with patch('calmar.qc.run_hd_bet',new=fail),pytest.raises(RuntimeError,match='interrupted'):
        execute({'function':'run_hd_bet','args':['T1.nii.gz','brain'],'kwargs':{}})
    assert original.read_text()=='preserved'
    assert (final/'linked.txt').is_symlink()


def test_implicit_nested_work_directory_is_staged_and_failure_preserves_it(tmp_path, monkeypatch):
    monkeypatch.setenv('SLURM_JOB_ID', 'fixture')
    final = tmp_path/'linda'; final.mkdir()
    work = tmp_path/'_hdbet_work'; work.mkdir()
    (work/'ratings.json').write_text('original')
    def nested(t1w_path, linda_out_dir, *, work_dir=None):
        assert Path(work_dir) != work
        (Path(work_dir)/'ratings.json').write_text('changed')
        raise RuntimeError('nested repair failed')
    with patch('calmar.qc.hdbet_then_linda', new=nested), pytest.raises(RuntimeError, match='nested repair'):
        execute({'function': 'hdbet_then_linda', 'args': encode([tmp_path/'T1.nii.gz', final]), 'kwargs': {}})
    assert (work/'ratings.json').read_text() == 'original'
