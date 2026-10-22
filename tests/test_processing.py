"""Scientific cache and publication contracts, using tiny synthetic fixtures."""
import json
import os
from pathlib import Path
from unittest.mock import patch
import nibabel as nib
import numpy as np
import pytest
from calmar.processing import product, validate_image, manual_inputs, process, paths, warp_product


def image(path, value=1):
    nib.save(nib.Nifti1Image(np.full((3,3,3),value,dtype='uint8'),np.eye(4)),path)


def test_failed_build_cannot_publish_or_overwrite(tmp_path):
    source=tmp_path/'input.nii.gz'; image(source)
    final=tmp_path/'output'
    def fail(path):
        path.mkdir(); image(path/'mask.nii.gz'); raise RuntimeError('tool failed')
    with pytest.raises(RuntimeError,match='tool failed'):
        product(final,[source],{},fail,lambda d:[d/'mask.nii.gz'],'test')
    assert not final.exists()
    assert not list(tmp_path.glob('output.attempt.*'))


def test_changed_input_invalidates_cache_without_modifying_result(tmp_path):
    source=tmp_path/'input.nii.gz'; image(source)
    final=tmp_path/'output'
    def build(path): path.mkdir(); image(path/'mask.nii.gz')
    with patch('calmar.processing.publish',side_effect=lambda a,b,c:os.rename(a,b)):
        assert product(final,[source],{},build,lambda d:[d/'mask.nii.gz'],'test')['status']=='computed'
    before=(final/'mask.nii.gz').read_bytes()
    image(source,0)
    with pytest.raises(RuntimeError,match='Stale output preserved'):
        product(final,[source],{},build,lambda d:[d/'mask.nii.gz'],'test')
    assert (final/'mask.nii.gz').read_bytes()==before


def test_legacy_cache_is_never_labelled_new_execution(tmp_path):
    source=tmp_path/'input.nii.gz'; image(source)
    final=tmp_path/'output'; final.mkdir(); image(final/'mask.nii.gz')
    result=product(final,[source],{},lambda p:pytest.fail('must not rebuild'),lambda d:[d/'mask.nii.gz'],'test')
    assert result['status']=='legacy-cache'
    assert not (final/'calmar-cache.json').exists()


@pytest.mark.parametrize('output_id', ['brain', 'linda'])
def test_legacy_brain_and_linda_outputs_are_stale(tmp_path, output_id):
    # Made before run records, so possibly HD-BET-only / unseeded multi-threaded.
    source=tmp_path/'input.nii.gz'; image(source)
    final=tmp_path/'output'; final.mkdir(); image(final/'mask.nii.gz')
    with pytest.raises(RuntimeError, match='no run record'):
        product(final,[source],{},lambda p:pytest.fail('must not rebuild'),lambda d:[d/'mask.nii.gz'],output_id)
    assert (final/'mask.nii.gz').exists()


def test_cache_ignores_unrelated_code_and_module_environment_but_checks_parameters(tmp_path):
    source = tmp_path/'input.nii.gz'; image(source)
    final = tmp_path/'output'
    def build(path): path.mkdir(); image(path/'mask.nii.gz')
    options = {'module': 'test/1.0', 'threshold': .5}
    with patch('calmar.processing.publish', side_effect=lambda a,b,c:a.rename(b)):
        product(final, [source], options, build, lambda d:[d/'mask.nii.gz'], 'test')
    record = final/'calmar-cache.json'; original = json.loads(record.read_text())
    original['identity'].update(implementation='old UI revision', qc_implementation='old logging',
                                loaded_modules='fsl/other:linda/other', script_sha256='old CPU directives')
    record.write_text(json.dumps(original))
    before = record.read_bytes()
    no_build = lambda p: pytest.fail('must not rerun inference')
    assert product(final, [source], options, no_build, lambda d:[d/'mask.nii.gz'], 'test')['status'] == 'cached'
    assert record.read_bytes() == before  # Retain the original run record.
    with pytest.raises(RuntimeError, match='Stale output'):
        product(final, [source], {**options, 'threshold': .6}, no_build, lambda d:[d/'mask.nii.gz'], 'test')
    with patch.dict('calmar.processing.ALGORITHM_VERSIONS', {'test': 2}):
        with pytest.raises(RuntimeError, match='Stale output'):
            product(final, [source], options, no_build, lambda d:[d/'mask.nii.gz'], 'test')


def test_processing_requires_scheduler():
    with patch.dict(os.environ,{},clear=True),pytest.raises(RuntimeError,match='sbatch'):
        process('brain',{})


def test_grid_and_binary_validation(tmp_path):
    a=tmp_path/'a.nii.gz'; image(a,2)
    with pytest.raises(ValueError,match='Nonbinary'):
        validate_image(a,binary=True)
    b=tmp_path/'b.nii.gz'; nib.save(nib.Nifti1Image(np.ones((4,3,3)),np.eye(4)),b)
    with pytest.raises(ValueError,match='Grid mismatch'):
        validate_image(a,b)


