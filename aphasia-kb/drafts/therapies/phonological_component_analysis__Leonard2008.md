---
schema_version: 2.3
id: phonological_component_analysis
name: Phonological Components Analysis
kind: therapy
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
short_description: A phonologically based naming treatment modeled after Semantic Feature Analysis (SFA)
  where patients identify rhymes, first/final sounds, first sound associates, and syllable counts for
  target items.
targets_impairments:
- anomic_aphasia
findings:
- id: f1
  target: anomic_aphasia
  target_kind: impairment
  claim: Phonological Components Analysis (PCA) treatment significantly improves the naming of treated
    items in individuals with aphasia.
  direction: likely
  relationship: responder
  citation: '@Leonard2008'
  method: behavioral_only
  design: case-series
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 10
    population: individuals with aphasia (6 Broca's, 2 anomic, 1 mixed nonfluent, 1 Wernicke's)
    time_post_onset: '>= 1 year'
    age_range: mean 61.7 years
    handedness: all right-handed
    language: English-speaking
    phase: chronic
  statistics:
    threshold: two standard deviation band method
    effect_size: all averaged effect sizes for all patients were found to be large (Busk and Serlin criteria)
    p_value: not_reported
  confounders_controlled: []
  confounders_not_controlled:
  - lesion volume
  - age
  - time post-stroke
  region_definition:
    kind: not_reported
    description: behavioural-only treatment-efficacy finding — no specific brain region
  imaging_details:
    reference_space: not_reported
    atlases_used: []
  author_limitations:
  - Small sample size limits the power of correlational analyses.
  - The use of picture stimuli introduced a semantic component to the phonological therapy.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, pages 932-933
    confidence: high
    flags: []
  source_passages:
  - section: Outcomes & Results
    page: 2
    quote: Of the 10 individuals, 7 demonstrated notable treatment effects.
    supports: claim
  - section: Participants
    page: 4
    quote: A total of 10 individuals with aphasia participated in this investigation... All participants
      were right-handed, English-speaking individuals who had experienced a single left-hemisphere cerebrovascular
      accident and were at least 1 year post-onset at the time of enrolment.
    supports: sample
  - section: Design and treatment stimuli
    page: 7
    quote: A single-subject multiple-baseline across behaviours design (McReynolds & Kearns, 1983) was
      employed.
    supports: method
  - section: Treatment
    page: 1
    quote: The target picture was presented in the centre of the chart and the participant was asked to
      name it. Irrespective of his/her ability to name the picture, the participant was asked to identify
      five phonological components related to the target item
    supports: method
  - section: Treatment
    page: 11
    quote: The visual analysis of the data indicating a treatment effect is supported statistically using
      the two standard deviation band method
    supports: statistics
  - section: Treatment
    page: 12
    quote: all averaged effect sizes for all patients were found to be large.
    supports: statistics
  - section: Discussion
    page: 16
    quote: it must be acknowledged that the use of picture stimuli in this study meant that there was
      also a semantic component to our therapy approach.
    supports: limitation
  - section: Relationships between pre-treatment tests and response to treatment
    page: 14
    quote: it is acknowledged that due to the small sample size, the power of this analysis is limited.
    supports: limitation
---
This study establishes the efficacy of PCA, a phonological analogue to SFA, for treating anomia across various aphasia types.
