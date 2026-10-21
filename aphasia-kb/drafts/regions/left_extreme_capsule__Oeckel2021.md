---
schema_version: 2.6
id: left_extreme_capsule
name: "Left Extreme Capsule"
kind: tract
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: left
findings:
  - id: f1
    target: aphasia
    target_kind: impairment
    claim: "Damage to the left extreme capsule (specifically >15% overlap) is a strong independent predictor of aphasia in acute stroke patients without cortical language area lesions."
    direction: likely
    relationship: causal
    citation: "@Oeckel2021"
    method: LSM
    design: cross-sectional
    strength: strong
    evidence_quality: cohort
    sample:
      n: 123
      population: "acute left-hemispheric stroke patients without lesions of language-related cortical areas"
      time_post_onset: "<10 days"
      phase: acute
      age_range: "< 90 years"
      handedness: not_reported
      language: "German native speaker"
    statistics:
      threshold: "P < 0.01"
      effect_size: "OR 16.37"
      ci_95: "[3.11, 86.16]"
    confounders_controlled:
      - "arcuate fascicle lesions"
      - "stroke volume"
      - "age"
      - "gender"
    confounders_not_controlled: []
    region_definition:
      kind: tract
      description: "Extreme capsule fibre (ECF) system quantified via global fibre tractography and slice-plane overlap percentage."
    imaging_details:
      field_strength: "3T"
      modalities:
        - modality: DTI
          sequence: "diffusion-sensitive single-shot spin-echo echo-planar imaging"
          voxel_size_mm: [2, 2, 2]
          TR_ms: 11800
          TE_ms: 96
          n_directions: 61
          b_values: [0, 1000]
        - modality: T1
          sequence: "magnetization-prepared rapid gradient echo"
          voxel_size_mm: [1, 1, 1]
          TR_ms: 2200
          TE_ms: 4.11
      preprocessing_pipeline: "MATLAB-based in-house toolbox for fibre tracking"
      reference_space: not_reported
      atlases_used: ["Stanford atlas of functional regions of interest"]
    author_limitations:
      - "The size of the study cohort of 123 stroke patients including 18 (14.6%) with aphasia may be considered as a study limitation."
      - "The Stanford atlas does not include all brain regions potentially involved in language processing."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 7"
      confidence: high
      flags: []
    source_passages:
      - section: "Abstract"
        page: 1
        quote: "More than 15% damage of the slice plane through the extreme capsule was a strong independent predictor of aphasia in stroke patients, odds ratio 16.37, 95% confidence interval: 3.11-86.16, P < 0.01."
        supports: claim
      - section: "Materials and methods"
        page: 3
        quote: "The inclusion criteria were (i) embolic first-time stroke of the left middle cerebral artery-territory, (ii) age < 90 years and (iii) German native speaker."
        supports: sample
      - section: "Materials and methods"
        page: 3
        quote: "We explored the anatomical region 'extreme capsule' and its relation to the syndrome 'aphasia' as tested by the Aachen Aphasia Test (AAT) [...] in patients with acute (<10 days) first ever stroke due to a singular ischaemic infarct of the left hemisphere."
        supports: method
      - section: "Materials and methods"
        page: 3
        quote: "MRI acquisition: on a 3-T TIM TRIO scanner [...] diffusion-sensitive single-shot spin-echo echo-planar imaging sequence was acquired with the following parameters: 61 diffusion encoding gradient directions (b-factor, 1000s/mm2); repetition time, 11 800ms; echo time, 96ms; inversion time, 2300ms; [...] voxel size, 2 mm x 2 mm x 2 mm."
        supports: imaging_details
      - section: "Discussion"
        page: 8
        quote: "The size of the study cohort of 123 stroke patients including 18 (14.6%) with aphasia may be considered as a study limitation."
        supports: limitation
---
