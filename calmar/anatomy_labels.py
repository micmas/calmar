"""Atlas label metadata for tables; never infer lesion laterality from ROI names."""

from functools import lru_cache
from pathlib import Path
import re
import xml.etree.ElementTree as ET


@lru_cache(maxsize=8)
def aal_labels(atlas_dir):
    root = Path(atlas_dir)
    for relative in ('aal_SPM12/aal/ROI_MNI_V4.xml', 'aal_mirror/AAL.xml'):
        path = root / relative
        if path.is_file():
            return {int(e.findtext('index')): e.findtext('name')
                    for e in ET.parse(path).iter('label')
                    if e.findtext('index') and e.findtext('name')}
    return {}


def roi_hemisphere(region, atlas=''):
    text = str(region).lower()
    tokens = set(re.split(r'[^a-z]+', text))
    left = bool(tokens & {'left', 'l', 'lh'})
    right = bool(tokens & {'right', 'r', 'rh'})
    if left and right:
        return 'Bilateral ROI'
    if left:
        return 'Left'
    if right:
        return 'Right'
    if 'vermis' in tokens:
        return 'Midline'
    if str(atlas) == 'HarvardOxford' and not text.startswith('region_'):
        return 'Bilateral ROI'
    return 'Not specified'


def label_table(df, atlas='', atlas_dir=None):
    result = df.copy()
    if 'region' not in result:
        return result
    atlas_dir = atlas_dir or Path(__file__).resolve().parents[1] / 'atlases'
    mapping = aal_labels(str(atlas_dir)) if atlas == 'AAL' else {}
    def name(value):
        value = value.decode() if isinstance(value, bytes) else str(value)
        match = re.fullmatch(r'Region_(\d+)', value)
        return mapping.get(int(match[1]), value) if match else value
    result['region'] = result.region.map(name)
    result['roi_hemisphere'] = result.region.map(lambda r: roi_hemisphere(r, atlas))
    def lesion_side(row):
        fields = ('left_overlap_voxels', 'right_overlap_voxels', 'midline_overlap_voxels')
        if any(field not in row or row[field] != row[field] for field in fields):
            return 'Not calculated'
        left, right, midline = (row[field] for field in fields)
        if left and right:
            return f'Bilateral (L {int(left)}, R {int(right)})'
        return 'Left' if left else 'Right' if right else 'Midline' if midline else 'None'
    result['lesion_hemisphere'] = result.apply(lesion_side, axis=1) if len(result) else ''
    return result
