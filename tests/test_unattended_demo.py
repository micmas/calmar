"""Controller failure tests with a fake kernel; no imaging jobs are submitted."""
import asyncio
from contextlib import asynccontextmanager
import importlib.util
import json
import os
from pathlib import Path
import signal
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("unattended_demo", ROOT / "src/python/unattended_demo.py")
demo = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(demo)


class SilentKernel:
    def __init__(self, *args, **kwargs):
        pass

    def set_widgets_metadata(self):
        pass

    @asynccontextmanager
    async def async_setup_kernel(self, **kwargs):
        yield

    async def async_execute_cell(self, cell, index):
        # Simulate a checkpoint guard replacing every cell with `pass`.
        return cell


def args():
    return SimpleNamespace(source=str(ROOT / "lesion-interpretation-pipeline.ipynb"),
        optional="all", reports="reports/demo-test", build_only=False, completion="completion.json")


def test_silent_checkpoint_cannot_publish_success(tmp_path, monkeypatch):
    monkeypatch.setattr(demo, "NotebookClient", SilentKernel)
    monkeypatch.setenv("SLURM_JOB_ID", "test")
    with pytest.raises(FileNotFoundError, match="completion-proof"):
        asyncio.run(demo.execute(args(), tmp_path, tmp_path / "run"))
    status = json.loads((tmp_path / "run/status.json").read_text())
    assert status["state"] == "failed"
    assert not (tmp_path / "completion.json").exists()


def test_shutdown_signal_saves_interrupted_state(tmp_path, monkeypatch):
    async def scenario():
        entered = asyncio.Event()

        class WaitingKernel(SilentKernel):
            async def async_execute_cell(self, cell, index):
                entered.set()
                await asyncio.Event().wait()

        monkeypatch.setattr(demo, "NotebookClient", WaitingKernel)
        monkeypatch.setenv("SLURM_JOB_ID", "test")
        task = asyncio.create_task(demo.execute(args(), tmp_path, tmp_path / "run"))
        await asyncio.wait_for(entered.wait(), timeout=10)
        os.kill(os.getpid(), signal.SIGUSR1)
        with pytest.raises(asyncio.CancelledError):
            await task

    asyncio.run(scenario())
    status = json.loads((tmp_path / "run/status.json").read_text())
    assert status["state"] == "interrupted"
    assert status["signal"] == signal.SIGUSR1
    assert "child jobs may still be running" in status["error"]
    assert Path(status["notebook"]).is_file()
    assert not (tmp_path / "completion.json").exists()
