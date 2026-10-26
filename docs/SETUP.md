# Setting up CALMaR

## Install

CALMaR runs inside [Neurodesktop](https://www.neurodesk.org/) (Play or
local), which provides the neuroimaging tools that the Slurm scripts in
`src/` load with pinned `module load` versions: LINDA, HD-BET,
SynthStrip, SynthStroke, BCBToolkit, DeepDisco, DeepWMH, SynthSeg, ANTs,
FSL, FreeSurfer, OpenADS, QSIPrep and QSIRecon. Clone
into persistent Neurodesktop storage and open the notebooks from the
repository root:

```bash
cd ~/neurodesktop-storage
git clone --recurse-submodules https://github.com/micmas/calmar.git
cd calmar
```

`--recurse-submodules` also fetches the aphasia knowledge base, a
separate repository
([micmas/stroke-aphasia-kb](https://github.com/micmas/stroke-aphasia-kb))
pinned here as the submodule `stroke-aphasia-kb/`. In a checkout cloned
without it, run `git submodule update --init`.

Python helpers live in the local `calmar/` package; no editable install
is needed. Python dependencies are in `requirements.txt` (mostly
pre-installed in Neurodesktop; the notebook's Setup cell installs what
is missing with `pip install --user` and prints instructions for
anything it cannot install). Contributors running the test suite also
install `requirements-dev.txt`. The notebook loads explicit module
versions; follow its setup sequence rather than inferring a tool
version from an older notebook's outputs.

Keep `nilearn<0.14` in this Neurodesk environment: Nilearn 0.14 requires
`packaging>=26`, while the installed Snakemake requires `packaging<26`.
The September 29 setup repair verified imports with Nilearn 0.13.1,
ipylab 1.0.0, SimpleITK 2.5.6 and packaging 25.0. The continuation
buttons need `ipylab==1.0.0` and `anywidget`; after installing them,
reload JupyterLab (restart the server if the ipylab frontend is still
not registered).

Then open `calmar-guided.ipynb` (form-based) or
`lesion-interpretation-pipeline.ipynb` (detailed), run Setup, and wait
for **CALMaR setup imports completed.** How the notebooks behave from
there is in [NOTEBOOK_GUIDE.md](NOTEBOOK_GUIDE.md).

Optional inputs: a FreeSurfer licence at `~/license.txt` or in
`FS_LICENSE` for the QSIRecon route, and a local copy of ISLES 2022 for
the acute DWI route (see the notebook guide).

## Updating an existing checkout

Preserve local edits before updating. After pulling a change to the
repository layout, restart the notebook kernel and rerun Setup: live
viewer state cannot safely be mixed across layouts. Pulling CALMaR does
not move the submodule by itself; use `git pull --recurse-submodules`
(or `git submodule update` after a pull).

`main` contains the whole workflow. The `ollama-local-models` branch,
which added local-model KB extraction and review, was merged; it had
its history rebased in September 2026, so preserve local work before
synchronising a checkout that still has the old history.

## The knowledge base

`stroke-aphasia-kb/` is a git submodule checkout of
[micmas/stroke-aphasia-kb](https://github.com/micmas/stroke-aphasia-kb)
at the commit CALMaR was last tested with (`git submodule status` shows
which). CALMaR's report code imports the KB's modules from
`stroke-aphasia-kb/scripts/` through `calmar/kb_paths.py`. Its commands
run from the CALMaR root, for example:

```bash
python stroke-aphasia-kb/scripts/kb_status.py
```

Edits to KB entries or scripts are commits in the KB repository, not in
CALMaR: commit and push inside `stroke-aphasia-kb/` (it is a full
clone), then `git add stroke-aphasia-kb && git commit` here so CALMaR
records the new commit. `git submodule update --remote stroke-aphasia-kb`
moves the checkout to the KB's latest `main`. Source PDFs under
`stroke-aphasia-kb/papers/` are local files, never committed. See the
KB's [README](../stroke-aphasia-kb/README.md) and
[docs/HOWTO.md](../stroke-aphasia-kb/docs/HOWTO.md) for extraction and
review.

## What travels through Git

| Content | In Git? |
|---|---|
| Notebooks, `calmar/`, retained source scripts, tests, documentation | Yes, when committed |
| KB code, curated entries and tracked review records | Yes, in the KB repository; CALMaR tracks only the submodule commit |
| Datasets and derivatives under `data/` | No |
| QC sidecars stored alongside those derivatives | No |
| Reports, QC summaries, cached atlases and `qc_edits/` | No |
| Source paper PDFs and generated Neurosynth caches | No |
| Local handoffs, recovery snapshots and cleanup archives under `notes/` | No |

Copy scientific results, ratings, manual edits and provenance
separately when moving machines. Re-running segmentation does not
restore a manually edited mask or its QC history; preserve the mask and
its sidecar together, since edit logs do not automatically replay
edits. Review `git status` and stage intended source paths explicitly
when sharing changes: an untracked analysis script or specification can
still be important unfinished work.

## Checking the install

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q tests
```

No imaging jobs or downloads are run. Heavier validation (Slurm
verification, browser suite, notebook smoke test) is described in
[RUNNING_JOBS.md](RUNNING_JOBS.md).
