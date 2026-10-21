---
schema_version: 2.3
id: left_ifg_pars_opercularis
name: Left Inferior Frontal Gyrus Pars Opercularis
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
hemisphere: left
findings:
- id: f1
  target: speech_repetition
  target_kind: impairment
  claim: Structural damage to Broca's area is associated with impaired speech repetition.
  direction: likely
  relationship: causal
  citation: '@Fridriksson2010'
  method: VLSM
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 39
    population: left hemisphere ischemic stroke
    time_post_onset: within 3 d of hospital admission (some up to 20 d)
    age_range: mean 63.5 years (range 34-85, SD 12)
    handedness: not_reported
    language: Icelandic
    phase: acute
  statistics:
    threshold: 1% false-discovery rate (FDR)
    effect_size: not_reported
    p_value: not_reported
  confounders_controlled:
  - auditory comprehension
  confounders_not_controlled: []
  region_definition:
    kind: data_driven_cluster
    description: Broca's area identified via structural VLBM.
  imaging_details:
    modalities:
    - modality: T1
      voxel_size_mm:
      - 0.9
      - 0.9
      - 0.9
    - modality: DWI
      voxel_size_mm:
      - 1.2
      - 1.2
      - 6.5
    preprocessing_pipeline: SPM5 unified segmentation and normalization algorithm
    reference_space: MNI152
    atlases_used: []
    coordinates_reported:
    - region: Broca's area
      mni:
      - -41
      - 36
      - 10
  author_limitations:
  - The study sample included patients with various aphasia types and other deficits (e.g., apraxia of
    speech), not just pure conduction aphasia.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 3
    confidence: high
    flags:
    - target impairment 'speech_repetition' is forward-looking
  source_passages:
  - section: Results
    page: 3
    quote: Additional structural damage associated with impaired speech repetition was noted in Broca's
      area (-41, 36, 10).
    supports: claim
  - section: Materials and Methods
    page: 2
    quote: Therefore, data from 39 patients were included in the final statistical analyses described
      below.
    supports: sample
  - section: Materials and Methods
    page: 2
    quote: The mean patient age was 63.5 years (range 34-85, SD 12).
    supports: sample
  - section: Materials and Methods
    page: 1
    quote: All participants had incurred a single event ischemic stroke to the left hemisphere
    supports: sample
  - section: Materials and Methods
    page: 2
    quote: The resulting statistical map from the VLBM analysis was corrected for multiple comparisons
      using a 1% false-discovery rate (FDR) threshold
    supports: statistics
  - section: Materials and Methods
    page: 2
    quote: The resulting transforms were used to reslice both the T1 images and lesion maps to an isotropic
      2 mm in standard stereotaxic space
    supports: imaging_details
  - section: Materials and Methods
    page: 2
    quote: computing whether speech repetition performance was correlated with injury to that voxel, using
      the level of auditory comprehension performance as a regressor.
    supports: confounders
  - section: Discussion
    page: 4
    quote: the study sample included some patients who had difficulty repeating due to factors such as
      apraxia of speech, nonfluent aphasia, or auditory comprehension impairment rather than the primary
      repetition impairment seen in conduction aphasia.
    supports: limitation
---
