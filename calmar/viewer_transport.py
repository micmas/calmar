"""Keep local image bytes out of widget restoration; serve bounded chunks on demand."""

from pathlib import Path
from types import MethodType
from urllib.parse import quote

from ipyniivue.widget import Volume, NiiVue
import traitlets as t
import numpy as np

CHUNK_BYTES = 256 * 1024
_file_server = None


def configure_file_server(base_url, root):
    """Offer an authenticated HTTP path; keep comm transport as a fallback."""
    global _file_server
    _file_server = (base_url.rstrip('/') + '/', Path(root).absolute())


def _file_descriptor(value, widget):
    if value is None:
        return {"name": None, "data": None}
    path = Path(value).absolute()
    result = {"name": path.name, "data": None, "calmar_lazy": True}
    if _file_server:
        base, root = _file_server
        try:
            relative = path.relative_to(root)
            result['url'] = f"{base}files/{quote(relative.as_posix())}?v={path.stat().st_mtime_ns}"
        except (ValueError, OSError):
            pass
    return result


def _lazy_path():
    return t.Union([t.Instance(Path), t.Unicode()], default_value=None,
                   allow_none=True).tag(sync=True, to_json=_file_descriptor)


def _omit_image(value, widget):
    # NiiVue sends decoded pixels back to Python after loading. Keep them
    # available in Python, but do not send them back during widget restoration:
    # the frontend loads the compressed source instead. Drawing state is separate.
    return None


def _image_trait():
    return t.Instance(np.ndarray, default_value=None, allow_none=True).tag(
        sync=True, to_json=_omit_image)


class LazyVolume(Volume):
    path = _lazy_path()
    paired_img_path = _lazy_path()
    img = _image_trait()


def make_lazy(volume):
    """Upgrade an existing model without replacing its ID, settings or callbacks."""
    if volume.trait_metadata("path", "to_json") is not _file_descriptor:
        volume.add_traits(path=_lazy_path(), paired_img_path=_lazy_path())
    if volume.trait_metadata('img', 'to_json') is not _omit_image:
        volume.add_traits(img=_image_trait())


def attach_transport(viewer):
    def receive(_widget, content, buffers):
        if content.get("type") != "calmar:read-volume":
            return
        request = content.get("request")
        if not isinstance(request, str) or len(request) > 100:
            return
        try:
            field = content.get("field")
            if field not in ("path", "paired_img_path"):
                raise ValueError("Unknown image source")
            # The browser can request only an existing volume owned by this
            # viewer, never an arbitrary path supplied in a frontend message.
            volume = next(v for v in viewer.volumes
                          if v.model_id == content.get("volume"))
            source = getattr(volume, field)
            if source is None:
                raise ValueError("Image source is unavailable")
            with Path(source).open("rb") as stream:
                offset = 0
                while chunk := stream.read(CHUNK_BYTES):
                    viewer.send({"type": "calmar:volume-chunk", "request": request,
                                 "offset": offset}, buffers=[chunk])
                    offset += len(chunk)
                viewer.send({"type": "calmar:volume-complete", "request": request,
                             "size": offset})
        except Exception as error:
            viewer.send({"type": "calmar:volume-error", "request": request,
                         "message": f"Could not read image ({type(error).__name__})."})

    viewer._calmar_file_handler = receive
    # NiiVue overrides Widget._handle_custom_msg and does not dispatch on_msg
    # callbacks. Preserve its native event handling and intercept only our type.
    def dispatch(self, content, buffers):
        if content.get("type") == "calmar:read-volume":
            self._calmar_file_handler(self, content, buffers)
        else:
            NiiVue._handle_custom_msg(self, content, buffers)
    viewer._handle_custom_msg = MethodType(dispatch, viewer)
