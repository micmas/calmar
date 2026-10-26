---
schema_version: 2.7
id: left_thalamus
name: Left Thalamus
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
hemisphere: left
findings:
- id: f1
  target: aphasia
  target_kind: impairment
  claim: Isolated left thalamic infarcts can cause aphasia independently of cortical hypoperfusion due
    to arterial stenosis or occlusion.
  direction: likely
  relationship: causal
  citation: '@Sebastian2014'
  method: LSM
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 10
    population: patients with isolated left thalamic infarct
    time_post_onset: within 24 h of symptom onset
    phase: acute
    age_range: mean 45.3 years (SD 8.8)
    handedness: not_reported
    language: not_reported
    cohort: not_reported
  statistics:
    threshold: not_reported
    effect_size: 5/10 patients with left thalamic infarcts had aphasia
    p_value: not_reported
  confounders_controlled:
  - ' cortical hypoperfusion due to arterial stenosis or occlusion'
  confounders_not_controlled:
  - ' diaschisis'
  region_definition:
    kind: manual_ROI
    description: Isolated infarct limited to the left thalamus
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
    paper_section: Results, page 4
    confidence: high
    flags: []
  source_passages:
  - section: Abstract
    page: 1
    quote: Results revealed that 5/10 patients with left thalamic infarcts had aphasia and only 1 had
      cortical hypoperfusion
    supports: claim
  - section: Materials and Methods
    page: 3
    quote: A subset of 10 participants had isolated left thalamic infarct (infarct limited to the thalamus)
    supports: sample
  - section: Materials and Methods
    page: 3
    quote: All participants were admitted and received MRI within 24 h of symptom onset.
    supports: sample
  - section: Results
    page: 4
    quote: Of the 10 patients with isolated left thalamic lesions, 5 had aphasia... Four of the five aphasic
      patients had normal cortical perfusion.
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
