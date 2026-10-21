"""Interactive viewer under each processing step (replaces the QC thumbnails).

``show_step_viewer(stage, entries, study)`` displays ONE NiiVue viewer per step
(``calmar.widgets.fresh_viewer``; a re-run replaces it), with:

* a participant menu when the step ran for several participants (kernel);
* overlay checkboxes coloured as everywhere else (``calmar.colors``), lesion
  source buttons for the disconnectome steps, the plane and "Centre on lesion".
  These act in the browser (``calmar.layer_controls``), so they respond at
  once even while the kernel runs another cell.

Layers per step (``step_layers``):

=============  ==============================  ==========================================
step           background                      overlays (first ones shown)
=============  ==============================  ==========================================
brain          T1w                             HD-BET brain mask
linda          N4-corrected T1w (else T1w)     LINDA lesion; brain mask (hidden)
synthstroke    N4-corrected T1w                SynthStroke lesion; LINDA (hidden)
manual         N4-corrected T1w                manual, LINDA; SynthStroke, registered
                                               reference scan (hidden)
bcb            participant in template space   BCBToolkit map + lesion of the chosen source
deepdisco      participant in template space   DeepDisco map of the chosen model (fibre
                                               class) + lesion of the chosen source
compare        participant in template space   BCBToolkit and DeepDisco maps (model chosen)
                                               + lesion of the chosen source
=============  ==============================  ==========================================

The controls only change layer opacity, the crosshair and the plane; files are
never re-read or recomputed. Each opacity change redraws NiiVue's overlays, so
only the layers whose visibility changes are touched.
The viewer is live only while the kernel runs; the saved notebook keeps the
summary table and the QC figure paths.
"""
from pathlib import Path

import ipywidgets as widgets
from ipyniivue import MultiplanarType, ShowRender
from IPython.display import HTML, display

from . import colors as cc
from . import masks as cm
from . import qc as q
from . import widgets as cw
from .layer_controls import LayerControls, mm_to_frac
from .disconnectomes import MODEL_NAMES, SOURCE_TOKENS

LESION = {"cal_min": 0.5, "cal_max": 1.0}
MAP = {"cal_min": 0.1, "cal_max": 1.0}       # disconnectome probabilities; below 0.1 is transparent
OPACITY = {"mask": 0.35, "lesion": 0.5, "map": 0.6, "scan": 1.0, "atlas": 0.25}
MODEL_LABELS = {"whole_brain": "Whole brain", "association": "Association",
                "projection": "Projection", "commissural": "Commissural"}
HINTS = {"brain": "The brain mask should cover all brain tissue, including a lesion cavity, and no skull, scalp or neck.",
         "linda": "The lesion should follow the infarct; check for missed parts and spill into ventricles or CSF.",
         "synthstroke": "When LINDA ran, compare with it by ticking its layer.",
         "openads": "Acute lesion from OpenADS on the diffusion-weighted image (bright = restricted diffusion). "
                    "Tick the ADC map: the lesion should be dark there. Very small lesions are often missed.",
         "registration": "The T1w warped to the MNI152 template. Tick MNI152 brain on and off: the warped brain "
                         "should fill the template's brain, with ventricles and cortex in the same places. Every "
                         "template-space mask, disconnectome and atlas overlap relies on this registration.",
         "manual": "The manual mask (registered to this T1w) is the reference for both automatic masks. "
                   "Tick the registered reference scan on and off: its anatomy should line up with the T1w; "
                   "if not, the manual mask is misplaced and the Dice scores are meaningless.",
         "bcb": "Map value 0.1-1 (probability that a voxel's fibres pass through the lesion).",
         "deepdisco": "Map value 0.1-1. Model: the DeepDisco network trained on all fibres (whole brain) "
                      "or on one fibre class.",
         "compare": "Tick BCBToolkit and DeepDisco on and off to compare them at the same location "
                    "(map value 0.1-1; both ticked = blended). Untick both to see the lesion alone."}


def _label(entry):
    return f"{entry['subject']} {entry.get('session') or ''}".strip()


def _native_lesion(study, entry, source):
    return study.masks(entry).get(source, {}).get("T1w")


def _layer(name, origin, path, kind, shown=True, group="", variant="", role=None, **display):
    """One overlay. ``role`` is its checkbox; ``group`` its lesion source when the
    step offers a source choice (BCBToolkit, DeepDisco); ``variant`` its DeepDisco
    model. ``display`` overrides the NiiVue spec (e.g. ``colormap``, ``opacity``)
    for an overlay without an origin colour; ``css`` is then its swatch colour."""
    role = role or (kind if group else origin)
    return {"name": name, "origin": origin, "path": Path(path), "kind": kind, "shown": shown,
            "lesion": kind == "lesion", "role": role, "group": group, "variant": variant, "display": display}


