---
schema_version: 2.3
id: left_arcuate_fasciculus_slf
name: Left Arcuate Fasciculus and Superior Longitudinal Fascicle (Dorsal Language Pathway)
kind: tract
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
hemisphere: left
members:
- left_superior_temporal_gyrus
- left_ifg_pars_opercularis
findings:
- id: f1
  target: phonological_production
  target_kind: impairment
  claim: Damage to the left dorsal superior longitudinal and arcuate fasciculus is associated with impaired
    speech repetition in acute stroke.
  direction: likely
  relationship: causal
  citation: '@Kummerer2013'
  method: VLSM
  design: cross-sectional
  strength: strong
  evidence_quality: cohort
  sample:
    n: 100
    population: acute left-hemisphere stroke patients with aphasia
    time_post_onset: mean 3 +/- 2.6 days
    age_range: mean 62 years
    handedness: 6 left-handed
    language: native German-speaking
    phase: acute
  statistics:
    threshold: P = 0.01 (FDR corrected)
    effect_size: r = -0.45
    p_value: '0.01'
  confounders_controlled:
  - lesion volume
  - comprehension deficit
  confounders_not_controlled: []
  region_definition:
    kind: data_driven_cluster
    description: Statistical lesion maximum in the periventricular white matter in projection of the dorsal
      SLF and arcuate fasciculus.
  imaging_details:
    field_strength: 3T
    acquisition:
      voxel_size_mm:
      - 1.8
      - 1.8
      - 5
      TR_ms: 3100
      TE_ms: 79
      sequence: DWI
    preprocessing_pipeline: SPM 8 spatial normalization to MNI template
    reference_space: MNI152
    atlases_used: []
    coordinates_reported:
    - region: frontal semioval centre
      mni:
      - -36
      - -20
      - 28
    - region: posterior temporal cortex
      mni:
      - -30
      - -24
      - 8
  author_limitations:
  - Subcortical lesions can be accompanied by cortical hypoperfusion or diaschisis, potentially overestimating
    the structure-function relationship.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, pages 623, 625
    confidence: high
    flags: []
  source_passages:
  - section: Abstract
    page: 1
    quote: repetition impairments were mainly associated with lesions located in the posterior temporoparietal
      region with a statistical lesion maximum in the periventricular white matter in projection of the
      dorsal superior longitudinal and arcuate fasciculus.
    supports: claim
  - section: Materials and methods
    page: 2
    quote: we included 100 native German-speaking patients (mean age 62 years, 67 male, 6 left-handed)
      with acute aphasia caused by ischaemic stroke... who were examined on average 3 +/- 2.6 (SD) days
      after onset.
    supports: sample
  - section: Lesion analysis
    page: 4
    quote: we performed the Brunner-Munzel test, a rank test for continuous behavioural variables and
      binary images to identify lesioned voxels associated with repetition or comprehension deficits.
    supports: method
  - section: Lesion analysis
    page: 4
    quote: The statistical threshold was set to P = 0.01 (using a false discovery rate correction for
      multiple comparisons).
    supports: statistics
  - section: Results
    page: 7
    quote: Significant negative relationships were found in the regression analyses between individual
      damage to dorsal association tracts (i.e. 'dorsal lesion volume') and repetition performance (Spearman
      rank correlation coefficient r = -0.45, P = 0.01, Fig. 4E)
    supports: statistics
  - section: Discussion
    page: 9
    quote: Both cortical hypoperfusion as well as the previously described diaschisis might lead to a
      potential 'overestimation' of the structure-function relationship in acute lesion studies.
    supports: limitation
---
