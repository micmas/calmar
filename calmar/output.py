"""Output panels that work with server-side notebook execution.

The collaborative server also handles IOPub clear_output messages, outside the
frontend widget's capture hook. Capture locally and sync the Output model's
contents instead, so refreshing a panel cannot erase its containing cell.
"""
import io
import sys
import traceback

import ipywidgets as widgets
from IPython.utils.capture import capture_output


class _Stream(io.TextIOBase):
    def __init__(self, records, name):
        self.records, self.name = records, name

    @property
    def encoding(self):
        return "utf-8"

    def write(self, text):
        if text:
            if self.records and self.records[-1].get("name") == self.name:
                self.records[-1]["text"] += text
            else:
                self.records.append(dict(output_type="stream", name=self.name, text=text))
        return len(text)

    def flush(self):
        pass


class Output(widgets.Output):
    def __enter__(self):
        context = capture_output()
        context.__enter__()
        records = context.shell.display_pub.outputs if context.display else []
        frame = dict(context=context, records=records, cleared=False)
        stack = self.__dict__.setdefault("_capture_stack", [])
        stack.append(frame)

        def clear(wait=False):
            records.clear()
            frame["cleared"] = True

        if context.display:
            context.shell.display_pub.clear_output = clear
        sys.stdout = _Stream(records, "stdout")
        sys.stderr = _Stream(records, "stderr")
        return self

    def __exit__(self, exc_type, exc_value, tb):
        frame = self._capture_stack.pop()
        frame["context"].__exit__(exc_type, exc_value, tb)
        records = frame["records"]
        if exc_type is not None:
            records.append(dict(output_type="error", ename=exc_type.__name__,
                                evalue=str(exc_value),
                                traceback=traceback.format_exception(exc_type, exc_value, tb)))
        outputs = []
        for record in records:
            if "output_type" in record:
                outputs.append(record)
            else:
                outputs.append(dict(output_type="display_data", data=record["data"],
                                    metadata=record.get("metadata") or {}))
        previous = () if frame["cleared"] else self.outputs
        self.outputs = (*previous, *outputs)
        return exc_type is not None

    def clear_output(self, *args, **kwargs):
        stack = self.__dict__.get("_capture_stack", [])
        if stack:
            stack[-1]["records"].clear()
            stack[-1]["cleared"] = True
        else:
            self.outputs = ()
