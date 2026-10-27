from pathlib import Path
import subprocess

import pytest

from calmar.kb_location import kb_git_state, resolve_kb_root
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

    assert resolve_kb_root(project, {}) == (submodule, "pinned CALMaR submodule")


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
    assert kb_git_state(root)["uncommitted"] is True


def test_git_state_does_not_claim_a_parent_repository(tmp_path):
    parent = tmp_path / "outer"
    parent.mkdir()
    subprocess.run(["git", "init", "-q", str(parent)], check=True)
    root = make_kb(parent / "copied-kb")

    assert kb_git_state(root) == {"commit": None, "date": None, "uncommitted": None}


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
