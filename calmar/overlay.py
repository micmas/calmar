"""Binary-mask comparison controls without automatic colour scaling."""

import ipywidgets as widgets
from pathlib import Path
from html import escape

import nibabel as nib
import numpy as np

from . import colors


def agreement_table(metrics, manual_voxels, errors=None):
    """Compare tools in columns, with the same metric on each row."""
    errors = errors or {}
    tools = list(metrics)
    header = '<tr><th>Metric</th>' + ''.join(
        f'<th>{colors.legend([name.lower()])}</th>' for name in tools) + '</tr>'
    rows = []
    for label, key, format_value in (
        ('Dice', 'dice', lambda x: f'{x:.3f}'),
        ('IoU / Jaccard', 'iou', lambda x: f'{x:.3f}'),
        ('Sensitivity', 'sens', lambda x: f'{x:.1%}'),
        ('Precision', 'prec', lambda x: f'{x:.1%}'),
        ('Lesion voxels', 'n', lambda x: f'{x:,}'),
        ('Overlapping voxels', 'overlap', lambda x: f'{x:,}'),
    ):
        cells = ''.join(f'<td style="text-align:right;padding:5px 18px">{format_value(metrics[name][key]) if metrics[name] else "—"}</td>' for name in tools)
        rows.append(f'<tr><td style="padding:5px 12px">{label}</td>{cells}</tr>')
    if any(metrics[name] is None for name in tools):
        rows.append('<tr><td>Status</td>' + ''.join(
            '<td>' + ('Available' if metrics[name] else escape(errors.get(name, 'Not yet run'))) + '</td>' for name in tools) + '</tr>')
    return (f'<p>Manual reference: {manual_voxels:,} lesion voxels. Each tool is compared with this mask.</p>'
            '<div style="overflow-x:auto"><table style="border-collapse:collapse">' + header + ''.join(rows) + '</table></div>')


def mask_comparison(cw, key, volumes, **viewer_kwargs):
    """Keep zero-valued voxels transparent, including in very sparse masks."""
    specs = [dict(v) for v in volumes]
    for spec in specs[1:]:
        spec.update(cal_min=0.5, cal_max=1.0)
    nv = cw.fresh_viewer(key, **viewer_kwargs)
    controls = [widgets.Checkbox(value=True, description=spec.get("name", f"Mask {i}"),
                                indent=False)
                for i, spec in enumerate(specs[1:], 1)]

    # Keep the same Volume models and GPU textures while toggling visibility.
    # Replacing the volume list creates new asynchronous loads, which can race
    # checkbox changes and leave the browser showing an older selection.
    nv.load_volumes(cw.vols(specs))
    for index, (spec, control) in enumerate(zip(specs[1:], controls), 1):
        opacity = spec.get("opacity", 1.0)

        def update(change, index=index, opacity=opacity):
            nv.set_opacity(index, opacity if change["new"] else 0.0)

        control.observe(update, names="value")
    return widgets.VBox([widgets.HBox(controls), nv])


def reference_edges(path):
    """Cache an anatomical edge overlay for reviewing an existing registration."""
    path = Path(path)
    target = path.with_name(path.name.replace('.nii.gz', '_edges.nii.gz'))
    if target.exists() and target.stat().st_mtime >= path.stat().st_mtime:
        return target
    img = nib.load(path)
    data = img.get_fdata(dtype=np.float32)
    gradient = np.sqrt(sum(np.square(np.gradient(data, axis=axis)) for axis in range(3)))
    nonzero = gradient[gradient > 0]
    threshold = np.percentile(nonzero, 92) if nonzero.size else 1.
    nib.save(nib.Nifti1Image((gradient >= threshold).astype(np.uint8), img.affine), target)
    return target


def mask_review(cw, key, volumes, *, coreg_path=None, metrics_html=''):
    """One canvas for registration review followed by lesion-mask comparison."""
    specs = [dict(v) for v in volumes]
    has_coreg = coreg_path is not None and Path(coreg_path).is_file()
    mask_opacities = [s.get('opacity', 1.) for s in specs[1:]]
    for spec in specs[1:]:
        spec.update(cal_min=.5, cal_max=1., opacity=0. if has_coreg else spec.get('opacity', 1.))
    if has_coreg:
        specs.append(dict(path=str(reference_edges(coreg_path)), name='Registered scan edges',
                          colormap='warm', cal_min=.5, cal_max=1., opacity=1.))
    viewer = cw.fresh_viewer(key, height=440)
    viewer.load_volumes(cw.vols(specs))
    options = [('1. Coregistration', 'coreg'), ('2. Lesion masks', 'masks')] if has_coreg else [('Lesion masks', 'masks')]
    mode = widgets.ToggleButtons(options=options)
    note = widgets.HTML()
    masks = [widgets.Checkbox(value=True, description=s.get('name', f'Mask {i}'), indent=False)
             for i, s in enumerate(volumes[1:], 1)]
    mask_controls = widgets.HBox(masks, layout=widgets.Layout(flex_flow='row wrap'))
    opacity = widgets.FloatSlider(value=1., min=0., max=1., step=.05,
                                   description='Scan edges:', continuous_update=False)
    metrics = widgets.Accordion(children=[widgets.HTML(metrics_html)], selected_index=None)
    metrics.set_title(0, 'Agreement with manual mask')
    def update(*_):
        coreg = mode.value == 'coreg'
        mask_controls.layout.display = 'none' if coreg else ''
        opacity.layout.display = '' if coreg else 'none'
        metrics.layout.display = 'none' if coreg else ''
        note.value = (
            'Check that the registered reference-scan edges follow the T1 anatomy, especially '
            'the ventricles and cortex. Use Scan edges to fade the overlay, then select Lesion masks.'
            if coreg else colors.legend([s.get('name', '').lower() for s in volumes[1:]]) +
            '<br>Manual mask is filled; automatic masks are outlines. Toggle each mask to compare.' +
            ('' if has_coreg else '<br>No reference-scan coregistration is available for this comparison.'))
        # Visibility updates keep the same layers, canvas and slice position.
        for i, (control, value) in enumerate(zip(masks, mask_opacities), 1):
            viewer.set_opacity(i, value if control.value and not coreg else 0.)
        if has_coreg:
            viewer.set_opacity(len(specs)-1, opacity.value if coreg else 0.)
    mode.observe(update, names='value')
    opacity.observe(update, names='value')
    for control in masks:
        control.observe(update, names='value')
    update()
    panel = widgets.VBox([mode, note, opacity, mask_controls, viewer, metrics])
    panel.review_mode, panel.viewer, panel.mask_controls = mode, viewer, masks
    return panel
