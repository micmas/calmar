# Setting up aphasia-lesion-pipeline on a new machine

This is a step-by-step for getting the notebook + KB workflow running
on a second Mac with Neurodesk installed (the typical scenario:
syncing your work between two computers via a git remote).

> **Note on the local folder name.** The GitHub repo is
> `aphasia-lesion-pipeline`. Throughout this doc we use the same name
> for the local folder under `~/neurodesktop-storage/`. If you have an
> older folder called `LINDA-STUFF` from earlier work on the primary
> machine, you can rename it once with
> `mv ~/neurodesktop-storage/LINDA-STUFF ~/neurodesktop-storage/aphasia-lesion-pipeline`
> (the code uses relative paths, so nothing else needs to change).

## Pre-flight (once per machine)

1. Install Neurodesktop on the new Mac following the official
   instructions: https://www.neurodesk.org/docs/getting-started/neurodesktop/macos/
   The Docker image bundles LINDA, HD-BET, FSL, FreeSurfer, ANTs, etc.
2. Make sure git is installed (it ships with macOS Command Line Tools).

## Cloning the repo

```bash
cd ~/neurodesktop-storage          # the persistent storage Neurodesk mounts
git clone <YOUR_REMOTE_URL> aphasia-lesion-pipeline
cd aphasia-lesion-pipeline
```

`<YOUR_REMOTE_URL>` is the GitHub / GitLab / Bitbucket URL you set up
on the primary machine (see "Pushing from machine A" below).

## Re-installing the dataset (datalad)

The raw dataset is *not* tracked in git. On each machine you reinstall
it from OpenNeuro via datalad. From inside `aphasia-lesion-pipeline/`:

```bash
datalad install -d . https://github.com/OpenNeuroDatasets/ds004884.git
cd ds004884 && git checkout 1.0.2 && cd ..
```

Or just run the notebook's data-preparation cell — it does the same
thing automatically (`CONFIG["DATASET_SOURCE"] = "openneuro"`).

## First run

Open the notebook in Neurodesktop (Jupyter) and run the cells **in
order**:

1. **Load LINDA** (`module.load('linda/0.5.1')`).
2. **Load brain extractor** — `module.load('hd-bet/1.0.0')`. Required
   because the segmentation pipeline now uses HD-BET preprocessing by
   default. If you skip this, the segmentation cell will refuse to run
   with a clear message.
3. **Imports**.
4. **CONFIG** — review the values; they should already match what's
   in the repo. Defaults: `USE_HDBET_PREPROCESSING = True`,
   `HDBET_PADDING_MM = 8.0`, `HDBET_MODE = "fast"`.
5. **Atlases** — fetch on first run (cached under `atlases/`).
6. **Data preparation** — `datalad install` + symlink anatomicals.
7. **Run LINDA on every discovered T1w** — this re-creates the
   derivatives on the new machine. A few minutes per subject on CPU.
8. **QC review** — your existing `*.qc.json` sidecars are in the
   repo, so the QC widget will load with your prior ratings and edit
   history. The startup banner will offer to clear them if you want
   to start fresh on the new machine's freshly-derived outputs.

## Aphasia knowledge base

Same idea: code + KB markdown files travel via git. Source paper PDFs
in `aphasia-kb/papers/` are *not* tracked (potential copyright +
size); keep them locally per machine, or use a separate cloud sync if
you want them on both machines.

To verify the KB loads cleanly:

```bash
cd aphasia-kb
python aphasia_kb.py
```

Expected output: "Knowledge base @ … regions: N impairments: M
therapies: K findings: X drafts: Y issues: 0".

## Pushing from machine A (one-time, after `git init`)

The repo lives in your personal GitHub account (`micmas`), not in any
Neurodesk-affiliated org.

1. On github.com (logged in as `micmas`), create a new **private** repo
   (recommended; you can flip to public later). Suggested name:
   `aphasia-lesion-pipeline`. **Do not** let GitHub add a
   README, license, or .gitignore — we already have those locally.
2. From the primary machine, set the remote and push:
   ```bash
   cd ~/neurodesktop-storage/aphasia-lesion-pipeline
   git remote add origin git@github.com:micmas/aphasia-lesion-pipeline.git
   # or, if you use HTTPS instead of SSH:
   # git remote add origin https://github.com/micmas/aphasia-lesion-pipeline.git
   git branch -M main
   git push -u origin main
   ```
3. On machine B, clone with:
   ```bash
   cd ~/neurodesktop-storage
   git clone git@github.com:micmas/aphasia-lesion-pipeline.git aphasia-lesion-pipeline
   ```

## Day-to-day sync

On the machine you've been working on:

```bash
cd ~/neurodesktop-storage/aphasia-lesion-pipeline
git status                          # see what changed
git add -A                          # stage everything tracked
git commit -m "QC ratings for sub-M2040..M2049"
git push
```

On the other machine:

```bash
cd ~/neurodesktop-storage/aphasia-lesion-pipeline
git pull
```

## What syncs vs what doesn't

| Item                                          | Syncs via git? | How to recreate                              |
|-----------------------------------------------|----------------|----------------------------------------------|
| `lesion-interpretation-pipeline.ipynb`        | ✅             | n/a                                          |
| `linda_qc.py`                                 | ✅             | n/a                                          |
| `aphasia-kb/` (code, KB, drafts, examples)    | ✅             | n/a                                          |
| `*.qc.json` sidecars                          | ✅             | n/a                                          |
| `qc_summary.csv`                              | ✅             | regenerated by QC summary cell               |
| `README.md`, `QC_RUBRIC.md`, `SETUP.md`       | ✅             | n/a                                          |
| `requirements.txt`, `.gitignore`              | ✅             | n/a                                          |
| `ds004884/` (raw OpenNeuro)                   | ❌             | `datalad install …` (~1 GB)                  |
| `ds004884_anat/sub-*/anat/*_T1w.nii.gz`       | ❌             | re-symlinked by data-prep cell               |
| `ds004884_anat/derivatives/.../linda/*.nii.gz`| ❌             | re-run segmentation cell                     |
| `ds004884_anat/derivatives/.../_linda_original/`| ❌           | regenerated when re-running through HD-BET   |
| `_hdbet_work/`                                | ❌             | regenerated each run (intermediate)          |
| `atlases/`                                    | ❌             | `nilearn` re-downloads (~500 MB)             |
| `aphasia-kb/papers/*.pdf`                     | ❌             | manual copy or separate cloud sync           |

## Manual edits to lesion masks

If you've used the deterministic-ops or paint tools to manually edit a
mask on machine A, those edits are stored in two places:

  - The *edited mask file* (`Lesion_in_MNI.nii.gz`) on disk — **NOT in
    git** because it's a binary derivative.
  - The *edit log* in the QC sidecar's `edits[]` list — **IS in git**.

When machine B re-runs the segmentation, it'll produce a fresh
unedited mask. The sidecar's edit log tells you which operations were
applied previously, but doesn't auto-replay them. If you want the
edits to also travel, you have two options:

  - **Replay manually** on machine B using the same Tier-1 deterministic
    ops with the same parameters (the log records them).
  - **Sync the edited masks separately** — e.g. add specific
    `Lesion_in_MNI.nii.gz` paths to a non-tracked sync folder, or use
    `git lfs` for those files.

For most cases, replay-from-log on machine B is fine and gives you
audit clarity.
