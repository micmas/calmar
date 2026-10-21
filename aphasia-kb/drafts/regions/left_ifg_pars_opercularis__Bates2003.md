---
schema_version: 2.3
id: left_ifg_pars_opercularis
name: "Left Inferior Frontal Gyrus Pars Opercularis"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-20
hemisphere: left
findings:
  - id: f1
    target: fluency
    target_kind: impairment
    claim: "Damage to Broca's area is not especially important for speech fluency once lesions to the insula have been accounted for."
    direction: no_effect
    relationship: causal
    citation: "@Bates2003"
    method: VLSM
    design: cross-sectional
    strength: moderate
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
    confounders_controlled: ["anterior insula lesion state"]
    confounders_not_controlled: ["lesion volume"]
    region_definition:
      kind: manual_ROI
      description: "Central voxel in Broca's area used as covariate in ANCOVA."
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
        quote: "Broca's area is not especially important for fluency once lesions to the insula have been accounted for"
        supports: claim
---
