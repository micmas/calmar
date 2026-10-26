---
schema_version: 2.7
id: constraint_induced_aphasia_therapy
name: Constraint-Induced Aphasia Therapy (CIAT / CILT)
kind: therapy
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-22
short_description: A therapeutic technique requiring intense massed practice of speech acts in a communicative
  environment, constraining the use of non-verbal communication strategies.
targets_impairments:
- fluency
- semantics
- phonological_production
dosage: 3 hours per day minimum for 10 consecutive days (total 30-35 hours)
findings:
- id: f1
  target: severity_metric
  target_kind: predictor
  claim: Constraint-induced aphasia therapy leads to significant improvements in standard clinical language
    tests compared to conventional therapy in chronic aphasia.
  direction: likely
  relationship: responder
  citation: '@Pulvermuller2001'
  method: clinical_RCT
  design: RCT
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 17
    population: chronic aphasia consequent to single stroke affecting the left middle cerebral artery
    time_post_onset: mean [SD], 98.2 [74.2] for CI group; 24 [20.6] for control group
    phase: mixed
    age_range: mean 53.9-55.4 years
    handedness: mostly right-handed (3 ambidextrous)
    language: monolingual native speakers of German
    cohort: not_reported
  statistics:
    threshold: P < 0.0008 (planned comparison for CI group)
    effect_size: cumulative change of 17% for CI group vs 2% for control group
  confounders_controlled:
  - total amount of treatment hours
  confounders_not_controlled:
  - time post-stroke
  region_definition:
    kind: not_reported
    description: behavioural-only treatment-efficacy finding — no specific brain region
  author_limitations:
  - Results are from a single study into a new therapeutic domain.
  - Necessary to investigate whether more intense practice (e.g., 6 hours a day) can further improve outcome.
  - Necessary to investigate if performance increase can be maintained over longer periods.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 1624
    confidence: high
    flags:
    - sample.phase marked as mixed due to wide variance in time post-onset (24 to 98 months)
  source_passages:
  - section: Abstract
    page: 1
    quote: CI aphasia therapy led to significant and pronounced improvements on several standard clinical
      tests, on self-ratings, and on blinded-observer ratings of the patients' communicative effectiveness
      in everyday life.
    supports: claim
  - section: Subjects and Methods
    page: 2
    quote: A total of 17 patients suffering from aphasia were treated. Patients presented with language
      impairment due to a single stroke affecting the territory of the left middle cerebral artery.
    supports: sample
  - section: Subjects and Methods
    page: 2
    quote: Patients were randomly assigned to groups that received either conventional treatment (n=7)
      or CI aphasia therapy (n=10) by a random process.
    supports: method
  - section: Results
    page: 4
    quote: The group that received CI aphasia therapy showed a substantial improvement after the 10-day
      treatment interval (planned comparison, F[1,15]=17.3; P < 0.0008), whereas the group that received
      conventional aphasia treatment did not reveal significant overall improvement (F < 1).
    supports: statistics
  - section: Discussion
    page: 4
    quote: Results presented here are from a single study into a new therapeutic domain. Replication of
      these findings in a larger population of patients is important.
    supports: limitation
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
- id: f2
  target: severity_metric
  target_kind: predictor
  claim: Constraint-induced aphasia therapy significantly increases the amount of verbal communication
    in everyday life for patients with chronic aphasia.
  direction: likely
  relationship: responder
  citation: '@Pulvermuller2001'
  method: behavioral_only
  design: RCT
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 10
    population: chronic aphasia consequent to single stroke affecting the left middle cerebral artery
    time_post_onset: mean [SD], 98.2 [74.2]
    phase: chronic
    age_range: mean 55.4 years
    handedness: mostly right-handed
    language: monolingual native speakers of German
    cohort: not_reported
  statistics:
    threshold: P < 0.001 (self-ratings); P < 0.01 (clinician ratings)
    effect_size: 30% increase in amount of communication (self-ratings); 10% increase (clinician ratings)
  confounders_controlled: []
  confounders_not_controlled:
  - time post-stroke
  region_definition:
    kind: not_reported
    description: behavioural-only treatment-efficacy finding — no specific brain region
  author_limitations:
  - Results are from a single study into a new therapeutic domain.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 4
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 4
    quote: These patients reported a significant increase of 30% in the amount of communication in everyday
      life after treatment (F[1,7]=25.0, P < 0.001; average, 30.1 versus 39.2 points).
    supports: claim
  - section: Results
    page: 4
    quote: This index revealed a quantitative improvement of 10% in communicative activities over the
      brief 10-day treatment interval (F[1,6]=10.5, P < 0.01; average, 31.2 versus 34,4 points).
    supports: statistics
  - section: Discussion
    page: 4
    quote: Results presented here are from a single study into a new therapeutic domain.
    supports: limitation
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
---
