---
schema_version: 2.3
id: time_post_onset
name: Time Post-Onset
kind: predictor
predictor_type: clinical
short_definition: The duration of time elapsed since the stroke event occurred.
units: weeks/months
typical_range: not_reported
direction_of_severity: not_applicable
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
findings:
- id: f1
  target: melodic_intonation_therapy
  target_kind: therapy
  claim: Earlier initiation of Melodic Intonation Therapy in the subacute phase predicts greater improvement
    in language repetition and verbal communication.
  direction: likely
  relationship: responder
  citation: '@vanderMeulen2014'
  method: behavioral_only
  design: longitudinal
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 27
    population: subacute severe nonfluent aphasia after left hemisphere stroke
    time_post_onset: 2 to 3 months
    age_range: 18 to 80 years
    handedness: all right-handed
    language: Dutch
    phase: early_subacute
  statistics:
    threshold: p < .05
    effect_size: beta = -0.68 (untrained items), -1.54 (AAT repetition), -0.46 (ANELT)
    p_value: .01 to .04
  confounders_controlled: []
  confounders_not_controlled:
  - lesion size
  - lesion location
  region_definition:
    kind: not_reported
    description: predictor-based finding
  author_limitations:
  - The study is too underpowered to obtain significant effects on most of the outcome measures.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 5
    confidence: high
    flags: []
  source_passages:
  - section: Abstract
    page: 1
    quote: Finally, delaying MIT was related to less improvement in the repetition of trained material.
    supports: claim
  - section: Results
    page: 5
    quote: Time poststroke at the start of MIT predicted outcome on untrained items, MIT task (beta =
      -.68, p = .01), on AAT repetition (beta = -1.54, p = .02), and on the ANELT (beta = -.46, p = .04).
      The earlier MIT was started, the greater the improvement on these outcome measures.
    supports: statistics
  - section: Discussion
    page: 7
    quote: A delay of merely 6 weeks was related to less improvement.
    supports: claim
  - section: Discussion
    page: 6
    quote: The study is too underpowered to obtain significant effects on most of the outcome measures
    supports: limitation
---
