---
schema_version: 2.6
id: right_temporal_operculum
name: "Right Temporal Operculum"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-23
hemisphere: right
findings:
  - id: f1
    target: affective_prosody_comprehension
    target_kind: impairment
    claim: "Injury to the right temporal operculum is strongly associated with deficits in the comprehension of affective prosody."
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
      threshold: "p = .003"
      effect_size: not_reported
    confounders_controlled: []
    confounders_not_controlled: ["lesion volume"]
    region_definition:
      kind: data_driven_cluster
      description: "Right temporal operculum, including Heschl's gyrus."
    imaging_details:
      field_strength: "1.5T"
      preprocessing_pipeline: "projection technique that isomorphically adjusts for normal variations in brain width, height and depth"
      reference_space: "native"
      atlases_used: []
    author_limitations:
      - "Some patients with predominantly supra-Sylvian lesions had comprehension deficits due to small planum lesions of the temporal operculum that could be missed on standard transaxial cuts."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, Section 3.4.3"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 10
        quote: "Data from Table 9 and Fig. 5 indicate that only temporal opercula lesions were associated significantly with poor Comprehension of affective prosody (p = .003)."
        supports: claim
      - section: "Results"
        page: 10
        quote: "all three had small planum lesions of the temporal operculum that involved, at minimum, Heshel's gyrus (Fig. 6). These lesions could be missed easily on standard transaxial cuts."
        supports: limitation
---

Findings from Ross & Monnot (2008) regarding the right temporal operculum's role in affective prosody comprehension.
