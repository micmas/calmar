"""Optional OpenADS analysis of DWI discovered alongside a T1 workflow.

Discovery happens with participant selection.  This module makes the choice
explicit early, records the exact DWI/ADC pair, and prepares a separate acute
``Study`` for processing in the single-subject test and the later batch.
Nothing here performs image processing.
"""

from copy import deepcopy
from html import escape
import json
from pathlib import Path

import ipywidgets as w
from IPython import get_ipython
from IPython.display import display

from .execution import ExecutionCheckpoint
from .notebook_navigation import NotebookNavigation
from .study import ENTRY_CONFIG, ENTRY_DATASET, Study, config_for_entry, modality
from .widget_lifecycle import close_widget


_MISSING = object()


def openads_options(entry):
    """OpenADS-ready inventory records, same-session first then by session/path."""
    ready = []
    for item in entry.get("dwi_inventory", ()):
        if not item.get("openads_ready") or not item.get("adc"):
            continue
        item = dict(item)
        item["anatomical_session"] = entry.get("session")
        for key in (ENTRY_DATASET, ENTRY_CONFIG):
            if key in entry:
                item[key] = entry[key]
        ready.append(item)
    return sorted(ready, key=lambda item: (
        not bool(item.get("same_session")), item.get("session") or "", str(item.get("dwi") or "")))


def dwi_entry(item, anatomical_session=_MISSING):
    """Convert one inventory item into the processing entry OpenADS expects."""
    if anatomical_session is _MISSING:
        anatomical_session = item.get("anatomical_session", _MISSING)
    entry = {**item, "t1w": item["dwi"], "modality": "dwi"}
    if anatomical_session is not _MISSING:
        entry["anatomical_session"] = anatomical_session
    if ENTRY_CONFIG in entry:
        entry[ENTRY_CONFIG] = {**entry[ENTRY_CONFIG], "MODALITY": "dwi",
                               "SEGMENTATION_METHODS": ["openads"]}
    return entry


def apply_dwi_selection(namespace, selected):
    """Record selected pairs and expose the optional OpenADS route."""
    sessions_by_subject = {}
    for entry in namespace.get("SUBJECTS", ()):
        sessions_by_subject.setdefault(entry["subject"], []).append(entry.get("session"))
    processing = {}
    for key, item in selected.items():
        subject = key[0] if isinstance(key, tuple) else key
        known_session = False
        if isinstance(key, tuple):
            anatomical_session = key[1]
            known_session = True
        elif "anatomical_session" in item:
            anatomical_session = item["anatomical_session"]
            known_session = True
        elif len(sessions_by_subject.get(subject, ())) == 1:
            anatomical_session = sessions_by_subject[subject][0]
            known_session = True
        if not known_session:
            raise ValueError(f"DWI selection for {subject} is not linked to a unique anatomical session.")
        processing[(subject, anatomical_session)] = dwi_entry(item, anatomical_session)
    subjects = []
    for entry in namespace.get("SUBJECTS", ()):
        copied = dict(entry)
        copied.pop("dwi_analysis", None)
        chosen = processing.get((entry["subject"], entry.get("session")))
        if chosen is not None:
            copied["dwi_analysis"] = chosen
        subjects.append(copied)

    config = namespace["CONFIG"]
    # ANALYSE_DWI is the user's configured policy (None asks, True selects,
    # False skips). Keep the interactive answer separate so rerunning this
    # cell cannot silently turn a partial selection into "select all".
    config["_DWI_ANALYSIS_SELECTED"] = bool(processing)
    dwi_config = deepcopy(config)
    dwi_config.update(MODALITY="dwi", SEGMENTATION_METHODS=["openads"])
    # A manually configured T1-space mask must not silently be treated as a
    # DWI-space mask. Dataset-native masks can still be discovered normally.
    dwi_config.update(MANUAL_MASK_PATH=None, MANUAL_MASK_REF=None)
    dwi_subjects = list(processing.values())
    namespace.update(SUBJECTS=subjects, DWI_SUBJECTS=dwi_subjects, DWI_CONFIG=dwi_config,
                     DWI_STUDY=Study(dwi_config, namespace["RAW_DATASET_DIR"], namespace["PROJECT_DIR"]))

    record = {
        "analyse_dwi": bool(selected),
        "selection": [{"subject": e["subject"], "session": e.get("session"),
                       "anatomical_session": e.get("anatomical_session"),
                       "dwi": str(e["dwi"]), "adc": str(e["adc"])} for e in dwi_subjects],
    }
    path = Path(namespace["PROJECT_DIR"]) / "reports" / "dwi-selection.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return dwi_subjects


