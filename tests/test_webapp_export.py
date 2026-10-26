"""The knowledge-base export for the CALMaR webapp (stroke-aphasia-kb/export_webapp.py)."""
import json
from pathlib import Path

import yaml

KB_ROOT = Path(__file__).resolve().parents[1] / "stroke-aphasia-kb"
from calmar.kb_paths import add_kb_to_path  # noqa: E402
add_kb_to_path(KB_ROOT)
import atlas_mapping  # noqa: E402
import export_webapp  # noqa: E402


def test_disconnectome_mapping_is_consistent():
    disco = yaml.safe_load((atlas_mapping.DIR / "disconnectome.yaml").read_text())
    units, regions, unmapped = atlas_mapping.load()
    for uid in disco["units"]:
        assert uid in units and units[uid]["kind"] == "tract", uid
    for uid, unit in disco["extra_units"].items():
        assert uid not in units, uid
        assert {"name", "kind", "labels", "basis"} <= set(unit)
    for rid, region in disco["extra_regions"].items():
        assert rid not in regions and rid in unmapped, rid
        assert all(u in disco["extra_units"] for u in region["units"])
    tract_units = {u for u, unit in units.items() if unit["kind"] == "tract"}
    assert tract_units <= set(disco["units"]), tract_units - set(disco["units"])


def test_export_is_json_and_complete(tmp_path):
    data = export_webapp.export(KB_ROOT, ("approved",))
    text = json.dumps(data, ensure_ascii=False)
    assert "NaN" not in text
    assert data["schemaVersion"] == 1
    assert data["findings"] and data["entries"] and data["citations"]
    finding = data["findings"][0]
    assert {"source_id", "source_kind", "target", "target_kind", "direction", "citation", "stages"} <= set(finding)
    assert set(data["mapping"]) == {"units", "regions", "unmapped", "atlasLabels", "disconnectome"}
    assert data["rules"]["strengthWeight"] == {"weak": 1.0, "moderate": 2.0, "strong": 3.0}
    for entry in data["entries"].values():
        assert entry["bucket"] in ("regions", "impairments", "therapies", "predictors", "ingredients")
    export_webapp.main(["--out", str(tmp_path / "kb.json"), "--fixtures", str(tmp_path)])
    fixtures = json.loads((tmp_path / "kb-parity.json").read_text())
    assert fixtures["cases"]["left_perisylvian"]["locationFindings"]
    assert fixtures["disconnectome"]["arcuate_cut"]["regionDisconnection"]


def test_fixture_region_shares_are_plausible():
    fixtures = export_webapp.fixtures(KB_ROOT, ("approved",))
    for case in fixtures["cases"].values():
        for row in case["regionDamage"]:
            assert row["region_pct"] is None or 0 <= row["region_pct"] <= 100, row
