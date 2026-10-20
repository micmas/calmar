---
schema_version: 2.3
id: left_middle_temporal_gyrus
name: "Left Middle Temporal Gyrus"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-20
hemisphere: left
findings:
  - id: f1
    target: semantics
    target_kind: impairment
    claim: "Damage to the left anterior to mid middle temporal gyrus is associated with an increased rate of semantic naming errors."
    direction: likely
    relationship: causal
    citation: "@Schwartz2009"
    method: VLSM
    design: cross-sectional
    strength: strong
    evidence_quality: cohort
    sample:
      n: 64
      population: "post-stroke aphasia"
      time_post_onset: "mean 68 months"
      age_range: "mean 58"
      handedness: "right-handed"
      language: "English"
    statistics:
      threshold: "FDR q = 0.01"
      effect_size: "r = 0.34"
      p_value: "0.006"
    confounders_controlled: ["total lesion volume"]
    confounders_not_controlled: []
    region_definition:
      kind: atlas
      atlas: "Brodmann area 21"
      description: "Anterior to mid middle temporal gyrus."
    imaging_details:
      reference_space: MNI152
      atlases_used: ["AAL"]
    author_limitations:
      - "Vascular anatomy of MCA strokes limits coverage of the inferior temporal and fusiform gyri."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 3419"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 3417
        quote: "The strongest associations were found in the left anterior to mid middle temporal gyrus."
        supports: claim
      - section: "Results"
        page: 3419
        quote: "Moreover, we statistically conﬁrmed the independent contribution of anterior tempo ral lobe in a regional analysis, in which we calculated the percentage of damage within Brodmann areas 38 (temporal pole) and 21 (middle temporal gyrus) and computed partial correlations with SemErr, controlling for total lesion volume. Results were signiﬁcant for both areas (Brodmann area 21: r = 0.34, P = 0.006; Brodmann area 38: r = 0.33, P = 0.008)"
        supports: statistics
      - section: "Discussion"
        page: 3422
        quote: "It must be emphasized that the region within the left anterior temporal lobe that our analysis picked out almost certainly underestimates the extent of the temporal lobe involvement."
        supports: limitation
---

# Left Middle Temporal Gyrus

Findings from @Schwartz2009 associate the anterior to mid portions of the left MTG (BA 21) with semantic naming errors, independent of total lesion volume.
