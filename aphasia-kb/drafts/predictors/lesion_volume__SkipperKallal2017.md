---
schema_version: 2.6
id: lesion_volume
name: Total lesion volume
kind: predictor
predictor_type: imaging_metric
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-23
short_definition: The total volume of the stroke lesion in the left hemisphere.
units: mm3
typical_range: not_reported
direction_of_severity: higher_is_worse
findings:
- id: f1
  target: right_hemisphere_recruitment
  target_kind: region
  claim: Larger left hemisphere lesion volume is associated with increased right hemisphere activity during
    both covert and overt picture naming.
  direction: likely
  relationship: correlational
  citation: '@SkipperKallal2017'
  method: fMRI_activation
  design: cross-sectional
  strength: strong
  evidence_quality: cohort
  sample:
    n: 39
    population: chronic left hemisphere stroke survivors with aphasia
    time_post_onset: at least six months after their stroke (mean chronicity = 52.9 months)
    phase: chronic
    age_range: mean 59.8 (SD 10.1)
    handedness: mixed
    language: native English speakers
  statistics:
    threshold: cluster corrected P < 0.01
    effect_size: not_reported
    p_value: not_reported
  confounders_controlled: []
  confounders_not_controlled: []
  region_definition:
    kind: data_driven_cluster
    description: Right hemisphere areas homotopic to the normal left hemisphere language network, including
      right PTr, posterior STS, and posterior STG.
  imaging_details:
    field_strength: 3.0 T
    modalities:
    - modality: T1
      sequence: MPRAGE
      voxel_size_mm:
      - 1
      - 1
      - 1
      TR_ms: 1900
      TE_ms: 2.56
    - modality: fMRI
      sequence: gradient-echo echo-planar pulse
      voxel_size_mm:
      - 3.2
      - 3.2
      - 3.2
      TR_ms: 2000
      TE_ms: 30
    task:
      name: Delayed naming task
      description: Participants named line drawings silently (covert) then aloud (overt).
      contrasts:
      - covert > fixation
      - overt > fixation
      baseline: fixation
    preprocessing_pipeline: 'FSL 5.0.6: high pass filter, MCFLIRT motion correction, slice timing correction,
      intensity normalization, 5mm FWHM smoothing, registration to MNI'
    reference_space: MNI152
    atlases_used: []
  author_limitations:
  - Right hemisphere activity may reflect increased effort required for language tasks by people with
    larger lesions rather than true plasticity.
  - Right hemisphere activity may reflect recruitment of domain general attentional systems.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 4-5
    confidence: high
    flags:
    - target_id right_hemisphere_recruitment is forward-looking
  source_passages:
  - section: Abstract
    page: 1
    quote: We found that lesion size was positively associated with greater right hemisphere activity
      during both phases of naming
    supports: claim
  - section: Materials and Methods
    page: 3
    quote: Forty-nine chronic left hemisphere stroke survivors with a history of aphasia were recruited.
      Ten participants were then excluded based on fMRI task performance (<10% accuracy) resulting in
      a final sample of 39 participants in the aphasia group.
    supports: sample
  - section: fMRI Analysis
    page: 4
    quote: Lesion size was measured in mm3 after warping to a standardized template and then entered as
      a voxelwise continuous predictor variable in a group analysis.
    supports: method
  - section: fMRI Analysis
    page: 4
    quote: All whole-brain analyses were examined at cluster corrected P < 0.01
    supports: statistics
  - section: Scanning Parameters and Preprocessing
    page: 4
    quote: MRI data were collected on a 3.0 T Siemens Trio Scanner... Registration and normalization were
      carried out to the MNI standardized brain provided by FSL.
    supports: imaging_details
  - section: General Discussion
    page: 12
    quote: This effect may not reflect plasticity at all but rather the increased effort required for
      language tasks by people with larger lesions.
    supports: limitation
---

Notes: Finding f1 targets a forward-looking ID `right_hemisphere_recruitment` to capture the general phenomenon of contralesional shift.
