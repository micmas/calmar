---
schema_version: 2.7
id: left_angular_gyrus
name: Left Angular Gyrus
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
hemisphere: left
findings:
- id: f1
  target: alexia
  target_kind: impairment
  claim: The left angular gyrus is a critical region for written language after controlling for verbal
    working memory.
  direction: likely
  relationship: causal
  citation: '@Henseler2014'
  method: VLSM
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 78
    population: chronic left-hemisphere ischemic stroke
    time_post_onset: '>= 12 months'
    age_range: mean 52 (SD 12)
    handedness: all right-handed
    language: native German
    phase: chronic
    cohort: not_reported
  statistics:
    threshold: FDR p < 0.01
    effect_size: not_reported
  confounders_controlled:
  - verbal working memory
  confounders_not_controlled:
  - lesion size
  region_definition:
    kind: data_driven_cluster
    description: VLSM cluster associated with written language after regressing out WMS-R.
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: SPM8 unified segmentation + cost function masking
    reference_space: MNI152
    atlases_used: []
  author_limitations:
  - Chronic aphasia may favour larger lesions, which may sharpen the distinction between syndromes.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 7
    confidence: high
    flags:
    - target alexia is forward-looking
  source_passages:
  - section: Results
    page: 7
    quote: after factoring out verbal working memory, the region around the left angular gyrus remained
      the most critical region for this modality.
    supports: claim
  - section: Materials and methods
    page: 4
    quote: From the large neuropsychological test battery we included a measure of the verbal working
      memory capacity (Wechsler memory scale revised, WMS-R)
    supports: method
  - section: added by backfill
    page: 4
    quote: To grant reasonable levels of statistical power, statistical analyses were restricted to those
      voxels where at least 10% of the patients were lesioned.
    supports: method
  - section: added by backfill
    page: 7
    quote: Therefore we regressed out verbal working memory performance in the VLSM analysis (this was
      done in a subgroup of patients; Table 1).
    supports: method
  - section: added by backfill
    page: 4
    quote: The resulting maps were corrected for multiple comparisons using a 1% false discovery rate
      (FDR corrected P 5 0.01) for the AAT subtests.
    supports: method
  lesion_mapping:
    analysis: univariate
    n_analysed: 78
    min_lesion_overlap: 10% of the sample
    lesion_volume_correction: not_reported
    multiple_comparisons: fdr
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
    - lesion_mapping
---
