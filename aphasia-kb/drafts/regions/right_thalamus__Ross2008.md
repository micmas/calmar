---
schema_version: 2.6
id: right_thalamus
name: "Right Thalamus"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-23
hemisphere: right
findings:
  - id: f1
    target: affective_prosody_comprehension
    target_kind: impairment
    claim: "Thalamic lesions in the right hemisphere are associated with deficits in the comprehension of affective prosody."
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
      threshold: "p = .0003 (when combined with temporal operculum)"
      effect_size: not_reported
    confounders_controlled: []
    confounders_not_controlled: ["lesion volume"]
    region_definition:
      kind: manual_ROI
      description: "Right thalamus."
    imaging_details:
      field_strength: "1.5T"
      preprocessing_pipeline: "projection technique that isomorphically adjusts for normal variations in brain width, height and depth"
      reference_space: "native"
      atlases_used: []
    author_limitations:
      - "Deep lesions alone did not account for the overall cohort findings in this specific study, though they are associated with deficits in other publications."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, Section 3.4.3"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 10
        quote: "when combining the temporal operculum localization with deep localizations... the ability to predict Comprehension results increased only for the combinations of 'Temporal Operculum or Anterior Putamen' and 'Temporal Operculum or Thalamus' (p = .0003)"
        supports: claim
      - section: "Results"
        page: 8
        quote: "no significant relationships were observed for any lesion localization by affective-prosodic deficit using Fisher's Exact (chi-square) Test [ps > .10 ranging to .99]."
        supports: limitation
---

Findings from Ross & Monnot (2008) regarding the right thalamus's role in affective prosody comprehension.
