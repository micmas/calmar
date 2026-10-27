"""The participant report cell, run end-to-end on tiny fixtures (Slurm helpers mocked)."""
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import ipywidgets as w
import nibabel as nib
import numpy as np
import pandas as pd
import pytest
from IPython.display import HTML

from calmar.guided import source_cell
from calmar import participant_report as pr

KB_ROOT = Path(__file__).resolve().parents[1] / "stroke-aphasia-kb"


def _mask(path, box):
    data = np.zeros((10, 10, 10), dtype=np.uint8)
    data[box] = 1
    path.parent.mkdir(parents=True, exist_ok=True)
    nib.save(nib.Nifti1Image(data, np.diag([2., 2., 2., 1.])), path)
    return path


@pytest.fixture
def fixture(tmp_path):
    entry = dict(subject="sub-T1", session="ses-1", t1w="t1.nii.gz")
    linda, synth = tmp_path/"linda", tmp_path/"synth"
    masks = {"linda": _mask(linda/"Lesion_in_MNI.nii.gz", np.s_[2:6, 2:6, 2:6]),
             "synthstroke": _mask(synth/"SynthStroke_in_MNI.nii.gz", np.s_[2:6, 2:6, 3:7])}
    _mask(linda/"Subject_in_MNI.nii.gz", np.s_[:, :, :])
    study = SimpleNamespace(mni_sources=lambda e: list(masks), mni_mask=lambda e, s: masks[s],
                            linda_dir=lambda e: linda, template_dir=lambda e: linda, lesion_mni=lambda e: masks["linda"], qc_anchor=lambda e: masks["linda"], qc_dir=lambda e: linda,
                            dirs=lambda e: {"linda": linda, "synthstroke": synth, "hdbet": tmp_path/"hdbet",
                                            "template": linda, "registration": tmp_path/"registration"})
    dataset = tmp_path/"data"; dataset.mkdir()
    (dataset/"participants.tsv").write_text(
        "participant_id\tsex\tage_at_stroke\twab_days\twab_aq\twab_type\n"
        "sub-T1\tF\t60\t400\t55.2\tTranscorticalMotor\n")
    reports = tmp_path/"reports"; reports.mkdir()
    pd.DataFrame([dict(subject="sub-T1", session="ses-1", region="Inferior Frontal Gyrus, pars opercularis",
                       lesion_in_roi_percent=40., roi_coverage_percent=10., overlap_voxels=26,
                       total_lesion_voxels=64, left_overlap_voxels=26, right_overlap_voxels=0,
                       midline_overlap_voxels=0),
                  dict(subject="sub-T1", session="ses-1", region="Tiny ROI", lesion_in_roi_percent=1.,
                       roi_coverage_percent=1., overlap_voxels=1, total_lesion_voxels=64)]
                 ).to_csv(reports/"lesion_atlas_overlap_HarvardOxford_linda.csv", index=False)
    from calmar import qc as q
    record = q.QCRecord.load(masks["linda"]); record.set_stage("lesion", rating=3); record.reviewer = "rater"
    record.save()
    png = tmp_path/"overlay.png"; png.write_bytes(b"\x89PNG fixture")
    helpers = SimpleNamespace(fresh_viewer=Mock(return_value=w.HTML()), set_volumes=Mock())
    return SimpleNamespace(entry=entry, study=study, dataset=dataset, reports=reports, png=png,
                           helpers=helpers, masks=masks, root=tmp_path)


def _run_cells(f, **extra):
    ns = dict(SUBJECTS=[f.entry], TEST_SUBJECT_IDX=0, PROJECT_DIR=KB_ROOT.parent, CONFIG={"LESION_THRESHOLD": .5},
              study=f.study, REPORTS_DIR=f.reports, RAW_DATASET_DIR=f.dataset, ATLAS_DIR=f.root,
              cw=f.helpers, display=Mock(), HTML=HTML)
    exec("".join(source_cell(77)["source"]), ns)
    ns.update(INTERP_MASK_SOURCE="linda", INTERP_KB_ATLASES=["HarvardOxford"], **extra)
    with patch("calmar.atlas_overlap.prepare_report_overlap") as prepare, \
            patch("calmar.reporting.run_reporting_task", return_value=str(f.png)) as overlay:
        exec("".join(source_cell(81)["source"]), ns)
    return ns, prepare, overlay


