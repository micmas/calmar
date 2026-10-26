"""Early opt-in choice for direct analysis of directional diffusion MRI."""

from copy import deepcopy
from html import escape
import json
from pathlib import Path

import ipywidgets as w
from IPython import get_ipython
from IPython.display import display

from .diffusion import assess_dwi_sessions
from .execution import ExecutionCheckpoint
from .notebook_navigation import NotebookNavigation
from .study import ENTRY_CONFIG, ENTRY_DATASET, Study, config_for_entry, modality
from .widget_lifecycle import close_widget


def dmri_options(entry):
    """Report-ready directional-dMRI sessions for one participant."""
    return assess_dwi_sessions(entry)


def _has_anatomical_t1(config, entry):
    """The current direct-dMRI pipeline requires a genuine T1-route anatomy."""
    return modality(config_for_entry(config, entry)) == "t1"


def _processing_entry(entry, option):
    """Combine the anatomical entry with one explicit diffusion session."""
    primary = option["primary"]
    selected = {key: value for key, value in entry.items() if key != "dwi_inventory"}
    selected.update({
        "session": option["session"], "dwi": primary["dwi"],
        "bval": primary["bval"], "bvec": primary["bvec"], "json": primary["json"],
        "dwi_series": [item["dwi"] for item in option["series"]],
        "dmri_assessment": option,
        "anatomical_session": entry.get("session"),
        "anatomical_t1w": entry.get("t1w"),
    })
    # Keep t1w as the participant anatomy; preprocessing needs it and must not
    # accidentally treat the first DWI volume as an anatomical reference.
    return selected


def apply_dmri_selection(namespace, selected):
    """Record direct-dMRI choices without changing the OpenADS selection."""
    processing = {subject: _processing_entry(entry, option)
                  for subject, (entry, option) in selected.items()}
    subjects = []
    for entry in namespace.get("SUBJECTS", ()):
        copied = dict(entry)
        copied.pop("dmri_analysis", None)
        if entry["subject"] in processing:
            # Report linkage is deliberately compact and JSON-serializable.
            chosen = processing[entry["subject"]]
            copied["dmri_analysis"] = {
                key: chosen.get(key) for key in
                ("subject", "session", "dwi", "bval", "bvec", "json",
                 "n_directions", "shells") if chosen.get(key) is not None
            }
            copied["dmri_analysis"].update(
                n_directions=chosen["dmri_assessment"]["n_directions"],
                shells=chosen["dmri_assessment"]["shells"])
            for key in (ENTRY_DATASET, ENTRY_CONFIG):
                if key in chosen:
                    copied["dmri_analysis"][key] = chosen[key]
        subjects.append(copied)

    config = namespace["CONFIG"]
    config["_TRACT_DWI_SELECTED"] = bool(processing)
    dmri_config = deepcopy(config)
    dmri_config.update(MODALITY="t1")
    entries = list(processing.values())
    namespace.update(
        SUBJECTS=subjects, DMRI_SUBJECTS=entries, DMRI_CONFIG=dmri_config,
        DMRI_STUDY=Study(dmri_config, namespace["RAW_DATASET_DIR"], namespace["PROJECT_DIR"]))
    record = {
        "analyse_directional_dwi": bool(entries),
        "selection": [{
            "subject": item["subject"], "session": item.get("session"),
            "dwi": str(item["dwi"]),
            "n_directions": item["dmri_assessment"]["n_directions"],
            "shells": item["dmri_assessment"]["shells"],
            "has_reverse_phase": item["dmri_assessment"]["has_reverse_phase"],
            "warnings": item["dmri_assessment"]["warnings"],
        } for item in entries],
    }
    path = Path(namespace["PROJECT_DIR"]) / "reports" / "dmri-selection.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=2, default=str) + "\n", encoding="utf-8")
    return entries


