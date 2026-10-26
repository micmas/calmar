# Using the notebooks

How the two notebooks behave once they are open: the setup cell, the
guided form, the stop points, the QC dashboard, the results preview and
the participant report. Installation is in [SETUP.md](SETUP.md); what
each processing step computes is in [PIPELINE.md](PIPELINE.md); how
jobs are submitted and cached is in [RUNNING_JOBS.md](RUNNING_JOBS.md).

Both notebooks use `Path.cwd()` for every path, so open them from the
repository root and nothing needs editing. They import the local
`calmar` package directly; no editable install is required.

## The two notebooks

`calmar-guided.ipynb` is the form-based workflow: run its first code
cell, fill in the inputs and options, click **Start workflow**, and
drive the rest with buttons. Its code is collapsed and reuses the
detailed notebook's cells, resolved by stable cell IDs in
`calmar/workflow_cells.json`. It saves your selected inputs in
`reports/guided-inputs.json`.

`lesion-interpretation-pipeline.ipynb` is the detailed notebook and the
canonical implementation. Every processing step follows the same
pattern: a markdown cell (what, why, inputs, outputs, parameters, what
to check), a short code cell that submits the step
(`submit_step("linda", entries, study)`), and `show_step(result, study)`,
which shows per participant the result, plausibility metrics, ⚠
prompts, the exact commands that produced the outputs and the Slurm log
folder (this table stays in the saved notebook), then an interactive
NiiVue viewer of the step's images (`calmar/step_viewer.py`:
participant menu, overlay checkboxes, plane, centre on lesion). Each job
also writes a static QC figure to `reports/qc/steps/<step>/`;
`show_step(..., images=True)` embeds it.

Cell identity is stored in the notebook structure and retained in
`# CALMAR_CELL_ID:` comments for clients that omit JupyterLab's
execution metadata. Keep these comments when editing cell bodies.

## Setup cell

Setup installs missing notebook packages (nilearn, SimpleITK, PyMuPDF,
ipylab, …) with `pip install --user`, into `~/.local` on the persistent
home volume, so they survive a Neurodesk restart; installed packages are
not upgraded. If it reports that the installation changed a package the
kernel had already loaded, use **Kernel → Restart Kernel** and rerun
Setup through Configuration. Continue only after
**CALMaR setup imports completed.** appears. If an earlier run installed
packages and subsequent cells all fail with missing variables, restart
the kernel first: rerunning downstream cells cannot recover failed
imports. The import cell detects a stale in-memory `packaging` version;
downstream decoding checks that setup completed before proceeding.

After pulling a change to the repository layout, restart the kernel and
rerun Setup so old module instances and viewer registries are not mixed
with the reorganised package.

## The guided input form

Changing **Input type** immediately switches the visible fields:
OpenNeuro accession/version, a local folder, or one T1 file. Single-file
mode hides cohort filters and sampling options and always uses the
selected file as participant 0. In OpenNeuro mode, leaving both
participant and session fields blank enables random selection up to the
participant limit. Sampling chooses distinct people and one available T1
session per person; limit 0 includes all people. The saved
configuration's random seed makes the selection repeatable. Session
filters apply to T1 inputs. A publisher mask can come from another
session of the same participant: the pipeline locates its source
T2/FLAIR scan and registers that scan and mask to the selected T1, as in
the detailed notebook.

### ISLES 2022

