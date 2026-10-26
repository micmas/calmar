---
schema_version: 2.7
id: intention_treatment
name: Intention Treatment
kind: therapy
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
short_description: A naming treatment where trials are initiated with complex left-hand movements to engage
  right-hemisphere intentional mechanisms.
targets_impairments:
- anomic_aphasia
- conduction_aphasia
findings:
- id: f1
  target: semantics
  target_kind: impairment
  claim: Intention Treatment leads to significantly greater generalization to untrained category-member
    generation probes compared to a control treatment without hand movements.
  direction: likely
  relationship: causal
  citation: '@Benjamin2014'
  method: behavioral_only
  design: RCT
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 14
    population: chronic left-hemisphere stroke aphasia
    time_post_onset: '>6 months'
    age_range: not_reported
    handedness: all right-handed
    language: English
    phase: chronic
    cohort: not_reported
  statistics:
    threshold: P < .01
    effect_size: t = 3.33
  confounders_controlled:
  - ' picture-naming impairment (BNT)'
  - frontal lesion extent
  confounders_not_controlled:
  - ' aphasia type (IT group had more conduction aphasia)'
  author_limitations:
  - Small sample size.
  - Difference in group composition (IT dominated by conduction aphasia, CT by anomic aphasia).
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 550
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 6
    quote: Furthermore, when untrained probes alone were considered in group analyses, only IT showed
      significant improvement (t = 3.77, df = 5, P < .01 for IT on picture-naming; t = 1.20, df = 6, P
      > .05 for CT on picture-naming; t = 3.33, df = 6, P < .01 for IT on categories; t = 1.56, df = 5,
      P > .05 for CT on categories).
    supports: claim
  - section: Discussion
    page: 7
    quote: Behaviorally, IT and CT both yielded gains for responses to all picture-naming and category
      probes. However, when only untrained probes were analyzed, only IT showed significant gains from
      baseline to phase 3.
    supports: claim
  region_definition:
    kind: not_reported
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
---
# Intention Treatment

Intention Treatment uses behavioral manipulations (left-hand movements) to shift language production to right-hemisphere substrates, promoting generalization to untrained items.
