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
| [docs/CHANGELOG.md](docs/CHANGELOG.md) | what changed |

## Repository layout

```
calmar-guided.ipynb                   form-based workflow
lesion-interpretation-pipeline.ipynb  the detailed notebook (canonical implementation)
lesion-segmentation-benchmark.ipynb   segmentation benchmark (a separate study, see below)
calmar/                               Python package used by the notebooks
src/                                  Slurm entry points (analysis_NN_*.sh) and their Python/R
tests/                                pytest suite, no imaging jobs
analyses/                             ASTRA scientific records, one folder per analysis
docs/                                 documentation (index above)
container/                            in-container LINDA wrapper
stroke-aphasia-kb/                    git submodule: the aphasia knowledge base
```

`analyses/` holds one folder per analysis (`alignment-repair`,
`brain-health-analysis`, `diffusion-tract-analysis`,
`segmentation-benchmark`, `workflow-acceptance`, `workflow-validation`),
each an ASTRA record of its inputs, decisions, outputs and findings,
validated with `astra validate`. The segmentation benchmark is a
separate study from the participant workflow: its notebook, the scripts
`src/analysis_00`–`12` and `calmar/synthetic.py` are never called by the
guided or detailed notebook. Runtime data (`data/`, `atlases/`,
`reports/`, `qc_edits/`, `logs/`) is created on first use and never
committed.

## The aphasia knowledge base

The interpretation stage draws on
[micmas/stroke-aphasia-kb](https://github.com/micmas/stroke-aphasia-kb),
a curated, source-traceable literature base in which each finding links
a brain region, predictor or therapy to an outcome with the verbatim
passages that support it. CALMaR records a tested KB release as the git
submodule `stroke-aphasia-kb/`, but the notebooks prefer a sibling
working copy at `../stroke-aphasia-kb/` when one is present. During
Setup, the selected checkout is fetched and fast-forwarded to the latest
`origin/main` before any KB module is imported. If the network is unavailable,
Setup continues with a prominent “latest not verified” warning. A checkout that already
contains current `main` may retain local commits or uncommitted drafts;
a stale dirty or divergent checkout stops with instructions rather than
mixing KB versions. Setup and every participant report identify the
selected root, its full commit and, for uncommitted content, a SHA-256
digest and changed-path inventory.

Selection order is `CALMAR_KB_ROOT`, the sibling working copy, then the
CALMaR submodule. Set the environment variable before starting
JupyterLab to force the submodule or another checkout:

```bash
CALMAR_KB_ROOT="$PWD/stroke-aphasia-kb" jupyter lab
CALMAR_KB_ROOT="$HOME/GITHUB/stroke-aphasia-kb" jupyter lab
```

Reports default to **All, including unreviewed drafts** during
development and label each finding's review status. Set
`CALMAR_KB_UPDATE=off` only for a deliberately pinned or offline run;
the exact revision remains recorded in the report. The submodule pointer
is also updated when CALMaR is released:

```bash
git submodule update --init
# .gitmodules declares main as the update --remote branch.
git submodule update --remote stroke-aphasia-kb
git add stroke-aphasia-kb
git commit -m "KB: track <commit>"
python stroke-aphasia-kb/scripts/kb_status.py
```

## Tests

```bash
python -m pip install -r requirements.txt
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
