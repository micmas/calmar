---
schema_version: 2.3
id: left_arcuate_fasciculus
name: "Left Arcuate Fasciculus"
kind: tract
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-20
hemisphere: left
findings:
  - id: f1
    target: phonological_production
    target_kind: impairment
    claim: "Reduced integrity of the left arcuate fasciculus is associated with impaired speech repetition in chronic stroke patients."
    direction: likely
    relationship: correlational
    citation: "@Breier2008"
    method: DTI
    design: cross-sectional
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 20
      population: "chronic left-hemisphere stroke"
      time_post_onset: "mean 22 months (SD 24 months; range 1-72 months)"
      age_range: "38-77 years (mean 58, SD 11)"
      handedness: "all premorbidly right handed"
      language: "not_reported"
    statistics:
      threshold: "P < 0.017"
      effect_size: "F[1,18] = 10.64"
      p_value: "0.004"
    confounders_controlled:
      - "cortical damage to Broca area"
      - "white matter disease (lacunar infarcts/periventricular abnormalities)"
    confounders_not_controlled:
      - "poststroke reorganization"
    region_definition:
      kind: manual_ROI
      description: "FA values obtained in the portion that curves around the depth of the caudal portion of the Sylvian fissure, forming an arc."
    imaging_details:
      field_strength: "3T"
      modalities:
        - modality: DTI
          sequence: "single-shot spin-echo diffusion sensitized echo-planar imaging (EPI)"
          voxel_size_mm: [3, 3, 3]
          TR_ms: 6100
          TE_ms: 84
          n_directions: 21
          b_values: [1000]
      preprocessing_pipeline: "not_reported"
      reference_space: "not_reported"
      atlases_used: ["Mori et al. 2005"]
    author_limitations:
      - "FA decreases may be non-specific, potentially caused by fiber attenuation or multidirectionality."
      - "Use of standard rectangular rather than tailored irregular ROIs may contribute to spuriously decreased FA values."
      - "Poststroke reorganization is a potential confound."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 484"
      confidence: high
      flags: ["reference_space not explicitly stated", "preprocessing_pipeline not reported"]
    source_passages:
      - section: "Results"
        page: 484
        quote: "The relationship between the FA value for the AF and the repetition AQ (F[1,18] 10.64; P 0.004) was significant"
        supports: claim
      - section: "Methods - Participants"
        page: 483
        quote: "Twenty individuals (13 men) with a history of left hemisphere stroke... participated in the study."
        supports: sample
      - section: "Methods - DTI Analyses"
        page: 484
        quote: "Fractional anisotropy (FA) indices for the left and right SLF, AF, and UF were determined in each hemisphere for each patient"
        supports: method
      - section: "Results"
        page: 484
        quote: "The relationship between the FA value for the AF and the repetition AQ (F[1,18] 10.64; P 0.004) was significant"
        supports: statistics
      - section: "Methods - DTI Acquisition"
        page: 483
        quote: "The diffusion-weighted data were acquired using a single-shot spin-echo diffusion sensitized echo-planar imaging (EPI) sequence... a diffusion sensitization of b 1000 s/mm2"
        supports: imaging_details
      - section: "Methods - DTI Analyses"
        page: 484
        quote: "We obtained FA values for the AF in the portion that curves around the depth of the caudal portion of the Sylvian fissure, forming an arc."
        supports: region_definition
      - section: "Discussion"
        page: 486
        quote: "Changes in fiber attenuation, multidirectionality of fibers within sampled voxels, and partial volume averaging because of use of standard rectangular rather than tailored irregular ROIs may all contribute to spuriously decreased FA values."
        supports: limitation
  - id: f2
    target: form_to_meaning
    target_kind: impairment
    claim: "Reduced integrity of the left arcuate fasciculus is marginally associated with comprehension deficits, though this relationship depends on cortical damage."
    direction: likely
    relationship: correlational
    citation: "@Breier2008"
    method: DTI
    design: cross-sectional
    strength: weak
    evidence_quality: cohort
    sample:
      n: 20
      population: "chronic left-hemisphere stroke"
      time_post_onset: "mean 22 months"
      age_range: "38-77 years"
      handedness: "all premorbidly right handed"
      language: "not_reported"
    statistics:
      threshold: "P < 0.017"
      effect_size: "F[1,18] = 6.74"
      p_value: "0.018"
    confounders_controlled:
      - "white matter disease"
    confounders_not_controlled:
      - "cortical damage to temporal lobe"
    region_definition:
      kind: manual_ROI
      description: "FA values obtained in the portion that curves around the depth of the caudal portion of the Sylvian fissure, forming an arc."
    imaging_details:
      field_strength: "3T"
      modalities:
        - modality: DTI
          sequence: "single-shot spin-echo diffusion sensitized echo-planar imaging (EPI)"
          voxel_size_mm: [3, 3, 3]
          TR_ms: 6100
          TE_ms: 84
          n_directions: 21
          b_values: [1000]
      preprocessing_pipeline: "not_reported"
      reference_space: "not_reported"
      atlases_used: ["Mori et al. 2005"]
    author_limitations:
      - "the relationship between damage to the AF and comprehension was not independent of cortical areas within the left hemisphere associated with language comprehension"
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 484"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 484
        quote: "the relationship with the comprehension AQ (F[1,18] 6.74; P 0.018) was marginally significant."
        supports: claim
      - section: "Discussion"
        page: 485
        quote: "the relationship between damage to the AF and comprehension was not independent of cortical areas within the left hemisphere associated with language comprehension (posterior superior, middle temporal, and supramarginal gyri)."
        supports: limitation
---

Findings from Breier 2008 regarding the left arcuate fasciculus and its correlation with repetition and comprehension.
