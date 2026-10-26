from importlib.metadata import version
from pathlib import Path
import subprocess

import nibabel as nib
import numpy as np
import yaml

from calmar import synthetic


ROOT = Path(__file__).resolve().parents[1]
BENCHMARK_SCRIPTS = sorted((ROOT / "src").glob("analysis_0[0-9]_*.sh")) + sorted(
    (ROOT / "src").glob("analysis_1[0-2]_*.sh")
)


def _template(shape=(18, 18, 18)):
    grid = np.indices(shape).astype(float)
    radius = np.sqrt(sum((axis - (size - 1) / 2) ** 2
                         for axis, size in zip(grid, shape)))
    brain = radius < 7
    data = np.zeros(shape, dtype=np.float32)
    data[brain] = 0.35 + 0.5 * (1 - radius[brain] / 7)
    return nib.Nifti1Image(data, np.diag([2.0, 2.0, 2.0, 1.0])), brain


def test_edgecase_generator_writes_co_registered_acute_modalities(tmp_path):
    template, brain = _template()
    spec = dict(phase="acute", n=(1, 1), r=(2.5, 3.0), place="deep",
                contrast=1.0)

    result = synthetic._gen_one_edgecase(
        "sub-test", tmp_path, np.random.RandomState(4), template, brain, spec)

    mask_path = tmp_path / "derivatives/sub-test/sub-test_msk.nii.gz"
    mask = nib.load(mask_path).get_fdata() > 0
    assert result["lesion_voxels"] == int(mask.sum()) > 0
    for name, folder in (("T1w", "anat"), ("T2w", "anat"),
                         ("FLAIR", "anat"), ("dwi", "dwi"), ("adc", "dwi")):
        image = nib.load(tmp_path / f"sub-test/{folder}/sub-test_{name}.nii.gz")
        assert image.shape == template.shape
        np.testing.assert_allclose(image.affine, template.affine)

    dwi = nib.load(tmp_path / "sub-test/dwi/sub-test_dwi.nii.gz").get_fdata()
    adc = nib.load(tmp_path / "sub-test/dwi/sub-test_adc.nii.gz").get_fdata()
    background = brain & ~mask
    assert dwi[mask].mean() > dwi[background].mean()
    assert adc[mask].mean() < adc[background].mean()


def test_edgecase_catalog_includes_negative_and_mixed_chronology_controls():
    assert len(synthetic.EDGECASE_SPECS) == 12
    assert synthetic.EDGECASE_SPECS["acuneg"]["n"] == (0, 0)
    assert synthetic.EDGECASE_SPECS["chrneg"]["n"] == (0, 0)
    assert synthetic.EDGECASE_SPECS["acumixed"]["distractor"] is True
    assert {spec["phase"] for spec in synthetic.EDGECASE_SPECS.values()} == {
        "acute", "chronic"
    }


def test_periventricular_candidates_exclude_sulcal_and_cortical_csf():
    shape = (31, 31, 31)
    brain = np.zeros(shape, dtype=bool)
    brain[2:-2, 2:-2, 2:-2] = True
    tissue = np.zeros(shape, dtype=float)
    tissue[brain] = 0.6
    cortical_csf = brain.copy()
    cortical_csf[5:-5, 5:-5, 5:-5] = False
    ventricular_csf = np.zeros(shape, dtype=bool)
    ventricular_csf[13:18, 13:18, 13:18] = True
    csf = cortical_csf | ventricular_csf
    tissue[csf] = 0.1

    candidates = synthetic._edge_candidates("periv", brain, tissue, csf)

    assert len(candidates) > 0
    assert np.all(np.abs(candidates - np.array([15, 15, 15])).max(axis=1) <= 6)
    assert not csf[tuple(candidates.T)].any()


def test_benchmark_scripts_use_neurodesk_environment_and_provenance():
    assert len(BENCHMARK_SCRIPTS) == 13
    for script in BENCHMARK_SCRIPTS:
        text = script.read_text()
        assert "source /opt/neurodesktop/agent_bash_env.sh" in text, script.name
        assert "neurodesk-astra-provenance publish" in text, script.name
        subprocess.run(["bash", "-n", script], check=True)


def test_benchmark_astra_outputs_are_typed_and_recipes_name_software():
    spec = yaml.safe_load((ROOT / "analyses/segmentation-benchmark/astra.yaml").read_text())
    assert spec["version"] == version("astra-spec")
    for analysis in spec["analyses"].values():
        for output in analysis.get("outputs", []):
            assert output.get("format"), output["id"]
            recipe = output.get("recipe")
            if recipe:
                assert recipe.get("container"), output["id"]


def test_current_tool_profiles_have_separate_preprocessing_and_tool_provenance():
    spec = yaml.safe_load((ROOT / "analyses/segmentation-benchmark/astra.yaml").read_text())
    cross = spec["analyses"]["synthetic_crosstool"]
    outputs = {output["id"]: output for output in cross["outputs"]}
    assert outputs["synthstroke_masks"]["recipe"]["container"] == "synthstroke:0.0.0"
    assert outputs["linda_masks"]["recipe"]["container"] == "linda:0.5.1"
    assert outputs["edgecase_synthstroke_masks"]["recipe"]["container"] == "synthstroke:0.0.0"
    assert outputs["synthstroke_brain_masks"]["when"] == [
        "synthstroke_profile.calmar_current"
    ]
    assert outputs["edgecase_synthstroke_brain_masks"]["when"] == [
        "synthstroke_profile.calmar_current"
    ]

    synth = (ROOT / "src/analysis_04_synthetic_synthstroke.sh").read_text()
    linda = (ROOT / "src/analysis_05_synthetic_linda.sh").read_text()
    assert 'BRAIN_DIR="${WORK}/preproc-hdbet-${HDBET_MODE}"' in synth
    assert 'HDBET_DIR="${WORK}/preproc-hdbet-${HDBET_MODE}"' in linda
    assert "--output-id synthstroke_brain_masks" in synth
    assert "--output-id linda_brain_masks" in linda
    assert "unset ANTS_RANDOM_SEED CALMAR_R_SEED" in linda


def test_benchmark_analyses_consume_prepared_dataset_outputs():
    spec = yaml.safe_load((ROOT / "analyses/segmentation-benchmark/astra.yaml").read_text())
    isles = spec["analyses"]["isles2022_openads"]["inputs"]
    cross = spec["analyses"]["synthetic_crosstool"]["inputs"]
    assert isles == [{"id": "isles2022", "from": "../benchmark_inputs.isles2022_dataset"}]
    assert {item["from"] for item in cross} == {
        "../benchmark_inputs.synthetic_acute_dataset",
        "../benchmark_inputs.synthetic_chronic_dataset",
        "../benchmark_inputs.synthetic_edgecases_dataset",
    }
