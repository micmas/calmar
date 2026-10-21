---
schema_version: 2.3
id: left_precentral_gyrus_insula
name: "Left Precentral Gyrus of the Insula"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-20
hemisphere: left
findings:
  - id: f1
    target: fluency
    target_kind: impairment
    claim: "Damage to the left anterior insula is strongly associated with reduced speech fluency."
    direction: likely
    relationship: causal
    citation: "@Bates2003"
    method: VLSM
    design: cross-sectional
    strength: strong
    evidence_quality: cohort
    sample:
      n: 101
      population: "left-hemisphere-damaged aphasic patients"
      time_post_onset: "at least one year after stroke"
      age_range: not_reported
      handedness: not_reported
      language: "native English speakers"
    statistics:
      threshold: "P = 0.05 (controlling the expected proportion of false positives)"
      effect_size: not_reported
    confounders_controlled: []
    confounders_not_controlled: ["lesion volume"]
    region_definition:
      kind: data_driven_cluster
      description: "Voxel-based lesion-symptom mapping peak for fluency."
    imaging_details:
      reference_space: other
      atlases_used: []
      preprocessing_pipeline: "Lesions reconstructed onto templates by a board-certified neurologist."
    author_limitations:
      - "An area may emerge as relevant either because it has a direct causal role or because of a diaschitic effect."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 449"
      confidence: high
      flags: ["reference_space is described as stereotactic templates but specific atlas not named"]
    source_passages:
      - section: "Results"
        page: 449
        quote: "Fluency was most affected by lesions in the insula"
        supports: claim
      - section: "Methods"
        page: 449
        quote: "We analyzed data on speech fluency and language comprehension for 101 left-hemisphere-injured stroke patients"
        supports: sample
      - section: "Figure 1 caption"
        page: 449
        quote: "Only voxels that were significant at P = 0.05 (controlling the expected proportion of false positives) are shown."
        supports: statistics
      - section: "Discussion"
        page: 450
        quote: "an area may emerge as relevant either because it has a direct causal role or because of a diaschitic effect"
        supports: limitation
  - id: f2
    target: fluency
    target_kind: impairment
    claim: "The anterior insula is critical for speech fluency independently of damage to Broca's area."
    direction: likely
    relationship: causal
    citation: "@Bates2003"
    method: VLSM
    design: cross-sectional
    strength: strong
    evidence_quality: cohort
    sample:
      n: 101
      population: "left-hemisphere-damaged aphasic patients"
      time_post_onset: "at least one year after stroke"
      age_range: not_reported
      handedness: not_reported
      language: "native English speakers"
    statistics:
      threshold: not_reported
      effect_size: not_reported
    confounders_controlled: ["Broca's area lesion state"]
    confounders_not_controlled: ["lesion volume"]
    region_definition:
      kind: manual_ROI
      description: "Central voxel in the anterior insula used as covariate in ANCOVA."
    imaging_details:
      reference_space: other
      atlases_used: []
    author_limitations:
      - "An area may emerge as relevant either because it has a direct causal role or because of a diaschitic effect."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 450"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 450
        quote: "These maps showed that the anterior insula is critical for fluency, independent of Broca's area"
        supports: claim
      - section: "Results"
        page: 450
        quote: "We constructed four maps factoring out the effects of these voxels by carrying out analyses of covariance (ANCOVAs)"
        supports: method
---
