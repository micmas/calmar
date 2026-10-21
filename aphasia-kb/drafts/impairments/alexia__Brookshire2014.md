---
schema_version: 2.3
id: alexia
name: Alexia
kind: impairment
short_definition: Acquired reading disorder characterized by an inability to read written words or text.
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
findings:
- id: f1
  target: alexia
  target_kind: impairment
  claim: Alexia is frequent in individuals with chronic aphasia, occurring in approximately 68% of patients.
  direction: likely
  relationship: causal
  citation: '@Brookshire2014'
  method: behavioral_only
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 99
    population: persons with chronic aphasia
    time_post_onset: '>= 6 months'
    age_range: mean 62.02 (SD 13.20)
    handedness: 91 R, 6 L, 2 A
    language: English
    phase: chronic
  statistics:
    threshold: score < 36.67/52 on SAPA Subtest 1 (2 SD below NC mean)
    effect_size: 67.78%
    p_value: not_reported
  confounders_controlled: []
  confounders_not_controlled:
  - motor speech impairments
  region_definition:
    kind: not_reported
    description: behavioral-only frequency finding
  author_limitations:
  - Retrospective analysis of a convenience sample may not be fully representative of the population.
  - Potential co-occurring motor speech impairments (AOS/dysarthria) could have negatively impacted oral
    reading performance.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 8
    confidence: high
    flags:
    - 'new impairment id: alexia'
  source_passages:
  - section: Abstract
    page: 1
    quote: Of the 99 PWA, 68% met our alexia criteria.
    supports: claim
  - section: Method - Participants
    page: 3
    quote: The inclusion criteria for PWA were history of left hemisphere stroke at least 6 months prior
      to enrolment and a diagnosis of aphasia...
    supports: sample
  - section: Results - Frequency of alexia
    page: 8
    quote: Of the 99 PWA, 67 individuals (67.78%) scored more than 2 SD below the NC mean
    supports: statistics
  - section: Discussion - Limitations
    page: 14
    quote: We employed a retrospective analysis of a convenience sample of individuals with chronic aphasia
      that may not have been fully representative of the population...
    supports: limitation
- id: f2
  target: alexia
  target_kind: impairment
  claim: Alexia in chronic aphasia is predominantly sublexical in nature, with significantly greater impairment
    in reading nonwords and pseudohomophones than real words.
  direction: likely
  relationship: causal
  citation: '@Brookshire2014'
  method: behavioral_only
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 67
    population: persons with chronic aphasia and alexia
    time_post_onset: '>= 6 months'
    age_range: mean 62.02 (SD 13.20)
    handedness: 91 R, 6 L, 2 A
    language: English
    phase: chronic
  statistics:
    threshold: p < .001
    effect_size: t(66) = 9.09
    p_value: <.001
  confounders_controlled: []
  confounders_not_controlled:
  - motor speech impairments
  region_definition:
    kind: not_reported
    description: behavioral-only nature of impairment finding
  author_limitations:
  - Only oral reading abilities for single words were assessed; the study does not speak to text comprehension.
  - Lack of access to verbal reading responses precluded a sharp distinction between alexia subtypes.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 9
    confidence: high
    flags:
    - 'new impairment id: alexia'
  source_passages:
  - section: Results - Nature of reading performance
    page: 9
    quote: lexical reading abilities (regular and irregular word reading scores) were significantly higher
      than sublexical reading abilities (pseudohomophones and nonwords reading scores), t(66) = 9.09,
      p < .001, for PWA and alexia.
    supports: claim
  - section: Results - Nature of reading performance
    page: 9
    quote: lexical reading abilities... were significantly higher than sublexical reading abilities...
      t(66) = 9.09, p < .001
    supports: statistics
  - section: Discussion - Limitations
    page: 15
    quote: this study is limited by the fact that only oral reading abilities for single words were assessed,
      and this work does not speak to text comprehension abilities in PWA and alexia.
    supports: limitation
---
Findings from Brookshire et al. (2014) regarding the prevalence and nature of alexia in a chronic aphasia cohort.
