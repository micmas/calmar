# How processing runs: Slurm jobs, caching and validation

The notebooks do not run imaging tools in the kernel. Every heavy step
is submitted as a Slurm job through a retained script in `src/`, and
its outputs are published atomically with provenance. This page is for
anyone debugging a job, re-running a step or validating a checkout.
The scientific records of individual analyses are the `astra.yaml`
files listed in [REPOSITORY_LAYOUT.md](REPOSITORY_LAYOUT.md).

## Submissions

The detailed and guided notebooks submit acquisition, segmentation,
manual-mask registration, disconnectomes and explicit QC repairs through
retained Slurm scripts (`src/analysis_*.sh`, implementations under
`src/python/` and `src/r/`). Each request gets a unique directory under
`reports/jobs/`, including its job ID, stdout/stderr, output receipt and
provenance. Completion requires terminal accounting, fresh logs and a
matching publication receipt. Keep these records when reporting a failed
job; a timeout does not cancel it automatically.

Submit from the repository root and create `logs/` first. Standalone
scripts resolve `PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"` and must not
infer a submission directory from a spool copy's filename. `calmar.qc`
resolves repository resources relative to its installed source location
and passes `CALMAR_SOURCE_DIR` to the wrappers. Follow `AGENTS.md` for
module initialisation, Slurm submission, validation and provenance.

The notebook keeps its own Python environment; tools load only inside
their jobs. Every submission explicitly passes the kernel's Python
interpreter, so a previously loaded FSL/container wrapper cannot replace
it. Setup checks installed dependencies and the local TLS context
without probing package servers or installing system packages.
Neurodesk's artifact-v2 LINDA wrappers are supported; explicit
environment exports carry CPU allocation limits into containers that
use `--cleanenv`. Keep the project module pins unless intentionally
changing the analysis. Logs from temporary attempts are retained under
`logs/processing_attempts/`, including nested tool diagnostics and
partial output after timeouts.

## Reporting computations

Atlas preparation, overlap, group frequency maps, mask agreement,
comparison figures, report overlays and Neurosynth decoding use
`src/analysis_35_reporting.sh`. Report generation reads its selected
participant's published overlap tables and preserves historical shared
CSVs. The native-mask viewer reads prepared scores and outlines.
Changing a display layer never starts registration or segmentation.

## Caching and reuse

Completed steps and report computations are reused across reruns and
kernel restarts while their requests and input/output file identities
stay unchanged. Reopening a view does not submit another job.
Image-product checks compare scientific inputs, parameters, pinned
module options and output hashes; unrelated UI/logging edits or CPU
directives do not invalidate images. When changing an algorithm,
increment its entry in `calmar.processing.ALGORITHM_VERSIONS`. Original
provenance records are retained. Existing results without a cache
identity remain explicitly labelled legacy caches; known stale results
are preserved and require deliberate replacement, with backups.

## Lightweight tests

```bash
python -m pip install -r requirements.txt
python -m pytest -q tests
```

These tests exercise discovery, imports, widget callbacks and script
dispatch without launching imaging jobs or downloads. They do not
replace the three-participant end-to-end run or browser QC. Optional
browser checks need Playwright (the commented line in `requirements.txt`) and
`python -m playwright install chromium`.

## Validating a checkout

The retained `src/analysis_19_verify_interpretation.sh` verifies overlap
laterality and cached Neurosynth decoding on existing outputs through
Slurm; `analyses/workflow-validation/astra.yaml` records its inputs and
verification scope.

To validate the software and browser fixtures using an owned Jupyter
server:

```bash
mkdir -p logs
sbatch --export=ALL src/analysis_34_validate_workflow.sh notes/my-validation-attempt
```

The browser suite uses disposable notebooks and includes a small
group-map job. It does not establish scientific mask quality.
Fresh-cohort inspection uses `src/analysis_32_inspect_acceptance.sh`;
review the PNGs and agreement metrics before recording findings in
`analyses/workflow-acceptance/astra.yaml`.

The real notebook-cell smoke check (requires the existing acceptance
cohort) uses an isolated kernel, deliberately loads FSL first to
exercise PATH contamination, and forbids inference while checking
existing products:

```bash
python tests/notebook_smoke.py --artifacts notes/notebook-smoke
python tests/notebook_smoke.py --guided --artifacts notes/guided-smoke
```

It exercises setup through HTML reporting/decoding and asserts that
reopening unchanged results creates no new jobs. The browser suite
separately exercises the workflow buttons, QC preservation and viewer
controls.

## Known issues

Write-ups of problems met in the Neurodesk environment and how they were
resolved are in [issues/](issues/).
