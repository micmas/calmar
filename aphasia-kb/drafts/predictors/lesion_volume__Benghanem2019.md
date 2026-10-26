---
schema_version: 2.7
id: lesion_volume
name: Total lesion volume
kind: predictor
predictor_type: imaging_metric
short_definition: The total volume of the infarct lesion.
units: ml
typical_range: not_reported
direction_of_severity: higher_is_worse
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-22
findings:
- id: f1
  target: prognosis
  target_kind: prognosis
  claim: Large infarct volume (>= 50 ml) is associated with poor language outcome at 3 months, particularly
    in patients with initially severe aphasia.
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
    threshold: p = 0.001
    effect_size: explained 19.7% of the variance
    p_value: '0.001'
  confounders_controlled: []
  confounders_not_controlled:
  - amount of Speech and Language Therapy
  author_limitations:
  - We may have underestimated the stroke volume in the MNI normalised images since we did not use lesion
    masking in the process.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 1305
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 1305
    quote: The infarct volume explained 19.7% of the variance (p = 0.001) [of 3-month good outcome].
    supports: claim
  - section: Materials and methods
    page: 1305
    quote: Infarct volume was defined as abnormal hyper-intense regions observed on the DW images (b =
      1000s/mm2) and was measured using interactive manual outlining with the MRIcron software.
    supports: method
  - section: Limitations
    page: 1308
    quote: Finally, we may have underestimated the stroke volume in the MNI normalised images since we
      did not use lesion masking in the process.
    supports: limitation
  - section: added by backfill
    page: 3
    quote: Seventy-three patients were included in the study.
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
    kind: not_reported
  lesion_mapping:
    analysis: region_based
    n_analysed: 73
    min_lesion_overlap: not_reported
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
