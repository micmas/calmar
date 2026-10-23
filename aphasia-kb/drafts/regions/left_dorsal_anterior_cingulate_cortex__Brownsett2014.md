---
schema_version: 2.6
id: left_dorsal_anterior_cingulate_cortex
name: "Left Dorsal Anterior Cingulate Cortex"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-23
hemisphere: left
findings:
  - id: f1
    target: severity_metric
    target_kind: predictor
    claim: "Activity in the dorsal anterior cingulate cortex and adjacent superior frontal gyrus correlates positively with communicative abilities (picture description) in chronic aphasia, independent of lesion volume and age."
    direction: likely
    relationship: correlational
    citation: "@Brownsett2014"
    method: fMRI_activation
    design: cross-sectional
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 16
      population: "chronic post-stroke aphasia"
      time_post_onset: "at least 6 months (mean 4 years, range 6 months to 11 years)"
      phase: chronic
      age_range: "mean 60 years (range 37-84 years)"
      handedness: "all right-handed"
      language: "English"
    statistics:
      threshold: "Z >= 2.3, corrected P = 0.05"
      effect_size: "r = 0.63"
      p_value: "0.01"
    confounders_controlled:
      - "lesion volume"
      - "age"
    confounders_not_controlled: []
    region_definition:
      kind: data_driven_cluster
      description: "ROI defined by multiplying probabilistic anatomical masks from the FSL Harvard-Oxford Cortical Structural Atlas with functional activity observed in healthy participants during noise-vocoded speech perception."
    imaging_details:
      field_strength: "3T"
      modalities:
        - modality: fMRI
          sequence: "T2*-weighted, gradient-echo, echoplanar imaging (EPI)"
          voxel_size_mm: not_reported
          TR_ms: 8000
          TE_ms: 30
      preprocessing_pipeline: "FSL FEAT 5.98: MCFLIRT realignment, BET non-brain removal, 6mm Gaussian smoothing, grand-mean normalization, high pass temporal filtering, FLIRT registration with cost-function masking"
      reference_space: MNI152
      atlases_used: ["FSL Harvard-Oxford Cortical Structural Atlas"]
    author_limitations:
      - "Small sample size (n=16)."
      - "Univariate statistical analyses may be too insensitive to reveal training-induced functional changes."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 250"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 250
        quote: "The mean performance on the picture description test across the three sessions was then correlated with the mean dACC/SFG activation across three sessions. There was a significant positive correlation (r = 0.63, P = 0.01), with better picture description scores associated with greater dACC/SFG activation."
        supports: claim
      - section: "Materials and methods"
        page: 243
        quote: "only 16 patients (five females, mean age 60 years; range 37-84 years) completed the study."
        supports: sample
      - section: "Materials and methods"
        page: 243
        quote: "All patients were at least 6 months post-stroke (mean 4 years, range 6 months to 11 years)"
        supports: sample
      - section: "Materials and methods"
        page: 244
        quote: "MRI data were obtained on a Philips Intera 3.0 T scanner... Functional magnetic resonance images were obtained using a T2*-weighted, gradient-echo, echoplanar imaging (EPI) sequence... (repetition time, 8.0 s; acquisition time, 2.0 s; echo time, 30 ms; flip angle, 90)"
        supports: imaging_details
      - section: "Materials and methods"
        page: 245
        quote: "Univariate analyses were carried out within the framework of the general linear model using FEAT (FMRI Expert Analysis Tool) Version 5.98, part of FSL... Registration to high resolution structural and Montreal Neurological Institute (MNI) standard space images (MNI 152) were carried out using FMRIB's Linear Image Registration Tool (FLIRT)"
        supports: imaging_details
      - section: "Materials and methods"
        page: 245
        quote: "the theoretically motivated region of interest was defined by multiplying probabilistic anatomical masks from the FSL Harvard-Oxford Cortical Structural Atlas with functional activity observed in healthy participants."
        supports: region_definition
      - section: "Results"
        page: 250
        quote: "The results of the regression indicated that the model was statistically significant and accounted for 50% of the variance [R2 = 0.501, F(3,12) = 4.02, P = 0.03]. It was found that dACC/SFG activation predicted picture description score (beta = 0.56, P = 0.03), but age (beta = 0.16, P = 0.46) and lesion volume did not (beta = -0.28, P = 0.22)"
        supports: statistics
      - section: "Discussion"
        page: 252
        quote: "This study reports conventional univariate statistical analyses, which may be too insensitive to reveal the training-induced functional changes."
        supports: limitation
---
