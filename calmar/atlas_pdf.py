"""PDF export of one participant's lesion–atlas overlap table.

Used by the "Export selected atlas PDF" button inside the atlas-results preview.
The PDF has a summary page (lesion size, number of regions, QC checkpoint
status and a bar chart of the 20 regions holding most of the lesion) followed
by the full region table.

Numbers come straight from the overlap table (``calmar.atlas_overlap``):
``lesion_in_roi_percent`` = % of lesion voxels inside the ROI,
``roi_coverage_percent`` = % of ROI voxels covered by lesion,
``overlap_voxels`` = voxels in both. No image is read here.
"""
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

#: Rows of the region table per PDF page.
ROWS_PER_PAGE = 35
#: Regions shown in the summary bar chart.
TOP_REGIONS = 20

CAVEAT = ("Research use only; not a diagnosis. Lesion masks are on FSL MNI152; overlaps with small or "
          "thin regions depend on the individual registration.")


def write_atlas_pdf(subject, session, df, atlas_name, mask_source="selected", *,
                    pdf_dir, atlas_dir=None, qc_text=""):
    """Write ``<pdf_dir>/<sub>_<ses>_<atlas>_<source>.pdf``; return its path or None.

    ``df`` is an overlap table that may hold several participants; only rows of
    ``subject``/``session`` are used. ``qc_text`` is printed on the summary page
    (e.g. :func:`calmar.qc_decisions.report_qc_text`).
    """
    from .anatomy_labels import label_table
    df = label_table(df, atlas_name, atlas_dir)
    df["session"] = df["session"].fillna("").astype(str)
    sel = df[(df["subject"] == subject) & (df["session"] == (session or ""))].copy()
    if sel.empty:
        print(f"  no data for {subject} {session} ({atlas_name})")
        return None
    sel = sel.sort_values("lesion_in_roi_percent", ascending=False)
    total = int(sel["total_lesion_voxels"].iloc[0])
    pdf_dir = Path(pdf_dir)
    pdf_dir.mkdir(parents=True, exist_ok=True)
    fname = pdf_dir / f"{subject}_{session or 'no-ses'}_{atlas_name}_{mask_source}.pdf"

    with PdfPages(str(fname)) as pdf:
        # Page 1 — summary + bar chart
        fig = plt.figure(figsize=(8.5, 11))
        plt.suptitle(f"Lesion report  —  {subject} {session or ''}  ({atlas_name}, {mask_source} mask)",
                     fontsize=14, fontweight="bold")
        ax_meta = fig.add_axes([0.08, 0.76, 0.84, 0.14]); ax_meta.axis("off")
        ax_meta.text(0, 0.7,
                     f"Date: {datetime.now():%Y-%m-%d %H:%M}\n"
                     f"Total lesion volume: {total} voxels\n"
                     f"Regions affected: {len(sel)}\n" + qc_text,
                     family="monospace", fontsize=10)
        ax_meta.text(0, 0.0, CAVEAT, fontsize=7, wrap=True, color="#555555")
        ax_bar = fig.add_axes([0.08, 0.08, 0.84, 0.62])
        top = sel.head(TOP_REGIONS)
        ax_bar.barh(top["region"][::-1], top["lesion_in_roi_percent"][::-1])
        ax_bar.set_xlabel("% of lesion in ROI")
        ax_bar.set_title(f"Top {len(top)} affected regions")
        pdf.savefig(fig); plt.close(fig)

        # Subsequent pages — full table
        for start in range(0, len(sel), ROWS_PER_PAGE):
            chunk = sel.iloc[start:start + ROWS_PER_PAGE]
            fig = plt.figure(figsize=(8.5, 11))
            plt.suptitle(f"All regions  —  rows {start + 1}-{start + len(chunk)} of {len(sel)}", fontsize=11)
            ax = fig.add_axes([0.05, 0.05, 0.9, 0.85]); ax.axis("off")
            text = (f"{'Rank':<5s}{'Region':<31s}{'Lesion side':<17s}"
                    f"{'Lesion%':>10s}{'ROI%':>8s}{'vox':>8s}\n" + "-" * 79 + "\n")
            for i, row in enumerate(chunk.itertuples(), start + 1):
                side = row.lesion_hemisphere.split(" (")[0]
                text += (f"{i:<5d}{row.region[:29]:<31s}{side:<17s}"
                         f"{row.lesion_in_roi_percent:>9.1f}%"
                         f"{row.roi_coverage_percent:>7.1f}%"
                         f"{int(row.overlap_voxels):>8d}\n")
            text += "\nLesion side comes from intersecting mask voxels in MNI space."
            ax.text(0, 1, text, family="monospace", fontsize=8, verticalalignment="top")
            pdf.savefig(fig); plt.close(fig)
    print(f"  ✓ {fname}")
    return fname


def attach_pdf_export(panel, pdf_dir, *, atlas_dir, deriv_path_for):
    """Add an export button to the atlas-results preview ``panel``.

    The button exports exactly the participant, atlas and mask currently
    selected in the preview. ``deriv_path_for(entry)`` locates the folder
    holding ``QC_decision.json`` for the QC line. Returns the button, or None
    when there is no preview panel.
    """
    import ipywidgets as widgets
    from .qc_decisions import report_qc_text
    from .report_ui import file_link
    if not panel:
        return None
    button = widgets.Button(description="Export selected atlas PDF", button_style="primary",
                            layout=widgets.Layout(width="250px"))
    status = widgets.HTML()

    def export(_):
        selection = panel["selection"]
        df, subject, session = selection.current()
        entry = dict(subject=subject, session=session)
        button.disabled = True
        try:
            path = write_atlas_pdf(subject, session, df, selection.atlas.value, selection.source.value,
                                   pdf_dir=pdf_dir, atlas_dir=atlas_dir,
                                   qc_text=report_qc_text(deriv_path_for(entry), entry))
            status.value = file_link(path, "Download selected atlas PDF") if path else "No rows for the selected report."
        finally:
            button.disabled = False

    button.on_click(export)
    panel["export"].children = (button, status)
    return button
