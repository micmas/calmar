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
from .diffusion import (DMRI_METHODS, DMRI_SUBDIR, assess_dwi_sessions,
                        dmri_method, dmri_option_shells, tensor_metrics_paths,
                        tractometry_paths)
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


def _dipy_single_shell(option):
    """DIPY DTI is validated only for one nonzero acquisition shell."""
    shells = {float(value) for value in dmri_option_shells(option) if float(value) >= 100}
    return len(shells) == 1


def _apply_action_state(widget, state):
    if not state.get("method_available", True):
        widget.disabled = False
        widget.options = [("Unavailable for this acquisition", SKIP)]
        widget.value = SKIP
        widget.disabled = True
        return
    widget.disabled = False
    set_action_options(widget, **action_state_kwargs(state))


def _stage_labels(method):
    return {
        "dmri_preproc": "QSIPrep",
        "dmri_recon": "QSIRecon" if method == "qsirecon" else "DIPY DTI",
        "dmri_metrics": "tract metrics" if method == "qsirecon" else "tensor metrics",
    }


def dmri_analysis_state(namespace, entry, option, method=None):
    """Read-only saved-result state for one exact directional-dMRI choice."""
    try:
        config = _dmri_config(namespace["CONFIG"])
        method = method or dmri_method(config_for_entry(config, entry))
        if method == "dipy_dti" and not _dipy_single_shell(option):
            shells = "/".join(map(str, dmri_option_shells(option))) or "unknown"
            return {
                "status": ("DIPY DTI is unavailable for this multi-shell acquisition "
                           f"(b={shells}); choose QSIRecon"),
                "kind": "unavailable", "current_complete": False,
                "prior_available": False, "outputs_exist": False,
                "rerun_required": False, "method_available": False,
            }
        selected = _processing_entry(entry, option)
        overrides = dict(selected.get(ENTRY_CONFIG) or {})
        overrides["DMRI_METHOD"] = method
        selected[ENTRY_CONFIG] = overrides
        study = Study(config, namespace["RAW_DATASET_DIR"], namespace["PROJECT_DIR"])
        from .scheduled import (cached_step_results, previous_step_results,
                                usable_previous_step_results)
        labels = _stage_labels(method)
        cached = {
            stage: cached_step_results(stage, [selected], study)[0]
            for stage in labels
        }
        previous = {
            stage: previous_step_results(stage, [selected], study)[0]
            for stage in labels
        }
        usable_previous = {
            stage: usable_previous_step_results(stage, [selected], study)[0]
            for stage in labels
        }

        # Receipts are the authoritative match to the current inputs and settings.
        # A later stage is not operationally reusable when an earlier stage must rerun.
        stages = list(labels)
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
        table, _ = (tractometry_paths(dataset, route_config, selected)
                    if method == "qsirecon" else tensor_metrics_paths(dataset, route_config, selected))
        paths = {
            "dmri_preproc": root / "qsiprep",
            "dmri_recon": root / ("qsirecon" if method == "qsirecon" else "dipy_dti"),
            "dmri_metrics": table,
        }
        unmatched = [
            labels[stage] for stage in stages[len(reusable_prefix):]
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
            labels[stage] for stage in stages[len(reusable_prefix):]
            if usable_previous[stage] is not None
        ]
        outputs_exist = bool(existing_stages or prior_prefix or reusable_prefix)
        if overwrite_requested and outputs_exist:
            text = "↻ rerun requested in CONFIG; existing results will not be reused"
            kind = "rerun"
        elif derived:
            text = ("⚠ analysed using explicitly retained older inputs: " +
                    ", ".join(labels[stage] for stage in derived))
            kind = "derived"
        elif len(reusable_prefix) == len(stages):
            text = "✓ analysed already (reusable)"
            kind = "reusable"
        elif reusable_prefix:
            text = "◐ partly analysed: " + ", ".join(
                labels[stage] for stage in reusable_prefix)
            if unmatched:
                text += "; later outputs not reusable: " + ", ".join(unmatched)
            if retained_prior:
                text += ("; input file date or size differs for this or an earlier stage: " +
                         ", ".join(retained_prior))
            kind = "partial_changed" if retained_prior else "partial"
        elif prior_prefix:
            text = ("⚠ input file date or size differs for this or an earlier stage: " +
                    ", ".join(labels[stage] for stage in prior_prefix))
            if unmatched:
                text += "; later outputs not reusable: " + ", ".join(unmatched)
            kind = "changed"
        else:
            found = [
                labels[stage] for stage in stages
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


def dmri_analysis_status(namespace, entry, option, method=None):
    """Short status retained for reports, tests and configured workflows."""
    return dmri_analysis_state(namespace, entry, option, method)["status"]


def _dmri_option_label(option):
    """Describe a diffusion choice without repeating its saved-result status."""
    relation = "same session" if option["same_session"] else "different session"
    reverse = "opposite-PE pair" if option["has_reverse_phase"] else "single PE"
    shells = "/".join(map(str, dmri_option_shells(option)))
    return (f"{option['session'] or '(no session)'} · {relation} · "
            f"{option['n_directions']} dirs · b={shells} · {reverse}")


def _dmri_row_heading(entry, option, options, states, selected, method="qsirecon"):
    method_states = states[method] if isinstance(states, dict) else states
    state = method_states[selected]
    warning_count = len(option.get("warnings") or ())
    details = []
    for index, (candidate, candidate_state) in enumerate(zip(options, method_states)):
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
        identity, state["kind"], details, tags=(DMRI_METHODS[method],),
        warning_count=warning_count)


