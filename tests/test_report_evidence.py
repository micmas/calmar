"""Report sections that show each finding with its direction."""
import sys
import re
from pathlib import Path
from types import SimpleNamespace

import pandas as pd
from bs4 import BeautifulSoup

KB_ROOT = Path(__file__).resolve().parents[1] / "aphasia-kb"
sys.path.insert(0, str(KB_ROOT))
import aphasia_rules as rules  # noqa: E402
from aphasia_kb import KnowledgeBase  # noqa: E402
from calmar.participant_report import ReportSettings  # noqa: E402
from calmar.report_evidence import (_claims, _evidence_context, location_coverage, location_section,
                                    measures_section, wab_band)  # noqa: E402

KB = KnowledgeBase(KB_ROOT, include=("approved", "in_review", "draft"))


def test_location_section_shows_regions_damage_and_merges_kb_synonyms():
    damage = pd.DataFrame([
        dict(region="left_inferior_fronto_occipital_fasciculus", side="left", lesion_pct=0.1, region_pct=56.0, review=False),
        dict(region="left_inferior_frontal_occipital_fasciculus", side="left", lesion_pct=0.1, region_pct=56.0, review=False),
        dict(region="left_arcuate_fasciculus", side="left", lesion_pct=1.0, region_pct=90.0, review=True)])
    rows = KB.location_findings(damage, min_overlap=5, min_region=10)
    html = location_section(KB, rules, rows, damage, location_coverage(KB, rows, damage), ReportSettings())
    assert "56% of the region destroyed" in html and "90% of the region destroyed" in html
    assert html.count("Also recorded in the knowledge base as") == 1          # two spellings, one row
    assert "Atlas match includes a documented judgement call" in html
    assert ">association<" in html and "LIKELY" not in html
    assert "finding-claim" in html and "Evidence strength" in html and "Extraction confidence" in html
    assert "Source passages" in html and "Full citation for" in html
    assert "Project-specific display heuristic" in html and "&#9733;" in html
    assert "very strong / replicated" in html and "display-label" in html
    assert "visually-hidden" in html and "of 4 stars" in html
    assert "All implicated regions:" in html and "display-signal-print" in html
    assert rows["source_path"].str.len().gt(0).all()


def test_measures_section_states_direction_and_flags_late_severity_scores():
    html = measures_section(KB, {"severity_metric": {"instrument": "WAB-AQ", "value": 51.5}, "lesion_volume": 199.0},
                            days=3839)
    assert "WAB-AQ 51.5 (moderate" in html and "measured 3839 days after the stroke" in html
    assert "Lower values go with worse language or recovery" in html
    assert "Higher values go with worse language or recovery" in html            # lesion volume
    assert "distinct findings" in html
    assert "apply only loosely" in html
    assert "of these findings" in html and "distinct findings" in html
    # Findings about predicting the measure itself are not "what it implies".
    assert "A ResNet-18 CNN" not in html
    assert "LIKELY" not in html
    assert measures_section(KB, {"severity_metric": {"instrument": "WAB-AQ", "value": 51.5}}, days=30).count("loosely") == 0


def test_wab_bands():
    assert [wab_band(x) for x in (10, 40, 51.5, 80, 95)] == ["very severe", "severe", "moderate", "mild",
                                                            "within normal limits"]


def test_regions_resting_on_few_studies_are_marked():
    damage = pd.DataFrame([dict(region="left_insula", side="left", lesion_pct=0.1, region_pct=40.0, review=False)])
    rows = KB.location_findings(damage, min_overlap=5, min_region=10)
    html = location_section(KB, rules, rows, damage, location_coverage(KB, rows, damage), ReportSettings())
    assert "Limited citation base: 1 citation key" in html


def test_location_summary_keeps_association_null_mixed_and_inverse_counts_separate():
    damage = pd.DataFrame([
        dict(region="left_arcuate_fasciculus", side="left", lesion_pct=10.0, region_pct=50.0, review=False),
        dict(region="left_ifg_pars_opercularis", side="left", lesion_pct=8.0, region_pct=40.0, review=False),
    ])
    rows = pd.DataFrame([
        dict(region="left_arcuate_fasciculus", side="left", lesion_pct=10.0, region_pct=50.0,
             predicts="speech_repetition", predicts_kind="impairment", claim=f"Claim {i}", direction=direction,
             citation=f"@Study{i}", method=None, strength=None, evidence_quality=None, confidence=None,
             source_id="missing", finding_id=f"f{i}", contribution=contribution)
        for i, (direction, contribution) in enumerate([
            ("likely", 1.0), ("no_effect", 0.0), ("mixed", 0.0), ("unlikely", -0.5),
            ("not_yet_classified", 0.0),
        ])
    ])
    # An identical claim/citation attached to another damaged region is one
    # distinct finding, but both implicated regions must remain visible.
    rows = pd.concat([rows, rows.iloc[[0]].assign(region="left_ifg_pars_opercularis",
                                                   lesion_pct=8.0, region_pct=40.0)], ignore_index=True)
    html = location_section(KB, rules, rows, damage,
                            {"findings": 4, "undamaged": 0, "unmappable": 0}, ReportSettings())
    for label in ("Associations", "Inverse associations", "Null findings", "Mixed results"):
        assert f"<span><strong>{label}</strong> 1</span>" in html
    assert "<span><strong>Other / unclassified</strong> 1</span>" in html
    assert "5 distinct matched findings" in html
    assert "Left arcuate fasciculus" in html and "Left IFG Pars Opercularis" in html
    assert "Study method: Not reported" in html
    assert "<dd>Not reported</dd>" in html
    assert "findings may come from the same study or overlapping cohorts" in html


