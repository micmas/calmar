"""BCBToolkit vs DeepDisco: interactive disconnectome comparison panel.

Entry point: :func:`show_disconnectome_comparison`. It shows the same viewer
and controls as the processing steps (``calmar.step_viewer``, stage
``compare``): the participant's ``Subject_in_MNI`` anatomy with, for the
chosen lesion source, its template-space lesion, the BCBToolkit map and the
DeepDisco map of the chosen model. The source and model buttons, the
checkboxes, the plane and "Centre on lesion" act in the browser
(``calmar.layer_controls``); they never reload files or recompute.

Agreement metrics are computed on request (when the "Agreement metrics"
section is opened) by the ``disconnectome`` reporting task, which runs in a
Slurm job (``calmar.reporting.run_reporting_task``) and is cached by the
input files' modification times. Their definitions are in
:data:`METRIC_DEFINITIONS` and are printed under the table.
"""

from pathlib import Path

import ipywidgets as widgets
import nibabel as nib
import numpy as np
from IPython.display import HTML, display

from . import disconnectomes as cd
from . import widgets as cw
from .masks import MASK_LABELS


#: Disconnectome value above which a voxel counts as "disconnected" for Dice
#: and the voxel counts (both maps are probabilities in 0-1).
DICE_THRESHOLD = 0.5
#: Lowest map value drawn in the viewer (values below are transparent).
DISPLAY_MIN = 0.1

METRIC_DEFINITIONS = (
    "<b>Pearson r</b>: voxel-wise correlation of the two maps (each clipped to 0–1; DeepDisco "
    "resampled linearly onto the BCBToolkit grid), computed over voxels where either map is "
    "&gt; 0. It measures whether the <i>pattern</i> agrees, independent of overall scale. "
    f"<b>Dice</b>: overlap of the binarised maps (value &gt; {DICE_THRESHOLD}), "
    "2·|A∩B| / (|A|+|B|); 1 = identical extent, 0 = no overlap. "
    "High r with low Dice usually means the same tracts are found but one method is more "
    "conservative (check the voxel counts); low r means different tracts are implicated — "
    "inspect both maps against the lesion before trusting either.")

_METRICS_CACHE = {}


def comparison_paths(study, entry, source, model):
    """Return ``(bcb_map, deepdisco_map)`` paths for one source and model."""
    dirs = study.dirs(entry)
    token = cd.SOURCE_TOKENS[source]
    return (Path(dirs["bcbtoolkit"]) / f"Disconnectome_{token}.nii.gz",
            Path(dirs["deepdisco"]) / f"DeepDisco_{token}_{model}.nii.gz")


def agreement_metrics(bcb, deepdisco, project_dir, *, threshold=DICE_THRESHOLD):
    """Pearson r, Dice and voxel counts for two maps (see METRIC_DEFINITIONS).

    Runs the ``disconnectome`` reporting task (a Slurm job) the first time;
    results are cached in memory by the files' mtimes and on disk by the
    reporting task, so reopening is instant.
    """
    from .reporting import run_reporting_task
    bcb, deepdisco = Path(bcb), Path(deepdisco)
    key = (str(bcb), str(deepdisco), bcb.stat().st_mtime_ns, deepdisco.stat().st_mtime_ns, threshold)
    if key not in _METRICS_CACHE:
        _METRICS_CACHE[key] = run_reporting_task(
            {"PROJECT_DIR": Path(project_dir)}, "disconnectome",
            bcb=str(bcb), deepdisco=str(deepdisco), threshold=threshold)
    return _METRICS_CACHE[key]


def metrics_table_html(metrics, title):
    """HTML table of the agreement metrics followed by their definitions."""
    thr = metrics["thr"]
    rows = [("Spatial correlation (Pearson r, 0–1 maps)", f"<b>{metrics['r']:.3f}</b>"),
            (f"Dice (thresholded &gt; {thr})", f"{metrics['dice']:.3f}"),
            (f"BCBToolkit voxels &gt; {thr}", f"{metrics['n_bcb']:,}"),
            (f"DeepDisco voxels &gt; {thr}", f"{metrics['n_dd']:,}")]
    body = "".join(f"<tr><td style='padding:3px 8px'>{k}</td>"
                   f"<td style='text-align:right;padding:3px 8px'>{v}</td></tr>" for k, v in rows)
    return (f"<div style='font-family:sans-serif'><h4 style='margin-bottom:4px'>{title}</h4>"
            "<table style='border-collapse:collapse;font-size:13px'>"
            "<tr style='background:#2c3e50;color:#fff'><th style='padding:4px 8px;text-align:left'>"
            "Metric</th><th style='padding:4px 8px'>Value</th></tr>"
            f"{body}</table><p style='font-size:12px;max-width:760px'>{METRIC_DEFINITIONS}</p></div>")


