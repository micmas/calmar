---
schema_version: 2.6
id: initial_aphasia_severity
name: Initial aphasia severity (acute WAB composite)
kind: predictor
predictor_type: behavioural
short_definition: The severity of aphasia measured at the time of acute admission.
assessment:
- Scandinavian Stroke Scale (SSS) aphasia score
units: score 0-3
typical_range: 0 (severe) to 3 (no aphasia)
direction_of_severity: lower_is_worse
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
findings:
- id: f1
  target: prognosis
  target_kind: prognosis
  claim: Initial severity of aphasia is the most significant clinical predictor of long-term language
    outcome after stroke.
  direction: likely
  relationship: correlational
  citation: '@Pedersen1995'
  method: behavioral_only
  design: longitudinal
  strength: strong
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
    effect_size: explained 50% of the total variance
    p_value: not_reported
  confounders_controlled:
  - age
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
    paper_section: Results, page 5; Discussion, page 7
    confidence: high
    flags: []
  source_passages:
  - section: Abstract
    page: 1
    quote: Initial severity of aphasia was the only clinically relevant predictor of aphasia outcome.
    supports: claim
  - section: Materials and Methods
    page: 1
    quote: A total of 1,014 patients with acute stroke were admitted... Included were thus 881 patients.
    supports: sample
  - section: Materials and Methods
    page: 1
    quote: Median time from stroke onset to admission was 12 hours.
    supports: sample
  - section: Factors Related to Recovery
    page: 5
    quote: Aphasia score on admission and neurological severity on admission explained 50% of the total
      variance.
    supports: statistics
  - section: Discussion
    page: 6
    quote: The aphasia assessment employed in this study rates spoken language, but does not assess auditory
      impressive function.
    supports: limitation
---

# Findings from Pedersen 1995

This study of a large community-based cohort establishes that initial aphasia severity is the primary determinant of recovery outcome, outweighing demographics like age and sex.