def test_configured_directories_and_optional_manual_mask(tmp_path):
    request={'dataset':str(tmp_path),'config':{'DERIVATIVES_SUBDIR':'derivatives/custom'}}
    entry={'subject':'sub-one','session':None,'t1w':str(tmp_path/'T1.nii.gz')}
    assert paths(request,entry)['linda']==tmp_path/'derivatives/custom/sub-one/anat'
    assert manual_inputs(request,entry)==(None,None,None)


def test_isles_expert_mask_is_discovered_on_the_native_dwi_grid(tmp_path):
    sub, ses = 'sub-strokecase0001', 'ses-0001'
    dwi = tmp_path/sub/ses/'dwi'/f'{sub}_{ses}_dwi.nii.gz'
    mask = tmp_path/'derivatives'/sub/ses/f'{sub}_{ses}_msk.nii.gz'
    dwi.parent.mkdir(parents=True)
    mask.parent.mkdir(parents=True)
    image(dwi)
    image(mask)
    request = {'dataset': str(tmp_path), 'config': {'MODALITY': 'dwi'}}
    entry = {'subject': sub, 'session': ses, 't1w': str(dwi), 'dwi': str(dwi)}
    assert manual_inputs(request, entry) == (mask, None, 't1')


def test_isles_mask_is_not_guessed_when_the_dwi_has_no_session(tmp_path):
    sub, ses = 'sub-strokecase0001', 'ses-0001'
    dwi = tmp_path/sub/'dwi'/f'{sub}_dwi.nii.gz'
    mask = tmp_path/'derivatives'/sub/ses/f'{sub}_{ses}_msk.nii.gz'
    dwi.parent.mkdir(parents=True)
    mask.parent.mkdir(parents=True)
    image(dwi)
    image(mask)
    request = {'dataset': str(tmp_path), 'config': {'MODALITY': 'dwi'}}
    entry = {'subject': sub, 'session': None, 't1w': str(dwi), 'dwi': str(dwi)}
    assert manual_inputs(request, entry) == (None, None, None)


def test_disabled_segmentation_never_calls_tool(tmp_path,monkeypatch):
    monkeypatch.setenv('SLURM_JOB_ID','fixture')
    request={'dataset':str(tmp_path),'config':{'RUN_SEGMENTATION':False},
             'entries':[{'subject':'sub-one','t1w':'not-downloaded.nii.gz'}]}
    with patch('calmar.processing.run',side_effect=AssertionError('must not run')):
        for stage in ('brain','linda','synthstroke'):
            assert process(stage,request)[0]['outputs'][0]['status']=='skipped'


def test_changed_output_is_not_silently_reused(tmp_path):
    source=tmp_path/'input.nii.gz'; image(source)
    final=tmp_path/'output'
    def build(path): path.mkdir(); image(path/'mask.nii.gz')
    with patch('calmar.processing.publish',side_effect=lambda a,b,c:a.rename(b)):
        product(final,[source],{},build,lambda d:[d/'mask.nii.gz'],'test')
    image(final/'mask.nii.gz',0)
    with pytest.raises(RuntimeError,match='Stale output'):
        product(final,[source],{},build,lambda d:[d/'mask.nii.gz'],'test')


def test_failed_overwrite_restores_old_output_and_provenance(tmp_path):
    source=tmp_path/'input.nii.gz'; image(source)
    final=tmp_path/'output'; final.mkdir(); image(final/'mask.nii.gz')
    sidecar=Path(str(final)+'.prov.json'); sidecar.write_text('original provenance')
    before=(final/'mask.nii.gz').read_bytes()
    def build(path): path.mkdir(); image(path/'mask.nii.gz',0)
    with patch('calmar.processing.publish',side_effect=RuntimeError('publication failed')):
        with pytest.raises(RuntimeError,match='publication failed'):
            product(final,[source],{},build,lambda d:[d/'mask.nii.gz'],'test',overwrite=True)
    assert (final/'mask.nii.gz').read_bytes()==before
    assert sidecar.read_text()=='original provenance'


def test_mni_warp_failure_leaves_no_final_mask(tmp_path):
    for name in ('native.nii.gz','Subject_in_MNI.nii.gz','Reg3_sub_to_template_warp.nii.gz'):
        image(tmp_path/name)
    (tmp_path/'Reg3_sub_to_template_affine.mat').write_text('fixture')
    final=tmp_path/'mask_mni.nii.gz'
    def fail(linda,native,output,**kwargs):
        image(output)
        return 1
    with patch('calmar.processing.q.warp_native_mask_to_mni',side_effect=fail):
        with pytest.raises(RuntimeError,match='warp failed'):
            warp_product(tmp_path,tmp_path/'native.nii.gz',final,'manual_mni')
    assert not final.exists()


