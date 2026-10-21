---
schema_version: 2.3
id: left_temporoparietal_junction
name: Left Temporoparietal Junction
kind: classical
hemisphere: left
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
findings:
- id: f1
  target: prognosis
  target_kind: prognosis
  claim: Damage to the left temporoparietal white matter (TPWM) is associated with poor 3-month functional
    outcome.
  direction: likely
  relationship: causal
  citation: '@Benghanem2019'
  method: LSM
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 73
    population: post-stroke aphasia
    time_post_onset: 24-48 h
    age_range: median 63.7 (IQR 52.3-78)
    handedness: not_reported
    language: not_reported
    phase: mixed
  statistics:
    threshold: p = 0.002
    effect_size: explained 13.3% of the variance
    p_value: '0.002'
  confounders_controlled: []
  confounders_not_controlled:
  - amount of Speech and Language Therapy
  region_definition:
    kind: manual_ROI
    description: Left temporo-parietal white matter (TPWM) region-of-interest as defined in Rosso et al.
      2015.
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: normalized to MNI space using the Echo-planar imaging (EPI) template provided
      in SPM12
    reference_space: MNI152
    atlases_used: []
  author_limitations:
  - Only investigated the impact of the TPWM area, though other areas may be critical.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 1305
    confidence: high
    flags:
    - 'new region id: left_temporoparietal_junction'
  source_passages:
  - section: Results
    page: 3
    quote: The ART at D7, infarct volume, and the intersection index were univariate predictors of good
      outcome at 3 months (AHS 0-2) (Table 2).
    supports: claim
  - section: Results
    page: 3
    quote: The intersection index explained 13.3% of the variance (p = 0.002)
    supports: statistics
  - section: Limitations
    page: 6
    quote: Third, we only investigated the impact of the lesion of the TPWM area... but we acknowledge
      that other areas may be still critical for aphasia outcome
    supports: limitation
- id: f2
  target: prognosis
  target_kind: prognosis
  claim: The predictive value of left temporoparietal junction damage on outcome is significant only in
    patients with initially severe aphasia.
  direction: likely
  relationship: causal
  citation: '@Benghanem2019'
  method: LSM
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 73
    population: post-stroke aphasia
    time_post_onset: day 7
    age_range: median 63.7 (IQR 52.3-78)
    handedness: not_reported
    language: not_reported
    phase: not_reported
  statistics:
    threshold: p = 0.006 for severe; p = 0.19 for mild
    effect_size: not_reported
    p_value: '0.006'
  confounders_controlled:
  - initial severity (ART D7)
  confounders_not_controlled:
  - amount of Speech and Language Therapy
  region_definition:
    kind: manual_ROI
    description: Left temporo-parietal white matter (TPWM) region-of-interest.
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: normalized to MNI space using the Echo-planar imaging (EPI) template provided
      in SPM12
    reference_space: MNI152
    atlases_used: []
  author_limitations:
  - In-sample analysis requiring external validation.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 1306
    confidence: high
    flags:
    - 'new region id: left_temporoparietal_junction'
  source_passages:
  - section: Results
    page: 4
    quote: in the subgroup of 37 patients with ART D7 >= 11, the combined variable had a significant impact
      on outcome (p = 0.006) [whereas] in the subgroup of 36 patients with ART D7 < 11, the combined variable...
      had no significant effect on outcome (p = 0.19).
    supports: claim
  - section: Results
    page: 4
    quote: in the subgroup of 37 patients with ART D7 >= 11, the combined variable had a significant impact
      on outcome (p = 0.006)
    supports: statistics
  - section: Limitations
    page: 1308
    quote: Fourth, our analyses are an in-sample analysis and should be confirmed by independent out-of-sample
      studies
    supports: limitation
---
