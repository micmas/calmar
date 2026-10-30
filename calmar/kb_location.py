"""Resolve, update and describe the stroke aphasia knowledge-base checkout."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import subprocess


_REQUIRED = (Path("scripts/aphasia_kb.py"), Path("regions"))
_KB_UPDATE_STATUS = {}


def _is_kb_root(path: Path) -> bool:
    return (path / _REQUIRED[0]).is_file() and (path / _REQUIRED[1]).is_dir()


def resolve_kb_root(project_dir=None, environ=None) -> tuple[Path, str]:
    """Return ``(root, reason)`` for the KB used by this CALMaR checkout.

    ``CALMAR_KB_ROOT`` is a strict explicit override. Without it, a sibling
    working copy is preferred over CALMaR's submodule.
    """
    project = Path(project_dir or Path(__file__).resolve().parents[1]).expanduser().resolve()
    environment = os.environ if environ is None else environ
    override = str(environment.get("CALMAR_KB_ROOT", "")).strip()
    if override:
        candidates = [(Path(override).expanduser().resolve(), "CALMAR_KB_ROOT override")]
    else:
        candidates = [
            (project.parent / "stroke-aphasia-kb", "sibling working copy"),
            (project / "stroke-aphasia-kb", "CALMaR submodule"),
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


def update_kb_to_latest(kb_root, reason, environ=None) -> str:
    """Fast-forward a selected KB checkout to the latest ``origin/main``.

    Development notebooks call this once during Setup.  A checkout already
    containing ``origin/main`` may also contain local commits or uncommitted
    drafts; those are preserved.  A stale dirty or divergent checkout is
    rejected instead of silently mixing old KB code with current evidence.
    Set ``CALMAR_KB_UPDATE=off`` for a deliberately pinned/offline run; the
    report still records the exact commit and dirty state.
    """
    environment = os.environ if environ is None else environ
    policy = str(environment.get("CALMAR_KB_UPDATE", "latest")).strip().lower()
    if policy not in {"latest", "off"}:
        raise ValueError("CALMAR_KB_UPDATE must be 'latest' or 'off'")
    root = Path(kb_root).expanduser().resolve()

    def record(latest_verified, origin_main, message):
        _KB_UPDATE_STATUS[root] = {
            "latest_verified": latest_verified,
            "verified_origin_main": origin_main,
            "latest_status": message,
        }
        return message

    if policy == "off":
        return record(False, None, "Knowledge-base update disabled by CALMAR_KB_UPDATE=off.")

    git_environment = dict(os.environ, GIT_TERMINAL_PROMPT="0")

    def run(*args, timeout=20):
        try:
            completed = subprocess.run(
                ["git", "-C", str(root), *args], capture_output=True, text=True,
                timeout=timeout, check=False, env=git_environment)
        except (OSError, subprocess.TimeoutExpired) as error:
            raise RuntimeError(f"Could not check the latest knowledge base: {error}") from error
        if completed.returncode:
            detail = completed.stderr.strip() or completed.stdout.strip() or "git command failed"
            raise RuntimeError(f"Could not update the knowledge base at {root}: {detail}")
        return completed.stdout.strip()

    def is_ancestor(ancestor, descendant):
        try:
            completed = subprocess.run(
                ["git", "-C", str(root), "merge-base", "--is-ancestor", ancestor, descendant],
                capture_output=True, text=True, timeout=20, check=False, env=git_environment)
        except (OSError, subprocess.TimeoutExpired) as error:
            raise RuntimeError(f"Could not compare knowledge-base revisions: {error}") from error
        if completed.returncode == 0:
            return True
        if completed.returncode == 1:
            return False
        detail = completed.stderr.strip() or completed.stdout.strip() or "git merge-base failed"
        raise RuntimeError(f"Could not compare knowledge-base revisions: {detail}")

    top_level = Path(run("rev-parse", "--show-toplevel")).resolve()
    if top_level != root:
        raise RuntimeError(f"The selected knowledge base is not a standalone Git checkout: {root}")
    try:
        run("fetch", "--quiet", "origin",
            "+refs/heads/main:refs/remotes/origin/main", timeout=60)
    except RuntimeError as error:
        head = run("rev-parse", "HEAD")
        try:
            cached_main = run("rev-parse", "origin/main")
        except RuntimeError:
            cached_main = None
        return record(
            False, cached_main,
            f"WARNING: latest knowledge base not verified; using local HEAD {head[:12]}. "
            f"Fetch failed: {error}")
    head = run("rev-parse", "HEAD")
    latest = run("rev-parse", "origin/main")
    if head == latest:
        return record(True, latest, f"Knowledge base is current with origin/main ({latest[:12]}).")

    if is_ancestor(latest, head):
        return record(
            True, latest,
            f"Knowledge base includes current origin/main ({latest[:12]}) plus local commits; "
            "the exact HEAD will be recorded.")

    dirty = bool(run("status", "--porcelain", "--untracked-files=normal"))
    if dirty:
        raise RuntimeError(
            f"The knowledge base is behind origin/main ({latest[:12]}) and has uncommitted changes. "
            "Commit/stash them, or set CALMAR_KB_UPDATE=off for an explicitly pinned run.")

    if not is_ancestor(head, latest):
        raise RuntimeError(
            f"The knowledge-base checkout has diverged from origin/main ({latest[:12]}). "
            "Reconcile it explicitly instead of combining versions automatically.")

    branch = run("branch", "--show-current")
    if branch and branch != "main":
        raise RuntimeError(
            f"The knowledge base is on branch {branch!r}, behind origin/main ({latest[:12]}). "
            "Update that branch explicitly or select a current main checkout.")
    if branch == "main":
        run("merge", "--quiet", "--ff-only", "origin/main")
    else:
        run("checkout", "--quiet", "--detach", "origin/main")
    pointer_note = (" CALMaR's submodule pointer now differs from the committed release pin; "
                    "do not commit it unless intentionally updating the release."
                    if reason == "CALMaR submodule" else "")
    return record(
        True, latest,
        f"Knowledge base updated to latest origin/main ({latest[:12]}; {reason}).{pointer_note}")


def kb_git_state(kb_root) -> dict:
    """Return exact Git and dirty-content provenance for a KB checkout."""
    root = Path(kb_root).expanduser().resolve()
    git_environment = dict(os.environ, GIT_TERMINAL_PROMPT="0")

    def git(*args):
        try:
            completed = subprocess.run(
                ["git", "-C", str(root), *args], capture_output=True, text=True,
                timeout=20, check=False, env=git_environment)
        except (OSError, subprocess.TimeoutExpired):
            return None
        return completed.stdout.strip() if completed.returncode == 0 else None

    top_level = git("rev-parse", "--show-toplevel")
    if top_level is None or Path(top_level).resolve() != root:
        return {"commit": None, "date": None, "uncommitted": None}
    status = git("status", "--porcelain", "--untracked-files=normal")
    dirty = None if status is None else bool(status)
    state = {
        "commit": git("rev-parse", "HEAD"),
        "date": git("show", "-s", "--format=%cs", "HEAD"),
        "uncommitted": dirty,
        **_KB_UPDATE_STATUS.get(root, {
            "latest_verified": None, "verified_origin_main": None,
            "latest_status": "Latest origin/main was not checked in this process.",
        }),
    }
    origin_main = git("rev-parse", "origin/main")
    if origin_main:
        try:
            ancestry = subprocess.run(
                ["git", "-C", str(root), "merge-base", "--is-ancestor", "HEAD", origin_main],
                capture_output=True, text=True, timeout=20, check=False, env=git_environment)
            state["commit_on_origin_main"] = (
                ancestry.returncode == 0 if ancestry.returncode in (0, 1) else None)
        except (OSError, subprocess.TimeoutExpired):
            state["commit_on_origin_main"] = None
    else:
        state["commit_on_origin_main"] = None
    state["working_tree_sha256"] = None
    state["changed_paths"] = []
    if dirty:
        try:
            diff = subprocess.run(
                ["git", "-C", str(root), "diff", "--binary", "--no-ext-diff",
                 "--no-textconv", "--no-color", "HEAD", "--"],
                capture_output=True, timeout=20, check=True, env=git_environment).stdout
            tracked_raw = subprocess.run(
                ["git", "-C", str(root), "diff", "--name-only", "--no-ext-diff",
                 "--no-textconv", "-z", "HEAD", "--"],
                capture_output=True, timeout=20, check=True, env=git_environment).stdout
            tracked = [item.decode("utf-8", "surrogateescape")
                       for item in tracked_raw.split(b"\0") if item]
            untracked_raw = subprocess.run(
                ["git", "-C", str(root), "ls-files", "--others", "--exclude-standard", "-z"],
                capture_output=True, timeout=20, check=True, env=git_environment).stdout
            untracked = [item.decode("utf-8", "surrogateescape")
                         for item in untracked_raw.split(b"\0") if item]
            digest = hashlib.sha256(b"tracked-diff\0" + diff)
            for relative in sorted(untracked):
                path = root / relative
                digest.update(b"\0untracked\0" + relative.encode("utf-8", "surrogateescape") + b"\0")
                digest.update(os.readlink(path).encode() if path.is_symlink() else path.read_bytes())
            state["working_tree_sha256"] = digest.hexdigest()
            state["changed_paths"] = sorted(set(tracked + untracked))
        except (OSError, subprocess.SubprocessError):
            state["working_tree_sha256"] = "unavailable"
    return state


def kb_selection_text(kb_root, reason) -> str:
    """One traceable notebook line describing the selected checkout."""
    root = Path(kb_root).expanduser().resolve()
    state = kb_git_state(root)
    revision = (f"git {state['commit']} ({state['date']})"
                if state["commit"] else "git version unknown")
    working = ("working-tree status unknown" if state["uncommitted"] is None else
               (f"with uncommitted changes (SHA-256 {state.get('working_tree_sha256')}; "
                f"paths: {', '.join(state.get('changed_paths') or [])})")
               if state["uncommitted"] else "clean working tree")
    origin_basis = ("verified origin/main" if state.get("latest_verified") is True
                    else "last-fetched origin/main")
    publication = (f"; HEAD is not contained in {origin_basis}"
                   if state.get("commit_on_origin_main") is False else "")
    latest = ("latest origin/main verified"
              if state.get("latest_verified") is True else
              f"latest not verified ({state.get('latest_status')})")
    return f"Knowledge base: {root} ({reason}); {revision}; {working}{publication}; {latest}."