def step_layers(stage, entry, study):
    """``(background path or None, overlay layers)`` that exist for one participant."""
    d = study.dirs(entry)
    layers = []
    if stage in ("brain", "linda", "synthstroke", "manual", "openads"):
        n4 = Path(d["linda"]) / "N4corrected.nii.gz"
        native = n4 if cm.present(n4) else Path(entry["t1w"])
        brain = q.find_best_hdbet_mask(study.hdbet_dir(entry))
    if stage == "brain":
        background = Path(entry["t1w"])
        if brain is not None:
            layers.append(_layer("HD-BET brain mask", "hdbet", brain, "mask"))
    elif stage in ("linda", "synthstroke", "manual", "openads"):
        background = native
        order = {"linda": [("linda", True)],
                 "synthstroke": [("synthstroke", True), ("linda", False)],
                 "openads": [("openads", True), ("manual", False)],
                 "manual": [("manual", True), ("linda", True), ("synthstroke", False), ("openads", True)]}[stage]
        for source, shown in order:
            path = _native_lesion(study, entry, source)
            if cm.present(path):
                layers.append(_layer(f"{cm.MASK_LABELS[source]} lesion", source, path, "lesion", shown))
        if stage == "linda" and brain is not None:
            layers.append(_layer("Brain mask", "hdbet", brain, "mask", False))
        if stage == "openads" and entry.get("adc") and cm.present(entry["adc"]):
            layers.append(_layer("ADC map", "reference", Path(entry["adc"]), "scan", False))
        reference = Path(d["template"]) / "_manual_mask_compare" / "T2_in_T1_sitk.nii.gz"
        if stage == "manual" and cm.present(reference):
            layers.append(_layer("Registered reference scan", "reference", reference, "scan", False))
    elif stage == "registration":
        # Template registration without LINDA: the warped T1 against MNI152.
        from . import templates
        background = Path(d["registration"]) / "Subject_in_MNI.nii.gz"
        layers.append(_layer("MNI152 brain", "template", templates.BRAIN_MASK, "mask", False,
                             colormap="cyan", css=cc.CSS["cyan"]))
        lesion = study.masks(entry).get("synthstroke", {}).get("MNI")
        if cm.present(lesion):
            layers.append(_layer("SynthStroke lesion", "synthstroke", lesion, "lesion"))
    elif stage == "compare":
        # BCBToolkit and DeepDisco maps of one lesion source, each with its own checkbox.
        background = Path(d["template"]) / "Subject_in_MNI.nii.gz"
        for source, token in SOURCE_TOKENS.items():
            lesion = study.masks(entry).get(source, {}).get("MNI")
            if cm.present(lesion):
                layers.append(_layer("Lesion", source, lesion, "lesion", group=source))
            bcb = Path(d["bcbtoolkit"]) / f"Disconnectome_{token}.nii.gz"
            if cm.present(bcb):
                layers.append(_layer("BCBToolkit map", "bcbtoolkit", bcb, "map", group=source, role="bcb"))
            for model in MODEL_NAMES:
                path = Path(d["deepdisco"]) / f"DeepDisco_{token}_{model}.nii.gz"
                if cm.present(path):
                    layers.append(_layer("DeepDisco map", "deepdisco", path, "map", False,
                                         group=source, variant=model, role="deepdisco"))
    elif stage in ("bcb", "deepdisco"):
        # One lesion source at a time: its map and its lesion are shown together.
        background = Path(d["template"]) / "Subject_in_MNI.nii.gz"
        for source, token in SOURCE_TOKENS.items():
            if stage == "bcb":
                maps = [("BCBToolkit map", "bcbtoolkit", Path(d["bcbtoolkit"]) / f"Disconnectome_{token}.nii.gz", "")]
            else:
                maps = [("DeepDisco map", "deepdisco", Path(d["deepdisco"]) / f"DeepDisco_{token}_{model}.nii.gz", model)
                        for model in MODEL_NAMES]
            maps = [m for m in maps if cm.present(m[2])]
            for name, origin, path, model in maps:
                layers.append(_layer(name, origin, path, "map", group=source, variant=model))
            if maps:
                lesion = study.masks(entry).get(source, {}).get("MNI")
                if cm.present(lesion):
                    layers.append(_layer("Lesion", source, lesion, "lesion", group=source))
    else:
        raise ValueError(f"No viewer layers defined for step {stage!r}")
    return (background if cm.present(background) else None), layers


def _opacity(layer):
    return layer.get("display", {}).get("opacity", OPACITY[layer["kind"]])


def _css(layer):
    if "css" in layer.get("display", {}):
        return layer["display"]["css"]
    return "#999999" if layer["kind"] == "scan" else cc.css(layer["origin"])


def _spec(layer, shown):
    display = {k: v for k, v in layer.get("display", {}).items() if k != "css"}
    if layer["kind"] == "scan":
        return {"path": str(layer["path"]), "colormap": "gray", "colorbar_visible": False,
                "opacity": OPACITY["scan"] if shown else 0.0}
    window = {"map": MAP, "atlas": {}}.get(layer["kind"], LESION)   # atlas labels: NiiVue's own range
    spec = {"path": str(layer["path"]), "colormap": display.get("colormap") or cc.color(layer["origin"]),
            "colorbar_visible": False, **window, **display}
    spec["opacity"] = _opacity(layer) if shown else 0.0
    return spec


