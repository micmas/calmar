---
schema_version: 2.7
id: executive_functions
name: Executive Functions
kind: predictor
predictor_type: behavioural
short_definition: Higher-order cognitive processes including planning, working memory, and mental flexibility.
assessment:
- Cognitive-Linguistic Quick Test
- Raven's Colored Progressive Matrices
- Geometric Inclusion
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-23
findings:
- id: f1
  target: naming
  target_kind: impairment
  claim: Higher pretreatment executive function significantly predicts greater immediate and maintained
    gains following semantic-based naming therapy.
  direction: likely
  relationship: responder
  citation: '@Gilmore2019'
  method: behavioral_only
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 27
    population: persons with poststroke aphasia
    time_post_onset: mean 54.49 months (SD 51.92)
    phase: chronic
    age_range: mean 62.71 (SD 10.31)
    handedness: not_reported
    language: not_reported
    cohort: not_reported
  statistics:
    threshold: P < .05
    effect_size: 1-unit increase predicts .29 increase in PMG and .28 increase in PMGM
    p_value: '.05'
  confounders_controlled:
  - pretreatment apraxia of speech
  - auditory comprehension impairment
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: Behavioural predictor; no specific brain region targeted.
  author_limitations:
  - Small sample size may have resulted in an under-powered analysis.
  - Lack of gold standard assessments for nonlinguistic cognition in aphasia; performance may be confounded
    by speech, language, or motor impairments.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results - Study 2, pages 5-6
    confidence: high
    flags: []
  source_passages:
  - section: Results - Study 2
    page: 6
    quote: only executive function, visual short-term memory, and auditory comprehension were significant
      predictors, with 1-unit increases in each ability predicting .29 (P<.05), .30 (P<.05), and .41 (P<.05)
      increases in PMG, respectively.
    supports: claim
  - section: Results - Study 2
    page: 6
    quote: only executive function and visual short-term memory were significant predictors, with 1-unit
      increases predicting increases in PMGM of .28 (P<.05) and .33 (P<.05), respectively.
    supports: statistics
  - section: Methods - Study 2
    page: 3
    quote: subset of 27 participants from study 1 who received a semantic-based naming treatment
    supports: sample
  - section: Study limitations
    page: 7
    quote: The findings may have been affected by sample size (ie, under-powered principal components
      analyses), especially in study 2 (n=27).
    supports: limitation
  - section: Study limitations
    page: 7
    quote: there are currently no gold standard assessments for assessing nonlinguistic cognition in aphasia...
      participants' performance... may have been negatively affected by speech... language... or motor
      impairment.
    supports: limitation
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
---
