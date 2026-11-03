"""A JupyterLab bridge that resolves a cell in the button's own notebook."""

from pathlib import Path
import asyncio
from html import escape
import time
import anywidget


class NotebookNavigation(anywidget.AnyWidget):
    _esm = Path(__file__).with_name("notebook_navigation.js")

    def __init__(self, message, *, on_cell_order=None, on_error=None, focus_checkpoint=None):
        super().__init__()
        self.message = message
        self.on_cell_order = on_cell_order
        self.on_error = on_error
        self._focus_checkpoint = focus_checkpoint
        self._focus_deadline = None
        self._focus_events = None
        self._focus_event_handler = None
        self._arm_focus_window()
        self.ready = False
        self.pending = None
        self.pending_request = None
        self._watchdog = None
        self.on_msg(self._receive)

    def request(self, role, before_run, *, all_below=True, prompt=""):
        self._clear_focus()
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

    def _arm_focus_window(self):
        checkpoint = self._focus_checkpoint
        if checkpoint is None:
            return
        events = getattr(getattr(checkpoint, "shell", None), "events", None)
        if events is None:
            # Unit tests and non-IPython callers have no cell lifecycle. Their
            # construction time is the best available approximation.
            self._focus_deadline = time.monotonic() + 10
            return

        def start_after_cell(*_):
            self._focus_deadline = time.monotonic() + 10
            self._remove_focus_hook()
            if self.ready:
                self._send_pending_focus()

        self._focus_events = events
        self._focus_event_handler = start_after_cell
        events.register("post_run_cell", start_after_cell)

    def _remove_focus_hook(self):
        if self._focus_events is not None and self._focus_event_handler is not None:
            try:
                self._focus_events.unregister("post_run_cell", self._focus_event_handler)
            except ValueError:
                pass
        self._focus_events = None
        self._focus_event_handler = None

    def _clear_focus(self):
        self._remove_focus_hook()
        self._focus_checkpoint = None
        self._focus_deadline = None

    def _send_pending_focus(self):
        checkpoint = self._focus_checkpoint
        deadline = self._focus_deadline
        # Focus is best-effort presentation only. Give up if the widget took
        # too long to connect, the gate was already released, or this request
        # has no stable notebook cell id.
        if checkpoint is None:
            return
        # In a real kernel the one-shot post_run_cell hook starts the window.
        # If an unusual frontend processes ready earlier, that hook sends the
        # still-pending focus as soon as the cell finishes.
        if deadline is None:
            return
        if (time.monotonic() > deadline
                or not getattr(checkpoint, "paused", False)
                or not getattr(checkpoint, "boundary_cell_id", None)):
            self._clear_focus()
            return
        cell_id = checkpoint.boundary_cell_id
        self._clear_focus()  # one shot: a late retry must never steal focus
        self.send(dict(action="focus", cell_id=cell_id))

    def _receive(self, _, data, buffers):
        event = data.get("event")
        if event == "ready":
            self.ready = True
            self.send(dict(action="connected"))
            self._send_pending_focus()
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
        self._clear_focus()
        self._cancel_watchdog()
        super().close()
