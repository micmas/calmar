"""Brain-mask post-processing that keeps lesioned tissue inside the mask.

Brain extractors segment *tissue*. In chronic stroke the infarcted cortex is
resorbed and replaced by CSF that is continuous with the subarachnoid space, so
the extracted brain boundary follows the surviving tissue and leaves the lesion
cavity outside the mask. ``close_cavities`` adds such concavities back.
"""
import nibabel as nib
import numpy as np
from scipy import ndimage


def save_like(data, reference, path, dtype=np.uint8):
    """Save ``data`` with the reference image's header, qform and sform unchanged.

    ``Nifti1Image(data, ref.affine)`` rebuilds qform/sform and pixdim from one
    affine. When a scan's qform and sform differ slightly (common for scanner
    exports) the voxel size then changes in the 6th decimal, and ITK-based tools
    (LINDA, ANTs) refuse to combine the T1 with the mask ("Inputs do not occupy
    the same physical space").
    """
    ref = reference if isinstance(reference, nib.spatialimages.SpatialImage) else nib.load(str(reference))
    header = ref.header.copy()
    header.set_data_dtype(dtype)
    header.set_slope_inter(None, None)
    img = nib.Nifti1Image(np.asarray(data).astype(dtype), None, header)
    img.set_qform(ref.header.get_qform(), int(ref.header['qform_code']))
    img.set_sform(ref.header.get_sform(), int(ref.header['sform_code']))
    nib.save(img, str(path))
    return path


def ball(radius_vox):
    r = np.asarray(radius_vox, dtype=float)
    grid = np.mgrid[tuple(slice(-int(np.ceil(x)), int(np.ceil(x)) + 1) for x in r)]
    return sum((g / x) ** 2 for g, x in zip(grid, r)) <= 1.0


def close_cavities(mask, zooms, radius_mm=6.0):
    """Morphological closing with a ``radius_mm`` ball, then hole filling.

    Fills concavities narrower than ~2 x radius (sulci, cortical cavities)
    without growing the convex outer surface. Returns a boolean array.

    The closing is done with Euclidean distance transforms (in mm), which is
    the same operation as dilating then eroding with the ball but runs in
    seconds instead of minutes for large radii.
    """
    mask = np.asarray(mask) > 0.5
    zooms = [float(z) for z in zooms[:3]]
    pad = int(np.ceil(radius_mm / min(zooms))) + 2
    padded = np.pad(mask, pad)
    dilated = ndimage.distance_transform_edt(~padded, sampling=zooms) <= radius_mm
    closed = ndimage.distance_transform_edt(dilated, sampling=zooms) > radius_mm
    closed = closed[pad:-pad, pad:-pad, pad:-pad]
    return ndimage.binary_fill_holes(closed | mask)
