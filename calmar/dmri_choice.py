"""Early opt-in choice for direct analysis of directional diffusion MRI."""

from copy import deepcopy
from html import escape
import json
from pathlib import Path

import ipywidgets as w
from IPython import get_ipython
from IPython.display import display

from .analysis_choice import (RUN, SKIP, action_buttons, action_dropdown,
                              action_help_html, action_state_kwargs,
                              compact_choice_heading, entry_with_action,
                              set_action_options, without_action_policy)
from .diffusion import DMRI_SUBDIR, assess_dwi_sessions, tractometry_paths
from .execution import ExecutionCheckpoint
from .notebook_navigation import NotebookNavigation
from .study import (ENTRY_CONFIG, ENTRY_DATASET, Study, config_for_entry,
                    dataset_for_entry, modality)
from .widget_lifecycle import close_widget


def dmri_options(entry):
    """Report-ready gradient-bearing diffusion sessions for one participant."""
    return assess_dwi_sessions(entry)


def _has_anatomical_t1(config, entry):
    """The current direct-dMRI pipeline requires a genuine T1-route anatomy."""
    return modality(config_for_entry(config, entry)) == "t1"


def _processing_entry(entry, option):
    """Combine the anatomical entry with one explicit diffusion session."""
    primary = option["primary"]
    selected = {key: value for key, value in entry.items()
                if key not in ("dwi_inventory", "dmri_analysis")}
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


def _dmri_config(config):
    selected = deepcopy(config)
    selected.update(MODALITY="t1")
    return selected


_DMRI_STAGE_LABELS = {
    "dmri_preproc": "QSIPrep",
    "dmri_recon": "QSIRecon",
    "dmri_metrics": "final metrics",
}


def dmri_analysis_state(namespace, entry, option):
    """Read-only saved-result state for one exact directional-dMRI choice."""
    try:
        selected = _processing_entry(entry, option)
        config = _dmri_config(namespace["CONFIG"])
        study = Study(config, namespace["RAW_DATASET_DIR"], namespace["PROJECT_DIR"])
        from .scheduled import (cached_step_results, previous_step_results,
                                usable_previous_step_results)
        cached = {
            stage: cached_step_results(stage, [selected], study)[0]
            for stage in _DMRI_STAGE_LABELS
        }
        previous = {
            stage: previous_step_results(stage, [selected], study)[0]
            for stage in _DMRI_STAGE_LABELS
        }
        usable_previous = {
            stage: usable_previous_step_results(stage, [selected], study)[0]
            for stage in _DMRI_STAGE_LABELS
        }

        # Receipts are the authoritative match to the current inputs and settings.
        # A later stage is not operationally reusable when an earlier stage must rerun.
        stages = list(_DMRI_STAGE_LABELS)
        reusable_prefix = []
        for stage in stages:
            if cached[stage] is None:
                break
            reusable_prefix.append(stage)

        route_config = config_for_entry(config, selected)
        overwrite_requested = bool(route_config.get(
            "DMRI_OVERWRITE", route_config.get("OVERWRITE", False)))
        dataset = dataset_for_entry(namespace["RAW_DATASET_DIR"], selected)
        root = (Path(dataset) / route_config.get("DMRI_SUBDIR", DMRI_SUBDIR) /
                selected["subject"] / (selected.get("session") or ""))
        table, _ = tractometry_paths(dataset, route_config, selected)
        paths = {
            "dmri_preproc": root / "qsiprep",
            "dmri_recon": root / "qsirecon",
            "dmri_metrics": table,
        }
        unmatched = [
            _DMRI_STAGE_LABELS[stage] for stage in stages[len(reusable_prefix):]
            if ((cached[stage] is not None or previous[stage] is not None or paths[stage].exists())
                and usable_previous[stage] is None)
        ]

        prior_prefix = []
        for stage in stages:
            if usable_previous[stage] is None:
                break
            prior_prefix.append(stage)

        existing_stages = [stage for stage in stages if paths[stage].exists()]
        derived = [
            stage for stage in stages
            if cached[stage] is not None and any(
                row.get("derived_from_prior") for row in cached[stage].get("results", []))
        ]
        retained_prior = [
            _DMRI_STAGE_LABELS[stage] for stage in stages[len(reusable_prefix):]
            if usable_previous[stage] is not None
        ]
        outputs_exist = bool(existing_stages or prior_prefix or reusable_prefix)
        if overwrite_requested and outputs_exist:
            text = "↻ rerun requested in CONFIG; existing results will not be reused"
            kind = "rerun"
        elif derived:
            text = ("⚠ analysed using explicitly retained older inputs: " +
                    ", ".join(_DMRI_STAGE_LABELS[stage] for stage in derived))
            kind = "derived"
        elif len(reusable_prefix) == len(stages):
            text = "✓ analysed already (reusable)"
            kind = "reusable"
        elif reusable_prefix:
            text = "◐ partly analysed: " + ", ".join(
                _DMRI_STAGE_LABELS[stage] for stage in reusable_prefix)
            if unmatched:
                text += "; later outputs not reusable: " + ", ".join(unmatched)
            if retained_prior:
                text += ("; input file date or size differs for this or an earlier stage: " +
                         ", ".join(retained_prior))
            kind = "partial_changed" if retained_prior else "partial"
        elif prior_prefix:
            text = ("⚠ input file date or size differs for this or an earlier stage: " +
                    ", ".join(_DMRI_STAGE_LABELS[stage] for stage in prior_prefix))
            if unmatched:
                text += "; later outputs not reusable: " + ", ".join(unmatched)
            kind = "changed"
        else:
            found = [
                _DMRI_STAGE_LABELS[stage] for stage in stages
                if cached[stage] is not None or paths[stage].exists()
            ]
            if found:
                suffix = "; overwrite/recompute requested" if route_config.get("DMRI_OVERWRITE") else \
                    "; no reusable receipt for current inputs/settings"
                text = "⚠ existing " + ", ".join(found) + suffix
                kind = "existing"
            else:
                text = "○ not analysed yet"
                kind = "new"
        return {"status": text,
                "kind": kind,
                "current_complete": len(reusable_prefix) == len(stages) and not derived,
                "prior_available": bool(prior_prefix),
                "outputs_exist": outputs_exist,
                # An unmatched later-stage folder blocks safe incremental reuse:
                # that stage refuses to overwrite it and must be explicitly rerun.
                "rerun_required": bool(unmatched or (overwrite_requested and outputs_exist))}
    except Exception as exc:
        return {"status": f"⚠ analysis status unavailable ({type(exc).__name__})",
                "kind": "unavailable", "current_complete": False,
                "prior_available": False, "outputs_exist": True, "rerun_required": True}


