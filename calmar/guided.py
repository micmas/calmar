"""Guided controls that reuse the detailed notebook's processing cells."""

import ast
import inspect
import json
from html import escape
from pathlib import Path

import ipywidgets as w
from IPython import get_ipython
from IPython.display import display, HTML
from .execution import ExecutionCheckpoint
from .notebook_navigation import NotebookNavigation

NOTEBOOK = Path(__file__).resolve().parents[1] / "lesion-interpretation-pipeline.ipynb"


def notebook_cells():
    return json.loads(NOTEBOOK.read_text())["cells"]


def source_cell(number, cells=None):
    cells = notebook_cells() if cells is None else cells
    mapping = json.loads(Path(__file__).with_name("workflow_cells.json").read_text())
    wanted = mapping[str(number)]
    return next(cell for cell in cells if cell.get("id") == wanted)


def defaults():
    tree = ast.parse("".join(source_cell(12)["source"]))
    node = next(n for n in tree.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == "CONFIG" for t in n.targets))
    return eval(compile(ast.Expression(node.value), str(NOTEBOOK), "eval"), {"Path": Path})


def normalize_selection(values):
    """Interpret form filters without constraining the manual-mask session."""
    values = dict(values)
    for key in ("SUBJECT_FILTER", "SESSION_FILTER"):
        values[key] = [v.strip() for v in values[key].split(",") if v.strip()] or None
    values["MAX_SUBJECTS"] = values["MAX_SUBJECTS"] or None
    if values["DATASET_SOURCE"] == "single":
        values.update(SUBJECT_FILTER=None, SESSION_FILTER=None,
                      MAX_SUBJECTS=1, RANDOM_SAMPLE=False, TEST_SUBJECT_IDX=0)
    elif (values["DATASET_SOURCE"] == "openneuro"
          and values["SUBJECT_FILTER"] is None and values["SESSION_FILTER"] is None):
        values["RANDOM_SAMPLE"] = True
    return values


async def run_cells(numbers, namespace, *, stop_at=None):
    """Execute canonical sources in order; never continue past an unexpected error.

    Supports notebook magics and top-level await, without nesting IPython's
    execution machinery. The guided notebook retains its own output areas.
    """
    cells = notebook_cells()
    shell = get_ipython()
    for number in numbers:
        cell = source_cell(number, cells)
        if cell["cell_type"] != "code":
            raise ValueError(f"Cell {number} is not code")
        source = "".join(cell["source"])
        if not (23 <= number <= 39 and not namespace.get("RUN_TEST", False)):
            display(HTML(f"<small>Processing step {number}</small>"))
        try:
            transformed = shell.transform_cell(source)
            compiled = compile(transformed, f"{NOTEBOOK.name}:cell-{number}", "exec",
                               flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)
            result = eval(compiled, namespace)
            if inspect.isawaitable(result):
                await result
        except Exception as error:
            if number == stop_at and isinstance(error, namespace.get("StopExecution", type(None))):
                return
            raise


def action_button(label, role, *, all_below=False):
    message = w.HTML()
    nav = NotebookNavigation(message)
    button = w.Button(description=label, button_style="primary", layout=w.Layout(width="230px"))
    button.on_click(lambda _: nav.request(role, lambda: True, all_below=all_below))
    display(w.VBox([button, message, nav]))


def pause_for_report(namespace):
    shell = get_ipython()
    previous = getattr(shell, "_calmar_report_checkpoint", None)
    if previous:
        previous.close()
    gate = ExecutionCheckpoint(shell, "Choose a participant and mask, then click Generate report.")
    shell._calmar_report_checkpoint = gate
    message = w.HTML("Choose a participant and mask above, then generate the report.")
    nav = NotebookNavigation(message, on_cell_order=gate._update_cell_order)
    button = w.Button(description="Generate report", button_style="success")
    def release():
        if namespace.get("INTERP_MASK_SOURCE") is None:
            message.value = "Choose a participant with an available MNI mask."
            return False
        gate.release()
        return True
    button.on_click(lambda _: nav.request("report-start", release, all_below=False))
    gate.controls = [message, button, nav]
    display(w.VBox(gate.controls))
    gate._cancel_queued()
    raise namespace["StopExecution"]("Choose report inputs above.")


