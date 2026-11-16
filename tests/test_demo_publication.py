"""Static publication boundary checks; no GitHub writes or imaging jobs."""
import importlib.util
import json
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'src/python' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


package = load('package_demo_site')
publish = load('publish_demo_site')


def test_jupyter_links_copy_report_and_relative_figure(tmp_path):
    source = tmp_path / 'data/sub-M2001'
    source.mkdir(parents=True)
    (source / 'image.png').write_bytes(b'example image')
    (source / 'report.html').write_text('<img src="image.png">')
    assets = package.Assets(tmp_path, tmp_path / 'public')
    output = assets.rewrite('<a href="/user/researcher/files/data/sub-M2001/report.html">Report</a>')
    assert '/files/' not in output
    assert len(assets.mapping) == 2
    package.check_links(tmp_path / 'public')
    assert not assets.unavailable


def test_widget_javascript_is_preserved(tmp_path):
    assets = package.Assets(tmp_path, tmp_path / 'public')
    javascript = 'return `<a href="${url}">Run</a>`;'
    assert assets.tree({'_esm': javascript}) == {'_esm': javascript}
    assert assets.rewrite(javascript) == javascript


def test_does_not_export_raw_mri_or_other_participants(tmp_path):
    folder = tmp_path / 'data/sub-M2001'
    folder.mkdir(parents=True)
    raw = folder / 'scan.nii.gz'
    raw.write_bytes(b'not for publication')
    other = tmp_path / 'reports/sub-M9999.html'
    other.parent.mkdir()
    other.write_text('other participant')
    assets = package.Assets(tmp_path, tmp_path / 'public')
    with pytest.raises(ValueError):
        assets.add(raw)
    with pytest.raises(ValueError):
        assets.add(other)
    prefixed = other.with_name('group_sub-M9999.png')
    prefixed.write_bytes(b'other participant image')
    with pytest.raises(ValueError, match='unselected participant'):
        assets.add(prefixed)


def test_symlinks_cannot_hide_unselected_participants(tmp_path):
    annex = tmp_path / 'data/.git/annex/example.png'
    annex.parent.mkdir(parents=True)
    annex.write_bytes(b'image')
    source = tmp_path / 'data/sub-M9999/image.png'
    source.parent.mkdir(parents=True)
    source.symlink_to(annex)
    assets = package.Assets(tmp_path, tmp_path / 'public')
    with pytest.raises(ValueError, match='unselected participant'):
        assets.add(source)
    metadata = tmp_path / 'data/participants.tsv'
    metadata.write_text('participant_id\nsub-M9999\n')
    with pytest.raises(ValueError, match='Dataset-wide metadata'):
        assets.add(metadata)


def test_local_widget_volume_urls_are_disabled(tmp_path):
    assets = package.Assets(tmp_path, tmp_path / 'public')
    state = {'volumes': [{'url': '/user/example/files/data/sub-M2001/scan.nii.gz'}]}
    assert assets.tree(state) == {'volumes': [{'url': None}]}
    assert len(assets.unavailable) == 1


def test_workflow_changes_only_add_demo_path_and_build_selection():
    text = (ROOT / publish.WORKFLOW).read_text()
    result = publish.adapt_workflow(text)
    assert publish.adapt_workflow(result) == result
    before, after = yaml.safe_load(text), yaml.safe_load(result)
    assert before['jobs']['deploy'] == after['jobs']['deploy']
    assert before['permissions'] == after['permissions']
    assert before['concurrency'] == after['concurrency']
    assert 'demo/**' in result and 'cp -a demo/. _site/' in result
    assert after['env']['PUBLISH_DEMO'] == '1'
    assert '--notebook demo/lesion-interpretation-demo.ipynb' in result


def test_preview_is_rejected_before_network_access(tmp_path, monkeypatch):
    (tmp_path / 'publication.json').write_text(json.dumps({'state': 'preview'}))
    def no_network(*args, **kwargs):
        raise AssertionError('No network operation should run')
    monkeypatch.setattr(publish, 'run', no_network)
    with pytest.raises(ValueError, match='completed bundle'):
        publish.publish(tmp_path, tmp_path / 'state', '34')
