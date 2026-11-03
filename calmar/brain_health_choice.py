"""Opt-in notebook choice for structural brain-health analysis."""

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
from .brain_health import brain_health_inventory
from .execution import ExecutionCheckpoint
from .notebook_navigation import NotebookNavigation
from .study import (ENTRY_CONFIG, ENTRY_DATASET, config_for_entry,
                    dataset_for_entry)
from .widget_lifecycle import close_widget


def _selected_entry(entry, inventory, components):
    selected = deepcopy(entry)
    selected["brain_health_components"] = list(components)
    selected["flair"] = inventory.get("flair")
    selected["anatomical_t1w"] = inventory.get("t1w")
    return selected


def brain_health_analysis_state(namespace, entry, inventory, components):
    """Read-only receipt status for the exact brain-health selection."""
    try:
        selected = _selected_entry(entry, inventory, components)
        from .scheduled import (cached_step_results, previous_step_results,
                                usable_previous_step_results)
        from .study import Study
        study = Study(namespace["CONFIG"], namespace["RAW_DATASET_DIR"], namespace["PROJECT_DIR"])
        stages = (["brain_health_anatomy"] if "atrophy" in components else []) + \
                 (["brain_health_wmh"] if "wmh" in components else []) + ["brain_health_metrics"]
        current = {stage: cached_step_results(stage, [selected], study)[0] for stage in stages}
        previous = {stage: previous_step_results(stage, [selected], study)[0] for stage in stages}
        usable_previous = {
            stage: usable_previous_step_results(stage, [selected], study)[0]
            for stage in stages
        }
        labels = {"brain_health_anatomy": "T1 volumetry", "brain_health_wmh": "FLAIR WMH",
                  "brain_health_metrics": "final metrics"}
        current_stages = [stage for stage in stages if current[stage] is not None]
        prior_stages = [stage for stage in stages if usable_previous[stage] is not None]
        retained_prior = [stage for stage in stages
                          if current[stage] is None and usable_previous[stage] is not None]
        from .brain_health import output_paths
        route_config = config_for_entry(namespace["CONFIG"], selected)
        overwrite_requested = bool(route_config.get(
            "BRAIN_HEALTH_OVERWRITE", route_config.get("OVERWRITE", False)))
        dataset = dataset_for_entry(namespace["RAW_DATASET_DIR"], selected)
        paths = output_paths(dataset, route_config, selected)
        stage_paths = {
            "brain_health_anatomy": paths["anatomy"],
            "brain_health_wmh": paths["wmh"],
            "brain_health_metrics": paths["metrics"],
        }
        existing_stages = [stage for stage in stages if Path(stage_paths[stage]).exists()]
        unmatched = [
            stage for stage in stages
            if current[stage] is None and usable_previous[stage] is None and
            (previous[stage] is not None or stage in existing_stages)
        ]
        outputs_exist = bool(existing_stages or any(current.values()) or any(previous.values()))
        derived_stages = []
        for stage in stages:
            result = current[stage] or usable_previous[stage]
            if result is not None and any(
                    row.get("derived_from_prior") for row in result.get("results", [])):
                derived_stages.append(stage)
        if overwrite_requested and outputs_exist:
            text = "↻ rerun requested in CONFIG; existing results will not be reused"
            kind = "rerun"
        elif derived_stages:
            text = ("⚠ analysed using explicitly retained older inputs: " +
                    ", ".join(labels[s] for s in derived_stages))
            kind = "derived"
        elif len(current_stages) == len(stages):
            text = "✓ analysed already (reusable)"
            kind = "reusable"
        elif current_stages:
            text = "◐ partly analysed: " + ", ".join(labels[s] for s in current_stages)
            if unmatched:
                text += "; later outputs not reusable: " + ", ".join(labels[s] for s in unmatched)
            if retained_prior:
                text += ("; input file date or size differs for this or an earlier stage: " +
                         ", ".join(labels[s] for s in retained_prior))
            kind = "partial_changed" if retained_prior else "partial"
        elif prior_stages:
            text = ("⚠ input file date or size differs for this or an earlier stage: " +
                    ", ".join(labels[s] for s in prior_stages))
            if unmatched:
                text += "; later outputs not reusable: " + ", ".join(labels[s] for s in unmatched)
            kind = "changed"
        elif outputs_exist:
            found = unmatched or existing_stages
            text = "⚠ existing brain-health output"
            if found:
                text += ": " + ", ".join(labels[s] for s in found)
            text += "; no reusable receipt"
            kind = "existing"
        else:
            text = "○ not analysed yet"
            kind = "new"
        return {"status": text,
                "kind": kind,
                "current_complete": len(current_stages) == len(stages) and not derived_stages,
                "prior_available": bool(prior_stages),
                "outputs_exist": outputs_exist,
                "rerun_required": bool(unmatched or (overwrite_requested and outputs_exist)),
                "requires_overwrite": bool(unmatched)}
    except Exception as exc:
        return {"status": f"⚠ analysis status unavailable ({type(exc).__name__})",
                "kind": "unavailable", "current_complete": False,
                "prior_available": False, "outputs_exist": True, "rerun_required": True,
                "requires_overwrite": True}