ISLES 2022 is distributed separately from OpenNeuro. Obtain and extract
the [official dataset](https://www.isles-challenge.org/) so one directory
contains both `sub-strokecase*` and `derivatives/`; the default local
location is `data/ISLES-2022/`. In the guided notebook choose
**DWI + ADC — OpenADS** as the imaging route, **ISLES 2022 (local)** as
the input type, select the extracted dataset root, optionally restrict
the participants, and start. The form checks for `*_dwi.nii.gz` files
with sibling `*_adc.nii.gz` maps before processing. It also recognises
the official expert masks at
`derivatives/{sub}/{ses}/{sub}_{ses}_msk.nii.gz`; you do not need to
construct a `MANUAL_MASK_PATH` template. For a nonstandard copy, choose
**Local BIDS** and configure the manual-mask path and space explicitly.

## The example cohort

The current example cohort is configured, in discovery order, for
**sub-M2001 / ses-1076**, **sub-M2075 / ses-602** and
**sub-M2077 / ses-250**, with BCBToolkit and DeepDisco enabled for
LINDA, SynthStroke and manual masks, and all four DeepDisco models. The
default dataset is OpenNeuro ds004884, pinned to tag 1.0.2, under
`data/ds004884/`; missing content is fetched through DataLad. The cohort
size is three, random sampling is disabled and overwrite is false. At
selection time, participants 1 and 3 have no local processing outputs
and participant 2 has existing outputs; a new checkout's local files
determine which steps are cached. Existing outputs do not by themselves
establish completed QC or end-to-end verification.

## Stop points and continuation

Every stop point follows the same rule: earlier cells and the stop's own
cell can be rerun; later cells wait for its continuation choice. This
applies to the single-subject checkpoint, QC, report selection and the
guided input form. Rerunning an earlier viewer does not record a QC
choice or start report generation. Intentional pauses suppress queued
downstream cells without a traceback for each one.

**Single-subject test.** Before brain extraction,
**Choose the single-subject test participant** lists the cohort and each
participant's processing state; it defaults to an unprocessed
participant when available. **Run single-subject test** starts the
selected participant's steps. With `RUN_TEST=True` the checkpoint blocks
batch and later cells, including when the runner continues after errors.
Review the results and click **Continue to batch**: processing starts at
the batch section and stops again at QC. With `RUN_TEST=False` every
single-subject code cell prints only
`RUN_TEST = False — continuing into batch processing` and the checkpoint
is skipped.

**Jump to reporting.** After the single-subject review,
**Jump to reporting** starts at report setup and opens report selection,
bypassing batch segmentation, QC and disconnectome computation.
Generating the selected report prepares any missing atlas overlap tables
for that participant and mask. Saved QC decisions remain unchanged.

**Navigation widgets.** The continuation buttons need `ipylab==1.0.0`
and `anywidget`, both in `requirements.txt`. The controls connect
through the active extension registry rather than a saved child widget;
clicking a workflow button retries a failed connection, and the
checkpoint remains closed until connection and confirmation succeed.
After installing the packages, reload JupyterLab; if the ipylab
frontend is still not registered, restart the JupyterLab server and
reopen the notebook.

**Recovery without widgets.** If widgets remain at **Loading widget…**,
the checkpoints also accept explicit commands in a temporary code cell.
`%calmar_continue batch` releases the batch checkpoint: then select the
first batch code cell under **Batch processing** and choose
**Run → Run All Cells Below**. At a paused QC checkpoint,
`%calmar_continue skip-qc` records that QC was skipped by the user before
releasing the pause, and `%calmar_continue skip-qc-to-report` skips QC
and opens report selection directly. These commands do not repair widget
loading. Remove the temporary cell afterwards so it is not part of later
runs.

## Quality control

The QC dashboard blocks later cells until you choose for the current
cohort. The choices appear once, above the review panel; repair and
continue buttons sit below the ratings and save controls.

When QC already exists, the dashboard lists those participants and their
saved stage counts and offers **Use existing QC**, **Redo QC** or
**Skip QC**. Reusing keeps saved ratings and immediately continues after
QC; unrated stages in a mixed cohort remain unrated. Redo starts blank
ratings from stage 1; saved ratings are replaced only when you save.
When no saved QC exists, choose **Do QC** or **Skip QC**.

- **Do QC** enables manual review and repair work without marking QC
  complete; it records review intent, not completed review.
- **Skip QC** saves a dated choice for each participant/session; newly
  generated reports, including printed PDFs, state
  **QC was skipped by the user**. It stays available after choosing Do
  QC.
- **Skip QC → open report** skips only QC, records that decision, then
  opens report settings and participant selection without running the
  remaining batch stages.

Neither button runs subsequent cells; existing ratings remain intact,
and reports distinguish reused QC from skipped QC. The choice is saved
in `QC_decision.json` under the participant/session's LINDA output
directory, separately from the `*.qc.json` ratings and edits; regenerate
a report after changing it to update the saved notice.

**Rating.** QC offers only the stages that are available: a SynthStroke
native mask does not require a LINDA lesion output, and the manual mask
is rated only after warping to MNI (the native delineation is a
reference). Existing QC sidecar locations are preserved. Ratings are
clickable for every available stage; **Save stage →** saves the current
rating and opens the next stage, **Save & next participant** saves all
available stages and starts the next participant at stage 1, and saving
also releases the checkpoint. Draft choices survive navigation within
the panel, but not a kernel restart or rerunning the QC cell. The
rating scale and issue tags are in [QC_RUBRIC.md](QC_RUBRIC.md).

**Repair.** A poor skull-strip rating queues repair; **Run skull-strip
repair** runs the next queued participant. In the detailed notebook,
rerun the QC dashboard afterwards to review the repaired outputs; the
guided notebook reopens QC automatically. LINDA-specific edit and rerun
actions remain specific to LINDA; the acute DWI route's separate lesion
and registration QC stages do not expose them. Use
**Continue after QC** to start disconnectomes and reports without
running optional repair/edit/reset cells.

Configured manual masks must declare their space, and masks drawn on
another scan need registration before they can be used in T1w QC.
Finding a file does not validate its alignment.

## Viewers and comparisons

The single-subject review uses one canvas for reference-scan
coregistration and automatic/manual lesion masks. Switch between the two
checks without reloading the images; cached registrations remain
available for inspection. The agreement table compares LINDA and
SynthStroke in separate columns; agreement metrics are collapsed and
calculated when their panel is opened. The comparison checkboxes change
overlay opacity without reloading volumes, and the single-subject
comparison prepares the manual MNI mask before the disconnectome test
cells, with independent overlay toggles and fixed binary display ranges
(including for very sparse masks). It is the place to compare masks in
native T1 space.

The disconnectome comparison and viewer each have independent subject,
mask and map selectors. They include DeepDisco outputs even when the
corresponding BCBToolkit map is missing; agreement metrics appear only
when both maps exist. DeepDisco models are selected with individual
buttons, and changing model preserves the selected method, image
position and unchanged layers. The lesion is placed beneath the maps.
Use **Refresh files** after upstream computation finishes. Manual-mask
outputs retain the legacy `expert` filename token.

Brain viewers load their imaging bundle after widget startup, so a cold
cache does not trip anywidget's short initialisation timeout; they show
a loading message while the bundle arrives and an explicit error if it
cannot load. Local images use authenticated HTTP with browser caching
when available, including with `NIIVUE_URL_BASE=False`; bounded 256 KiB
kernel messages are the fallback, and with it image loading waits while
a computation occupies the kernel, then resumes. A busy or disconnected
kernel does not discard a pending image request after one minute;
interrupted transfers retry when the connection returns, and late chunks
from an earlier attempt cannot corrupt the new transfer. Widget
restoration contains file descriptions instead of full image buffers.
Off-screen viewers load when scrolled into view or when their tab is
opened. Dynamic panels use `calmar.widgets.Output`, which captures their
content in Python so a panel's `clear_output()` cannot delete the whole
cell's controls in server-side execution.

## Colours

`CONFIG["MASK_COLORS"]` sets one colour per origin throughout the
workflow: native/MNI overlays, QC, group maps, comparison legends and
report figures. Defaults: LINDA red, Manual blue, SynthStroke green,
brain mask yellow (its HD-BET part orange), BCBToolkit magenta and
DeepDisco cyan. Supported colours are red, green, blue, yellow, cyan and
magenta. After changing the mapping, rerun Configuration and the
affected viewer/report cells. Probability maps keep their value scale
while using their method's hue; the comparison's absolute-difference
map has its own quantitative scale. The palette for figures and UI is
[CALMAR_PALETTE.md](CALMAR_PALETTE.md).

## Timing

Cell timing labels use titles and current cell numbers. Each batch step
shows participant/session durations and outcomes, with separate HD-BET
and LINDA entries. The final summary includes participant totals; cached
timings measure this run's cache checks, and reruns replace earlier
timings. Detailed processing logs stay beside the outputs, with error
excerpts shown when a tool fails.

## Preview and export results

**Preview and export results** uses one atlas, mask and participant
selection for its table, brain view, region chart and PDF export. Each
view names its atlas and mask. SynthStroke is the initial choice when
available; Manual and LINDA remain selectable (a display preference, not
a quality ranking). Atlas previews update the table immediately and load
brain images only when their tab is opened, reusing unchanged layers.
**Export selected atlas PDF** uses the preview's exact selection.
Participant menus retain the full configured cohort, including completed
zero-overlap results.

Tables show the hemisphere of actual intersecting lesion voxels, with
left/right counts for bilateral intersections. Cache status records
track subject/session pairs and changed masks; older tables are
refreshed once to calculate laterality. A bilateral atlas region does
not imply a bilateral lesion.

The collapsed **Group summaries (optional)** section adds a
cross-participant heatmap for the selected atlas, a Schaefer400 network
summary of the selected mask, and a lesion-frequency map that is built
only when you click **Build selected group map**. All three use the
preview's mask source and the configured cohort, and do not depend on
the selected individual.

## The participant report

At **Choose report inputs**, select the participant, MNI mask and display
atlas. The report selector lists only locally available MNI masks for the
selected subject and session; native automatic masks remain available
for QC. An optional mask-comparison viewer (**Compare available MNI
masks**) and a Neurosynth checkbox are in the same form.
**Generate participant report** starts the remaining report cells
automatically; **Choose another report** returns to the form.

The result has one panel with expandable evidence sections, a lazy brain
viewer, optional decoding and an HTML download (use its Print button for
PDF). QC decisions remain in the saved report. Neurosynth reports whether
decoding completed, how many terms were tested and whether any
correlations exceeded its display threshold; warnings remain visible.

**Behavioural / clinical table.** It does not display the recorded
aphasia-type label. A recognised Kertesz WAB/WAB-R type profile can seed
only fluency, comprehension and repetition context: impaired (`-`) axes
receive a mild profile floor, while relatively preserved (`+`) axes keep
severity unassigned. Every profile-derived row is labelled and can be
replaced by an assessed level.

**Lesion-location section.** Symptom summaries appear in its primary
list when their matched records span at least two citation keys and two
distinct anatomy mappings after knowledge-base synonyms are merged;
every relationship type, including null and mixed findings, counts. This
is a display relevance rule, not a certainty threshold. Other symptom
summaries remain expandable. White-matter tract rows show the
relationship-direction counts and cross-reference symptom targets that
also have direct-damage evidence from a different anatomy; each
cross-reference shows the direction mix on both paths without treating
them as independent or additive evidence.

Reports tag each knowledge-base finding with the recovery phase it was
studied in, so an acute participant sees how much of the evidence comes
from chronic-stroke studies. The fixed rules the report applies (WAB
type profile, recovery stage cut-offs, evidence-strength stars) are
printed as tables under the settings cell and defined, with their
sources, in `stroke-aphasia-kb/scripts/aphasia_rules.py`. The report
carries a research-only caveat that no flag removes.
