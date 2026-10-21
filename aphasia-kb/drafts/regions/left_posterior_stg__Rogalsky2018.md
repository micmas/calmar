---
schema_version: 2.3
id: left_posterior_stg
name: "Left Posterior Superior Temporal Gyrus"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: left
findings:
  - id: f1
    target: syntactic_processing
    target_kind: impairment
    claim: "Damage to the left posterior superior temporal gyrus and inferior parietal regions is associated with agrammatic sentence comprehension (impaired performance on noncanonical versus canonical sentences)."
    direction: likely
    relationship: causal
    citation: "@Rogalsky2018"
    method: VLSM
    design: cross-sectional
    strength: strong
    evidence_quality: cohort
    sample:
      n: 66
      population: "chronic left-hemisphere stroke and unilateral left temporal lobectomy patients"
      time_post_onset: "6 months or more postonset"
      age_range: "mean 62 (stroke), 46 (lobectomy)"
      handedness: "vast majority strongly right-handed"
      language: "native speakers of English"
    statistics:
      threshold: "p < .001, corrected"
      effect_size: "not_reported"
    confounders_controlled:
      - "lesion size"
      - "canonical sentence performance (as covariate)"
    confounders_not_controlled: []
    region_definition:
      kind: data_driven_cluster
      description: "Large clusters spanning the left superior temporal lobe and inferior parietal lobe, including Heschl's gyrus, STG, MTG, and supramarginal gyrus."
    imaging_details:
      field_strength: "not_reported"
      preprocessing_pipeline: "MAP-3 lesion analysis methods implemented on Brainvox software"
      reference_space: "Talairach"
      atlases_used: []
      coordinates_reported:
        - region: "white matter underlying posterior STG (sentence-picture matching)"
          mni: [-35, -52, 14]
        - region: "superior temporal cortex (plausibility judgments)"
          mni: [-54, -26, 5]
    author_limitations:
      - "The temporal lobectomy group may have experienced functional neural reorganization due to epilepsy or surgery."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results: VLSM Results: Agrammatic Comprehension, page 12"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 12
        quote: "For both tasks, the VLSMs for performance on the noncanonical (OR and passive) sentences with canonical (SR and active) sentence performance as a covariate identified large clusters of voxels spanning the left superior temporal lobe and, to a lesser extent, the inferior parietal lobe"
        supports: claim
      - section: "Methods"
        page: 5
        quote: "Sixty-six of these patients were included in this study based on the following criteria: (i) a chronic focal (6 months or more postonset) lesion due to a stroke in the left hemisphere (n = 48...) or a unilateral left temporal lobectomy (n = 18...)"
        supports: sample
      - section: "Methods"
        page: 9
        quote: "VLSM (Bates et al., 2003) was used among all of the 66 left-hemisphere patients... a voxel-wise threshold of p < .001 was used. Multiple comparisons were controlled for using a cluster size-based permutation method"
        supports: method
      - section: "Results"
        page: 12
        quote: "p < .001, corrected"
        supports: statistics
      - section: "Methods"
        page: 10
        quote: "Variance due to lesion size... was regressed out of all VLSM analyses via an ANCOVA."
        supports: confounders
      - section: "Discussion"
        page: 16
        quote: "our ATL group consists of temporal lobectomy patients who have likely experienced functional neural reorganization due to their medically intractable epilepsy and perhaps additionally after their temporal resection surgery."
        supports: limitation
---
