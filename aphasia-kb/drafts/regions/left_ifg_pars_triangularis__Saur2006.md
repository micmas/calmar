---
schema_version: 2.3
id: left_ifg_pars_triangularis
name: "Left Inferior Frontal Gyrus pars triangularis"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: left
findings:
  - id: f1
    target: severity_metric
    target_kind: predictor
    claim: "In the acute phase post-stroke, better initial language performance is positively correlated with higher activation in the left inferior frontal gyrus."
    direction: likely
    relationship: correlational
    citation: "@Saur2006"
    method: fMRI_activation
    design: longitudinal
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 14
      population: "aphasia due to an infarction of the left middle cerebral artery territory"
      time_post_onset: "acute phase (mean: 1.8 dps)"
      age_range: "16-68 years"
      handedness: "mixed"
      language: "German"
    statistics:
      threshold: "P < 0.001 uncorrected"
      effect_size: "r = 0.93"
      p_value: "< 0.001"
    confounders_controlled: []
    confounders_not_controlled: ["lesion location (some peaks in infarcted tissue)"]
    region_definition:
      kind: data_driven_cluster
      description: "Clusters in the left IFG identified via linear regression of LRSEx1 with language activation."
    imaging_details:
      field_strength: "3T"
      modalities:
        - modality: fMRI
          sequence: "gradient echo echoplanar imaging (EPI) T2*-sensitive"
          voxel_size_mm: [3, 3, 3]
          TR_ms: 1830
          TE_ms: 25
      preprocessing_pipeline: "SPM2 slice timing, realignment, lesion-mask incorporated normalization (Brett et al. 2001), 9mm Gaussian smoothing"
      reference_space: "MNI152"
      atlases_used: []
    author_limitations:
      - "The results are limited to somewhat less severely impaired patients who were able to understand the task and sustain an fMRI session in the first days after stroke."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 7"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 7
        quote: "In the acute phase, there was a strong positive linear correlation of LRSEx1 with language activation with two large clusters in the left IFG (r = 0.93, P < 0.001)..."
        supports: claim
      - section: "Methods - Subjects"
        page: 2
        quote: "We examined 14 patients with aphasia due to an infarction of the left middle cerebral artery territory..."
        supports: sample
      - section: "Methods - Statistical analysis"
        page: 4
        quote: "for the correlation analyses, the statistical threshold was lowered to P < 0.001 uncorrected for multiple comparisons across the whole brain."
        supports: statistics
      - section: "Discussion"
        page: 12
        quote: "the results are limited to somewhat less severely impaired patients who were clearly aphasic at the first exam but were able to understand the task."
        supports: limitation
---
