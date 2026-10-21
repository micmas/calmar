---
schema_version: 2.3
id: left_ifg_pars_triangularis
name: Left Inferior Frontal Gyrus Pars Triangularis
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
hemisphere: left
findings:
- id: f1
  target: verbal_quality
  target_kind: impairment
  claim: Damage to the left inferior frontal gyrus pars triangularis is associated with reduced verbal
    quality in connected speech.
  direction: likely
  relationship: causal
  citation: '@Alyahya2020'
  method: VBCM
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 46
    population: chronic left-hemisphere stroke
    time_post_onset: 4-12 months
    age_range: mean 63.21 (SD 11.93)
    handedness: right-handed
    language: English
    phase: mixed
  statistics:
    threshold: P = 0.001 voxel-level, FWE P = 0.05 cluster-level
    effect_size: not_reported
  confounders_controlled:
  - age
  - education
  - time since stroke onset
  confounders_not_controlled: []
  region_definition:
    kind: atlas
    atlas: Harvard-Oxford
    description: Inferior frontal gyrus (pars triangularis)
  imaging_details:
    field_strength: 3.0 T
    reference_space: not_reported
    atlases_used:
    - Harvard-Oxford
    preprocessing_pipeline: SPM8
  author_limitations:
  - White matter tracts were descriptive based on atlas overlap rather than directly measured via DWI.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results
    confidence: high
    flags:
    - target verbal_quality is a new impairment ID
    - imaging_details.reference_space not extracted by the model — set to not_reported; verify against
      the paper
  source_passages:
  - section: Results
    page: 8
    quote: the 'verbal quality' component showed neural correlates across left frontal regions, including
      the inferior frontal gyrus (pars opercularis and pars triangularis)
    supports: claim
  - section: Materials and methods
    page: 4
    quote: The unified PCA model was mapped onto brain lesions using a voxel-based correlational methodology
      (VBCM) (Tyler et al., 2005).
    supports: method
  - section: Discussion
    page: 12
    quote: it must be acknowledged that white matter tracts described in this study are descriptive...
      rather than directly measured using diffusion-weighted imaging.
    supports: limitation
---
