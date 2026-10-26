---
schema_version: 2.7
id: initial_aphasia_severity
name: Initial aphasia severity (acute WAB composite)
kind: predictor
predictor_type: behavioural
short_definition: The severity of language impairment measured shortly after stroke onset.
assessment:
- BDAE
- WAB
units: score 0-30 (combined domain score)
typical_range: 0-30 (lower = more severe)
direction_of_severity: lower_is_worse
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
findings:
- id: f1
  target: prognosis
  target_kind: prognosis
  claim: Initial language functioning is a significant predictor of language functioning at 90 days post-stroke.
  direction: likely
  relationship: correlational
  citation: '@Lazar2008'
  method: behavioral_only
  design: longitudinal
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 22
    population: first-time stroke patients with aphasia
    time_post_onset: 24-72 hours (baseline), 90 days (follow-up)
    phase: longitudinal
    age_range: mean 63.8 (SD 5.6)
    handedness: 20/22 right-handed
    language: English- and Spanish-speaking
    cohort: PARIS
  statistics:
    threshold: p = 0.001
    effect_size: r = 0.60
  confounders_controlled: []
  confounders_not_controlled:
  - speech-language therapy intensity
  region_definition:
    kind: not_reported
    description: Behavioural-only predictor finding.
  author_limitations:
  - Small sample size may limit the variance explained by the regression model.
  - Positive correlation may be confounded by mild deficits at onset.
  - Negative correlation with change score may be due to floor effects (more room to improve).
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 531
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 531
    quote: Initial syndrome scores were positively correlated (Pearson) with 90-day scores (r = 0.60,
      p = 0.001)
    supports: claim
  - section: Subjects and Methods
    page: 530
    quote: The Columbia PARIS database is comprised of English- and Spanish-speaking patients with first-time
      stroke... All were examined for baseline function within 24-72 hours of stroke onset.
    supports: sample
  - section: Results
    page: 531
    quote: Regression analysis demonstrated that baseline language functioning was predictive of 90-day
      language functioning, accounting for 33% of the variance (p < 0.01).
    supports: statistics
  - section: Discussion
    page: 532
    quote: Among the limits of this study was the small sample size; a larger cohort might have increased
      the extent to which our regression model would explain variance
    supports: limitation
  - section: Discussion
    page: 532
    quote: First, a positive correlation between the initial and final scores is likely to occur when
      there are mild deficits at syndrome onset.
    supports: limitation
  - section: added by backfill
    page: 1
    quote: Using our Performance and Recovery in Stroke Study (PARIS) database, we evaluated consecutive
      first-time stroke patients with aphasia and diffusion-weighted-image-positive lesions on admission
      and at 90 days.
    supports: sample
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
---
