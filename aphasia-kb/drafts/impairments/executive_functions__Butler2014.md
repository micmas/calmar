---
schema_version: 2.3
id: executive_functions
name: "Executive Functions"
kind: impairment
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-20
short_definition: "Higher-order cognitive processes including planning, working memory, and mental flexibility."
findings:
  - id: f1
    target: executive_functions
    target_kind: impairment
    claim: "No specific brain region uniquely correlated with executive-cognitive performance in chronic stroke aphasia when controlling for phonological and semantic factors."
    direction: no_effect
    relationship: causal
    citation: "@Butler2014"
    method: VBCM
    design: cross-sectional
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 31
      population: "chronic stroke aphasia"
      time_post_onset: ">= 12 months"
      age_range: not_reported
      handedness: "all right-handed"
      language: "English first language"
    statistics:
      threshold: "P = 0.001 voxel-level, P < 0.001 FWE corrected cluster-level"
      effect_size: not_reported
    confounders_controlled:
      - "lesion volume"
      - "phonological factor"
      - "semantic factor"
    confounders_not_controlled: []
    region_definition:
      kind: not_reported
      description: "Whole-brain VBCM analysis for the executive-cognition factor."
    author_limitations:
      - "The test battery was not designed to extensively assess executive capacities."
      - "Lesions of the aphasic patients considered did not encompass many regions thought to be key for executive capacity."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 8"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 8
        quote: "In contrast to the phonological and semantic factors, there were no clusters that correlated uniquely with the cognitive factor score and survived correction for multiple comparisons."
        supports: claim
      - section: "Materials and methods"
        page: 3
        quote: "Participants were included if they had chronic stroke aphasia... and were at least 12 months post-stroke at time of scanning and assessment (n = 31)."
        supports: sample
      - section: "Discussion"
        page: 16
        quote: "In terms of the absence of correlates of executive-cognitive function, it is worth noting that our test battery was not designed to extensively assess these capacities, nor did the lesions of the aphasic patients that were considered encompass many regions thought to be key for this capacity."
        supports: limitation
---

Finding f1: Butler et al. (2014) found no unique regional correlates for the executive-cognition factor in their chronic stroke aphasia sample.
