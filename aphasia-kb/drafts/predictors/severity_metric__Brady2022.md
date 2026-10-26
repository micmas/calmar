---
schema_version: 2.7
id: severity_metric
name: Aphasia severity metric (instrument-agnostic)
kind: predictor
predictor_type: clinical
short_definition: The severity of aphasia at baseline, typically measured by a standardized language battery.
assessment:
- WAB-AQ
- AAT-TT
- AAT-SSC
units: score
typical_range: 0-100 (WAB-AQ)
direction_of_severity: lower_is_worse
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
findings:
- id: f1
  target: severity_metric
  target_kind: predictor
  claim: Participants with moderate-severe aphasia achieve greatest overall-language gains with moderate-intensity
    SLT (3-4 h/week), while mild-moderate participants achieve greatest gains with high-intensity SLT
    (>9 h/week).
  direction: likely
  relationship: responder
  citation: '@Brady2022'
  method: meta-analysis
  design: meta-analysis
  strength: moderate
  evidence_quality: cohort
  instrument: WAB-AQ
  score_band: moderate-severe vs mild-moderate
  interpretation: Dichotomized based on median language modality score.
  sample:
    n: 959
    population: stroke-related aphasia
    time_post_onset: not_reported
    age_range: not_reported
    handedness: not_reported
    language: English predominant
    phase: not_reported
    cohort: RELEASE
  statistics:
    threshold: 95% CI
    effect_size: not_reported
  confounders_controlled:
  - age
  - sex
  - time post-onset
  confounders_not_controlled: []
  author_limitations:
  - Risk of false negatives and positives due to hypothesis-generating approach.
  - Spontaneous recovery may impact treatment gains.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 8
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 8
    quote: The moderate-severe group made significant gains on overall language at all intensities, with
      greatest gains for 3-to-4 SLT-h/week... In contrast, the mild-moderate group's gains were associated
      with higher-intensity SLT (> 9 h/week).
    supports: claim
  - section: Methods
    page: 5
    quote: We dichoto-mized IPD based on key demographic and clinical data... moderate-severe and mild-moderate
      groups based on the overall median language modality score.
    supports: sample
  - section: Methods
    page: 4
    quote: Drawing only RCT IPD from the wider RELEASE database (21), we conducted a network meta-analysis
      of SLT interventions delivered by language outcomes (15).
    supports: method
  - section: Discussion
    page: 9
    quote: Our statistical inferencing, hypothesis generating approach carries a risk of false nega-tive
      and positive findings.
    supports: limitation
  - section: added by backfill
    page: 4
    quote: We created the international RELEASE IPD database of aphasia research to support several planned
      analyses
    supports: sample
  region_definition:
    kind: not_reported
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
---
