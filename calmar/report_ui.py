"""Report inputs and presentation shared by the detailed and guided notebooks."""
from html import escape
from pathlib import Path
from urllib.parse import quote
import re
from html import unescape

import ipywidgets as w
from .output import Output
from IPython import get_ipython
from IPython.display import display

from .atlas_ui import ordered_sources
from .execution import ExecutionCheckpoint
from .masks import MASK_LABELS
from .notebook_navigation import NotebookNavigation
from . import colors
from .widget_lifecycle import close_widget


def file_link(path, label):
    from .widgets import _detect_server
    base, root = _detect_server()
    try:
        url = base + "files/" + quote(Path(path).absolute().relative_to(root).as_posix())
        return f'<a href="{escape(url, quote=True)}" target="_blank">{escape(label)}</a>'
    except ValueError:
        return escape(str(path))


def report_sections(body):
    """Group the existing report markup without changing its evidence tables."""
    sections = []
    for title, content in re.findall(r"<h4[^>]*>(.*?)</h4>(.*?)(?=<h4|<hr|$)", body, re.S):
        label = " ".join(unescape(re.sub(r"<[^>]+>", "", title)).split())
        sections.append((label, content))
    if "<hr" in body:
        legend = body[body.index("<hr"):].rsplit("</div>", 1)[0]
        sections.append(("Legend and evidence notes", legend))
    return sections


class ReportInputs:
    def __init__(self, namespace, shell=None):
        self.ns = namespace
        self.entries = [dict(e) for e in namespace["SUBJECTS"]]
        self.busy = False
        self.preview = None
        self.gate = ExecutionCheckpoint(shell, "Choose report inputs, then click Generate participant report.") if shell else None
        if shell:
            shell._calmar_report_checkpoint = self.gate
        index = namespace.get("INTERP_SUBJECT_IDX") or 0
        self.subject = w.Dropdown(
            options=[(f"{e['subject']} {e.get('session') or ''}".strip(), i) for i, e in enumerate(self.entries)],
            value=index if 0 <= index < len(self.entries) else 0, description="Participant:",
            style={"description_width": "initial"}, layout=w.Layout(width="360px"))
        self.source = w.Dropdown(description="Lesion mask:", options=[],
            style={"description_width": "initial"}, layout=w.Layout(width="300px"))
        atlases = list(namespace.get("INTERP_KB_ATLASES", ["HarvardOxford"]))
        preferred = namespace.get("INTERP_DISPLAY_ATLAS", "HarvardOxford")
        self.atlas = w.Dropdown(options=atlases, value=preferred if preferred in atlases else atlases[0],
            description="Display atlas:", style={"description_width": "initial"}, layout=w.Layout(width="330px"))
        self.decode = w.Checkbox(value=namespace.get("INTERP_RUN_DECODING", False),
            description="Include Neurosynth decoding (optional; takes longer)", indent=False,
            layout=w.Layout(width="auto"))
        self.summary, self.message = w.HTML(), w.HTML()
        self.generate = w.Button(description="Generate participant report", button_style="success",
            icon="play", layout=w.Layout(width="270px", min_height="36px"))
        self.navigation = NotebookNavigation(
            self.message, on_cell_order=self.gate._update_cell_order if self.gate else None)
        self.compare_body = w.VBox()
        self.compare = w.Accordion(children=[self.compare_body], selected_index=None)
        self.compare.set_title(0, "Compare available MNI masks (optional)")
        self.subject.observe(self.refresh, names="value")
        self.source.observe(self.apply, names="value")
        self.atlas.observe(self.apply, names="value")
        self.decode.observe(self.apply, names="value")
        self.compare.observe(self.show_comparison, names="selected_index")
        self.generate.on_click(lambda _: self.navigation.request("report-start", self.approve))
        self.widget = w.VBox([w.HTML("<h3>Choose the participant report</h3>"
            "<p>Choose a participant, lesion mask and display atlas below. "
            "Generate creates the report and its downloadable HTML file.</p>"),
            self.subject, self.source, self.atlas, self.decode, self.summary,
            self.compare, self.generate, self.message, self.navigation])
        self.refresh()

    def refresh(self, *_):
        self.busy = True
        sources = ordered_sources(self.ns["available_mni_sources"](self.entries[self.subject.value]))
        previous = self.source.value or self.ns.get("INTERP_MASK_SOURCE")
        self.source.options = [(MASK_LABELS[s], s) for s in sources]
        self.source.value = previous if previous in sources else next(iter(sources), None)
        self.source.disabled = not sources
        self.busy = False
        self.apply()

    def apply(self, *_):
        if self.busy:
            return
        self.ns.update(INTERP_SUBJECT_IDX=self.subject.value, INTERP_MASK_SOURCE=self.source.value,
                       INTERP_DISPLAY_ATLAS=self.atlas.value, INTERP_RUN_DECODING=self.decode.value)
        self.generate.disabled = self.source.value is None
        if self.source.value is None:
            self.summary.value = "<b>No available MNI lesion mask for this participant.</b> Complete its warp before generating a report."
        else:
            self.summary.value = (f"<b>Report selection:</b> {escape(self.subject.label)} · "
                f"{escape(self.source.label)} mask · {escape(self.atlas.value)} atlas. "
                "Click Generate participant report when ready.")
        if self.compare.selected_index is not None:
            self.show_comparison()

    def show_comparison(self, *_):
        if self.compare.selected_index is None:
            return
        helpers = self.ns["cw"]
        if self.preview is None:
            self.preview = helpers.fresh_viewer("report_mask_comparison", height=330)
        entry = self.entries[self.subject.value]
        inventory = self.ns["mask_inventory_for"](entry)
        brain = self.ns["deriv_path_for"](entry) / "Subject_in_MNI.nii.gz"
        if not brain.exists():
            self.preview.load_volumes([])
            self.compare_body.children = (w.HTML("The MNI brain image is unavailable; complete the warp first."),)
            return
        checks, specs = [], [{"path": str(brain), "colormap": "gray", "opacity": 1.}]
        for source in ordered_sources(inventory):
            path = inventory[source].get("MNI")
            if path is None or not Path(path).exists():
                continue
            shown = source == self.source.value
            specs.append({"path": str(path), "name": MASK_LABELS[source],
                "colormap": colors.color(source),
                "opacity": .55 if shown else 0., "cal_min": .5, "cal_max": 1.})
            check = w.Checkbox(value=shown, description=MASK_LABELS[source], indent=False)
            index = len(specs)-1
            check.observe(lambda c, i=index: setattr(self.preview.volumes[i], "opacity", .55 if c["new"] else 0.),
                          names="value")
            checks.append(check)
        helpers.set_volumes(self.preview, specs)
        self.compare_body.children = (w.HTML(colors.legend(ordered_sources(inventory))),
                                      w.HBox(checks), self.preview)

    def approve(self):
        if self.source.value not in self.ns["available_mni_sources"](self.entries[self.subject.value]):
            self.refresh()
            self.message.value = "The chosen mask is no longer available. Choose an available mask."
            return False
        self.apply()
        if self.gate:
            self.gate.release()
        self.message.value = "Generating the selected participant report…"
        return True

    def close(self):
        if self.gate:
            self.gate.close()
        close_widget(self.navigation)
        close_widget(self.widget)


