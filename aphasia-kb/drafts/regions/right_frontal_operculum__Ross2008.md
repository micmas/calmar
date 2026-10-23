---
schema_version: 2.6
id: right_frontal_operculum
name: "Right Frontal Operculum"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-23
hemisphere: right
findings:
  - id: f1
    target: affective_prosody_production
    target_kind: impairment
    claim: "Injury to the right frontal operculum is strongly associated with deficits in the spontaneous production of affective prosody."
    direction: likely
    relationship: causal
    citation: "@Ross2008"
    method: LSM
    design: cross-sectional
    strength: strong
    evidence_quality: cohort
    sample:
      n: 21
      population: "right hemisphere stroke"
      time_post_onset: "3 to 8 weeks post-stroke"
      phase: early_subacute
      age_range: "44-78 years"
      handedness: "strongly right-handed"
      language: "English"
    statistics:
      threshold: "Fisher's Exact (chi-square) p < .000003"
      effect_size: not_reported
    confounders_controlled: []
    confounders_not_controlled: ["lesion volume"]
    region_definition:
      kind: data_driven_cluster
      description: "Right frontal operculum, often involving the anterior insula."
    imaging_details:
      field_strength: "1.5T"
      preprocessing_pipeline: "projection technique that isomorphically adjusts for normal variations in brain width, height and depth"
      reference_space: "native"
      atlases_used: []
    author_limitations:
      - "Very small lesions of the right frontal operculum did not produce loss of spontaneous affective prosody, possibly due to insufficient cortical destruction or rapid recovery."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, Section 3.4.1"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 9
        quote: "by combining patients with 'Large Frontal Operculum' and 'Small frontal Operculum' lesions using an 'or' function... all 21 patients in our cohort were correctly classified regarding their performance on Spontaneous affective prosody (p = .000003)."
        supports: claim
      - section: "Methods"
        page: 4
        quote: "Testing of the brain-damaged patients was completed within three to eight weeks post-stroke"
        supports: sample
      - section: "Methods"
        page: 4
        quote: "MRI scans were obtained between 2 and 6 weeks post-stroke. They were done in a standard fashion on either a Phillips Medical Systems 1.5 T Gyroscan or a GE 9600 1.5 T scanner."
        supports: imaging_details
      - section: "Discussion"
        page: 9
        quote: "The interesting observation is that very small lesions of the right frontal operculum, involving the homologue of Broca's area, did not produce loss of Spontaneous affective prosody."
        supports: limitation
  - id: f2
    target: affective_prosody_repetition
    target_kind: impairment
    claim: "Injury to the right frontal operculum predicts deficits in the repetition of affective prosody."
    direction: likely
    relationship: causal
    citation: "@Ross2008"
    method: LSM
    design: cross-sectional
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 21
      population: "right hemisphere stroke"
      time_post_onset: "3 to 8 weeks post-stroke"
      phase: early_subacute
      age_range: "44-78 years"
      handedness: "strongly right-handed"
      language: "English"
    statistics:
      threshold: "p = .001 (Large Frontal Operculum or VSF Operculum combination)"
      effect_size: not_reported
    confounders_controlled: []
    confounders_not_controlled: ["lesion volume"]
    region_definition:
      kind: data_driven_cluster
      description: "Right frontal operculum."
    imaging_details:
      field_strength: "1.5T"
      preprocessing_pipeline: "projection technique that isomorphically adjusts for normal variations in brain width, height and depth"
      reference_space: "native"
      atlases_used: []
    author_limitations:
      - "The relationship is not perfect because small, as opposed to very small, frontal operculum lesions did not produce Repetition deficits."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, Section 3.4.5"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 12
        quote: "By combining patients with 'Large Frontal Operculum' and 'Very Small Frontal Operculum' lesions using an 'or' function... the results were slightly more robust (p = .001) than for 'Large Frontal Operculum' alone (p = .005)."
        supports: claim
      - section: "Discussion"
        page: 12
        quote: "The relationship is not perfect because small, as opposed to very small, frontal operculum lesions did not produce Repetition deficits"
        supports: limitation
---

Findings from Ross & Monnot (2008) regarding the right frontal operculum's role in affective prosody production and repetition.
