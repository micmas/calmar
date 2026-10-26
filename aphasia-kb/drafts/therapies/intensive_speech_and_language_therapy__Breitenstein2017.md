---
schema_version: 2.7
id: intensive_speech_and_language_therapy
name: Intensive Speech and Language Therapy
kind: therapy
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-22
short_description: High-intensity speech and language therapy (>=10h/week) combining linguistic and communicative-pragmatic
  approaches.
targets_impairments:
- global_aphasia
- brocas_aphasia
- wernickes_aphasia
- anomic_aphasia
dosage: 3 weeks or more, >=10 h per week professional therapy + >=5 h per week self-managed training
findings:
- id: f1
  target: severity_metric
  target_kind: predictor
  claim: Three weeks of intensive speech and language therapy significantly improves verbal communication
    in everyday life for patients with chronic aphasia.
  direction: likely
  relationship: responder
  citation: '@Breitenstein2017'
  method: clinical_RCT
  design: RCT
  strength: strong
  evidence_quality: RCT
  sample:
    n: 156
    population: chronic aphasia after stroke
    time_post_onset: 6 months or more
    phase: chronic
    age_range: 18-70 years
    handedness: not_reported
    language: German
    cohort: FCET2EC
  statistics:
    threshold: p=0.0004
    effect_size: Cohen's d 0.58
    p_value: 0.0004
  confounders_controlled:
  - baseline ANELT A-scale score
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: behavioural-only treatment-efficacy finding — no specific brain region
  imaging: none
  imaging_details:
    reference_space: not_reported
    atlases_used: []
  author_limitations:
  - Low-intensity therapy provided to control group and during follow-up might have supported maintenance
    of effects.
  - Study does not address if a critical time window exists for maximum effects.
  - Results may not generalize to patients older than 70 years.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Summary, page 1
    confidence: high
    flags: []
  source_passages:
  - section: Summary
    page: 1
    quote: Verbal communication was significantly improved from baseline to after intensive speech and
      language treatment (mean difference 2.61 points [SD 4.94]; 95% CI 1.49 to 3.72), but not from baseline
      to after treatment deferral... between-group difference Cohen's d 0.58; p=0.0004.
    supports: claim
  - section: Participants
    page: 3
    quote: Inclusion criteria... were chronic aphasia... lasting 6 months or more after an ischaemic or
      haemorrhagic stroke, age 18-70 years, German as first language...
    supports: sample
  - section: Study design
    page: 2
    quote: We did a randomised, open-label, blinded-endpoint, multicentre, stratified-by-centre, waiting-list-controlled,
      parallel-group, superiority trial...
    supports: method
  - section: Statistical analysis
    page: 5
    quote: We used an ANCOVA model to assess the primary outcome with the ANELT A-scale score... as a
      dependent variable, treatment group as an independent variable, and baseline ANELT A-scale score
      as a covariate.
    supports: statistics
  - section: Discussion
    page: 10
    quote: First, low intensity speech and language therapy was provided to the control group during the
      treatment deferral period and to both groups during the 6-month follow-up.
    supports: limitation
  - section: added by backfill
    page: 2
    quote: The aims of our multicentre randomised controlled trial, From Controlled Experimental Trial
      2 Everyday Communication (FCET2EC), were to assess the effectiveness of 3 weeks or more of intensive
      (≥10 h per week) speech and language therapy in chronic aphasia after stroke compared with 3 weeks
      of treatment deferral in terms of improved everyday verbal communication.
    supports: sample
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
notes: Primary outcome measured by ANELT A-scale. Findings show stability of effect at 6 months.
---
