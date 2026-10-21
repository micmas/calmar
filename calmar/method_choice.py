"""Tick boxes choosing the automatic lesion segmentations (CONFIG["SEGMENTATION_METHODS"]).

Shown where the notebook pauses before processing (single-subject participant
picker, batch checkpoint) and in the guided form. A change is written straight
into the CONFIG dict, which ``study`` and every later step read, so it applies
to the next step submitted. Rerunning the configuration cell resets it to the
value written there.
"""
from html import escape

import ipywidgets as w


METHOD_CHOICES = {"linda": "LINDA lesion segmentation (slow: 1.5-3.7 h per participant; "
                           "without it, ANTs registers each brain to the template)",
                  "synthstroke": "SynthStroke lesion segmentation"}


class MethodChoice:
    """One tick box per method; ``widget`` to display, ``valid`` when at least one
    is ticked. ``on_change(valid)`` is called after each change."""

    def __init__(self, config, on_change=None):
        self.config, self.on_change = config, on_change
        from .study import modality
        self.acute = modality(config) == "dwi"
        if self.acute:
            # The acute route has one segmentation; nothing to choose.
            self.boxes, self.note = {}, w.HTML()
            self.widget = w.HTML("<b>Lesion segmentation:</b> acute (DWI) route: OpenADS on the diffusion-weighted "
                                 "image and ADC map (CONFIG[\"MODALITY\"] = \"dwi\").")
            return
        chosen = config.get("SEGMENTATION_METHODS") or list(METHOD_CHOICES)
        self.boxes = {m: w.Checkbox(value=m in chosen, description=label, indent=False,
                                    layout=w.Layout(width="auto"))
                      for m, label in METHOD_CHOICES.items()}
        self.note = w.HTML()
        for box in self.boxes.values():
            box.observe(self.apply, names="value")
        self.widget = w.VBox([w.HTML("<b>Lesion segmentation</b> (applies to the single-subject test "
                                     "and to batch processing):"), *self.boxes.values(), self.note])
        self.apply()

    @property
    def methods(self):
        if self.acute:
            return ["openads"]
        return [m for m, box in self.boxes.items() if box.value]

    @property
    def valid(self):
        return bool(self.methods)

    def apply(self, *_):
        if self.valid:
            self.config["SEGMENTATION_METHODS"] = self.methods
            self.note.value = ("" if "linda" in self.methods else
                               "<span style='font-size:12px'>Without LINDA, the registration step "
                               "(ANTs, about 10 min per participant) registers each brain to the "
                               "MNI152 template; LINDA's cells are skipped.</span>")
        else:
            self.note.value = "<b>Choose at least one lesion segmentation.</b>"
        if self.on_change:
            self.on_change(self.valid)

    def summary(self):
        if self.acute:
            return "OpenADS"
        return ", ".join(escape(METHOD_CHOICES[m].split(" lesion")[0]) for m in self.methods)

    def disable(self):
        for box in self.boxes.values():
            box.disabled = True
