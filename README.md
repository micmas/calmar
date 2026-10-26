# CALMaR — Co-designed, Automated Lesion Mapping and Reporting

CALMaR is an open-source Jupyter notebook pipeline for stroke lesion
segmentation, quality control and clinician-facing interpretation of
structural brain MRI. It runs inside
[Neurodesktop](https://www.neurodesk.org/), which provides every
neuroimaging tool pre-installed.

Given a BIDS dataset, it will:

1. **Segment lesions** with an HD-BET brain mask and LINDA and/or SynthStroke (`SEGMENTATION_METHODS`); or OpenADS on DWI + ADC for acute stroke.
2. **QC every mask** in an interactive, stage-aware dashboard with an edit audit trail.
3. **Analyse regional overlap** against five atlases (HarvardOxford, AAL, Destrieux, Schaefer400, JHU).
4. **Compute disconnectomes** (BCBToolkit, DeepDisco) and optionally direct dMRI tractometry (QSIPrep / QSIRecon).
5. **Optionally measure background brain health** (SynthSeg volumetry, DeepWMH white-matter hyperintensities).
6. **Decode the lesion** against Neurosynth meta-analytic maps.
7. **Interpret it clinically** with the aphasia knowledge base: predicted impairments, outcome predictions and stage-aware therapy evidence, every claim cited.

All model steps run locally. The knowledge base's extraction and review
use a local model through Ollama; paper text and patient-derived lesion
data never leave the machine.

## Quick start

```bash
# In a Neurodesktop JupyterLab session, clone into storage that persists:
git clone --recurse-submodules https://github.com/micmas/calmar.git ~/neurodesktop-storage/calmar
cd ~/neurodesktop-storage/calmar
# File → Open → calmar-guided.ipynb, run the first cell, fill in the form, click Start workflow
```

Requirements: Neurodesktop (Play or local), a BIDS dataset (the default
fetches OpenNeuro `ds004884` through DataLad), the Python packages in
`requirements.txt` (the Setup cell installs what is missing), and a
FreeSurfer licence only for the optional QSIRecon route. Details and
troubleshooting: [docs/SETUP.md](docs/SETUP.md).

## Documentation

| | |
|---|---|
| [docs/SETUP.md](docs/SETUP.md) | installing, updating a checkout, the knowledge-base submodule, what Git tracks |
| [docs/NOTEBOOK_GUIDE.md](docs/NOTEBOOK_GUIDE.md) | using the notebooks: the form, stop points, QC dashboard, results preview, participant report |
| [docs/PIPELINE.md](docs/PIPELINE.md) | what each stage computes, the tools and the reasons behind the defaults |
| [docs/RUNNING_JOBS.md](docs/RUNNING_JOBS.md) | Slurm submission, caching and provenance, tests and validation |
| [docs/QC_RUBRIC.md](docs/QC_RUBRIC.md) | the stage-aware rating scale and issue tags used in QC |
| [docs/REPOSITORY_LAYOUT.md](docs/REPOSITORY_LAYOUT.md) | what is where, the module map, layout history |
| [docs/CT_ROUTE.md](docs/CT_ROUTE.md), [docs/DOMAIN_SEVERITY_INPUT.md](docs/DOMAIN_SEVERITY_INPUT.md), [docs/SAMPLE_APPLICABILITY_FIELDS.md](docs/SAMPLE_APPLICABILITY_FIELDS.md) | design proposals not yet implemented |
| [CHANGELOG.md](CHANGELOG.md) | what changed |

## Repository layout

```
calmar-guided.ipynb                   form-based workflow
lesion-interpretation-pipeline.ipynb  the detailed notebook (canonical implementation)
lesion-segmentation-benchmark.ipynb   segmentation benchmark
calmar/                               Python package used by the notebooks
src/                                  Slurm entry points (analysis_NN_*.sh) and their Python/R
tests/                                pytest suite, no imaging jobs
docs/                                 documentation (index above)
container/                            in-container LINDA wrapper
stroke-aphasia-kb/                    git submodule: the aphasia knowledge base
*/astra.yaml                          scientific records of individual analyses (see below)
```

The six folders `alignment-repair/`, `brain-health-analysis/`,
`diffusion-tract-analysis/`, `segmentation-benchmark/`,
`workflow-acceptance/` and `workflow-validation/` are ASTRA records: the
inputs, decisions, outputs and findings of one analysis each, kept as
the scientific record and validated with `astra validate`. Runtime data
(`data/`, `atlases/`, `reports/`, `qc_edits/`, `logs/`) is created on
first use and never committed.

## The aphasia knowledge base

The interpretation stage draws on
[micmas/stroke-aphasia-kb](https://github.com/micmas/stroke-aphasia-kb),
a curated, source-traceable literature base in which each finding links
a brain region, predictor or therapy to an outcome with the verbatim
passages that support it. CALMaR pins it as the git submodule
`stroke-aphasia-kb/` and imports its modules from
`stroke-aphasia-kb/scripts/`. Entries are written, reviewed and
committed in that repository; CALMaR only records which commit it was
tested with.

```bash
git submodule update --init                       # existing checkout without the KB
git submodule update --remote stroke-aphasia-kb \
    && git add stroke-aphasia-kb && git commit -m "KB: track <commit>"   # move to the KB's latest main
python stroke-aphasia-kb/scripts/kb_status.py     # what is in it
```

## Tests

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q tests
```

## Citation

If you use CALMaR in your research, please cite it using
[`CITATION.cff`](CITATION.cff):

> Michele Masson-Trottier (2025). CALMaR: Co-designed, Automated Lesion
> Mapping and Reporting (v1.0.0). https://github.com/micmas/calmar

The detailed notebook's **Citation and Resources** section lists the
primary citations for each tool and the ARC and ISLES 2022 datasets.

## License

MIT — see [`LICENSE`](LICENSE).
