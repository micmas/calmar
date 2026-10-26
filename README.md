# CALMaR — Co-designed, Automated Lesion Mapping and Reporting

CALMaR is an open-source Jupyter notebook pipeline for automated stroke lesion segmentation, quality control, and clinician-facing interpretation of structural brain MRI data. It is designed to run inside [Neurodesktop](https://www.neurodesk.org/), a browser-accessible neuroimaging environment that provides all required tools pre-installed.

> [!NOTE]
> **All model steps run locally.** `stroke-aphasia-kb/extract.py`,
> `auto_review.py --llm-review` and `aphasia_kb_rag.py --llm` use a local
> model via Ollama; paper text and patient-derived lesion data never leave
> the machine. Model choice is in `stroke-aphasia-kb/models.yaml`
> (see `stroke-aphasia-kb/MODELS.md`); who may approve what is in
> `stroke-aphasia-kb/GOVERNANCE.md`. The CALMaR colour palette for figures and
> UI is `docs/CALMAR_PALETTE.md`.

> [!IMPORTANT]
> **The knowledge base is a separate repository:
> [micmas/stroke-aphasia-kb](https://github.com/micmas/stroke-aphasia-kb).**
> CALMaR consumes it as a git submodule at `stroke-aphasia-kb/`, pinned to
> one KB commit, so clone with `--recurse-submodules` (or run
> `git submodule update --init` in an existing checkout). Entries, scripts
> and governance documents are edited and reviewed in that repository, not
> here; see [Aphasia knowledge base](#aphasia-knowledge-base) below for how
> to update the pinned commit.

Given a BIDS-formatted dataset, CALMaR will:

1. **Segment lesions** using an HD-BET brain mask, LINDA and/or SynthStroke (`SEGMENTATION_METHODS`), and optionally BCBToolkit
2. **QC every mask** with an interactive dashboard, stage-aware rubric, and edit audit trail
3. **Analyse regional overlap** against five atlases (HarvardOxford, AAL, Destrieux, Schaefer400, JHU)
4. **Optionally analyse directional dMRI** with lesion-aware QSIPrep and experimental QSIRecon tractometry, kept separate from normative disconnectomes
5. **Optionally measure background brain health** with T1-derived atrophy-sensitive volumetry and stroke-aware FLAIR white-matter-hyperintensity burden
6. **Decode the lesion** against Neurosynth v7 meta-analytic language/cognitive maps
7. **Interpret clinically** using an aphasia knowledge base: predicted impairments, WAB-driven outcome predictions, and evidence-based therapy recommendations with stage-mismatch warnings

---

## Requirements

- [Neurodesktop](https://www.neurodesk.org/) (Play or local) — provides the neuroimaging tools that the retained Slurm scripts in `src/` load with pinned `module load` versions: LINDA, HD-BET, SynthStrip, SynthStroke, BCBToolkit, DeepDisco, DeepWMH, SynthSeg, ANTs, FSL, FreeSurfer, OpenADS, QSIPrep and QSIRecon, plus all Python/R dependencies
- A BIDS-formatted dataset (the notebook fetches `ds004884` from OpenNeuro via datalad by default)
- Python packages listed in `requirements.txt` (usually pre-installed in Neurodesktop; Setup prints terminal installation instructions for anything missing)
- A FreeSurfer licence at `~/license.txt` or in `FS_LICENSE` when the optional QSIRecon route is selected

---

## Repository layout

| Path | Purpose |
|------|---------|
| `calmar-guided.ipynb` | Guided workflow — inputs, options, QC, and continuation buttons |
| `lesion-interpretation-pipeline.ipynb` | Detailed processing notebook and canonical implementation |
| `lesion-segmentation-benchmark.ipynb` | Benchmarks LINDA / SynthStroke across chronic and acute datasets |
| `calmar/` | Shared Python package. Key modules: `study.py` (participant discovery + every derivatives path), `processing.py` (one documented `step_<name>` function per processing step, run inside Slurm), `scheduled.py` (`submit_step`: one Slurm job per participant, receipts, reuse; `in_slurm` for QC repairs), `step_qc.py` (saved QC figure + plausibility metrics per step), `step_summary.py` (`show_step` tables), `step_viewer.py` (the viewer under each step), `methods.py` (methods table), plus QC, viewer and report modules |
| `src/analysis_*.sh` | Retained analysis entry points; submit from the repository root |
| `src/python/`, `src/r/` | Python/R implementations called by the analysis scripts |
| `tests/` | Lightweight regression tests; no imaging jobs or downloads |
| `alignment-repair/astra.yaml` | Scientific record of the native-to-MNI correction |
| `diffusion-tract-analysis/astra.yaml` | Planned/implemented decisions and outputs for optional direct dMRI; no findings are recorded before execution and QC |
| `brain-health-analysis/astra.yaml` | Scientific record for optional SynthSeg volumetry and stroke-aware DeepWMH measurements |
| `docs/REPOSITORY_LAYOUT.md` | Module map, script entry points, and migration notes |
| `docs/DOMAIN_SEVERITY_INPUT.md` | Report-only domain impairment scale, domain set, and instrument mapping proposed before any KB schema change |
| `docs/CT_ROUTE.md` | CT lesion-segmentation and CT-to-MNI scope, reporting cautions, and minimum validation plan; no CT dependency is installed |
| `docs/SAMPLE_APPLICABILITY_FIELDS.md` | Approval-gated proposal for stroke-history, laterality, modality, and age applicability fields |
| `QC_RUBRIC.md` | Stage-aware QC rating reference (acute / subacute / chronic) |
| `stroke-aphasia-kb/` | **Git submodule** → [micmas/stroke-aphasia-kb](https://github.com/micmas/stroke-aphasia-kb), the aphasia literature knowledge base (its own repository; see its `README.md`) |
| `container/` | In-container LINDA wrapper source (baked into the Neurodesk image) |
| `requirements.txt` | Python dependencies |

Runtime directories (created automatically, excluded from git):

| Path | Contents |
|------|---------|
| `data/` | Datalad-installed datasets (ds004884, ISLES-2022, …) |
| `atlases/` | Cached nilearn atlas files |
| `reports/` | CSVs, group maps, HTML interpretation reports |
| `qc_edits/` | Round-trip folder for ITK-SNAP / FSLeyes edits |

---

## Quickstart

```bash
# 1. Open Neurodesktop (Play or local) and start a JupyterLab session
# 2. Clone the repo into neurodesktop-storage so it persists across sessions
git clone https://github.com/micmas/calmar.git ~/neurodesktop-storage/calmar
cd ~/neurodesktop-storage/calmar

# 3. Open the notebook
# File → Open → calmar-guided.ipynb

# 4. Run the Inputs and options cell once, then use the form and buttons
```

The notebook uses `Path.cwd()` for all paths — no path editing required as long as you open it from the repo root.

### ISLES 2022 quickstart

ISLES 2022 is distributed separately from OpenNeuro. Obtain and extract the
[official dataset](https://www.isles-challenge.org/) so one directory contains
both `sub-strokecase*` and `derivatives/`; the default local location is
`data/ISLES-2022/`. In `calmar-guided.ipynb`:

1. Choose **DWI + ADC — OpenADS** as the imaging route.
2. Choose **ISLES 2022 (local)** as the input type.
3. Select the extracted dataset root, optionally restrict the participants, and start.

The form checks for `*_dwi.nii.gz` files with sibling `*_adc.nii.gz` maps before
processing. It also recognises the official expert masks at
`derivatives/{sub}/{ses}/{sub}_{ses}_msk.nii.gz`; users do not need to construct
a `MANUAL_MASK_PATH` template. For a nonstandard copy, choose **Local BIDS** and
configure the manual-mask path and space explicitly.

The notebooks import the local `calmar` package directly; no editable install
is required when launched from this directory. After updating from the older
root-script layout, restart the kernel and rerun Setup so old module instances
and viewer registries are not mixed with the reorganized package.

The guided notebook reuses the detailed notebook's cells, resolved by stable cell
IDs in `calmar/workflow_cells.json`. It saves your selected inputs in
`reports/guided-inputs.json`. QC supports clickable ratings for every available
stage, saving a whole participant at once, and a persistent Skip QC option.
Manual masks are rated for their registration to MNI; the native delineation is
a reference. See [SETUP.md](SETUP.md) for continuation and repair controls.

When QC already exists, the dashboard lists those participants and their saved
stage counts and offers **Use existing QC**, **Redo QC**, or **Skip QC**.
Reusing keeps saved ratings and immediately continues after QC. Unrated stages
in a mixed cohort remain unrated.
Redo starts blank ratings from stage 1; saved ratings are replaced only when
you save. Reports distinguish reused QC from skipped QC.

Setup installs missing notebook packages (nilearn, SimpleITK, PyMuPDF, ipylab, …)
with `pip install --user`, into `~/.local` on the persistent home volume, so they
survive a Neurodesk restart; installed packages are not upgraded. If it reports
that the installation changed a package the kernel had already loaded, use
**Kernel → Restart Kernel** and rerun Setup through Configuration. Continue
only after **CALMaR setup imports completed.** appears. If an earlier run
installed packages and subsequent cells all fail with missing variables, restart
the kernel first: rerunning downstream cells cannot recover failed imports.
The import cell detects a stale in-memory `packaging` version; downstream
decoding checks that setup completed before proceeding.

For already discovered T1w subjects, QC discovers existing masks and offers
only available stages: a SynthStroke native mask does not require a
LINDA lesion output. The manual mask is rated only after warping to MNI.
Existing QC sidecar locations are preserved. The report
selector lists only locally available MNI masks for the selected subject and
session; native automatic masks remain available for QC. Configured manual masks
must declare their space, and masks drawn on another scan need registration
before they can be used in T1w QC. Finding a file does not validate its alignment.
LINDA-specific edit and rerun actions remain specific to LINDA. The acute DWI
route discovers DWI/ADC pairs and uses OpenADS; its separate lesion and
registration QC stages do not expose the LINDA-only repair actions.

Lightweight regression checks (no segmentation or data downloads):

```bash
python -m unittest discover -s tests -v
```

The disconnectome comparison and viewer each have independent subject, mask,
and map selectors. They include DeepDisco outputs even when the corresponding
BCBToolkit map is missing; agreement metrics appear only when both maps exist.
Use **Refresh files** after upstream computation finishes. Manual-mask outputs
retain the legacy `expert` filename token.

Native LINDA, manual and SynthStroke masks use LINDA's complete native→Penn→ch2
transform chain (including the inverse subject affine and bundled Penn→ch2
transforms), continued ch2→MNI152 in the same resampling. The final reference is `Subject_in_MNI.nii.gz`; the intermediate
`Reg3_registered_to_template.nii.gz` is not MNI. The single-subject comparison prepares the manual MNI
mask before the disconnectome test cells and provides independent overlay
toggles with fixed binary display ranges, including for very sparse masks.
Alignment verification and repair records live in `alignment-repair/astra.yaml`.

The current example cohort is configured, in discovery order, for
**sub-M2001 / ses-1076**, **sub-M2075 / ses-602**, and **sub-M2077 / ses-250**,
with BCBToolkit and DeepDisco enabled for LINDA, SynthStroke, and manual masks,
and all four DeepDisco models. Discovery uses the normal DataLad fetch for any
missing content. The cohort size remains three, random sampling is disabled,
and overwrite remains false. At selection time, participants 1 and 3 have no local
processing outputs; participant 2 has existing outputs. Their processed state
depends on the checkout's data directory. Existing outputs do not by themselves establish
completed QC or end-to-end verification.

The single-subject comparison checkboxes change overlay opacity without reloading volumes.
The optional **Lesion frequency** tab in the results preview builds a group map
only when you click **Build selected group map**.
Before brain extraction, **Choose the single-subject test participant** lists the cohort and
each participant's processing state. It defaults to an unprocessed participant
when available. **Run single-subject test** starts the selected participant's steps.
Cell identities are stored in the notebook structure, without ID comments in code.

The single-subject checkpoint blocks batch and later cells when `RUN_TEST=True`, including
when the runner continues after errors. Earlier cells, including the single-subject
viewers, can be edited and rerun while the batch checkpoint remains paused.
Review the results and click **Continue to batch**. Processing starts at the
batch section and stops again at QC. With
`RUN_TEST=False`, this checkpoint is skipped and batch processing continues.
Every stop point follows the same rule: earlier cells and the stop's own cell
can be rerun; later cells wait for its continuation choice. This also applies
to QC, report selection, and the guided input form. Rerunning an earlier viewer
does not record a QC choice or start report generation.
Cell identity is retained in `# CALMAR_CELL_ID:` comments for clients that omit
JupyterLab's execution metadata. Keep these comments when editing cell bodies.

`CONFIG["MASK_COLORS"]` sets one colour per origin throughout the workflow,
including native/MNI overlays, QC, group maps, comparison legends and report
figures. Defaults: LINDA red, Manual blue, SynthStroke green, brain mask yellow (its HD-BET part orange),
BCBToolkit magenta and DeepDisco cyan. Supported colours are red, green, blue,
yellow, cyan and magenta. After changing the mapping, rerun Configuration and
the affected viewer/report cells. Probability maps retain their value scale
while using their method's hue; the comparison's absolute-difference map has
its own quantitative scale.
The QC dashboard blocks later cells until you choose **Do QC** or **Skip QC** for the
current cohort. **Do QC** enables manual review and repair work without marking
QC complete. **Skip QC** saves a dated choice for each participant/session;
newly generated reports, including printed PDFs, state **QC was skipped by the
user**. Neither button runs subsequent cells. Existing ratings remain intact.
**Skip QC → open report** skips only QC, records that decision, and then opens
report settings and participant selection without running the remaining batch stages.

If widgets remain at **Loading widget…**, the checkpoints also support explicit
recovery commands in a temporary code cell. Run `%calmar_continue batch` by
itself to release the batch checkpoint, then select the first batch code cell
under **Batch processing** and choose **Run → Run All Cells Below**. At a paused QC checkpoint,
`%calmar_continue skip-qc` records that QC was skipped by the user before releasing
the pause. `%calmar_continue skip-qc-to-report` skips QC and opens report
selection directly. These commands do not repair widget loading.
Remove the temporary recovery cell afterwards so it is not part of later runs.

**Preview and export results** uses one atlas, mask and participant selection
for its table, brain view, region chart and PDF export. The collapsed **Group
summaries (optional)** section adds a cross-participant heatmap, an explicitly
built lesion-frequency map, and a Schaefer network summary, all using the same
mask source. Group summaries include the configured cohort and do not depend
on the selected individual. Each view names its atlas and mask. SynthStroke is the initial
choice when available; Manual and LINDA remain selectable. This is a display
preference, not a quality ranking. Atlas previews update the table immediately
and load brain images only when their tab is opened, reusing unchanged layers.
**Export selected atlas PDF** uses the preview's exact selection.
Participant menus retain the full configured cohort, including completed
zero-overlap results. Tables show the hemisphere of actual intersecting lesion
voxels, with left/right counts for bilateral intersections. Cache status records
track subject/session pairs and changed masks; older tables are refreshed once
to calculate laterality. A bilateral atlas region does not imply a bilateral lesion.

The single-subject review uses one canvas for reference-scan coregistration and
automatic/manual lesion masks. Switch between the two checks without reloading
the images; cached registrations remain available for inspection. Agreement
metrics are collapsed, and development voxel-count diagnostics are removed.
The agreement table compares LINDA and SynthStroke in separate columns.
The lesion/disconnectome comparison places the lesion beneath the maps and
preserves the selected method, image position and unchanged layers when changing
DeepDisco models. Agreement metrics are calculated when their panel is opened.
DeepDisco models are selected with individual buttons.
Cell timing labels use titles and current cell numbers. Each batch step shows
participant/session durations and outcomes, with separate HD-BET and LINDA entries.
The final summary includes participant totals; cached timings measure this run's
cache checks. Reruns replace the earlier timings. Detailed processing logs stay
beside the outputs, with error excerpts shown when a tool fails.

After the single-subject review, **Jump to reporting** starts at report setup and
opens report selection, bypassing batch segmentation, QC and disconnectome computation.
Generating the selected report prepares any missing atlas overlap tables for that
participant and mask. Saved QC decisions remain unchanged.

At **Choose report inputs**, select the participant, MNI mask and display atlas.
An optional mask-comparison viewer and Neurosynth checkbox are in the same form.
**Generate participant report** starts the remaining report cells automatically.
The result has one panel with expandable evidence sections, a lazy brain viewer,
optional decoding and an HTML download. QC decisions remain in the saved report.
The lesion-location section shows symptom summaries in its primary list when
their matched records span at least two citation keys and two distinct anatomy
mappings after knowledge-base synonyms are merged; every relationship type,
including null and mixed findings, counts. This is a display relevance rule,
not a certainty threshold.
Other symptom summaries remain expandable. White-matter tract rows show the
relationship-direction counts and cross-reference symptom targets that also
have direct-damage evidence from a different anatomy. Each cross-reference
shows the direction mix on both paths without treating them as independent or
additive evidence.
Use **Choose another report** to return to the form. The single-subject comparison
remains the place to compare masks in native T1 space.
Neurosynth reports whether decoding completed, how many terms were tested, and
whether any correlations exceeded its display threshold; warnings remain visible.

---

## Pipeline overview

```
Dataset (BIDS)
    │
    ├─ Brain mask (HD-BET; + SynthStrip per participant when a cavity is left out)
    ├─ Lesion segmentation (LINDA, optional)      ─┐
    ├─ Lesion segmentation (SynthStroke, optional)  ├─ warped to MNI space (LINDA's registration,
    ├─ (no LINDA: ANTs template registration)        │  or the ANTs registration step)
    └─ Expert/manual mask                          ─┘
    (acute route, MODALITY = "dwi": OpenADS on DWI + ADC, warped with its own registration)
            │
            ├─ QC dashboard (interactive, stage-aware)
            │
            ├─ Group lesion frequency map (glass-brain viewer)
            ├─ Atlas overlap (5 atlases, configurable mask source)
            ├─ Schaefer 7-network summary
            ├─ Per-subject interactive report
            │
            ├─ Disconnectome — BCBToolkit + Tractotron, and DeepDisco (deep-learning)
            ├─ Neurosynth lesion decoding
            │
            └─ KB-driven clinical interpretation
                   ├─ Predicted impairments (lesion location × atlas)
                   ├─ Outcome predictions (WAB-AQ, age, lesion volume)
                   ├─ Therapy recommendations (RTSS-tagged, stage-aware)
                   └─ Printable HTML report (Save as PDF)
```

### Reading the detailed notebook

Every processing step follows the same pattern: a markdown cell (what, why, inputs, outputs, parameters, **what to check**), a short code cell that submits the step (`submit_step("linda", entries, study)`), and `show_step(result, study)`, which shows per participant the result, plausibility metrics, ⚠ prompts, the exact commands that produced the outputs and the Slurm log folder (this table stays in the saved notebook), then an interactive NiiVue viewer of the step's images (`calmar/step_viewer.py`: participant menu, overlay checkboxes, plane, centre on lesion). Each job also writes a static QC figure to `reports/qc/steps/<step>/`; `show_step(..., images=True)` embeds it.

### Brain mask

`BRAIN_MASK = "hdbet"` (default): the brain mask that LINDA and SynthStroke use is HD-BET (brain tissue). HD-BET follows surviving tissue, so a CSF-filled chronic infarct cavity that opens onto the brain surface can fall outside its mask (more than 5% of the expert lesion in 12 of 36 sessions, worst 35%). `BRAIN_MASK = "hdbet+synthstrip"` adds SynthStrip's CSF-inclusive mask (2 of 36 sessions above 5%, worst 7%, plus a ~160 ml CSF rim), but LINDA then also labels CSF next to the lesion: on 8 sessions its median Dice fell from 0.61 to 0.59 and false positives rose from 45 to 84 ml. The union helped only where about 40 ml or more of the lesion lay outside HD-BET (sub-M2045, sub-M2029). It is therefore applied per participant: tag the skull strip `lesion_excluded_by_strip` in QC, mark the participant for repair, and the skull-strip repair uses the union for that participant. Evidence and the per-session table: [`docs/validation/brain-mask/`](docs/validation/brain-mask/README.md). Closing (`calmar.brainmask.close_cavities`) does not recover these cavities, because they are wider than any closing radius that would not also fill sulci.

### Template space

LINDA registers each brain to its **ch2 (Colin27)** template (single-subject anatomy in MNI coordinates). The atlases, BCBToolkit tractograms and DeepDisco are defined on **FSL MNI152** (MNI152NLin6Asym), so ch2 is registered to MNI152 once (`src/analysis_38_template_ch2_to_mni152.sh`, ANTs SyN; transforms in `atlases/templates/ch2_to_MNI152NLin6Asym/`) and every mask is warped native → Penn → ch2 → MNI152 in one resampling. `*_in_MNI.nii.gz` are on MNI152 (182×218×182); LINDA's original ch2 outputs are kept as `*_in_ch2.nii.gz`.

`SEGMENTATION_METHODS` (default `["linda", "synthstroke"]`) chooses the automatic segmentations; at least one is required. LINDA takes 1.5-3.7 h per participant, almost all of it its registration to the template. Without LINDA, the **registration step** (`src/analysis_29_registration.sh`, ANTs 2.6.5) registers the brain-extracted T1w directly to the MNI152 brain, with the SynthStroke lesion (dilated 2 voxels) excluded from the cost function: an affine stage (Mattes MI, one thread, seeded), then SyN (cross-correlation, `REGISTRATION_THREADS`), ANTs' documented route to a reproducible result. It took 9 min with 4 threads for sub-M2051 ses-284 (template correlation 0.66, vs 0.63 for LINDA's registration; SynthStroke's template-space mask Dice 0.80 between the two registrations). Its outputs, and the manual mask's products and template-space SynthStroke mask made with it, are in `derivatives/registration/`, so masks warped by the two registrations never share a file.

**Acute route (`MODALITY = "dwi"`).** For acute stroke imaged with diffusion MRI (e.g. ISLES-2022: `sub-*/ses-*/dwi/*_dwi.nii.gz` with `*_adc.nii.gz`), OpenADS (`openadscpu/1.0.0`, `src/analysis_43_openads.sh`) segments the lesion on the DWI and its ADC map. The T1 steps (brain extraction, LINDA, SynthStroke, registration) are skipped.
- **Guided ISLES input:** choose **ISLES 2022 (local)** and its extracted root. The form validates compatible pairs, and the official `*_msk.nii.gz` reference masks are discovered automatically.
- **Optional DWI beside a T1 workflow:** after participant discovery, the notebooks ask whether to analyse any OpenADS-ready DWI/ADC pair they find. A pair may come from the selected T1 session or another session and remains labelled with its own session. The choice is recorded immediately, but OpenADS runs only after the ordinary T1/manual-mask registration inspection and QC. Its registration receives a separate QC checkpoint because DWI contrast and lesion boundaries can change over time, even when the anatomical lesion is expected to be stable in chronic stroke.
- **Directional dMRI is a separate opt-in route:** participant discovery inventories every BIDS `*_dwi.nii.gz` in the selected and other participant sessions. `calmar.diffusion` checks the b-values, b-vectors and JSON sidecar without fetching the NIfTI, requires a b=0 image and at least 30 distinct diffusion directions for participant reporting, and detects an opposite phase-encoding series when present. Trace-DWI/ADC cases without gradients remain eligible for OpenADS but are not treated as tensor or tractography data.
- **Direct processing and reporting:** selected series run after lesion QC through `src/analysis_45_dmri_preproc.sh` (QSIPrep 26.1.1), `analysis_46_dmri_recon.sh` (QSIRecon 26.0.1, default `ss3t_fod_autotrack`) and `analysis_47_dmri_metrics.sh`. The selected native-T1 lesion mask is supplied to QSIPrep as a BIDS lesion ROI. QSIRecon bundle FA/MD summaries are normalized to `derivatives/calmar-dmri/<sub>/<ses>/dwi/metrics/*_desc-direct_tractometry.tsv`; uncomputed fields remain explicitly missing. Reports place these participant measurements in their own section and never numerically combine them with BCB/DeepDisco probabilities. Because stroke pathology can cause registration or tracking failure, a missing bundle is never called proof of disconnection.
- **Template space:** OpenADS also registers the DWI to MNI152 (affine + SyN against its JHU ADC template). Its own template-space "stroke" image is not the lesion, so the native lesion is warped with those transforms (`src/analysis_44_apply_openads_registration.sh`). On 10 ISLES-2022 cases the side was preserved in all, and OpenADS agreed with the expert masks at Dice 0.75–0.91 in template space for most lesions; small lesions are often missed.
- **Same downstream steps:** manual masks, disconnectomes, atlas overlap and the report work as in the chronic route.
- **Recovery phase:** reports tag each knowledge-base finding with the phase it was studied in, so an acute participant sees how much of the evidence comes from chronic-stroke studies.

### Optional brain-health interpretation

`ANALYSE_BRAIN_HEALTH` is an independent opt-in choice. On genuine T1w entries,
`src/analysis_48_brain_health_anatomy.sh` runs robust SynthSeg 8.2.1 parcellation and records
brain-tissue fraction and ventricular volume. These are **atrophy-sensitive descriptive
features**, not a diagnosis: a single scan has no age-/scanner-matched reference, and a
stroke cavity can look like tissue loss. The report therefore also shows a cavity-adjusted
fraction and keeps the caveat visible.

When a same-session FLAIR exists, `analysis_49_brain_health_wmh.sh` runs DeepWMH 1.0.1.
`analysis_50_brain_health_metrics.sh` registers the selected native stroke lesion to FLAIR
with ANTs 2.6.5 and reports both the raw hyperintensity volume and the remainder after
excluding the lesion plus `BRAIN_HEALTH_LESION_EXCLUSION_MM` (default 3 mm). The remainder
is called a **WMH candidate burden**, not automatically small-vessel disease. This matters
especially in acute stroke, where infarct-related oedema can extend beyond the exclusion
zone. CALMaR does not infer a Fazekas grade from volume. Results live under
`derivatives/calmar-brain-health/<sub>/<ses>/anat/`, remain provisional until the saved PNG
overlay is reviewed, and appear in a separate report section.

---

## Aphasia knowledge base

The knowledge base lives in its own repository,
**[micmas/stroke-aphasia-kb](https://github.com/micmas/stroke-aphasia-kb)**
(moved out of this repository's `aphasia-kb/` folder in October 2026 with
its history). `stroke-aphasia-kb/` here is a git submodule: a checkout of
that repository at the commit CALMaR was last tested with. It is a curated,
source-traceable literature base: each finding links a brain region,
predictor or therapy to an outcome, with the verbatim passages from the
paper that support it. CALMaR's clinical-interpretation stage imports
`aphasia_kb.py`, `aphasia_rules.py` and `atlas_mapping/` from it to turn a
lesion mask into a cited report. Extraction and review run on a local model
via Ollama; approval follows the two-tier policy in
`stroke-aphasia-kb/GOVERNANCE.md` (an independent model may approve routine
findings after re-reading the PDF; a person approves the rest and audits).

Working with the submodule:

```bash
git clone --recurse-submodules https://github.com/micmas/calmar.git   # new checkout
git submodule update --init                                           # existing checkout without the KB
git submodule update --remote stroke-aphasia-kb && git add stroke-aphasia-kb \
    && git commit -m "KB: track <commit>"                             # move CALMaR to the KB's latest main
```

KB entries are written, reviewed and committed in the KB repository.
`stroke-aphasia-kb/` is a full clone of it, so a commit made there and
pushed (`cd stroke-aphasia-kb && git push`) lands in the KB repository;
then record the new commit in CALMaR with `git add stroke-aphasia-kb`.
The commands below are the KB's own, run from the CALMaR root:

```bash
python stroke-aphasia-kb/kb_status.py                                        # what is in it
python stroke-aphasia-kb/extract.py --pdf stroke-aphasia-kb/papers/<Key>.pdf        # one paper → drafts
python stroke-aphasia-kb/auto_review.py --all --llm-review --require-pdf-match
python stroke-aphasia-kb/promote.py --list                                   # what needs a person
```

See `stroke-aphasia-kb/README.md` for the layout and `stroke-aphasia-kb/HOWTO.md` for
the full procedure.

---

## Provenance model

CALMaR separates two kinds of work:

**Pipeline outputs** (derivatives) are published atomically with a `*.prov.json` sidecar and a cache record of their inputs (hashes), parameters and the exact commands that produced them. Re-running reuses an output only when all of these match; if a parameter changed, the output is reported as stale and kept until you set the matching `OVERWRITE` / `BCB_OVERWRITE` / `DEEPDISCO_OVERWRITE` (the old output is preserved as `*.previous.*`).

**QC ratings and KB claims** earn full provenance: every QC edit is logged in a sidecar JSON file (`Lesion_in_MNI.qc.json`) with reviewer, timestamp, and a before/after record. Every KB finding carries a citation, method, sample description, and extraction log.

---

## Citation

If you use CALMaR in your research, please cite it using the metadata in `CITATION.cff`:

```
Michele Masson-Trottier (2025). CALMaR: Co-designed, Automated Lesion Mapping and Reporting (v1.0.0).
GitHub: https://github.com/micmas/calmar
```

The detailed notebook's **Citation and Resources** section lists the primary
citations and software resources for each workflow tool, plus the ARC and ISLES
2022 dataset citations.

---

## License

MIT — see `LICENSE`.
