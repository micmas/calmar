"""Keep widget containers serializable when their children are replaced."""

import ipywidgets as widgets
from ipywidgets.widgets.widget import _instances


def detach_closed_children(closing=None):
    """Remove stale child references from retained notebook containers.

    Clearing an output does not close its Python Box model. A closed child has
    no comm/model_id, so serializing any retained Box that references it breaks
    the widget manager's restoration of the entire notebook. The ipywidgets
    registry is needed because containers outlive their cell's local variables.
    """
    changed = 0
    for parent in tuple(_instances.values()):
        if not isinstance(parent, widgets.Box) or parent.comm is None:
            continue
        children = tuple(child for child in parent.children
                         if child is not closing and child.comm is not None)
        if len(children) != len(parent.children):
            parent.children = children
            changed += 1
    return changed


def close_widget(widget):
    detach_closed_children(closing=widget)
    widget.close()