def dmri_analysis_status(namespace, entry, option):
    """Short status retained for reports, tests and configured workflows."""
    return dmri_analysis_state(namespace, entry, option)["status"]


def _dmri_option_label(option):
    """Describe a diffusion choice without repeating its saved-result status."""
    relation = "same session" if option["same_session"] else "different session"
    reverse = "opposite-PE pair" if option["has_reverse_phase"] else "single PE"
    shells = "/".join(map(str, option["shells"]))
    return (f"{option['session'] or '(no session)'} · {relation} · "
            f"{option['n_directions']} dirs · b={shells} · {reverse}")


def _dmri_row_heading(entry, option, options, states, selected):
    state = states[selected]
    warning_count = len(option.get("warnings") or ())
    details = []
    for index, (candidate, candidate_state) in enumerate(zip(options, states)):
        session = candidate["session"] or "(no session)"
        if index == selected:
            session += " (selected)"
        value = candidate_state["status"]
        warnings = candidate.get("warnings") or ()
        if warnings:
            value += "; scan checks: " + "; ".join(map(str, warnings))
        details.append((session, value))
    identity = entry["subject"]
    if entry.get("session"):
        identity += f" · anatomy {entry['session']}"
    return compact_choice_heading(
        identity, state["kind"], details, warning_count=warning_count)