def test_report_cell_saves_report_with_provenance_and_rules(fixture):
    ns, prepare, overlay = _run_cells(fixture)
    report = ns["PARTICIPANT_REPORT"]
    assert prepare.call_args.args[0]["INTERP_KB_ATLASES"] == ["HarvardOxford"]
    assert overlay.call_args.args[1] == "report_overlay"
    html = report.path.read_text()
    assert report.path.name == "interpretation_sub-T1_ses-1_linda.html"
    assert ns["_rpt_path"] == report.path and ns["_calmar_generated_report_selection"] == ("sub-T1", "ses-1", "linda")
    # Provenance block: research use, mask + QC rating, how the mask was made, template caveat.
    assert "Research use only" in html and "not a diagnosis" in html
    assert "Lesion_in_MNI.nii.gz" in html and "<b>poor</b>" in html and "rater" in html
    assert "Rated poor" in html
    assert "How this lesion mask was made" in html and "Segmented by LINDA" in html
    assert "LINDA vs SynthStroke" not in html                  # agreement is shown before, in the form
    assert "MNI152" in html
    assert "<b>Knowledge base:</b> version " in html and "papers ·" in html and "extracted findings" in html
    # Damaged regions use the min-overlap threshold (5 %): the 1 % ROI is not shown.
    assert "pars opercularis" in html and "Tiny ROI" not in html
    assert html.index("Behavioural / clinical data") < html.index("Damaged regions")
    assert html.count("class='report-section'") == 6 and html.count(" open><summary") == 3
    # Non-lesion predictors come before lesion location (pessimist review, 2026-10-26)
    assert html.index("This participant’s measures: what the evidence says") < \
        html.index("Lesion location: what the evidence says")
    # The WAB type label is hidden; its Kertesz profile seeds the three domains.
    assert "TranscorticalMotor" not in html and "WAB type</b>" not in html
    assert "WAB/WAB-R profile" in html and "− impaired → mild profile floor" in html
    assert "Speech fluency" in html and "Mild" in html
    assert "TranscorticalMotor" not in "\n".join(report.messages)
    assert "Chronic (&gt;6 mo)" in html or "Chronic (>6 mo)" in html
    titles = [section.get_title(0) for section in report.panel.section_accordions]
    assert titles[0] == "Provenance and caveats" and "Generation details" in titles
    # The settings cell displays the rule tables.
    shown = "".join(c.args[0].data for c in ns["display"].call_args_list if hasattr(c.args[0], "data"))
    assert "Transcortical motor" in shown and "Bernhardt" in shown
    report.panel.widget.close()


def test_report_rejects_unavailable_mask_and_missing_selection(fixture):
    with pytest.raises(ValueError, match="No existing MNI mask"):
        pr.generate_participant_report(fixture.entry, "manual", pr.ReportSettings(), study=fixture.study,
                                       namespace={}, reports_dir=fixture.reports, dataset_dir=fixture.dataset,
                                       atlas_dir=fixture.root, kb_root=KB_ROOT, helpers=fixture.helpers)
    with pytest.raises(ValueError, match="Choose a participant"):
        pr.selected_entry([fixture.entry], 3)


def test_mask_agreement_resamples_and_reports_dice(tmp_path):
    a = _mask(tmp_path/"a.nii.gz", np.s_[2:6, 2:6, 2:6])
    b = _mask(tmp_path/"b.nii.gz", np.s_[2:6, 2:6, 2:6])
    img = nib.load(b); nib.save(nib.Nifti1Image(np.asanyarray(img.dataobj), np.diag([2., 2., 2., 1.]) @ np.eye(4)), b)
    volumes, pairs = pr.mask_agreement({"linda": a, "manual": b})
    assert pairs == [("linda", "manual", 1.0)]
    assert volumes["linda"] == pytest.approx(64 * 8 / 1000)


def test_kb_root_without_entries_is_an_error(tmp_path):
    pr._kb_modules(KB_ROOT)  # modules come from the real KB; the entries root is empty
    with pytest.raises(FileNotFoundError):
        pr.load_kb(tmp_path, pr.ReportSettings())


def test_kb_version_counts_what_the_report_used(tmp_path):
    import pandas as pd
    from types import SimpleNamespace
    kb = SimpleNamespace(include=("approved",), regions=[1, 2], impairments=[1], therapies=[], predictors=[1],
                         findings=pd.DataFrame({"citation": ["@A", "@A", "@B", None],
                                                "review_kind": ["human", "legacy", "legacy", "human"]}))
    version = pr.kb_version(tmp_path, kb)                    # not a git checkout
    assert (version["commit"], version["papers"], version["findings"], version["findings_reviewed"]) == (None, 2, 4, 2)
    assert pr.kb_version_text(version) == (
        "version unknown (not under git version control) · 2 papers · 4 extracted findings "
        "(2 approved by a named reviewer) in 4 entries (2 regions, 1 impairments, 0 therapies, 1 predictors) · "
        "statuses used: approved")
    version = pr.kb_version(KB_ROOT, kb)                      # the repository's KB is in git
    assert version["commit"] and version["date"]


