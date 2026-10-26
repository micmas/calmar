"""Opt-in notebook choice for structural brain-health analysis."""

from copy import deepcopy
from html import escape
import json
from pathlib import Path

import ipywidgets as w
from IPython import get_ipython
from IPython.display import display

from .brain_health import brain_health_inventory
from .execution import ExecutionCheckpoint
from .notebook_navigation import NotebookNavigation
from .study import ENTRY_CONFIG, ENTRY_DATASET
from .widget_lifecycle import close_widget


def _selected_entry(entry, inventory, components):
    selected = deepcopy(entry)
    selected["brain_health_components"] = list(components)
    selected["flair"] = inventory.get("flair")
    selected["anatomical_t1w"] = inventory.get("t1w")
    return selected


def apply_brain_health_selection(namespace, selected):
    """Attach compact report metadata and retain processing entries."""
    processing = {key: _selected_entry(entry, inventory, components)
                  for key, (entry, inventory, components) in selected.items()}
    subjects = []
    for entry in namespace.get("SUBJECTS", ()):
        copied = dict(entry)
        copied.pop("brain_health_analysis", None)
        chosen = processing.get((entry["subject"], entry.get("session")))
        if chosen is not None:
            copied["brain_health_analysis"] = {
                "subject": chosen["subject"], "session": chosen.get("session"),
                "components": list(chosen["brain_health_components"]),
                "flair": chosen.get("flair"),
            }
            for key in (ENTRY_DATASET, ENTRY_CONFIG):
                if key in chosen:
                    copied["brain_health_analysis"][key] = chosen[key]
        subjects.append(copied)
    namespace["SUBJECTS"] = subjects
    namespace["BRAIN_HEALTH_SUBJECTS"] = list(processing.values())
    namespace["CONFIG"]["_BRAIN_HEALTH_SELECTED"] = bool(processing)
    record = {
        "analyse_brain_health": bool(processing),
        "selection": [{
            "subject": item["subject"], "session": item.get("session"),
            "components": item["brain_health_components"], "t1w": item.get("anatomical_t1w"),
            "flair": item.get("flair"),
        } for item in processing.values()],
    }
    path = Path(namespace["PROJECT_DIR"]) / "reports" / "brain-health-selection.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=2, default=str) + "\n", encoding="utf-8")
    return list(processing.values())


def available_entries(namespace):
    found = {}
    for entry in namespace.get("SUBJECTS", ()):
        inventory = brain_health_inventory(namespace["CONFIG"], namespace["RAW_DATASET_DIR"], entry)
        components = []
        if inventory["atrophy_available"]:
            components.append("atrophy")
        if inventory["wmh_available"]:
            components.append("wmh")
        if components:
            found[(entry["subject"], entry.get("session"))] = (entry, inventory, components)
    return found


class BrainHealthChoice(w.VBox):
    def __init__(self, namespace, shell):
        self.namespace = namespace
        self.checkpoint = ExecutionCheckpoint(shell, "Execution is paused for the optional brain-health decision.")
        self.message = w.HTML()
        self.navigation = NotebookNavigation(self.message, on_cell_order=self.checkpoint._update_cell_order)
        self.rows = []
        children = [w.HTML(
            "<h3>Optional structural brain health</h3>"
            "<p>Analyse T1-derived atrophy-sensitive volumes and, where same-session FLAIR exists, white-matter "
            "hyperintensity burden. These measurements remain separate from the focal stroke interpretation.</p>"
            "<p>A single scan cannot diagnose atrophy. Stroke cavities and acute FLAIR lesion signal can bias both "
            "analyses, so CALMaR reports lesion-adjusted values, preserves the raw burden and requires visual QC.</p>")]
        for key, (entry, inventory, components) in available_entries(namespace).items():
            subject, session = key
            include = w.Checkbox(value=False, description=f"Analyse {subject}", indent=False,
                                 layout=w.Layout(width="230px"))
            options = []
            if "atrophy" in components:
                options.append("T1 volumetry")
            if "wmh" in components:
                options.append("FLAIR WMH candidates")
            detail = w.HTML("<span style='color:#555'>" + escape(" + ".join(options)) + "</span>")
            flair_options = inventory.get("flair_candidates") or []
            flair_choice = None
            if len(flair_options) > 1:
                flair_choice = w.Dropdown(
                    options=[(Path(path).name, path) for path in flair_options], value=inventory.get("flair"),
                    description="FLAIR:", style={"description_width": "initial"},
                    layout=w.Layout(width="520px"))
            self.rows.append((entry, inventory, components, include, flair_choice))
            children.append(w.HBox([item for item in (include, detail, flair_choice) if item is not None],
                                   layout=w.Layout(flex_flow="row wrap")))
        self.analyse = w.Button(description="Analyse selected brain health", button_style="primary",
                                layout=w.Layout(width="270px"))
        self.skip = w.Button(description="Continue without brain health", layout=w.Layout(width="250px"))
        self.analyse.on_click(lambda _: self._request(True))
        self.skip.on_click(lambda _: self._request(False))
        children.extend([w.HBox([self.analyse, self.skip]), self.message, self.navigation])
        super().__init__(children)
        self.checkpoint.controls = []
        self.checkpoint._cancel_queued()

    def _selection(self):
        selected = {}
        for entry, inventory, components, include, flair_choice in self.rows:
            if not include.value:
                continue
            chosen = dict(inventory)
            if flair_choice is not None:
                chosen["flair"] = flair_choice.value
            selected[(entry["subject"], entry.get("session"))] = (entry, chosen, components)
        return selected

    def _request(self, analyse):
        self.navigation.request("single-test-selection", lambda: self._apply(analyse), all_below=True)

    def _apply(self, analyse):
        selected = self._selection() if analyse else {}
        if analyse and not selected:
            self.message.value = "Select at least one participant, or continue without brain-health analysis."
            return False
        apply_brain_health_selection(self.namespace, selected)
        self.checkpoint.release()
        self.analyse.disabled = self.skip.disabled = True
        for _, _, _, include, flair_choice in self.rows:
            include.disabled = True
            if flair_choice is not None:
                flair_choice.disabled = True
        if selected:
            labels = [f"{subject} {session or ''}".strip() for subject, session in selected]
            self.message.value = "<b>Brain-health analysis selected:</b> " + escape(", ".join(labels)) + "."
        else:
            self.message.value = "<b>Brain-health analysis declined.</b>"
        return True

    def close(self):
        checkpoint = getattr(self, "checkpoint", None)
        if checkpoint is not None:
            checkpoint.close()
        for child in getattr(self, "children", ()):
            close_widget(child)
        super().close()


def show_brain_health_choice(namespace, shell=None):
    available = available_entries(namespace)
    if not available:
        apply_brain_health_selection(namespace, {})
        print("No eligible T1w or same-session FLAIR is available; continuing without brain-health analysis.")
        return None
    configured = namespace["CONFIG"].get("ANALYSE_BRAIN_HEALTH")
    if configured is not None:
        selected = available if configured else {}
        apply_brain_health_selection(namespace, selected)
        print((f"Brain-health analysis selected for {len(selected)} participant(s)."
               if selected else "Brain-health analysis disabled in CONFIG."))
        return None
    shell = shell or get_ipython()
    if shell is None:
        raise RuntimeError("The brain-health choice requires an IPython notebook kernel.")
    previous = getattr(shell, "_calmar_brain_health_choice", None)
    if previous is not None:
        previous.close()
    panel = BrainHealthChoice(namespace, shell)
    shell._calmar_brain_health_choice = panel
    display(panel)
    return panel