def apply_dmri_selection(namespace, selected):
    """Record direct-dMRI choices without changing the OpenADS selection."""
    processing, actions = {}, {}
    for value in selected.values():
        entry, option, action = (*value, RUN) if len(value) == 2 else value
        if action == SKIP:
            continue
        chosen = _processing_entry(entry, option)
        chosen = entry_with_action(chosen, action, overwrite_key="DMRI_OVERWRITE",
                                   reuse_key="DMRI_REUSE_PRIOR")
        key = (entry["subject"], entry.get("session"))
        processing[key], actions[key] = chosen, action
    subjects = []
    for entry in namespace.get("SUBJECTS", ()):
        copied = dict(entry)
        copied.pop("dmri_analysis", None)
        chosen = processing.get((entry["subject"], entry.get("session")))
        if chosen is not None:
            # Report linkage is deliberately compact and JSON-serializable.
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
                    value = chosen[key]
                    if key == ENTRY_CONFIG:
                        value = without_action_policy({ENTRY_CONFIG: value}).get(ENTRY_CONFIG)
                    if value:
                        copied["dmri_analysis"][key] = value
        subjects.append(copied)

    config = namespace["CONFIG"]
    config["_TRACT_DWI_SELECTED"] = bool(processing)
    dmri_config = _dmri_config(config)
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
            "action": actions[(item["subject"], item.get("anatomical_session"))],
        } for item in entries],
    }
    path = Path(namespace["PROJECT_DIR"]) / "reports" / "dmri-selection.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=2, default=str) + "\n", encoding="utf-8")
    return entries


