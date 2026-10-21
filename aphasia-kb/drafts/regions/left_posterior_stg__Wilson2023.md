---
schema_version: 2.6
id: left_posterior_stg
name: "Left Posterior Superior Temporal Gyrus"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: left
findings:
  - id: f1
    target: syntactic_processing
    target_kind: impairment
    claim: "Extensive damage to the left posterior temporoparietal cortex, including the posterior superior temporal gyrus, is associated with ubiquitous and persistent deficits in sentence comprehension."
    direction: likely
    relationship: causal
    citation: "@Wilson2023"
    method: LSM
    design: longitudinal
    strength: strong
    evidence_quality: cohort
    sample:
      n: 218
      population: "individuals with aphasia after left hemisphere stroke"
      time_post_onset: "1-5 days to 1 year"
      phase: longitudinal
      age_range: "mean 62.6 (SD 13.6)"
      handedness: "193 R; 20 L; 5 Am"
      language: "English"
    statistics:
      threshold: "not_reported"
      effect_size: "not_reported"
      p_value: "not_reported"
    confounders_controlled: ["lesion extent", "lesion location"]
    confounders_not_controlled: []
    region_definition:
      kind: data_driven_cluster
      description: "Part of the TP+ (Temporal or temporoparietal, more extensive) and FTP (Complete perisylvian) groups, with complete overlap in the posterior superior temporal gyrus."
    author_limitations:
      - "Lesions were identified based only on acute clinical imaging... reconstructed lesions may not reflect the exact location and extent of irreversible tissue damage."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results - Temporal or temporoparietal, more extensive: TP+, page 1030"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 1030
        quote: "Lesion overlap was complete in the posterior superior temporal gyrus... Sentence comprehension remained significantly impaired in all patients throughout the year."
        supports: claim
      - section: "Materials and methods"
        page: 1025
        quote: "Lesions were manually delineated using ITK-SNAP version 3.6.0... DWI images were coregistered to FLAIR images... warped to Montreal Neurological Institute (MNI) space using Unified Segmentation"
        supports: method
      - section: "Results"
        page: 1030
        quote: "All patients had severe aphasia on initial evaluation (two were untestable)."
        supports: sample
      - section: "Limitations"
        page: 1036
        quote: "these limitations entail that reconstructed lesions may not reflect the exact location and extent of irreversible tissue damage in all patients."
        supports: limitation
    imaging_details:
      reference_space: MNI152
      atlases_used: []
      preprocessing_pipeline: "ITK-SNAP delineation + SPM12 Unified Segmentation + enantiomorphic normalization"
---
