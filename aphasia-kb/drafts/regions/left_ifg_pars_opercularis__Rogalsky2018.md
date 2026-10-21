---
schema_version: 2.3
id: left_ifg_pars_opercularis
name: Left Inferior Frontal Gyrus Pars Opercularis
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
hemisphere: left
findings:
- id: f1
  target: syntactic_processing
  target_kind: impairment
  claim: Damage to Broca's area (including pars opercularis and pars triangularis) is not causally associated
    with agrammatic sentence comprehension patterns in chronic patients.
  direction: no_effect
  relationship: causal
  citation: '@Rogalsky2018'
  method:
  - VLSM
  - behavioral_only
  design: cross-sectional
  strength: strong
  evidence_quality: cohort
  sample:
    n: 66
    population: chronic left-hemisphere stroke and unilateral left temporal lobectomy patients
    time_post_onset: 6 months or more postonset
    age_range: mean 62 (stroke), 46 (lobectomy)
    handedness: vast majority strongly right-handed
    language: native speakers of English
    phase: chronic
  statistics:
    threshold: p < .001, corrected
    effect_size: not_reported
  confounders_controlled:
  - lesion size
  confounders_not_controlled: []
  region_definition:
    kind: manual_ROI
    description: Posterior two thirds of the left inferior frontal gyrus, that is, the pars triangularis
      and pars opercularis.
  imaging_details:
    field_strength: not_reported
    preprocessing_pipeline: MAP-3 lesion analysis methods implemented on Brainvox software
    reference_space: Talairach
    atlases_used: []
  author_limitations:
  - The temporal lobectomy group may have experienced functional neural reorganization.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: 'Results: Behavioral Results, page 10'
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 10
    quote: The Broca's area group exhibited no significant difference between object-relative and subject-relative
      performance... as well as between passive and active performance
    supports: claim
  - section: Results
    page: 12
    quote: these findings align with the agrammatic comprehension lesion distribution results, implicating
      temporal and inferior parietal damage (but not frontal lobe damage) in agrammatic comprehension.
    supports: claim
  - section: Methods
    page: 8
    quote: Patients with damage anywhere in Broca's area, defined as the posterior two thirds of the left
      inferior frontal gyrus, that is, the pars triangularis and pars opercularis...
    supports: region_definition
  - section: Discussion
    page: 16
    quote: The finding that damage to Broca's area is not reliably associated with agrammatic comprehension
      coincides with previous lesion work
    supports: claim
---
