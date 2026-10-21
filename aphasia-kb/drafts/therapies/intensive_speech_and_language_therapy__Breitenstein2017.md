---
schema_version: 2.3
id: intensive_speech_and_language_therapy
name: Intensive Speech and Language Therapy
kind: therapy
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
short_description: Intensive speech and language therapy (>=10 h/week) combining linguistic and communicative-pragmatic
  approaches individualised to the patient.
targets_impairments:
- verbal_communication
- semantics
- syntactic_processing
dosage: '>=10 h per week for 3 weeks'
findings:
- id: f1
  target: verbal_communication
  target_kind: impairment
  claim: Three weeks of intensive speech and language therapy significantly improves verbal communication
    effectiveness in everyday life for patients with chronic aphasia.
  direction: likely
  relationship: causal
  citation: '@Breitenstein2017'
  method: clinical_RCT
  design: RCT
  strength: strong
  evidence_quality: RCT
  sample:
    n: 156
    population: chronic aphasia after stroke
    time_post_onset: '>=6 months'
    age_range: 18-70 years
    handedness: not_reported
    language: German
    phase: chronic
  statistics:
    threshold: p=0.0004
    effect_size: Cohen's d 0.58
  confounders_controlled:
  - treatment centre
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: behavioural-only treatment-efficacy finding
  author_limitations:
  - Low-intensity therapy provided to control group might have supported maintenance of effects.
  - Study did not address whether a critical time window exists for maximum effects.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Summary, page 1
    confidence: high
    flags:
    - target verbal_communication is forward-looking
  source_passages:
  - section: Summary
    page: 1
    quote: Verbal communication was significantly improved from baseline to after intensive speech and
      language treatment... between-group difference Cohen's d 0.58; p=0.0004.
    supports: claim
  - section: Methods
    page: 3
    quote: Inclusion criteria... were chronic aphasia... lasting 6 months or more after an ischaemic or
      haemorrhagic stroke, age 18-70 years, German as first language
    supports: sample
  - section: Discussion
    page: 10
    quote: low intensity speech and language therapy was provided to the control group... we cannot rule
      out that low-intensity therapy after the intensive study intervention could have supported the maintenance
      of the treatment effect.
    supports: limitation
- id: f2
  target: semantics
  target_kind: impairment
  claim: Intensive speech and language therapy significantly improves lexical abilities in patients with
    chronic aphasia.
  direction: likely
  relationship: causal
  citation: '@Breitenstein2017'
  method: clinical_RCT
  design: RCT
  strength: moderate
  evidence_quality: RCT
  sample:
    n: 156
    population: chronic aphasia after stroke
    time_post_onset: '>=6 months'
    age_range: 18-70 years
    handedness: not_reported
    language: German
    phase: chronic
  statistics:
    threshold: p<0.05
    effect_size: not_reported
  confounders_controlled:
  - treatment centre
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: behavioural-only treatment-efficacy finding
  author_limitations:
  - Low-intensity therapy provided to control group might have supported maintenance of effects.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 7
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 7
    quote: Scores on the linguistic screening measure (SAPS... lexicon, syntax...) were significantly
      improved from baseline to after the 3-week intensive therapy compared with from baseline to after
      the 3-week treatment deferral (all p<0.05; table 2; figure 4).
    supports: claim
- id: f3
  target: syntactic_processing
  target_kind: impairment
  claim: Intensive speech and language therapy significantly improves syntactic abilities in patients
    with chronic aphasia.
  direction: likely
  relationship: causal
  citation: '@Breitenstein2017'
  method: clinical_RCT
  design: RCT
  strength: moderate
  evidence_quality: RCT
  sample:
    n: 156
    population: chronic aphasia after stroke
    time_post_onset: '>=6 months'
    age_range: 18-70 years
    handedness: not_reported
    language: German
    phase: chronic
  statistics:
    threshold: p<0.05
    effect_size: not_reported
  confounders_controlled:
  - treatment centre
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: behavioural-only treatment-efficacy finding
  author_limitations:
  - Low-intensity therapy provided to control group might have supported maintenance of effects.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 7
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 7
    quote: Scores on the linguistic screening measure (SAPS... lexicon, syntax...) were significantly
      improved from baseline to after the 3-week intensive therapy compared with from baseline to after
      the 3-week treatment deferral (all p<0.05; table 2; figure 4).
    supports: claim
---
Findings from the FCET2EC trial demonstrate that intensive SLT (>=10h/week) is effective for improving everyday communication and core linguistic functions in chronic aphasia.
