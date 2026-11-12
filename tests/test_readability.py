import re
import subprocess
from pathlib import Path

import pandas as pd

from calmar.anatomy_labels import label_table, roi_hemisphere
from calmar.methods import TOOLS
from calmar.timing import step_key, step_title
from calmar.guided import source_cell


def test_citation_resources_cover_all_imaging_routes_and_collapsible_datasets():
    import json
    notebook = json.loads((Path(__file__).resolve().parents[1]/'lesion-interpretation-pipeline.ipynb').read_text())
    source = ''.join(next(c for c in notebook['cells'] if c['id'] == 'calmar-citations')['source'])
    module_pins = set(re.findall(
        r'\b[a-z][a-z0-9_-]*/[0-9][A-Za-z0-9.]*', ' '.join(TOOLS.values())))
    for required in (*module_pins, '10.1038/s43856-021-00062-8',
                     'github.com/farialab/OpenADS',
                     '10.1038/s41592-021-01185-5',
                     '10.3389/fninf.2014.00008',
                     '10.1073/pnas.2216399120', '10.1016/j.scib.2024.01.034',
                     '10.1038/s41598-026-73385-y',
                     '10.18112/openneuro.ds004884.v1.0.2',
                     '10.5281/zenodo.7153326', '10.1038/s41597-022-01875-5'):
        assert required in source
    assert source.count('<details') == source.count('</details>')
    dataset_heading = source.index('#### Datasets')
    blocks = re.findall(r'<details\b.*?</details>', source[dataset_heading:], re.DOTALL)
    dataset = next(block for block in blocks
                   if '10.18112/openneuro.ds004884.v1.0.2' in block
                   and '10.5281/zenodo.7153326' in block)
    assert '<summary' in dataset and 'ARC' in dataset and 'ISLES 2022' in dataset
    recon_script = (Path(__file__).resolve().parents[1]/'src/analysis_46_dmri_recon.sh').read_text()
    dipy_pin = re.search(r'^export CALMAR_DIPY_VERSION=([0-9.]+)$',
                         recon_script, re.MULTILINE).group(1)
    assert f'`dipy=={dipy_pin}`' in source
    assert f'Python package {dipy_pin})' in TOOLS['dmri_recon']
    requirements = [line.split('#', 1)[0].strip() for line in
                    (Path(__file__).resolve().parents[1]/'requirements.txt').read_text().splitlines()]
    assert f'dipy=={dipy_pin}' in requirements


def test_citation_cell_and_update_script_use_latest_kb():
    import json
    root = Path(__file__).resolve().parents[1]
    notebook = json.loads((root/'lesion-interpretation-pipeline.ipynb').read_text())
    source = ''.join(next(c for c in notebook['cells'] if c['id'] == 'calmar-citations')['source'])
    script = (root/'src/analysis_51_update_kb.sh').read_text()
    assert 'latest available `origin/main`' in source
    assert 'latest version was not verified' in source
    assert 'CALMAR_KB_UPDATE=latest' in script
    assert 'update_kb_to_latest(root, reason)' in script
    assert 'EXPECTED_COMMIT=' not in script


def test_timing_labels_use_titles_and_current_cell_numbers():
    key = step_key('# CALMAR_CELL_ID: calmar-step-25\nprint(1)')
    assert key == 'calmar-step-25'
    import json
    cells = json.loads((Path(__file__).resolve().parents[1]/'lesion-interpretation-pipeline.ipynb').read_text())['cells']
    position = next(i for i, c in enumerate(cells, 1) if c['id'] == 'calmar-step-25')   # moves as cells are added
    assert step_title(key) == f'LINDA lesion segmentation — single subject (cell {position})'
    assert step_title('CALMAR_CELL_ID: calmar-step-25') == step_title(key)
    source = ''.join(source_cell(25)['source'])
    assert 'CALMAR_CELL_ID:' not in source
    assert step_key(source) == key


def test_hemispheres_are_atlas_metadata_not_guessed_lesion_side(tmp_path):
    for label, expected in [('Left Insula', 'Left'), ('Precentral_R', 'Right'),
                            ('L G_and_S_frontomargin', 'Left'),
                            ('7Networks_RH_Vis_1', 'Right'), ('Vermis_1_2', 'Midline'),
                            ('Tract_1', 'Not specified')]:
        assert roi_hemisphere(label) == expected
    assert roi_hemisphere('Frontal Pole', 'HarvardOxford') == 'Bilateral ROI'
    path = tmp_path / 'aal_mirror' / 'AAL.xml'
    path.parent.mkdir()
    path.write_text('<atlas><label><index>2001</index><name>Precentral_L</name></label></atlas>')
    df = pd.DataFrame([dict(region='Region_2001', overlap_voxels=17)])
    labelled = label_table(df, 'AAL', tmp_path)
    assert labelled.region.iloc[0] == 'Precentral_L'
    assert labelled.roi_hemisphere.iloc[0] == 'Left'
    assert labelled.overlap_voxels.iloc[0] == 17
    assert df.region.iloc[0] == 'Region_2001'
