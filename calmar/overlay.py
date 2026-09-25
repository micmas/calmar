"""Binary-mask comparison controls without automatic colour scaling."""

import ipywidgets as widgets


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
