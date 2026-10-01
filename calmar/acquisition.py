"""Materialize individual NIfTI inputs while preserving dataset-relative paths."""

import os
from pathlib import Path
import shutil
import subprocess

import nibabel as nib


def nifti_available(path):
    """Check the image header, without a size heuristic or loading voxel data."""
    try:
        img = nib.load(str(path))
        return len(img.shape) >= 3 and all(size > 0 for size in img.shape)
    except (OSError, ValueError, EOFError, nib.filebasedimages.ImageFileError):
        return False


def ensure_nifti_content(path, dataset_root=None):
    """Fetch missing annex content and confirm a readable NIfTI header.

    Keep the logical BIDS filename: resolving an annex symlink would instead
    hand DataLad a path inside its object store. Existing small masks are valid.
    """
    path = Path(os.path.abspath(Path(path).expanduser()))
    if nifti_available(path):
        return True

    root = Path(os.path.abspath(Path(dataset_root).expanduser())) if dataset_root else None
    if root is None or not path.is_relative_to(root):
        root = next((parent for parent in path.parents
                     if (parent / ".datalad").is_dir()
                     or (parent / ".git").exists()), None)
    if root is None:
        print(f"  ❌ NIfTI content unavailable: {path} (no dataset found)")
        return False
    if shutil.which("datalad") is None:
        print(f"  ❌ NIfTI content unavailable: {path}; DataLad is not on PATH.")
        return False

    relative = path.relative_to(root)
    script = Path(__file__).resolve().parents[1] / "src" / "analysis_18_fetch_nifti_content.sh"
    print(f"  → Fetching {relative} via DataLad …")
    result = subprocess.run(["bash", str(script), str(root), str(relative)],
                            capture_output=True, text=True)
    if result.returncode == 0 and nifti_available(path):
        print(f"    ✓ NIfTI content available: {path.name}")
        return True
    print(f"  ❌ Could not fetch readable NIfTI content: {path} (exit {result.returncode})")
    detail = (result.stderr or result.stdout or "").strip()
    if detail:
        print(f"    {detail[-1000:]}")
    return False
