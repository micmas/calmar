"""Human-readable notebook step names, retaining stable keys for reruns."""

import re
from .execution import _notebook_cells


TITLES = {
    4: 'Setup imports', 5: 'Check software', 7: 'Certificate setup',
    8: 'Load software modules', 10: 'Enable step timing', 12: 'Configuration',
    13: 'Confirm inputs', 15: 'Load atlases', 17: 'Prepare dataset',
    19: 'Discover subjects', 23: 'HD-BET brain extraction — single subject',
    25: 'LINDA lesion segmentation — single subject',
    27: 'SynthStroke lesion segmentation — single subject',
    29: 'Inspect segmentation stages', 30: 'Compare with manual lesion mask',
    32: 'BCBToolkit disconnectome — single subject',
    34: 'DeepDisco disconnectome — single subject',
    35: 'Compare disconnectomes and lesion',
    39: 'Continue to batch', 42: 'HD-BET and LINDA — batch',
    44: 'SynthStroke — batch', 46: 'Warp SynthStroke to MNI',
    48: 'Warp manual masks to MNI', 51: 'Quality control',
    53: 'Repair brain extraction', 55: 'Manual mask editing',
    56: 'Inspect manual edits', 57: 'Apply mask edits', 58: 'Refresh QC',
    60: 'Reset QC', 63: 'BCBToolkit disconnectomes — batch',
    65: 'DeepDisco disconnectomes — batch', 67: 'Group lesion overlap',
    69: 'Calculate atlas overlap', 71: 'Explore atlas results',
    72: 'Network summaries', 74: 'Preview atlas tables', 75: 'Export atlas results',
    77: 'Prepare interpretation', 79: 'Choose report inputs',
    81: 'Generate participant report', 85: 'Functional decoding', 87: 'Available outputs',
}


def step_key(source):
    marker = re.search(r'^# CALMAR_CELL_ID: ([\w-]+)', source, re.M)
    if marker:
        return marker.group(1)
    return next((s.strip().lstrip('#').strip()[:80] for s in source.splitlines()
                 if s.strip() and not set(s.strip()) <= set('# =')), '(empty cell)')


def step_title(key):
    key = key.removeprefix('CALMAR_CELL_ID: ').strip()
    match = re.fullmatch(r'calmar-step-(\d+)', key)
    if not match:
        return key
    title = TITLES.get(int(match[1]), 'Notebook step')
    cells = _notebook_cells('lesion-interpretation-pipeline.ipynb')
    position = next((i for i, c in enumerate(cells, 1) if c['id'] == key), None)
    return f'{title} (cell {position})' if position else title
