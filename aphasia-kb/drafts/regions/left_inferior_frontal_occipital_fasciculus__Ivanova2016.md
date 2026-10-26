---
schema_version: 2.7
id: left_inferior_frontal_occipital_fasciculus
name: Left Inferior Frontal-Occipital Fasciculus
kind: tract
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
hemisphere: left
findings:
- id: f1
  target: semantics
  target_kind: impairment
  claim: Integrity of the left inferior frontal-occipital fasciculus is significantly related to language
    comprehension in chronic aphasia.
  direction: likely
  relationship: correlational
  citation: '@Ivanova2016'
  method: DTI
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 37
    population: individuals with aphasia due to left hemisphere stroke
    time_post_onset: mean 26.38 months (SD 21.40)
    age_range: 34-78 years
    handedness: all right-handed
    language: native speakers of Russian
    phase: chronic
    cohort: not_reported
  statistics:
    threshold: p < .01
    effect_size: r = .504 (single word comprehension)
  confounders_controlled:
  - age
  - time post-onset
  - lesion size
  confounders_not_controlled: []
  region_definition:
    kind: atlas
    atlas: John Hopkins University White Matter Tractography atlas
    description: Tract masks thresholded with probability value of .25 in MNI space.
  imaging_details:
    field_strength: 1.5T
    modalities:
    - modality: T1
      sequence: high-resolution structural T1-weighted
      voxel_size_mm:
      - 1
      - 1
      - 1
    - modality: DTI
      sequence: spin echo, single shot EPI
      voxel_size_mm:
      - 2.7
      - 2.7
      - 2.7
      TR_ms: 6000
      TE_ms: 95
      b_values:
      - 1000
      n_directions: 20
    preprocessing_pipeline: FSL (eddy_correct, BET, DTIFIT) + SPM-8 (AC-PC reorientation) + Camino (eigenvalue
      extraction)
    reference_space: MNI152
    atlases_used:
    - John Hopkins University White Matter Tractography atlas
  author_limitations:
  - The extent to which language deficits are directly a result of white or grey matter involvement cannot
    be definitively determined as only lesion size (but not location) was used as a covariate.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, Table 3
    confidence: high
    flags: []
  source_passages:
  - section: Abstract
    page: 2
    quote: Language comprehension was predominantly related to integrity of the left IFOF and left ILF
    supports: claim
  - section: Materials and methods
    page: 5
    quote: 'Thirty-seven individuals (18 males, 19 females; Mage = 54 years, SD = 10.53, age range: 34-78
      years) with various types of aphasia were recruited... All participants were right-handed and native
      speakers of Russian.'
    supports: sample
  - section: Materials and methods
    page: 6
    quote: MRI data were acquired using a 1.5T Siemens Avanto scanner.
    supports: imaging_details
  - section: Materials and methods
    page: 6
    quote: The AF, SLF, ILF, IFOF, UF, and CST tract maps for both hemispheres were taken from the John
      Hopkins University White Matter Tractography atlas (Mori et al., 2005)... thresholded with the probability
      value of .25 in MNI space
    supports: region_definition
  - section: Materials and methods
    page: 7
    quote: factoring out effects of age, time post-onset and lesion size... the significance level for
      all statistical comparisons performed was set to .01
    supports: statistics
  - section: Discussion
    page: 12
    quote: It should be acknowledged that the extent to which language deficits are directly a result
      of white or grey matter involvement cannot be definitively determined here, as only lesion size
      (but not location) was used as a covariate in the correlational analyses.
    supports: limitation
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
---
Finding f1: Left IFOF integrity (FA) correlates with single word comprehension scores.
