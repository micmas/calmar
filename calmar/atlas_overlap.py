"""Atlas overlap, including laterality of the actual intersecting lesion voxels."""

from pathlib import Path
import json
import os

import nibabel as nib
import numpy as np
import pandas as pd
from nilearn.image import resample_to_img

SIDE_COLUMNS = ['left_overlap_voxels', 'right_overlap_voxels', 'midline_overlap_voxels']
COLUMNS = ['subject', 'session', 'atlas', 'region', 'region_id',
           'lesion_in_roi_percent', 'roi_coverage_percent', 'overlap_voxels',
           'total_region_voxels', 'total_lesion_voxels', *SIDE_COLUMNS]


def calculate_overlap(lesion_path, atlas_img, atlas_data, atlas_labels, threshold=.5):
    """Keep ROI totals intact; count sides using MNI world x, not array indices."""
    lesion = resample_to_img(nib.load(str(lesion_path)), atlas_img,
                            interpolation='nearest', force_resample=True, copy_header=True)
    selected = np.asarray(lesion.dataobj) > threshold
    total = int(selected.sum())
    points = np.argwhere(selected)
    values = np.asarray(atlas_data)[selected].astype(int)
    x = nib.affines.apply_affine(atlas_img.affine, points)[:, 0]
    result = {}
    ids, sizes = np.unique(atlas_data, return_counts=True)
    sizes = dict(zip(ids.astype(int), sizes))
    for region_id in np.unique(values):
        if region_id == 0:
            continue
        hit = values == region_id
        n = int(hit.sum())
        if isinstance(atlas_labels, dict):
            name = atlas_labels.get(int(region_id), f'Region_{region_id}')
        else:
            name = atlas_labels[region_id] if region_id < len(atlas_labels) else f'Region_{region_id}'
        if isinstance(name, bytes):
            name = name.decode()
        result[str(name)] = dict(
            region_id=int(region_id), overlap_voxels=n,
            total_region_voxels=int(sizes[region_id]),
            lesion_in_roi_percent=100. * n / total,
            roi_coverage_percent=100. * n / sizes[region_id],
            left_overlap_voxels=int(np.count_nonzero(hit & (x < -1e-5))),
            right_overlap_voxels=int(np.count_nonzero(hit & (x > 1e-5))),
            midline_overlap_voxels=int(np.count_nonzero(hit & (np.abs(x) <= 1e-5))))
    return result, total


def cached_overlap(csv, entries, mask_path, atlas_name, atlas_img, atlas_data,
                   atlas_labels, threshold=.5, overwrite=False):
    """Cache completed subject/session pairs even when no atlas ROI was hit.

    Legacy CSVs are refreshed once to add measured laterality. Source file
    identity and the atlas geometry/data invalidate changed inputs.
    """
    import hashlib
    csv = Path(csv)
    manifest = csv.with_suffix('.status.json')
    df = pd.read_csv(csv).fillna({'session': ''}) if csv.exists() else pd.DataFrame(columns=COLUMNS)
    state = json.loads(manifest.read_text()) if manifest.exists() else {}
    atlas_digest = hashlib.sha256(np.asarray(atlas_data).tobytes() + atlas_img.affine.tobytes()).hexdigest()
    statuses = {}
    for entry in entries:
        subject, session = entry['subject'], entry.get('session') or ''
        key = json.dumps([subject, session])
        path = Path(mask_path(entry))
        selected = (df.subject == subject) & (df.session == session)
        if not path.is_file():
            df = df.loc[~selected]
            statuses[key] = {'status': 'missing_mask'}
            continue
        stat = path.stat()
        identity = [str(path.resolve()), stat.st_mtime_ns, stat.st_size, float(threshold), atlas_digest]
        previous = state.get(key, {})
        if not overwrite and set(SIDE_COLUMNS).issubset(df.columns) and previous.get('identity') == identity:
            statuses[key] = previous
            continue
        overlaps, total = calculate_overlap(path, atlas_img, atlas_data, atlas_labels, threshold)
        rows = [dict(subject=subject, session=session, atlas=atlas_name, region=region,
                     total_lesion_voxels=total, **stats) for region, stats in overlaps.items()]
        df = pd.concat([df.loc[~selected], pd.DataFrame(rows, columns=COLUMNS)], ignore_index=True)
        statuses[key] = dict(status='complete', total_lesion_voxels=total,
                             regions=len(rows), identity=identity)
    # Concatenating an empty (zero-overlap) result must not leave object arrays;
    # matplotlib heatmaps and numerical consumers require numeric dtypes.
    for column in COLUMNS[4:]:
        df[column] = pd.to_numeric(df[column])
    csv.parent.mkdir(parents=True, exist_ok=True)
    if csv.exists() and not csv.with_suffix('.before-laterality.csv').exists():
        import shutil
        shutil.copy2(csv, csv.with_suffix('.before-laterality.csv'))
    tmp = csv.with_name(f'.{csv.name}.{os.getpid()}.tmp')
    df.to_csv(tmp, index=False)
    tmp.replace(csv)
    tmp = manifest.with_name(f'.{manifest.name}.{os.getpid()}.tmp')
    tmp.write_text(json.dumps(statuses, indent=2))
    tmp.replace(manifest)
    df.attrs['overlap_status'] = statuses
    return df
