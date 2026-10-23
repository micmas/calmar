"""Explicit notebook checkpoints, including clients that continue after errors."""

from IPython import get_ipython
from IPython.display import display, Markdown
import ast
import json
import operator
import re
import time
from pathlib import Path
import ipywidgets as widgets
from html import escape
from uuid import uuid4

from .qc_decisions import record_qc_choice
from .notebook_navigation import NotebookNavigation
from .widget_lifecycle import close_widget


_NOTEBOOK_CELLS = globals().get("_NOTEBOOK_CELLS", {})


def _notebook_cells(name):
    """Read a complete notebook, tolerating a concurrent Jupyter autosave.

    Keep the last complete snapshot in memory. On a cold start, retry briefly;
    the navigation widget can supply the live order if disk remains unavailable.
    A failed read must never prevent checkpoint controls from being created.
    """
    path = Path(__file__).resolve().parents[1] / name
    for attempt in range(4):
        try:
            cells = json.loads(path.read_text())["cells"]
            if not isinstance(cells, list) or any("id" not in c for c in cells):
                raise ValueError("Incomplete notebook cells")
            _NOTEBOOK_CELLS[name] = cells
            return cells
        except (OSError, ValueError, KeyError, TypeError):
            if name in _NOTEBOOK_CELLS:
                return _NOTEBOOK_CELLS[name]
            if attempt < 3:
                time.sleep(.05)
    return []


def _request_cell_id(shell):
    kernel = getattr(shell, "kernel", None)
    get_parent = getattr(kernel, "get_parent", None)
    parent = get_parent() if callable(get_parent) else {}
    cell_id = parent.get("metadata", {}).get("cellId")
    if cell_id:
        return cell_id
    # Retain compatibility with notebooks saved before IDs moved out of source.
    source = parent.get("content", {}).get("code", "")
    marker = re.search(r"^# CALMAR_CELL_ID: ([A-Za-z0-9_-]+)\s*$", source, re.MULTILINE)
    if marker:
        return marker.group(1)
    # Clients that omit cellId can use the frontend's live source/ID mapping,
    # including unsaved edits. Whole-cell matching keeps unknown requests blocked.
    def unmarked(text):
        return re.sub(r"^# CALMAR_CELL_ID: [^\n]+\n?", "", text, flags=re.MULTILINE).strip()
    if source.strip():
        matches = [cell_id for cell_id, text in getattr(shell, '_calmar_live_cell_sources', {}).items()
                   if unmarked(text) == unmarked(source)]
        if len(matches) == 1:
            return matches[0]
        for name in ("lesion-interpretation-pipeline.ipynb", "calmar-guided.ipynb"):
            matches = [cell["id"] for cell in _notebook_cells(name)
                       if cell["cell_type"] == "code" and unmarked("".join(cell["source"])) == unmarked(source)]
            if len(matches) == 1:
                return matches[0]
    return None


def _saved_upstream_ids(shell, boundary_role=None):
    """Bootstrap the boundary without waiting for the notebook widget to load."""
    current = _request_cell_id(shell)
    if not current:
        return set()
    for name in ("lesion-interpretation-pipeline.ipynb", "calmar-guided.ipynb"):
        cells = _notebook_cells(name)
        ids = [cell["id"] for cell in cells]
        if current not in ids:
            continue
        if boundary_role is None:
            return set(ids[:ids.index(current) + 1])
        boundaries = [i for i, cell in enumerate(cells)
                      if cell.get("metadata", {}).get("calmar", {}).get("role") == boundary_role]
        if len(boundaries) == 1:
            return set(ids[:boundaries[0]])
    return set()


# Recovery commands a paused checkpoint accepts: the batch checkpoint can be
# released towards batch processing or towards reporting (its two buttons).
# The report form's checkpoint is released by "generate", its Generate button.
RECOVERY_COMMANDS = {"batch": ("batch", "report"), "skip-qc": ("skip-qc",), "generate": ("generate",)}
_MISSING = object()


