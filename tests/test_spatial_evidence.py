import json
import numpy as np
import nibabel as nib
import pytest
from calmar.spatial_evidence import (build, lesion_measurements, interpretation_context,
                                     render_appendix, DEFAULT_KB)
from calmar.kb_paths import load_kb_modules


def fixture_atlas(tmp_path, name, data):
    engine, = load_kb_modules(DEFAULT_KB, 'spatial_harmonisation')
    image = nib.Nifti1Image(data.astype('int16'), np.eye(4))
    image.header.set_xyzt_units('mm')
    image.set_qform(np.eye(4), 1)
    image.set_sform(np.eye(4), 1)
    nib.save(image, tmp_path / (name + '.nii.gz'))
    spec = dict(atlas_id=name, version='synthetic-v1', space='synthetic:shared-RAS',
                template_reference='test only', source='generated', licence='CC0',
                representation='deterministic_labels', units='mm', world_axes='RAS+',
                image=name+'.nii.gz', labels={str(int(i)):f'ROI {i}' for i in np.unique(data) if i})
    path = tmp_path / (name + '.json')
    path.write_text(json.dumps(spec))
    return path, engine.load_atlas(path)


def test_same_broad_damage_does_not_imply_same_child_damage(tmp_path):
    _, broad = fixture_atlas(tmp_path, 'broad', np.ones((5,2,2)))
    _, fine = fixture_atlas(tmp_path, 'fine', np.broadcast_to(np.arange(1,6)[:,None,None],(5,2,2)))
    masks = []
    for index in (0,1):
        mask = np.zeros((5,2,2)); mask[index] = 1; masks.append(mask)
    coarse = [lesion_measurements(m,np.eye(4),broad.metadata['space'],broad) for m in masks]
    assert coarse[0]['regions'][0]['roi_damage_fraction'] == coarse[1]['regions'][0]['roi_damage_fraction'] == .2
    detailed = [lesion_measurements(m,np.eye(4),fine.metadata['space'],fine) for m in masks]
    assert detailed[0]['regions'][0]['roi_damage_fraction'] == 1
    assert detailed[1]['regions'][0]['roi_damage_fraction'] == 0


@pytest.mark.parametrize('kind', ['normative_disconnection','participant_diffusion','unspecified'])
def test_white_matter_methods_are_not_interchangeable(kind):
    context = interpretation_context(dict(tissue_class='white_matter',measurement_kind=kind))
    assert context['comparison_status'] == 'not_established'
    assert not context['clinical_inference_permitted']


def test_appendix_retains_one_finding_and_escapes_text(tmp_path):
    source, atlas = fixture_atlas(tmp_path, 'source', np.ones((5,2,2)))
    target, _ = fixture_atlas(tmp_path, 'target', np.broadcast_to(np.arange(1,6)[:,None,None],(5,2,2)))
    record = dict(evidence_id='example',citation='<script>bad</script>',source_location='Table 2',
                  kind='atlas_roi',atlas=atlas.identity(),roi_id=1,
                  tissue_class='white_matter',measurement_kind='normative_disconnection')
    records = tmp_path/'records.json'; records.write_text(json.dumps([record]))
    data = build(source,target,records)
    assert not data['approved']
    findings = data['evidence']['findings']
    assert len(findings) == 1 and len(findings[0]['spatial_candidates']) == 5
    assert findings[0]['original'] == record
    html = render_appendix(data)
    assert '<script>' not in html and '&lt;script&gt;' in html
    assert 'normative_disconnection' in html


@pytest.mark.parametrize('problem', ['space','affine','probability','empty'])
def test_invalid_lesions_are_rejected(tmp_path, problem):
    _, atlas = fixture_atlas(tmp_path, 'atlas', np.ones((2,2,2)))
    mask = np.ones((2,2,2)); affine = np.eye(4); space = atlas.metadata['space']
    if problem == 'space': space = 'other'
    if problem == 'affine': affine[0,3] = 1
    if problem == 'probability': mask[:] = .5
    if problem == 'empty': mask[:] = 0
    with pytest.raises(ValueError): lesion_measurements(mask,affine,space,atlas)


def test_processed_mask_manifest_build_and_missing_qc(tmp_path):
    source, _ = fixture_atlas(tmp_path, 'source', np.ones((2,2,2)))
    records = tmp_path/'records.json'; records.write_text('[]')
    spec = dict(image='source.nii.gz',space='synthetic:shared-RAS',world_axes='RAS+',
                provenance='synthetic test only',qc_status='synthetic fixture')
    lesion = tmp_path/'lesion.json'; lesion.write_text(json.dumps(spec))
    data = build(source,source,records,lesion)
    assert data['lesion']['source_atlas']['regions'][0]['roi_damage_fraction'] == 1
    assert len(data['lesion']['provenance']['image_sha256']) == 64
    assert 'synthetic fixture' in render_appendix(data)
    del spec['qc_status']; lesion.write_text(json.dumps(spec))
    with pytest.raises(ValueError,match='qc_status'): build(source,source,records,lesion)
