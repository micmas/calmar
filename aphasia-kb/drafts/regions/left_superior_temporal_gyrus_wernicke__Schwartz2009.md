---
schema_version: 2.3
id: left_superior_temporal_gyrus_wernicke
name: "Left Superior Temporal Gyrus (Wernicke's Area)"
kind: classical
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-20
hemisphere: left
findings:
  - id: f1
    target: semantics
    target_kind: impairment
    claim: "Damage to the left posterior superior temporal gyrus (Wernicke's area) was not significantly associated with the production of semantic naming errors."
    direction: no_effect
    relationship: causal
    citation: "@Schwartz2009"
    method: VLSM
    design: cross-sectional
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 64
      population: "post-stroke aphasia"
    statistics:
      threshold: "FDR q = 0.01"
      effect_size: "peak t around 1.8"
    confounders_controlled: []
    confounders_not_controlled: []
    region_definition:
      kind: data_driven_cluster
      description: "Posterior superior temporal gyrus, corresponding to Wernicke's area."
    imaging_details:
      reference_space: MNI152
      atlases_used: []
    author_limitations:
      - "The study focuses on chronic patients; acute patients may show different patterns due to diaschisis."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 3417"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 3417
        quote: "As indicated in Fig. 4, there were no sig- niﬁcant voxels in the posterior superior temporal gyrus, corre- sponding to Wernicke's area; indeed, the peak t-values observed in this region were around 1.8, far below the critical t (3.27)."
        supports: claim
      - section: "Discussion"
        page: 3423
        quote: "The superior temporal gyrus, including Wernicke's area in the posterior third, yielded low t-values in both unﬁltered and ﬁltered analyses."
        supports: claim
      - section: "Discussion"
        page: 3424
        quote: "In acute patients, tissue damage in posterior superior temporal gyrus could temporarily impede or suppress this residual capacity (e.g. through diaschisis), thereby yielding the correlation with performance that Hillis and colleagues observed."
        supports: limitation
---

# Left Superior Temporal Gyrus (Wernicke's Area)

Contrary to classical views, @Schwartz2009 found no significant association between lesions in Wernicke's area and the production of semantic naming errors in chronic aphasia.
