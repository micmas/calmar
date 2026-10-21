---
schema_version: 2.3
id: left_uncinate_fasciculus
name: "Left Uncinate Fasciculus"
kind: tract
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
hemisphere: left
findings:
  - id: f1
    target: semantics
    target_kind: impairment
    claim: "The uncinate fasciculus is involved in semantic processing and auditory working memory/sound recognition."
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
      paper_section: "Uncinate fasciculus: functional and clinical correlates, page 10"
      confidence: high
      flags: ["new region id - flag for reviewer to add to KB"]
    source_passages:
      - section: "Uncinate fasciculus: functional and clinical correlates"
        page: 10
        quote: "In summary, there is suggestive evidence for involvement of the uncinate fasciculus in at least two language-related functions: semantic processing and auditory working memory/sound recognition."
        supports: claim
      - section: "Summary of methods"
        page: 4
        quote: "Across individuals, such anatomical differences are useful to establish functional correlates with specific pathways... but individual differences also contribute to the difficulty of determining precise trajectories of the pathways"
        supports: limitation
---