class DMRIChoice(w.VBox):
    """Opt-in panel kept separate from the DWI/ADC OpenADS decision."""

    def __init__(self, namespace, shell):
        self.namespace = namespace
        self.checkpoint = ExecutionCheckpoint(
            shell, "Execution is paused for the optional diffusion tract-microstructure decision.")
        self.message = w.HTML()
        self.navigation = NotebookNavigation(
            self.message, on_cell_order=self.checkpoint._update_cell_order,
            focus_checkpoint=self.checkpoint)
        self.rows = []
        children = [w.HTML(
            "<h3>Optional diffusion tract-microstructure analysis</h3>"
            "<p>Choose one action per participant. The badge shows the selected session's saved-result "
            "status; open <i>Details</i> only when you need the exact receipt or scan warning.</p>"
            "<details style='margin-bottom:10px'><summary style='cursor:pointer'>About this analysis and the "
            "available actions</summary>"
            "<p>This is separate from OpenADS: it preprocesses gradient-bearing 4-D diffusion MRI and can "
            "measure participant-specific tract microstructure. Results remain separate from BCB/DeepDisco "
            "normative disconnectome predictions.</p>"
            "<p>Stroke lesions can distort registration and cause tractography to stop. CALMaR reports lesion "
            "overlap and diffusion QC, and never treats a missing reconstructed tract as proof of "
            "disconnection.</p>"
            "<p><b>Prior-analysis status is checked without running tools.</b> Reusable means all three saved "
            "receipts still match the selected inputs and outputs. Partial and changed results are identified "
            "explicitly and are not silently treated as current.</p>" + action_help_html() + "</details>")]
        for entry in namespace.get("SUBJECTS", ()):
            if not _has_anatomical_t1(namespace["CONFIG"], entry):
                continue
            options = dmri_options(entry)
            if not options:
                continue
            choices, states = [], []
            for index, option in enumerate(options):
                state = dmri_analysis_state(namespace, entry, option)
                states.append(state)
                choices.append((_dmri_option_label(option), index))
            choice = w.Dropdown(options=choices, value=0, description="Diffusion session:",
                                style={"description_width": "initial"}, layout=w.Layout(width="460px"))
            action = action_dropdown(**action_state_kwargs(states[0]))
            heading = w.HTML(_dmri_row_heading(entry, options[0], options, states, 0))

            def update_session(change, a=action, s=states, e=entry, o=options, h=heading):
                selected = change["new"]
                set_action_options(a, **action_state_kwargs(s[selected]))
                h.value = _dmri_row_heading(e, o[selected], o, s, selected)

            choice.observe(update_session, names="value")
            self.rows.append((entry, options, action, choice, states, heading))
            children.append(w.VBox([
                heading, w.HBox([action, choice], layout=w.Layout(flex_flow="row wrap"))]))
        self.analyse, self.skip = action_buttons()
        self.analyse.on_click(lambda _: self._request(True))
        self.skip.on_click(lambda _: self._request(False))
        children.extend([w.HBox([self.analyse, self.skip]), self.message, self.navigation])
        super().__init__(children)
        self.checkpoint.controls = []
        self.checkpoint._cancel_queued()

    def _selection(self):
        return {(entry["subject"], entry.get("session")): (entry, options[choice.value], action.value)
                for entry, options, action, choice, *_ in self.rows if action.value != SKIP}

    def _request(self, analyse):
        self.navigation.request("brain-health-choice", lambda: self._apply(analyse), all_below=True)

    def _apply(self, analyse):
        selected = self._selection() if analyse else {}
        apply_dmri_selection(self.namespace, selected)
        self.checkpoint.release()
        self.analyse.disabled = self.skip.disabled = True
        for _, _, action, choice, *_ in self.rows:
            action.disabled = choice.disabled = True
        if selected:
            sessions = ", ".join(
                (f"{key[0] if isinstance(key, tuple) else key} {option.get('session') or ''} "
                 f"({action.replace('_', ' ')})").strip()
                for key, (_, option, action) in selected.items())
            self.message.value = "<b>Diffusion tract-microstructure analysis selected:</b> " + escape(sessions) + "."
        elif analyse:
            self.message.value = ("<b>No participant had an analysis action selected.</b> "
                                  "Continuing without participant diffusion measurements.")
        else:
            self.message.value = ("<b>Diffusion tract-microstructure analysis declined.</b> "
                                  "Continuing without participant diffusion measurements.")
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
    available = {(entry["subject"], entry.get("session")): (entry, dmri_options(entry))
                 for entry in namespace.get("SUBJECTS", ())
                 if _has_anatomical_t1(namespace["CONFIG"], entry)}
    available = {key: pair for key, pair in available.items() if pair[1]}
    if not available:
        apply_dmri_selection(namespace, {})
        directional_without_t1 = any(
            dmri_options(entry) and not _has_anatomical_t1(namespace["CONFIG"], entry)
            for entry in namespace.get("SUBJECTS", ()))
        has_dwi = any(entry.get("dwi_inventory") for entry in namespace.get("SUBJECTS", ()))
        if directional_without_t1:
            print("Directional diffusion MRI was detected, but the tract-microstructure route requires a "
                  "genuine T1w anatomical entry; continuing without participant diffusion measurements.")
        elif has_dwi:
            print("DWI data were detected, but none qualifies for the separate tract-microstructure "
                  "workflow. That route requires a gradient-bearing 4-D series with valid sidecars and at "
                  "least 30 distinct diffusion directions; this is independent of OpenADS DWI+ADC "
                  "acute-lesion segmentation.")
        else:
            print("No gradient-bearing diffusion MRI was found; continuing without tract-microstructure "
                  "analysis.")
        return None
    configured = namespace["CONFIG"].get("ANALYSE_TRACT_DWI")
    if configured is not None:
        states = [
            ((entry["subject"], options[0]["session"]), entry,
             dmri_analysis_state(namespace, entry, options[0]))
            for entry, options in available.values()
        ]
        if configured:
            unsafe = []
            for key, entry, state in states:
                effective = config_for_entry(namespace["CONFIG"], entry)
                overwrite = bool(effective.get(
                    "DMRI_OVERWRITE", effective.get("OVERWRITE", False)))
                reuse = bool(effective.get("DMRI_REUSE_PRIOR"))
                if ((state.get("rerun_required") and not overwrite) or
                        (state["outputs_exist"] and not state["current_complete"] and
                         not overwrite and not reuse)):
                    unsafe.append(key)
            if unsafe:
                names = ", ".join(" ".join(filter(None, key)) for key in unsafe)
                raise RuntimeError(
                    "Configured diffusion tract-microstructure analysis found prior or unmatched "
                    "outputs for " + names + ". Set DMRI_OVERWRITE=True to recompute them, or "
                    "DMRI_REUSE_PRIOR=True to explicitly retain compatible prior results.")
        selected = ({key: (entry, options[0])
                     for key, (entry, options) in available.items()} if configured else {})
        apply_dmri_selection(namespace, selected)
        print((f"Diffusion tract-microstructure analysis selected for {len(selected)} participant(s)."
               if selected else "Diffusion tract-microstructure analysis disabled in CONFIG."))
        for (subject, session), _, state in states:
            print(f"  {subject} {session or '(no session)'}: {state['status']}")
        return None
    shell = shell or get_ipython()
    if shell is None:
        raise RuntimeError("The diffusion tract-microstructure choice requires an IPython notebook kernel.")
    previous = getattr(shell, "_calmar_dmri_choice", None)
    if previous is not None:
        previous.close()
    panel = DMRIChoice(namespace, shell)
    shell._calmar_dmri_choice = panel
    display(panel)
    return panel
