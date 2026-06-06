# Changelog

All notable changes to CALMaR are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.0.0] – 2025-06-06 — Initial public release

### Pipeline

- **HD-BET** skull stripping with fallback to SynthStrip (FSL)
- **LINDA** lesion segmentation (R, via container); skip logic prevents re-running completed subjects
- **SynthStroke** lesion segmentation with configurable TTA and per-subject timeout
- **BCBToolkit** disconnectome analysis (Disconnectome.nii.gz + Tractotron probability maps)
- Batch processing for all three segmentation pipelines with per-subject skip/overwrite logic
- Warp SynthStroke output to MNI space using LINDA's own affine transform
- Warp expert/manual lesion masks to MNI space using LINDA's affine + CoM offset
- Derivatives inventory: cross-session discovery that finds completed subjects and extends the working subject list

### Quality control

- Interactive QC dashboard with NiiVue viewers per subject and pipeline stage
- Stage-aware QC ratings (acute / subacute / chronic) with per-edit audit log
- HD-BET re-run cell for failed skull strips
- Manual mask editing round-trip (ITK-SNAP / FSLeyes via `qc_edits/`)
- QC sidecar JSON files (`Lesion_in_MNI.qc.json`) with full edit provenance

### Results & visualisation

- Group lesion frequency map in MNI space with glass-brain NiiVue viewer
- Atlas overlap computation (HarvardOxford, AAL, Destrieux, Schaefer400, JHU) with per-subject skip logic
- Configurable mask source for atlas overlap: LINDA, expert, SynthStroke, or all three
- Interactive per-subject atlas overlap plots (bar chart + cross-subject heatmap)
- Schaefer 7-network summary bar chart
- Interactive per-subject report with NiiVue lesion viewer
- Comparison viewer: LINDA vs expert mask in MNI space with side-by-side NiiVue display

### Clinical interpretation

- KB-driven interpretation cell: predicted impairments from lesion location (five atlases), predictor-driven outcome predictions from WAB-AQ / age / lesion volume / sex, evidence-based therapy recommendations with RTSS ingredient badges
- Post-onset stage classification (acute / subacute / chronic) with stage-mismatch warnings on therapy evidence
- WAB type → impairment decomposition (fluency / comprehension / repetition)
- HTML report with Save / Print PDF button; standalone file saved to `reports/`
- Neurosynth lesion decoding against language/cognitive term maps with HarvardOxford atlas overlap

### Aphasia knowledge base (`aphasia-kb/`)

- YAML/Markdown KB with findings, citations, RTSS ingredients, sample population metadata
- Draft → review → promote workflow (`promote.py`)
- RAG interface (`aphasia_kb_rag.py`) for natural-language KB queries
- LLM-assisted paper extraction (`extract.py`, `EXTRACTION_SKILL.md`)

### Infrastructure

- Fully BIDS-compatible derivatives layout (`sub-*/ses-*/anat/`)
- datalad integration for OpenNeuro dataset fetching
- `Path.cwd()`-relative CONFIG — no hardcoded paths
- GitHub-based sync between Neurodesktop Play and local machines