def apply_dmri_selection(namespace, selected):
    """Record direct-dMRI choices without changing the OpenADS selection."""
    # A re-applied choice can change method, cohort or selected session.  Do
    # not let a single-subject preview from the previous choice suppress the
    # newly selected batch preview.
    namespace.pop("_SINGLE_DMRI_VISUALIZED", None)
    processing, actions, methods = {}, {}, {}
    for value in selected.values():
        if len(value) == 2:
            entry, option = value
            action, method = RUN, dmri_method(config_for_entry(namespace["CONFIG"], entry))
        elif len(value) == 3:
            entry, option, action = value
            method = dmri_method(config_for_entry(namespace["CONFIG"], entry))
        else:
            entry, option, action, method = value
        if method not in DMRI_METHODS:
            raise ValueError(f"Unknown direct-dMRI method: {method!r}")
        if action == SKIP:
            continue
        chosen = _processing_entry(entry, option)
        chosen = entry_with_action(chosen, action, overwrite_key="DMRI_OVERWRITE",
                                   reuse_key="DMRI_REUSE_PRIOR")
        chosen.setdefault(ENTRY_CONFIG, {})["DMRI_METHOD"] = method
        key = (entry["subject"], entry.get("session"))
        processing[key], actions[key], methods[key] = chosen, action, method
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
                shells=dmri_option_shells(chosen["dmri_assessment"]),
                method=config_for_entry(namespace["CONFIG"], chosen)["DMRI_METHOD"])
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
            "shells": dmri_option_shells(item["dmri_assessment"]),
            "has_reverse_phase": item["dmri_assessment"]["has_reverse_phase"],
            "warnings": item["dmri_assessment"]["warnings"],
            "action": actions[(item["subject"], item.get("anatomical_session"))],
            "method": methods[(item["subject"], item.get("anatomical_session"))],
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
        configured_method = dmri_method(namespace["CONFIG"])
        children = [w.HTML(
            "<h3>Optional diffusion tract-microstructure analysis</h3>"
            "<p>Choose a reconstruction method, then one action per participant. The badge shows the selected session's saved-result "
            "status; open <i>Details</i> only when you need the exact receipt or scan warning.</p>"
            "<details style='margin-bottom:10px'><summary style='cursor:pointer'>About this analysis and the "
            "available actions</summary>"
            "<p>This is separate from OpenADS: it preprocesses gradient-bearing 4-D diffusion MRI and can "
            "measure participant-specific diffusion. QSIRecon reconstructs bundles and tractometry; DIPY "
            "fits voxelwise DTI maps (FA, MD, AD and RD). Results remain separate from BCB/DeepDisco "
            "normative disconnectome predictions.</p>"
            "<p>These methods answer different questions and are not interchangeable. Stroke lesions can "
            "distort both; CALMaR never treats a missing reconstructed tract as proof of disconnection.</p>"
            "<p><b>Prior-analysis status is checked without running tools.</b> Reusable means all three saved "
            "receipts still match the selected inputs and outputs. Partial and changed results are identified "
            "explicitly and are not silently treated as current.</p>" + action_help_html() + "</details>")]
        self.method = w.Dropdown(
            options=[(label, key) for key, label in DMRI_METHODS.items()],
            value=configured_method, description="dMRI method:",
            style={"description_width": "initial"}, layout=w.Layout(width="460px"))
        children.append(self.method)
        for entry in namespace.get("SUBJECTS", ()):
            if not _has_anatomical_t1(namespace["CONFIG"], entry):
                continue
            options = dmri_options(entry)
            if not options:
                continue
            choices = []
            states = {method: [] for method in DMRI_METHODS}
            for index, option in enumerate(options):
                for method in DMRI_METHODS:
                    states[method].append(dmri_analysis_state(namespace, entry, option, method))
                choices.append((_dmri_option_label(option), index))
            choice = w.Dropdown(options=choices, value=0, description="Diffusion session:",
                                style={"description_width": "initial"}, layout=w.Layout(width="460px"))
            action = action_dropdown(**action_state_kwargs(states[configured_method][0]))
            _apply_action_state(action, states[configured_method][0])
            heading = w.HTML(_dmri_row_heading(
                entry, options[0], options, states, 0, configured_method))

            def update_session(change, a=action, s=states, e=entry, o=options, h=heading,
                               method_widget=self.method):
                selected = change["new"]
                method = method_widget.value
                _apply_action_state(a, s[method][selected])
                h.value = _dmri_row_heading(e, o[selected], o, s, selected, method)

            choice.observe(update_session, names="value")
            self.rows.append((entry, options, action, choice, states, heading))
            children.append(w.VBox([
                heading, w.HBox([action, choice], layout=w.Layout(flex_flow="row wrap"))]))
        self.analyse, self.skip = action_buttons()
        self.analyse.on_click(lambda _: self._request(True))
        self.skip.on_click(lambda _: self._request(False))
        self.method.observe(self._update_method, names="value")
        children.extend([w.HBox([self.analyse, self.skip]), self.message, self.navigation])
        super().__init__(children)
        self.checkpoint.controls = []
        self.checkpoint._cancel_queued()

    def _selection(self):
        return {(entry["subject"], entry.get("session")):
                (entry, options[choice.value], action.value, self.method.value)
                for entry, options, action, choice, *_ in self.rows if action.value != SKIP}

    def _update_method(self, change):
        method = change["new"]
        for entry, options, action, choice, states, heading in self.rows:
            selected = choice.value
            _apply_action_state(action, states[method][selected])
            heading.value = _dmri_row_heading(
                entry, options[selected], options, states, selected, method)

    def _request(self, analyse):
        self.navigation.request("brain-health-choice", lambda: self._apply(analyse), all_below=True)

    def _apply(self, analyse):
        selected = self._selection() if analyse else {}
        apply_dmri_selection(self.namespace, selected)
        self.checkpoint.release()
        self.analyse.disabled = self.skip.disabled = True
        for _, _, action, choice, *_ in self.rows:
            action.disabled = choice.disabled = True
        self.method.disabled = True
        if selected:
            sessions = ", ".join(
                (f"{key[0] if isinstance(key, tuple) else key} {option.get('session') or ''} "
                 f"({action.replace('_', ' ')})").strip()
                for key, (_, option, action, _) in selected.items())
            self.message.value = ("<b>Diffusion analysis selected:</b> " +
                                  escape(DMRI_METHODS[self.method.value]) + " · " + escape(sessions) + ".")
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
            unavailable = []
            for key, entry, state in states:
                if not state.get("method_available", True):
                    unavailable.append(key)
                    continue
                effective = config_for_entry(namespace["CONFIG"], entry)
                overwrite = bool(effective.get(
                    "DMRI_OVERWRITE", effective.get("OVERWRITE", False)))
                reuse = bool(effective.get("DMRI_REUSE_PRIOR"))
                if ((state.get("rerun_required") and not overwrite) or
                        (state["outputs_exist"] and not state["current_complete"] and
                         not overwrite and not reuse)):
                    unsafe.append(key)
            if unavailable:
                names = ", ".join(" ".join(filter(None, key)) for key in unavailable)
                raise RuntimeError(
                    "Configured DIPY DTI analysis is unavailable for multi-shell input: " + names +
                    ". Select QSIRecon or a single-shell diffusion session.")
            if unsafe:
                names = ", ".join(" ".join(filter(None, key)) for key in unsafe)
                raise RuntimeError(
                    "Configured diffusion tract-microstructure analysis found prior or unmatched "
                    "outputs for " + names + ". Set DMRI_OVERWRITE=True to recompute them, or "
                    "DMRI_REUSE_PRIOR=True to explicitly retain compatible prior results.")
        selected = ({key: (entry, options[0])
                     for key, (entry, options) in available.items()} if configured else {})
        apply_dmri_selection(namespace, selected)
        selected_method = dmri_method(namespace["CONFIG"])
        print((f"{DMRI_METHODS[selected_method]} selected for {len(selected)} participant(s)."
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
