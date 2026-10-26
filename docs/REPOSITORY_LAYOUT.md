# Repository layout

Open the notebooks and submit jobs from the repository root. `calmar/`
is a regular Python package importable from this checkout; its
initialiser does not start processing or build UI.

```text
calmar-guided.ipynb                   form-based workflow (reuses the detailed notebook's cells)
lesion-interpretation-pipeline.ipynb  the detailed notebook and canonical implementation
lesion-segmentation-benchmark.ipynb   LINDA / SynthStroke / OpenADS benchmark (see below)

calmar/                               the Python package (module map below)
src/
  analysis_NN_*.sh                    retained Slurm entry points, numbered in pipeline order;
                                      00–12 belong to the segmentation benchmark
  python/  r/                         implementations those scripts call
  constraints-neurodesk.txt           version pins the two environment-restore scripts apply
tests/                                pytest suite (no imaging jobs); images/ holds a sample T1
container/                            in-container LINDA wrapper source and build notes
stroke-aphasia-kb/                    SUBMODULE: the aphasia knowledge base (github.com/micmas/stroke-aphasia-kb)

analyses/                             ASTRA scientific records, one folder per analysis
  alignment-repair/                   (astra.yaml, universes/, request fixtures): the inputs,
  brain-health-analysis/              decisions, outputs and findings, validated with
  diffusion-tract-analysis/           `astra validate`; their runtime products land beside
  segmentation-benchmark/             them and are git-ignored
  workflow-acceptance/
  workflow-validation/

docs/                                 SETUP, NOTEBOOK_GUIDE, PIPELINE, RUNNING_JOBS, QC_RUBRIC,
                                      CHANGELOG, design proposals, palette, validation evidence,
                                      issues/, images/
AGENTS.md                             operating contract for agents working in Neurodesk
CITATION.cff  LICENSE
requirements.txt  requirements-dev.txt
```

Runtime directories, created on first use and git-ignored: `data/`
(DataLad datasets), `atlases/` (nilearn cache and the ch2→MNI152
transforms), `reports/` (CSVs, group maps, HTML reports, `jobs/`),
`qc_edits/` (ITK-SNAP / FSLeyes round trip), `logs/`, `notes/`.

## Module map (`calmar/`)