def lesion_centre_mm(path):
    """World coordinate (mm) of the lesion voxel closest to the lesion centroid.

    Returns None for an empty mask. The nearest *lesion* voxel is used so
    that the crosshair lands inside non-convex lesions.
    """
    img = nib.load(str(path))
    points = np.argwhere(np.asanyarray(img.dataobj) > .5)
    if not len(points):
        return None
    voxel = points[np.argmin(np.sum((points - points.mean(axis=0)) ** 2, axis=1))]
    return nib.affines.apply_affine(img.affine, voxel).tolist()


def _label(entry):
    return f"{entry['subject']} {entry.get('session') or ''}".strip()


def show_disconnectome_comparison(study, entry, *, mask_source=None, model="whole_brain",
                                  entries=None, project_dir=None, viewer_key="bcb_vs_deepdisco"):
    """Display the BCBToolkit vs DeepDisco comparison panel and return its widgets.

    Parameters
    ----------
    study : calmar.study.Study
        Provides ``dirs(entry)`` and ``masks(entry)`` (template-space lesion
        masks per source).
    entry : dict
        Participant shown first (``{"subject", "session", "t1w", ...}``).
    mask_source : {"linda", "synthstroke", "manual"} or None
        Lesion source shown first; None picks the first source with outputs.
    model : str
        DeepDisco fibre class shown first (``whole_brain``, ``association``,
        ``projection`` or ``commissural``); falls back to the first available.
    entries : list of dict, optional
        Participants offered in the participant menu (default: ``[entry]``).
    project_dir : path, optional
        Root for the reporting cache (default: ``study.project``).
    viewer_key : str
        Registry key of the single NiiVue viewer; a re-run replaces it.

    Returns
    -------
    dict with ``viewer``, ``participant``, ``controls`` (lesion source =
    ``controls.group``, DeepDisco model = ``controls.variant``), ``details``
    (the agreement-metrics section), ``status`` and ``panel``.
    """
    from .step_viewer import Shown, show_step_viewer
    entries = list(entries) if entries else [entry]
    if entry not in entries:
        entries.insert(0, entry)
    project_dir = Path(project_dir or study.project)

    glass_cb = widgets.Checkbox(value=False, description="glass-brain figures", indent=False)
    out = cw.Output()
    metrics_note = widgets.HTML(
        "<span style='font-size:12px'>Opening this section computes the agreement metrics for the "
        "selection above in a short Slurm job (about 10 s; cached afterwards). It starts only when the "
        "kernel is free: while another cell is running, nothing appears until that cell finishes.</span>")
    metrics_status = widgets.HTML()
    details = widgets.Accordion(children=[widgets.VBox([metrics_note, metrics_status, out, glass_cb])],
                                selected_index=None)
    details.set_title(0, "Agreement metrics and optional glass-brain figures")
    shown = show_step_viewer("compare", entries, study, height=560, start=entries.index(entry),
                             group=mask_source or "", variant=model or "", extra=(details,), key=viewer_key)
    if shown is None:
        display(HTML("<p>No participant with a T1w image to compare.</p>"))
        return None
    controls, participant = shown["controls"], shown["participant"]

    def render_metrics(current, source, mdl, show_glass=False):
        tag, lab = _label(current), MASK_LABELS.get(source, source)
        bcb, dd = comparison_paths(study, current, source, mdl)
        if not (cd.present(bcb) and cd.present(dd)):
            missing = "BCBToolkit" if not cd.present(bcb) else "DeepDisco"
            display(HTML(f"<h4>{tag} · {lab}</h4><p>{missing} map missing for this selection; "
                         "agreement metrics require both methods.</p>"))
            return
        m = agreement_metrics(bcb, dd, project_dir)
        display(HTML(metrics_table_html(
            m, f"BCBToolkit vs DeepDisco &mdash; {tag} &middot; mask: {lab} &middot; map: {mdl}")))
        if show_glass:
            try:
                from IPython.display import Image
                display(Image(filename=str(m["png"])))
            except Exception as ex:
                print(f"  (figure failed: {ex})")

    def show_details(*_):
        if details.selected_index is None:
            return
        if not controls.group:
            metrics_status.value = "No lesion source with disconnectome maps for this participant."
            return
        metrics_status.value = "<i>Computing agreement metrics (Slurm reporting job)…</i>"
        try:
            with out:
                out.clear_output(wait=True)
                render_metrics(shown["entries"][participant.value], controls.group,
                               controls.variant, glass_cb.value)
            metrics_status.value = ""
        except Exception as error:  # shown in the panel; a callback error is otherwise invisible
            metrics_status.value = (f"<span style='color:#c62828'>Agreement metrics failed: "
                                    f"{type(error).__name__}: {error}</span>")

    # The metrics follow the source and model chosen in the browser.
    controls.observe(show_details, names=["group", "variant"])
    participant.observe(show_details, names="value")
    glass_cb.observe(show_details, names="value")
    details.observe(show_details, names="selected_index")
    return Shown(shown, details=details)
