---
schema_version: 2.3
id: lesion_volume
name: Lesion Volume
kind: predictor
predictor_type: imaging_metric
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
findings:
- id: f1
  target: severity_metric
  target_kind: predictor
  claim: There is a strong coupling between impairment and lesion size, as larger lesions are more likely
    to affect critical anatomical structures.
  direction: likely
  relationship: synthesis
  citation: '@Karnath2018'
  method: narrative_review
  design: narrative-review
  strength: moderate
  evidence_quality: narrative-review
  sample:
    n: null
    population: not_reported
    phase: not_reported
  author_limitations:
  - Lesion-behavior mapping is necessarily spatially biased by vasculature.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Voxel-based lesion behavior mapping (VLBM), page 3
    confidence: high
    flags:
    - finding is a synthesis of field consensus, not a primary data result
  source_passages:
  - section: Voxel-based lesion behavior mapping (VLBM)
    page: 3
    quote: as a rule of thumb there is a strong coupling between impairment and lesion size.
    supports: claim
  - section: Voxel-based lesion behavior mapping (VLBM)
    page: 3
    quote: The use of naturally occurring strokes to infer lesion-behavior relationships is necessarily
      spatially biased.
    supports: limitation
short_definition: Total volume of structural damage on the patient's lesion mask, typically reported in
  millilitres (cubic centimetres) of T1- or FLAIR-defined tissue loss.
units: ml (cc)
direction_of_severity: higher_is_worse
---