| Area | Modules |
|---|---|
| Study and inputs | `study.py` (where every input and derivative lives), `acquisition.py`, `cohort.py`, `single_subject.py`, `masks.py`, `templates.py`, `methods.py` (the run's scientific choices as one table) |
| Processing (Slurm only) | `processing.py` (one `step_<name>` per step, atomic publication, cache identity), `scheduled.py` (`submit_step`, receipts, reuse), `job_progress.py`, `process_output.py`, `reporting.py` (atlas overlap, group maps, decoding), `dmri_pipeline.py`, `brain_health_pipeline.py`, `qc_operation.py` |
| Choices made in the notebook | `method_choice.py` (segmentation methods), `dwi_choice.py` (OpenADS on a found DWI), `dmri_choice.py` (directional dMRI), `brain_health_choice.py` |
| Route-specific logic | `brainmask.py`, `diffusion.py`, `brain_health.py`, `synthetic.py` (benchmark phantoms), `mask_method.py` |
| Notebook execution | `execution.py` (checkpoints), `guided.py`, `notebook_navigation.py`, `workflow_cells.json` (stable cell IDs), `timing.py` |
| QC | `qc.py` (ratings, edits, registration, tool dispatch; rubric in `docs/QC_RUBRIC.md`), `qc_panel.py`, `qc_decisions.py`, `qc_repair.py`, `step_qc.py`, `review.py` |
| Viewers and widgets | `step_viewer.py`, `step_summary.py`, `widgets.py`, `widget_lifecycle.py`, `viewer_transport.py`, `layer_controls.py`, `overlay.py`, `output.py`, `colors.py` |
| Results and atlases | `atlas_loader.py`, `atlas_overlap.py`, `anatomy_labels.py`, `atlas_ui.py`, `atlas_results.py`, `atlas_pdf.py`, `disconnectomes.py`, `disconnectome_compare.py` |
| Participant report | `participant_report.py`, `report_evidence.py`, `report_ui.py`, `kb_paths.py` (where the KB's modules are imported from) |

Each module starts with a docstring saying what it is for.

## Conventions

- The segmentation benchmark is a separate study that shares the
  package: `lesion-segmentation-benchmark.ipynb`, `src/analysis_00`–`12`,
  `calmar/synthetic.py` and `analyses/segmentation-benchmark/`. The
  participant workflow (`calmar-guided.ipynb`, the detailed notebook,
  `src/analysis_13` onwards) never calls them.
- `calmar.qc` resolves repository resources relative to its own source
  location and passes `CALMAR_SOURCE_DIR` to the wrappers. Standalone
  scripts resolve `PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"` and must not
  infer a submission directory from a spool copy's filename.
- The Neurodesk command `linda_predict_with_mask.sh` provided by the
  installed container keeps its name; notebook calls to it are
  intentional. The repository fallback is `src/analysis_17_*`, which
  pins LINDA 0.5.1 in Neurodesk and retains native-R dispatch outside it.
- The segmentation benchmark's scripts and ASTRA record live here even
  though the participant workflow does not call them. Absence of a
  caller in the main notebook does not make benchmark, KB, container or
  provenance files obsolete.
- The QC choice (Do QC / Skip QC) is stored in `QC_decision.json` under
  the participant/session's LINDA output directory, separately from the
  `*.qc.json` ratings and edits.

## History

**October 2026.** The six ASTRA record folders moved under `analyses/`,
`CHANGELOG.md`, `SETUP.md` and `QC_RUBRIC.md` into `docs/`,
`constraints-neurodesk.txt` into `src/`, and `tests/requirements*.txt`
were folded into `requirements-dev.txt`; the
README was split into `docs/NOTEBOOK_GUIDE.md`, `docs/PIPELINE.md` and
`docs/RUNNING_JOBS.md`, report screenshots moved to `docs/images/` and
the sample image to `tests/images/`. The knowledge base moved its
Python modules into `stroke-aphasia-kb/scripts/`; CALMaR imports them
through `calmar/kb_paths.py`, which also accepts the old flat layout.

**September 2026 (`2026-09-24`).** Root-level modules became the
`calmar/` package and loose scripts moved under `src/`. Old names and
their replacements:

| Previous path/import | Replacement |
|---|---|
| `import linda_qc as q` | `from calmar import qc as q` |
| `import calmar_masks as cm` | `from calmar import masks as cm` |
| `import calmar_widgets as cw` | `from calmar import widgets as cw` |
| `import calmar_disconnectomes as cd` | `from calmar import disconnectomes as cd` |
| `from calmar_overlay import mask_comparison` | `from calmar.overlay import mask_comparison` |
| `from calmar_atlas_ui import OverlapSelection` | `from calmar.atlas_ui import OverlapSelection` |
| `from synthetic_stroke import synthetic_install` | `from calmar.synthetic import synthetic_install` |
| root `linda_predict_with_mask.sh` | `src/analysis_17_linda_predict_with_mask.sh` |
| root `linda_predict_with_mask.R` | `src/r/linda_predict_with_mask.R` |
| root `warp_native_to_mni.sh` | `src/analysis_15_warp_native_to_mni.sh` (same arguments) |
| `src/inspect_alignment.py` | `src/python/inspect_alignment.py` |
| `src/refresh_corrected_disconnectomes.py` | `src/python/refresh_corrected_disconnectomes.py` |
| `src/warp_native_mask_to_ch2.R` | `src/r/warp_native_mask_to_ch2.R` |

Both were source layout changes: data, derivatives, QC sidecars, report
locations, scientific parameters and saved provenance stayed in place.
Historical scripts are recoverable from the pre-migration commit
recorded in `analyses/alignment-repair/astra.yaml`. Old notebook snapshots with
recovery value were archived under the ignored
`notes/archive/repository-layout-2026-09-24/` with a `manifest.json` of
SHA-256 hashes; they are not scientific results. The knowledge base
itself moved out of the in-tree `aphasia-kb/` folder into its own
repository in October 2026.