def _open_report_setup(shell, *, reset_selection=True):
    """Open report selection without changing any saved QC decision.

    This is shared by the live batch-checkpoint button and the text recovery
    command.  Keeping it independent of a *paused* BatchCheckpoint lets a
    user recover from a stale notebook widget after that checkpoint has
    already been released, as long as the kernel still has a valid selected
    single-subject index.
    """
    namespace = getattr(shell, "user_ns", {})
    waiting = [(name, getattr(shell, name, None)) for name in
               ("_calmar_qc_checkpoint", "_calmar_report_checkpoint")]
    if any(name == "_calmar_qc_checkpoint" and gate is not None and gate.paused
           for name, gate in waiting):
        raise RuntimeError(
            "Quality control is waiting for a decision. Finish QC or use "
            "%calmar_continue skip-qc; reporting was not opened."
        )
    if any(name == "_calmar_report_checkpoint" and gate is not None and gate.paused
           for name, gate in waiting):
        raise RuntimeError(
            "The report form is waiting for validated inputs. Use "
            "%calmar_continue generate [participant] [mask]; reporting was not reopened."
        )
    candidate = (namespace.get("TEST_SUBJECT_IDX", _MISSING) if reset_selection else
                 namespace.get("INTERP_SUBJECT_IDX", namespace.get("TEST_SUBJECT_IDX", _MISSING)))
    try:
        if candidate is _MISSING or isinstance(candidate, bool):
            raise TypeError
        index = operator.index(candidate)
    except TypeError:
        raise RuntimeError(
            "No single-subject selection is available. Rerun the participant "
            "selection cell, then run the single-subject checkpoint cell."
        )
    subjects = namespace.get("SUBJECTS")
    if subjects is None:
        raise RuntimeError(
            "No participant cohort is available. Rerun participant discovery "
            "and selection before opening reporting."
        )
    if not 0 <= index < len(subjects):
        raise RuntimeError(
            "The selected participant is no longer in the current cohort. "
            "Rerun the participant selection cell before opening reporting."
        )
    # Release old in-memory gates without changing any saved QC decisions.
    for _, previous in waiting:
        if previous is not None:
            previous.close()
    namespace["INTERP_SUBJECT_IDX"] = index
    return index


def _recovery_action(lines):
    """Recognize only a standalone recovery magic, after IPython transforms it."""
    try:
        tree = ast.parse("".join(lines))
    except SyntaxError:
        return None
    for action in ("batch", "report", "skip-qc"):
        expected = ast.parse(f"get_ipython().run_line_magic('calmar_continue', {action!r})")
        if ast.dump(tree) == ast.dump(expected):
            return action
    # "generate" may name the participant and mask: %calmar_continue generate sub-01 manual
    body = tree.body[0].value if len(tree.body) == 1 and isinstance(tree.body[0], ast.Expr) else None
    if isinstance(body, ast.Call) and len(body.args) == 2 and isinstance(body.args[1], ast.Constant) \
            and isinstance(body.args[1].value, str) and body.args[1].value.split()[:1] == ["generate"]:
        expected = ast.parse("get_ipython().run_line_magic('calmar_continue', 'generate')").body[0].value
        if ast.dump(body.func) == ast.dump(expected.func) and ast.dump(body.args[0]) == ast.dump(expected.args[0]):
            return "generate"
    return None


