---
schema_version: 2.3
id: rhythm_production
name: Rhythm Production (Tapping)
kind: impairment
short_definition: The ability to synchronize motor output (e.g., tapping) to an external rhythmic beat.
assessment:
- Isochronous tapping
- Music tapping
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
findings:
- id: f1
  target: severity_metric
  target_kind: predictor
  claim: Rhythm tapping performance is positively correlated with overall aphasia severity.
  direction: likely
  relationship: correlational
  citation: '@Kasdan2025'
  method: behavioral_only
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 33
    population: chronic post-stroke aphasia
    time_post_onset: approximately 1 yr or more post-stroke
    age_range: 18-90 years
    handedness: 27 R; 3 L; 3 Am
    language: English
    phase: chronic
  statistics:
    threshold: not_reported
    effect_size: r = 0.41
    p_value: '0.018'
  confounders_controlled: []
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: behavioural-only correlation
  author_limitations:
  - The association between tapping and language measures must be considered exploratory.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 14
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 14
    quote: Tapping correlated with overall aphasia severity (r = 0.41, p = 0.018)
    supports: claim
  - section: Results
    page: 15
    quote: In sum, this set of results—which must be considered exploratory—shows that some aspects of
      fluency... were highly correlated with tapping
    supports: limitation
---
