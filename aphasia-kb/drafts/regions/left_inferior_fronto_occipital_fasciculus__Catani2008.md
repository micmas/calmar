---
schema_version: 2.4
id: left_inferior_fronto_occipital_fasciculus
name: "Left Inferior Fronto-Occipital Fasciculus"
kind: tract
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-20
hemisphere: left
findings:
  - id: f1
    target: semantics
    target_kind: impairment
    claim: "The left inferior fronto-occipital fasciculus may be involved in reading and writing."
    direction: likely
    relationship: synthesis
    citation: "@Catani2008"
    method: narrative_review
    design: narrative-review
    strength: weak
    evidence_quality: narrative-review
    author_limitations:
      - "The relevance of this fasciculus to language is not fully understood."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Beyond the arcuate fasciculus: the ventral pathways"
      confidence: high
      flags: ["target_id left_inferior_fronto_occipital_fasciculus is forward-looking"]
    source_passages:
      - section: "Beyond the arcuate fasciculus: the ventral pathways"
        page: 5
        quote: "The relevance of this fasciculus to language is not fully understood but may involve reading and writing."
        supports: claim
      - section: "Beyond the arcuate fasciculus: the ventral pathways"
        page: 5
        quote: "The relevance of this fasciculus to language is not fully understood"
        supports: limitation
---
