---
schema_version: 2.3
id: age
name: Age at stroke
kind: predictor
predictor_type: demographic
short_definition: Age of the patient at the time of stroke.
units: years
typical_range: 18-100+
direction_of_severity: higher_is_worse
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
findings:
- id: f1
  target: aphasia_severity
  target_kind: impairment
  claim: Older age at the time of stroke is associated with higher rates of aphasia.
  direction: likely
  relationship: correlational
  citation: '@Wallentin2018'
  method: behavioral_only
  design: cross-sectional
  strength: strong
  evidence_quality: cohort
  sample:
    n: 1967038
    population: US American stroke patients (HCUP database)
    time_post_onset: not_reported
    age_range: not_reported
    handedness: not_reported
    language: English
    phase: not_reported
  statistics:
    threshold: p(uncorrected)<0.05
    effect_size: t(274.83) = 2.11
  confounders_controlled:
  - sex
  - stroke severity
  confounders_not_controlled: []
  author_limitations:
  - The database used a crude proxy for stroke severity (hemiplegia diagnoses).
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results of database analysis, page 9
    confidence: high
    flags: []
  source_passages:
  - section: Results of database analysis
    page: 10
    quote: A significant effect of age, t(274.83) = 2.11, p(uncorrected)<0.05... was observed.
    supports: claim
  - section: Discussion
    page: 10
    quote: The plot illustrates the large age difference between men and women at time of stroke. It also
      shows a positive correlation between average age and aphasia rate, suggesting that older stroke
      patients more often get aphasia.
    supports: claim
  - section: Discussion
    page: 11
    quote: It has to be said, however, that this analysis used a somewhat crude proxy for stroke severity.
    supports: limitation
  region_definition:
    kind: not_reported
---
