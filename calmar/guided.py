"""Guided controls that reuse the detailed notebook's processing cells."""

import ast
import inspect
import json
import time
from html import escape
from pathlib import Path

import ipywidgets as w
from IPython import get_ipython
from IPython.display import display, HTML
from .execution import ExecutionCheckpoint
from .notebook_navigation import NotebookNavigation
from .timing import step_title

NOTEBOOK = Path(__file__).resolve().parents[1] / "lesion-interpretation-pipeline.ipynb"
SOURCE_OPTIONS = {
    "t1": [("OpenNeuro", "openneuro"), ("Local BIDS", "local"),
           ("Flat T1 folder", "flat"), ("Single T1 file", "single")],
    "dwi": [("ISLES 2022 (local)", "isles2022"),
            ("OpenNeuro", "openneuro"), ("Local BIDS", "local")],
}


def initial_input_route(config):
    """Route whose source options can represent the configured default."""
    return "dwi" if config.get("DATASET_SOURCE") == "isles2022" else config.get("MODALITY", "t1")


def set_route_source_options(widget, route):
    """Change valid input sources without resetting a still-valid selection."""
    options = SOURCE_OPTIONS[route]
    current = widget.value
    widget._calmar_swapping_options = True
    try:
        if list(widget.options) != options:
            widget.options = options
        values = [value for _, value in options]
        widget.value = current if current in values else "local"
    finally:
        widget._calmar_swapping_options = False


def validate_isles_input(root, sub_filter=None, ses_filter=None):
    """Validate an extracted ISLES root and return the requested DWI+ADC pairs."""
    from .study import discover_dwi
    root = Path(root)
    if not root.is_dir():
        raise ValueError("Enter an existing local dataset folder.")
    all_pairs = discover_dwi(root)
    if not all_pairs:
        raise ValueError(
            "No ISLES-style DWI+ADC pairs were found. Choose the extracted dataset root "
            "containing sub-strokecase*/ses-*/dwi/*_dwi.nii.gz and sibling *_adc.nii.gz files."
        )
    if not (root / "derivatives").is_dir():
        nested = sorted(path.parent for path in root.glob("*/derivatives")
                        if any(path.parent.glob("sub-strokecase*")))
        if nested:
            raise ValueError(
                f"The ISLES dataset is nested. Choose {nested[0]} as the dataset folder "
                "so its sub-strokecase* and derivatives/ folders share one root."
            )
    pairs = discover_dwi(root, sub_filter, ses_filter)
    if not pairs:
        raise ValueError(
            f"Found {len(all_pairs)} ISLES DWI+ADC pairs, but none match the participant/session filters. "
            "Clear or change those filters."
        )
    return pairs


def notebook_cells():
    return json.loads(NOTEBOOK.read_text())["cells"]


def cell_id(key):
    """A notebook cell id, from the id itself or a legacy cell number."""
    if isinstance(key, str) and key.startswith("calmar-"):
        return key
    mapping = json.loads(Path(__file__).with_name("workflow_cells.json").read_text())
    return mapping[str(key)]


def source_cell(number, cells=None):
    """The detailed notebook's cell, by id ("calmar-...") or legacy number."""
    cells = notebook_cells() if cells is None else cells
    wanted = cell_id(number)
    return next(cell for cell in cells if cell.get("id") == wanted)


# Cells of the optional single-subject test (their titles are hidden when skipped).
TEST_CELLS = {"calmar-step-23", "calmar-step-25", "calmar-step-27", "calmar-registration", "calmar-openads", "calmar-manual",
              "calmar-step-32", "calmar-step-34", "calmar-step-35", "calmar-step-39"}


def defaults():
    tree = ast.parse("".join(source_cell(12)["source"]))
    node = next(n for n in tree.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == "CONFIG" for t in n.targets))
    return eval(compile(ast.Expression(node.value), str(NOTEBOOK), "eval"), {"Path": Path})


from .method_choice import METHOD_CHOICES


