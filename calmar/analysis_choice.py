"""Shared interaction conventions for optional notebook analyses."""

from copy import deepcopy
from html import escape

import ipywidgets as w

from .study import ENTRY_CONFIG


RUN = "run"
USE_PRIOR = "use_prior"
RERUN = "rerun"
SKIP = "skip"
ACTION_CONFIG_KEYS = {
    "OPENADS_OVERWRITE", "OPENADS_REUSE_PRIOR",
    "DMRI_OVERWRITE", "DMRI_REUSE_PRIOR",
    "BRAIN_HEALTH_OVERWRITE", "BRAIN_HEALTH_REUSE_PRIOR",
}


def action_help_html():
    return (
        "<p><b>Choose one action per participant.</b> Use saved results keeps valid stages and, when clearly "
        "warned, can retain an older result; missing stages still run. Rerun starts this optional analysis "
        "again under the pipeline's overwrite policy. New, partial, or changed analyses remain unselected "
        "until you choose an action. Visual QC is still required.</p>")


def action_options(*, prior_available=False, current_complete=False, outputs_exist=False):
    """Return consistent action labels and a safe default for one analysis."""
    if prior_available:
        label = "Use saved results" if current_complete else "Use saved results where available"
        options = [
            (label, USE_PRIOR),
            ("Rerun from the start", RERUN),
            ("Do not analyse", SKIP),
        ]
        # Optional work stays opt-in when a prior result is stale or partial.
        return options, USE_PRIOR if current_complete else SKIP
    if outputs_exist:
        return [("Rerun from the start", RERUN),
                ("Do not analyse", SKIP)], SKIP
    return [("Run analysis", RUN), ("Do not analyse", SKIP)], SKIP


def action_dropdown(*, prior_available=False, current_complete=False, outputs_exist=False):
    options, value = action_options(
        prior_available=prior_available, current_complete=current_complete,
        outputs_exist=outputs_exist)
    return w.Dropdown(
        options=options, value=value, description="Action:",
        style={"description_width": "initial"}, layout=w.Layout(width="360px"))


_STATUS_BADGES = {
    "reusable": ("✓ Reusable", "#e8f5e9", "#1b5e20"),
    "partial": ("◐ Partial", "#fff8e1", "#7a4f00"),
    "partial_changed": ("◐ Some stages need review", "#fff8e1", "#7a4f00"),
    "new": ("○ Not analysed", "#f2f2f2", "#444"),
    "derived": ("⚠ Uses an older input", "#fff3e0", "#8a3f00"),
    "changed": ("⚠ Saved result may be out of date", "#fff3e0", "#8a3f00"),
    "existing": ("⚠ Unmatched saved files", "#fff3e0", "#8a3f00"),
    "rerun": ("↻ Rerun configured", "#e8f0fe", "#174ea6"),
    "unavailable": ("⚠ Status unavailable", "#ffebee", "#8a1c1c"),
}


def action_state_kwargs(state):
    """Translate a receipt state into safe shared action-menu inputs."""
    if state.get("rerun_required"):
        return {"prior_available": False, "current_complete": False, "outputs_exist": True}
    return {key: state[key]
            for key in ("prior_available", "current_complete", "outputs_exist")}


def compact_choice_heading(subject, kind, details, *, tags=(), warning_count=0):
    """Render the common compact heading used by optional-analysis decisions."""
    label, background, foreground = _STATUS_BADGES.get(
        kind, ("⚠ Review", "#fff3e0", "#8a3f00"))
    pills = [
        f"<span style='display:inline-block;margin-left:6px;padding:2px 7px;border-radius:10px;"
        f"background:#eef2f6;color:#34495e;font-size:12px'>{escape(str(tag))}</span>"
        for tag in tags if tag
    ]
    if warning_count:
        noun = "warning" if warning_count == 1 else "warnings"
        pills.append(
            "<span style='display:inline-block;margin-left:7px;color:#7a4f00;font-size:12px'>"
            f"· {warning_count} scan {noun}</span>")
    rows = "".join(
        f"<li><b>{escape(str(name))}</b>: {escape(str(value))}</li>"
        for name, value in details
    )
    disclosure = (
        "<details style='display:inline-block;margin-left:8px;font-size:12px;vertical-align:middle'>"
        f"<summary aria-label='Details for {escape(str(subject))}' "
        "style='cursor:pointer;color:#52606d'>&nbsp;Details</summary>"
        "<ul style='margin:5px 0 3px 18px;padding:0;min-width:390px'>" + rows +
        "</ul></details>")
    return (
        f"<div style='margin:4px 0'><b>{escape(str(subject))}</b> "
        f"<span style='display:inline-block;margin-left:8px;padding:2px 7px;border-radius:10px;"
        f"background:{background};color:{foreground};font-size:12px'>{escape(label)}</span>"
        f"{''.join(pills)}{disclosure}</div>")


def set_action_options(widget, *, prior_available=False, current_complete=False, outputs_exist=False):
    options, default = action_options(
        prior_available=prior_available, current_complete=current_complete,
        outputs_exist=outputs_exist)
    widget.options = options
    # A session/FLAIR change is a new decision. In particular, never carry an
    # automatic current-result reuse into a stale-result choice.
    widget.value = default


def action_buttons():
    """Same primary/secondary controls in every optional-analysis panel."""
    apply = w.Button(
        description="Apply choices and continue", button_style="primary",
        layout=w.Layout(width="230px"))
    skip = w.Button(
        description="Skip all and continue", button_style="warning",
        layout=w.Layout(width="190px"))
    return apply, skip


def entry_with_action(entry, action, *, overwrite_key, reuse_key):
    """Attach a participant-specific scheduler policy without changing siblings."""
    selected = deepcopy(entry)
    overrides = dict(selected.get(ENTRY_CONFIG) or {})
    if action == RUN:
        # The configured path keeps its existing policy; this also preserves
        # backward compatibility for callers that predate action menus.
        pass
    else:
        overrides[overwrite_key] = action == RERUN
        overrides[reuse_key] = action == USE_PRIOR
    selected[ENTRY_CONFIG] = overrides
    return selected


def without_action_policy(entry):
    """Remove notebook-only action flags from compact report-link metadata."""
    selected = deepcopy(entry)
    overrides = dict(selected.get(ENTRY_CONFIG) or {})
    for key in ACTION_CONFIG_KEYS:
        overrides.pop(key, None)
    if overrides:
        selected[ENTRY_CONFIG] = overrides
    else:
        selected.pop(ENTRY_CONFIG, None)
    return selected
