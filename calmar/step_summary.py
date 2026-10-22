"""Readable, saved summaries of a processing step for the notebook.

``show_step(result, study=study)`` renders, for each participant: what happened
(computed / reused / skipped / stale), key plausibility metrics, any ⚠ flags and
the exact commands that produced the outputs, followed by an interactive viewer
of the step's images (``calmar.step_viewer``). The QC figure each job writes is
listed by path; ``images=True`` embeds it instead (static, kept in the saved
notebook without a kernel).
"""
import base64
from html import escape
from pathlib import Path

from IPython.display import HTML, display

STATUS = {"computed": "computed now", "cached": "reused (unchanged)",
          "legacy-cache": "reused (older output, no run record)", "skipped": "skipped",
          "missing": "input missing", "stale": "⚠ stale — method changed"}
METRIC_LABELS = {
    "brain_volume_ml": "brain volume (ml)", "template_correlation": "T1↔MNI152 r",
    "linda_volume_ml": "LINDA lesion (ml)", "linda_components": "LINDA blobs",
    "linda_mni_volume_ml": "LINDA lesion in template (ml)",
    "linda_fraction_outside_brain": "LINDA outside brain mask",
    "synthstroke_volume_ml": "SynthStroke lesion (ml)", "synthstroke_components": "SynthStroke blobs",
    "synthstroke_removed_outside_brain_ml": "removed outside dilated brain mask (ml)",
    "synthstroke_fraction_outside_brain": "SynthStroke outside brain mask",
    "dice_synthstroke_vs_linda": "Dice SynthStroke–LINDA",
    "manual_volume_ml": "manual lesion (ml)", "manual_components": "manual blobs",
    "dice_linda_vs_manual": "Dice LINDA–manual", "dice_synthstroke_vs_manual": "Dice SynthStroke–manual",
    "dice_linda_vs_manual_mni": "Dice LINDA–manual (template)",
    "manual_fraction_outside_brain": "manual outside brain mask", "manual_fraction_outside_head": "manual outside head",
    "synthstroke_mni_volume_ml": "SynthStroke lesion in template (ml)", "manual_mni_volume_ml": "manual lesion in template (ml)",
    "mask_session": "mask session", "t1_session": "T1 session", "mask_space": "mask drawn on",
}
VIEWER_STAGES = ("brain", "linda", "synthstroke", "registration", "openads", "manual", "bcb", "deepdisco")
EMBED_LIMIT = 12  # participants whose figures are embedded; beyond that, paths only


def _fmt(value):
    if isinstance(value, float):
        return f"{value:.3g}" if abs(value) < 1000 else f"{value:,.0f}"
    return str(value)


def _status(entry):
    states = [o.get("status", "validated") for o in entry.get("outputs", [])]
    reasons = [o.get("reason") for o in entry.get("outputs", []) if o.get("reason")]
    text = ", ".join(sorted({STATUS.get(s, s) for s in states})) or "no outputs"
    return text, reasons


SOURCES = {"linda": "LINDA", "synthstroke": "SynthStroke", "openads": "OpenADS", "manual": "Manual"}


def _pct(value):
    return "0%" if value == 0 else ("<1%" if value < 0.005 else f"{value:.0%}")


