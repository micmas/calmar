"""Checkpoint controls must survive concurrent notebook autosaves."""
import json
from types import SimpleNamespace
from unittest.mock import patch

from calmar import execution as ex

_read_text = ex.Path.read_text


def notebook_read(values):
    values = iter(values)
    def read(path, *args, **kwargs):
        if path.suffix == ".ipynb":
            return next(values, "")
        return _read_text(path, *args, **kwargs)
    return read


CELLS = [
    {"id": "viewer", "cell_type": "code", "source": "show_viewer()"},
    {"id": "pause", "cell_type": "code", "source": "pause_before_batch()"},
    {"id": "batch", "cell_type": "code", "source": "run_batch()",
     "metadata": {"calmar": {"role": "batch-start"}}},
]


def shell():
    return SimpleNamespace(input_transformers_post=[], kernel=SimpleNamespace(
        get_parent=lambda: {"metadata": {"cellId": "pause"}}))


def test_checkpoint_retries_partial_autosave_and_keeps_upstream_rerunnable():
    valid = json.dumps({"cells": CELLS})
    with patch.object(ex, "_NOTEBOOK_CELLS", {}), \
         patch.object(ex.Path, "read_text", notebook_read(["", valid, ""])), \
         patch.object(ex.time, "sleep"):
        gate = ex.BatchCheckpoint(shell())
        try:
            assert gate.upstream_cell_ids == {"viewer", "pause"}
            assert gate.button.description == "Continue to batch"
            assert gate.paused
        finally:
            gate.close()


def test_unreadable_notebook_still_creates_controls_and_accepts_live_order():
    with patch.object(ex, "_NOTEBOOK_CELLS", {}), \
         patch.object(ex.Path, "read_text", notebook_read(["{"])), \
         patch.object(ex.time, "sleep"):
        gate = ex.BatchCheckpoint(shell())
        try:
            assert gate.upstream_cell_ids == set()
            assert gate.paused
            gate._update_cell_order(["viewer", "pause", "batch"], "batch")
            assert gate.upstream_cell_ids == {"viewer", "pause"}
        finally:
            gate.close()


def test_legacy_identity_uses_last_complete_snapshot_during_autosave():
    request_shell = SimpleNamespace(kernel=SimpleNamespace(get_parent=lambda: {
        "content": {"code": "show_viewer()"}}))
    with patch.object(ex, "_NOTEBOOK_CELLS", {"lesion-interpretation-pipeline.ipynb": CELLS}), \
         patch.object(ex.Path, "read_text", return_value=""):
        assert ex._request_cell_id(request_shell) == "viewer"
