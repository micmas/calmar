"""Overlay controls of a NiiVue viewer that act in the browser, not the kernel.

Ticking an overlay, choosing a lesion source, changing the plane or centring on
the lesion are applied directly to the viewer's widget models in the browser
(anywidget + the widget manager). They respond while the kernel is busy, e.g.
while a later cell waits for a Slurm job; with ordinary ipywidgets callbacks
they would wait until that cell finished.

The state the controls show is synced back to Python (``roles``, ``group``,
``plane``), so the kernel can rebuild the layers for another participant and
keep the same choices.

``layers``: one dict per overlay volume, in viewer order after the background:
``model_id`` (the Volume widget), ``role`` (which checkbox), ``group`` (lesion
source, or "" when there is no source choice), ``opacity`` when shown, ``color``
(CSS) and ``centre`` (crosshair position as NiiVue fractions, lesions only).
``roles``: the checkboxes, ``{"key", "label", "shown"}``.
``groups``: ``[[label, key], ...]`` for the source buttons (empty = none).
``variants``: ``[[label, key], ...]`` for a second row of buttons (e.g. the
DeepDisco model); a layer's ``variant`` is "" when it does not depend on it.
"""
import anywidget
import nibabel as nib
import numpy as np
import traitlets as t

# One look for every choice row (lesion source, model, QC stage).
BUTTON_CSS = ("padding:2px 10px;border:1px solid var(--jp-border-color1);border-radius:3px;cursor:pointer;")
ON_CSS = "background:var(--jp-brand-color1);color:white"
OFF_CSS = "background:var(--jp-layout-color2);color:inherit"

ESM = r"""
function el(tag, style, text) {
  const node = document.createElement(tag);
  if (style) node.style.cssText = style;
  if (text !== undefined) node.textContent = text;
  return node;
}

export default {
  render({ model, el: root }) {
    const manager = model.widget_manager;
    const box = el("div", "display:flex;flex-direction:column;gap:6px;font-size:13px;margin:4px 0");
    root.appendChild(box);
    let applied = null;                     // opacity last sent per volume model

    const visible = (layer) => {
      const shown = Object.fromEntries(model.get("roles").map((r) => [r.key, r.shown]));
      return chosen(layer) && !!shown[layer.role];
    };
    const chosen = (layer) => (!layer.group || layer.group === model.get("group"))
      && (!layer.variant || layer.variant === model.get("variant"));

    async function apply() {
      // Only volumes whose visibility changed: each change redraws NiiVue's overlays.
      const layers = model.get("layers");
      if (!applied || applied.length !== layers.length) applied = layers.map(() => null);
      for (const [i, layer] of layers.entries()) {
        const opacity = visible(layer) ? layer.opacity : 0;
        if (applied[i] === opacity) continue;
        const volume = await manager.get_model(layer.model_id);
        if (volume.get("opacity") !== opacity) {
          volume.set("opacity", opacity);
          volume.save_changes();
        }
        applied[i] = opacity;
      }
    }

    async function centre() {
      const target = model.get("layers").find((l) => l.centre && visible(l));
      if (!target) {
        note.textContent = "Show a lesion first.";
        return;
      }
      note.textContent = "";
      const viewer = await manager.get_model(model.get("viewer_id"));
      viewer.set("scene", { ...(viewer.get("scene") || {}), crosshairPos: target.centre });
      viewer.save_changes();
      viewer.trigger("msg:custom", { type: "draw_scene", data: [] }, []);
    }

    async function setPlane(value) {
      model.set("plane", value);
      model.save_changes();
      const viewer = await manager.get_model(model.get("viewer_id"));
      viewer.set("opts", { ...(viewer.get("opts") || {}), sliceType: value });
      viewer.save_changes();
      // ipyniivue copies new options without redrawing.
      viewer.trigger("msg:custom", { type: "draw_scene", data: [] }, []);
    }

    const note = el("span", "color:var(--jp-ui-font-color2);margin-left:8px");

    function choice(title, options, trait) {
      // One row of buttons; the chosen one is highlighted.
      if (options.length < 2) return;
      const row = el("div", "display:flex;align-items:center;gap:4px;flex-wrap:wrap");
      row.appendChild(el("span", "margin-right:4px;min-width:48px", title));
      for (const [label, key] of options) {
        const button = el("button", "BUTTON_CSS" + (key === model.get(trait) ? "ON_CSS" : "OFF_CSS"), label);
        button.onclick = () => { model.set(trait, key); model.save_changes(); };
        row.appendChild(button);
      }
      box.appendChild(row);
    }

    function draw() {
      box.replaceChildren();
      choice("Lesion:", model.get("groups"), "group");
      choice("Model:", model.get("variants"), "variant");
      const row = el("div", "display:flex;align-items:center;gap:14px;flex-wrap:wrap");
      for (const role of model.get("roles")) {
        const layer = model.get("layers").find((l) => l.role === role.key && chosen(l));
        if (!layer) continue;
        const label = el("label", "display:flex;align-items:center;gap:4px;cursor:pointer");
        const swatch = el("span", `color:${layer.color};font-size:16px`, "■");
        const tick = el("input");
        tick.type = "checkbox";
        tick.checked = role.shown;
        tick.onchange = () => {
          model.set("roles", model.get("roles").map((r) => (r.key === role.key ? { ...r, shown: tick.checked } : r)));
          model.save_changes();
        };
        label.append(swatch, tick, document.createTextNode(role.label));
        row.appendChild(label);
      }
      const plane = el("select", "margin-left:8px");
      for (const [text, value] of [["Axial", 0], ["Coronal", 1], ["Sagittal", 2], ["Three planes", 3]]) {
        const option = el("option", "", text);
        option.value = value;
        option.selected = value === model.get("plane");
        plane.appendChild(option);
      }
      plane.onchange = () => setPlane(Number(plane.value));
      row.appendChild(plane);
      if (model.get("layers").some((l) => l.centre)) {
        const button = el("button", "BUTTON_CSS" + "OFF_CSS", "Centre on lesion");
        button.onclick = centre;
        row.appendChild(button);
      }
      row.appendChild(note);
      box.appendChild(row);
    }

    model.on("change:layers", () => { applied = null; draw(); });
    model.on("change:roles change:group change:variant", () => { draw(); apply(); });
    model.on("change:groups change:variants", draw);
    draw();
  },
};
"""


