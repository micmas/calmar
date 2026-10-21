"""A JupyterLab bridge that resolves a cell in the button's own notebook."""

from pathlib import Path
import asyncio
from html import escape
import anywidget


class NotebookNavigation(anywidget.AnyWidget):
    _esm = Path(__file__).with_name("notebook_navigation.js")

    def __init__(self, message, *, on_cell_order=None, on_error=None):
        super().__init__()
        self.message = message
        self.on_cell_order = on_cell_order
        self.on_error = on_error
        self.ready = False
        self.pending = None
        self.pending_request = None
        self._watchdog = None
        self.on_msg(self._receive)

    def request(self, role, before_run, *, all_below=True, prompt=""):
        self._cancel_watchdog()
        self.pending = before_run
        self.pending_request = dict(action="prepare", role=role, all_below=all_below, prompt=prompt)
        # A restored/virtualized view can disappear after its earlier ready event.
        # Reconnect for every click rather than trusting stale Python readiness.
        self.ready = False
        self.message.value = "Connecting notebook controls…"
        self.send(dict(action="connect"))
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            return True
        # A message can be lost while the browser reconnects; ask again.
        resend = [loop.call_later(t, self._resend_connect) for t in (3, 6, 9)]
        self._watchdog = loop.call_later(12, self._connection_timeout)
        self._resends = resend
        return True

    def _resend_connect(self):
        if self.pending_request is not None and not self.ready:
            self.send(dict(action="connect"))

    def _cancel_watchdog(self):
        if getattr(self, '_watchdog', None) is not None:
            self._watchdog.cancel()
            self._watchdog = None
        for handle in getattr(self, '_resends', ()):
            handle.cancel()
        self._resends = ()

    def _connection_timeout(self):
        self.pending = self.pending_request = None
        self.ready = False
        self.message.value = ("Notebook controls did not respond: this browser page has lost its connection "
                              "to the notebook kernel. Reload the page (F5), rerun this cell, then click again.")
        if self.on_error:
            self.on_error()

    def _send_pending_request(self):
        if self.pending_request is not None:
            self._cancel_watchdog()
            request, self.pending_request = self.pending_request, None
            self.send(request)

    def _receive(self, _, data, buffers):
        event = data.get("event")
        if event == "ready":
            self.ready = True
            self.send(dict(action="connected"))
            self._send_pending_request()
        elif event == "cell-sources":
            from IPython import get_ipython
            shell = get_ipython()
            if shell is not None:
                shell._calmar_live_cell_sources = data.get('sources', {})
        elif event == "cell-order" and self.on_cell_order is not None:
            self.on_cell_order(data["ids"], data.get("batch_start"))
        elif event == "approved" and self.pending is not None:
            self._cancel_watchdog()
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
                            command = dict(action="execute")
                            if data.get('view_id'):
                                command['view_id'] = data['view_id']
                            self.send(command)
                            return
                        await asyncio.sleep(.01)
                    self.message.value = "Queue cancellation is still in progress. Click the continuation button again."
                    if self.on_error:
                        self.on_error()
                asyncio.get_running_loop().create_task(continue_when_ready())
        elif event in ("error", "cancelled"):
            self._cancel_watchdog()
            self.pending = None
            self.pending_request = None
            if data.get("connection"):
                self.ready = False
            self.message.value = escape(data.get("message", "Continuation cancelled."))
            if self.on_error:
                self.on_error()

    def close(self):
        self._cancel_watchdog()
        super().close()
