"""One concise visual review panel for each selected direct-dMRI result.

The reconstruction tools already write several overlapping figures.  This
module deliberately selects one representative preview per participant and
links to the complete preprocessing/reconstruction reports instead of
embedding them again.  The same renderer is used by the single-participant and
batch notebook paths.
"""

from __future__ import annotations

import base64
from io import BytesIO
from html import escape
from pathlib import Path

from IPython.display import HTML, display
from PIL import Image

from .diffusion import (DMRI_METHODS, DMRI_SUBDIR, dmri_method,
                        tensor_metrics_paths, tractometry_paths)
from .report_ui import file_link
from .study import config_for_entry, dataset_for_entry


INLINE_PREVIEW_LIMIT = 6


def _effective(study, entry):
    config = (study.config_for(entry) if hasattr(study, "config_for")
              else config_for_entry(study.config, entry))
    dataset = (study.dataset_for(entry) if hasattr(study, "dataset_for")
               else dataset_for_entry(study.dataset, entry))
    return config, Path(dataset)


def _root(study, entry):
    config, dataset = _effective(study, entry)
    return (dataset / config.get("DMRI_SUBDIR", DMRI_SUBDIR) /
            entry["subject"] / (entry.get("session") or "")), config, dataset


def _first(root, *patterns):
    for pattern in patterns:
        matches = sorted(root.rglob(pattern)) if root.is_dir() else []
        if matches:
            return matches[0]
    return None


def _thumbnail(path, maximum=(1000, 700)):
    """Small saved-notebook preview; never embed a 10–20 MB QSIRecon PNG."""
    try:
        with Image.open(path) as source:
            image = source.convert("RGB")
            image.thumbnail(maximum, Image.Resampling.LANCZOS)
            stream = BytesIO()
            image.save(stream, format="JPEG", quality=84, optimize=True)
        return base64.b64encode(stream.getvalue()).decode("ascii")
    except (OSError, ValueError):
        return None


def _artifact_item(study, entry):
    root, config, dataset = _root(study, entry)
    method = dmri_method(config)
    subject, session = entry["subject"], entry.get("session")
    stem = "_".join(filter(None, [subject, session]))
    qsiprep = root / "qsiprep" / f"{subject}.html"
    links = [(qsiprep, "QSIPrep report")] if qsiprep.is_file() else []

    if method == "dipy_dti":
        metrics, _ = tensor_metrics_paths(dataset, config, entry)
        preview = metrics.with_name(metrics.name.replace("_metrics.tsv", "_qc.png"))
        if preview.is_file():
            links.append((preview, "Full-size tensor QC"))
        if metrics.is_file():
            links.append((metrics, "Tensor metrics"))
        caption = ("FA and MD on the preprocessed b0 image. Review alignment, distortion and "
                   "unexpected spatial patterns before interpreting the summary values.")
    else:
        recon = root / "qsirecon"
        # SS3T is the selected reconstruction.  Do not also show the similar
        # GQI and ODF panels: one orientation preview is enough here.
        preview = _first(recon, "*desc-wmFOD_peaks.png", "*desc-GQIODF_peaks.png")
        report = _first(recon, f"{stem}.html")
        metrics, _ = tractometry_paths(dataset, config, entry)
        if report is not None:
            links.append((report, "Full QSIRecon report"))
        if metrics.is_file():
            links.append((metrics, "Tractometry table"))
        caption = ("Direction-coloured fibre-orientation peaks. This is an orientation QC view, "
                   "not streamline density or proof that a tract is intact or disconnected.")

    return {
        # Subject labels are only unique inside a dataset, and the same
        # participant can legitimately be reviewed under both reconstruction
        # methods during one kernel session.
        "key": (str(dataset.resolve()), subject, session, method),
        "subject": subject, "session": session,
        "method": method, "method_label": DMRI_METHODS[method],
        "preview": Path(preview) if preview is not None and Path(preview).is_file() else None,
        "caption": caption, "links": links,
    }


def _links(item):
    return " · ".join(file_link(path, label) for path, label in item["links"])


def _card(item):
    who = escape(" ".join(filter(None, [item["subject"], item["session"]])))
    image = _thumbnail(item["preview"]) if item["preview"] else None
    visual = (
        f'<img loading="lazy" src="data:image/jpeg;base64,{image}" '
        f'alt="{escape(item["method_label"])} visual QC for {who}" '
        'style="display:block;width:100%;max-height:430px;object-fit:contain;background:#111">'
        if image else
        '<div style="padding:28px;text-align:center;background:var(--jp-layout-color2);'
        'color:var(--jp-ui-font-color2)">No representative preview is available yet.</div>'
    )
    links = _links(item)
    return (
        '<article style="border:1px solid var(--jp-border-color2);border-radius:6px;overflow:hidden">'
        f'<div style="padding:8px 10px"><b>{who}</b><br><span style="font-size:12px">'
        f'{escape(item["method_label"])}</span></div>{visual}'
        f'<p style="margin:8px 10px;font-size:12px">{escape(item["caption"])}</p>'
        + (f'<p style="margin:8px 10px;font-size:12px">{links}</p>' if links else "") +
        '</article>')


def dmri_visual_html(entries, study, *, title="Diffusion visual review",
                     max_inline=INLINE_PREVIEW_LIMIT, already_shown=()):
    """Return one bounded visual panel and the participant keys it rendered."""
    items = [_artifact_item(study, entry) for entry in entries]
    prior = set(already_shown or ())
    available = [item for item in items if item["key"] not in prior]
    inline, remainder = available[:max_inline], available[max_inline:]
    cards = "".join(_card(item) for item in inline)
    html = (
        '<section class="calmar-dmri-visuals" style="font-family:sans-serif">'
        f'<h4 style="margin:12px 0 5px">{escape(title)}</h4>'
        '<p style="font-size:12px;margin-top:0">One selected-method preview per participant. '
        'The complete preprocessing and reconstruction reports are linked rather than repeated inline.</p>')
    if cards:
        html += ('<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(360px,1fr));'
                 'gap:12px">' + cards + '</div>')
    if prior:
        repeated = [item for item in items if item["key"] in prior]
        if repeated:
            html += ('<p style="font-size:12px"><b>Already reviewed above:</b> ' + "; ".join(
                escape(" ".join(filter(None, [item["subject"], item["session"]]))) +
                ((" · " + _links(item)) if item["links"] else "") for item in repeated) + '</p>')
    if remainder:
        rows = "".join(
            '<tr><td>' + escape(" ".join(filter(None, [item["subject"], item["session"]]))) +
            '</td><td>' + escape(item["method_label"]) + '</td><td>' + (_links(item) or "—") + '</td></tr>'
            for item in remainder)
        html += (f'<details><summary>{len(remainder)} more participant'
                 f'{"s" if len(remainder) != 1 else ""} — reports and metrics</summary>'
                 '<table><tr><th>Participant</th><th>Method</th><th>Open</th></tr>' + rows +
                 '</table></details>')
    if not cards and not prior and not remainder:
        html += '<p>No selected diffusion results are available for visual review.</p>'
    return html + '</section>', {item["key"] for item in inline}


def show_dmri_visuals(entries, study, **kwargs):
    """Display the shared single/group dMRI review and return shown keys."""
    html, shown = dmri_visual_html(entries, study, **kwargs)
    display(HTML(html))
    return shown