class DWIChoice(w.VBox):
    """Early opt-in panel for optional DWI processing."""

    def __init__(self, namespace, shell):
        self.namespace = namespace
        config = namespace["CONFIG"]
        self.entries = [dict(e) for e in namespace["SUBJECTS"]
                        if modality(config_for_entry(config, e)) == "t1"]
        self.checkpoint = ExecutionCheckpoint(
            shell, "Execution is paused for the optional DWI decision. Choose analyse or continue without DWI.")
        self.message = w.HTML()
        self.navigation = NotebookNavigation(self.message, on_cell_order=self.checkpoint._update_cell_order)
        self.rows = []
        children = [w.HTML(
            "<h3>Optional DWI analysis</h3><p>OpenADS-ready DWI+ADC data were found for the selected "
            "participant(s). Choose which pairs to analyse. The selected test participant is processed in "
            "the single-subject check; remaining pairs are processed after the ordinary QC.</p><p>A pair from another session is "
            "allowed and stays labelled with its own session. This can be useful in chronic stroke, but DWI "
            "contrast changes over time: CALMaR registers and QC-checks it independently and does not assume "
            "that signal or lesion boundaries are identical across sessions.</p>")]
        for entry in self.entries:
            options = openads_options(entry)
            if not options:
                continue
            include = w.Checkbox(value=True, description=f"Analyse {entry['subject']}", indent=False,
                                 layout=w.Layout(width="220px"))
            choices = []
            for i, item in enumerate(options):
                relation = "same session" if item.get("same_session") else "different session"
                label = f"{item.get('session') or '(no session)'} · {relation} · {Path(item['dwi']).name}"
                choices.append((label, i))
            pair = w.Dropdown(options=choices, value=0, description="DWI + ADC:",
                              style={"description_width": "initial"}, layout=w.Layout(width="680px"))
            self.rows.append((entry, options, include, pair))
            children.append(w.HBox([include, pair], layout=w.Layout(flex_flow="row wrap")))
        self.analyse = w.Button(description="Analyse selected DWI", button_style="primary",
                                layout=w.Layout(width="250px"))
        self.skip = w.Button(description="Continue without DWI", layout=w.Layout(width="210px"))
        self.analyse.on_click(lambda _: self._request(True))
        self.skip.on_click(lambda _: self._request(False))
        children.extend([w.HBox([self.analyse, self.skip]), self.message, self.navigation])
        super().__init__(children)
        # The panel closes itself after releasing this checkpoint.  Registering
        # the panel as one of the checkpoint's controls makes close() recurse
        # through ExecutionCheckpoint.close().
        self.checkpoint.controls = []
        self.checkpoint._cancel_queued()

    def _selection(self):
        return {(entry["subject"], entry.get("session")): options[pair.value]
                for entry, options, include, pair in self.rows if include.value}

    def _request(self, analyse):
        # Directional dMRI is a separate decision in the next cell. It decides
        # whether to continue to the single-test selection after its own choice.
        self.navigation.request("dmri-choice", lambda: self._apply(analyse), all_below=True)

    def _apply(self, analyse):
        selected = self._selection() if analyse else {}
        if analyse and not selected:
            self.message.value = "Select at least one participant, or choose Continue without DWI."
            return False
        apply_dwi_selection(self.namespace, selected)
        self.checkpoint.release()
        self.analyse.disabled = self.skip.disabled = True
        for _, _, include, pair in self.rows:
            include.disabled = pair.disabled = True
        if selected:
            sessions = ", ".join((f"{key[0] if isinstance(key, tuple) else key} "
                                  f"{item.get('session') or ''}").strip()
                                 for key, item in selected.items())
            self.message.value = ("<b>DWI analysis selected:</b> " + escape(sessions)
                                  + ". The test participant will run in the single-subject check.")
        else:
            self.message.value = "<b>DWI analysis declined.</b> Continuing with the T1 workflow."
        return True

    def close(self):
        checkpoint = getattr(self, "checkpoint", None)
        if checkpoint is not None:
            checkpoint.close()
        for child in getattr(self, "children", ()):
            close_widget(child)
        super().close()


def show_dwi_choice(namespace, shell=None):
    """Show the optional-DWI choice, or continue with an explicit status line."""
    config = namespace["CONFIG"]
    if modality(config) == "dwi":
        namespace["DWI_SUBJECTS"] = []
        print("DWI is the primary imaging route; OpenADS will run in the ordinary DWI cells.")
        return None
    t1_entries = [entry for entry in namespace.get("SUBJECTS", ())
                  if modality(config_for_entry(config, entry)) == "t1"]
    available = {(entry["subject"], entry.get("session")): openads_options(entry)
                 for entry in t1_entries}
    available = {key: options for key, options in available.items() if options}
    if not available:
        apply_dwi_selection(namespace, {})
        has_dwi = any(entry.get("dwi_inventory") for entry in t1_entries)
        if has_dwi:
            print("DWI was detected, but optional OpenADS analysis is unavailable: no DWI has a matching ADC map.")
        else:
            print("DWI is unavailable for the selected participant(s); continuing with the T1 workflow.")
        return None
    configured = config.get("ANALYSE_DWI")
    if configured is not None:
        selected = ({key: options[0] for key, options in available.items()} if configured else {})
        apply_dwi_selection(namespace, selected)
        print((f"Optional DWI analysis selected for {len(selected)} participant(s); the test participant "
               "will run in the single-subject check."
               if selected else "Optional DWI analysis disabled in CONFIG."))
        return None
    shell = shell or get_ipython()
    if shell is None:
        raise RuntimeError("The optional DWI choice requires an IPython notebook kernel.")
    previous = getattr(shell, "_calmar_dwi_choice", None)
    if previous is not None:
        previous.close()
    panel = DWIChoice(namespace, shell)
    shell._calmar_dwi_choice = panel
    display(panel)
    return panel
