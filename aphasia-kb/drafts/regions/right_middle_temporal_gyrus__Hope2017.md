---
schema_version: 2.3
id: right_middle_temporal_gyrus
name: Right Middle Temporal Gyrus
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
hemisphere: right
findings:
- id: f1
  target: anomic_aphasia
  target_kind: impairment
  claim: Hypertrophy in the right middle temporal gyrus is associated with improvement in spoken object
    naming in chronic aphasia.
  direction: likely
  relationship: correlational
  citation: '@Hope2017'
  method: VBM
  design: longitudinal
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 28
    population: right-handed left-hemisphere stroke patients
    time_post_onset: T1 > 1 year; mean T1 50.7 months, mean T2 80.4 months
    age_range: mean 51.7 years (SD 10.4)
    handedness: all right-handed
    language: English first language
    phase: longitudinal
  statistics:
    threshold: permutation thresholding (P < 0.05), cluster extent > 30 voxels
    effect_size: r = 0.88 (cross-validation positive-only)
    p_value: '0.001'
  confounders_controlled:
  - lesion volume
  - age at stroke onset
  - time post-stroke at T1
  - task score at T1
  confounders_not_controlled: []
  region_definition:
    kind: data_driven_cluster
    description: VBM cluster on the right middle temporal gyrus associating increasing grey matter with
      increasing task score.
  imaging_details:
    reference_space: MNI152
    preprocessing_pipeline: SPM 2012 + modified unified segmentation (Seghier et al. 2008) + 8mm Gaussian
      smoothing
    atlases_used: []
    coordinates_reported:
    - region: peak positive cluster
      mni:
      - 48
      - -6
      - -30
  author_limitations:
  - The distinction between improvers and decliners might reflect subtle multivariate distinctions or
    variable patterns of everyday language use.
  - The relationship between impairment-based measures and day-to-day experiences of language use might
    be complex.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 1722
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 1722
    quote: The 'positive' clusters (i.e. associating increasing grey matter with increasing task score
      and vice versa) were both on the right middle temporal gyrus...
    supports: claim
  - section: Materials and methods
    page: 3
    quote: 'Summary details of the 28 patients who met these criteria are as follows: 10 females; mean/standard
      deviation (SD) of age at stroke onset = 51.7/10.4 years; mean/SD of time post-stroke when assessed
      = (T1) 50.7/43.7 months; (T2) 80.4/53.5 months...'
    supports: sample
  - section: Materials and methods
    page: 1720
    quote: 'Voxel-wise associations between rate of brain structure change and rate of behavioural change...
      were measured as partial correlations... while accounting for: lesion volume, age at stroke onset,
      time post-stroke at T1, and task score at T1.'
    supports: method
  - section: Materials and methods
    page: 4
    quote: The results were corrected for multiple comparisons using permutation thresholding (Rorden
      et al., 2009), with 10 000 permutations (P < 0.05), and a cluster extent threshold of 30 voxels
      was applied to the results.
    supports: statistics
  - section: Materials and methods
    page: 4
    quote: Preprocessed with Statistical Parametric Mapping software (SPM, 2012), these images were spatially
      normalized into Montreal Neurological Institute (MNI) space using a modified version of the unified
      segmentation algorithm (Ashburner and Friston, 2005) that has been optimized for use in patients
      with focal brain lesions (Seghier et al., 2008).
    supports: imaging_details
  - section: Discussion
    page: 9
    quote: The distinction between improvers and decliners might reflect some more subtle (e.g. more multivariate)
      distinction between the patients, or it might reflect variable patterns of everyday language use...
    supports: limitation
---
# Right Middle Temporal Gyrus

This region is associated with longitudinal improvement in object naming in chronic aphasia via structural adaptation (hypertrophy).