def enable_checkpoint_recovery(shell=None):
    """Install widget-independent recovery, including for an already paused kernel.

    Installation leaves checkpoints paused and does not run processing cells.
    """
    shell = shell or get_ipython()
    if shell is None:
        raise RuntimeError("Checkpoint recovery requires an IPython kernel.")

    def recover(line):
        action, *arguments = line.split() or [""]
        if action == "batch":
            checkpoint = getattr(shell, "_calmar_batch_checkpoint", None)
            if checkpoint is None or not checkpoint.paused:
                raise RuntimeError("There is no paused batch checkpoint.")
            checkpoint._resume()
            print("Batch checkpoint released. Select the first code cell in Batch processing, "
                  "then choose Run > Run All Cells Below. Processing will pause at QC.")
        elif action == "report":
            # The code equivalent of the "Jump to reporting" button.
            checkpoint = getattr(shell, "_calmar_batch_checkpoint", None)
            if checkpoint is not None and checkpoint.paused:
                if checkpoint._report() is False:
                    raise RuntimeError(checkpoint._report_error)
            else:
                # The saved widget can outlive the paused state (for example,
                # after Continue to batch was already chosen).  The explicit
                # recovery command should still open report selection rather
                # than fail on that stale control.
                _open_report_setup(shell, reset_selection=False)
            print("Reporting opened; saved QC is unchanged.\n"
                  "Next, run these cells one by one (Shift+Enter), not Run All Below:\n"
                  "  1. the report settings cell ('Settings for the participant interpretation report'),\n"
                  "  2. the report form cell, choose the participant and mask, click Generate;\n"
                  "     or, without the form, run a cell such as\n"
                  "       INTERP_SUBJECT_IDX = [e['subject'] for e in SUBJECTS].index('sub-...')\n"
                  "       INTERP_MASK_SOURCE = 'manual'\n"
                  "     and then the report cell ('Generate the interpretation report ...').")
        elif action == "generate":
            # The code equivalent of the "Generate participant report" button.
            panel = getattr(shell, "_calmar_report_inputs", None)
            if panel is None or panel.gate is None or not panel.gate.paused:
                raise RuntimeError("There is no report form waiting; run the report form cell first.")
            if len(arguments) > 2:
                raise ValueError("Use %calmar_continue generate [participant] [mask].")
            if arguments:
                panel.choose_participant(arguments[0])
            if len(arguments) > 1:
                panel.choose_mask(arguments[1])
            if panel.approve() is False:
                raise RuntimeError(panel.message.value)
            print(f"Report inputs accepted: {panel.subject.label} · {panel.source.label} mask · "
                  f"{panel.atlas.value} atlas · evidence: {panel.evidence.label}.\n"
                  "Now run the report cell ('Generate the interpretation report ...') with Shift+Enter.")
        elif action == "skip-qc":
            checkpoint = getattr(shell, "_calmar_qc_checkpoint", None)
            if checkpoint is None or not checkpoint.paused:
                raise RuntimeError("There is no paused QC checkpoint.")
            if not checkpoint.choose("skipped"):
                raise RuntimeError("Could not save the QC skip decision; execution remains paused.")
            print("QC skipped by the user. The decision was saved for the final reports. "
                  "Select the next stage to run and use the notebook Run menu.")
        else:
            raise ValueError("Use %calmar_continue batch, report, generate or skip-qc.")

    register = getattr(shell, "register_magic_function", None)
    if callable(register):
        register(recover, magic_kind="line", magic_name="calmar_continue")
    # Upgrade the guard on existing checkpoint instances without recreating any
    # widgets or changing decisions. Useful when the browser cannot send clicks.
    for name, action in (("_calmar_batch_checkpoint", "batch"),
                         ("_calmar_qc_checkpoint", "skip-qc"),
                         ("_calmar_report_checkpoint", "generate")):
        checkpoint = getattr(shell, name, None)
        if checkpoint is not None:
            checkpoint.recovery_action = action
            if action == "batch" and not hasattr(checkpoint, "upstream_cell_ids"):
                checkpoint.upstream_cell_ids = _saved_upstream_ids(shell, "batch-start")
            if checkpoint.paused and checkpoint.guard in shell.input_transformers_post:
                index = shell.input_transformers_post.index(checkpoint.guard)
                checkpoint.guard = ExecutionCheckpoint._reject_while_paused.__get__(checkpoint)
                shell.input_transformers_post[index] = checkpoint.guard


