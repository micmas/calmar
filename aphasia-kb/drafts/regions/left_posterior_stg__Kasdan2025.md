---
schema_version: 2.3
id: left_posterior_stg
name: "Left Posterior Superior Temporal Gyrus"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: left
findings:
  - id: f1
    target: rhythm_production
    target_kind: impairment
    claim: "Damage to the left posterior superior temporal gyrus, extending into the supramarginal gyrus and arcuate fasciculus, is associated with impaired rhythm tapping in chronic aphasia."
    direction: likely
    relationship: causal
    citation: "@Kasdan2025"
    method: VLSM
    design: cross-sectional
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 33
      population: "chronic post-stroke aphasia"
      time_post_onset: "approximately 1 yr or more post-stroke"
      age_range: "18-90 years"
      handedness: "27 R; 3 L; 3 Am"
      language: "English"
    statistics:
      threshold: "cluster-based permutation testing with 10,000 iterations; corrected p < 0.05"
      effect_size: "r = -0.48"
      p_value: "0.036"
    confounders_controlled:
      - "total lesion volume"
    confounders_not_controlled: []
    region_definition:
      kind: data_driven_cluster
      description: "Significant cluster in posterior superior temporal gyrus extending into supramarginal gyrus and the posterior segment of the arcuate fasciculus and superior longitudinal fasciculus."
    imaging_details:
      field_strength: not_reported
      preprocessing_pipeline: "Unified Segmentation and enantiomorphic normalization to MNI space; 8 mm FWHM Gaussian kernel smoothing"
      reference_space: MNI152
      atlases_used: ["XTRACT"]
      coordinates_reported:
        - region: "Posterior STG cluster center of mass"
          mni: [-43, -43, 24]
    author_limitations:
      - "Cannot conclude about the role of the right hemisphere as only left hemisphere damage was recruited."
      - "Used brain scans from various time points, including acute scans for some individuals."
      - "LSM ignores non-infarcted tissue changes like leukoaraiosis."
      - "Used a mass univariate approach (VLSM) rather than multivariate techniques."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 14; Table 4"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 14
        quote: "The univariate LSM revealed one significant cluster (p = 0.036) in posterior superior temporal gyrus extending into supramarginal gyrus and the posterior segment of the arcuate fasciculus (AF) and superior longitudinal fasciculus... suggesting that damage to this region is associated with poorer tapping abilities."
        supports: claim
      - section: "Materials and Methods"
        page: 3
        quote: "Thirty-three individuals with chronic, post-stroke aphasia... were in the chronic stage of recovery (approximately 1 yr or more post-stroke)."
        supports: sample
      - section: "Statistical Analyses"
        page: 10
        quote: "Voxel-based LSM (VLSM) analyses were conducted with the vlsm2 function in MATLAB... Total lesion volume was always included as a covariate. Cluster-based permutation testing with 10,000 iterations was used to correct for multiple comparisons and only clusters with corrected p < 0.05 (right-tailed) were considered significant."
        supports: method
      - section: "Results"
        page: 14
        quote: "the proportion of damage to the region of interest from the whole-brain VLSM was correlated with the composite tapping score (r = -0.48, 95% CI = [-0.71, -0.17])"
        supports: statistics
      - section: "Neuroimaging"
        page: 8
        quote: "warped to Montreal Neurological Institute (MNI) space using Unified Segmentation... and enantiomorphic normalization... All lesion images were then smoothed with an 8 mm full-width half-maximum Gaussian kernel"
        supports: imaging_details
      - section: "Discussion"
        page: 18
        quote: "First and foremost, we cannot conclude anything about the role of the right hemisphere in rhythm processing directly from this study; only individuals with left hemisphere damage were recruited."
        supports: limitation
---
