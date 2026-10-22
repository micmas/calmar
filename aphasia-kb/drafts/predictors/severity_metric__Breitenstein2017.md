---
schema_version: 2.6
id: severity_metric
name: Aphasia severity metric (instrument-agnostic)
kind: predictor
predictor_type: clinical
short_definition: Overall measure of stroke severity or aphasia severity used to predict treatment outcome.
assessment:
- modified Rankin Scale (mRS)
- Aachen Aphasia Test (AAT)
units: score
typical_range: not_reported
direction_of_severity: higher_is_worse
findings:
- id: f1
  target: intensive_speech_and_language_therapy
  target_kind: therapy
  claim: Baseline stroke severity is a significant predictor of immediate treatment success in verbal
    communication, with milder stroke leading to greater improvement.
  direction: likely
  relationship: responder
  citation: '@Breitenstein2017'
  method: behavioral_only
  design: RCT
  strength: moderate
  evidence_quality: RCT
  sample:
    n: 156
    population: chronic aphasia after stroke
    time_post_onset: 6 months or more
    phase: chronic
    age_range: 18-70 years
    handedness: not_reported
    language: German
  statistics:
    threshold: p < 0.0001
    effect_size: not_reported
    p_value: 0.0001
  confounders_controlled: []
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: behavioural-only predictor finding
  imaging: none
  imaging_details:
    reference_space: not_reported
    atlases_used: []
  author_limitations:
  - The study did not address whether a critical time window exists after stroke for maximum treatment
    effects to be achieved.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 7
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 7
    quote: Of all patient-related, stroke-related, aphasia-related, and therapy-related variables... only
      baseline stroke severity was a significant predictor of immediate treatment success in verbal communication
      (data not shown); patients with less severe stroke at enrolment had greater improvement after treatment
      than those with more severe stroke (p < 0.0001).
    supports: claim
  - section: Participants
    page: 3
    quote: Inclusion criteria... were chronic aphasia... lasting 6 months or more after an ischaemic or
      haemorrhagic stroke, age 18-70 years, German as first language...
    supports: sample
  - section: Discussion
    page: 10
    quote: Second, the study design did not address whether a critical time window exists after stroke
      for maximum treatment effects to be achieved.
    supports: limitation
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-22
---
