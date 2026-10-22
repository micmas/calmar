---
schema_version: 2.3
id: severity_metric
name: Aphasia severity metric (instrument-agnostic)
kind: predictor
predictor_type: behavioural
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
short_definition: A general measure of aphasia severity, typically derived from a standardized battery.
assessment:
- WAB-R Aphasia Quotient
units: score 0-100
typical_range: 0-100 (lower = more severe)
direction_of_severity: lower_is_worse
findings:
- id: f1
  target: tdcs_aphasia_treatment
  target_kind: therapy
  claim: Baseline aphasia severity, measured by the WAB-R Aphasia Quotient, is positively correlated with
    the improvement in naming following aphasia treatment.
  direction: likely
  relationship: correlational
  citation: '@Fridriksson2018JAMA'
  method: behavioral_only
  design: RCT
  strength: moderate
  evidence_quality: RCT
  instrument: WAB-R Aphasia Quotient
  score_band: all severities
  interpretation: Higher baseline AQ (less severe) associated with greater naming improvement.
  sample:
    n: 74
    population: chronic left-hemisphere stroke aphasia
    time_post_onset: '>6 months'
    age_range: mean 60 (SD 10) years
    handedness: previously right-handed
    language: not_reported
    phase: chronic
  statistics:
    threshold: P = .01
    effect_size: Pearson rho = 0.29
    p_value: '.01'
  confounders_controlled:
  - enrolling site
  confounders_not_controlled: []
  author_limitations:
  - The current study was not powered for superiority analyses to compare A-tDCS with S-tDCS.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 1474
    confidence: high
    flags:
    - cohort overlaps with @Fridriksson2018, @Yourganov2015Predicting (USC/MUSC Aphasia Lab); flag for
      downstream double-counting risk in interpret_overlap().
  source_passages:
  - section: Results
    page: 5
    quote: Baseline aphasia severity (AQ) was correlated with the overall improvement in naming at 1 week
      posttreatment (Pearson rho = 0.29, P = .01).
    supports: claim
  - section: Results
    page: 1
    quote: A total of 74 patients were enrolled.
    supports: sample
  - section: Statistical Analysis
    page: 4
    quote: The primary analysis was an intent-to-treat analysis and was adjusted for enrolling site and
      baseline aphasia severity measured as the AQ from the WAB-R.
    supports: method
  - section: Results
    page: 5
    quote: Pearson rho = 0.29, P = .01
    supports: statistics
  - section: Limitations
    page: 6
    quote: The current study was not powered for superiority analyses to compare A-tDCS with S-tDCS.
    supports: limitation
  region_definition:
    kind: not_reported
---
