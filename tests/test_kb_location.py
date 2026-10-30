from pathlib import Path
import subprocess

import pytest

from calmar.kb_location import (kb_git_state, kb_selection_text, resolve_kb_root,
                                update_kb_to_latest)
from calmar.kb_paths import add_kb_to_path, load_kb_modules


PINNED_KB = Path(__file__).resolve().parents[1] / "stroke-aphasia-kb"


def make_kb(root):
    (root / "scripts").mkdir(parents=True)
    (root / "scripts" / "aphasia_kb.py").write_text("# fixture\n")
    (root / "regions").mkdir()
    return root.resolve()


def test_override_wins_over_sibling_and_submodule(tmp_path):
    project = tmp_path / "calmar"
    override = make_kb(tmp_path / "override-kb")
    make_kb(tmp_path / "stroke-aphasia-kb")
    make_kb(project / "stroke-aphasia-kb")

    root, reason = resolve_kb_root(project, {"CALMAR_KB_ROOT": str(override)})

    assert root == override
    assert reason == "CALMAR_KB_ROOT override"


def test_sibling_wins_over_submodule(tmp_path):
    project = tmp_path / "calmar"
    sibling = make_kb(tmp_path / "stroke-aphasia-kb")
    make_kb(project / "stroke-aphasia-kb")

    assert resolve_kb_root(project, {}) == (sibling, "sibling working copy")


def test_submodule_is_the_portable_fallback(tmp_path):
    project = tmp_path / "calmar"
    submodule = make_kb(project / "stroke-aphasia-kb")

    assert resolve_kb_root(project, {}) == (submodule, "CALMaR submodule")


def test_missing_kb_lists_paths_tried(tmp_path):
    project = (tmp_path / "calmar").resolve()

    with pytest.raises(FileNotFoundError) as caught:
        resolve_kb_root(project, {})

    message = str(caught.value)
    assert str(project.parent / "stroke-aphasia-kb") in message
    assert str(project / "stroke-aphasia-kb") in message
    assert "scripts/aphasia_kb.py and regions/" in message


def test_invalid_override_is_strict(tmp_path):
    project = tmp_path / "calmar"
    make_kb(tmp_path / "stroke-aphasia-kb")
    invalid = tmp_path / "not-a-kb"
    invalid.mkdir()

    with pytest.raises(FileNotFoundError, match="CALMAR_KB_ROOT is set"):
        resolve_kb_root(project, {"CALMAR_KB_ROOT": str(invalid)})


def test_git_state_marks_uncommitted_drafts(tmp_path):
    root = make_kb(tmp_path / "stroke-aphasia-kb")
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "add", "."], check=True)
    subprocess.run(["git", "-C", str(root), "-c", "user.name=fixture",
                    "-c", "user.email=fixture@example.test", "commit", "-qm", "fixture"], check=True)
    clean = kb_git_state(root)
    assert clean["commit"] and clean["date"] and not clean["uncommitted"]

    (root / "drafts").mkdir()
    (root / "drafts" / "new.md").write_text("uncommitted draft\n")
    dirty = kb_git_state(root)
    assert dirty["uncommitted"] is True
    assert len(dirty["working_tree_sha256"]) == 64
    assert dirty["changed_paths"] == ["drafts/new.md"]


def test_git_state_does_not_claim_a_parent_repository(tmp_path):
    parent = tmp_path / "outer"
    parent.mkdir()
    subprocess.run(["git", "init", "-q", str(parent)], check=True)
    root = make_kb(parent / "copied-kb")

    assert kb_git_state(root) == {"commit": None, "date": None, "uncommitted": None}


def _commit(root, text):
    (root / "regions" / "version.txt").write_text(text)
    subprocess.run(["git", "-C", str(root), "add", "."], check=True)
    subprocess.run(["git", "-C", str(root), "-c", "user.name=fixture",
                    "-c", "user.email=fixture@example.test", "commit", "-qm", text], check=True)


def test_update_kb_fast_forwards_a_clean_checkout(tmp_path):
    source = make_kb(tmp_path / "source")
    subprocess.run(["git", "init", "-q", "-b", "main", str(source)], check=True)
    _commit(source, "first")
    bare = tmp_path / "remote.git"
    subprocess.run(["git", "clone", "-q", "--bare", str(source), str(bare)], check=True)
    checkout = tmp_path / "checkout"
    subprocess.run(["git", "clone", "-q", str(bare), str(checkout)], check=True)
    first = subprocess.run(["git", "-C", str(checkout), "rev-parse", "HEAD"],
                           capture_output=True, text=True, check=True).stdout.strip()
    subprocess.run(["git", "-C", str(source), "remote", "add", "origin", str(bare)], check=True)
    _commit(source, "second")
    subprocess.run(["git", "-C", str(source), "push", "-q", "origin", "main"], check=True)

    message = update_kb_to_latest(checkout, "sibling working copy", {})

    current = subprocess.run(["git", "-C", str(checkout), "rev-parse", "HEAD"],
                             capture_output=True, text=True, check=True).stdout.strip()
    assert current != first
    assert "updated to latest origin/main" in message
    state = kb_git_state(checkout)
    assert state["latest_verified"] is True
    assert state["verified_origin_main"] == current


