---
schema_version: 2.6
id: age
name: Age at stroke
kind: predictor
predictor_type: demographic
short_definition: Age of the patient at the time of stroke.
units: years
typical_range: not_reported
direction_of_severity: not_applicable
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
findings:
- id: f1
  target: prognosis
  target_kind: prognosis
  claim: Age is not a clinically relevant independent predictor of aphasia recovery outcome.
  direction: no_effect
  relationship: correlational
  citation: '@Pedersen1995'
  method: behavioral_only
  design: longitudinal
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 881
    population: unselected and community-based sample of acute stroke patients
    time_post_onset: median 12 hours
    phase: acute
    age_range: mean 74.5 (SD 10.9)
    handedness: not_reported
    language: not_reported
  statistics:
    threshold: p < 0.05
    effect_size: not_reported
    p_value: not_reported
  confounders_controlled:
  - initial aphasia severity
  - neurological severity on admission
  - sex
  - side of stroke lesion
  - prior stroke
  - comorbidity
  - handedness
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: behavioural-only prognostic finding
  author_limitations:
  - The aphasia assessment employed in this study rates spoken language, but does not assess auditory
    impressive function.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Factors Related to Recovery, page 5
    confidence: high
    flags: []
  source_passages:
  - section: Factors Related to Recovery
    page: 5
    quote: Age, sex, side of stroke lesion, comorbidity, prior stroke, and handedness were thus not related
      to recovery from aphasia.
    supports: claim
  - section: Materials and Methods
    page: 1
    quote: Included were thus 881 patients.
    supports: sample
  - section: Discussion
    page: 6
    quote: The aphasia assessment employed in this study rates spoken language, but does not assess auditory
      impressive function.
    supports: limitation
---

# Findings from Pedersen 1995

In this large cohort, age did not independently predict the degree of language recovery when controlling for initial severity.
