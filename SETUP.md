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

1. Open `lesion-interpretation-pipeline.ipynb` from this checkout.
2. Complete Setup and confirm “CALMaR setup imports completed.”
3. Review Configuration. It currently selects two fresh verification
   participants; choose your intended cohort deliberately.
4. Run dataset discovery/acquisition and inspect the selected subject/session
   pairs. The default dataset is OpenNeuro ds004884, pinned to tag 1.0.2,
   under `data/ds004884/`. Missing content is fetched through DataLad.
5. Follow the single-subject test, then the batch workflow. The notebook
   deliberately stops at the test→batch boundary.
6. At the QC dashboard, execution stops so you can inspect and save ratings.
   Run repair cells only as needed, recheck affected masks, and continue manually.
7. Choose the subject and MNI lesion mask at the report-selection checkpoint
   before generating interpretation outputs.

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
python -m unittest discover -s tests -v
```

These tests exercise discovery, imports, widget callbacks, and script dispatch
without launching imaging jobs. They do not replace the two-participant
end-to-end run or browser QC.