def recovery_instructions(action):
    return Markdown(
        "**If the buttons do not respond (‘Loading widget…’ or ‘Waiting…’):** insert a temporary code cell "
        "and run this command by itself:\n\n"
        f"```python\n%calmar_continue {action}\n```\n\n"
        + ("This releases the batch checkpoint. Then select the first batch code cell "
           "below and choose **Run → Run All Cells Below**. Execution will pause at QC.\n\n"
           "To go to reporting instead (the **Jump to reporting** button), run "
           "`%calmar_continue report` by itself, then run the report cells one by one."
           if action == "batch" else
           "This does what **Generate participant report** does, with the form's current "
           "choices. To choose without the form, add the participant and the mask, e.g. "
           "`%calmar_continue generate sub-01 manual`. Then run the report cell below "
           "(Shift+Enter)."
           if action == "generate" else
           "This explicitly skips QC and saves ‘QC skipped by user’ for the reports. "
           "It does not start subsequent processing cells."))


class ExecutionCheckpoint:
    """Skip later cells until a widget click releases this kernel's checkpoint.

    Widget comm messages remain available while cell execution is blocked.
    Raising an exception alone depends on the client's stop_on_error setting.
    """

    def __init__(self, shell, rejection_message):
        self.shell = shell
        self.boundary_cell_id = _request_cell_id(shell)
        self.upstream_cell_ids = _saved_upstream_ids(shell)
        self.paused = True
        self.rejection_message = rejection_message
        self.controls = []
        self.guard = self._reject_while_paused
        self.shell.input_transformers_post.append(self.guard)

    def _update_cell_order(self, ids, _batch_start=None):
        # Include the checkpoint cell itself so its controls/viewers can be
        # rebuilt. Everything after it still requires the explicit choice.
        boundary = self.boundary_cell_id
        self.upstream_cell_ids = (set(ids[:ids.index(boundary) + 1])
                                  if boundary in ids else set())

    def _reject_while_paused(self, lines):
        if self.paused:
            action = getattr(self, "recovery_action", None)
            if action and _recovery_action(lines) in RECOVERY_COMMANDS.get(action, (action,)):
                return lines
            # JupyterLab includes the executing cell's stable ID in each
            # request. Earlier cells can be edited/rerun without releasing
            # the checkpoint. Unidentified requests remain blocked.
            if _request_cell_id(self.shell) in getattr(self, "upstream_cell_ids", ()):
                return lines
            hint = (f" If widgets are unavailable, run %calmar_continue "
                    f"{' or %calmar_continue '.join(RECOVERY_COMMANDS.get(action, (action,)))} "
                    "by itself in a temporary code cell." if action else "")
            # Some clients keep sending Run All requests after the pause.
            # Do not execute their contents or flood the notebook with error
            # tracebacks for an intentional checkpoint.
            if not getattr(self, '_pause_notice_shown', False):
                print(self.rejection_message + hint)
                self._pause_notice_shown = True
            return ['pass\n']
        return lines

    def _cancel_queued(self):
        # ipykernel's normal error path calls this only with stop_on_error=True.
        # Cancel already queued requests even when the client disables it.
        # The persistent input guard also rejects requests submitted later.
        abort = getattr(getattr(self.shell, "kernel", None), "_abort_queues", None)
        if callable(abort):
            abort()

    def release(self):
        if not self.paused:
            return
        # Discard old requests before a deliberately requested continuation.
        self._cancel_queued()
        self.paused = False
        if self.guard in self.shell.input_transformers_post:
            self.shell.input_transformers_post.remove(self.guard)

    def close(self):
        self.paused = False
        if self.guard in self.shell.input_transformers_post:
            self.shell.input_transformers_post.remove(self.guard)
        for control in self.controls:
            close_widget(control)


