"""Test the public-asset and saved-state boundaries, without imaging analysis."""
import sys
from pathlib import Path
import pytest
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src/python'))
from notebook_first import SavedWidgets, add_demo_guide, explorer_source
import json


def renderer(tmp_path, state=None):
    return SavedWidgets(tmp_path, tmp_path, state or {}, None, [])


def test_demo_guide_links_to_brain_health_without_duplicating_navigation():
    page = BeautifulSoup('<header><p class="lead"></p></header>', 'html.parser')
    add_demo_guide(page, page.header)
    add_demo_guide(page, page.header)
    assert len(page.select('.notebook-links')) == 1
    link = page.select_one('.notebook-links a[href="#optional-background-brain-health"]')
    assert link.string == 'See brain-health results'


@pytest.mark.parametrize('path', [
    'data/ds004884/derivatives/linda/sub-M9999/ses-1076/anat/a.nii.gz',
    'data/ds004884/sub-M2001/ses-1076/../../private.nii.gz',
    'reports/private.nii.gz',
    'data/PRIVATE/sub-M2001/ses-1076/a.nii.gz',
])
def test_public_scope(tmp_path, path):
    with pytest.raises(ValueError):
        renderer(tmp_path).volume({'path': {'url': '/user/me/files/neurodesktop-storage/calmar/' + path}})


def test_no_external_download(tmp_path):
    with pytest.raises(ValueError):
        renderer(tmp_path).volume({'path': {'url': 'https://example.com/private.nii.gz'}})


def test_unsaved_preview_is_not_published(tmp_path):
    r = renderer(tmp_path)
    assert r.volume({'path': {'url': '/user/me/files/neurodesktop-storage/calmar/qc_edits/_cleanup_preview.nii.gz'}}) is None
    assert r.omitted == ['qc_edits/_cleanup_preview.nii.gz']


def test_symlink_cannot_escape(tmp_path):
    project = tmp_path / 'project'
    source = project / 'data/ds004884/sub-M2001/ses-1076/anat/a.nii.gz'
    source.parent.mkdir(parents=True)
    outside = tmp_path / 'private.nii.gz'
    outside.write_bytes(b'private')
    source.symlink_to(outside)
    with pytest.raises(ValueError):
        renderer(project).volume({'path': {'url': '/files/neurodesktop-storage/calmar/data/ds004884/sub-M2001/ses-1076/anat/a.nii.gz'}})


def test_saved_controls_are_not_dead_buttons(tmp_path):
    r = renderer(tmp_path, {'button': {'state': {'_model_name': 'ButtonModel', 'description': 'Save QC'}}})
    markup = r.render('button')
    assert '<button' not in markup and 'requires Neurodesk' in markup


def test_saved_tabs_keep_each_panel_and_keyboard_relationships(tmp_path):
    state = {'tabs': {'state': {'_model_name': 'TabModel', 'titles': ['First', 'Second'], 'children': ['IPY_MODEL_a', 'IPY_MODEL_b']}},
             'a': {'state': {'_model_name': 'TextModel', 'value': 'one'}},
             'b': {'state': {'_model_name': 'TextModel', 'value': 'two'}}}
    markup = renderer(tmp_path, state).render('tabs')
    assert 'one' in markup and 'two' in markup and 'aria-controls="saved-tabs-1-1"' in markup


def test_report_identity_comes_from_own_widget_and_ambiguity_fails(tmp_path):
    r = renderer(tmp_path, {'root': {'state': {'children': ['IPY_MODEL_link']}},
                           'link': {'state': {'value': '<a href="interpretation_sub-M2004_ses-524.html">Report</a>'}}})
    r.cases = [{'id':'sub-M2001'}, {'id':'sub-M2004'}]
    assert r.report_subject('root', []) == 'sub-M2004'
    with pytest.raises(ValueError, match='Ambiguous'):
        r.report_subject('root', [{'text':'interpretation_sub-M2001_ses-1076.html'}])


def test_rebuild_preserves_secondary_explorer(tmp_path):
    demo = tmp_path / 'demo'
    demo.mkdir()
    (demo / 'publication.json').write_text(json.dumps({'architecture':'notebook-first'}))
    (demo / 'index.html').write_text('This is the notebook')
    expected = demo / 'explorer.html'
    expected.write_text('<div id="explore"></div><script src="reader.js"></script>')
    assert explorer_source(tmp_path) == expected
    expected.unlink()
    with pytest.raises(ValueError):
        explorer_source(tmp_path)


def test_saved_layer_opacity_and_plane_are_retained(tmp_path):
    state = {'view': {'state': {'volumes':['IPY_MODEL_bg','IPY_MODEL_mask']}},
             'bg': {'state': {'name':'Subject_in_MNI.nii.gz'}},
             'mask': {'state': {'name':'Lesion_in_MNI.nii.gz'}},
             'controls': {'state': {'_anywidget_id':'calmar.layer_controls.LayerControls', 'viewer_id':'view',
                                    'plane':1, 'layers':[{'model_id':'mask','opacity':.35,'role':'mask','color':'#ff0000'}],
                                    'roles':[{'key':'mask','label':'LINDA'}]}}}
    r = renderer(tmp_path, state)
    r.volume = lambda m: {'name':m['name'],'source':'data/ds004884/derivatives/linda/sub-M2001/ses-1076/anat/'+m['name'],'url':'test.nii.gz'}
    r.viewer('view')
    assert r.viewers['view']['layers'][1]['saved_opacity'] == .35
    assert r.viewers['view']['layers'][1]['label'] == 'LINDA'
    assert r.viewers['view']['plane'] == 1
    assert r.viewers['view']['space'] == 'MNI template space'
