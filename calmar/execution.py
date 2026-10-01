"""Explicit notebook checkpoints, including clients that continue after errors."""

from IPython import get_ipython
from IPython.core.error import InputRejected
from IPython.display import display, Markdown
import ast
import json
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
    # Some notebook clients omit JupyterLab's optional cellId metadata.
    # Keep identity in the code too, including after edits to a cell body.
    source = parent.get("content", {}).get("code", "")
    marker = re.search(r"^# CALMAR_CELL_ID: ([A-Za-z0-9_-]+)\s*$", source, re.MULTILINE)
    if marker:
        return marker.group(1)
    # Compatibility for already-open notebooks predating the marker. Match
    # whole cells only; fragments/unknown requests still cannot unlock work.
    def unmarked(text):
        return re.sub(r"^# CALMAR_CELL_ID: [^\n]+\n?", "", text, flags=re.MULTILINE).strip()
    if source.strip():
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


def _recovery_action(lines):
    """Recognize only a standalone recovery magic, after IPython transforms it."""
    try:
        tree = ast.parse("".join(lines))
    except SyntaxError:
        return None
    for action in ("batch", "skip-qc"):
        expected = ast.parse(f"get_ipython().run_line_magic('calmar_continue', {action!r})")
        if ast.dump(tree) == ast.dump(expected):
            return action
    return None


def enable_checkpoint_recovery(shell=None):
    """Install widget-independent recovery, including for an already paused kernel.

    Installation leaves checkpoints paused and does not run processing cells.
    """
    shell = shell or get_ipython()
    if shell is None:
        raise RuntimeError("Checkpoint recovery requires an IPython kernel.")

    def recover(action):
        action = action.strip()
        if action == "batch":
            checkpoint = getattr(shell, "_calmar_batch_checkpoint", None)
            if checkpoint is None or not checkpoint.paused:
                raise RuntimeError("There is no paused batch checkpoint.")
            checkpoint._resume()
            print("Batch checkpoint released. Select the first code cell in Batch processing, "
                  "then choose Run > Run All Cells Below. Processing will pause at QC.")
        elif action == "skip-qc":
            checkpoint = getattr(shell, "_calmar_qc_checkpoint", None)
            if checkpoint is None or not checkpoint.paused:
                raise RuntimeError("There is no paused QC checkpoint.")
            if not checkpoint.choose("skipped"):
                raise RuntimeError("Could not save the QC skip decision; execution remains paused.")
            print("QC skipped by the user. The decision was saved for the final reports. "
                  "Select the next stage to run and use the notebook Run menu.")
        else:
            raise ValueError("Use %calmar_continue batch or %calmar_continue skip-qc.")

    register = getattr(shell, "register_magic_function", None)
    if callable(register):
        register(recover, magic_kind="line", magic_name="calmar_continue")
    # Upgrade the guard on existing checkpoint instances without recreating any
    # widgets or changing decisions. Useful when the browser cannot send clicks.
    for name, action in (("_calmar_batch_checkpoint", "batch"),
                         ("_calmar_qc_checkpoint", "skip-qc")):
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
        "**If the buttons remain at ‘Loading widget…’:** insert a temporary code cell "
        "and run this command by itself:\n\n"
        f"```python\n%calmar_continue {action}\n```\n\n"
        + ("This releases the batch checkpoint. Then select the first batch code cell "
           "below and choose **Run → Run All Cells Below**. Execution will pause at QC."
           if action == "batch" else
           "This explicitly skips QC and saves ‘QC skipped by user’ for the reports. "
           "It does not start subsequent processing cells."))


class ExecutionCheckpoint:
    """Reject later cells until a widget click releases this kernel's checkpoint.

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
            if action and _recovery_action(lines) == action:
                return lines
            # JupyterLab includes the executing cell's stable ID in each
            # request. Earlier cells can be edited/rerun without releasing
            # the checkpoint. Unidentified requests remain blocked.
            if _request_cell_id(self.shell) in getattr(self, "upstream_cell_ids", ()):
                return lines
            hint = (f" If widgets are unavailable, run %calmar_continue {action} "
                    "by itself in a temporary code cell." if action else "")
            raise InputRejected(self.rejection_message + hint)
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
            "to run the batch cells below. This cell has not executed.")
        self.upstream_cell_ids = _saved_upstream_ids(shell, "batch-start")
        self.message = widgets.HTML(
            "<b>⏸ Paused before batch processing.</b> Review the results above. "
            "You can rerun cells above this checkpoint while batch processing stays paused. "
            "Click <b>Continue to batch</b> to confirm Run all cells below. "
            "Processing will stop again at QC.")
        self.navigation = NotebookNavigation(self.message, on_cell_order=self._update_cell_order)
        self.button = widgets.Button(description="Continue to batch",
                                     button_style="warning",
                                     layout=widgets.Layout(width="190px"))
        self.button.on_click(self.resume)
        self.controls = [self.message, self.button, self.navigation]

    def _update_cell_order(self, ids, batch_start):
        # Use the open notebook's order, including unsaved inserted/moved cells.
        self.upstream_cell_ids = (set(ids[:ids.index(batch_start)])
                                  if batch_start in ids else set())

    def resume(self, _button=None):
        self.navigation.request("batch-start", self._resume,
            prompt="Run all cells below, starting at batch processing? Execution will pause at QC.")

    def _resume(self):
        self.release()
        self.button.disabled = True
        self.message.value = (
            "<b>Starting batch processing.</b> Execution will pause again at QC.")


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
    display(checkpoint.message, checkpoint.button, checkpoint.navigation)
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