class BatchCheckpoint(ExecutionCheckpoint):
    def __init__(self, shell):
        self.recovery_action = "batch"
        enable_checkpoint_recovery(shell)
        super().__init__(shell,
            "Execution is paused before batch processing. Click 'Continue to batch', "
            "or 'Jump to reporting' at the checkpoint. This cell has not executed.")
        self.upstream_cell_ids = _saved_upstream_ids(shell, "batch-start")
        self.message = widgets.HTML(
            "<b>⏸ Paused before batch processing.</b> Review the results above. "
            "You can rerun cells above this checkpoint while batch processing stays paused. "
            "Click <b>Continue to batch</b> to confirm Run all cells below. "
            "Processing will stop again at QC. Or choose <b>Jump to reporting</b> to open report "
            "setup and selection without running the batch processing cells. "
            "This does not mark QC as completed.")
        self.navigation = NotebookNavigation(self.message, on_cell_order=self._update_cell_order,
                                             on_error=self._retry_controls)
        self.button = widgets.Button(description="Continue to batch",
                                     button_style="warning",
                                     layout=widgets.Layout(width="190px"))
        self.button.on_click(self.resume)
        self.reporting = widgets.Button(description="Jump to reporting",
                                       layout=widgets.Layout(width="190px"))
        self.reporting.on_click(self.report)
        from .method_choice import MethodChoice
        config = getattr(shell, 'user_ns', {}).get('CONFIG')
        self.methods = MethodChoice(config, on_change=self._methods_changed) if config is not None else None
        self.controls = [self.message, self.button, self.reporting, self.navigation]
        self.widget = widgets.VBox([self.message, *([self.methods.widget] if self.methods else []),
                                    widgets.HBox([self.button, self.reporting]), self.navigation])
        self.controls.append(self.widget)

    def _update_cell_order(self, ids, batch_start):
        # Use the open notebook's order, including unsaved inserted/moved cells.
        self.upstream_cell_ids = (set(ids[:ids.index(batch_start)])
                                  if batch_start in ids else set())

    def resume(self, _button=None):
        self.navigation.request("batch-start", self._resume)

    def _methods_changed(self, valid):
        self.button.disabled = not valid

    def _retry_controls(self):
        self.button.disabled = self.reporting.disabled = False

    def _resume(self):
        if self.methods and not self.methods.valid:
            self.message.value = '<b>Choose at least one lesion segmentation.</b>'
            return False
        self.release()
        if self.methods:
            self.methods.disable()
        self.button.disabled = True
        self.reporting.disabled = True
        self.message.value = (
            "<b>Starting batch processing</b>"
            + (f" ({self.methods.summary()})" if self.methods else "") + ". Execution will pause again at QC.")

    def report(self, _button=None):
        self.navigation.request('report-setup', self._report)

    def _report(self):
        try:
            _open_report_setup(self.shell)
        except RuntimeError as error:
            self._report_error = str(error)
            self.message.value = f"<b>Could not open reporting:</b> {escape(str(error))}"
            return False
        self.release()
        self.button.disabled = self.reporting.disabled = True
        self.message.value = ('<b>Opening report setup.</b> '
                              'Choose the participant and mask in the report selector. Saved QC is unchanged.')
        return True


