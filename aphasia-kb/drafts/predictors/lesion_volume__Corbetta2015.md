---
schema_version: 2.7
id: lesion_volume
name: Total lesion volume
kind: predictor
predictor_type: imaging_metric
short_definition: The total volume of the brain lesion.
units: mm3
typical_range: average 34,176 mm3
direction_of_severity: higher_is_worse
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
findings:
- id: f1
  target: severity_metric
  target_kind: predictor
  claim: Total lesion volume accounts for a small amount of variance in language and other behavioral
    deficits in acute stroke.
  direction: likely
  relationship: correlational
  citation: '@Corbetta2015'
  method: MLPA
  design: cross-sectional
  strength: strong
  evidence_quality: cohort
  sample:
    n: 132
    population: first-time stroke patients
    time_post_onset: mean 13 +/- 4.9 days
    phase: acute
    age_range: median 54
    handedness: not_reported
    language: not_reported
    cohort: not_reported
  statistics:
    threshold: not_reported
    effect_size: < 20% variance
    p_value: not_reported
  confounders_controlled: []
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: Global lesion volume measure.
  author_limitations:
  - The absence of measures in some domains may partly account for unexplained behavioral variance.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 933
    confidence: high
    flags:
    - imaging_details.reference_space not extracted by the model — set to not_reported; verify against
      the paper
  source_passages:
  - section: Results
    page: 933
    quote: First, lesion volume accounts for only small amounts of variance (< 20%) in all domains.
    supports: claim
  - section: Results
    page: 928
    quote: Subjects (n = 172) with a first symptomatic stroke... n = 132 meeting post-enrollment inclusion
      criteria
    supports: sample
  - section: Experimental Procedures
    page: 939
    quote: The voxel-wise relationship between lesion maps and behavioral scores for each domain was analyzed
      using a multivariate leave-one-out ridge regression machine learning algorithm
    supports: method
  - section: Discussion
    page: 937
    quote: First, some important cognitive domains... were either not tested or only coarsely evaluated.
    supports: limitation
  - section: added by backfill
    page: 3
    quote: n = 132 meeting post-enrollment inclusion criteria
    supports: method
  - section: added by backfill
    page: not_reported
    quote: To map lesion-behavior relationships, we applied ridge regression models separately for each
      factor. Ridge regression is a multivariate machine-learning method.
    supports: method
  imaging_details:
    reference_space: not_reported
    atlases_used: []
  lesion_mapping:
    analysis: multivariate
    n_analysed: 132
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
