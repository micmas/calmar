# CALMaR — Co-designed, Automated Lesion Mapping and Reporting

CALMaR is an open-source Jupyter notebook pipeline for automated stroke lesion segmentation, quality control, and clinician-facing interpretation of structural brain MRI data. It is designed to run inside [Neurodesktop](https://www.neurodesk.org/), a browser-accessible neuroimaging environment that provides all required tools pre-installed.

Given a BIDS-formatted dataset, CALMaR will:

1. **Segment lesions** using HD-BET + LINDA, SynthStroke, and optionally BCBToolkit
2. **QC every mask** with an interactive dashboard, stage-aware rubric, and edit audit trail
3. **Analyse regional overlap** against five atlases (HarvardOxford, AAL, Destrieux, Schaefer400, JHU)
4. **Decode the lesion** against Neurosynth v7 meta-analytic language/cognitive maps
5. **Interpret clinically** using an aphasia knowledge base: predicted impairments, WAB-driven outcome predictions, and evidence-based therapy recommendations with stage-mismatch warnings

---

## Requirements

- [Neurodesktop](https://www.neurodesk.org/) (Play or local) — provides LINDA, HD-BET, SynthStroke, BCBToolkit, and all Python/R dependencies
- A BIDS-formatted dataset (the notebook fetches `ds004884` from OpenNeuro via datalad by default)
- Python packages listed in `requirements.txt` (pre-installed in Neurodesktop; run the pip cell in the notebook if anything is missing)

---

## Repository layout

| Path | Purpose |
|------|---------|
| `lesion-interpretation-pipeline.ipynb` | Main pipeline notebook — run this |
| `linda_qc.py` | Helper module for QC, mask edits, coregistration, and sidecars |
| `QC_RUBRIC.md` | Stage-aware QC rating reference (acute / subacute / chronic) |
| `lesion-segmentation-benchmark.ipynb` | Benchmarks LINDA / SynthStroke across chronic and acute datasets |
| `aphasia-kb/` | Aphasia literature knowledge base (see `aphasia-kb/README.md`) |
| `container/` | Docker/Singularity wrappers for containerised tool calls |
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
# File → Open → lesion-interpretation-pipeline.ipynb

# 4. Run cells top to bottom, or jump to any section
# Each section has a config block at the top — edit those, then run the cell
```

The notebook uses `Path.cwd()` for all paths — no path editing required as long as you open it from the repo root.

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
            ├─ BCBToolkit disconnectome + Tractotron
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
