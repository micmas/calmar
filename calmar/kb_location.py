"""Resolve and describe the stroke aphasia knowledge-base checkout."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess


_REQUIRED = (Path("scripts/aphasia_kb.py"), Path("regions"))


def _is_kb_root(path: Path) -> bool:
    return (path / _REQUIRED[0]).is_file() and (path / _REQUIRED[1]).is_dir()


def resolve_kb_root(project_dir=None, environ=None) -> tuple[Path, str]:
    """Return ``(root, reason)`` for the KB used by this CALMaR checkout.

    ``CALMAR_KB_ROOT`` is a strict explicit override. Without it, a sibling
    working copy is preferred over CALMaR's pinned submodule.
    """
    project = Path(project_dir or Path(__file__).resolve().parents[1]).expanduser().resolve()
    environment = os.environ if environ is None else environ
    override = str(environment.get("CALMAR_KB_ROOT", "")).strip()
    if override:
        candidates = [(Path(override).expanduser().resolve(), "CALMAR_KB_ROOT override")]
    else:
        candidates = [
            (project.parent / "stroke-aphasia-kb", "sibling working copy"),
            (project / "stroke-aphasia-kb", "pinned CALMaR submodule"),
        ]
    for root, reason in candidates:
        root = root.resolve()
        if _is_kb_root(root):
            return root, reason
    attempted = "\n".join(
        f"  - {root.resolve()} ({reason}; expected scripts/aphasia_kb.py and regions/)"
        for root, reason in candidates)
    prefix = ("CALMAR_KB_ROOT is set but is not a stroke aphasia knowledge base."
              if override else "Could not locate the stroke aphasia knowledge base.")
    raise FileNotFoundError(f"{prefix}\nPaths tried:\n{attempted}")


def kb_git_state(kb_root) -> dict:
    """Return the checkout's HEAD commit/date and whole-tree dirty state."""
    root = Path(kb_root).expanduser().resolve()

    def git(*args):
        try:
            completed = subprocess.run(
                ["git", "-C", str(root), *args], capture_output=True, text=True,
                timeout=20, check=False)
        except (OSError, subprocess.TimeoutExpired):
            return None
        return completed.stdout.strip() if completed.returncode == 0 else None

    top_level = git("rev-parse", "--show-toplevel")
    if top_level is None or Path(top_level).resolve() != root:
        return {"commit": None, "date": None, "uncommitted": None}
    status = git("status", "--porcelain", "--untracked-files=normal")
    return {
        "commit": git("rev-parse", "--short=12", "HEAD"),
        "date": git("show", "-s", "--format=%cs", "HEAD"),
        "uncommitted": None if status is None else bool(status),
    }


def kb_selection_text(kb_root, reason) -> str:
    """One traceable notebook line describing the selected checkout."""
    root = Path(kb_root).expanduser().resolve()
    state = kb_git_state(root)
    revision = (f"git {state['commit']} ({state['date']})"
                if state["commit"] else "git version unknown")
    working = ("working-tree status unknown" if state["uncommitted"] is None else
               "with uncommitted changes" if state["uncommitted"] else "clean working tree")
    return f"Knowledge base: {root} ({reason}); {revision}; {working}."