def normalize_selection(values):
    """Interpret form filters without constraining the manual-mask session."""
    values = dict(values)
    # ISLES 2022 is a DWI+ADC dataset with no T1w input. Keep its guided source
    # self-contained: choosing it always selects the compatible OpenADS route.
    if values.get("DATASET_SOURCE") == "isles2022":
        values["MODALITY"] = "dwi"
    for key in ("SUBJECT_FILTER", "SESSION_FILTER"):
        values[key] = [v.strip() for v in values[key].split(",") if v.strip()] or None
    values["MAX_SUBJECTS"] = values["MAX_SUBJECTS"] or None
    # The DWI route currently has one eligible method; the T1 route exposes one
    # checkbox per automatic segmentation.
    if values.get("MODALITY", "t1") == "dwi":
        for method in METHOD_CHOICES:
            values.pop(f"_method_{method}", None)
        values["SEGMENTATION_METHODS"] = ["openads"]
    elif any(f"_method_{m}" in values for m in METHOD_CHOICES):
        values["SEGMENTATION_METHODS"] = [m for m in METHOD_CHOICES if values.pop(f"_method_{m}", False)]
        if not values["SEGMENTATION_METHODS"]:
            raise ValueError("Choose at least one lesion segmentation (LINDA or SynthStroke).")
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
    stop_at = cell_id(stop_at) if stop_at is not None else None
    for number in numbers:
        cell = source_cell(number, cells)
        number = cell["id"]
        if cell["cell_type"] != "code":
            raise ValueError(f"Cell {number} is not code")
        source = "".join(cell["source"])
        if not (number in TEST_CELLS and not namespace.get("RUN_TEST", False)):
            display(HTML(f"<small>{escape(step_title(cell['id']))}</small>"))
        started = time.perf_counter()
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
        finally:
            if number != "calmar-step-10":
                namespace.setdefault('STEP_TIMINGS', {})[cell['id']] = time.perf_counter() - started


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
    initial_route = initial_input_route(cfg)
    fields["DATASET_SOURCE"] = w.Dropdown(options=SOURCE_OPTIONS[initial_route], value=cfg["DATASET_SOURCE"],
                                           description="Input type:")
    fields["MODALITY"] = w.Dropdown(
        options=[("T1w — LINDA / SynthStroke", "t1"), ("DWI + ADC — OpenADS", "dwi")],
        value=initial_route, description="Imaging route:", style=style)
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
    check("OVERWRITE", "Replace existing processing outputs")
    check("RANDOM_SAMPLE", "Randomly sample participants")
    text("MANUAL_MASK_PATH", "Manual mask (blank = discover):")
    fields["MANUAL_MASK_SPACE"] = w.Dropdown(options=[("Native processing image (T1w or DWI)", "t1"),
                                                       ("MNI", "mni"), ("Other scan", "other")],
        value=cfg["MANUAL_MASK_SPACE"], description="Manual mask space:", style=style)
    text("MANUAL_MASK_REF", "Other reference scan:")
    fields["HDBET_MODE"] = w.Dropdown(options=["fast", "accurate"], value=cfg["HDBET_MODE"],
                                     description="Initial HD-BET:", style=style)
    check("SYNTHSTROKE_TTA", "SynthStroke test-time augmentation")
    selected = cfg.get("SEGMENTATION_METHODS") or list(METHOD_CHOICES)
    for method, label in METHOD_CHOICES.items():
        fields[f"_method_{method}"] = w.Checkbox(value=method in selected, description=label, indent=False,
                                                 layout=w.Layout(width="700px"))
    # Give each section its own layout: the text inputs share a width layout,
    # so hiding an individual text input's layout would hide all text inputs.
    openneuro_inputs = w.VBox([fields["OPENNEURO_ID"], fields["OPENNEURO_TAG"]])
    local_inputs = w.VBox([fields["LOCAL_DATASET"]])
    single_input = w.VBox([fields["SINGLE_T1W"]])
    cohort_inputs = w.VBox([fields[key] for key in (
        "SUBJECT_FILTER", "SESSION_FILTER", "MAX_SUBJECTS", "RANDOM_SAMPLE")])
    method_inputs = w.VBox([w.HTML("<b>Lesion segmentation</b> (at least one):"),
                            *[fields[f"_method_{m}"] for m in METHOD_CHOICES],
                            fields["HDBET_MODE"], fields["SYNTHSTROKE_TTA"]])
    route_note = w.HTML()
    isles_note = w.HTML(
        "<b>ISLES 2022:</b> choose the extracted dataset root containing "
        "<code>sub-strokecase*</code> and <code>derivatives/</code>. CALMaR checks for "
        "sibling DWI/ADC pairs and recognises the official <code>*_msk.nii.gz</code> expert masks."
    )
    default_subjects = ", ".join(cfg["SUBJECT_FILTER"] or [])
    default_sessions = ", ".join(cfg["SESSION_FILTER"] or [])
    isles_state = {"active": False, "previous_filters": None, "auto_path": None}

    def update_route(*_):
        route = fields["MODALITY"].value
        leaving_isles = route == "t1" and fields["DATASET_SOURCE"].value == "isles2022"
        set_route_source_options(fields["DATASET_SOURCE"], route)
        if leaving_isles:
            fields["DATASET_SOURCE"].value = "openneuro"
        if (route == "dwi" and fields["DATASET_SOURCE"].value == "openneuro"
                and fields["OPENNEURO_ID"].value == str(cfg.get("OPENNEURO_ID") or "")):
            fields["DATASET_SOURCE"].value = "isles2022"
        method_inputs.layout.display = "" if route == "t1" else "none"
        route_note.value = (
            "<b>DWI route:</b> OpenADS requires a DWI with an exact sibling ADC map. "
            "Regardless of route, the fetch step inventories every DWI series for each selected participant, "
            "including other sessions, without treating an ordinary diffusion series as OpenADS-ready. "
            "For the ISLES 2022 example, choose <b>ISLES 2022 (local)</b> below."
            if route == "dwi" else
            "<b>T1w route:</b> the fetch step also inventories any DWI series for each selected participant, "
            "including other sessions; these are reported separately from the T1w processing input.")
        update_input_mode()

    fields["MODALITY"].observe(update_route, names="value")

    def update_input_mode(*_):
        if getattr(fields["DATASET_SOURCE"], "_calmar_swapping_options", False):
            return
        mode = fields["DATASET_SOURCE"].value
        entering_isles = mode == "isles2022" and not isles_state["active"]
        leaving_isles = mode != "isles2022" and isles_state["active"]
        if entering_isles:
            isles_state["previous_filters"] = (
                fields["SUBJECT_FILTER"].value, fields["SESSION_FILTER"].value)
            if (fields["SUBJECT_FILTER"].value == default_subjects
                    and fields["SESSION_FILTER"].value == default_sessions):
                fields["SUBJECT_FILTER"].value = ""
                fields["SESSION_FILTER"].value = ""
        elif leaving_isles and isles_state["previous_filters"] is not None:
            fields["SUBJECT_FILTER"].value, fields["SESSION_FILTER"].value = isles_state["previous_filters"]
            if (isles_state["auto_path"] is not None
                    and fields["LOCAL_DATASET"].value == isles_state["auto_path"]):
                fields["LOCAL_DATASET"].value = ""
        isles_state["active"] = mode == "isles2022"
        for section, visible in (
            (openneuro_inputs, mode == "openneuro"),
            (local_inputs, mode in ("local", "flat", "isles2022")),
            (single_input, mode == "single"),
            (cohort_inputs, mode != "single"),
            (isles_note, mode == "isles2022"),
        ):
            section.layout.display = "" if visible else "none"
        if mode == "isles2022" and not fields["LOCAL_DATASET"].value.strip():
            project = Path(fields["PROJECT_DIR"].value).expanduser()
            candidates = (project / "data" / "ISLES-2022", project / "ISLES-2022")
            candidate = next((path for path in candidates if path.is_dir()), candidates[0])
            fields["LOCAL_DATASET"].value = str(candidate)
            isles_state["auto_path"] = str(candidate)

    fields["DATASET_SOURCE"].observe(update_input_mode, names="value")
    update_route()
    update_input_mode()
    sampling_note = w.HTML()
    sampling_state = {"automatic": False, "previous": fields["RANDOM_SAMPLE"].value}
    def update_sampling(*_):
        if getattr(fields["DATASET_SOURCE"], "_calmar_swapping_options", False):
            return
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
        if fields["MODALITY"].value == "dwi":
            sampling_note.value = (
                "Participants and sessions select DWI+ADC inputs. ISLES expert masks are native to the DWI; "
                "other manual masks must declare their source space."
            )
        else:
            sampling_note.value = (
                "<b>Random selection:</b> sample participants up to the limit and choose a session "
                "with a T1 for each. A manual mask may come from another session; its source scan "
                "will be registered to the selected T1. Limit 0 includes all participants."
                if automatic else
                "Sessions select T1 inputs. Manual-mask discovery can use another session of the same participant.")
    for key in ("DATASET_SOURCE", "MODALITY", "SUBJECT_FILTER", "SESSION_FILTER"):
        fields[key].observe(update_sampling, names="value")
    update_sampling()
    message = w.HTML()
    nav = NotebookNavigation(message, on_cell_order=gate._update_cell_order)
    start = w.Button(description="Start workflow", button_style="success")
    def prepare():
        try:
            values = normalize_selection({key: widget.value for key, widget in fields.items()})
            # The guided form deliberately describes one route.  Additional
            # cohorts belong to the full notebook's explicit configuration.
            values["ADDITIONAL_COHORTS"] = []
            values["RANDOM_SEED"] = cfg.get("RANDOM_SEED", 42)
            for key in ("LOCAL_DATASET", "SINGLE_T1W", "MANUAL_MASK_PATH", "MANUAL_MASK_REF"):
                values[key] = str(Path(values[key]).expanduser()) if values[key].strip() else None
            values["PROJECT_DIR"] = str(Path(values["PROJECT_DIR"]).expanduser().resolve())
            mode = values["DATASET_SOURCE"]
            if mode in ("local", "flat", "isles2022") and not Path(values["LOCAL_DATASET"] or "__missing__").is_dir():
                raise ValueError("Enter an existing local dataset folder.")
            if mode == "isles2022":
                validate_isles_input(values["LOCAL_DATASET"], values.get("SUBJECT_FILTER"),
                                     values.get("SESSION_FILTER"))
            elif mode in ("local", "flat"):
                if values["MODALITY"] == "t1":
                    from .study import discover_t1w
                    found = discover_t1w(values["LOCAL_DATASET"], values.get("SUBJECT_FILTER"),
                                         values.get("SESSION_FILTER"), cfg.get("T1W_SELECTION", "first"))
                    if not found:
                        raise ValueError(
                            "No T1w images match this local dataset and participant/session selection."
                        )
                else:
                    from .study import discover_dwi
                    if not discover_dwi(values["LOCAL_DATASET"], values.get("SUBJECT_FILTER"),
                                        values.get("SESSION_FILTER")):
                        raise ValueError(
                            "No DWI images with sibling ADC maps match this local dataset and selection."
                        )
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
    sections = [openneuro_inputs, local_inputs, single_input, cohort_inputs,
                method_inputs, route_note, isles_note]
    gate.controls = [*fields.values(), *sections, sampling_note, start, message, nav]
    display(w.VBox([w.HTML("<b>Inputs and options</b> — leave manual mask blank to use dataset reference masks. "
                          "Leave both OpenNeuro participant/session fields blank for random selection."),
                    fields["MODALITY"], route_note,
                    fields["DATASET_SOURCE"], fields["PROJECT_DIR"],
                    openneuro_inputs, local_inputs, isles_note, single_input, cohort_inputs, sampling_note,
                    fields["RUN_TEST"], fields["OVERWRITE"],
                    fields["MANUAL_MASK_PATH"], fields["MANUAL_MASK_SPACE"], fields["MANUAL_MASK_REF"],
                    method_inputs, start, message, nav]))
    gate._cancel_queued()
