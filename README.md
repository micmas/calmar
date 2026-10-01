# CALMaR — Co-designed, Automated Lesion Mapping and Reporting

CALMaR is an open-source Jupyter notebook pipeline for automated stroke lesion segmentation, quality control, and clinician-facing interpretation of structural brain MRI data. It is designed to run inside [Neurodesktop](https://www.neurodesk.org/), a browser-accessible neuroimaging environment that provides all required tools pre-installed.

> [!CAUTION]
> ⚠️ **Copyright — the extraction CLI sends paper text to the Anthropic API.**
> On this (`main`) branch, `aphasia-kb/extract.py`,
> `auto_review.py --llm-review`, and `aphasia_kb_rag.py --llm` transmit
> **full paper text to a third-party API**. Do not run them on
> copyrighted PDFs you can't share off-machine.
>
> A fully local version — paper text never leaves your computer, via
> Ollama — lives on the **`ollama-local-models`** branch. Use that branch
> for copyright-sensitive material until it's merged.

Given a BIDS-formatted dataset, CALMaR will:

1. **Segment lesions** using HD-BET + LINDA, SynthStroke, and optionally BCBToolkit
2. **QC every mask** with an interactive dashboard, stage-aware rubric, and edit audit trail
3. **Analyse regional overlap** against five atlases (HarvardOxford, AAL, Destrieux, Schaefer400, JHU)
4. **Decode the lesion** against Neurosynth v7 meta-analytic language/cognitive maps
5. **Interpret clinically** using an aphasia knowledge base: predicted impairments, WAB-driven outcome predictions, and evidence-based therapy recommendations with stage-mismatch warnings

---

## Requirements

- [Neurodesktop](https://www.neurodesk.org/) (Play or local) — provides the neuroimaging tools the notebooks load via `module.load`: LINDA, HD-BET, SynthStroke, BCBToolkit, DeepDisco, ANTs, FSL, FreeSurfer (and OpenADS, used only by the benchmark), plus all Python/R dependencies
- A BIDS-formatted dataset (the notebook fetches `ds004884` from OpenNeuro via datalad by default)
- Python packages listed in `requirements.txt` (usually pre-installed in Neurodesktop; Setup prints terminal installation instructions for anything missing)

---

## Repository layout

| Path | Purpose |
|------|---------|
| `calmar-guided.ipynb` | Guided workflow — inputs, options, QC, and continuation buttons |
| `lesion-interpretation-pipeline.ipynb` | Detailed processing notebook and canonical implementation |
| `lesion-segmentation-benchmark.ipynb` | Benchmarks LINDA / SynthStroke across chronic and acute datasets |
| `calmar/` | Shared Python package: QC, mask/disconnectome discovery, viewer controls, and synthetic phantoms |
| `src/analysis_*.sh` | Retained analysis entry points; submit from the repository root |
| `src/python/`, `src/r/` | Python/R implementations called by the analysis scripts |
| `tests/` | Lightweight regression tests; no imaging jobs or downloads |
| `alignment-repair/astra.yaml` | Scientific record of the native-to-MNI correction |
| `docs/REPOSITORY_LAYOUT.md` | Module map, script entry points, and migration notes |
| `QC_RUBRIC.md` | Stage-aware QC rating reference (acute / subacute / chronic) |
| `aphasia-kb/` | Aphasia literature knowledge base (see `aphasia-kb/README.md`) |
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

Setup checks dependencies without installing into the running kernel. If a
package is missing, run the command it prints in a JupyterLab terminal, then
use **Kernel → Restart Kernel** and rerun Setup through Configuration. Continue
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
LINDA-specific edit and rerun actions remain specific to LINDA. DWI-only subject
discovery and OpenADS integration are separate, planned extensions.

Lightweight regression checks (no segmentation or data downloads):

```bash
python -m unittest discover -s tests -v
```

The disconnectome comparison and viewer each have independent subject, mask,
and map selectors. They include DeepDisco outputs even when the corresponding
BCBToolkit map is missing; agreement metrics appear only when both maps exist.
Use **Refresh files** after upstream computation finishes. Manual-mask outputs
retain the legacy `expert` filename token.

Native manual and SynthStroke masks now use LINDA's complete native→Penn→ch2
transform chain, including the inverse subject affine and bundled Penn→ch2
transforms. The final reference is `Subject_in_MNI.nii.gz`; the intermediate
`Reg3_registered_to_template.nii.gz` is not MNI. The single-subject comparison prepares the manual MNI
mask before the disconnectome test cells and provides independent overlay
toggles with fixed binary display ranges, including for very sparse masks.
Alignment verification and repair records live in `alignment-repair/astra.yaml`.

The current example cohort is configured, in discovery order, for
**sub-M2066 / ses-235**, **sub-M2075 / ses-602**, and **sub-M2176 / ses-1237**,
with BCBToolkit and DeepDisco enabled for LINDA, SynthStroke, and manual masks,
and all four DeepDisco models. Discovery uses the normal DataLad fetch for any
missing content. The cohort size remains three, random sampling is disabled,
and overwrite remains false. These participants have now been processed locally;
their processed state depends on the checkout's data directory. Existing outputs do not by themselves establish
completed QC or end-to-end verification.

The single-subject comparison checkboxes change overlay opacity without reloading volumes.
The **Group lesion overlap map** panel lets you select a mask source, then
click **Build selected group map** to build its frequency map.
The single-subject checkpoint blocks batch and later cells when `RUN_TEST=True`, including
when the runner continues after errors. Earlier cells, including the single-subject
viewers, can be edited and rerun while the batch checkpoint remains paused.
Review the results, click **Continue to
batch** there and confirm **Run all cells below**. Processing starts at the
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
figures. Defaults: LINDA red, Manual blue, SynthStroke green, HD-BET yellow,
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

If widgets remain at **Loading widget…**, the checkpoints also support explicit
recovery commands in a temporary code cell. Run `%calmar_continue batch` by
itself to release the batch checkpoint, then select the first batch code cell
under **Batch processing** and choose **Run → Run All Cells Below**. At a paused QC checkpoint,
`%calmar_continue skip-qc` records that QC was skipped by the user before releasing
the pause. These commands do not run subsequent cells or repair widget loading.
Remove the temporary recovery cell afterwards so it is not part of later runs.

**Explore atlas results** and **Preview and export atlas results** have independent
atlas, mask and participant selectors. Each table names the chosen atlas and mask;
the Schaefer network summary also has a mask selector. SynthStroke is the initial
choice when available; Manual and LINDA remain selectable. This is a display
preference, not a quality ranking. Atlas previews update the table immediately
and load brain images only when their tab is opened, reusing unchanged layers.
**Export selected atlas PDF** uses the preview's exact selection.
Participant menus retain the full configured cohort, including completed
zero-overlap results. Tables show the hemisphere of actual intersecting lesion
voxels, with left/right counts for bilateral intersections. Cache status records
track subject/session pairs and changed masks; older tables are refreshed once
to calculate laterality. A bilateral atlas region does not imply a bilateral lesion.

The single-subject diagnostics keep one combined automatic/manual mask viewer.
The lesion/disconnectome comparison places the lesion beneath the maps and
preserves the selected method, image position and unchanged layers when changing
DeepDisco models. Agreement metrics are calculated when their panel is opened.
Cell timing labels use titles and current cell numbers.

At **Choose report inputs**, select the participant, MNI mask and display atlas.
An optional mask-comparison viewer and Neurosynth checkbox are in the same form.
**Generate participant report** starts the remaining report cells automatically.
The result has one panel with expandable evidence sections, a lazy brain viewer,
optional decoding and an HTML download. QC decisions remain in the saved report.
Use **Choose another report** to return to the form. The single-subject comparison
remains the place to compare masks in native T1 space.
Neurosynth reports whether decoding completed, how many terms were tested, and
whether any correlations exceeded its display threshold; warnings remain visible.

---

## Pipeline overview

```
Dataset (BIDS)
    │
    ├─ Skull strip (HD-BET / SynthStrip)
    ├─ Lesion segmentation (LINDA)      ─┐
    ├─ Lesion segmentation (SynthStroke)  ├─ warped to MNI space
    └─ Expert/manual mask               ─┘
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

---

## Aphasia knowledge base

The `aphasia-kb/` subdirectory is a structured literature database of aphasia findings, therapies, and their active ingredients (RTSS framework). Each entry links a brain region or clinical predictor to an expected impairment or outcome, with citations, sample metadata, and confidence levels.

To add a paper to the KB, point the extraction agent at `aphasia-kb/EXTRACTION_SKILL.md`. Extracted drafts go to `aphasia-kb/drafts/`; promote reviewed entries with:

```bash
python aphasia-kb/promote.py --list      # review drafts
python aphasia-kb/promote.py --approve <id>
```

---

## Provenance model

CALMaR separates two kinds of work:

**Pipeline outputs** (derivatives) are versioned through BIDS-style folder structure and skip logic — re-running a cell never overwrites a completed subject unless you explicitly set `*_OVERWRITE = True`.

**QC ratings and KB claims** earn full provenance: every QC edit is logged in a sidecar JSON file (`Lesion_in_MNI.qc.json`) with reviewer, timestamp, and a before/after record. Every KB finding carries a citation, method, sample description, and extraction log.

---

## Citation

If you use CALMaR in your research, please cite it using the metadata in `CITATION.cff`:

```
Michele Masson-Trottier (2025). CALMaR: Co-designed, Automated Lesion Mapping and Reporting (v1.0.0).
GitHub: https://github.com/micmas/calmar
```

---

## License

MIT — see `LICENSE`.
