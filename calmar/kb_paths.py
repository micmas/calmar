"""Where the aphasia knowledge base keeps its code.

The knowledge base is the separate repository micmas/stroke-aphasia-kb,
checked out here as the submodule ``stroke-aphasia-kb/``. Since October
2026 its Python modules (``aphasia_kb``, ``aphasia_rules``,
``atlas_mapping``, ``lesion_mapping``, ``export_webapp`` …) live in its
``scripts/`` folder; older checkouts kept them at the repository root.
Everything in CALMaR that imports from the KB goes through these two
helpers so either layout works.
"""
from pathlib import Path
import sys


def kb_code_dir(kb_root) -> Path:
    """The folder that holds the KB's Python modules."""
    root = Path(kb_root).resolve()
    scripts = root / "scripts"
    return scripts if (scripts / "aphasia_kb.py").exists() else root


def add_kb_to_path(kb_root) -> Path:
    """Put the KB's code folder on ``sys.path`` (once) and return it."""
    code = kb_code_dir(kb_root)
    if str(code) not in sys.path:
        sys.path.insert(0, str(code))
    return code


def kb_content_paths(kb_root) -> tuple[str, ...]:
    """Paths (relative to ``kb_root``) whose content the interpretation depends on."""
    code = kb_code_dir(kb_root).relative_to(Path(kb_root).resolve())
    prefix = f"{code}/" if str(code) != "." else ""
    return ("regions", "impairments", "therapies", "predictors", "reviews", "ingredients",
            "citations.md", f"{prefix}aphasia_kb.py", f"{prefix}aphasia_rules.py")
