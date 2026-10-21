---
schema_version: 2.3
id: left_middle_longitudinal_fasciculus
name: "Left Middle Longitudinal Fasciculus"
kind: tract
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: left
findings:
  - id: f1
    target: semantics
    target_kind: impairment
    claim: "The middle longitudinal fasciculus is part of the ventral sound-to-meaning pathway."
    direction: likely
    relationship: synthesis
    citation: "@Dick2012"
    method: narrative_review
    design: narrative-review
    strength: weak
    evidence_quality: narrative-review
    author_limitations:
      - "Individual differences in anatomy contribute to the difficulty of determining precise trajectories of the pathways."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Middle longitudinal fasciculus: functional and clinical notions, page 12"
      confidence: high
      flags: ["new region id - flag for reviewer to add to KB"]
    source_passages:
      - section: "Middle longitudinal fasciculus: functional and clinical notions"
        page: 12
        quote: "Saur and colleagues (2008, 2010) and Wong and colleagues (2011) recently identified the middle longitudinal fasciculus as part of the ventral sound-to-meaning pathway."
        supports: claim
      - section: "Summary of methods"
        page: 4
        quote: "Across individuals, such anatomical differences are useful to establish functional correlates with specific pathways... but individual differences also contribute to the difficulty of determining precise trajectories of the pathways"
        supports: limitation
---
