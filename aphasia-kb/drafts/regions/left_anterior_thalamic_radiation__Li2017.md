---
schema_version: 2.6
id: left_anterior_thalamic_radiation
name: "Left Anterior Thalamic Radiation"
kind: tract
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: left
findings:
  - id: f1
    target: fluency
    target_kind: impairment
    claim: "Damage to the left anterior thalamic radiation is associated with deficits in both semantic and phonological verbal fluency."
    direction: likely
    relationship: causal
    citation: "@Li2017"
    method: [LSM, DTI]
    design: cross-sectional
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 51
      population: "right-handed stroke patients"
      time_post_onset: "at least 1-month post-onset (mean=11.9 months)"
      phase: chronic
      age_range: "mean 46.8 years (SD=11.0)"
      handedness: "all right-handed"
      language: "native Chinese speakers"
    statistics:
      threshold: "Bonferroni corrected (p < 0.0026 for lesion; p < 0.0023 for FA)"
      effect_size: "lesion r=-0.39 to -0.50; FA r=0.48 to 0.63"
    confounders_controlled:
      - "total lesion volume"
      - "type of aphasia"
      - "duration of illness"
      - "nonverbal control tasks"
    confounders_not_controlled: []
    region_definition:
      kind: atlas
      atlas: "JHU white-matter tractography atlas"
      description: "Left anterior thalamic radiation (ATR) extracted from JHU atlas"
    imaging_details:
      field_strength: "1.5T"
      modalities:
        - modality: T1
          sequence: MPRAGE
          voxel_size_mm: [0.49, 0.49, 0.70]
        - modality: DWI
          voxel_size_mm: [1.95, 1.95, 2.6]
          b_values: [1000]
      preprocessing_pipeline: "Manual registration to Talairach space via BrainVoyager QX v2.0, then to MNI space"
      reference_space: MNI152
      atlases_used: ["JHU white-matter tractography atlas"]
    author_limitations:
      - "Uneven distribution of patients across different tracts."
      - "Results based on a Chinese population; generalizability to other ethnic groups is unknown."
      - "High proportion of aphasic patients in the sample may have biased results toward the left hemisphere."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, pages 88-89"
      confidence: high
      flags: []
    source_passages:
      - section: "Abstract"
        page: 1
        quote: "We found five left-lateralized tracts including the anterior thalamic radiation (ATR) [...] were significantly correlated with the scores of both semantic and phonological fluencies."
        supports: claim
      - section: "Participants"
        page: 2
        quote: "Fifty-one right-handed stroke patients [...] all suffered from their first brain injury, which was at least 1-month post-onset (mean=11.9 months; SD=34.4; range: 1-184 months)."
        supports: sample
      - section: "Identifying verbal fluency tracts"
        page: 4
        quote: "Twenty tracts were extracted from the 'JHU white-matter tractography atlas' (Hua et al., 2008) in the FMRIB Software Library."
        supports: region_definition
      - section: "Imaging data collection and preprocessing"
        page: 3
        quote: "Imaging data were collected at the China Rehabilitation Research Center with a 1.5T GE SIGNA EXCITE scanner."
        supports: imaging_details
      - section: "Results"
        page: 5
        quote: "Four tracts were significantly negatively correlated with the t scores of both cues of the phonological fluency task: the left ATR (r=-0.50 and -0.49, corrected p-values < 0.01) [and semantic fluency]."
        supports: statistics
      - section: "Methodological considerations"
        page: 10
        quote: "the numbers of patients with different lesions were not equivalent across tracts... the structural network of verbal fluency was constructed on the basis of a Chinese population... our patient sample included a high proportion of aphasic patients."
        supports: limitation
  - id: f2
    target: semantics
    target_kind: impairment
    claim: "The left anterior thalamic radiation provides a unique contribution to semantic fluency over and above phonological fluency."
    direction: likely
    relationship: causal
    citation: "@Li2017"
    method: [LSM, DTI]
    design: cross-sectional
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 51
      population: "right-handed stroke patients"
      time_post_onset: "at least 1-month post-onset"
      phase: chronic
      age_range: "mean 46.8 years"
      handedness: "all right-handed"
      language: "native Chinese speakers"
    statistics:
      threshold: "p < 0.02"
      effect_size: "partial r=0.36 to 0.49"
    confounders_controlled:
      - "phonological fluency scores"
      - "total lesion volume"
      - "type of aphasia"
      - "duration of illness"
      - "nonverbal control tasks"
    confounders_not_controlled: []
    region_definition:
      kind: atlas
      atlas: "JHU white-matter tractography atlas"
      description: "Left anterior thalamic radiation (ATR)"
    imaging_details:
      reference_space: MNI152
      atlases_used: ["JHU white-matter tractography atlas"]
    author_limitations:
      - "Uneven distribution of patients across different tracts."
      - "Results based on a Chinese population."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 7"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 7
        quote: "We observed that the FA values of left ATR, IFOF and UF were kept significant correlation with semantic fluency when the covariates included the phonological fluency scores and the potential confounding factors (partial r=0.36 to 0.49, p-values < 0.02)."
        supports: claim
---
