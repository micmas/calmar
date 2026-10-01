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
   Path mode carries small file descriptors. The frontend tries authenticated
   HTTP first, then falls back to 256 KiB kernel messages for inaccessible files.
   This also loads while the kernel is computing and caches compressed bytes.
   Decoded image arrays are omitted from widget restoration.

The URL base is auto-detected per user (JupyterHub sets
JUPYTERHUB_SERVICE_PREFIX for whoever runs the notebook), so nothing
here is machine- or user-specific. CONFIG["NIIVUE_URL_BASE"] can
override it: None = direct URL mode, False = authenticated lazy transport with
kernel fallback, or an explicit prefix like "/user/alice/".
"""

import os
import json
from .widget_lifecycle import close_widget
from .output import Output
from pathlib import Path
from types import MethodType
from collections import OrderedDict
from urllib.parse import quote

from ipyniivue import NiiVue
from .viewer_transport import LazyVolume, attach_transport, make_lazy, configure_file_server


def _deferred_viewer_source():
    template = Path(__file__).with_name("viewer_bootstrap.js").read_text()
    return template.replace("__CALMAR_VIEWER_SOURCE__", json.dumps(str(NiiVue._esm)))


class _DeferredNiiVue(NiiVue):
    """Load the imaging frontend during rendering, outside model startup timeout."""

    _esm = _deferred_viewer_source()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        attach_transport(self)

    def load_volumes(self, volumes):
        models = [LazyVolume(**v) if isinstance(v, dict) else v for v in volumes]
        for model in models:
            make_lazy(model)
        NiiVue.load_volumes(self, models)

    def add_volume(self, volume):
        model = LazyVolume(**volume) if isinstance(volume, dict) else volume
        make_lazy(model)
        NiiVue.add_volume(self, model)

# ── URL-mode configuration ──────────────────────────────────────────
_URL_BASE = globals().get("_URL_BASE")  # False disables URL mode
_SERVE_ROOT = globals().get("_SERVE_ROOT")  # Jupyter server filesystem root
_configured = globals().get("_configured", False)


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

    url_base : None → auto-detect; False → authenticated lazy transport; or an
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
    configure_file_server(auto_base, _SERVE_ROOT)
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
                v = p.stat().st_mtime_ns
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
_VIEWERS = globals().get("_VIEWERS", {})


def refresh_viewer_frontends():
    """Update live viewer loaders without rerunning analysis or changing volumes.

    A browser reload recreates any frontend models already rejected by a timeout.
    Keep the registry across module reloads so the existing views can be repaired.
    """
    source = _deferred_viewer_source()
    updated = 0
    for nv in _VIEWERS.values():
        # Keep current output IDs and selections when repairing an open kernel.
        attach_transport(nv)
        nv.load_volumes = MethodType(_DeferredNiiVue.load_volumes, nv)
        nv.add_volume = MethodType(_DeferredNiiVue.add_volume, nv)
        for volume in nv.volumes:
            make_lazy(volume)
            volume.send_state(["path", "paired_img_path"])
        if nv._esm != source:
            nv._esm = source
            updated += 1
    return updated


def viewer(key, height=300, colorbar=False, colorbar_height=None):
    """Return the existing NiiVue instance for ``key`` (get-or-create).

    Use this inside widget CALLBACKS, where the viewer created at the
    top of the cell must be updated in place. Display options are
    applied only on creation.
    """
    nv = _VIEWERS.get(key)
    if nv is None:
        nv = _DeferredNiiVue(height=height)
        if colorbar:
            nv.opts.is_colorbar = True
        if colorbar_height is not None:
            nv.opts.colorbar_height = colorbar_height
        _VIEWERS[key] = nv
    return nv


def fresh_viewer(key, **viewer_kwargs):
    """Close any previous viewer under ``key`` and create a new one.

    Use this at the TOP of a cell (re-)run. A fresh widget renders
    reliably even after the notebook document was reloaded from disk
    (a re-displayed pre-reload model can silently fail to render), and
    closing the predecessor removes its views so WebGL contexts do not
    accumulate across re-runs. Callbacks within the cell should keep
    using the returned instance (or ``viewer(key)``) so interactions
    update it in place instead of churning widgets.
    """
    old = _VIEWERS.pop(key, None)
    if old is not None:
        try:
            for model in getattr(old, "_calmar_layer_cache", {}).values():
                model.close()
            close_widget(old)
        except Exception:
            pass
    return viewer(key, **viewer_kwargs)


def show(key, volumes, **viewer_kwargs):
    """One-liner for run-once cells: fresh viewer + volumes, ready to
    display.

    ``volumes`` is the usual list of {"path": ..., "colormap": ...}
    dicts. Returns the NiiVue widget (pass it to ``display``).
    """
    nv = fresh_viewer(key, **viewer_kwargs)
    nv.load_volumes(vols(volumes))
    return nv


def set_volumes(viewer, specs, *, cache_size=12):
    """Reuse unchanged layers so switching an atlas/mask does not reload the brain."""
    cache = getattr(viewer, "_calmar_layer_cache", None)
    if cache is None:
        cache = viewer._calmar_layer_cache = OrderedDict()
    models = []
    for spec in vols(specs):
        if "data" in spec:
            # In-memory sources are unusual; callers can cache them to disk.
            models.append(LazyVolume(**spec))
            continue
        identity = dict(spec)
        # Visibility is mutable UI state, not the identity of an image layer.
        identity.pop('opacity', None)
        identity.pop('colorbar_visible', None)
        if "path" in spec:
            p = Path(spec["path"])
            stat = p.stat()
            identity.update(path=str(p.absolute()), mtime_ns=stat.st_mtime_ns, size=stat.st_size)
        key = json.dumps(identity, sort_keys=True, default=str)
        model = cache.get(key)
        if model is None:
            model = LazyVolume(**spec)
            cache[key] = model
        else:
            for setting in ("opacity", "colormap", "cal_min", "cal_max", "colorbar_visible"):
                if setting in spec:
                    setattr(model, setting, spec[setting])
        cache.move_to_end(key)
        models.append(model)
    viewer.volumes = models
    for key in list(cache):
        if len(cache) <= cache_size:
            break
        if cache[key] not in models:
            cache.pop(key).close()


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
