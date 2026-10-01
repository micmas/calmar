"""One configurable colour per mask/map origin, shared by viewers and plots."""

from html import escape

DEFAULT_MASK_COLORS = {
    "linda": "red", "manual": "blue", "synthstroke": "green",
    "hdbet": "yellow", "bcbtoolkit": "magenta", "deepdisco": "cyan",
}
LABELS = {"linda": "LINDA", "manual": "Manual", "synthstroke": "SynthStroke",
          "hdbet": "HD-BET", "bcbtoolkit": "BCBToolkit", "deepdisco": "DeepDisco"}
# Match NiiVue's primary-colour maps exactly (CSS 'green' is darker).
CSS = {"red": "#ff0000", "green": "#00ff00", "blue": "#0000ff",
       "yellow": "#ffff00", "cyan": "#00ffff", "magenta": "#ff00ff"}
_colors = globals().get("_colors", dict(DEFAULT_MASK_COLORS))


def configure(mapping=None):
    """Validate CONFIG overrides before replacing the current palette."""
    candidate = {**DEFAULT_MASK_COLORS, **(mapping or {})}
    unknown = set(candidate) - set(DEFAULT_MASK_COLORS)
    if unknown:
        raise ValueError(f"Unknown MASK_COLORS origins: {sorted(unknown)}")
    for source, value in candidate.items():
        if value not in CSS:
            raise ValueError(f"MASK_COLORS[{source!r}] must be one of {', '.join(CSS)}")
    global _colors
    _colors = candidate


def color(source):
    return _colors[source]


def css(source):
    return CSS[color(source)]


def cmap(source, *, continuous=False):
    """Use the same hue in exported figures and probability/frequency plots."""
    from matplotlib.colors import LinearSegmentedColormap, ListedColormap
    if continuous:
        return LinearSegmentedColormap.from_list(source, ["black", css(source)])
    # Nilearn builds a segmented colourbar from these samples. A one-entry
    # map has no x=1 endpoint and fails later when Matplotlib draws the report.
    return ListedColormap([css(source), css(source)])


def legend(sources):
    return " · ".join(f'<span style="color:{css(s)}">■</span> '
                      f'{escape(LABELS[s])} ({color(s)})' for s in sources)
