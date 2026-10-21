---
schema_version: 2.3
id: left_extreme_capsule
name: "Left Extreme Capsule"
kind: tract
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: left
members: ["left_middle_temporal_gyrus", "left_ifg_pars_triangularis", "left_ifg_pars_orbitalis"]
findings:
  - id: f1
    target: form_to_meaning
    target_kind: impairment
    claim: "Damage to the left ventral extreme capsule pathway is associated with impaired auditory comprehension in acute stroke."
    direction: likely
    relationship: causal
    citation: "@Kummerer2013"
    method: VLSM
    design: cross-sectional
    strength: strong
    evidence_quality: cohort
    sample:
      n: 100
      population: "acute left-hemisphere stroke patients with aphasia"
      time_post_onset: "mean 3 +/- 2.6 days"
      age_range: "mean 62 years"
      handedness: "6 left-handed"
      language: "native German-speaking"
    statistics:
      threshold: "P = 0.01 (FDR corrected)"
      effect_size: "r = -0.49"
      p_value: "0.01"
    confounders_controlled: ["lesion volume", "repetition deficit"]
    confounders_not_controlled: []
    region_definition:
      kind: data_driven_cluster
      description: "Statistical lesion maximum between the insular cortex and the putamen in projection of the ventral extreme capsule."
    imaging_details:
      field_strength: "3T"
      acquisition:
        voxel_size_mm: [1.8, 1.8, 5]
        TR_ms: 3100
        TE_ms: 79
        sequence: "DWI"
      preprocessing_pipeline: "SPM 8 spatial normalization to MNI template"
      reference_space: MNI152
      atlases_used: []
      coordinates_reported:
        - region: "ventral most part of the anterior insular cortex (insular apex)"
          mni: [-33, 17, -17]
        - region: "deep white matter between the insular cortex and the putamen"
          mni: [-26, 7, -15]
    author_limitations:
      - "Subcortical lesions can be accompanied by cortical hypoperfusion or diaschisis, potentially overestimating the structure-function relationship."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, pages 623, 625"
      confidence: high
      flags: []
    source_passages:
      - section: "Abstract"
        page: 1
        quote: "lesions associated with comprehension deficits were found more ventral-anterior in the temporoprefrontal region with a statistical lesion maximum between the insular cortex and the putamen in projection of the ventral extreme capsule."
        supports: claim
      - section: "Materials and methods"
        page: 2
        quote: "we included 100 native German-speaking patients (mean age 62 years, 67 male, 6 left-handed) with acute aphasia caused by ischaemic stroke... who were examined on average 3 +/- 2.6 (SD) days after onset."
        supports: sample
      - section: "Lesion analysis"
        page: 4
        quote: "we performed the Brunner-Munzel test, a rank test for continuous behavioural variables and binary images to identify lesioned voxels associated with repetition or comprehension deficits."
        supports: method
      - section: "Lesion analysis"
        page: 4
        quote: "The statistical threshold was set to P = 0.01 (using a false discovery rate correction for multiple comparisons)."
        supports: statistics
      - section: "Results"
        page: 625
        quote: "Significant negative relationships were found in the regression analyses... for damage to ventral association tracts (i.e. 'ventral lesion volume') and comprehension performance (Spearman rank correlation coefficient r = -0.49, P = 0.01, Fig. 4F)"
        supports: statistics
      - section: "Discussion"
        page: 9
        quote: "Both cortical hypoperfusion as well as the previously described diaschisis might lead to a potential 'overestimation' of the structure-function relationship in acute lesion studies."
        supports: limitation
---
