from pathlib import Path

from bs4 import BeautifulSoup
from PIL import Image

from calmar.diffusion import tensor_metrics_paths, tractometry_paths
from calmar.dmri_visualization import dmri_visual_html
from calmar.study import Study


def _image(path, color=(25, 90, 150)):
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (120, 90), color).save(path)


def _root(dataset, entry):
    return (Path(dataset) / "derivatives/calmar-dmri" /
            entry["subject"] / entry["session"])


def test_qsirecon_panel_uses_one_selected_preview_and_links_full_reports(tmp_path):
    entry = {"subject": "sub-one", "session": "ses-dwi"}
    study = Study({"DMRI_METHOD": "qsirecon"}, tmp_path, tmp_path)
    root = _root(tmp_path, entry)
    (root / "qsiprep").mkdir(parents=True)
    (root / "qsiprep/sub-one.html").write_text("report")
    figures = root / "qsirecon/derivatives/qsirecon-test/sub-one/ses-dwi/figures"
    _image(figures / "sub-one_ses-dwi_desc-wmFOD_peaks.png")
    # A second plausible figure must not create a redundant notebook panel.
    _image(figures / "sub-one_ses-dwi_desc-GQIODF_peaks.png", (120, 20, 80))
    report = root / "qsirecon/derivatives/qsirecon-test/sub-one_ses-dwi.html"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("report")
    table, _ = tractometry_paths(tmp_path, study.config, entry)
    table.parent.mkdir(parents=True, exist_ok=True)
    table.write_text("tract\n")

    html, shown = dmri_visual_html([entry], study)
    soup = BeautifulSoup(html, "html.parser")
    assert shown == {(str(tmp_path.resolve()), "sub-one", "ses-dwi", "qsirecon")}
    assert len(soup.select("article img")) == 1
    assert soup.select_one("article img")["src"].startswith("data:image/jpeg;base64,")
    assert "Direction-coloured fibre-orientation peaks" in soup.get_text(" ", strip=True)
    assert "not streamline density" in soup.get_text(" ", strip=True)
    assert "QSIPrep report" in soup.get_text(" ", strip=True)
    assert "Full QSIRecon report" in soup.get_text(" ", strip=True)
    assert "Tractometry table" in soup.get_text(" ", strip=True)


def test_dipy_panel_reuses_the_existing_fa_md_qc_without_extra_views(tmp_path):
    entry = {"subject": "sub-two", "session": "ses-dwi"}
    study = Study({"DMRI_METHOD": "dipy_dti"}, tmp_path, tmp_path)
    table, _ = tensor_metrics_paths(tmp_path, study.config, entry)
    table.parent.mkdir(parents=True, exist_ok=True)
    table.write_text("metric\n")
    qc = table.with_name(table.name.replace("_metrics.tsv", "_qc.png"))
    _image(qc)

    html, shown = dmri_visual_html([entry], study, title="DIPY review")
    soup = BeautifulSoup(html, "html.parser")
    assert shown == {(str(tmp_path.resolve()), "sub-two", "ses-dwi", "dipy_dti")}
    assert len(soup.select("article img")) == 1
    text = soup.get_text(" ", strip=True)
    assert "DIPY diffusion tensor maps" in text
    assert "FA and MD on the preprocessed b0 image" in text
    assert "Full-size tensor QC" in text and "Tensor metrics" in text


def test_group_panel_is_bounded_and_collapses_remaining_participants(tmp_path):
    study = Study({"DMRI_METHOD": "dipy_dti"}, tmp_path, tmp_path)
    entries = []
    for index in range(3):
        entry = {"subject": f"sub-{index}", "session": "ses-dwi"}
        entries.append(entry)
        table, _ = tensor_metrics_paths(tmp_path, study.config, entry)
        _image(table.with_name(table.name.replace("_metrics.tsv", "_qc.png")))

    html, shown = dmri_visual_html(entries, study, max_inline=2)
    soup = BeautifulSoup(html, "html.parser")
    assert len(soup.select("article img")) == 2
    assert shown == {
        (str(tmp_path.resolve()), "sub-0", "ses-dwi", "dipy_dti"),
        (str(tmp_path.resolve()), "sub-1", "ses-dwi", "dipy_dti"),
    }
    assert "1 more participant — reports and metrics" in soup.get_text(" ", strip=True)
    assert "sub-2 ses-dwi" in soup.get_text(" ", strip=True)


def test_single_entry_group_panel_points_upward_instead_of_repeating_image(tmp_path):
    entry = {"subject": "sub-one", "session": "ses-dwi"}
    study = Study({"DMRI_METHOD": "dipy_dti"}, tmp_path, tmp_path)
    table, _ = tensor_metrics_paths(tmp_path, study.config, entry)
    _image(table.with_name(table.name.replace("_metrics.tsv", "_qc.png")))

    html, shown = dmri_visual_html(
        [entry], study, already_shown={
            (str(tmp_path.resolve()), "sub-one", "ses-dwi", "dipy_dti")})
    soup = BeautifulSoup(html, "html.parser")
    assert shown == set()
    assert not soup.select("img")
    assert "Already reviewed above: sub-one ses-dwi" in soup.get_text(" ", strip=True)


def test_method_switch_does_not_hide_a_new_preview(tmp_path):
    entry = {"subject": "sub-one", "session": "ses-dwi"}
    qsirecon = Study({"DMRI_METHOD": "qsirecon"}, tmp_path, tmp_path)
    dipy = Study({"DMRI_METHOD": "dipy_dti"}, tmp_path, tmp_path)
    table, _ = tensor_metrics_paths(tmp_path, dipy.config, entry)
    _image(table.with_name(table.name.replace("_metrics.tsv", "_qc.png")))
    prior = {(str(tmp_path.resolve()), "sub-one", "ses-dwi", "qsirecon")}

    html, shown = dmri_visual_html([entry], dipy, already_shown=prior)

    assert shown == {(str(tmp_path.resolve()), "sub-one", "ses-dwi", "dipy_dti")}
    assert BeautifulSoup(html, "html.parser").select("article img")
