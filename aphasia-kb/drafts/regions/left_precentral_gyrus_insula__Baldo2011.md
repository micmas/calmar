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
    target: apraxia_of_speech
    target_kind: impairment
    claim: "Damage to the left superior precentral gyrus of the insula is associated with impaired articulation of complex words, specifically those that are multi-syllabic, require high articulatory travel, or contain initial consonant clusters."
    direction: likely
    relationship: causal
    citation: "@Baldo2011"
    method: VLSM
    design: cross-sectional
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 33
      population: "left hemisphere stroke patients"
      time_post_onset: "mean 60.3 months (SD 54.3)"
      age_range: "mean 58.6 (SD 9.9)"
      handedness: "all right-handed"
      language: "native English speakers"
    statistics:
      threshold: "permutation p < .05"
      effect_size: "not_reported"
    confounders_controlled: []
    confounders_not_controlled: ["lesion volume"]
    region_definition:
      kind: data_driven_cluster
      description: "Superior precentral gyrus of the insula (SPGI) centered at MNI -36, 1, 10."
    imaging_details:
      field_strength: "1.5T"
      acquisition:
        voxel_size_mm: [0.94, 1.3, 0.94]
        sequence: "SPGR"
      preprocessing_pipeline: "non-linearly transformed into MNI space (152-MNI template) in SPM5"
      reference_space: MNI152
      atlases_used: []
      coordinates_reported:
        - region: "SPGI"
          mni: [-36, 1, 10]
    author_limitations:
      - "Unable to fully sample the left hemisphere in the VLSM analyses due to the nature of the patients' lesions (predominantly MCA strokes) and statistical requirements."
      - "Difficulty creating 'pure' articulation conditions (e.g., 3-syllable words with absolutely no travel)."
      - "Potential brain reorganization following stroke may affect results in the chronic phase."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 804"
      confidence: high
      flags: ["target impairment id apraxia_of_speech is forward-looking"]
    source_passages:
      - section: "Abstract"
        page: 1
        quote: "We found that the SPGI was critical for performance on the articulation task across all three conditions, namely, when words were multi-syllabic, required a high degree of travel, or involved an initial consonant cluster."
        supports: claim
      - section: "Methods - Participants"
        page: 2
        quote: "The study included 33 patients (27 males) who had a history of a single, left hemisphere stroke."
        supports: sample
      - section: "Methods - Procedures"
        page: 1
        quote: "The role of the SPGI in performance across the three conditions was determined using voxel-based lesion symptom mapping (VLSM)..."
        supports: method
      - section: "Methods - Procedures"
        page: 4
        quote: "The VLSM analysis was subjected to permutation testing using Matlab, in order to determine a critical t cut-off (at p < .05), based on 1000 random permutations of the data."
        supports: statistics
      - section: "Methods - Procedures"
        page: 3
        quote: "Most of the patients' lesions (67%) were reconstructed based on high-resolution T1-weighted structural 3D MRI scans obtained from a 1.5 T Phillips Eclipse scanner."
        supports: imaging_details
      - section: "Methods - Procedures"
        page: 3
        quote: "The scans were then non-linearly transformed into MNI space (152-MNI template) in SPM5"
        supports: imaging_details
      - section: "Results"
        page: 5
        quote: "performance on the 3-syllable condition was associated with a large area of significance in the SPGI (centered at MNI -36, 1, 10)."
        supports: region_definition
      - section: "Discussion"
        page: 7
        quote: "Limitations of the current study include the fact that we were not able to fully sample the left hemisphere in the VLSM analyses."
        supports: limitation
  - id: f2
    target: apraxia_of_speech
    target_kind: impairment
    claim: "Damage to the left superior precentral gyrus of the insula does not significantly impair the articulation of simple, single-syllable words with minimal articulatory travel and no initial consonant clusters."
    direction: no_effect
    relationship: causal
    citation: "@Baldo2011"
    method: VLSM
    design: cross-sectional
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 33
      population: "left hemisphere stroke patients"
      time_post_onset: "mean 60.3 months (SD 54.3)"
      age_range: "mean 58.6 (SD 9.9)"
      handedness: "all right-handed"
      language: "native English speakers"
    statistics:
      threshold: "permutation p < .05"
      effect_size: "not_reported"
    confounders_controlled: []
    confounders_not_controlled: ["lesion volume"]
    region_definition:
      kind: data_driven_cluster
      description: "Superior precentral gyrus of the insula (SPGI) centered at MNI -36, 1, 10."
    imaging_details:
      field_strength: "1.5T"
      acquisition:
        voxel_size_mm: [0.94, 1.3, 0.94]
        sequence: "SPGR"
      preprocessing_pipeline: "non-linearly transformed into MNI space (152-MNI template) in SPM5"
      reference_space: MNI152
      atlases_used: []
      coordinates_reported:
        - region: "SPGI"
          mni: [-36, 1, 10]
    author_limitations:
      - "Unable to fully sample the left hemisphere in the VLSM analyses due to the nature of the patients' lesions (predominantly MCA strokes) and statistical requirements."
      - "Difficulty creating 'pure' articulation conditions (e.g., 3-syllable words with absolutely no travel)."
      - "Potential brain reorganization following stroke may affect results in the chronic phase."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Abstract, page 1"
      confidence: high
      flags: ["target impairment id apraxia_of_speech is forward-looking"]
    source_passages:
      - section: "Abstract"
        page: 1
        quote: "As a control, we also generated a VLSM map for articulation of words with minimal articulatory complexity... In this case, the SPGI was not implicated."
        supports: claim
      - section: "Results"
        page: 6
        quote: "whereas when articulatory complexity was minimal, the SPGI showed almost no involvement (50% vs 2% of SPGI, respectively)."
        supports: statistics
---

This paper uses VLSM to demonstrate that the left superior precentral gyrus of the insula (SPGI) is specifically critical for complex articulatory movements (multi-syllabic, high travel, initial clusters) but not for simple articulation.
