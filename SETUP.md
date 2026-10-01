# Setting up CALMaR on a new machine

Clone the repository into persistent Neurodesktop storage, then launch the
notebooks from its root directory:

```bash
cd ~/neurodesktop-storage
git clone https://github.com/micmas/calmar.git
cd calmar
```

The source layout is described in [docs/REPOSITORY_LAYOUT.md](docs/REPOSITORY_LAYOUT.md).
Python helpers live in the local `calmar/` package. No editable installation
is required when running from the repository root.

## Dependencies and first run

Use Neurodesktop for the neuroimaging tools. The notebook loads explicit module
versions; follow its setup sequence rather than inferring a tool version from
an older notebook's outputs. Python dependencies are listed in
`requirements.txt`. Setup checks them and prints terminal installation
instructions if something is missing; restart the kernel after installing
packages.

Keep `nilearn<0.14` in this Neurodesk environment: Nilearn 0.14 requires
`packaging>=26`, while the installed Snakemake requires `packaging<26`.
The September 29 setup repair verified imports with Nilearn 0.13.1,
ipylab 1.0.0, SimpleITK 2.5.6, and packaging 25.0. Installation logs are local
execution artifacts and are not distributed through Git.

For the form-based workflow, open `calmar-guided.ipynb`, run its first code cell,
fill in the inputs and options, and click **Start workflow**. The remaining
steps use buttons. Code is collapsed and reuses the detailed notebook.
Changing **Input type** immediately switches the visible fields: OpenNeuro
accession/version, a local folder, or one T1 file. Single-file mode hides cohort
filters and sampling options and always uses the selected file as participant 0.
In OpenNeuro mode, leaving both participant and session fields blank enables
random selection up to the participant limit. Sampling chooses distinct people
and one available T1 session per person; limit 0 includes all people. The saved
configuration's random seed makes the selection repeatable. Session filters
apply to T1 inputs. A publisher mask can come from another session of the same
participant: the pipeline locates its source T2/FLAIR scan and registers that
scan and mask to the selected T1, as in the detailed notebook.
Navigation requires `ipylab==1.0.0` and `anywidget`, included in requirements.
The controls connect through the active extension registry rather than a saved
child widget. Clicking a workflow button retries a failed connection; the
checkpoint remains closed until connection and confirmation succeed.
Brain viewers load their imaging bundle after widget startup, so a cold cache
does not trip anywidget's short initialization timeout. They show a loading
message while the bundle arrives and an explicit error if it cannot load.
Local images use authenticated HTTP with browser caching when available,
including with `NIIVUE_URL_BASE=False`; bounded 256 KiB kernel messages provide
a fallback. Widget restoration contains file descriptions instead of full image
buffers, allowing ordinary controls to load independently of image transfer.
Off-screen viewers load when scrolled into view or when their tab is opened.
With the kernel fallback, image loading waits while a computation occupies
the kernel, then resumes automatically. A busy or disconnected kernel no longer
causes the viewer to discard its pending image request after one minute.
Interrupted transfers retry after the notebook connection returns, and late
chunks from an earlier attempt cannot corrupt the new transfer.
Dynamic panels use `calmar.widgets.Output`, which captures their content in
Python and updates the widget state. This prevents a panel's `clear_output()`
from deleting the entire cell's controls and viewer in server-side execution.
After installing them, reload JupyterLab. If the ipylab frontend is still not
registered, restart the JupyterLab server, then reopen the notebook.

For the detailed notebook:

1. Open `lesion-interpretation-pipeline.ipynb` from this checkout.
2. Complete Setup and confirm “CALMaR setup imports completed.”
3. Review Configuration. The example selects three participants: sub-M2066,
   sub-M2075 and sub-M2176. They have been processed in the development checkout;
   a new checkout's local files determine which processing steps are cached.
4. Run dataset discovery/acquisition and inspect the selected subject/session
   pairs. The default dataset is OpenNeuro ds004884, pinned to tag 1.0.2,
   under `data/ds004884/`. Missing content is fetched through DataLad.
5. Follow the single-subject test, then the batch workflow. The notebook
   stops at the test→batch boundary when `RUN_TEST=True`.
   Cells above that boundary can still be rerun, including the single-subject
   viewers; rerunning them does not release the batch checkpoint.
   The same rule applies at QC, report selection, and the guided input form:
   earlier cells and the stop's own cell remain runnable; later cells wait.
   Click **Continue to batch** and accept the Run all cells below prompt. The
   button selects the correct starting cell and starts processing up to QC.
   With `RUN_TEST=False`, every single-subject code cell prints only
   `RUN_TEST = False — continuing into batch processing` and performs no test work.
