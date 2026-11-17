"""Publication allowlist and failure boundaries for the browser-native reader."""
import importlib.util
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('demo_reader', ROOT / 'src/python/demo_reader.py')
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)


@pytest.mark.parametrize('relative', [
    'data/ds004884/sub-M2001/ses-1076/anat/T1w.nii.gz',
    'data/ds004884/derivatives/linda/sub-M9999/ses-1076/anat/Subject_in_MNI.nii.gz',
    'data/ds004884/derivatives/linda/sub-M2001/ses-1076/anat/Prediction3_native.nii.gz',
    'data/ds004884/derivatives/linda/sub-M2001/ses-1076/anat/../../../../../../private.nii.gz',
])
def test_rejects_everything_outside_exact_registered_derivatives(tmp_path, relative):
    with pytest.raises(ValueError, match='approved demo derivative'):
        reader.copy_volume(tmp_path, tmp_path / 'site', relative)


def test_symlink_cannot_leave_project(tmp_path):
    project = tmp_path / 'project'
    relative = sorted(reader.allowed_volumes())[0]
    source = project / relative
    source.parent.mkdir(parents=True)
    outside = tmp_path / 'private.nii.gz'
    outside.write_bytes(b'private')
    source.symlink_to(outside)
    with pytest.raises(ValueError):
        reader.copy_volume(project, tmp_path / 'site', relative)


def test_missing_expected_volume_is_an_error(tmp_path):
    with pytest.raises(ValueError, match='Missing or oversized'):
        reader.copy_volume(tmp_path, tmp_path / 'site', sorted(reader.allowed_volumes())[0])


def test_notebook_has_no_nonfunctional_widget_bootstrap():
    page = '<html><main class="nb-main"><section class="cell"><pre>log</pre><div class="widget">widget</div></section></main><script type="application/vnd.jupyter.widget-state+json">{}</script></html>'
    rendered = reader.readable_notebook(page)
    assert 'details class="saved-cell"' in rendered
    assert 'application/vnd.jupyter.widget-state' not in rendered
    assert 'index.html#explore' in rendered
    assert '<pre>log</pre>' in rendered