def _metric_lines(metrics):
    """Metrics as a few readable lines: ``[(heading, text), ...]``."""
    m = {k: v for k, v in metrics.items() if k != "mask_file"}
    used, lines = set(), []
    def take(key):
        used.add(key)
        return m.get(key)
    if "dwi_series_available" in m:
        total = take("dwi_series_available")
        sessions = take("dwi_sessions_available")
        same, other = take("dwi_same_session"), take("dwi_other_session")
        ready = take("dwi_openads_ready")
        text = (f"{total} series across {sessions}; {same} in the selected session, "
                f"{other} in other sessions; {ready} with an exact sibling ADC map for OpenADS")
        lines.append(("DWI availability", text))
    if "brain_volume_ml" in m:
        parts = [f"{_fmt(take('brain_volume_ml'))} ml"]
        if m.get("added_by_synthstrip_ml") is not None:
            parts.append(f"{_fmt(take('added_by_synthstrip_ml'))} ml added by SynthStrip")
        lines.append(("Brain", ", ".join(parts)))
    if "template_correlation" in m:
        lines.append(("Registration", f"T1 vs MNI152 template r = {take('template_correlation'):.2f}"))
    if "mask_space" in m:
        space, mask_ses, t1_ses = take("mask_space"), take("mask_session"), take("t1_session")
        where = {"t1": "drawn on this scan (no registration needed)", "mni": "drawn in template space",
                 "other": "drawn on another scan, rigidly registered to this T1"}.get(space, f"space: {space}")
        if mask_ses and t1_ses and mask_ses != t1_ses:
            where += f" (mask from {mask_ses}, T1 from {t1_ses})"
        lines.append(("Manual mask", where))
    for source, label in SOURCES.items():
        if f"{source}_volume_ml" not in m and f"{source}_mni_volume_ml" not in m:
            continue
        parts = []
        if m.get(f"{source}_volume_ml") is not None:
            blobs = m.get(f"{source}_components")
            parts.append(f"{_fmt(take(f'{source}_volume_ml'))} ml"
                         + (f" in {take(f'{source}_components')} blob{'s' if blobs != 1 else ''}" if blobs is not None else ""))
        if m.get(f"{source}_mni_volume_ml") is not None:
            parts.append(f"{_fmt(take(f'{source}_mni_volume_ml'))} ml in template")
        for key, what in ((f"{source}_fraction_outside_brain", "outside brain mask"),
                          (f"{source}_fraction_outside_head", "outside head")):
            if m.get(key) is not None:
                parts.append(f"{_pct(take(key))} {what}")
        if m.get(f"{source}_removed_outside_brain_ml") is not None:
            parts.append(f"{_fmt(take(f'{source}_removed_outside_brain_ml'))} ml removed outside the dilated brain mask")
        lines.append((f"{label} lesion", ", ".join(parts)))
    dice = []
    for key in sorted(k for k in m if k.startswith("dice_")):
        a, _, rest = key[5:].partition("_vs_")
        b, _, space = rest.partition("_")
        dice.append(f"{SOURCES.get(a, a)} vs {SOURCES.get(b, b)}"
                    + (" (template)" if space == "mni" else "") + f" <b>{take(key):.2f}</b>")
    if dice:
        lines.append(("Agreement (Dice)", " · ".join(dice)))
    # Why a Dice is low: too large (little of it inside the manual lesion) or
    # too small (covers little of the manual lesion).
    versus = []
    for source, label in SOURCES.items():
        covers, inside = m.get(f"{source}_covers_manual"), m.get(f"{source}_inside_manual")
        if covers is None or inside is None:
            continue
        take(f"{source}_covers_manual"), take(f"{source}_inside_manual")
        text = f"{label} covers {_pct(covers)} of the manual lesion and {_pct(inside)} of {label} lies inside it"
        ratio = (m.get(f"{source}_volume_ml") or 0) / (m.get("manual_volume_ml") or float("nan"))
        if ratio > 1.2:
            text += f" ({ratio:.1f}× the manual volume: larger)"
        elif ratio < 1 / 1.2:
            text += f" ({ratio:.1f}× the manual volume: smaller)"
        versus.append(text)
    if versus:
        lines.append(("Versus manual", " · ".join(versus)))
    maps = [(source, label) for source, label in SOURCES.items() if f"{source}_voxels_above_0.5" in m]
    for source, label in maps:
        text = f"{take(f'{source}_voxels_above_0.5'):,} voxels above 0.5"
        if m.get(f"{source}_r_vs_bcb") is not None:
            text += f", r = {take(f'{source}_r_vs_bcb'):.2f} with BCBToolkit"
        lines.append((f"Map ({label} lesion)", text))
    lines += [(METRIC_LABELS.get(k, k), _fmt(v)) for k, v in m.items() if k not in used]
    return lines


def _metrics(entry):
    lines = _metric_lines((entry.get("qc") or {}).get("metrics", {}))
    return "".join(f"<div style='margin-bottom:2px'><span style='color:var(--jp-ui-font-color2)'>"
                   f"{escape(head)}:</span> {text if '<b>' in text else escape(text)}</div>"
                   for head, text in lines)


