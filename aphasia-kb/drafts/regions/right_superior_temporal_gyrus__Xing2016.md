---
schema_version: 2.6
id: right_superior_temporal_gyrus
name: "Right Superior Temporal Gyrus"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: right
findings:
  - id: f1
    target: severity_metric
    target_kind: predictor
    claim: "Greater grey matter volume in the right superior temporal gyrus is positively associated with overall aphasia severity (WAB-R AQ) in chronic stroke, independent of left hemisphere lesion burden."
    direction: likely
    relationship: correlational
    citation: "@Xing2016"
    method: VBM
    design: cross-sectional
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 32
      population: "chronic left hemisphere stroke survivors with aphasia"
      time_post_onset: "at least 6 months post-stroke"
      phase: chronic
      age_range: "mean 59.13 (SD 9.41)"
      handedness: "26/6 (R/L)"
      language: "native English speaker"
    statistics:
      threshold: "cluster-level corrected P = 0.05 (height P = 0.005, k = 323)"
      effect_size: "t = 5.18"
      p_value: "0.0001"
    confounders_controlled:
      - "PCAD (proportion of critical area damaged)"
      - "lesion size"
      - "total volume of grey and white matter"
      - "age"
      - "gender"
      - "education"
      - "handedness"
    confounders_not_controlled: []
    region_definition:
      kind: data_driven_cluster
      description: "Right temporoparietal cluster including the right superior temporal gyrus (peak MNI: 60, -45, 22)."
    imaging_details:
      field_strength: "3.0 T"
      acquisition:
        sequence: "3D T1-weighted (MPRAGE)"
        voxel_size_mm: [1, 1, 1]
        TR_ms: 1900
        TE_ms: 2.56
      preprocessing_pipeline: "VBM8 toolbox in SPM8; joint spatial normalization and segmentation; modulated grey matter volumes; 8mm Gaussian smoothing"
      reference_space: MNI152
      atlases_used: []
      coordinates_reported:
        - region: "right superior temporal gyrus"
          mni: [60, -45, 22]
    author_limitations:
      - "Cross-sectional design prevents definitive causal inference regarding plasticity vs premorbid differences."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 5; Table 2, page 7"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 5
        quote: "The VBM analysis on overall aphasia severity (WAB-R AQ) demonstrated a positive relationship between grey matter volume and AQ in the right temporoparietal cortex including the supramarginal gyrus and posterior superior temporal gyrus"
        supports: claim
      - section: "Materials and methods"
        page: 3
        quote: "Thirty-two chronic left hemisphere stroke survivors with history of aphasia were recruited with inclusion criteria as follows: native English speaker; at least 6 months post-stroke"
        supports: sample
      - section: "Materials and methods"
        page: 4
        quote: "The structural volume preprocessing and analysis were performed using the VBM8 toolbox in Statistical Parametric Mapping software (SPM8)"
        supports: method
      - section: "Statistical analysis"
        page: 4
        quote: "We maintained a cluster-level corrected P = 0.05 significance threshold by applying height and extent thresholds of P = 0.005 and k = 323"
        supports: statistics
      - section: "Discussion"
        page: 12
        quote: "Because we used a cross-sectional design rather than a longitudinal study with one specific intervention, our results suggest that compensation by right hemisphere grey matter structures may serve as a general mechanism of aphasia recovery."
        supports: limitation
  - id: f2
    target: fluency
    target_kind: impairment
    claim: "Greater grey matter volume in the right superior temporal gyrus is positively associated with spontaneous speech scores in chronic stroke."
    direction: likely
    relationship: correlational
    citation: "@Xing2016"
    method: VBM
    design: cross-sectional
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 32
      population: "chronic left hemisphere stroke survivors with aphasia"
      time_post_onset: "at least 6 months post-stroke"
      phase: chronic
      age_range: "mean 59.13 (SD 9.41)"
      handedness: "26/6 (R/L)"
      language: "native English speaker"
    statistics:
      threshold: "cluster-level corrected P = 0.05 (height P = 0.005, k = 323)"
      effect_size: "t = 4.64"
      p_value: "0.0002"
    confounders_controlled:
      - "PCAD"
      - "lesion size"
      - "total volume of grey and white matter"
      - "age"
      - "gender"
      - "education"
      - "handedness"
    confounders_not_controlled: []
    region_definition:
      kind: data_driven_cluster
      description: "Right posterior superior temporal gyrus (peak MNI: 66, -43, 15)."
    imaging_details:
      field_strength: "3.0 T"
      reference_space: MNI152
      atlases_used: []
      coordinates_reported:
        - region: "right superior temporal gyrus"
          mni: [66, -43, 15]
    author_limitations:
      - "Cross-sectional design prevents definitive causal inference regarding plasticity vs premorbid differences."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 5; Table 2, page 7"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 5
        quote: "For Spontaneous Speech, a small area of the right posterior superior temporal gyrus related positively to the scores"
        supports: claim
      - section: "Statistical analysis"
        page: 4
        quote: "We maintained a cluster-level corrected P = 0.05 significance threshold by applying height and extent thresholds of P = 0.005 and k = 323"
        supports: statistics
      - section: "Discussion"
        page: 12
        quote: "Because we used a cross-sectional design rather than a longitudinal study with one specific intervention, our results suggest that compensation by right hemisphere grey matter structures may serve as a general mechanism of aphasia recovery."
        supports: limitation
---