class DMRIChoice(w.VBox):
    """Opt-in panel kept separate from the trace-DWI/ADC OpenADS decision."""

    def __init__(self, namespace, shell):
        self.namespace = namespace
        self.checkpoint = ExecutionCheckpoint(
            shell, "Execution is paused for the optional directional-dMRI decision.")
        self.message = w.HTML()
        self.navigation = NotebookNavigation(self.message, on_cell_order=self.checkpoint._update_cell_order)
        self.rows = []
        children = [w.HTML(
            "<h3>Optional direct diffusion / tract analysis</h3>"
            "<p>Gradient-bearing 4-D diffusion MRI was found. This is separate from OpenADS: it preprocesses "
            "the diffusion series and can measure participant-specific tract microstructure. The report keeps "
            "these measurements separate from BCB/DeepDisco normative disconnectome predictions.</p>"
            "<p>Stroke lesions can distort registration and cause tractography to stop. CALMaR therefore reports "
            "lesion overlap and diffusion QC, and never treats a missing reconstructed tract as proof of "
            "disconnection.</p>")]
        for entry in namespace.get("SUBJECTS", ()):
            if not _has_anatomical_t1(namespace["CONFIG"], entry):
                continue
            options = dmri_options(entry)
            if not options:
                continue
            include = w.Checkbox(value=False, description=f"Analyse {entry['subject']}", indent=False,
                                 layout=w.Layout(width="220px"))
            choices = []
            for index, option in enumerate(options):
                relation = "same session" if option["same_session"] else "different session"
                reverse = "opposite-PE pair" if option["has_reverse_phase"] else "single PE"
                shells = "/".join(map(str, option["shells"]))
                label = (f"{option['session'] or '(no session)'} · {relation} · "
                         f"{option['n_directions']} distinct directions · b={shells} · {reverse}")
                choices.append((label, index))
            choice = w.Dropdown(options=choices, value=0, description="Diffusion session:",
                                style={"description_width": "initial"}, layout=w.Layout(width="760px"))
            self.rows.append((entry, options, include, choice))
            children.append(w.HBox([include, choice], layout=w.Layout(flex_flow="row wrap")))
        self.analyse = w.Button(description="Analyse selected directional DWI", button_style="primary",
                                layout=w.Layout(width="270px"))
        self.skip = w.Button(description="Continue without direct dMRI", layout=w.Layout(width="240px"))
        self.analyse.on_click(lambda _: self._request(True))
        self.skip.on_click(lambda _: self._request(False))
        children.extend([w.HBox([self.analyse, self.skip]), self.message, self.navigation])
        super().__init__(children)
        self.checkpoint.controls = []
        self.checkpoint._cancel_queued()

    def _selection(self):
        return {entry["subject"]: (entry, options[choice.value])
                for entry, options, include, choice in self.rows if include.value}

    def _request(self, analyse):
        self.navigation.request("brain-health-choice", lambda: self._apply(analyse), all_below=True)

    def _apply(self, analyse):
        selected = self._selection() if analyse else {}
        if analyse and not selected:
            self.message.value = "Select at least one participant, or continue without direct dMRI."
            return False
        apply_dmri_selection(self.namespace, selected)
        self.checkpoint.release()
        self.analyse.disabled = self.skip.disabled = True
        for _, _, include, choice in self.rows:
            include.disabled = choice.disabled = True
        if selected:
            sessions = ", ".join(
                f"{subject} {option.get('session') or ''}".strip()
                for subject, (_, option) in selected.items())
            self.message.value = "<b>Direct dMRI selected:</b> " + escape(sessions) + "."
        else:
            self.message.value = "<b>Direct dMRI declined.</b> Continuing without tract measurements."
        return True

    def close(self):
        checkpoint = getattr(self, "checkpoint", None)
        if checkpoint is not None:
            checkpoint.close()
        for child in getattr(self, "children", ()):
            close_widget(child)
        super().close()


def show_dmri_choice(namespace, shell=None):
    """Offer direct analysis only for sidecar-validated directional dMRI."""
    available = {entry["subject"]: dmri_options(entry) for entry in namespace.get("SUBJECTS", ())
                 if _has_anatomical_t1(namespace["CONFIG"], entry)}
    available = {subject: options for subject, options in available.items() if options}
    if not available:
        apply_dmri_selection(namespace, {})
        directional_without_t1 = any(
            dmri_options(entry) and not _has_anatomical_t1(namespace["CONFIG"], entry)
            for entry in namespace.get("SUBJECTS", ()))
        has_dwi = any(entry.get("dwi_inventory") for entry in namespace.get("SUBJECTS", ()))
        if directional_without_t1:
            print("Directional dMRI was detected, but the current direct-tract route requires a genuine T1w "
                  "anatomical entry; continuing without direct tract analysis.")
        elif has_dwi:
            print("DWI was detected, but no series has sufficient valid gradients for direct diffusion reporting.")
        else:
            print("Directional diffusion MRI is unavailable; continuing without direct tract analysis.")
        return None
    configured = namespace["CONFIG"].get("ANALYSE_TRACT_DWI")
    if configured is not None:
        by_subject = {entry["subject"]: entry for entry in namespace.get("SUBJECTS", ())}
        selected = ({subject: (by_subject[subject], options[0])
                     for subject, options in available.items()} if configured else {})
        apply_dmri_selection(namespace, selected)
        print((f"Direct diffusion analysis selected for {len(selected)} participant(s)."
               if selected else "Direct diffusion analysis disabled in CONFIG."))
        return None
    shell = shell or get_ipython()
    if shell is None:
        raise RuntimeError("The direct-dMRI choice requires an IPython notebook kernel.")
    previous = getattr(shell, "_calmar_dmri_choice", None)
    if previous is not None:
        previous.close()
    panel = DMRIChoice(namespace, shell)
    shell._calmar_dmri_choice = panel
    display(panel)
    return panel
