"""Independent selectors for existing atlas-overlap tables; no processing."""

import ipywidgets as widgets
import json
from html import escape

from .masks import MASK_LABELS
from .anatomy_labels import label_table

SOURCE_ORDER = ("synthstroke", "manual", "linda")


def ordered_sources(sources):
    return sorted(sources, key=lambda s: (SOURCE_ORDER.index(s) if s in SOURCE_ORDER else 99, s))


def overlap_table(df, subject, session, atlas, source, *, metric="lesion_in_roi_percent", limit=None):
    """Label the table with its exact inputs; distinguish total from displayed rows."""
    title = f"{atlas} — {MASK_LABELS.get(source, source)} mask — {subject} {session}".strip()
    df = label_table(df, atlas)
    selected = df[(df.subject == subject) & (df.session.fillna('') == (session or ""))].sort_values(metric, ascending=False)
    if selected.empty:
        status = df.attrs.get('overlap_status', {}).get(json.dumps([subject, session or '']), {})
        message = ('Mask unavailable for this participant and source.' if status.get('status') == 'missing_mask'
                   else 'Overlap calculated: no lesion voxels intersect this atlas’s labelled regions.'
                   if status.get('status') == 'complete' else
                   'No cached overlap rows. Run atlas overlap to distinguish zero overlap from missing results.')
        return f"<h3>{escape(title)}</h3><p>{message}</p>"
    shown = selected.head(limit) if limit is not None else selected
    cell = "style='padding:5px 10px;text-align:right;border-bottom:1px solid #8884'"
    rows = "".join(f"<tr><td style='padding:5px 10px;border-bottom:1px solid #8884'>{escape(str(r.region))}</td>"
                   f"<td {cell}>{escape(r.lesion_hemisphere)}</td>"
                   f"<td {cell}>{r.lesion_in_roi_percent:.1f}%</td>"
                   f"<td {cell}>{r.roi_coverage_percent:.1f}%</td><td {cell}>{int(r.overlap_voxels)}</td></tr>"
                   for r in shown.itertuples())
    return (f"<h3>{escape(title)}</h3><p><b>Total lesion volume:</b> "
            f"{int(selected.total_lesion_voxels.iloc[0])} voxels · <b>Regions overlapped:</b> {len(selected)}"
            f" · Showing {len(shown)} of {len(selected)}</p>"
            "<table class='calmar-overlap' style='border-collapse:collapse;font-size:13px'>"
            f"<caption>{escape(atlas)} atlas overlap · {escape(MASK_LABELS.get(source, source))}</caption>"
            f"<thead><tr><th {cell}>Region</th><th {cell}>Lesion side</th><th {cell}>Lesion in ROI</th>"
            f"<th {cell}>ROI coverage</th><th {cell}>Voxels</th></tr></thead>"
            f"<tbody>{rows}</tbody></table>"
            "<p>Lesion side is measured from intersecting mask voxels in MNI space. "
            "Bilateral includes left/right voxel counts; it does not describe the atlas region’s extent. "
            "Not calculated means the cached table needs an atlas-overlap refresh.</p>")


class OverlapSelection:
    """Keep atlas, mask, and subject selections valid as one UI transaction."""

    def __init__(self, tables, default_atlas=None, subject_pairs=None):
        self.subject_pairs = (sorted(subject_pairs) if isinstance(subject_pairs, set)
                              else list(subject_pairs)) if subject_pairs is not None else None
        self.tables = {}
        for key, original in tables.items():
            df = label_table(original, key.rsplit('_', 1)[0])
            df["session"] = df["session"].fillna("").astype(str)
            if subject_pairs is not None:
                df = df.loc[[pair in subject_pairs for pair in
                             zip(df["subject"], df["session"])], :]
            if not df.empty or self.subject_pairs:
                self.tables[key] = df
        self._callbacks = []
        self._busy = False
        atlases = sorted({key.rsplit("_", 1)[0] for key in self.tables})
        self.atlas = widgets.Dropdown(
            options=atlases, description="Atlas:",
            value=default_atlas if default_atlas in atlases else next(iter(atlases), None),
            layout=widgets.Layout(width="300px"))
        self.source = widgets.Dropdown(options=[], description="Mask:",
                                       layout=widgets.Layout(width="200px"))
        self.subject = widgets.Dropdown(options=[], description="Subject:",
                                        layout=widgets.Layout(width="300px"))
        self._refresh()
        self.atlas.observe(self._refresh, names="value")
        self.source.observe(self._refresh, names="value")
        self.subject.observe(self._subject_changed, names="value")
        self.widget = widgets.VBox([self.atlas, self.source, self.subject])

    def _refresh(self, change=None):
        if self._busy:
            return
        self._busy = True
        try:
            sources = ordered_sources({key.rsplit("_", 1)[1] for key in self.tables
                              if key.rsplit("_", 1)[0] == self.atlas.value})
            previous = self.source.value
            self.source.options = [(MASK_LABELS.get(s, s), s) for s in sources]
            self.source.value = previous if previous in sources else next(iter(sources), None)
            df = self.tables.get(f"{self.atlas.value}_{self.source.value}")
            pairs = (self.subject_pairs if self.subject_pairs is not None else
                     sorted(set(zip(df["subject"], df["session"]))) if df is not None else [])
            previous = self.subject.value
            self.subject.options = [(f"{sub} {ses}".strip(), (sub, ses)) for sub, ses in pairs]
            self.subject.value = previous if previous in pairs else next(iter(pairs), None)
        finally:
            self._busy = False
        self._emit(False)

    def _subject_changed(self, change):
        if not self._busy:
            self._emit(True)

    def _emit(self, subject_only):
        for callback in self._callbacks:
            callback(subject_only=subject_only)

    def observe(self, callback):
        self._callbacks.append(callback)

    def current(self):
        """Return the exact selected table and subject/session, or no selection."""
        df = self.tables.get(f"{self.atlas.value}_{self.source.value}")
        sub, ses = self.subject.value or ("", "")
        return df, sub, ses
