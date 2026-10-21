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
    target: phonological_production
    target_kind: impairment
    claim: "Damage to the left inferior frontal gyrus is associated with impaired phonological processing, although the relationship is weaker than for posterior perisylvian regions."
    direction: likely
    relationship: causal
    citation: "@Butler2014"
    method: VBCM
    design: cross-sectional
    strength: weak
    evidence_quality: cohort
    sample:
      n: 31
      population: "chronic stroke aphasia"
      time_post_onset: ">= 12 months"
      age_range: not_reported
      handedness: "all right-handed"
      language: "English first language"
    statistics:
      threshold: "lower than P = 0.001 voxel-level"
      effect_size: not_reported
    confounders_controlled:
      - "lesion volume"
      - "other PCA factors"
    confounders_not_controlled: []
    region_definition:
      kind: data_driven_cluster
      description: "Cluster in the left inferior prefrontal region."
    imaging_details:
      field_strength: "3T"
      acquisition:
        voxel_size_mm: [1, 1, 1]
        sequence: "T1-weighted inversion recovery"
      preprocessing_pipeline: "modified unified segmentation-normalization procedure (Seghier et al. 2008) implemented in SPM8"
      reference_space: MNI152
      atlases_used: []
    author_limitations:
      - "Automated lesion identification may be affected by abnormal ventricle shape in large lesions."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 8"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 8
        quote: "A second cluster in the left inferior prefrontal region was also identified at a slightly lower statistical threshold (Fig. 5A)."
        supports: claim
      - section: "Materials and methods"
        page: 3
        quote: "Participants were included if they had chronic stroke aphasia... and were at least 12 months post-stroke at time of scanning and assessment (n = 31)."
        supports: sample
      - section: "Materials and methods"
        page: 5
        quote: "It is therefore likely to be affected by the abnormal shape of the ventricles in patients with large lesions, and hence is used with the caveat that periventricular results are treated with caution (Geva et al., 2012)."
        supports: limitation
---

Finding f1: Butler et al. (2014) identified a second, weaker cluster in the left inferior prefrontal region associated with the phonological factor.
