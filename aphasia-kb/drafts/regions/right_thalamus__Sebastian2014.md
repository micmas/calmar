---
schema_version: 2.7
id: right_thalamus
name: Right Thalamus
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
hemisphere: right
findings:
- id: f1
  target: hemispatial_neglect
  target_kind: impairment
  claim: Hemispatial neglect after isolated right thalamic infarct occurs only when there is concurrent
    cortical hypoperfusion due to arterial stenosis or occlusion.
  direction: likely
  relationship: causal
  citation: '@Sebastian2014'
  method: LSM
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 10
    population: patients with isolated right thalamic lesions
    time_post_onset: within 24 h of symptom onset
    phase: acute
    age_range: mean 52.3 years (SD 9.8)
    handedness: not_reported
    language: not_reported
    cohort: not_reported
  statistics:
    threshold: X2 = 10; p = 0.001
    effect_size: 2/10 patients with right thalamic infarcts had hemispatial neglect and both had cortical
      hypoperfusion
    p_value: '.001'
  confounders_controlled:
  - ' cortical hypoperfusion due to arterial stenosis or occlusion'
  confounders_not_controlled: []
  region_definition:
    kind: manual_ROI
    description: Isolated infarct limited to the right thalamus
  imaging_details:
    field_strength: not_reported
    preprocessing_pipeline: not_reported
    reference_space: not_reported
    atlases_used: []
  author_limitations:
  - Small sample size demands further studies to support these findings.
  - Unable to determine which specific thalamic nuclei were affected due to low spatial resolution of
    DWI scans.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 5
    confidence: high
    flags: []
  source_passages:
  - section: Abstract
    page: 1
    quote: neglect occurred after isolated right thalamic infarcts only when there was cortical hypoperfusion
      due to arterial stenosis or occlusion.
    supports: claim
  - section: Materials and Methods
    page: 3
    quote: 10 participants had isolated right thalamic lesions
    supports: sample
  - section: Results
    page: 5
    quote: Of the 10 patients with exclusively right thalamic lesions, two had left hemispatial neglect.
      Both the patients had cortical hypoperfusion... Eight patients without hemispatial neglect showed
      no cortical hypoperfusion (X2 = 10; p = 0.001).
    supports: statistics
  - section: Discussion
    page: 7
    quote: The small size of our patient group demands further studies to support these findings.
    supports: limitation
  - section: Materials and Methods
    page: 3
    quote: We were unable to determine which thalamic nuclei were affected due to the low spatial resolution
      of the DWI scans relative to thalamic nuclei.
    supports: limitation
  lesion_mapping:
    analysis: not_reported
    n_analysed: 10
    min_lesion_overlap: not_reported
    lesion_volume_correction: not_reported
    multiple_comparisons: not_reported
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
    - lesion_mapping
---