class QCCheckpoint(ExecutionCheckpoint):
    def __init__(self, shell, entries, directory_for):
        self.recovery_action = "skip-qc"
        enable_checkpoint_recovery(shell)
        super().__init__(shell,
            "Execution is paused for quality control. Use existing QC, choose Do QC / Redo QC, or Skip QC there. "
            "This cell has not executed.")
        # Freeze the cohort and paths so later notebook cells cannot change
        # which participants a button click applies to.
        self.targets = [(dict(entry), directory_for(entry)) for entry in entries]
        self.checkpoint_id = str(uuid4())
        self.choice = None
        self._choice_targets = None
        self.message = widgets.HTML(
            "<b>⏸ QC decision required for the current cohort.</b> "
            "Choose <b>Do QC</b> to review/save ratings and run any repairs manually, "
            "or <b>Skip QC</b> to continue with a skip note in the reports. "
            "Neither button starts subsequent cells.")
        self.do_qc = widgets.Button(description="Do QC", button_style="primary")
        self.skip_qc = widgets.Button(description="Skip QC", button_style="warning")
        self.do_qc.on_click(lambda _: self.choose("review_requested"))
        self.skip_qc.on_click(lambda _: self.choose("skipped"))
        self.controls = [self.message, self.do_qc, self.skip_qc]

    def choose(self, choice, *, existing_entries=(), reviewed_entry=None):
        existing = {(e["subject"], e.get("session") or "") for e in existing_entries}
        targets = [(entry, directory, "review_requested" if choice == "existing_reused"
                    and (entry["subject"], entry.get("session") or "") not in existing else choice)
                   for entry, directory in self.targets]
        selected_choice = choice
        if reviewed_entry is not None and self.choice == "existing_reused":
            # Saving a newly reviewed participant must not relabel other
            # participants' reused QC as a fresh review.
            selected_choice = self.choice
            key = (reviewed_entry["subject"], reviewed_entry.get("session") or "")
            targets = [(entry, directory, choice if (entry["subject"], entry.get("session") or "") == key
                        else self._choice_targets[i]) for i, (entry, directory, _) in enumerate(targets)]
        target_choices = tuple(action for _, _, action in targets)
        if choice == "existing_reused" and "existing_reused" not in target_choices:
            self.message.value = "No saved QC is available to reuse. Choose Do QC or Skip QC."
            return False
        if selected_choice == self.choice and target_choices == self._choice_targets:
            return True
        action_id = str(uuid4()) if self.choice else self.checkpoint_id
        try:
            for entry, directory, action in targets:
                record_qc_choice(directory, entry, action, action_id)
        except Exception as error:
            self.message.value = (
                "<b>Could not save the QC choice; execution remains paused.</b> "
                + escape(str(error)))
            return False
        self.release()
        self.choice = selected_choice
        self._choice_targets = target_choices
        self.do_qc.disabled = choice == "review_requested"
        self.skip_qc.disabled = choice == "skipped"
        if choice == "skipped":
            self.message.value = (
                "<b>QC was skipped by the user.</b> This choice is saved for each "
                "participant/session and will appear in newly generated reports.")
        elif choice == "existing_reused":
            self.message.value = (
                "<b>Existing QC retained.</b> Review any unrated stages below and any repair flags, "
                "then use Continue after QC. Reusing ratings is recorded separately from skipping QC.")
        else:
            self.message.value = (
                "<b>QC review selected.</b> Review and save ratings below. Run any "
                "needed repairs and recheck the results before continuing. "
                "Requesting review does not mark it complete.")
        return True


def pause_before_batch():
    shell = get_ipython()
    if shell is None:
        raise RuntimeError("The batch checkpoint requires an IPython notebook kernel.")
    previous = getattr(shell, "_calmar_batch_checkpoint", None)
    if previous is not None:
        previous.close()
    checkpoint = BatchCheckpoint(shell)
    shell._calmar_batch_checkpoint = checkpoint
    display(checkpoint.widget)
    display(recovery_instructions("batch"))
    checkpoint._cancel_queued()
    return checkpoint


def pause_for_qc(entries, directory_for, *, display_controls=True):
    shell = get_ipython()
    if shell is None:
        raise RuntimeError("The QC checkpoint requires an IPython notebook kernel.")
    previous = getattr(shell, "_calmar_qc_checkpoint", None)
    if previous is not None:
        previous.close()
    checkpoint = QCCheckpoint(shell, entries, directory_for)
    shell._calmar_qc_checkpoint = checkpoint
    if display_controls:
        checkpoint.navigation = NotebookNavigation(
            checkpoint.message, on_cell_order=checkpoint._update_cell_order)
        checkpoint.controls.append(checkpoint.navigation)
        display(*checkpoint.controls)
    display(recovery_instructions("skip-qc"))
    checkpoint._cancel_queued()
    return checkpoint