def _styled(esm):
    return (esm.replace('"BUTTON_CSS"', repr(BUTTON_CSS)).replace('"ON_CSS"', repr(ON_CSS))
            .replace('"OFF_CSS"', repr(OFF_CSS)))


CHOICE_ESM = r"""
export default {
  render({ model, el: root }) {
    const row = document.createElement("div");
    row.style.cssText = "display:flex;align-items:center;gap:4px;flex-wrap:wrap;font-size:13px;margin:4px 0";
    root.appendChild(row);
    function draw() {
      row.replaceChildren();
      if (model.get("title")) {
        const title = document.createElement("span");
        title.style.cssText = "margin-right:4px;min-width:48px";
        title.textContent = model.get("title");
        row.appendChild(title);
      }
      for (const [label, key] of model.get("options")) {
        const button = document.createElement("button");
        button.style.cssText = "BUTTON_CSS" + (key === model.get("value") ? "ON_CSS" : "OFF_CSS");
        button.textContent = label;
        button.disabled = model.get("disabled");
        button.onclick = () => { model.set("value", key); model.save_changes(); };
        row.appendChild(button);
      }
    }
    model.on("change:options change:value change:disabled change:title", draw);
    draw();
  },
};
"""


class ChoiceButtons(anywidget.AnyWidget):
    """A row of buttons, one chosen (``value``), in the same style as the viewer
    controls. ``options``: ``[(label, value), ...]``. Unlike the viewer controls
    the choice is handled by the kernel."""
    _esm = _styled(CHOICE_ESM)
    options = t.List().tag(sync=True)
    value = t.Any(None, allow_none=True).tag(sync=True)
    title = t.Unicode("").tag(sync=True)
    disabled = t.Bool(False).tag(sync=True)

    @property
    def label(self):
        return next((label for label, value in self.options if value == self.value), None)


class LayerControls(anywidget.AnyWidget):
    _esm = _styled(ESM)
    viewer_id = t.Unicode("").tag(sync=True)
    layers = t.List().tag(sync=True)
    roles = t.List().tag(sync=True)
    groups = t.List().tag(sync=True)
    group = t.Unicode("").tag(sync=True)
    variants = t.List().tag(sync=True)
    variant = t.Unicode("").tag(sync=True)
    plane = t.Int(3).tag(sync=True)

    def visible(self, layer):
        """Same rule as the browser: the layer's checkbox is ticked and its source
        (and model) chosen."""
        shown = {r["key"]: r["shown"] for r in self.roles}
        return ((not layer["group"] or layer["group"] == self.group)
                and (not layer.get("variant") or layer["variant"] == self.variant)
                and bool(shown.get(layer["role"])))


def mm_to_frac(image_path, mm):
    """NiiVue fraction coordinates of a world position (mm) in an image.

    NiiVue reorients each image to the nearest RAS voxel order and places the
    crosshair at ``(voxel + 0.5) / dims`` of that grid (``convert_mm2frac``).
    Computed from the header only; the image data is not read.
    """
    image = nib.load(str(image_path))
    shape = np.array(image.shape[:3])
    ornt = nib.orientations.io_orientation(image.affine)
    ras = image.affine @ nib.orientations.inv_ornt_aff(ornt, shape)
    ras_shape = shape[ornt[:, 0].astype(int).argsort()]
    voxel = np.linalg.inv(ras) @ np.array([*mm[:3], 1.0])
    return ((voxel[:3] + 0.5) / ras_shape).tolist()
