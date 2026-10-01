"""A JupyterLab bridge that resolves a cell in the button's own notebook."""

from pathlib import Path
import asyncio
from html import escape
import anywidget


class NotebookNavigation(anywidget.AnyWidget):
    _esm = Path(__file__).with_name("notebook_navigation.js")

    def __init__(self, message, *, on_cell_order=None):
        super().__init__()
        self.message = message
        self.on_cell_order = on_cell_order
        self.ready = False
        self.pending = None
        self.pending_request = None
        self.on_msg(self._receive)

    def request(self, role, before_run, *, all_below=True, prompt=""):
        self.pending = before_run
        self.pending_request = dict(action="prepare", role=role, all_below=all_below, prompt=prompt)
        if self.ready:
            self._send_pending_request()
        else:
            self.message.value = "Connecting notebook controls…"
            self.send(dict(action="connect"))
        return True

    def _send_pending_request(self):
        if self.pending_request is not None:
            request, self.pending_request = self.pending_request, None
            self.send(request)

    def _receive(self, _, data, buffers):
        event = data.get("event")
        if event == "ready":
            self.ready = True
            self.send(dict(action="connected"))
            self._send_pending_request()
        elif event == "cell-order" and self.on_cell_order is not None:
            self.on_cell_order(data["ids"], data.get("batch_start"))
        elif event == "approved" and self.pending is not None:
            callback, self.pending = self.pending, None
            if callback() is not False:
                # Releasing a checkpoint cancels old queued execute requests.
                # Wait until that cancellation is finished before submitting
                # the new, explicitly requested continuation.
                from IPython import get_ipython
                kernel = getattr(get_ipython(), "kernel", None)
                async def continue_when_ready():
                    for _ in range(200):
                        if not getattr(kernel, "_aborting", False):
                            self.send(dict(action="execute"))
                            return
                        await asyncio.sleep(.01)
                    self.message.value = "Queue cancellation is still in progress. Click the continuation button again."
                asyncio.get_running_loop().create_task(continue_when_ready())
        elif event in ("error", "cancelled"):
            self.pending = None
            self.pending_request = None
            if data.get("connection"):
                self.ready = False
            self.message.value = escape(data.get("message", "Continuation cancelled."))
