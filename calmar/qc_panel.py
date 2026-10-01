"""QC controls with participant-local drafts and explicit save/navigation actions."""

from copy import deepcopy
from datetime import date
from html import escape

import ipywidgets as w
from . import qc as q
from .notebook_navigation import NotebookNavigation
from . import colors
from .widget_lifecycle import close_widget


class QCPanel(w.VBox):
    def __init__(self, entries, stages_for, anchor_for, volumes_for, viewer,
                 checkpoint, *, encode_volumes=lambda volumes: volumes):
        self.entries = tuple(dict(e) for e in entries)
        self.stages_for = stages_for
        self.anchor_for = anchor_for
        self.volumes_for = volumes_for
        self.viewer = viewer
        self.checkpoint = checkpoint
        self.encode_volumes = encode_volumes
        self.drafts = {}
        self.loading = False
        self.inactive = False
        self.message = w.HTML()
        self.navigation = NotebookNavigation(
            self.message, on_cell_order=checkpoint._update_cell_order)
        self.subject = w.Dropdown(options=[
            (f"{i+1}. {e['subject']} {e.get('session') or ''}", i)
            for i, e in enumerate(self.entries)], description="Participant:",
            style={"description_width": "initial"}, layout=w.Layout(width="500px"))
        self.stage = w.ToggleButtons(description="View:", style={"button_width":"235px"})
        self.rows = w.VBox()
        self.rating_buttons = {}
        self.help = w.HTML()
        self.reference = w.Checkbox(description="Show manual reference in native space", value=False,
                                    layout=w.Layout(width="auto"))
        self.synth = w.Checkbox(description="Show SynthStroke reference in MNI", value=True,
                                layout=w.Layout(width="auto"))
        self.issues = w.SelectMultiple(description="Issues:", rows=5)
        self.notes = w.Textarea(description="Notes:", layout=w.Layout(width="90%"))
        self.reviewer = w.Text(description="Reviewer:")
        self.repair = w.Checkbox(description="Mark participant for repair")
        self.save = w.Button(description="Save stage →", button_style="primary")
        self.save_next = w.Button(description="Save & next participant", button_style="success",
                                  layout=w.Layout(width="210px"))
        self.repair_button = w.Button(description="Run skull-strip repair", layout=w.Layout(width="190px"))
        self.continue_button = w.Button(description="Continue after QC", layout=w.Layout(width="180px"))
        self.existing_summary = w.HTML()
        self.use_existing = w.Button(description="Use existing QC", button_style="success",
                                     layout=w.Layout(width="170px"))
        self.redo = w.Button(description="Redo QC", button_style="primary")
        saved = self._saved_records()
        self._show_existing_summary(saved)
        has_existing = any(self._has_saved_qc(i, record) for i, record in saved.items())
        if has_existing:
            checkpoint.message.value = (
                "<b>⏸ QC already exists for participants below.</b> Use the saved QC or redo the review. "
                "Use existing QC continues directly to the next processing step. Skip QC remains available.")
        self.use_existing.on_click(lambda _: self.reuse_saved())
        self.redo.on_click(lambda _: self.redo_qc())
        checkpoint.skip_qc.on_click(self._sync_existing_buttons)
        choice_buttons = w.HBox(
            [self.use_existing, self.redo, checkpoint.skip_qc] if has_existing
            else [checkpoint.do_qc, checkpoint.skip_qc],
                                layout=w.Layout(flex_flow="row wrap"))
        next_steps = w.HBox([self.repair_button, self.continue_button],
                           layout=w.Layout(flex_flow="row wrap", margin="12px 0 0 0"))
        super().__init__([
            checkpoint.message, self.existing_summary, choice_buttons, self.subject,
            w.HTML("<b>Rate each available stage: 1 good · 2 acceptable · 3 poor.</b> "
                   "Click a number to view that stage. Save &amp; next saves all stages together. "
                   "Unsaved choices stay in this panel until it is rerun or the kernel restarts."),
            self.rows, self.stage, self.help,
            w.HBox([self.reference, self.synth], layout=w.Layout(flex_flow="row wrap")), viewer,
            self.issues, self.notes, self.reviewer, self.repair,
            w.HBox([self.save, self.save_next]),
            w.HTML(colors.legend(["hdbet", "linda", "manual", "synthstroke"])),
            next_steps, self.message, self.navigation])
        self.subject.observe(self._load_subject, names="value")
        self.stage.observe(self._load_stage, names="value")
        self.reference.observe(self._render, names="value")
        self.synth.observe(self._render, names="value")
        self.issues.observe(self._capture, names="value")
        self.notes.observe(self._capture, names="value")
        self.repair.observe(self._capture, names="value")
        self.save.on_click(lambda _: self.save_current())
        self.save_next.on_click(lambda _: self.save_participant())
        self.repair_button.on_click(lambda _: self.navigation.request(
            "skull-repair", self._prepare_repair, all_below=False,
            prompt="Run the next participant needing skull-strip repair? This reruns HD-BET and LINDA."))
        self.continue_button.on_click(lambda _: self.continue_after_qc())
        if self.entries:
            self._load_subject()
        else:
            self.save.disabled = self.save_next.disabled = self.repair_button.disabled = True
            self.message.value = "No masks are available for QC. Choose Skip QC to continue."

    def _saved_records(self):
        return {i: q.QCRecord.load(self.anchor_for(e)) for i, e in enumerate(self.entries)}

    def _sync_existing_buttons(self, *_):
        if not self.inactive:
            self.use_existing.disabled = self.checkpoint.choice == "existing_reused"
            self.redo.disabled = self.checkpoint.choice == "review_requested"

    def _has_saved_qc(self, index, record):
        return any(data.get("rating") in (1, 2, 3) or data.get("issue_tags")
                   or (data.get("notes") or "").strip()
                   for stage in self.stages_for(self.entries[index])
                   for data in [record.get_stage(stage)])

    def _show_existing_summary(self, saved):
        rows = []
        for i, record in saved.items():
            if not self._has_saved_qc(i, record):
                continue
            entry = self.entries[i]
            stages = self.stages_for(entry)
            count = sum(record.get_stage(s).get("rating") in (1, 2, 3) for s in stages)
            who = " · ".join(str(v) for v in (record.reviewer, record.reviewed_on) if v)
            flags = " · Repair flagged" if record.marked_for_rerun else ""
            rows.append(f"<li><b>{escape(entry['subject'])} {escape(entry.get('session') or '')}</b>: "
                        f"{count}/{len(stages)} stages rated"
                        + (f" · {escape(who)}" if who else "") + flags + "</li>")
        self.existing_summary.value = (
            "<b>Saved QC:</b><ul>" + "".join(rows) + "</ul>"
            "Use existing QC keeps these ratings and continues after QC. "
            "Redo QC starts fresh ratings for this group; saved ratings remain until you save replacements."
            if rows else "")

    def reuse_saved(self):
        if self.inactive:
            return False
        try:
            saved = self._saved_records()
            existing = [self.entries[i] for i, record in saved.items() if self._has_saved_qc(i, record)]
            if not self.checkpoint.choose("existing_reused", existing_entries=existing):
                return False
        except Exception as error:
            self.message.value = "Could not load existing QC: " + escape(str(error))
            return False
        self.drafts = saved
        self._show_existing_summary(saved)
        pending = [(i, s) for i, e in enumerate(self.entries) for s in self.stages_for(e)
                   if saved[i].get_stage(s).get("rating") not in (1, 2, 3)]
        self.subject.value = pending[0][0] if pending else 0
        self._load_subject()
        if pending:
            self.stage.value = pending[0][1]
            self.message.value = "Existing QC kept. Continuing after QC; unrated stages remain unrated."
        else:
            self.message.value = "All available stages have saved ratings. Continuing after QC."
        self.use_existing.disabled, self.redo.disabled = True, False
        # Choosing saved QC is already an explicit continuation action. Use the
        # same navigation as Continue after QC, without requiring a second click.
        return self.continue_after_qc(confirm=False)

    def continue_after_qc(self, *, confirm=True):
        if self.inactive:
            return False
        return self.navigation.request(
            "after-qc", self._continue,
            prompt=("Continue to disconnectomes and reports using the saved QC choices?"
                    if confirm else ""))

    def redo_qc(self):
        if self.inactive or not self.checkpoint.choose("review_requested"):
            return False
        # Reset drafts only. Persisting a stage replaces just that stage;
        # unrelated ratings and the mask's edit history remain on disk.
        for i, entry in enumerate(self.entries):
            record = q.QCRecord.load(self.anchor_for(entry))
            for stage in self.stages_for(entry):
                record.stages[stage] = {"rating": None, "issue_tags": [], "notes": ""}
            self.drafts[i] = record
        self.subject.value = 0
        self._load_subject()
        self.use_existing.disabled, self.redo.disabled = False, True
        self.message.value = "Redoing QC from stage 1. Previous ratings remain saved until you save replacements."
        return True

    @property
    def entry(self):
        return self.entries[self.subject.value]

    @property
    def record(self):
        return self.drafts[self.subject.value]

    def _load_subject(self, *_):
        if self.loading or self.inactive:
            return
        self.loading = True
        try:
            idx = self.subject.value
            if idx not in self.drafts:
                self.drafts[idx] = q.QCRecord.load(self.anchor_for(self.entry))
            stages = self.stages_for(self.entry)
            self.stage.options = [(q.STAGE_LABELS[s], s) for s in stages]
            self.stage.value = stages[0] if stages else None
            for button in self.rating_buttons.values():
                close_widget(button)
            self.rating_buttons = {}
            for stage in stages:
                button = w.ToggleButtons(options=[("—", None), ("1", 1), ("2", 2), ("3", 3)],
                    value=self.record.get_stage(stage).get("rating"),
                    description=q.STAGE_LABELS[stage], style={"description_width": "230px", "button_width": "45px"})
                button.observe(lambda change, s=stage: self._rate(s, change["new"]), names="value")
                self.rating_buttons[stage] = button
            self.rows.children = tuple(self.rating_buttons.values())
            self.repair.value = self.record.marked_for_rerun
            self.reviewer.value = self.record.reviewer or self.reviewer.value
            self.message.value = ""
        finally:
            self.loading = False
        self._load_stage()

    def _rate(self, stage, value):
        if self.loading or self.inactive:
            return
        self.record.get_stage(stage)["rating"] = value
        if stage == "skull_strip" and value == 3:
            self.repair.value = True
        if self.stage.value != stage:
            self.stage.value = stage
        else:
            self._load_stage()

    def _capture(self, *_):
        if self.loading or self.inactive or not self.entries or self.stage.value is None:
            return
        data = self.record.get_stage(self.stage.value)
        data.update(issue_tags=list(self.issues.value), notes=self.notes.value)
        self.record.marked_for_rerun = self.repair.value

    def _load_stage(self, *_):
        if self.loading or self.stage.value is None:
            return
        self.loading = True
        try:
            stage = self.stage.value
            data = self.record.get_stage(stage)
            tags, rubric = q.STAGE_VOCAB[stage]
            self.issues.options = list(tags)
            self.issues.value = tuple(t for t in data.get("issue_tags", []) if t in tags)
            self.notes.value = data.get("notes", "")
            self.reference.disabled = stage not in ("lesion", "synthstroke_lesion")
            self.synth.disabled = stage != "expert_mni_warp"
            self.help.value = "<b>" + escape(q.STAGE_LABELS[stage]) + "</b><br>" + "<br>".join(
                f"{r}: {escape(text).replace('**', '')}" for r, text in rubric.items())
            if stage == "expert_mni_warp":
                self.help.value += ("<br><b>Rate registration to MNI, not the manual delineation.</b> "
                    "Compare anatomy and native placement; agreement with a predicted lesion alone does not validate registration.")
        finally:
            self.loading = False
        self._render()

    def _render(self, *_):
        if self.loading or self.stage.value is None:
            return
        try:
            volumes = self.volumes_for(self.stage.value, self.entry,
                self.reference.value and not self.reference.disabled,
                self.synth.value and not self.synth.disabled)
            self.viewer.load_volumes(self.encode_volumes(volumes))
        except Exception as error:
            self.message.value = "Could not display this stage: " + escape(str(error))

    def _persist(self, stages):
        if self.inactive:
            self.message.value = "This QC panel was replaced. Use the newest QC panel."
            return False
        self._capture()
        missing = [q.STAGE_LABELS[s] for s in stages if self.record.get_stage(s).get("rating") not in (1, 2, 3)]
        if missing:
            self.message.value = "Choose a rating for: " + escape(", ".join(missing))
            return False
        try:
            saved = q.QCRecord.load(self.anchor_for(self.entry))
            for stage in stages:
                data = deepcopy(self.record.get_stage(stage))
                saved.set_stage(stage, rating=data["rating"],
                                issue_tags=data.get("issue_tags", []), notes=data.get("notes", ""))
            saved.subject, saved.session = self.entry["subject"], self.entry.get("session")
            saved.reviewer = self.reviewer.value.strip() or saved.reviewer
            saved.reviewed_on = date.today().isoformat()
            saved.marked_for_rerun = self.repair.value
            saved.save()
            self.record.reviewer = saved.reviewer
            # Saving ratings is itself an explicit choice to do QC.
            choice_options = ({"reviewed_entry": self.entry}
                              if self.checkpoint.choice == "existing_reused" else {})
            if self.checkpoint.choose("review_requested", **choice_options) is False:
                self.message.value = "Ratings saved, but the QC choice could not be recorded. Retry saving or choosing QC above."
                return False
        except Exception as error:
            self.message.value = "Could not save QC: " + escape(str(error))
            return False
        self.message.value = "Saved QC for " + escape(self.entry["subject"])
        return True

    def save_current(self):
        stage = self.stage.value
        if not stage or not self._persist([stage]):
            return False
        stages = list(self.rating_buttons)
        index = stages.index(stage)
        if index + 1 < len(stages):
            self.stage.value = stages[index + 1]
        else:
            self.message.value += ". Last stage; use Save & next participant."
        return True

    def save_participant(self):
        if not self._persist(list(self.rating_buttons)):
            return False
        if self.subject.value + 1 < len(self.entries):
            self.subject.value += 1  # _load_subject always selects stage 1.
        else:
            self.message.value += ". Last participant saved. Run repairs if needed, or Continue after QC."
        return True

    def _continue(self):
        if self.inactive:
            return False
        if self.checkpoint.choice is None:
            self.message.value = "Choose Use existing QC, Do QC / Redo QC, or Skip QC before continuing."
            return False
        return True

    def _prepare_repair(self):
        if self.inactive:
            return False
        if "skull_strip" in self.rating_buttons and self.repair.value:
            if not self._persist(["skull_strip"]):
                return False
        options = {"reviewed_entry": self.entry} if self.checkpoint.choice == "existing_reused" else {}
        return self.checkpoint.choose("review_requested", **options)

    def deactivate(self):
        """Prevent an old panel from resaving stale drafts after repair/reload."""
        self.inactive = True
        for control in [self.subject, self.stage, *self.rating_buttons.values(), self.reference,
                        self.synth, self.issues, self.notes, self.reviewer, self.repair,
                        self.save, self.save_next, self.repair_button, self.continue_button,
                        self.use_existing, self.redo]:
            control.disabled = True
        self.message.value = "This QC panel was replaced. Use the newest QC panel."
