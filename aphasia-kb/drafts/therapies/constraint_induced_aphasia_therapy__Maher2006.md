---
schema_version: 2.6
id: constraint_induced_aphasia_therapy
name: Constraint-Induced Aphasia Therapy (CIAT / CILT)
kind: therapy
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-22
targets_impairments:
- fluency
- semantics
short_description: A language rehabilitation approach applying principles of use-dependent learning by
  restricting communication to the spoken modality and employing massed practice.
findings:
- id: f1
  target: severity_metric
  target_kind: predictor
  claim: Intensive Constraint Induced Language Therapy (CILT) leads to significant improvements in overall
    aphasia severity (WAB-AQ) in chronic aphasia, with gains maintained or increased at one-month follow-up.
  direction: likely
  relationship: causal
  citation: '@Maher2006'
  method: behavioral_only
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 4
    population: chronic left-hemisphere stroke aphasia
    time_post_onset: at least one year prior
    phase: chronic
    age_range: mean 48 (SD not reported)
    handedness: right-handed
    language: English
  statistics:
    threshold: p = .004
    effect_size: f = 17.58
    p_value: 0.004
  confounders_controlled:
  - treatment intensity
  - nature of therapeutic activities
  confounders_not_controlled:
  - apraxia of speech severity
  region_definition:
    kind: not_reported
    description: behavioural-only treatment-efficacy finding — no specific brain region
  author_limitations:
  - Sample of convenience, not a randomized clinical trial.
  - Small sample size limits generalizability.
  - Lack of blinded scoring for all measures.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 847
    confidence: high
    flags:
    - sample n for CILT group is 4 based on Table 2 and text (5 started, 1 withdrew)
  source_passages:
  - section: Results
    page: 847
    quote: Using repeated measures ANOVA, both groups demonstrated significant change pre- to post-therapy
      on the WAB ( f = 17.58, p = .004).
    supports: statistics
  - section: Results
    page: 847
    quote: three of the four participants in the CILT group showed change of 5 points or more on the WAB
      AQ... and this gain was further increased at the one-month follow-up.
    supports: claim
  - section: Subjects
    page: 845
    quote: Inclusion criteria were a single, left hemisphere CVA at least one year prior (confirmed by
      CT or MRI), right hand dominance, and English speaking...
    supports: sample
  - section: Discussion
    page: 849
    quote: First, this was a sample of convenience, not a randomized clinical trial.
    supports: limitation
- id: f2
  target: fluency
  target_kind: impairment
  claim: CILT participants showed more consistent improvement in narrative discourse (story retelling)
    compared to a comparison group allowing multiple modalities.
  direction: likely
  relationship: causal
  citation: '@Maher2006'
  method: behavioral_only
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 4
    population: chronic left-hemisphere stroke aphasia
    time_post_onset: at least one year prior
    phase: chronic
    age_range: mean 48
    handedness: right-handed
    language: English
  statistics:
    threshold: subjective assessment by blinded raters
    effect_size: not_reported
    p_value: not_reported
  confounders_controlled:
  - treatment intensity
  - nature of therapeutic activities
  confounders_not_controlled:
  - apraxia of speech severity
  region_definition:
    kind: not_reported
    description: behavioural-only treatment-efficacy finding — no specific brain region
  author_limitations:
  - Small sample size prevents firm conclusions.
  - Blinded experts' specific judgment criteria were not clear.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 848
    confidence: high
    flags: []
  source_passages:
  - section: Abstract
    page: 843
    quote: CILT participants showed more consistent improvement on standard aphasia measures and clinician
      judgments of narrative discourse.
    supports: claim
  - section: Results
    page: 848
    quote: the overall picture for the CILT group is one of improved story re-telling following therapy.
    supports: claim
  - section: Discussion
    page: 848
    quote: Because firm conclusions cannot be made on such a limited sample, and it is not clear upon
      what the blinded experts were basing their judgments...
    supports: limitation
---

# Draft Entry for Constraint Induced Aphasia Therapy

This pilot study investigated the efficacy of Constraint Induced Language Therapy (CILT) in chronic aphasia, specifically testing whether restricting communication to the spoken modality (forced use) provides an advantage over a modified PACE approach that allows multiple modalities, while keeping intensity and task nature constant.
