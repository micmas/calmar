---
schema_version: 2.7
id: left_hemisphere_intrahemispheric_connectivity
name: Left Hemisphere Intrahemispheric Connectivity
kind: network
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
hemisphere: left
findings:
- id: f1
  target: severity_metric
  target_kind: predictor
  claim: Accurate language performance in stroke patients depends significantly on positive intrahemispheric
    connectivity within the left hemisphere.
  direction: likely
  relationship: correlational
  citation: '@Siegel2016'
  method: rs_fMRI
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 98
    population: subacute stroke patients
    time_post_onset: 1-2 wk after stroke
    phase: early_subacute
    age_range: mean 52.8 y
    handedness: 119 right handed
    language: not_reported
    cohort: not_reported
  statistics:
    threshold: ANOVA P = 1.6 x 10-6
    effect_size: not_reported
    p_value: not_reported
  confounders_controlled:
  - head motion
  confounders_not_controlled: []
  region_definition:
    kind: data_driven_cluster
    description: Positive intrahemispheric weights in the left hemisphere derived from ridge regression
      of FC matrices.
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: fMRI
      sequence: gradient echo EPI
      voxel_size_mm:
      - 4.0
      - 4.0
      - 4.0
      TR_ms: 2000
      TE_ms: 27
    preprocessing_pipeline: FSL FNIRT registration + FreeSurfer surface projection + global signal regression
    reference_space: MNI152
    atlases_used:
    - Gordon et al. 2016 parcellation
  author_limitations:
  - The accuracy of brain network models depends in part on the brain regions used in the models.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 4
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 4
    quote: Language is an exception because a significant prediction comes from positive intra-hemispheric
      weights in the left hemisphere, i.e., accurate language performance depends on communication between
      regions of the left hemisphere.
    supports: claim
  - section: Results
    page: 4
    quote: An ANOVA confirmed a significant difference in the contribution of connection types (P = 1.6
      x 10-6) to deficit prediction
    supports: statistics
  - section: Caveats/Limitations
    page: 7
    quote: The accuracy of brain network models depends in part on the brain regions used in the models.
    supports: limitation
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
---
