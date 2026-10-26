"""The curated atlas -> knowledge-base mapping (stroke-aphasia-kb/atlas_mapping/)."""
from pathlib import Path

import pandas as pd
import pytest

KB_ROOT = Path(__file__).resolve().parents[1] / "stroke-aphasia-kb"
from calmar.kb_paths import add_kb_to_path  # noqa: E402
add_kb_to_path(KB_ROOT)
import atlas_mapping  # noqa: E402
from aphasia_kb import KnowledgeBase  # noqa: E402


def test_mapping_files_are_consistent():
    assert atlas_mapping.problems() == []


def test_every_location_finding_is_mapped_or_explained():
    """A new paper naming a new region must be added to kb_regions.yaml
    (mapped, or under `unmapped` with the reason): nothing is dropped silently."""
    kb = KnowledgeBase(KB_ROOT, include=("approved", "in_review", "draft"))
    found = atlas_mapping.coverage(kb.findings)
    assert found["missing"] == {}, f"Add these regions to stroke-aphasia-kb/atlas_mapping/kb_regions.yaml: {found['missing']}"
    assert found["mapped"] >= 0.9 * found["findings"]


def test_generated_table_is_up_to_date():
    assert (atlas_mapping.DIR / "MAPPING.md").read_text() == atlas_mapping.markdown_table(), \
        "Run: python stroke-aphasia-kb/scripts/atlas_mapping.py --write-table"


def overlap_rows(atlas, rows, total=1000):
    df = pd.DataFrame(rows)
    df["total_lesion_voxels"] = total
    df["atlas"] = atlas
    return df


def test_side_comes_from_the_voxels_for_bilateral_labels_and_from_the_label_otherwise():
    ho = overlap_rows("HarvardOxford", [dict(
        region="Precentral Gyrus", overlap_voxels=100, total_region_voxels=2000,
        left_overlap_voxels=20, right_overlap_voxels=80, left_region_voxels=1000, right_region_voxels=1000)])
    jhu = overlap_rows("JHU", [dict(region="Superior longitudinal fasciculus L", overlap_voxels=50,
                                    total_region_voxels=100, left_overlap_voxels=50, right_overlap_voxels=0)])
    units = atlas_mapping.unit_damage({"HarvardOxford": ho, "JHU": jhu}).set_index(["unit", "side"])
    assert units.loc[("precentral_gyrus", "right"), "lesion_pct"] == 8.0          # 80 of 1000 lesion voxels
    assert units.loc[("precentral_gyrus", "right"), "region_pct"] == 8.0          # 80 of the right gyrus' 1000
    assert units.loc[("precentral_gyrus", "left"), "lesion_pct"] == 2.0
    assert units.loc[("slf", "left"), "region_pct"] == 50.0 and units.loc[("slf", "right"), "overlap_voxels"] == 0
    assert not units.loc[("putamen", "left"), "measured"]                         # no AAL table given
    regions = atlas_mapping.region_damage(units.reset_index()).set_index("region")
    # Right-hemisphere damage no longer counts as damage to the left precentral gyrus.
    assert regions.loc["left_precentral_gyrus", "lesion_pct"] == 2.0
    assert regions.loc["right_precentral_gyrus", "lesion_pct"] == 8.0


def test_older_tables_without_region_sizes_still_give_the_lesion_share():
    ho = overlap_rows("HarvardOxford", [dict(region="Angular Gyrus", overlap_voxels=60, total_region_voxels=900,
                                             left_overlap_voxels=60, right_overlap_voxels=0)])
    regions = atlas_mapping.region_damage(atlas_mapping.unit_damage({"HarvardOxford": ho})).set_index("region")
    assert regions.loc["left_angular_gyrus", "lesion_pct"] == 6.0
    assert pd.isna(regions.loc["left_angular_gyrus", "region_pct"])


def test_findings_match_by_exact_region_name_and_thin_tracts_count_by_destroyed_share():
    kb = KnowledgeBase(KB_ROOT, include=("approved", "in_review", "draft"))
    damage = pd.DataFrame([
        dict(region="left_precentral_gyrus", side="left", lesion_pct=30.0, region_pct=40.0),
        dict(region="left_superior_longitudinal_fasciculus", side="left", lesion_pct=1.0, region_pct=95.0),
        dict(region="left_angular_gyrus", side="left", lesion_pct=1.0, region_pct=2.0)])
    rows = kb.location_findings(damage, min_overlap=5, min_region=10)
    assert set(rows["region"]) <= {"left_precentral_gyrus", "left_superior_longitudinal_fasciculus"}
    assert "left_superior_longitudinal_fasciculus" in set(rows["region"])     # 1 % of lesion, 95 % destroyed
    assert "left_angular_gyrus" not in set(rows["region"])                    # below both thresholds
    assert {"claim", "direction", "citation", "predicts", "population", "phase"} <= set(rows.columns)
    assert not kb.location_findings(damage, min_overlap=5, min_region=100)["region"].str.contains(
        "longitudinal").any()