def test_location_section_excludes_aphasia_types_and_non_symptom_targets():
    damage = pd.DataFrame([
        dict(region="left_ifg_pars_opercularis", side="left", lesion_pct=8.0, region_pct=40.0, review=False),
    ])
    common = dict(region="left_ifg_pars_opercularis", side="left", lesion_pct=8.0, region_pct=40.0,
                  direction="likely", method="VLSM", strength="moderate", evidence_quality="observational",
                  confidence="high", source_id="missing", contribution=1.0)
    rows = pd.DataFrame([
        dict(**common, predicts="speech_fluency", predicts_kind="impairment", claim="Symptom claim",
             citation="@Symptom", finding_id="symptom"),
        dict(**common, predicts="brocas_aphasia", predicts_kind="impairment", claim="Syndrome claim",
             citation="@Syndrome", finding_id="syndrome"),
        dict(**common, predicts="aphasia", predicts_kind="impairment", claim="Diagnosis claim",
             citation="@Diagnosis", finding_id="diagnosis"),
        dict(**common, predicts="language_recovery", predicts_kind="prognosis", claim="Prognosis claim",
             citation="@Prognosis", finding_id="prognosis"),
    ])
    html = location_section(KB, rules, rows, damage,
                            {"findings": 3, "undamaged": 0, "unmappable": 0}, ReportSettings())
    assert "Speech fluency" in html and "Symptom claim" in html
    assert "Syndrome claim" not in html and "@Syndrome" not in html
    assert "Diagnosis claim" not in html and "@Diagnosis" not in html
    assert "Language recovery" not in html and "Prognosis claim" not in html
    assert "does not infer the presence or type of aphasia from a lesion" in html


def test_additional_symptom_summaries_are_collapsed_together():
    damage = pd.DataFrame([
        dict(region="left_ifg_pars_opercularis", side="left", lesion_pct=8.0, region_pct=40.0, review=False),
    ])
    rows = pd.DataFrame([
        dict(region="left_ifg_pars_opercularis", side="left", lesion_pct=8.0, region_pct=40.0,
             predicts=f"symptom_{i}", predicts_kind="impairment", claim=f"Claim {i}", direction="likely",
             citation=f"@Study{i}", method="VLSM", strength="moderate", evidence_quality="observational",
             confidence="high", source_id="missing", finding_id=f"f{i}", contribution=10 - i)
        for i in range(4)
    ])
    html = location_section(KB, rules, rows, damage,
                            {"findings": 4, "undamaged": 0, "unmappable": 0}, ReportSettings(top_n=2))
    soup = BeautifulSoup(html, "html.parser")
    extra = soup.select_one("details.additional-outcomes")
    assert extra is not None and not extra.has_attr("open")
    assert "Show 2 additional symptom summaries" in extra.summary.get_text(" ", strip=True)


def test_white_matter_provenance_is_collapsed_by_default():
    from calmar.report_evidence import disconnection_section
    html = disconnection_section(KB, pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), ReportSettings(),
                                 "BCBToolkit", map_name="Disconnectome_expert.nii.gz", mask_label="manual lesion")
    evidence_path = BeautifulSoup(html, "html.parser").select_one("details.evidence-path")
    assert evidence_path is not None and not evidence_path.has_attr("open")
    assert evidence_path.has_attr("data-print-open")
    assert evidence_path.summary.get_text(" ", strip=True) == "Where this evidence comes from"


def test_print_notes_when_additional_regions_are_only_in_interactive_html():
    damage = pd.DataFrame([
        dict(region=f"region_{i}", side="left", lesion_pct=10.0 - i, region_pct=40.0, review=False)
        for i in range(3)
    ])
    rows = pd.DataFrame([
        dict(region=f"region_{i}", region_name=f"Region {i}", side="left", lesion_pct=10.0 - i,
             region_pct=40.0, predicts="speech_repetition", predicts_kind="impairment", claim=f"Claim {i}",
             direction="likely", citation=f"@Study{i}", method=None, strength=None, evidence_quality=None,
             confidence=None, source_id="missing", finding_id=f"f{i}", contribution=1.0, review=False)
        for i in range(3)
    ])
    settings = ReportSettings(max_evidence_regions=1)
    html = location_section(KB, rules, rows, damage, {"findings": 3, "undamaged": 0, "unmappable": 0}, settings)
    assert "2 additional qualifying damaged regions are available in the interactive HTML report" in html


