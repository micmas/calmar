"""Read-only discovery of per-subject disconnectomes for notebook viewers."""

from pathlib import Path

from .masks import MASK_LABELS, present


MODEL_NAMES = ("whole_brain", "association", "projection", "commissural")
SOURCE_TOKENS = {"linda": "linda", "synthstroke": "synthstroke", "manual": "expert"}


def discover(bcb_dir, deepdisco_dir):
    """Return available maps by source, independently for each method.

    Paths must already be scoped to one subject/session. Ignore resampling
    caches, empty files, and unfetched annex links. The legacy ``expert``
    filename token denotes the manual mask; it is not a fourth source.
    """
    found = {}
    for source, token in SOURCE_TOKENS.items():
        bcb = Path(bcb_dir) / f"Disconnectome_{token}.nii.gz"
        models = {}
        for model in MODEL_NAMES:
            path = Path(deepdisco_dir) / f"DeepDisco_{token}_{model}.nii.gz"
            if present(path):
                models[model] = path
        found[source] = {"bcb": bcb if present(bcb) else None, "deepdisco": models}
    return found


def available_sources(maps, lesions=None):
    """Offer sources with a map or an existing lesion, even without BCB."""
    lesions = lesions or {}
    return [(label, source) for source, label in MASK_LABELS.items()
            if maps[source]["bcb"] is not None or maps[source]["deepdisco"]
            or present(lesions.get(source))]


def map_options(maps, source):
    if source is None:
        return []
    item = maps[source]
    options = [("BCBToolkit", item["bcb"])] if item["bcb"] else []
    options.extend((f"DeepDisco · {model}", path)
                   for model, path in item["deepdisco"].items())
    return options
