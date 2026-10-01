from pathlib import Path
import pandas as pd

from calmar.anatomy_labels import label_table, roi_hemisphere
from calmar.timing import step_key, step_title


def test_timing_labels_use_titles_and_current_cell_numbers():
    key = step_key('# CALMAR_CELL_ID: calmar-step-25\nprint(1)')
    assert key == 'calmar-step-25'
    assert step_title(key) == 'LINDA lesion segmentation — single subject (cell 24)'
    assert step_title('CALMAR_CELL_ID: calmar-step-25') == step_title(key)


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
