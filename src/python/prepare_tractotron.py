"""Resample a binary MNI lesion to the actual bundled tract-atlas grid."""
import json
import os
from pathlib import Path
import sys

import nibabel as nib
from nibabel.processing import resample_from_to
import numpy as np


def prepare(mask, reference, output):
    if not os.environ.get('SLURM_JOB_ID'):
        raise RuntimeError('Tractotron preparation requires a Slurm allocation.')
    ref = nib.load(reference)
    sampled = resample_from_to(nib.load(mask), ref, order=0)
    nib.save(nib.Nifti1Image((sampled.get_fdata() > .5).astype('uint8'), ref.affine), output)
    Path(str(output)+'.grid.json').write_text(json.dumps({
        'reference': 'BCBToolKit/Tools/HCP1065/prob/Arcuate_Fasciculus_L.nii.gz',
        'shape': list(ref.shape), 'affine': ref.affine.tolist(),
        'interpolation': 'nearest', 'threshold': .5}, indent=2))


if __name__ == '__main__':
    prepare(*sys.argv[1:])