def test_bcb_retains_optional_tractotron_tables(tmp_path, monkeypatch):
    monkeypatch.setenv('SLURM_JOB_ID', 'fixture')
    entry = {'subject': 'sub-fixture', 't1w': 'unused.nii.gz'}
    request = {'dataset': str(tmp_path), 'entries': [entry], 'config': {'BCB_MASKS': 'linda', 'BCB_RUN_TRACTOTRON': True}}
    directories = paths(request, entry)
    directories['linda'].mkdir(parents=True)
    mask = directories['linda']/'Lesion_in_MNI.nii.gz'; image(mask)
    before = mask.read_bytes()
    def fake_run(command, log, **kwargs):
        if command[0] == 'bash':
            prepared = Path(command[3]); image(prepared)
            Path(str(prepared)+'.grid.json').write_text('{}')
            return
        output = Path(command[command.index('-o')+1])
        if command[0] == 'run_disco.sh':
            image(output/'map.nii.gz')
        else:
            assert command[0] == 'tractotron_cli.sh'
            (output/'probabilities.csv').write_text('tract,probability\nArcuate,0.5\n')
    with patch('calmar.processing.run', side_effect=fake_run), \
            patch('calmar.processing.shutil.which', return_value='/fixture/tractotron_cli.sh'), \
            patch('calmar.processing.publish', side_effect=lambda a,b,c:a.rename(b)):
        results = process('bcb', request)
    assert len(results[0]['outputs']) == 2
    assert (directories['bcbtoolkit']/'Tractotron_probs/probabilities.csv').is_file()
    assert mask.read_bytes() == before


def test_bcb_sigill_never_publishes_or_uses_undefined_fallback(tmp_path, monkeypatch):
    import subprocess
    monkeypatch.setenv('SLURM_JOB_ID', 'fixture')
    entry = {'subject': 'sub-fixture', 't1w': 'unused.nii.gz'}
    request = {'dataset': str(tmp_path), 'entries': [entry], 'config': {'BCB_MASKS': 'linda'}}
    directories = paths(request, entry)
    directories['linda'].mkdir(parents=True); image(directories['linda']/'Lesion_in_MNI.nii.gz')
    with patch('calmar.processing.run', side_effect=subprocess.CalledProcessError(132, 'run_disco.sh')), \
            pytest.raises(RuntimeError, match='No validated Python fallback'):
        process('bcb', request)
    assert not (directories['bcbtoolkit']/'Disconnectome_linda.nii.gz').exists()


def test_build_commands_and_tool_paths_are_recorded_and_reused(tmp_path):
    from calmar.processing import run
    source=tmp_path/'input.nii.gz'; image(source)
    final=tmp_path/'output'
    def build(path):
        path.mkdir(); run(['echo', 'hello', path], path/'tool.log'); image(path/'mask.nii.gz')
    with patch('calmar.processing.publish',side_effect=lambda a,b,c:a.rename(b)):
        made = product(final,[source],{},build,lambda d:[d/'mask.nii.gz'],'test')
    assert made['commands'] == [f'echo hello {final}']   # staging path replaced by the final path
    assert made['tools']['echo'].endswith('echo')
    reused = product(final,[source],{},lambda p: pytest.fail('rebuilt'),lambda d:[d/'mask.nii.gz'],'test')
    assert reused['status'] == 'cached' and reused['commands'] == made['commands']


def test_transform_validation_reads_content(tmp_path):
    import SimpleITK as sitk
    from calmar.processing import validate_transform
    good = tmp_path/'Reg3_sub_to_template_affine.mat'
    sitk.WriteTransform(sitk.AffineTransform(3), str(good))
    assert validate_transform(good) == good
    bad = tmp_path/'broken_affine.mat'; bad.write_bytes(b'not a transform')
    with pytest.raises(ValueError, match='Unreadable'):
        validate_transform(bad)
    warp = tmp_path/'Reg3_sub_to_template_warp.nii.gz'
    nib.save(nib.Nifti1Image(np.full((2, 2, 2, 1, 3), np.nan, dtype='float32'), np.eye(4)), warp)
    with pytest.raises(ValueError, match='Invalid warp'):
        validate_transform(warp)


def test_legacy_disconnectome_is_flagged_as_possibly_old_method(tmp_path, monkeypatch):
    monkeypatch.setenv('SLURM_JOB_ID', 'fixture')
    entry = {'subject': 'sub-fixture', 't1w': 'unused.nii.gz'}
    request = {'dataset': str(tmp_path), 'entries': [entry], 'config': {'BCB_MASKS': 'linda'}}
    d = paths(request, entry)
    d['linda'].mkdir(parents=True); image(d['linda']/'Lesion_in_MNI.nii.gz')
    d['bcbtoolkit'].mkdir(parents=True); image(d['bcbtoolkit']/'Disconnectome_linda.nii.gz')  # no run record
    with patch('calmar.processing.run', side_effect=AssertionError('must not recompute')):
        out = process('bcb', request)[0]['outputs'][0]
    assert out['status'] == 'legacy-cache' and 'BCB grid correction' in out['reason']