@pytest.mark.parametrize("rid", ["left_long_segment_arcuate_fasciculus", "left_precentral_gyrus_insula", "left_extreme_capsule"])
def test_flagged_decisions_are_documented(rid):
    _, regions, unmapped = atlas_mapping.load()
    assert (rid in unmapped) or (regions[rid].get("review") and regions[rid]["basis"])


def test_evidence_gaps_name_known_areas_and_papers():
    gaps = atlas_mapping.load_gaps()
    assert {"thalamus_basal_ganglia", "right_hemisphere"} <= set(gaps) and "arcuate_and_long_tracts" not in set(gaps)
    status = atlas_mapping.citation_status()
    for gap in gaps.values():
        for paper in gap.get("papers") or []:
            assert status[paper] in ("seed", "extracted", "cited", "re-extracted-as-review"), paper
    kb = KnowledgeBase(KB_ROOT, include=("approved", "in_review", "draft"))
    text = atlas_mapping.gaps_markdown(kb.findings)
    assert "@Han2013 [seed]" in text and "`left_extreme_capsule` (" in text


def test_arcuate_comes_from_xtract_and_atlases_are_not_double_counted():
    _, regions, unmapped = atlas_mapping.load()
    assert regions["left_arcuate_fasciculus"]["units"] == ["arcuate_fasciculus"]
    assert not regions["left_arcuate_fasciculus"].get("review")
    assert {"left_frontal_aslant_tract", "left_optic_radiations"} <= set(regions) and "left_extreme_capsule" in unmapped
    xtract = overlap_rows("XTRACT", [dict(region="Arcuate Fasciculus L", overlap_voxels=100, total_region_voxels=200,
                                          left_overlap_voxels=100, right_overlap_voxels=0)])
    jhu = overlap_rows("JHU", [dict(region="Superior longitudinal fasciculus L", overlap_voxels=80,
                                    total_region_voxels=100, left_overlap_voxels=80, right_overlap_voxels=0)])
    damage = atlas_mapping.region_damage(atlas_mapping.unit_damage({"XTRACT": xtract, "JHU": jhu})).set_index("region")
    combined = damage.loc["left_arcuate_fasciculus_slf"]          # XTRACT arcuate + JHU SLF overlap
    assert combined["lesion_pct"] == 8.0 and combined["region_pct"] == 80.0   # the larger, not 18 % summed


def test_every_mapped_label_has_voxels_in_its_atlas_image():
    """JHU's 50 %-threshold image has no uncinate, cingulum or temporal SLF:
    atlas_labels.json lists only labels present in the images."""
    labels = atlas_mapping.atlas_labels()
    assert "Uncinate fasciculus L" not in labels["JHU"]
    units, _, _ = atlas_mapping.load()
    assert units["uncinate_fasciculus"]["atlas"] == "XTRACT"


def test_tract_disconnection_from_a_map(tmp_path):
    import nibabel as nib
    import numpy as np
    affine = np.diag([-1.0, 1.0, 1.0, 1.0]); affine[:3, 3] = [5, -5, -5]      # x > 0 for i < 5
    atlas = np.zeros((10, 10, 10), dtype=np.uint8)
    atlas[6:9, 2:8, 2:8] = 2                                                    # "Arcuate Fasciculus L" (x < 0)
    atlas[1:4, 2:8, 2:8] = 3                                                    # "Arcuate Fasciculus R"
    prob = np.zeros((10, 10, 10), dtype=np.float32)
    prob[6:9, 2:8, 2:5] = 0.9                                                   # half of the left arcuate
    nib.save(nib.Nifti1Image(atlas, affine), tmp_path / "x.nii.gz")
    nib.save(nib.Nifti1Image(prob, affine), tmp_path / "map.nii.gz")
    units = atlas_mapping.tract_disconnection(
        tmp_path / "map.nii.gz", {"XTRACT": (tmp_path / "x.nii.gz", {2: "Arcuate Fasciculus L", 3: "Arcuate Fasciculus R"})})
    arcuate = units[units.unit == "arcuate_fasciculus"].set_index("side")
    assert arcuate.loc["left", "disconnected_pct"] == 50.0 and arcuate.loc["right", "disconnected_pct"] == 0.0
    assert not units[units.atlas == "JHU"]["measured"].any()                    # JHU not given
    regions = atlas_mapping.region_disconnection(units).set_index("region")
    assert regions.loc["left_arcuate_fasciculus", "region_pct"] == 50.0
    assert regions.loc["left_arcuate_fasciculus", "lesion_pct"] == 0.0