def show_report_inputs(namespace):
    if not namespace["SUBJECTS"]:
        raise RuntimeError("No participants discovered.")
    previous = namespace.get("_report_inputs")
    if previous:
        previous.close()
    shell = get_ipython()
    old_gate = getattr(shell, "_calmar_report_checkpoint", None)
    if old_gate:
        old_gate.close()
    panel = ReportInputs(namespace, shell)
    namespace["_report_inputs"] = panel
    display(panel.widget)
    if panel.gate:
        panel.gate._cancel_queued()
    return panel


class ParticipantReport:
    def __init__(self, title, qc_notice, sections, path, full_html, brain, lesion, helpers, decode=False, source="linda"):
        self.path, self.full_html = Path(path), full_html
        self.brain, self.lesion, self.helpers = Path(brain), Path(lesion), helpers
        self.source = source
        self.brain_box = w.VBox([w.HTML("Open this tab to load the selected lesion on the MNI brain.")])
        self.decode_html = w.HTML("Neurosynth decoding is pending." if decode else "Neurosynth decoding was not requested.")
        self.decode_log = Output()
        decode_details = w.Accordion(children=[self.decode_log], selected_index=None)
        decode_details.set_title(0, "Decoding log")
        # Evidence tables use explicit light colours in the saved report.
        # Retain that background when presenting each section in a dark notebook.
        accordion = w.Accordion(children=[w.HTML(
            '<div style="background:#fafafa;color:#1a1a1a;padding:12px;overflow-x:auto">'
            + html + '</div>') for _, html in sections], selected_index=0)
        for i, (label, _) in enumerate(sections):
            accordion.set_title(i, label)
        children = [accordion, self.brain_box]
        if decode:
            children.append(w.VBox([self.decode_html, decode_details]))
        self.tabs = w.Tab(children=children)
        self.tabs.set_title(0, "Report")
        self.tabs.set_title(1, "Brain viewer")
        if decode:
            self.tabs.set_title(2, "Neurosynth")
        self.tabs.observe(self.show_brain, names="selected_index")
        self.navigation_message = w.HTML()
        self.navigation = NotebookNavigation(self.navigation_message)
        choose = w.Button(description="Choose another report", layout=w.Layout(width="220px"))
        choose.on_click(lambda _: self.navigation.request("report-selection", lambda: True, all_below=False))
        self.widget = w.VBox([w.HTML(title + qc_notice),
            w.HTML(file_link(path, "Open / download report HTML") + " · Use the saved report’s Print button for PDF."),
            self.tabs, choose, self.navigation_message, self.navigation])

    def show_brain(self, change):
        if change["new"] != 1 or getattr(self, "viewer", None) is not None:
            return
        if not self.brain.exists() or not self.lesion.exists():
            self.brain_box.children = (w.HTML("The selected MNI brain or lesion image is unavailable."),)
            return
        self.viewer = self.helpers.fresh_viewer("interp_viewer", height=400)
        self.helpers.set_volumes(self.viewer, [
            {"path": str(self.brain), "colormap": "gray", "opacity": 1.},
            {"path": str(self.lesion), "colormap": colors.color(self.source), "opacity": .7, "cal_min": .5, "cal_max": 1.}])
        self.brain_box.children = (w.HTML(colors.legend([self.source])), self.viewer)

    def add_decoding(self, html):
        self.decode_html.value = html
        # Replace a prior addition so repeated decoding does not duplicate it.
        start, end = "<!-- calmar-decoding-start -->", "<!-- calmar-decoding-end -->"
        base = self.full_html
        if start in base:
            a, rest = base.split(start, 1)
            base = a + rest.split(end, 1)[1]
        addition = start + "<section><h2>Optional Neurosynth decoding</h2>" + html + "</section>" + end
        self.full_html = base.replace("</body>", addition + "</body>")
        self.path.write_text(self.full_html, encoding="utf-8")
