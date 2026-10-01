"""Exercise the notebook checkpoint against a real, isolated Jupyter kernel."""

import ast
import json
from pathlib import Path
import tempfile
import time
import unittest

from jupyter_client import KernelManager


ROOT = Path(__file__).resolve().parents[1]
CELLS = {int(c["id"].rsplit("-", 1)[1]) - 1: c for c in json.loads((ROOT / "lesion-interpretation-pipeline.ipynb").read_text())["cells"] if c["id"].startswith("calmar-step-")}


class ExecutionCheckpointTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manager = KernelManager(kernel_name="python3")
        cls.manager.start_kernel()
        cls.client = cls.manager.client()
        cls.client.start_channels()
        cls.client.wait_for_ready(timeout=30)

    @classmethod
    def tearDownClass(cls):
        cls.client.stop_channels()
        cls.manager.shutdown_kernel(now=True)

    def reply(self, message_id):
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            message = self.client.get_shell_msg(timeout=max(.1, deadline - time.monotonic()))
            # wait_for_ready can leave additional kernel-info replies queued.
            if message["msg_type"] != "execute_reply":
                continue
            self.assertEqual(message["parent_header"]["msg_id"], message_id)
            return message["content"]
        self.fail("Timed out waiting for execute_reply")

    def output_until_idle(self, message_id):
        messages = []
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            message = self.client.get_iopub_msg(timeout=max(.1, deadline - time.monotonic()))
            if message.get("parent_header", {}).get("msg_id") != message_id:
                continue
            messages.append(message)
            if (message["msg_type"] == "status"
                    and message["content"]["execution_state"] == "idle"):
                return messages
        self.fail("Timed out waiting for kernel idle")

    def execute_cell(self, code, cell_id):
        message = self.client.session.msg("execute_request", content={
            "code": code, "silent": False, "store_history": True,
            "user_expressions": {}, "allow_stdin": False, "stop_on_error": False,
        }, metadata={"cellId": cell_id} if cell_id else {})
        self.client.shell_channel.send(message)
        message_id = message["header"]["msg_id"]
        reply = self.reply(message_id)
        self.output_until_idle(message_id)
        return reply

    def test_panel_clear_keeps_its_containing_cell_and_captures_stream_order(self):
        code = (
            f"import sys\nsys.path.insert(0, {str(ROOT)!r})\n"
            "from calmar.output import Output\n"
            "from IPython.display import display, HTML, clear_output\n"
            "import ipywidgets as w\n"
            "panel = Output()\ndisplay(w.VBox([w.HTML('Controls remain visible'), panel]))\n"
            "with panel:\n"
            "    display(HTML('old output'))\n"
            "    clear_output(wait=True)\n"
            "    print('before')\n"
            "    display(HTML('new metrics'))\n"
            "    print('after')\n"
            "assert [o['output_type'] for o in panel.outputs] == ['stream', 'display_data', 'stream']\n"
            "assert panel.outputs[1]['data']['text/html'] == 'new metrics'\n"
            "assert panel.outputs[0]['text'] == 'before\\n'\n"
            "assert panel.outputs[2]['text'] == 'after\\n'\n")
        message_id = self.client.execute(code)
        self.assertEqual(self.reply(message_id)['status'], 'ok')
        messages = self.output_until_idle(message_id)
        self.assertFalse(any(m['msg_type'] in ('clear_output', 'stream', 'error') for m in messages))
        displays = [m for m in messages if m['msg_type'] == 'display_data']
        self.assertEqual(len(displays), 1)
        self.assertIn('application/vnd.jupyter.widget-view+json', displays[0]['content']['data'])

    def test_batch_pause_allows_earlier_cells_without_unlocking_downstream(self):
        self.assertEqual(self.reply(self.client.execute(
            f"import sys\nsys.path.insert(0, {str(ROOT)!r})\n"
            "from calmar.execution import pause_before_batch\n"
            "earlier_runs = 0\ndownstream_ran = False"))["status"], "ok")
        try:
            # These are the saved detailed notebook IDs, sent as JupyterLab
            # sends them. No imaging or data acquisition is executed.
            self.assertEqual(self.execute_cell("gate = pause_before_batch()", "calmar-step-39")["status"], "ok")
            for _ in range(2):
                reply = self.execute_cell("earlier_runs += 1\nassert gate.paused", "calmar-step-23")
                self.assertEqual(reply["status"], "ok", reply)
            for cell_id in ("calmar-step-42", "calmar-step-81", "unknown-cell"):
                reply = self.execute_cell("downstream_ran = True", cell_id)
                self.assertEqual(reply["ename"], "InputRejected")
            self.assertEqual(self.execute_cell(
                "assert earlier_runs == 2 and not downstream_ran and gate.paused\n"
                "gate.navigation._receive(None, {'event': 'cell-order', "
                "'ids': ['inserted-above', 'calmar-step-39', 'calmar-step-42', 'calmar-step-23'], "
                "'batch_start': 'calmar-step-42'}, [])", "calmar-step-23")["status"], "ok")
            self.assertEqual(self.execute_cell("assert gate.paused", "inserted-above")["status"], "ok")
            # Moving a previously allowed cell below the boundary blocks it.
            self.assertEqual(self.execute_cell("downstream_ran = True", "calmar-step-23")["ename"], "InputRejected")
        finally:
            self.assertEqual(self.reply(self.client.execute("%calmar_continue batch"))["status"], "ok")
        self.assertEqual(self.execute_cell("assert not downstream_ran\ndownstream_ran = True", "calmar-step-42")["status"], "ok")

    def test_client_without_cell_metadata_can_rerun_viewer_before_batch(self):
        setup = (f"import sys\nsys.path.insert(0, {str(ROOT)!r})\n"
                 "from calmar.execution import pause_before_batch\n"
                 "RUN_TEST = True\nshow_timings = lambda **kw: None\n"
                 "class StopExecution(Exception): pass\n")
        self.assertEqual(self.reply(self.client.execute(setup))["status"], "ok")
        # The real client omitted cellId even at checkpoint creation. Exercise
        # its unmarked legacy cell, then rerun a marked/edited viewer cell.
        source = ''.join(CELLS[38]['source'])
        source = '\n'.join(line for line in source.splitlines() if not line.startswith('# CALMAR_CELL_ID:'))
        self.assertEqual(self.execute_cell(source, None)['ename'], 'StopExecution')
        try:
            reply = self.execute_cell(
                '# CALMAR_CELL_ID: calmar-step-35\n'
                'assert get_ipython()._calmar_batch_checkpoint.paused\nviewer_rerun_allowed = True', None)
            self.assertEqual(reply['status'], 'ok', reply)
            blocked = self.execute_cell('# CALMAR_CELL_ID: calmar-step-42\nraise AssertionError("Must not run")', None)
            self.assertEqual(blocked['ename'], 'InputRejected')
        finally:
            self.assertEqual(self.reply(self.client.execute('%calmar_continue batch'))['status'], 'ok')

    def click_widget(self, comm_id, *, acknowledged=True):
        # Send the same widget message as a frontend click. Executing Python
        # button.click() in another cell would itself be blocked by the gate.
        message = self.client.session.msg("comm_msg", content={
            "comm_id": comm_id,
            "data": {"method": "custom", "content": {"event": "click"}},
        })
        self.client.shell_channel.send(message)
        messages = self.output_until_idle(message["header"]["msg_id"])
        if not acknowledged:
            return
        self.assertTrue(any(
            m["msg_type"] == "comm_msg"
            and m["content"].get("comm_id") == comm_id
            and m["content"].get("data", {}).get("state", {}).get("disabled") is True
                    for m in messages), "Button did not acknowledge the click")

    def test_remaining_stops_allow_upstream_and_checkpoint_cells_in_both_notebooks(self):
        self.assertEqual(self.reply(self.client.execute(
            f"import sys\nsys.path.insert(0, {str(ROOT)!r})\n"
            "from calmar.execution import ExecutionCheckpoint, pause_for_qc\n"
            "from pathlib import Path"))["status"], "ok")
        for filename, stops in (
            ("lesion-interpretation-pipeline.ipynb", [("qc", "calmar-step-51"), ("report", "calmar-step-79")]),
            ("calmar-guided.ipynb", [("inputs", "d49f8035"), ("qc", "0b6d41b5"), ("report", "972e1347")]),
        ):
            cells = json.loads((ROOT / filename).read_text())["cells"]
            ids = [cell["id"] for cell in cells]
            for kind, boundary in stops:
                with self.subTest(notebook=filename, stop=kind), tempfile.TemporaryDirectory() as temporary:
                    index = ids.index(boundary)
                    earlier = next((c["id"] for c in reversed(cells[:index]) if c["cell_type"] == "code"), boundary)
                    later = next(c["id"] for c in cells[index+1:] if c["cell_type"] == "code")
                    code = (f"root = Path({temporary!r})\ndownstream_ran = False\n"
                            + ("gate = pause_for_qc([dict(subject='sub-fixture', session='ses-1')], lambda e: root)"
                               if kind == "qc" else "gate = ExecutionCheckpoint(get_ipython(), 'Wait for the choice')"))
                    self.assertEqual(self.execute_cell(code, boundary)["status"], "ok")
                    cleanup_id = boundary
                    try:
                        for cell_id in (earlier, boundary):
                            reply = self.execute_cell("assert gate.paused\nassert not downstream_ran", cell_id)
                            self.assertEqual(reply["status"], "ok", reply)
                        self.assertEqual(self.execute_cell("downstream_ran = True", later)["ename"], "InputRejected")
                        self.assertEqual(list(Path(temporary).glob('QC_decision.json')), [])
                        # An unsaved insertion above the stop is runnable; moving
                        # the stop out of the order leaves everything blocked.
                        order = ["new-earlier", boundary, later]
                        self.assertEqual(self.execute_cell(f"gate._update_cell_order({order!r})", boundary)["status"], "ok")
                        self.assertEqual(self.execute_cell("assert gate.paused", "new-earlier")["status"], "ok")
                        self.assertEqual(self.execute_cell("downstream_ran = True", later)["ename"], "InputRejected")
                    finally:
                        self.assertEqual(self.execute_cell("gate.close()", cleanup_id)["status"], "ok")
                    self.assertEqual(self.execute_cell("assert not downstream_ran\nassert not gate.paused", later)["status"], "ok")

    def test_checkpoint_enforces_pause_even_when_client_continues_after_errors(self):
        for run_test, stop_on_error in ((True, True), (True, False), (False, True), (False, False)):
            with self.subTest(RUN_TEST=run_test, stop_on_error=stop_on_error):
                setup = f"import sys\nsys.path.insert(0, {str(ROOT)!r})\n"
                setup += "".join(CELLS[12]["source"]) + "\n"
                setup += "show_timings = lambda **kwargs: None\nqueued_ran = False\n"
                setup += "delayed_ran = False\n"
                # Browser navigation is exercised separately. Simulate its
                # prepare/approve exchange here while testing the kernel lock.
                setup += "from calmar.notebook_navigation import NotebookNavigation\n"
                setup += "NotebookNavigation.request = lambda self, role, callback, **kw: callback()\n"
                setup += f"RUN_TEST = {run_test!r}\n"
                self.assertEqual(self.reply(self.client.execute(setup))["status"], "ok")

                checkpoint = self.client.execute("".join(CELLS[38]["source"]), stop_on_error=stop_on_error)
                following = self.client.execute("queued_ran = True", stop_on_error=stop_on_error)
                stopped = self.reply(checkpoint)
                queued = self.reply(following)
                messages = self.output_until_idle(checkpoint)
                self.output_until_idle(following)

                if run_test:
                    self.assertEqual(stopped["status"], "error")
                    self.assertEqual(stopped["ename"], "StopExecution")
                    self.assertIn(queued["status"], ("aborted", "error"))
                    buttons = [m["content"]["comm_id"] for m in messages
                               if m["msg_type"] == "comm_open"
                               and m["content"].get("data", {}).get("state", {}).get("description")
                               == "Continue to batch"]
                    self.assertEqual(len(buttons), 1)

                    # Also cover a frontend that submits its next request only
                    # after the exception, once normal queue cancellation ends.
                    delayed_id = self.client.execute("delayed_ran = True", stop_on_error=False)
                    delayed = self.reply(delayed_id)
                    self.output_until_idle(delayed_id)
                    self.assertEqual(delayed["status"], "error")
                    self.assertEqual(delayed["ename"], "InputRejected")
                    self.click_widget(buttons[0])
                else:
                    self.assertEqual(stopped["status"], "ok")
                    self.assertEqual(queued["status"], "ok")

                # Old queued work stays cancelled. A new frontend execution works.
                manual = self.reply(self.client.execute(
                    f"assert queued_ran is {not run_test!r}\n"
                    "assert not delayed_ran\nmanual_ran = True\n"
                    "assert not any(getattr(t, '__self__', None) is "
                    "getattr(get_ipython(), '_calmar_batch_checkpoint', None) "
                    "for t in get_ipython().input_transformers_post)"))
                self.assertEqual(manual["status"], "ok")

    def test_qc_requires_choice_and_records_it_before_unlocking(self):
        tree = ast.parse("".join(CELLS[50]["source"]))
        start = next(i for i, node in enumerate(tree.body)
                     if isinstance(node, ast.ImportFrom) and node.module == "calmar"
                     and any(alias.name == "execution" for alias in node.names))
        end = next(i for i, node in enumerate(tree.body)
                   if isinstance(node, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == "_qc_checkpoint" for t in node.targets))
        checkpoint_code = ast.unparse(ast.Module(body=tree.body[start:end+1], type_ignores=[]))
        checkpoint_code += '\nraise StopExecution("Choose QC")'
        for label, choice in (("Do QC", "review_requested"), ("Skip QC", "skipped")):
            with self.subTest(choice=choice), tempfile.TemporaryDirectory() as temporary:
                entries = [{"subject": "sub-test", "session": ses} for ses in ("ses-1", "ses-2")]
                setup = (f"import sys, importlib\nfrom pathlib import Path\nsys.path.insert(0, {str(ROOT)!r})\n"
                         + "".join(CELLS[12]["source"]) + "\n"
                         + f"SUBJECTS = {entries!r}\nroot = Path({temporary!r})\n"
                         + "deriv_path_for = lambda e: root / e['subject'] / e['session']\n"
                         + "qc_queued_ran = qc_delayed_ran = False\n")
                self.assertEqual(self.reply(self.client.execute(setup))["status"], "ok")
                checkpoint = self.client.execute(checkpoint_code, stop_on_error=False)
                queued = self.client.execute("qc_queued_ran = True", stop_on_error=False)
                self.assertEqual(self.reply(checkpoint)["status"], "error")
                self.assertIn(self.reply(queued)["status"], ("error", "aborted"))
                messages = self.output_until_idle(checkpoint)
                self.output_until_idle(queued)
                buttons = [m["content"]["comm_id"] for m in messages
                           if m["msg_type"] == "comm_open"
                           and m["content"].get("data", {}).get("state", {}).get("description") == label]
                self.assertEqual(len(buttons), 1)
                delayed = self.client.execute("qc_delayed_ran = True", stop_on_error=False)
                self.assertEqual(self.reply(delayed)["ename"], "InputRejected")
                self.output_until_idle(delayed)
                self.assertEqual(list(Path(temporary).rglob("QC_decision.json")), [])
                self.click_widget(buttons[0])
                for entry in entries:
                    record = Path(temporary) / entry["subject"] / entry["session"] / "QC_decision.json"
                    data = json.loads(record.read_text())
                    self.assertEqual(data["session"], entry["session"])
                    self.assertEqual(data["events"][-1]["choice"], choice)
                manual = self.client.execute(
                    "assert not qc_queued_ran and not qc_delayed_ran\n"
                    "assert not _qc_checkpoint.paused\nqc_manual_ran = True")
                self.assertEqual(self.reply(manual)["status"], "ok")

    def test_widget_free_recovery_is_explicit_and_preserves_qc_decision(self):
        setup = (f"import sys\nsys.path.insert(0, {str(ROOT)!r})\n"
                 "from calmar.execution import pause_before_batch, pause_for_qc\n"
                 "from pathlib import Path\nran_without_permission = False\n")
        self.assertEqual(self.reply(self.client.execute(setup))["status"], "ok")
        paused = self.client.execute("pause_before_batch()", stop_on_error=False)
        self.assertEqual(self.reply(paused)["status"], "ok")
        messages = self.output_until_idle(paused)
        self.assertTrue(any("%calmar_continue batch" in m["content"].get("data", {}).get("text/markdown", "")
                            for m in messages if m["msg_type"] == "display_data"))
        for code in ("ran_without_permission = True", "%calmar_continue skip-qc",
                     "%calmar_continue batch\nran_without_permission = True"):
            reply = self.reply(self.client.execute(code, stop_on_error=False))
            self.assertEqual(reply["ename"], "InputRejected")
        self.assertEqual(self.reply(self.client.execute("%calmar_continue batch"))["status"], "ok")
        self.assertEqual(self.reply(self.client.execute(
            "assert not ran_without_permission\nassert not get_ipython()._calmar_batch_checkpoint.paused"))["status"], "ok")
        with tempfile.TemporaryDirectory() as temporary:
            paused = self.client.execute(
                f"pause_for_qc([dict(subject='sub-fixture',session='ses-1')], lambda e: Path({temporary!r}))")
            self.assertEqual(self.reply(paused)["status"], "ok")
            self.output_until_idle(paused)
            self.assertEqual(self.reply(self.client.execute("%calmar_continue batch"))["ename"], "InputRejected")
            self.assertEqual(list(Path(temporary).glob("QC_decision.json")), [])
            self.assertEqual(self.reply(self.client.execute("%calmar_continue skip-qc"))["status"], "ok")
            data = json.loads((Path(temporary)/"QC_decision.json").read_text())
            self.assertEqual(data["events"][-1]["choice"], "skipped")


if __name__ == "__main__":
    unittest.main()
