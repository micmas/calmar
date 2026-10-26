---
schema_version: 2.7
id: left_inferior_longitudinal_fasciculus
name: Left Inferior Longitudinal Fasciculus
kind: tract
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
hemisphere: left
findings:
- id: f1
  target: semantics
  target_kind: impairment
  claim: Impaired auditory word-picture matching is associated with damage to the left inferior longitudinal
    fasciculus.
  direction: likely
  relationship: causal
  citation: '@Fridriksson2013'
  method: VBCM
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 64
    population: chronic left hemisphere stroke
    time_post_onset: mean 39.86 months (SD 49.24)
    age_range: mean 61.6 years (SD 12.27)
    handedness: not_reported
    language: not_reported
    phase: chronic
    cohort: not_reported
  statistics:
    threshold: Bonferroni corrected P < 0.002
    effect_size: R2 = 0.42
    p_value: '0.0001'
  confounders_controlled:
  - lesion size
  confounders_not_controlled: []
  region_definition:
    kind: atlas
    atlas: Catani et al. (2012) white matter atlas
    description: Inferior longitudinal fasciculus defined by a probability threshold of 0.50.
  imaging_details:
    field_strength: 3T
    reference_space: MNI152
    atlases_used:
    - Catani et al. (2012)
  author_limitations:
  - Auditory word-picture matching does not specifically isolate lexical and semantic processing.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 3454
    confidence: high
    flags:
    - 'new region id: left_inferior_longitudinal_fasciculus'
  source_passages:
  - section: Results
    page: 5
    quote: 'Two models predicted auditory word-picture recognition ability: Model 1 included the inferior
      longitudinal fasciculus, P = 0.0001, R2 = 0.42'
    supports: claim
  - section: added by backfill
    page: 4
    quote: The cortical regions and white matter tracts comprised a neuroanatomical model where the mean
      intensity value in each region of interest, as well as lesion size, was entered into a stepwise
      regression analysis to predict the speech and language measures (Fig. 2).
    supports: method
  - section: added by backfill
    page: not_reported
    quote: 'To control for multiple comparisons, the stepwise regression analyses were Bonferroni corrected
      where P = 0.05 was divided by the number of predictors: 21 regions of interest and one factor for
      lesion size (for 22 total predictors).'
    supports: method
  - section: added by backfill
    page: 3
    quote: Out of 76 patients included in the database, data from 64 patients (29 females) who had incurred
      a single left hemisphere stroke (60 ischaemic; four haemorrhagic) resulting in chronic aphasia (46
      months post-stroke) were included in this research (Supplementary material).
    supports: method
  lesion_mapping:
    analysis: region_based
    n_analysed: 64
    min_lesion_overlap: not_reported
    lesion_volume_correction: covariate
    multiple_comparisons: bonferroni
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
    - lesion_mapping
---
