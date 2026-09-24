"""Independent selectors for existing atlas-overlap tables; no processing."""

import ipywidgets as widgets

from calmar_masks import MASK_LABELS


class OverlapSelection:
    """Keep atlas, mask, and subject selections valid as one UI transaction."""

    def __init__(self, tables, default_atlas=None, subject_pairs=None):
        self.tables = {}
        for key, original in tables.items():
            df = original.copy()
            df["session"] = df["session"].fillna("").astype(str)
            if subject_pairs is not None:
                df = df[[pair in subject_pairs for pair in
                         zip(df["subject"], df["session"])]]
            if not df.empty:
                self.tables[key] = df
        self._callbacks = []
        self._busy = False
        atlases = sorted({key.rsplit("_", 1)[0] for key in self.tables})
        self.atlas = widgets.Dropdown(
            options=atlases, description="Atlas:",
            value=default_atlas if default_atlas in atlases else next(iter(atlases), None),
            layout=widgets.Layout(width="260px"))
        self.source = widgets.Dropdown(options=[], description="Mask:",
                                       layout=widgets.Layout(width="200px"))
        self.subject = widgets.Dropdown(options=[], description="Subject:",
                                        layout=widgets.Layout(width="300px"))
        self._refresh()
        self.atlas.observe(self._refresh, names="value")
        self.source.observe(self._refresh, names="value")
        self.subject.observe(self._subject_changed, names="value")
        self.widget = widgets.HBox([self.atlas, self.source, self.subject])

    def _refresh(self, change=None):
        if self._busy:
            return
        self._busy = True
        try:
            sources = sorted({key.rsplit("_", 1)[1] for key in self.tables
                              if key.rsplit("_", 1)[0] == self.atlas.value})
            previous = self.source.value
            self.source.options = [(MASK_LABELS.get(s, s), s) for s in sources]
            self.source.value = previous if previous in sources else next(iter(sources), None)
            df = self.tables.get(f"{self.atlas.value}_{self.source.value}")
            pairs = sorted(set(zip(df["subject"], df["session"]))) if df is not None else []
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