def _brain_health_heading(entry, inventory, components, state):
    identity = entry["subject"]
    if entry.get("session"):
        identity += f" · {entry['session']}"
    component_labels = []
    if "atrophy" in components:
        component_labels.append("T1 volumetry")
    if "wmh" in components:
        component_labels.append("FLAIR WMH")
    details = [("Saved result", state["status"]),
               ("Measures", " + ".join(component_labels))]
    if inventory.get("t1w"):
        details.append(("T1 input", Path(inventory["t1w"]).name))
    if inventory.get("flair"):
        details.append(("FLAIR input", Path(inventory["flair"]).name))
    return compact_choice_heading(identity, state["kind"], details, tags=component_labels)


def apply_brain_health_selection(namespace, selected):
    """Attach compact report metadata and retain processing entries."""
    processing, actions = {}, {}
    for key, value in selected.items():
        entry, inventory, components, action = (*value, RUN) if len(value) == 3 else value
        if action == SKIP:
            continue
        chosen = _selected_entry(entry, inventory, components)
        processing[key] = entry_with_action(
            chosen, action, overwrite_key="BRAIN_HEALTH_OVERWRITE",
            reuse_key="BRAIN_HEALTH_REUSE_PRIOR")
        actions[key] = action
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
                    value = chosen[key]
                    if key == ENTRY_CONFIG:
                        value = without_action_policy({ENTRY_CONFIG: value}).get(ENTRY_CONFIG)
                    if value:
                        copied["brain_health_analysis"][key] = value
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
            "action": actions[(item["subject"], item.get("session"))],
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
        self.navigation = NotebookNavigation(
            self.message, on_cell_order=self.checkpoint._update_cell_order,
            focus_checkpoint=self.checkpoint)
        self.rows = []
        children = [w.HTML(
            "<h3>Optional structural brain health</h3>"
            "<p>Choose one action per participant. The badges show saved-result status and the measurements "
            "available from the selected scans. <b>These single-scan measures are not diagnostic; stroke "
            "lesions can bias them, and visual QC is required.</b></p>"
            "<details style='margin-bottom:10px'><summary style='cursor:pointer'>About these measurements and "
            "the available actions</summary>"
            "<p>T1-derived atrophy-sensitive volumes and same-session FLAIR white-matter-hyperintensity burden "
            "remain separate from the focal stroke interpretation.</p>"
            "<p>A single scan cannot diagnose atrophy. Stroke cavities and acute FLAIR lesion signal can bias "
            "both analyses, so CALMaR reports lesion-adjusted values, preserves the raw burden and requires "
            "visual QC.</p>" + action_help_html() + "</details>")]
        for key, (entry, inventory, components) in available_entries(namespace).items():
            subject, session = key
            flair_options = inventory.get("flair_candidates") or []
            flair_choice = None
            if len(flair_options) > 1:
                flair_choice = w.Dropdown(
                    options=[(Path(path).name, path) for path in flair_options], value=inventory.get("flair"),
                    description="FLAIR:", style={"description_width": "initial"},
                    layout=w.Layout(width="520px"))
            state = brain_health_analysis_state(namespace, entry, inventory, components)
            action = action_dropdown(**action_state_kwargs(state))
            heading = w.HTML(_brain_health_heading(entry, inventory, components, state))
            if flair_choice is not None:
                def update_flair(change, *, base=inventory, analysis=action, label=heading,
                                 source=entry, selected_components=components):
                    chosen = dict(base)
                    chosen["flair"] = change["new"]
                    updated = brain_health_analysis_state(
                        namespace, source, chosen, selected_components)
                    set_action_options(analysis, **action_state_kwargs(updated))
                    label.value = _brain_health_heading(
                        source, chosen, selected_components, updated)
                flair_choice.observe(update_flair, names="value")
            self.rows.append((entry, inventory, components, action, flair_choice, state, heading))
            children.append(w.VBox([
                heading, w.HBox([item for item in (action, flair_choice) if item is not None],
                                layout=w.Layout(flex_flow="row wrap"))]))
        self.analyse, self.skip = action_buttons()
        self.analyse.on_click(lambda _: self._request(True))
        self.skip.on_click(lambda _: self._request(False))
        children.extend([w.HBox([self.analyse, self.skip]), self.message, self.navigation])
        super().__init__(children)
        self.checkpoint.controls = []
        self.checkpoint._cancel_queued()

    def _selection(self):
        selected = {}
        for entry, inventory, components, action, flair_choice, *_ in self.rows:
            if action.value == SKIP:
                continue
            chosen = dict(inventory)
            if flair_choice is not None:
                chosen["flair"] = flair_choice.value
            selected[(entry["subject"], entry.get("session"))] = (
                entry, chosen, components, action.value)
        return selected

    def _request(self, analyse):
        self.navigation.request("single-test-selection", lambda: self._apply(analyse), all_below=True)

    def _apply(self, analyse):
        selected = self._selection() if analyse else {}
        apply_brain_health_selection(self.namespace, selected)
        self.checkpoint.release()
        self.analyse.disabled = self.skip.disabled = True
        for _, _, _, action, flair_choice, *_ in self.rows:
            action.disabled = True
            if flair_choice is not None:
                flair_choice.disabled = True
        if selected:
            labels = [
                (f"{subject} {session or ''} ({value[3].replace('_', ' ')})").strip()
                for (subject, session), value in selected.items()
            ]
            self.message.value = "<b>Brain-health analysis selected:</b> " + escape(", ".join(labels)) + "."
        elif analyse:
            self.message.value = ("<b>No participant had an analysis action selected.</b> "
                                  "Continuing without brain-health analysis.")
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
        states = [
            (key, brain_health_analysis_state(namespace, entry, inventory, components))
            for key, (entry, inventory, components) in available.items()
        ]
        if configured:
            unsafe = []
            for key, state in states:
                entry = available[key][0]
                effective = config_for_entry(namespace["CONFIG"], entry)
                overwrite = bool(effective.get(
                    "BRAIN_HEALTH_OVERWRITE", effective.get("OVERWRITE", False)))
                reuse = bool(effective.get("BRAIN_HEALTH_REUSE_PRIOR"))
                if ((state.get("requires_overwrite") and not overwrite) or
                        (state["outputs_exist"] and not state["current_complete"] and
                         not overwrite and not reuse)):
                    unsafe.append(key)
            if unsafe:
                names = ", ".join(" ".join(filter(None, key)) for key in unsafe)
                raise RuntimeError(
                    "Configured brain-health analysis found prior or unmatched outputs for " + names +
                    ". Set BRAIN_HEALTH_OVERWRITE=True to recompute them, or "
                    "BRAIN_HEALTH_REUSE_PRIOR=True to explicitly retain compatible prior results.")
        selected = available if configured else {}
        apply_brain_health_selection(namespace, selected)
        print((f"Brain-health analysis selected for {len(selected)} participant(s)."
               if selected else "Brain-health analysis disabled in CONFIG."))
        for (subject, session), state in states:
            print(f"  {subject} {session or '(no session)'}: {state['status']}")
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
