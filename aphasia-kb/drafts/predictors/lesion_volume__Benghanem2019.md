---
schema_version: 2.3
id: lesion_volume
name: Lesion Volume
kind: predictor
predictor_type: imaging_metric
short_definition: The total volume of the infarct lesion.
units: ml
typical_range: not_reported
direction_of_severity: higher_is_worse
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
findings:
- id: f1
  target: prognosis
  target_kind: prognosis
  claim: Total infarct volume is a univariate predictor of 3-month functional outcome.
  direction: likely
  relationship: causal
  citation: '@Benghanem2019'
  method: LSM
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 73
    population: post-stroke aphasia
    time_post_onset: 24-48 h
    age_range: median 63.7 (IQR 52.3-78)
    handedness: not_reported
    language: not_reported
    phase: mixed
  statistics:
    threshold: p = 0.001
    effect_size: explained 19.7% of the variance
    p_value: '0.001'
  confounders_controlled: []
  confounders_not_controlled:
  - amount of Speech and Language Therapy
  author_limitations:
  - In-sample analysis requiring external validation.
  - Potential underestimation of stroke volume in MNI normalised images.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 1305
    confidence: high
    flags:
    - imaging_details.reference_space not extracted by the model — set to not_reported; verify against
      the paper
  source_passages:
  - section: Results
    page: 3
    quote: The ART at D7, infarct volume, and the intersection index were univariate predictors of good
      outcome at 3 months (AHS 0-2) (Table 2).
    supports: claim
  - section: Results
    page: 3
    quote: The infarct volume explained 19.7% of the variance (p = 0.001)
    supports: statistics
  - section: Limitations
    page: 6
    quote: Finally, we may have underestimated the stroke volume in the MNI normalised images since we
      did not use lesion masking in the process.
    supports: limitation
  region_definition:
    kind: not_reported
  imaging_details:
    reference_space: not_reported
    atlases_used: []
---
