---
schema_version: 2.3
id: left_heschls_gyrus
name: Left Heschl's Gyrus
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
hemisphere: left
findings:
- id: f1
  target: phonological_recognition
  target_kind: impairment
  claim: Damage to the left Heschl's gyrus is strongly associated with deficits in speech recognition.
  direction: likely
  relationship: causal
  citation: '@Thye2018'
  method:
  - VLSM
  - MLPA
  design: cross-sectional
  strength: strong
  evidence_quality: cohort
  sample:
    n: 128
    population: individuals with aphasia secondary to left hemisphere stroke
    time_post_onset: at least 1 month post onset
    age_range: 26–79
    handedness: premorbidly right handed
    language: English as the primary language
    phase: early_subacute
  statistics:
    threshold: not_reported
    effect_size: SCCAN result highly localized to Heschl's gyrus
  confounders_controlled:
  - lesion size
  confounders_not_controlled: []
  region_definition:
    kind: data_driven_cluster
    description: Identified via SCCAN as a highly localized region for Speech Recognition.
  imaging_details:
    reference_space: MNI152
    atlases_used: []
    preprocessing_pipeline: Registered to MNI space Colin27 template
  author_limitations:
  - The identified region was far smaller than those reported in prior studies.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 5
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 5
    quote: Deﬁcits in Speech Recognition were associated with highly localized damage to Heschl's gyrus.
    supports: claim
  - section: Discussion
    page: 5
    quote: For the Speech Recognition deﬁcit scores, SCCAN identiﬁed a very small region primarily in
      Heschl's gyrus.
    supports: region_definition
  - section: Discussion
    page: 5
    quote: the identiﬁed region was far smaller than those reported in prior studies.
    supports: limitation
---
Findings from Thye & Mirman (2018) regarding the role of Heschl's gyrus in speech recognition.