def test_update_kb_refuses_to_overwrite_stale_drafts(tmp_path):
    source = make_kb(tmp_path / "source")
    subprocess.run(["git", "init", "-q", "-b", "main", str(source)], check=True)
    _commit(source, "first")
    bare = tmp_path / "remote.git"
    subprocess.run(["git", "clone", "-q", "--bare", str(source), str(bare)], check=True)
    checkout = tmp_path / "checkout"
    subprocess.run(["git", "clone", "-q", str(bare), str(checkout)], check=True)
    subprocess.run(["git", "-C", str(source), "remote", "add", "origin", str(bare)], check=True)
    _commit(source, "second")
    subprocess.run(["git", "-C", str(source), "push", "-q", "origin", "main"], check=True)
    (checkout / "drafts").mkdir()
    (checkout / "drafts" / "local.md").write_text("local draft\n")

    with pytest.raises(RuntimeError, match="behind origin/main.*uncommitted changes"):
        update_kb_to_latest(checkout, "sibling working copy", {})


def test_update_kb_can_be_explicitly_disabled(tmp_path):
    root = make_kb(tmp_path / "copied-kb")
    assert "disabled" in update_kb_to_latest(
        root, "CALMAR_KB_ROOT override", {"CALMAR_KB_UPDATE": "off"})


def test_update_kb_preserves_drafts_when_head_already_contains_latest_main(tmp_path):
    source = make_kb(tmp_path / "source")
    subprocess.run(["git", "init", "-q", "-b", "main", str(source)], check=True)
    _commit(source, "current")
    bare = tmp_path / "remote.git"
    subprocess.run(["git", "clone", "-q", "--bare", str(source), str(bare)], check=True)
    checkout = tmp_path / "checkout"
    subprocess.run(["git", "clone", "-q", str(bare), str(checkout)], check=True)
    (checkout / "drafts").mkdir()
    draft = checkout / "drafts" / "local.md"
    draft.write_text("keep this draft\n")

    message = update_kb_to_latest(checkout, "sibling working copy", {})

    assert "current with origin/main" in message
    assert draft.read_text() == "keep this draft\n"


def test_update_kb_reports_unverified_and_continues_when_fetch_fails(tmp_path):
    root = make_kb(tmp_path / "stroke-aphasia-kb")
    subprocess.run(["git", "init", "-q", "-b", "main", str(root)], check=True)
    _commit(root, "local")

    message = update_kb_to_latest(root, "sibling working copy", {})

    assert "WARNING: latest knowledge base not verified" in message
    assert subprocess.run(["git", "-C", str(root), "status", "--porcelain"],
                          capture_output=True, text=True, check=True).stdout == ""
    assert kb_git_state(root)["latest_verified"] is False
    assert "latest not verified" in kb_selection_text(root, "sibling working copy")


def test_submodule_update_detaches_at_latest_and_warns_about_release_pointer(tmp_path):
    source = make_kb(tmp_path / "source")
    subprocess.run(["git", "init", "-q", "-b", "main", str(source)], check=True)
    _commit(source, "first")
    bare = tmp_path / "remote.git"
    subprocess.run(["git", "clone", "-q", "--bare", str(source), str(bare)], check=True)
    checkout = tmp_path / "checkout"
    subprocess.run(["git", "clone", "-q", str(bare), str(checkout)], check=True)
    subprocess.run(["git", "-C", str(checkout), "checkout", "-q", "--detach"], check=True)
    subprocess.run(["git", "-C", str(source), "remote", "add", "origin", str(bare)], check=True)
    _commit(source, "second")
    subprocess.run(["git", "-C", str(source), "push", "-q", "origin", "main"], check=True)

    message = update_kb_to_latest(checkout, "CALMaR submodule", {})

    head = subprocess.run(["git", "-C", str(checkout), "rev-parse", "HEAD"],
                          capture_output=True, text=True, check=True).stdout.strip()
    latest = subprocess.run(["git", "-C", str(checkout), "rev-parse", "origin/main"],
                            capture_output=True, text=True, check=True).stdout.strip()
    branch = subprocess.run(["git", "-C", str(checkout), "branch", "--show-current"],
                            capture_output=True, text=True, check=True).stdout.strip()
    assert head == latest and branch == ""
    assert "submodule pointer" in message and "do not commit it unless" in message


def test_kb_modules_are_fresh_and_follow_the_selected_root(tmp_path):
    first = make_kb(tmp_path / "first-kb")
    second = make_kb(tmp_path / "second-kb")
    (first / "scripts" / "aphasia_kb.py").write_text("VALUE = 'first'\n")
    (second / "scripts" / "aphasia_kb.py").write_text("VALUE = 'second checkout'\n")

    try:
        module, = load_kb_modules(first, "aphasia_kb")
        assert module.VALUE == "first"
        (first / "scripts" / "aphasia_kb.py").write_text("VALUE = 'first, edited and uncommitted'\n")
        module, = load_kb_modules(first, "aphasia_kb")
        assert module.VALUE == "first, edited and uncommitted"
        module, = load_kb_modules(second, "aphasia_kb")
        assert module.VALUE == "second checkout"
    finally:
        add_kb_to_path(PINNED_KB)