6. At the **Quality control** dashboard, saved QC is listed with participant
   names and stage counts. Choose **Use existing QC** to retain it and immediately
   continue after QC, or **Redo QC** to start fresh ratings from stage 1.
   Reusing does not mark any previously unrated stages as complete.
   Redo preserves saved ratings until you save replacements. When no saved QC
   exists, choose **Do QC**. **Skip QC** is always available. These choices unlock
   execution and appear once, above the review panel; repair and
   continue buttons sit below the ratings and save controls. Saving ratings
   also releases the checkpoint. **Save stage →**
   saves the current rating and opens the next stage. **Save & next participant**
   saves all available stages and starts the next participant at stage 1.
   Draft choices survive navigation within the panel, but not a kernel restart
   or rerunning the QC cell. A poor skull-strip rating queues repair; use
   **Run skull-strip repair** to run the next queued participant. In the detailed
   notebook, rerun the QC dashboard afterward to review the repaired outputs; the guided
   notebook reopens QC automatically. Do QC does not certify completed review.
   Skip QC remains available after choosing Do QC and saves your choice per participant and
   session, and newly generated reports state that QC was skipped by the user.
   Both choices preserve existing ratings. Use **Continue after QC** to start
   disconnectomes and reports without running optional repair/edit/reset cells.
7. In **Group lesion overlap map**, choose the mask source and click **Build
   selected group map**. The atlas tables and Schaefer summary have their own
   mask selectors. Table titles identify the atlas and selected mask.
8. **Preview and export atlas results** lets you select a participant, atlas
   and mask. Open the brain tab to load images. **Export selected atlas PDF**
   exports these same choices.
9. At **Choose report inputs**, use the participant, mask and display-atlas
   dropdowns. Expand **Compare available MNI masks** if helpful; enable
   Neurosynth only when wanted. Click **Generate participant report** to start
   the report cells. Review the expandable sections, brain-viewer tab and
   optional Neurosynth tab, then download HTML or use its Print button for PDF.
   **Choose another report** returns to the input form.

Follow the execution environment's `AGENTS.md` for module initialization,
retained scripts, Slurm submission, validation, and provenance. Retained shell
entry points are in `src/analysis_*.sh`, with implementation files under
`src/python/` and `src/r/`. Submit from the repository root and create
`logs/` first. Data acquisition and imaging computation are not lightweight
setup/import checks.

## Updating an existing checkout

Preserve local edits before updating the branch. After pulling the repository
layout change, restart the notebook kernel and rerun Setup: old root-level
module names have moved to `calmar`, and live viewer state cannot safely be
mixed across both layouts. Both notebooks already use the updated imports and
script paths.

`main` contains the imaging workflow. `ollama-local-models` adds local-model
KB extraction/review and optional RAG narrative generation; that branch had its
history rebased in September 2026. Preserve local work before synchronizing a
checkout that still has the old history.

## Knowledge base

KB data and tools remain together under `aphasia-kb/`. From the repository root:

```bash
python aphasia-kb/aphasia_kb.py
```

See [aphasia-kb/README.md](aphasia-kb/README.md) and
[aphasia-kb/HOWTO.md](aphasia-kb/HOWTO.md) for extraction and review.
Source PDFs under `aphasia-kb/papers/` are local files, not distributed via Git.

## What travels through Git

| Content | In Git? |
|---|---|
| Notebooks, `calmar/`, retained source scripts, tests, documentation | Yes, when committed |
| KB code, curated entries, and tracked review records | Yes |
| Datasets and derivatives under `data/` | No |
| QC sidecars stored alongside those derivatives | No |
| Reports, QC summaries, cached atlases, and `qc_edits/` | No |
| Source paper PDFs and generated Neurosynth caches | No |
| Local handoffs, recovery snapshots, and cleanup archives under `notes/` | No |

Copy scientific results, ratings, manual edits, and provenance separately when
moving machines. Re-running segmentation does not restore a manually edited mask
or its QC history. Preserve the mask and its sidecar together; edit logs do not
automatically replay edits.

Review `git status` and stage intended source paths explicitly when sharing
changes. An untracked analysis script or specification can still be important
unfinished work; do not treat it as disposable.

## Lightweight verification

```bash
python -m pip install -r tests/requirements.txt
python -m pytest -q
```

These tests exercise discovery, imports, widget callbacks, and script dispatch
without launching imaging jobs. They do not replace the three-participant
end-to-end run or browser QC. Optional browser checks require
`tests/requirements-browser.txt` and a Playwright browser installation.
The retained `src/analysis_19_verify_interpretation.sh` verifies overlap
laterality and cached Neurosynth decoding on existing outputs through Slurm;
`workflow-validation/astra.yaml` records its inputs and verification scope.