def _image(path):
    data = base64.b64encode(Path(path).read_bytes()).decode()
    return f'<img src="data:image/png;base64,{data}" style="max-width:100%">'


def step_html(result, *, title=None, images=False):
    rows, details = [], []
    entries = result.get("results", [])
    for i, entry in enumerate(entries):
        who = escape(f"{entry['subject']} {entry.get('session') or ''}".strip())
        status, reasons = _status(entry)
        if entry.get("reused_from_job"):
            status = f"reused — unchanged since Slurm job {entry['reused_from_job']}"
        flags = list((entry.get("qc") or {}).get("flags", [])) + [
            r for r in reasons if "Stale" in r or "unavailable" in r or "predates" in r]
        flags = list(dict.fromkeys(flags))  # one line per distinct check, not per mask source
        flag_html = "<br>".join("⚠ " + escape(f) for f in flags) or "—"
        rows.append(f"<tr><td>{who}</td><td>{escape(status)}</td><td>{_metrics(entry) or '—'}</td>"
                    f"<td>{flag_html}</td><td>{entry.get('seconds', 0):.0f} s</td></tr>")
        commands = [c for o in entry.get("outputs", []) for c in o.get("commands", [])]
        tools = {k: v for o in entry.get("outputs", []) for k, v in (o.get("tools") or {}).items()}
        parts = []
        png = (entry.get("qc") or {}).get("png")
        if png and Path(png).is_file():
            parts.append(_image(png) if images and i < EMBED_LIMIT
                         else f"<p style='font-size:12px'>QC figure: <code>{escape(png)}</code></p>")
        if commands:
            parts.append("<details><summary>Commands that produced these outputs</summary><pre style='white-space:pre-wrap'>"
                         + escape("\n\n".join(dict.fromkeys(commands)))
                         + ("\n\nTools (resolved; Neurodesk container folder gives version and build):\n"
                            + escape("\n".join(f"{k}: {v}" for k, v in tools.items())) if tools else "")
                         + "</pre></details>")
        elif any(o.get("status") == "legacy-cache" for o in entry.get("outputs", [])):
            parts.append("<p><i>Commands not recorded: this output predates run records.</i></p>")
        outputs = [o["path"] for o in entry.get("outputs", []) if o.get("path")]
        if outputs:
            parts.append("<details><summary>Output files</summary><pre>" + escape("\n".join(outputs)) + "</pre></details>")
        if entry.get("log_folder"):
            parts.append(f"<p style='font-size:12px'>Slurm job logs: <code>{escape(entry['log_folder'])}</code></p>")
        if parts:
            details.append(f"<details><summary><b>{who}</b>: commands, files and logs</summary>{''.join(parts)}</details>")
    logs = None if any(e.get("log_folder") for e in entries) else result.get("log_folder")
    head = escape(title or f"{result.get('stage')} step")
    return (f"<div style='font-family:sans-serif'><h4 style='margin:6px 0'>{head}</h4>"
            "<table style='border-collapse:collapse;font-size:13px' border='1' cellpadding='4'>"
            "<tr><th>Participant</th><th>Result</th><th>Key metrics</th><th>⚠ Workflow checks</th><th>Time</th></tr>"
            + "".join(rows) + "</table>"
            + (f"<p style='font-size:12px'>Slurm logs: <code>{escape(logs)}</code></p>" if logs else "")
            + "".join(details) + "</div>")


def show_step(result, study=None, *, title=None, images=False, viewer=True):
    """Display the summary table, flags and commands of a step, then (with
    ``study``) the interactive viewer of its images."""
    display(HTML(step_html(result, title=title, images=images)))
    if viewer and study is not None and result.get("stage") in VIEWER_STAGES:
        from .step_viewer import show_step_viewer
        # Participants with published outputs (not those whose step was skipped).
        done = {(e["subject"], e.get("session")) for e in result.get("results", [])
                if any(o.get("path") for o in e.get("outputs", []))}
        entries = [e for e in (result.get("request") or {}).get("entries", [])
                   if (e["subject"], e.get("session")) in done]
        return show_step_viewer(result["stage"], entries, study)
    return None
