---
schema_version: 2.7
id: lesion_volume
name: Total lesion volume
kind: predictor
predictor_type: imaging_metric
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
short_definition: The total volume of the ischemic lesion.
units: voxels
findings:
- id: f1
  target: severity_metric
  target_kind: predictor
  claim: Larger left-hemisphere lesion volume is associated with worse language recovery (lower WAB-R
    AQ) at 6 months post-stroke.
  direction: unlikely
  relationship: causal
  citation: '@Forkel2014'
  method: tractography
  design: longitudinal
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 16
    population: left hemisphere stroke patients with aphasia
    time_post_onset: baseline within 2 weeks; follow-up at 6 months
    age_range: 28-87 years
    handedness: all right-handed
    language: native English speaker
    phase: longitudinal
    cohort: not_reported
  statistics:
    threshold: P = 0.011
    effect_size: beta = -0.630
    p_value: 0.011
  confounders_controlled:
  - age
  - sex
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: Total lesion volume extracted from T1-weighted images.
  author_limitations:
  - The sample was a selected group able to tolerate long MRI scans in the acute stage of stroke.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 2032
    confidence: high
    flags:
    - imaging_details.reference_space not extracted by the model — set to not_reported; verify against
      the paper
  source_passages:
  - section: Results
    page: 6
    quote: Among the four variables entered in the analysis only lesion size was an independent predictor
      [beta = -0.630, t(-3.129), P = 0.011] of longitudinal aphasia severity.
    supports: claim
  - section: Materials and methods
    page: 1
    quote: Sixteen patients (10 males; mean age 60 +/- 17 years, range 28-87 years) underwent post stroke
      language assessment with the Revised Western Aphasia Battery and neuroimaging scanning within a
      fortnight from symptoms onset.
    supports: sample
  - section: Discussion
    page: 11
    quote: our observations reflect results derived from a selected group of patients that were able to
      tolerate a 45-min MRI scanning session in the acute stage of stroke.
    supports: limitation
  imaging_details:
    reference_space: not_reported
    atlases_used: []
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
direction_of_severity: higher_is_worse
---
# Lesion Volume

Findings regarding the predictive value of total lesion volume on aphasia recovery.
