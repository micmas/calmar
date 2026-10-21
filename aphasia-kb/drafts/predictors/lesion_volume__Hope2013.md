---
schema_version: 2.3
id: lesion_volume
name: Lesion Volume
kind: predictor
predictor_type: imaging_metric
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
findings:
- id: f1
  target: fluency
  target_kind: impairment
  claim: Total lesion volume is a significant predictor of speech production impairment.
  direction: likely
  relationship: causal
  citation: '@Hope2013'
  method: MLPA
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 270
    population: stroke patients
    time_post_onset: less than a month to more than 30 years
    age_range: 20 to 90 years
    handedness: 242 right handed
    language: English
    phase: chronic
  statistics:
    threshold: p < 0.001
    effect_size: R2 = 0.35
  confounders_controlled:
  - age
  - handedness
  - gender
  - time post-stroke
  confounders_not_controlled: []
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, Section 3.2
    confidence: high
    flags:
    - target fluency used as proxy for composite speech production score
    - imaging_details.reference_space not extracted by the model — set to not_reported; verify against
      the paper
  source_passages:
  - section: Results
    page: 4
    quote: As expected, access to this kind of information [lesion volume]... did improve the predictions
      (R2 = 0.35, F = 144.73, p b 0.001)
    supports: claim
  - section: Method
    page: 2
    quote: This selection process left us with data from 270 patients
    supports: sample
  - section: Discussion
    page: 8
    quote: our preferred predictor configuration systematically under-estimates the severity of the impairments
      suffered by the most impaired patients
    supports: limitation
  author_limitations:
  - The model systematically underestimates severity for the most impaired patients.
  region_definition:
    kind: not_reported
  imaging_details:
    reference_space: not_reported
    atlases_used: []
short_definition: Total volume of structural damage on the patient's lesion mask, typically reported in
  millilitres (cubic centimetres) of T1- or FLAIR-defined tissue loss.
units: ml (cc)
direction_of_severity: higher_is_worse
---
