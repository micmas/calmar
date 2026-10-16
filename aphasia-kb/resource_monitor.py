"""
resource_monitor.py — sample GPU/CPU load while a local model runs.

Extraction is a single blocking HTTP call that can take minutes, during
which you otherwise have no idea whether the model is actually on the
GPU or has quietly spilled to CPU (the difference between 5 minutes and
50). This runs a background thread that samples cheaply and prints a
one-line summary at the end.

Two independent signals, both best-effort:

  * GPU offload — from Ollama's own /api/ps: how much of the loaded
    model sits in VRAM vs system RAM. This is the number that actually
    predicts speed on this hardware. 100% = fully on GPU.
  * CPU / RAM — from psutil if installed. Process-agnostic, whole-machine.

Neither is required; whatever isn't available is simply omitted. The
monitor must never be the reason an extraction fails, so every sample is
wrapped and errors are swallowed.
"""

from __future__ import annotations

import json
import threading
import time
import urllib.request
from dataclasses import dataclass, field

try:
    import psutil
    _HAVE_PSUTIL = True
except ImportError:
    _HAVE_PSUTIL = False


def _query_ps(host: str, timeout: float = 2.0) -> dict | None:
    try:
        with urllib.request.urlopen(f"{host}/api/ps", timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception:
        return None


def _gpu_offload_pct(ps: dict, model: str | None) -> float | None:
    """From /api/ps, the % of the (matching) loaded model held in VRAM.

    Ollama reports `size` (total) and `size_vram` per loaded model. When
    they're equal the model is fully GPU-resident; when size_vram is
    smaller, that fraction spilled to CPU RAM and inference crawls.
    """
    models = ps.get("models") or []
    if not models:
        return None
    m = None
    if model:
        m = next((x for x in models
                  if x.get("name", "").split(":")[0] == model.split(":")[0]),
                 None)
    m = m or models[0]
    total = m.get("size") or 0
    vram = m.get("size_vram")
    if not total or vram is None:
        return None
    return 100.0 * vram / total


@dataclass
class _Samples:
    gpu_offload: list[float] = field(default_factory=list)
    cpu_pct: list[float] = field(default_factory=list)
    ram_pct: list[float] = field(default_factory=list)


class ResourceMonitor:
    """Background sampler. Use as a context manager around a model call:

        with ResourceMonitor(host, model, live=True) as mon:
            ... blocking inference ...
        print(mon.summary())
    """

    def __init__(self, host: str, model: str | None = None, *,
                 interval: float = 5.0, live: bool = False):
        self.host = host.rstrip("/")
        self.model = model
        self.interval = interval
        self.live = live
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._s = _Samples()
        self._first_offload_warned = False

    # -- context manager ---------------------------------------------
    def __enter__(self) -> "ResourceMonitor":
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        return self

    def __exit__(self, *exc) -> bool:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=self.interval + 1)
        return False   # never suppress an exception from the inference

    # -- sampling loop -----------------------------------------------
    def _run(self) -> None:
        if _HAVE_PSUTIL:
            psutil.cpu_percent(interval=None)   # prime the first reading
        while not self._stop.is_set():
            self._sample_once()
            self._stop.wait(self.interval)

    def _sample_once(self) -> None:
        try:
            ps = _query_ps(self.host)
            off = _gpu_offload_pct(ps, self.model) if ps else None
            if off is not None:
                self._s.gpu_offload.append(off)
                if self.live:
                    self._live_line(off)
                if off < 99 and not self._first_offload_warned:
                    self._first_offload_warned = True
                    print(f"\n  ⚠ model is only {off:.0f}% on GPU — the rest "
                          f"spilled to CPU RAM. Expect it to be slow. Lower "
                          f"num_ctx (or use a smaller model) to fit.")
            if _HAVE_PSUTIL:
                self._s.cpu_pct.append(psutil.cpu_percent(interval=None))
                self._s.ram_pct.append(psutil.virtual_memory().percent)
        except Exception:
            pass   # a monitor must never break the run it's watching

    def _live_line(self, off: float) -> None:
        bits = [f"GPU offload {off:3.0f}%"]
        if _HAVE_PSUTIL and self._s.cpu_pct:
            bits.append(f"CPU {self._s.cpu_pct[-1]:2.0f}%")
            bits.append(f"RAM {self._s.ram_pct[-1]:2.0f}%")
        print(f"    · {'  '.join(bits)}", flush=True)

    # -- reporting ---------------------------------------------------
    def summary(self) -> str:
        s = self._s
        if not (s.gpu_offload or s.cpu_pct):
            return ("resource monitor: no samples (Ollama /api/ps "
                    "unavailable and psutil not installed)")
        parts: list[str] = []
        if s.gpu_offload:
            lo = min(s.gpu_offload)
            parts.append(f"GPU offload min {lo:.0f}% / "
                         f"avg {sum(s.gpu_offload)/len(s.gpu_offload):.0f}%")
        if s.cpu_pct:
            parts.append(f"CPU avg {sum(s.cpu_pct)/len(s.cpu_pct):.0f}% "
                         f"(peak {max(s.cpu_pct):.0f}%)")
        if s.ram_pct:
            parts.append(f"RAM peak {max(s.ram_pct):.0f}%")
        verdict = ""
        if s.gpu_offload and min(s.gpu_offload) >= 99:
            verdict = "  ✓ stayed fully on GPU"
        elif s.gpu_offload:
            verdict = "  ⚠ spilled off GPU at some point — see warning above"
        return "resource: " + "  ·  ".join(parts) + verdict


if __name__ == "__main__":
    # Quick manual check: sample the currently-loaded model for ~15s.
    import sys
    host = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:11434"
    print(f"sampling {host}/api/ps for 15s (psutil "
          f"{'on' if _HAVE_PSUTIL else 'off'}) ...")
    with ResourceMonitor(host, live=True, interval=3.0) as mon:
        time.sleep(15)
    print(mon.summary())
