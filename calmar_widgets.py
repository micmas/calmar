"""Shared widget helpers for the CALMaR notebook.

Solves two structural problems with the interactive cells:

1. WebGL context exhaustion. Browsers cap live WebGL contexts (~16).
   Creating a new ``NiiVue()`` on every widget change silently kills the
   oldest canvases — viewers go blank and never recover. ``viewer(key)``
   returns ONE persistent instance per key; callbacks swap
   ``nv.volumes`` in place instead of rebuilding the widget.

2. Volume bytes over the kernel websocket. ipyniivue's ``path=`` mode
   reads the whole file in the kernel and ships it through the comm on
   every render. ``vol(path)`` rewrites servable paths to a ``url=``
   spec so the *browser* fetches the file from the Jupyter file server
   (with normal HTTP caching); the kernel never touches the bytes.
   Files outside the server root (e.g. /tmp) fall back to ``path=``.

The URL base is auto-detected per user (JupyterHub sets
JUPYTERHUB_SERVICE_PREFIX for whoever runs the notebook), so nothing
here is machine- or user-specific. CONFIG["NIIVUE_URL_BASE"] can
override it: None = auto-detect, False = disable URL mode entirely
(always send bytes), or an explicit prefix like "/user/alice/".
"""

import os
from pathlib import Path
from urllib.parse import quote

from ipyniivue import NiiVue

# ── URL-mode configuration ──────────────────────────────────────────
_URL_BASE = None      # e.g. "/user/micmas/"; False disables URL mode
_SERVE_ROOT = None    # filesystem root the Jupyter server serves from
_configured = False


def _detect_server():
    """Return (base_url, root_dir) of the running Jupyter server."""
    base = os.environ.get("JUPYTERHUB_SERVICE_PREFIX")
    root = None
    try:
        from jupyter_server import serverapp
        cwd = Path.cwd()
        best = None
        for s in serverapp.list_running_servers():
            r = Path(s.get("root_dir") or s.get("notebook_dir") or "")
            try:
                cwd.relative_to(r)
            except ValueError:
                continue
            # prefer the deepest root that still contains the notebook
            if best is None or len(r.parts) > len(best[1].parts):
                best = (s.get("base_url") or "/", r)
        if best is not None:
            if base is None:
                base = best[0]
            root = best[1]
    except Exception:
        pass
    if base is None:
        base = "/"
    if root is None:
        root = Path.home()
    if not base.endswith("/"):
        base += "/"
    return base, root


def configure(url_base=None, serve_root=None):
    """Set URL mode explicitly. Called from the notebook CONFIG cell.

    url_base : None → auto-detect; False → disable URL mode (send
               bytes through the kernel, the old behaviour); or an
               explicit prefix such as "/user/alice/".
    """
    global _URL_BASE, _SERVE_ROOT, _configured
    auto_base, auto_root = _detect_server()
    if url_base is None:
        _URL_BASE = auto_base
    elif url_base is False:
        _URL_BASE = False
    else:
        _URL_BASE = url_base if str(url_base).endswith("/") else f"{url_base}/"
    _SERVE_ROOT = Path(serve_root) if serve_root else auto_root
    _configured = True


def _ensure_configured():
    if not _configured:
        configure()


def vol(path, **kw):
    """Build one NiiVue volume spec for ``load_volumes``.

    Servable files become {"url": ...} so the browser fetches (and
    caches) them directly; anything else stays {"path": ...}. The file
    mtime is appended as a query param, so a regenerated mask gets a
    fresh URL (never a stale browser-cache hit) while unchanged files
    stay cached.
    """
    _ensure_configured()
    p = Path(os.path.abspath(os.fspath(path)))  # keep symlinks unresolved
    if _URL_BASE is not False:
        try:
            rel = p.relative_to(_SERVE_ROOT)
            try:
                v = int(p.stat().st_mtime)
            except OSError:
                v = 0
            url = f"{_URL_BASE}files/{quote(rel.as_posix())}?v={v}"
            return {"url": url, **kw}
        except ValueError:
            pass  # outside the server root (e.g. /tmp) → bytes fallback
    return {"path": str(p), **kw}


def vols(specs):
    """Convert a list of {"path": ...} volume dicts via ``vol()``."""
    out = []
    for s in specs:
        s = dict(s)
        p = s.pop("path", None)
        if p is not None and "url" not in s and "data" not in s:
            out.append(vol(p, **s))
        else:
            out.append(s)
    return out


# ── Persistent viewer registry ──────────────────────────────────────
_VIEWERS = {}


def viewer(key, height=300, colorbar=False, colorbar_height=None):
    """Return the persistent NiiVue instance for ``key``.

    Created on first use; later calls return the same widget so
    re-running a cell (or a widget callback) reuses the existing WebGL
    canvas instead of leaking a new one. Display options are applied
    only on creation.
    """
    nv = _VIEWERS.get(key)
    if nv is None:
        nv = NiiVue(height=height)
        if colorbar:
            nv.opts.is_colorbar = True
        if colorbar_height is not None:
            nv.opts.colorbar_height = colorbar_height
        _VIEWERS[key] = nv
    return nv


def show(key, volumes, **viewer_kwargs):
    """One-liner: persistent viewer + URL-mode volumes, ready to display.

    ``volumes`` is the usual list of {"path": ..., "colormap": ...}
    dicts. Returns the NiiVue widget (pass it to ``display``).
    """
    nv = viewer(key, **viewer_kwargs)
    nv.load_volumes(vols(volumes))
    return nv


# ── Cached voxel counts ─────────────────────────────────────────────
_VOXCOUNT_CACHE = {}


def voxel_count(path):
    """Nonzero-voxel count of a NIfTI mask, cached by (path, mtime).

    Returns None if the file is missing/unreadable. Avoids repeated
    full float64 decompression when diagnostic cells are re-run.
    """
    import numpy as np
    import nibabel as nib
    p = Path(path)
    try:
        mtime = p.stat().st_mtime
    except OSError:
        return None
    key = (str(p), mtime)
    if key in _VOXCOUNT_CACHE:
        return _VOXCOUNT_CACHE[key]
    try:
        n = int((np.asanyarray(nib.load(str(p)).dataobj) > 0).sum())
    except Exception:
        n = None
    _VOXCOUNT_CACHE[key] = n
    return n
