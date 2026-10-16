"""Interactive brain-mask check (the registration and lesion-mask review is in
the manual step's viewer, ``calmar.step_viewer``)."""
from IPython.display import HTML, display
from . import colors as cc


def show_brain_mask(entry, hdbet_dir, cw):
    """Interactive check of the HD-BET mask on the T1w (toggle the overlay)."""
    import ipywidgets as widgets
    from . import qc as q
    mask = q.find_best_hdbet_mask(hdbet_dir)
    if mask is None:
        print('No HD-BET mask yet.')
        return None
    viewer = cw.show("hdbet_test", [
        {"path": str(entry["t1w"])},
        {"path": str(mask), "colormap": cc.color("hdbet"), "opacity": 0.35, "cal_min": 0.5, "cal_max": 1.0},
    ])
    toggle = widgets.Checkbox(value=True, description=f"Show brain mask ({cc.color('hdbet')})")
    def flip(change):
        viewer.volumes[1].opacity = 0.35 if change["new"] else 0.0
    toggle.observe(flip, names="value")
    display(HTML("<b>Interactive view</b> — scroll through slices; " + cc.legend(["hdbet"])
                 + " should cover all brain tissue and no skull, scalp or neck."), toggle, viewer)
    return viewer
