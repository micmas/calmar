---
schema_version: 2.3
id: severity_metric
name: Aphasia severity metric (instrument-agnostic)
kind: predictor
predictor_type: behavioural
short_definition: A measure of overall language impairment severity at a given time point.
assessment:
- WAB-AQ
- BDAE
- Aachener Aphasia Test
units: score
typical_range: not_reported
direction_of_severity: lower_is_worse
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
findings:
- id: f1
  target: prognosis
  target_kind: prognosis
  claim: Initial severity of the language deficit is a significant predictor of subsequent language recovery.
  direction: likely
  relationship: correlational
  citation: '@Hartwigsen2019'
  method: narrative_review
  design: narrative-review
  strength: strong
  evidence_quality: narrative-review
  sample:
    n: not_reported
    population: post-stroke aphasia
    phase: not_reported
  statistics:
    threshold: not_reported
    effect_size: not_reported
  author_limitations: []
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Neuroimaging-based outcome prediction, page 5
    confidence: high
    flags: []
  source_passages:
  - section: Neuroimaging-based outcome prediction
    page: 5
    quote: It is well established that initial severity of the language deficit and age are factors that
      influence later recovery (Pedersen et al., 1995).
    supports: claim
---
Entry for general aphasia severity as a predictor of recovery.
