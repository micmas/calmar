"""Report sections that show each finding with its direction."""
import sys
from pathlib import Path

import pandas as pd

KB_ROOT = Path(__file__).resolve().parents[1] / "aphasia-kb"
sys.path.insert(0, str(KB_ROOT))
import aphasia_rules as rules  # noqa: E402
from aphasia_kb import KnowledgeBase  # noqa: E402
from calmar.participant_report import ReportSettings  # noqa: E402
from calmar.report_evidence import location_coverage, location_section, measures_section, wab_band  # noqa: E402

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
    assert "⚑" in html                                                       # arcuate: judgement call
    assert ">association<" in html and "LIKELY" not in html


def test_measures_section_states_direction_and_flags_late_severity_scores():
    html = measures_section(KB, {"severity_metric": {"instrument": "WAB-AQ", "value": 51.5}, "lesion_volume": 199.0},
                            days=3839)
    assert "WAB-AQ 51.5 (moderate" in html and "measured 3839 days after the stroke" in html
    assert "Lower values go with worse language or recovery" in html
    assert "Higher values go with worse language or recovery" in html            # lesion volume
    assert "apply only loosely" in html
    # Findings about predicting the measure itself are not "what it implies".
    assert "A ResNet-18 CNN" not in html
    assert "LIKELY" not in html
    assert measures_section(KB, {"severity_metric": {"instrument": "WAB-AQ", "value": 51.5}}, days=30).count("loosely") == 0


def test_wab_bands():
    assert [wab_band(x) for x in (10, 40, 51.5, 80, 95)] == ["very severe", "severe", "moderate", "mild",
                                                            "within normal limits"]