def show_inputs(namespace):
    cfg = defaults()
    shell = get_ipython()
    previous = getattr(shell, "_calmar_inputs_checkpoint", None)
    if previous:
        previous.close()
    gate = ExecutionCheckpoint(shell, "Fill in the inputs and click Start workflow.")
    shell._calmar_inputs_checkpoint = gate
    fields = {}
    style = {"description_width": "190px"}
    layout = w.Layout(width="700px")
    def text(key, label, value=None):
        fields[key] = w.Text(value=str(cfg.get(key) or "") if value is None else value,
                            description=label, style=style, layout=layout)
    def check(key, label):
        fields[key] = w.Checkbox(value=bool(cfg.get(key)), description=label, indent=False)
    fields["DATASET_SOURCE"] = w.Dropdown(options=[("OpenNeuro", "openneuro"), ("Local BIDS", "local"),
        ("Flat T1 folder", "flat"), ("Single T1 file", "single")], value=cfg["DATASET_SOURCE"], description="Input type:")
    text("PROJECT_DIR", "Project folder:")
    text("OPENNEURO_ID", "OpenNeuro accession:")
    text("OPENNEURO_TAG", "Dataset version:")
    text("LOCAL_DATASET", "Local dataset folder:")
    text("SINGLE_T1W", "Single T1 file:")
    text("SUBJECT_FILTER", "Participants (comma-separated):", ", ".join(cfg["SUBJECT_FILTER"] or []))
    text("SESSION_FILTER", "Sessions (comma-separated):", ", ".join(cfg["SESSION_FILTER"] or []))
    fields["MAX_SUBJECTS"] = w.BoundedIntText(value=cfg["MAX_SUBJECTS"] or 0, min=0, max=100000,
        description="Participant limit (0 = all):", style=style)
    check("RUN_TEST", "Run a single-subject test before batch")
    fields["TEST_SUBJECT_IDX"] = w.BoundedIntText(value=cfg["TEST_SUBJECT_IDX"], min=0, max=99999,
        description="Test participant index (0 = first):", style=style)
    check("OVERWRITE", "Replace existing processing outputs")
    check("RANDOM_SAMPLE", "Randomly sample participants")
    text("MANUAL_MASK_PATH", "Manual mask (blank = discover):")
    fields["MANUAL_MASK_SPACE"] = w.Dropdown(options=[("T1", "t1"), ("MNI", "mni"), ("Other scan", "other")],
        value=cfg["MANUAL_MASK_SPACE"], description="Manual mask space:", style=style)
    text("MANUAL_MASK_REF", "Other reference scan:")
    fields["HDBET_MODE"] = w.Dropdown(options=["fast", "accurate"], value=cfg["HDBET_MODE"],
                                     description="Initial HD-BET:", style=style)
    check("SYNTHSTROKE_TTA", "SynthStroke test-time augmentation")
    # Give each section its own layout: the text inputs share a width layout,
    # so hiding an individual text input's layout would hide all text inputs.
    openneuro_inputs = w.VBox([fields["OPENNEURO_ID"], fields["OPENNEURO_TAG"]])
    local_inputs = w.VBox([fields["LOCAL_DATASET"]])
    single_input = w.VBox([fields["SINGLE_T1W"]])
    cohort_inputs = w.VBox([fields[key] for key in (
        "SUBJECT_FILTER", "SESSION_FILTER", "MAX_SUBJECTS", "RANDOM_SAMPLE")])
    test_index = w.VBox([fields["TEST_SUBJECT_IDX"]])

    def update_input_mode(*_):
        mode = fields["DATASET_SOURCE"].value
        for section, visible in (
            (openneuro_inputs, mode == "openneuro"),
            (local_inputs, mode in ("local", "flat")),
            (single_input, mode == "single"),
            (cohort_inputs, mode != "single"),
            (test_index, mode != "single"),
        ):
            section.layout.display = "" if visible else "none"

    fields["DATASET_SOURCE"].observe(update_input_mode, names="value")
    update_input_mode()
    sampling_note = w.HTML()
    sampling_state = {"automatic": False, "previous": fields["RANDOM_SAMPLE"].value}
    def update_sampling(*_):
        automatic = (fields["DATASET_SOURCE"].value == "openneuro"
                     and not any(p.strip() for p in fields["SUBJECT_FILTER"].value.split(","))
                     and not any(p.strip() for p in fields["SESSION_FILTER"].value.split(",")))
        if automatic and not sampling_state["automatic"]:
            sampling_state["previous"] = fields["RANDOM_SAMPLE"].value
            fields["RANDOM_SAMPLE"].value = True
        elif not automatic and sampling_state["automatic"]:
            fields["RANDOM_SAMPLE"].value = sampling_state["previous"]
        sampling_state["automatic"] = automatic
        fields["RANDOM_SAMPLE"].disabled = automatic
        sampling_note.layout.display = "none" if fields["DATASET_SOURCE"].value == "single" else ""
        sampling_note.value = (
            "<b>Random selection:</b> sample participants up to the limit and choose a session "
            "with a T1 for each. A manual mask may come from another session; its source scan "
            "will be registered to the selected T1. Limit 0 includes all participants."
            if automatic else "Sessions select T1 inputs. Manual-mask discovery can use another session of the same participant.")
    for key in ("DATASET_SOURCE", "SUBJECT_FILTER", "SESSION_FILTER"):
        fields[key].observe(update_sampling, names="value")
    update_sampling()
    message = w.HTML()
    nav = NotebookNavigation(message, on_cell_order=gate._update_cell_order)
    start = w.Button(description="Start workflow", button_style="success")
    def prepare():
        try:
            values = normalize_selection({key: widget.value for key, widget in fields.items()})
            values["RANDOM_SEED"] = cfg.get("RANDOM_SEED", 42)
            for key in ("LOCAL_DATASET", "SINGLE_T1W", "MANUAL_MASK_PATH", "MANUAL_MASK_REF"):
                values[key] = str(Path(values[key]).expanduser()) if values[key].strip() else None
            values["PROJECT_DIR"] = str(Path(values["PROJECT_DIR"]).expanduser().resolve())
            mode = values["DATASET_SOURCE"]
            if mode in ("local", "flat") and not Path(values["LOCAL_DATASET"] or "__missing__").is_dir():
                raise ValueError("Enter an existing local dataset folder.")
            if mode == "single" and not Path(values["SINGLE_T1W"] or "__missing__").is_file():
                raise ValueError("Enter an existing T1 file.")
            if mode == "openneuro" and not values["OPENNEURO_ID"].startswith("ds"):
                raise ValueError("Enter an OpenNeuro accession, for example ds004884.")
            if values["MANUAL_MASK_PATH"] and not Path(values["MANUAL_MASK_PATH"]).is_file():
                raise ValueError("The specified manual mask does not exist.")
            namespace["_CALMAR_CONFIG_OVERRIDES"] = values
            # Retain the actual user selections beside reports for repeatability.
            path = Path(values["PROJECT_DIR"]) / "reports" / "guided-inputs.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(values, indent=2) + "\n")
            gate.release()
            start.disabled = True
            for widget in fields.values():
                widget.disabled = True
            message.value = "Inputs saved. Starting workflow."
            return True
        except Exception as error:
            message.value = escape(str(error))
            return False
    start.on_click(lambda _: nav.request("guided-start", prepare,
        prompt="Start processing with these inputs? The workflow will pause at QC."))
    sections = [openneuro_inputs, local_inputs, single_input, cohort_inputs, test_index]
    gate.controls = [*fields.values(), *sections, sampling_note, start, message, nav]
    display(w.VBox([w.HTML("<b>Inputs and options</b> — leave manual mask blank to use dataset reference masks. "
                          "Leave both OpenNeuro participant/session fields blank for random selection."),
                    fields["DATASET_SOURCE"], fields["PROJECT_DIR"],
                    openneuro_inputs, local_inputs, single_input, cohort_inputs, sampling_note,
                    fields["RUN_TEST"], test_index, fields["OVERWRITE"],
                    fields["MANUAL_MASK_PATH"], fields["MANUAL_MASK_SPACE"], fields["MANUAL_MASK_REF"],
                    fields["HDBET_MODE"], fields["SYNTHSTROKE_TTA"], start, message, nav]))
    gate._cancel_queued()
