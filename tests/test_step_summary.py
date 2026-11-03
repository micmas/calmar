import json
from pathlib import Path

from bs4 import BeautifulSoup

from calmar.step_summary import _metric_lines, mask_inventory_html, step_html


def _entry(subject, path, log, *, command="run tool"):
    return {
        "subject": subject,
        "session": "ses-1",
        "outputs": [{"path": path, "status": "cached", "commands": [command]}],
        "log_folder": log,
        "qc": {"metrics": {}},
    }


def test_multi_participant_provenance_has_one_collapsed_parent(tmp_path):
    entries = [
        _entry("sub-a", "/outputs/a.nii.gz", "/logs/a", command="tool a"),
        _entry("sub-b", "/outputs/b.nii.gz", "/logs/b", command="tool b"),
    ]
    html = step_html({"stage": "acquisition", "results": entries})
    soup = BeautifulSoup(html, "html.parser")
    parent = soup.select_one("details.step-provenance")
    assert parent is not None and not parent.has_attr("open")
    assert parent.summary.get_text(" ", strip=True) == "Commands, output files and logs (2 participants)"
    assert [item.summary.get_text(" ", strip=True)
            for item in parent.find_all("details", recursive=False)] == ["sub-a ses-1", "sub-b ses-1"]
    for value in ("tool a", "tool b", "/outputs/a.nii.gz", "/outputs/b.nii.gz", "/logs/a", "/logs/b"):
        assert value in html
    png = tmp_path / "qc.png"
    png.write_bytes(b"not-a-real-png-but-valid-for-embedding")
    entries[0]["qc"]["png"] = str(png)
    open_html = step_html({"stage": "acquisition", "results": entries}, images=True)
    open_soup = BeautifulSoup(open_html, "html.parser")
    assert open_soup.select_one("details.step-provenance").has_attr("open")
    assert all(item.has_attr("open") for item in open_soup.select("details.step-provenance > details"))
    assert open_soup.select_one("details.step-provenance > details > img") is not None


def test_single_participant_provenance_keeps_direct_summary(tmp_path):
    entry = _entry("sub-one", "/outputs/one.nii.gz", "/logs/one")
    html = step_html({"stage": "acquisition", "results": [entry]})
    soup = BeautifulSoup(html, "html.parser")
    assert soup.select_one("details.step-provenance") is None
    assert soup.find("details").summary.get_text(" ", strip=True) == \
        "sub-one ses-1 : commands, files and logs"
    png = tmp_path / "qc.png"
    png.write_bytes(b"image")
    entry["qc"]["png"] = str(png)
    image_soup = BeautifulSoup(
        step_html({"stage": "acquisition", "results": [entry]}, images=True), "html.parser")
    assert image_soup.find("details").has_attr("open")
    assert image_soup.select_one("details > img") is not None


def test_mask_inventory_groups_patterns_and_preserves_every_label():
    entries = [
        {"subject": "sub-a", "session": "ses-1", "pattern": "full"},
        {"subject": "sub-<b>", "session": "ses-2", "pattern": "full"},
        {"subject": "sub-c", "session": "ses-3", "pattern": "acute"},
        {"subject": "sub-d", "session": "ses-4", "pattern": "none"},
    ]

    class Study:
        @staticmethod
        def label(entry):
            return f"{entry['subject']} {entry['session']}"
        @staticmethod
        def masks(entry):
            if entry["pattern"] == "full":
                return {"manual": {"MNI": "m", "T1w": "t"}, "linda": {"MNI": "m", "T1w": "t"}}
            if entry["pattern"] == "acute":
                return {"openads": {"T1w": "d"}}
            return {}

    html = mask_inventory_html(Study(), entries)
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.select("details.mask-inventory table tr")[1:]
    assert len(rows) == 3
    text = soup.get_text(" ", strip=True)
    for label in ("sub-a ses-1", "sub-<b> ses-2", "sub-c ses-3", "sub-d ses-4"):
        assert label in text
    assert "none found locally" in text
    assert "sub-&lt;b&gt;" in html and "<b> ses-2" not in html
    assert "LINDA: T1w, MNI<br/>Manual: T1w, MNI" in str(soup)
    assert "Availability is not QC" in text

    one = mask_inventory_html(Study(), entries[:1])
    assert "1 availability pattern across 1 participant" in one


def test_dwi_availability_is_compact_but_complete():
    metrics = {
        "dwi_series_available": 4,
        "dwi_sessions_available": "ses-529, ses-602",
        "dwi_same_session": 2,
        "dwi_other_session": 2,
        "dwi_openads_ready": 1,
    }
    assert _metric_lines(metrics) == [(
        "DWI availability",
        "4 series (ses-529, ses-602); selected session: 2; other sessions: 2; "
        "OpenADS-ready: 1 (exact sibling ADC)",
    )]
    assert _metric_lines({key: ("none" if key == "dwi_sessions_available" else 0)
                          for key in metrics}) == [("DWI availability", "none found")]


def test_selection_and_acquisition_share_one_compact_cell():
    notebook = json.loads((Path(__file__).resolve().parents[1] /
                           "lesion-interpretation-pipeline.ipynb").read_text())
    assert len(notebook["cells"]) == 98
    assert notebook["cells"][18].get("id") == "calmar-acquire"
    matches = [cell for cell in notebook["cells"] if cell.get("id") == "calmar-acquire"]
    assert len(matches) == 1
    source = "".join(matches[0]["source"])
    assert "select_cohorts(CONFIG, RAW_DATASET_DIR, PROJECT_DIR)" in source
    assert "submit_step(\"acquisition\", SUBJECTS, study" in source
    assert "from calmar.step_summary import show_mask_inventory, show_step" in source
    assert "show_mask_inventory(study, SUBJECTS)" in source
    assert "Acquisition failed for selected entries:" in source
    assert "for s in SUBJECTS[:10]" not in source
    assert not any(cell.get("id") in {"calmar-step-18", "calmar-step-19"}
                   for cell in notebook["cells"])
    assert matches[0]["execution_count"] is None
    assert matches[0]["outputs"] == []
    participant_choice = next(cell for cell in notebook["cells"]
                              if cell.get("id") == "calmar-test-participant")
    assert participant_choice["execution_count"] is None

    explanation = notebook["cells"][17]
    assert explanation.get("id") == "calmar-acquire-md"
    assert "Select participants and fetch image content" in "".join(explanation["source"])


def test_guided_setup_runs_combined_selection_and_acquisition_once():
    root = Path(__file__).resolve().parents[1]
    guided = json.loads((root / "calmar-guided.ipynb").read_text())
    setup = "".join(guided["cells"][3]["source"])
    assert setup.count('"calmar-acquire"') == 1
    assert "calmar-step-19" not in setup
    mapping = json.loads((root / "calmar" / "workflow_cells.json").read_text())
    assert mapping["19"] == "calmar-acquire"