def test_finding_disclosures_use_source_file_identity_and_handle_nan(tmp_path):
    approved = dict(id="same_region", status="approved", _path=tmp_path / "approved.yaml", reviewer="Reviewer A",
                    findings=[dict(id="f1", claim="Approved claim <exact>", citation="@Approved",
                                   source_passages=[dict(quote="Approved passage")])])
    draft = dict(id="same_region", status="draft", _path=tmp_path / "draft.yaml",
                 findings=[dict(id="f1", claim="Draft claim", citation="@Draft",
                                source_passages=[dict(quote="Draft passage")])])
    flat = pd.DataFrame([
        dict(source_id="same_region", source_path=str(approved["_path"]), id="f1", source_status="approved",
             claim=approved["findings"][0]["claim"], citation="@Approved", direction="likely", method=pd.NA, design=pd.NA,
             strength=pd.NA, confidence=pd.NA, reviewer=pd.NA, review_kind="human", review_tier=pd.NA),
        dict(source_id="same_region", source_path=str(draft["_path"]), id="f1", source_status="draft",
             claim="Draft claim", citation="@Draft", direction="likely", method="LSM", strength="moderate", confidence="high",
             reviewer=pd.NA, review_kind="none", review_tier=pd.NA),
    ])
    kb = SimpleNamespace(root=tmp_path, regions=pd.DataFrame([approved, draft]), impairments=pd.DataFrame(),
                         therapies=pd.DataFrame(), predictors=pd.DataFrame(), findings=flat)
    rows = flat.rename(columns={"id": "finding_id"})
    html = _claims(kb, rows, context=_evidence_context(kb))
    articles = BeautifulSoup(html, "html.parser").select("article.finding")
    assert len(articles) == 2
    approved_text, draft_text = (article.get_text(" ", strip=True) for article in articles)
    assert "Approved passage" in approved_text and "Draft passage" not in approved_text
    assert "Entry status: approved" in approved_text and "Reviewer: Reviewer A" in approved_text
    assert approved_text.count("Not reported") == 3 and not re.search(r"\bnan\b", approved_text, re.I)
    assert "Draft passage" in draft_text and "Approved passage" not in draft_text
    assert "Entry status: draft" in draft_text
    assert "Approved claim &lt;exact&gt;" in html


def test_measure_caution_count_uses_the_same_distinct_findings_as_details(tmp_path):
    finding = dict(id="f1", target="language_recovery", target_kind="prognosis",
                   claim="Early severity predicts recovery.", direction="likely", citation="@Study",
                   method="behavioral", strength="moderate", confidence="high")
    source_path = str(tmp_path / "severity.yaml")
    flat = pd.DataFrame([{**finding, "source_id": "severity_metric", "source_kind": "predictor", "source_path": source_path,
                          "source_status": "approved"},
                         {**finding, "source_id": "severity_metric", "source_kind": "predictor", "source_path": source_path,
                          "source_status": "approved"}])
    predictor = dict(id="severity_metric", name="Aphasia severity", status="approved", _path=source_path,
                     direction_of_severity="lower_is_worse", findings=[finding])
    kb = SimpleNamespace(
        root=tmp_path, regions=pd.DataFrame(), impairments=pd.DataFrame(), therapies=pd.DataFrame(),
        predictors=pd.DataFrame([predictor]), findings=flat,
        resolve_aliases=lambda keys: {key: key for key in keys}, label_for=lambda key: key.replace("_", " ").title(),
    )
    html = measures_section(kb, {"severity_metric": {"instrument": "WAB-AQ", "value": 50}}, days=365)
    assert "1 distinct findings" in html and "Show 1 distinct finding" in html
    assert "1 of these findings concern severity measured early" in html


def test_each_finding_shows_its_study_phase_and_sections_summarise_it():
    damage = pd.DataFrame([dict(region="left_arcuate_fasciculus", side="left", lesion_pct=1.0, region_pct=90.0,
                                review=False)])
    rows = KB.location_findings(damage, min_overlap=5, min_region=10)
    html = location_section(KB, rules, rows, damage, location_coverage(KB, rows, damage), ReportSettings(),
                            phase="acute")
    soup = BeautifulSoup(html, "html.parser")
    phases = [dt.find_next_sibling("dd").get_text() for dt in soup.select(".finding-indicators dt")
              if dt.get_text() == "Study phase"]
    assert len(phases) == len(soup.select("article.finding")) > 0
    assert any("stage mismatch" in p for p in phases)             # chronic evidence for an acute participant
    assert soup.select_one(".phase-summary") and "This participant is in the <b>acute</b>" in html
    plain = location_section(KB, rules, rows, damage, location_coverage(KB, rows, damage), ReportSettings())
    assert "phase-summary" not in plain and "stage mismatch" not in plain
