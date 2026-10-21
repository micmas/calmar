---
schema_version: 2.3
id: severity_metric
name: Aphasia Severity Metric
kind: predictor
predictor_type: behavioural
short_definition: A measure of overall aphasia severity used to predict recovery outcomes.
assessment:
- Aphasia Rapid Test (ART)
- WAB-AQ
- BDAE severity
units: score
typical_range: 0-100 (lower = more severe)
direction_of_severity: lower_is_worse
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
findings:
- id: f1
  target: prognosis
  target_kind: prognosis
  claim: Initial aphasia severity measured by the Aphasia Rapid Test at day 7 predicts 3-month functional
    outcome.
  direction: likely
  relationship: correlational
  citation: '@Benghanem2019'
  instrument: Aphasia Rapid Test (ART)
  score_band: all severities
  interpretation: Higher initial impairment predicts poorer 3-month outcome.
  method: behavioral_only
  design: cross-sectional
  strength: strong
  evidence_quality: cohort
  sample:
    n: 73
    population: post-stroke aphasia
    time_post_onset: day 7
    age_range: median 63.7 (IQR 52.3-78)
    handedness: not_reported
    language: not_reported
    phase: not_reported
  statistics:
    threshold: p < 0.0001
    effect_size: explained 55.8% of variance
    p_value: < 0.0001
  confounders_controlled: []
  confounders_not_controlled:
  - amount of Speech and Language Therapy
  author_limitations:
  - Single center study based on routine care data.
  - ART does not capture the full complexity of aphasia.
  - In-sample analysis requiring external validation.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 1305
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 3
    quote: The ART at D7, infarct volume, and the intersection index were univariate predictors of good
      outcome at 3 months (AHS 0-2) (Table 2).
    supports: claim
  - section: Results
    page: 3
    quote: The ART D7 explained 55.8% of the variance in 3-month good outcome (p < 0.0001) and correctly
      classified 84.9% of the patients
    supports: statistics
  - section: Limitations
    page: 6
    quote: First, this is a single center study based on data acquired during routine care.
    supports: limitation
  region_definition:
    kind: not_reported
---
