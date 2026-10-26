---
schema_version: 2.7
id: right_ifg_pars_triangularis
name: Right Inferior Frontal Gyrus pars triangularis
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
hemisphere: right
findings:
- id: f1
  target: severity_metric
  target_kind: predictor
  claim: In the subacute phase of aphasia recovery, an increase in activation of the right inferior frontal
    gyrus is strongly correlated with improvement in overall language function.
  direction: likely
  relationship: correlational
  citation: '@Saur2006'
  method: fMRI_activation
  design: longitudinal
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 14
    population: aphasia due to an infarction of the left middle cerebral artery territory
    time_post_onset: 'subacute phase (mean: 12.1 dps)'
    age_range: 16-68 years
    handedness: mixed (12 right-handed, 1 left-handed, 1 converted left-handed)
    language: German
    phase: early_subacute
    cohort: not_reported
  statistics:
    threshold: P < 0.001 uncorrected
    effect_size: r = 0.88
    p_value: not_reported
  confounders_controlled: []
  confounders_not_controlled:
  - practice effects
  region_definition:
    kind: peak_coord_sphere
    mni_peak:
    - 54
    - 30
    - 21
    description: Peak activation in the right Broca-homologue (BHo) / IFG pars triangularis during auditory
      comprehension task.
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: fMRI
      sequence: gradient echo echoplanar imaging (EPI) T2*-sensitive
      voxel_size_mm:
      - 3
      - 3
      - 3
      TR_ms: 1830
      TE_ms: 25
    preprocessing_pipeline: SPM2 slice timing, realignment, lesion-mask incorporated normalization (Brett
      et al. 2001), 9mm Gaussian smoothing
    reference_space: MNI152
    atlases_used: []
    coordinates_reported:
    - region: right IFG pars triangularis
      mni:
      - 54
      - 30
      - 21
  author_limitations:
  - The results are limited to somewhat less severely impaired patients who were able to understand the
    task and sustain an fMRI session in the first days after stroke.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 8
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 1
    quote: These upregulated areas also showed the strongest correlation between improved language function
      and increased activation (rBHo = 0.88, rSMA = 0.92).
    supports: claim
  - section: Methods - Subjects
    page: 1
    quote: We examined 14 patients with aphasia due to an infarction of the left middle cerebral artery
      territory...
    supports: sample
  - section: Methods - Statistical analysis
    page: 4
    quote: for the correlation analyses, the statistical threshold was lowered to P < 0.001 uncorrected
      for multiple comparisons across the whole brain.
    supports: statistics
  - section: Methods - Data acquisition
    page: 3
    quote: fMRI was performed on a 3T Siemens TRIO system... using a gradient echo echoplanar imaging
      (EPI) T2*-sensitive sequence [repetition time (TR) = 1.83 s, echo time (TE) = 25 ms... matrix =
      64 * 64, field of view = 192 * 192 mm].
    supports: imaging_details
  - section: Discussion
    page: 12
    quote: the results are limited to somewhat less severely impaired patients who were clearly aphasic
      at the first exam but were able to understand the task.
    supports: limitation
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
---
