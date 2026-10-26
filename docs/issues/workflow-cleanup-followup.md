# Interpretation workflow follow-up

## Notebook regressions repaired after user testing, October 8

The earlier imaging acceptance and widget fixtures did not exercise real
notebook submissions after module loading. Saved user errors showed that
Slurm jobs inherited FSL's container Python wrapper and lost `SLURM_JOB_ID`.
Every notebook submission now passes `sys.executable`, and retained scripts
honor it. Setup no longer loads all imaging modules into the notebook or
performs an internet TLS probe/system package installation.

Acquisition failure previously prevented path helpers from being defined,
causing subsequent `NameError`/`KeyError` failures. Helpers now exist before
acquisition is attempted, and discovery excludes derivatives. Tractotron is
opt-in: legacy header-only tables no longer block the core BCB workflow.

Cache checks no longer reject valid images because unrelated code, logging or
resource directives changed. Scientific inputs/options, explicit algorithm
versions and output hashes still govern image reuse. Completed step receipts
and reporting results persist across kernel restarts, with input/output file
checks before reuse. Checkpoint guards quietly skip queued downstream cells
while preserving the explicit navigation/QC decisions.

`tests/notebook_smoke.py` now runs the actual detailed cells and guided runner
in isolated kernels, including a deliberately module-contaminated PATH, all
three existing participants, report generation and Neurosynth decoding. Both
completed without errors and their reopen checks submitted no new jobs. Cached
processing/comparison cells took about 0.01 seconds; report plus decoding
reopened in about four seconds on this workspace. The four browser fixtures
(workflow, review, results, disconnectome) passed in job 52. Original saved
notebook errors and pre-fix notebooks are preserved under
`notes/notebook-regression-20261008/`; only obsolete error outputs were cleared
from the working notebooks. Existing image products and QC ratings were kept.

The October 8 imaging record below remains separate from these notebook checks.

Implemented in the current workflow:

- Guided inputs and stable notebook metadata IDs (no source comments), with checkpoints that allow upstream cells to rerun.
- A separate single-subject participant selector, defaulting to an unprocessed case when available.
- Participant-local QC drafts, save/next navigation, saved-QC reuse that continues after QC, and explicit skip notices.
- One native automatic/manual mask comparison and one lesion/disconnectome comparison. Model changes preserve the selected method and image position.
- Consistent mask-origin colours, deferred image loading, and title-based cell timings.
- One atlas results preview with shared selectors and collapsed optional group summaries.
- One canvas for cached or new reference-scan coregistration and lesion-mask review, with development voxel-count output removed.
- Batch timings by step and participant, cached/failed/missing outcomes, and participant totals.
- A single-subject checkpoint shortcut to report setup, retaining saved QC and stopping at report selection. Generating a report prepares missing selected-participant overlap tables.
- Full-cohort atlas selectors, explicit zero/missing status, subject/session cache keys, changed-mask invalidation, and measured overlap laterality.
- Integrated report selection, export and Neurosynth decoding with visible completion/failure status.

The current configured cohort is sub-M2001/ses-1076, sub-M2075/ses-602 and
sub-M2077/ses-250. Processing state depends on the local outputs.
The September 30 verification used sub-M2066/ses-235, sub-M2075/ses-602 and
sub-M2176/ses-1237, refreshed overlap tables for those participants and exercised
cached Neurosynth decoding; see `analyses/workflow-validation/astra.yaml`. Browser
fixtures exercised model switching, layer reuse and preserved slice position.
These checks do not certify scientific QC or a fresh end-to-end processing run.

October 8 verification:

- October 8: `GetEnvTimeout=0` is active and five launch probes passed, including
  export NONE and selective export. Dependencies were restored through job 6;
  `pip check` passed. The workflow browser fixture and the review, report,
  group-map and disconnectome browser checks passed using disposable notebooks.
- The expanded Python suite passed 158 tests and 20 subtests. Browser jobs 17
  and 27 passed review, results, group-map and disconnectome fixtures; the
  separate workflow navigation fixture also passed.
- Current uncommitted fixes separate QC/navigation messages, isolate relative
  and symlinked QC repair paths, validate staged MNI warps, check cache input
  and output identities, preserve replaced products, honor configured
  derivative folders/segmentation flags, and check scheduler logs and receipts.
- Tractotron output, native comparison scores and outlines, nested QC default
  work directories, artifact-v2 LINDA wrapper resolution and container thread
  limits are implemented. The undefined historical dipy fallback is replaced
  with an explicit failure that retains diagnostics.
- Atlas acquisition, overlap, group maps, comparison metrics/figures, report
  overlays and Neurosynth decoding now run through retained reporting jobs.
  Historical shared overlap tables are preserved; reports use the newly
  selected tables. The three-participant inspection also writes agreement scores.

- Fresh sub-M2077/ses-250 completed HD-BET (7), LINDA (11), SynthStroke (19),
  manual registration (20), all twelve DeepDisco maps (22), three BCB maps and
  three 64-tract Tractotron runs (31). Atlas acquisition (14), overlap (23),
  Neurosynth decoding (25), report preview (26) and final inspection (32)
  completed with exit 0:0. Failed attempts and superseded dependencies are
  retained in the job history, not counted as successful stages.
- Tractotron now uses the atlas's actual 1 mm grid rather than the incorrect
  2 mm assumption in module help. Its helper keeps the parent host Python
  instead of selecting FSL's container wrapper. See docs/SETUP.md for the bundled
  CLI's binary `probability.csv` limitation.
- All 69 inspected images were finite and nonempty; all disconnectome ranges
  were within [0,1]. Six contact sheets and selected full-size images were
  reviewed, including registered T2 edges on T1. This is sampled visual QC,
  not full-volume or clinical validation. Existing saved ratings were preserved.
- Native Dice against registered manual masks (LINDA / SynthStroke): M2001
  0.6660 / 0.7402; M2075 0.3587 / 0.7600; M2077 0.6087 / 0.7851.
  M2075 LINDA has 103.519 mL versus 25.448 mL manual and warrants review.
  M2077 LINDA has separate small regions visible in the sampled slices.
  These are QC flags, not automatic edits or accepted masks. The older two
  participants remain legacy outputs with incompletely established model
  identity; do not infer a cohort-wide model ranking from these numbers.
- `analyses/workflow-acceptance/astra.yaml` validates with three evidence-backed
  findings, and all 12 declared outputs pass the provenance check. Execution
  used plain sbatch and sidecars; no recognised ASTRA run manifest was created.
  Evidence: `notes/interpretation-update-20261008-ARaRpr/`; images and numerical
  results: `analyses/workflow-acceptance/inspection/`.

Further work:

- Adjudicate the flagged LINDA masks through the existing participant QC flow.
- Non-default SynthStroke baseline fallback / operation without an HD-BET
  mask is not supported by the retained stage; this run used synth-plus and
  HD-BET throughout. Uncached AAL mirror fallback also remains outside this
  acceptance run. Do not treat tested defaults as coverage of these paths.
- Continue separating optional diagnostics from the essential processing/QC/report workflow while preserving distinct scientific checks.
- Cross-reference #5 when extending cache invalidation to other scientific outputs; a working selector alone does not establish that all cached results are current.

Keep masks, ratings, manual edits, existing scientific decisions and run
provenance intact during follow-up work. Use panel titles and stable cell IDs
when referring to steps, since notebook cell positions change during cleanup.
