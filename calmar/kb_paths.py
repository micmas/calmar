"""Where the aphasia knowledge base keeps its code.

The knowledge base is the separate repository micmas/stroke-aphasia-kb,
checked out here as the submodule ``stroke-aphasia-kb/``. Since October
2026 its Python modules (``aphasia_kb``, ``aphasia_rules``,
``atlas_mapping``, ``lesion_mapping``, ``export_webapp`` …) live in its
``scripts/`` folder; older checkouts kept them at the repository root.
Everything in CALMaR that imports from the KB goes through these helpers
so either layout works and cached modules cannot come from another checkout.
"""
from pathlib import Path
import importlib
import sys


_KNOWN_CODE_DIRS = set()
_ACTIVE_CODE_DIR = None


def kb_code_dir(kb_root) -> Path:
    """The folder that holds the KB's Python modules."""
    root = Path(kb_root).resolve()
    scripts = root / "scripts"
    return scripts if (scripts / "aphasia_kb.py").exists() else root


def add_kb_to_path(kb_root) -> Path:
    """Make ``kb_root`` the active KB code folder and return it."""
    global _ACTIVE_CODE_DIR
    code = kb_code_dir(kb_root)
    previous = _ACTIVE_CODE_DIR
    _KNOWN_CODE_DIRS.add(code)
    for known in _KNOWN_CODE_DIRS:
        while str(known) in sys.path:
            sys.path.remove(str(known))
    sys.path.insert(0, str(code))
    if previous is not None and previous != code:
        _discard_kb_modules()
    _ACTIVE_CODE_DIR = code
    return code


def _discard_kb_modules():
    """Remove modules loaded from a known KB checkout from Python's cache."""
    for name, module in list(sys.modules.items()):
        filename = getattr(module, "__file__", None)
        if not filename:
            continue
        try:
            path = Path(filename).resolve()
        except (OSError, TypeError):
            continue
        if any(path == root or root in path.parents for root in _KNOWN_CODE_DIRS):
            sys.modules.pop(name, None)


def load_kb_modules(kb_root, *names):
    """Freshly import KB modules from one root, including local script edits."""
    code = kb_code_dir(kb_root)
    if not (code / "aphasia_kb.py").is_file():
        raise FileNotFoundError(
            f"No stroke aphasia knowledge-base code under {Path(kb_root).resolve()}; "
            "expected scripts/aphasia_kb.py")
    add_kb_to_path(kb_root)
    _discard_kb_modules()
    importlib.invalidate_caches()
    return tuple(importlib.import_module(name) for name in names)


def kb_content_paths(kb_root) -> tuple[str, ...]:
    """Paths (relative to ``kb_root``) whose content the interpretation depends on."""
    code = kb_code_dir(kb_root).relative_to(Path(kb_root).resolve())
    prefix = f"{code}/" if str(code) != "." else ""
    return ("regions", "impairments", "therapies", "predictors", "reviews", "ingredients",
            "citations.md", f"{prefix}aphasia_kb.py", f"{prefix}aphasia_rules.py")
