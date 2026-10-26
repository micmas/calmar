---
schema_version: 2.7
id: cognitive_linguistic_treatment
name: Cognitive-Linguistic Treatment
kind: therapy
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
short_description: Impairment-based treatment targeting specific linguistic functions (e.g., semantics
  via BOX or phonology via FIKS) to improve word finding.
targets_impairments:
- semantics
- phonological_production
notes: This entry captures the results of the RATS-3 trial regarding early intensive delivery.
findings:
- id: f1
  target: severity_metric
  target_kind: predictor
  claim: Four weeks of intensive cognitive-linguistic treatment initiated within two weeks of stroke is
    not more effective than no language treatment for the recovery of everyday verbal communication.
  direction: no_effect
  relationship: responder
  citation: '@Nouwens2017'
  method: clinical_RCT
  design: RCT
  strength: strong
  evidence_quality: RCT
  sample:
    n: 152
    population: stroke patients with first-ever aphasia
    time_post_onset: randomised within 2 weeks of onset
    phase: early_subacute
    age_range: 18-85 years
    handedness: not_reported
    language: near-native Dutch
    cohort: Rotterdam Aphasia Therapy Study-3
  statistics:
    threshold: p = 0.805
    effect_size: adjusted difference 0.39
    ci_95: '[-2.70 to 3.47]'
  confounders_controlled:
  - age
  - sex
  - education
  - baseline aphasia severity
  - type of stroke
  - location of stroke
  - baseline Barthel Index score
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: behavioural-only treatment-efficacy finding - no specific brain region
  imaging: none
  author_limitations:
  - 'Poor adherence to the protocol: less than 30% of the intervention-group achieved the requested intensity
    of 28 h.'
  - Patients were often too tired or ill to practise 1 h per day.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 129
    confidence: high
    flags: []
  source_passages:
  - section: Abstract
    page: 1
    quote: Four weeks of intensive cognitive-linguistic treatment initiated within 2 weeks of stroke is
      not more effective than no language treatment for the recovery of post-stroke aphasia.
    supports: claim
  - section: Methods and patients
    page: 1
    quote: Stroke patients with first-ever aphasia were randomised within 2 weeks of onset to either 4
      weeks of early intensive cognitive-linguistic treatment (1 h/day) or no language treatment.
    supports: sample
  - section: Methods
    page: 2
    quote: RATS-3 is a prospective multicentre controlled clinical trial with randomised treatment allocation,
      open label treatment and blinded evaluation of the primary outcome measure (PROBE-design).
    supports: method
  - section: Results
    page: 129
    quote: 'The adjusted mean difference in scores on the ANELT-A was 0.39; 95% CI: [-2.70 to 3.47], p
      = 0.805'
    supports: statistics
  - section: Statistical analyses
    page: 128
    quote: adjusted for age (years), sex, education (high or low), baseline aphasia severity (ASRS-score),
      type of stroke (ischaemic or haemorrhagic), location of stroke (right or left hemisphere) and baseline
      Barthel Index score.
    supports: confounders
  - section: Discussion
    page: 133
    quote: less than 30% of the intervention-group achieved the requested intensity. Patients were often
      too tired or ill to practise 1 h per day
    supports: limitation
  - section: added by backfill
    page: 1
    quote: We studied whether speech and language therapy early after stroke by way of intensive cognitive-linguistic
      treatment is more effective than no speech and language therapy in the Rotterdam Aphasia Therapy
      Study-3, a multicentre randomised single-blind trial.
    supports: sample
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
---
