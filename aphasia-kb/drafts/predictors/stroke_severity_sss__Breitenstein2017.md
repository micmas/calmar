---
schema_version: 2.3
id: stroke_severity_sss
name: Stroke Severity
kind: predictor
predictor_type: clinical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
short_definition: Clinical measure of stroke severity, typically using the modified Rankin Scale (mRS)
  or NIHSS.
assessment:
- modified Rankin Scale (mRS)
units: score
typical_range: 0-6 (higher = more severe)
direction_of_severity: higher_is_worse
findings:
- id: f1
  target: intensive_speech_and_language_therapy
  target_kind: therapy
  claim: Lower baseline stroke severity (mRS) predicts greater immediate improvement in verbal communication
    following intensive speech and language therapy.
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
    time_post_onset: '>=6 months'
    age_range: 18-70 years
    handedness: not_reported
    language: German
    phase: chronic
  statistics:
    threshold: p<0.0001
    effect_size: not_reported
  confounders_controlled: []
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: behavioural predictor
  author_limitations:
  - The study did not address whether a critical time window exists after stroke for maximum treatment
    effects.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 7
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 7
    quote: only baseline stroke severity was a significant predictor of immediate treatment success in
      verbal communication... patients with less severe stroke at enrolment had greater improvement after
      treatment than those with more severe stroke (p<0.0001).
    supports: claim
  - section: Discussion
    page: 10
    quote: the study design did not address whether a critical time window exists after stroke for maximum
      treatment effects to be achieved.
    supports: limitation
---
Baseline stroke severity (mRS) is a significant predictor of the magnitude of immediate gain in verbal communication following intensive SLT.