def _roles(layers, previous):
    """Checkboxes, in layer order; a choice made earlier is kept."""
    kept = {r["key"]: r["shown"] for r in previous}
    roles = {}
    for layer in layers:
        if layer["role"] not in roles:
            label = {"map": layer["name"], "lesion": "Lesion"}.get(layer["role"], layer["name"]) \
                if layer["group"] else layer["name"]
            roles[layer["role"]] = {"key": layer["role"], "label": label,
                                    "shown": kept.get(layer["role"], layer["shown"])}
    return list(roles.values())


def _centre(layer, background):
    from .disconnectome_compare import lesion_centre_mm
    if not layer["lesion"]:
        return None
    mm = lesion_centre_mm(layer["path"])
    return None if mm is None else mm_to_frac(background, mm)


def show_layers(nv, controls, background, layers, helpers=cw):
    """Load ``background`` + ``layers`` into the viewer and describe them to the
    browser-side ``controls``, keeping the checkbox, source and model choices
    made so far. ``helpers``: the notebook's viewer helpers (``calmar.widgets``)."""
    groups = list(dict.fromkeys(l["group"] for l in layers if l["group"]))
    variants = [m for m in MODEL_NAMES if any(l["variant"] == m for l in layers)]
    roles = _roles(layers, controls.roles)
    group = controls.group if controls.group in groups else (groups[0] if groups else "")
    variant = controls.variant if controls.variant in variants else (variants[0] if variants else "")
    shown = {r["key"]: r["shown"] for r in roles}
    helpers.set_volumes(nv, [{"path": str(background), "colormap": "gray", "colorbar_visible": False}]
                        + [_spec(l, shown[l["role"]] and (not l["group"] or l["group"] == group)
                                 and (not l["variant"] or l["variant"] == variant)) for l in layers])
    with controls.hold_sync():
        controls.viewer_id = nv.model_id
        controls.groups = [[cm.MASK_LABELS[g], g] for g in groups]
        controls.group = group
        controls.variants = [[MODEL_LABELS[m], m] for m in variants]
        controls.variant = variant
        controls.roles = roles
        controls.layers = [{"model_id": volume.model_id, "role": l["role"], "group": l["group"],
                            "variant": l["variant"], "opacity": _opacity(l), "color": _css(l),
                            "centre": _centre(l, background)}
                           for volume, l in zip(nv.volumes[1:], layers)]


def viewer_layout(nv):
    """The layout every CALMaR viewer starts with: the three planes in one row,
    without the 3D render."""
    nv.opts.is_corner_orientation_text = True
    nv.opts.multiplanar_layout = MultiplanarType.ROW
    nv.opts.multiplanar_show_render = ShowRender.NEVER
    nv.opts.slice_type = 3                    # multiplanar
    return nv


class Shown(dict):
    """A viewer's widgets. Already displayed, so a cell ending with the call
    does not print them again."""
    def _ipython_display_(self):
        pass


def show_step_viewer(stage, entries, study, *, height=360, start=0, group="", variant="",
                     extra=(), key=None):
    """Display the step's viewer for ``entries``; returns its widgets (or None).

    ``start``: participant shown first; ``group``/``variant``: lesion source and
    DeepDisco model shown first (when available); ``extra``: widgets added
    under the viewer; ``key``: viewer registry key (default ``step_<stage>``).
    """
    first = entries[start] if entries else None
    entries = [e for e in entries if e.get("t1w")]
    if not entries:
        return None
    nv = viewer_layout(cw.fresh_viewer(key or f"step_{stage}", height=height))
    participant = widgets.Dropdown(options=[(_label(e), i) for i, e in enumerate(entries)],
                                   value=entries.index(first) if first in entries else 0,
                                   description="Participant:", style={"description_width": "initial"},
                                   layout=widgets.Layout(width="320px", display="" if len(entries) > 1 else "none"))
    controls = LayerControls(plane=3, group=group or "", variant=variant or "")
    status = widgets.HTML()

    def load(*_):
        entry = entries[participant.value]
        background, layers = step_layers(stage, entry, study)
        if background is None:
            nv.load_volumes([])
            controls.layers = []
            status.value = f"No image to show for {_label(entry)} yet."
            return
        show_layers(nv, controls, background, layers)
        status.value = "" if layers else "Only the background image is available for this participant."

    participant.observe(load, names="value")
    load()
    hint = widgets.HTML(f"<span style='font-size:12px'>{HINTS[stage]}</span>")
    panel = widgets.VBox([participant, controls, hint, status, nv, *extra])
    display(panel)
    return Shown(viewer=nv, participant=participant, controls=controls, status=status,
                 entries=entries, panel=panel)
