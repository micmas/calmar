"""Optional OpenADS analysis of DWI discovered alongside a T1 workflow.

Discovery happens with participant selection.  This module makes the choice
explicit early, records the exact DWI/ADC pair, and prepares a separate acute
``Study`` for processing after the ordinary T1/manual-mask QC checkpoint.
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
from .study import Study, modality
from .widget_lifecycle import close_widget


def openads_options(entry):
    """OpenADS-ready inventory records, same-session first then by session/path."""
    ready = [dict(item) for item in entry.get("dwi_inventory", ())
             if item.get("openads_ready") and item.get("adc")]
    return sorted(ready, key=lambda item: (
        not bool(item.get("same_session")), item.get("session") or "", str(item.get("dwi") or "")))


def dwi_entry(item):
    """Convert one inventory item into the processing entry OpenADS expects."""
    return {**item, "t1w": item["dwi"], "modality": "dwi"}


def apply_dwi_selection(namespace, selected):
    """Record selected pairs and expose the separate post-QC OpenADS route."""
    selected = {subject: dwi_entry(item) for subject, item in selected.items()}
    subjects = []
    for entry in namespace.get("SUBJECTS", ()):
        copied = dict(entry)
        copied.pop("dwi_analysis", None)
        if entry["subject"] in selected:
            copied["dwi_analysis"] = selected[entry["subject"]]
        subjects.append(copied)

    config = namespace["CONFIG"]
    # ANALYSE_DWI is the user's configured policy (None asks, True selects,
    # False skips). Keep the interactive answer separate so rerunning this
    # cell cannot silently turn a partial selection into "select all".
    config["_DWI_ANALYSIS_SELECTED"] = bool(selected)
    dwi_config = deepcopy(config)
    dwi_config.update(MODALITY="dwi", SEGMENTATION_METHODS=["openads"])
    # A manually configured T1-space mask must not silently be treated as a
    # DWI-space mask. Dataset-native masks can still be discovered normally.
    dwi_config.update(MANUAL_MASK_PATH=None, MANUAL_MASK_REF=None)
    dwi_subjects = list(selected.values())
    namespace.update(SUBJECTS=subjects, DWI_SUBJECTS=dwi_subjects, DWI_CONFIG=dwi_config,
                     DWI_STUDY=Study(dwi_config, namespace["RAW_DATASET_DIR"], namespace["PROJECT_DIR"]))

    record = {
        "analyse_dwi": bool(selected),
        "selection": [{"subject": e["subject"], "session": e.get("session"),
                       "dwi": str(e["dwi"]), "adc": str(e["adc"])} for e in dwi_subjects],
    }
    path = Path(namespace["PROJECT_DIR"]) / "reports" / "dwi-selection.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return dwi_subjects


class DWIChoice(w.VBox):
    """Early opt-in panel for DWI that will be processed only after T1 QC."""

    def __init__(self, namespace, shell):
        self.namespace = namespace
        self.entries = [dict(e) for e in namespace["SUBJECTS"]]
        self.checkpoint = ExecutionCheckpoint(
            shell, "Execution is paused for the optional DWI decision. Choose analyse or continue without DWI.")
        self.message = w.HTML()
        self.navigation = NotebookNavigation(self.message, on_cell_order=self.checkpoint._update_cell_order)
        self.rows = []
        children = [w.HTML(
            "<h3>Optional DWI analysis</h3><p>OpenADS-ready DWI+ADC data were found for the selected "
            "participant(s). Choose which pairs to analyse. The choice is made now; processing starts only "
            "after the ordinary T1 and manual-mask registration QC.</p><p>A pair from another session is "
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
        self.analyse = w.Button(description="Analyse selected DWI after QC", button_style="primary",
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
        return {entry["subject"]: options[pair.value]
                for entry, options, include, pair in self.rows if include.value}

    def _request(self, analyse):
        # With RUN_TEST false, running below must continue into the batch cell.
        # With RUN_TEST true, the next checkpoint still provides the pause.
        self.navigation.request("single-test-selection", lambda: self._apply(analyse), all_below=True)

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
            sessions = ", ".join(f"{subject} {item.get('session') or ''}".strip()
                                 for subject, item in selected.items())
            self.message.value = ("<b>DWI analysis selected:</b> " + escape(sessions)
                                  + ". It will run after T1/manual-mask QC.")
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
        namespace.setdefault("DWI_SUBJECTS", [])
        print("DWI is the primary imaging route; OpenADS will run in the ordinary DWI cells.")
        return None
    available = {entry["subject"]: openads_options(entry) for entry in namespace.get("SUBJECTS", ())}
    available = {subject: options for subject, options in available.items() if options}
    if not available:
        apply_dwi_selection(namespace, {})
        has_dwi = any(entry.get("dwi_inventory") for entry in namespace.get("SUBJECTS", ()))
        if has_dwi:
            print("DWI was detected, but optional OpenADS analysis is unavailable: no DWI has a matching ADC map.")
        else:
            print("DWI is unavailable for the selected participant(s); continuing with the T1 workflow.")
        return None
    configured = config.get("ANALYSE_DWI")
    if configured is not None:
        selected = ({subject: options[0] for subject, options in available.items()} if configured else {})
        apply_dwi_selection(namespace, selected)
        print((f"Optional DWI analysis selected for {len(selected)} participant(s); it will run after T1 QC."
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
