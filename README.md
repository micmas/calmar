# LINDA stuff

Working folder for LINDA-based lesion segmentation, QC, and a parallel
literature knowledge base for clinical interpretation.

## What lives here

| Path                                     | Purpose                                                                 |
|------------------------------------------|-------------------------------------------------------------------------|
| `linda-example.ipynb`                    | Main working notebook. Source of truth — edit it directly.              |
| `linda-example.original-20260421.ipynb`  | Immutable seed (template author's original). Don't modify.              |
| `linda_qc.py`                            | Helper module imported by the notebook (QC, fixes, HD-BET, sidecars).   |
| `QC_RUBRIC.md`                           | Reference rubric for stage-aware mask QC.                               |
| `aphasia-kb/`                            | Aphasia literature knowledge base (separate provenance regime — see below). |
| `qc_edits/`                              | Round-trip folder for ITK-SNAP / FSLeyes edits.                         |
| `ds004884/`                              | Demo OpenNeuro dataset (datalad-installed).                             |
| `ds004884_anat/`                         | Anatomicals + LINDA derivatives for ds004884.                           |
| `atlases/`                               | Cached HarvardOxford / AAL / Destrieux / Schaefer400 atlases.           |
| `anat_inputs/`                           | Leftover from an early build attempt — safe to delete if unused.        |

## Two kinds of provenance

This folder has **two distinct provenance regimes**, deliberately separated:

### 1. Notebook iteration (light) — engineering work

The notebook is a research artifact iteratively developed with an agent.
Treat it like ordinary code: edit it directly, use git for change
tracking, keep `linda-example.original-20260421.ipynb` around as a
known-good restore point. No build pipeline, no SHA hashes, no
ceremonial change logs needed.

If you're not using git here, the simplest safety net is a local copy of
the notebook before any risky session — that's the same protection a
build pipeline gave you, with none of the overhead.

### 2. QC + knowledge-base claims (heavy) — epistemic work

These earn full provenance because each one is a *claim about reality*
that downstream conclusions depend on.

* **QC sidecars** (`<lesion>.qc.json`): per-stage rating, tags,
  reviewer, reviewed_on, plus a per-edit log of every modification
  (threshold X → morph Y → paint Z). Originals are preserved in
  `_linda_original/`. See `QC_RUBRIC.md` for the rating definitions.
* **Aphasia knowledge base** (`aphasia-kb/`): every finding has a
  citation, a method, a sample, statistics, confounders, and an
  extraction provenance block. Drafts go through `promote.py` review
  before becoming canonical. See `aphasia-kb/README.md`.

## Recommended workflow

1. Open `linda-example.ipynb`. Edit cells directly.
2. For changes to `linda_qc.py`, edit and save — the notebook cells
   reload it automatically (`importlib.reload(q)` is wired in).
3. When you ask an agent to extract from a paper, point it at
   `aphasia-kb/EXTRACTION_SKILL.md`. The agent writes to
   `aphasia-kb/drafts/`; you review with `python aphasia-kb/promote.py
   --list`.
4. For change history of the notebook itself, use git:
   ```bash
   cd LINDA-STUFF
   git init                                          # first time
   git add linda-example.ipynb linda_qc.py QC_RUBRIC.md README.md
   git commit -m "WIP: stage-aware QC"
   ```
   Or just keep a manual copy before risky changes.
