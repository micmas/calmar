---
schema_version: 2.3
id: left_superior_temporal_gyrus
name: "Left Superior Temporal Gyrus"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: left
findings:
  - id: f1
    target: syntactic_processing
    target_kind: impairment
    claim: "Damage to the left anterior superior temporal gyrus (BA22) is associated with deficits in the comprehension of simple sentences and basic morphosyntactic structures."
    direction: likely
    relationship: causal
    citation: "@Dronkers2004"
    method: VLSM
    design: cross-sectional
    strength: strong
    evidence_quality: cohort
    sample:
      n: 64
      population: "chronic left hemisphere stroke patients"
      time_post_onset: "mean 4.8 years (range 1-20.5)"
      age_range: "31-80 years (mean 61.5)"
      handedness: "all right-handed"
      language: "monolingual, native English speakers"
    statistics:
      threshold: "Bonferroni correction (t > 4.7)"
      effect_size: not_reported
    confounders_controlled: []
    confounders_not_controlled: ["lesion volume"]
    region_definition:
      kind: data_driven_cluster
      description: "VLSM-defined cluster in the anterior superior temporal gyrus (BA22, Slices 1-5)."
    imaging_details:
      field_strength: not_reported
      acquisition:
        voxel_size_mm: [0.5, 0.5, 0.5]
        sequence: not_reported
      preprocessing_pipeline: "Manual reconstruction onto 11 standard templates based on the atlas of DeArmond, Fusco, and Dewey (1976)."
      reference_space: Talairach
      atlases_used: ["DeArmond, Fusco, and Dewey (1976)"]
      coordinates_reported: []
    author_limitations:
      - "Brain regions cannot easily be separated from each other in lesion analysis."
      - "Possibility of diaschitic effects where injuries to one area cause dysfunction in remote, non-lesioned areas."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Discussion, page 22"
      confidence: high
      flags: ["coordinates in Table 3 are in an unfamiliar format and were omitted"]
    source_passages:
      - section: "Abstract"
        page: 1
        quote: "Results indicated that lesions to five left hemisphere brain regions affected performance on the CYCLE-R, including... the anterior superior temporal gyrus..."
        supports: claim
      - section: "Discussion"
        page: 22
        quote: "The anterior portion of Brodmann's area 22 may be critical for the comprehension of simple sentences or sub-sentential constituent structures, those that do not go beyond basic morphosyntactic structure."
        supports: claim
      - section: "Methods - Participants"
        page: 4
        quote: "Sixty-four left hemisphere-injured (LH) chronic stroke patients... All were right-handed, monolingual, native English speakers..."
        supports: sample
      - section: "Results - VLSM of overall CYCLE performance"
        page: 14
        quote: "T-values ranged from 21.4 to 6.3 (one-tailed), with those over 4.7... being statistically significant after Bonferroni correction..."
        supports: statistics
      - section: "Discussion"
        page: 21
        quote: "One caveat to any study that attempts to map cognitive functions is that brain regions cannot easily be separated from each other."
        supports: limitation
---
