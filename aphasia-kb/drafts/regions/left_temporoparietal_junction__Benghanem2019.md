---
schema_version: 2.7
id: left_temporoparietal_junction
name: Left Temporoparietal Junction
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-22
hemisphere: left
findings:
- id: f1
  target: prognosis
  target_kind: prognosis
  claim: Damage to the left temporoparietal white matter (TPWM) region is associated with poor language
    outcome at 3 months.
  direction: likely
  relationship: causal
  citation: '@Benghanem2019'
  method: LSM
  design: longitudinal
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 73
    population: ischemic stroke in the left middle cerebral artery (MCA) territory
    time_post_onset: 24-48 h
    phase: acute
    age_range: median 63.7 (IQR 52.3-78)
    handedness: not_reported
    language: not_reported
    cohort: not_reported
  statistics:
    threshold: p = 0.002
    effect_size: explained 13.3% of the variance
    p_value: '0.002'
  confounders_controlled: []
  confounders_not_controlled:
  - amount of Speech and Language Therapy
  author_limitations:
  - We only investigated the impact of the lesion of the TPWM area since it was the only area that correlated
    with chronic severity of aphasia in our previous DTI voxel-based study [18].
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 1305
    confidence: high
    flags:
    - region defined based on previous study @Rosso2015
  source_passages:
  - section: Results
    page: 1305
    quote: The intersection index explained 13.3% of the variance (p = 0.002) [of 3-month good outcome].
    supports: claim
  - section: Materials and methods
    page: 1305
    quote: The next step consisted in calculating the percent overlap of each subject's lesion with a
      TPWM region-of-interest as defined in Ref. [18].
    supports: region_definition
  - section: Limitations
    page: 1308
    quote: Third, we only investigated the impact of the lesion of the TPWM area since it was the only
      area that correlated with chronic severity of aphasia in our previous DTI voxel-based study [18]...
    supports: limitation
  - section: added by backfill
    page: 3
    quote: Seventy-three patients were included in the study.
    supports: method
  - section: added by backfill
    page: 5
    quote: the occurrence of DWI abnormalities in this area was a univariate predictor of outcome, with
      a best cutoff value of 20% overlap.
    supports: method
  imaging_details:
    field_strength: 3T
    acquisition:
      sequence: spin-echo multi-slice single-shot echo planar imaging
      voxel_size_mm:
      - not_reported
      - not_reported
      - 5
    preprocessing_pipeline: normalized to MNI space using the Echo-planar imaging (EPI) template provided
      in SPM12
    reference_space: MNI152
    atlases_used: []
  region_definition:
    kind: manual_ROI
    description: Temporoparietal white matter (TPWM) region-of-interest defined in Rosso et al. 2015.
  lesion_mapping:
    analysis: region_based
    n_analysed: 73
    min_lesion_overlap: 20%
    lesion_volume_correction: not_reported
    multiple_comparisons: not_reported
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
    - lesion_mapping
---
