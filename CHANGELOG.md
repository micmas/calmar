# Changelog

All notable changes to CALMaR are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

### Knowledge base moved to its own repository

- The aphasia knowledge base now lives at
  [micmas/stroke-aphasia-kb](https://github.com/micmas/stroke-aphasia-kb)
  (moved from `aphasia-kb/` with its git history, October 2026). CALMaR
  consumes it as the git submodule `stroke-aphasia-kb/`, pinned to one KB
  commit; clone with `--recurse-submodules`. Entries and KB scripts are
  edited and reviewed in that repository; CALMaR commits only the pointer.
  The CALMaR webapp (neurodesk/webapps) ships an export of the same
  repository.

### Knowledge base: local models, review governance, audit tooling

- **Merged `ollama-local-models`**: extraction, the review second
  opinion and the RAG narrative run on a local Ollama model; the
  Anthropic-API path and `anthropic` dependency are gone. Model per role
  in `stroke-aphasia-kb/models.yaml`; `stroke-aphasia-kb/MODELS.md` documents how to
  choose and benchmark one (`compare_extraction.py`).
- **Review governance** (`stroke-aphasia-kb/GOVERNANCE.md`, schema v2.5):
  deterministic checks can reject or defer but never approve
  (`auto_review.py --all` now yields `checks_passed`, not
  `auto_approve`); drafts are classified into Tier A (an independent
  model may approve after re-reading the PDF) or Tier B (a person
  must); the model reviewer gets the paper's text layer and answers
  seven per-finding checks under a constrained schema; approvals are
  stamped `human:<name>`/`model:<tag>` with `review_tier` and a
  per-finding `review` block; log lines `MODEL-APPROVED` and `AUDIT`;
  `--allow-local-override` deprecated; `AUTO-APPROVED` path removed.
- `promote.py`: normalises reviewers, refuses `auto-reviewer`, a model
  on Tier B, or a model reviewing its own extraction; `--tier`,
  `--extractor`.
- `aphasia_kb.py`: `reviewer_kind()`, `review_kind`/`reviewer`/
  `review_tier` columns in the findings table,
  `KnowledgeBase(review_kinds=("human",))` for the clinical path.
- `aphasia_kb_rag.py --human-approved-only`; reports mark
  model-approved and pre-policy findings inline.
- New `kb_status.py` (counts, review provenance, decoder reachability,
  `--papers-needed`, `--tag-legacy`) and `audit_quotes.py` (every
  canonical quote checked against its PDF).
- 33 pre-policy entries stamped `review_tier: legacy` (GOVERNANCE.md §5).
- `extract.py --pick-model` lists all pulled models, not only Gemma.
- `test_review_guardrails.py` covers tiers, independence and promote
  policy; `docs/CALMAR_PALETTE.md` + `calmar_palette.json` document the
  project palette.

### Interactive-widget performance & UX overhaul

- **New `calmar_widgets.py` helper module** shared by all viewer cells:
  - Persistent NiiVue viewer registry — widget callbacks now swap volumes on
    one existing viewer instead of creating a new WebGL canvas per change.
    Fixes viewers going blank mid-session (browsers cap live WebGL contexts
    at ~16 and silently destroy the oldest) and the gradual front-end
    slowdown from leaked widget models.
  - Volumes load by **URL from the Jupyter file server** (browser-fetched and
    browser-cached) instead of shipping file bytes through the kernel
    websocket on every render. The per-user URL prefix is auto-detected
    (`JUPYTERHUB_SERVICE_PREFIX`), configurable via
    `CONFIG["NIIVUE_URL_BASE"]`; an mtime cache-buster keeps regenerated
    masks fresh. Files outside the server root fall back to bytes.
  - mtime-cached voxel counts for the diagnostic tables.
- **QC dashboard** rebuilt as a build-once UI (was `widgets.interact`, which
  recreated the whole panel — viewer included — on every slider/stage/toggle
  change). Added a **Save & next** button for faster rating runs.
- **BCB vs DeepDisco comparison**: agreement metrics and the resample to the
  BCB grid are cached by file mtimes; glass brains render once to cached
  PNGs and default to off (with a progress hint on first render).
- **Atlas-overlap plots**: only the visible tab redraws on a control change
  (the cross-subject heatmap was re-rendered even while hidden); subject
  selection is preserved when switching atlas/mask, here and in the
  per-subject report.
- Group-map MNI template cached under `atlases/` instead of a tempfile.

### Fixed

- `aphasia_kb.interpret_predictors`: instrument aggregation is now NaN- and
  whitespace-safe.

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

### Aphasia knowledge base (`aphasia-kb/`, since October 2026 the separate repository micmas/stroke-aphasia-kb)

- YAML/Markdown KB with findings, citations, RTSS ingredients, sample population metadata
- Draft → review → promote workflow (`promote.py`)
- RAG interface (`aphasia_kb_rag.py`) for natural-language KB queries
- LLM-assisted paper extraction (`extract.py`, `EXTRACTION_SKILL.md`)

### Infrastructure

- Fully BIDS-compatible derivatives layout (`sub-*/ses-*/anat/`)
- datalad integration for OpenNeuro dataset fetching
- `Path.cwd()`-relative CONFIG — no hardcoded paths
- GitHub-based sync between Neurodesktop Play and local machines