def test_evidence_levels_choose_the_kb_statuses():
    assert pr.ReportSettings(evidence="approved").include == ("approved",)
    assert pr.ReportSettings(evidence="in_review").include == ("approved", "in_review")
    assert pr.ReportSettings(evidence="all").include == ("approved", "in_review", "draft")
    assert pr.ReportSettings(include_drafts=False).include == ("approved",)       # older setting still works
    with pytest.raises(ValueError):
        pr.ReportSettings(evidence="everything").include


def test_domain_levels_are_explicit_and_not_inferred():
    levels = pr.normalise_domain_levels({"naming": "moderate", "attention": "none"})
    assert levels["naming"] == "moderate" and levels["attention"] == "none"
    assert levels["reading"] == "not_assessed"
    html = pr.domain_levels_html(levels)
    assert "Naming / word finding" in html and "Moderate" in html
    assert "Attention" in html and "None observed" in html
    assert "Reading" in html and "Not assessed" in html
    assert "not inferred from WAB-AQ" in html
    with pytest.raises(ValueError, match="Unknown impairment domains"):
        pr.normalise_domain_levels({"made_up": "mild"})
    with pytest.raises(ValueError, match="Invalid level"):
        pr.normalise_domain_levels({"naming": "profound"})


def test_wab_type_profile_seeds_only_its_three_axes():
    _, rules = pr._kb_modules(KB_ROOT)
    levels, sources = pr.wab_profile_domain_levels(rules, "Broca")
    assert levels["fluency"] == "mild"
    assert levels["comprehension"] == "not_assessed"
    assert levels["repetition"] == "mild"
    assert levels["naming"] == "not_assessed"
    assert sources == {"fluency": "wab_profile_impaired",
                       "comprehension": "wab_profile_preserved",
                       "repetition": "wab_profile_impaired"}
    html = pr.domain_levels_html(levels, sources)
    assert "− impaired → mild profile floor" in html
    assert "+ relatively preserved → severity not assigned" in html
    missing, missing_sources = pr.wab_profile_domain_levels(rules, None)
    assert set(missing.values()) == {"not_assessed"} and missing_sources == {}

    global_levels, _ = pr.wab_profile_domain_levels(rules, "Global")
    assert {global_levels[key] for key in ("fluency", "comprehension", "repetition")} == {"mild"}


def test_standalone_report_is_responsive_accessible_and_prints_disclosures():
    html = pr.standalone_html("Fixture", "<details><summary>Evidence</summary><p>Claim</p></details>")
    assert '<meta name="viewport"' in html
    assert "font-size:17px" in html and "line-height:1.55" in html
    assert "--calmar-grape:#52489c" in html and "--calmar-blue:#4062bb" in html
    assert "summary:focus-visible" in html
    assert "document.querySelectorAll('details[data-print-open]')" in html
    assert ".print-only{display:none}" in html and ".print-only{display:block}" in html
    assert "@media screen and (max-width:700px)" in html and "overflow-wrap:break-word" in html
    assert 'font-family:"DejaVu Sans",Arial,Helvetica,sans-serif' in html
    assert "if(target.tagName==='DETAILS') target.open=true" in html
    assert "target.parentElement.closest('details')" in html
    assert ".calmar-report details[data-print-open]>*:not(summary){display:block!important}" in html
    assert ".calmar-report details:not([data-print-open]){display:none!important}" in html
    assert "window.addEventListener('beforeprint'" in html and "item.open=true" in html
    assert "window.addEventListener('afterprint'" in html and "item.open=calmarPrintState[index]" in html
    style = html.split("<style>", 1)[1].split("</style>", 1)[0]
    assert "\nbody{" not in style and "\nhtml{" not in style and "\nh1," not in style
    assert '<body class="calmar-report">' in html


def test_therapy_stage_mismatch_is_keyboard_and_print_readable():
    kb = SimpleNamespace(label_for=lambda value: value.replace("_", " "))
    therapies = pd.DataFrame([dict(
        therapy_id="fixture", therapy_name="Fixture therapy", behavioral_matched=["naming"], lesion_matched=[],
        short_description="Fixture description", rtss_summary=[], citations=["@Fixture"],
    )])
    html = pr.therapy_table(kb, therapies, "chronic", "Chronic (>6 mo)", {"fixture": {"acute"}})
    assert "<details class='stage-warning'><summary>Stage mismatch</summary>" in html
    assert "current patient is Chronic (&gt;6 mo)" in html
    assert "print-only stage-warning-print" in html
