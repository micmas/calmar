---
schema_version: 2.4
id: left_uncinate_fasciculus
name: Left Uncinate Fasciculus
kind: tract
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
hemisphere: left
findings:
- id: f1
  target: semantics
  target_kind: impairment
  claim: The left uncinate fasciculus is implicated in lexical retrieval, semantic associations, and the
    naming of actions.
  direction: likely
  relationship: synthesis
  citation: '@Catani2008'
  method: narrative_review
  design: narrative-review
  strength: weak
  evidence_quality: narrative-review
  author_limitations:
  - The relevance of ventral pathways to language is not fully understood.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: 'Beyond the arcuate fasciculus: the ventral pathways'
    confidence: high
    flags:
    - target_id left_uncinate_fasciculus is forward-looking
  source_passages:
  - section: 'Beyond the arcuate fasciculus: the ventral pathways'
    page: 5
    quote: The uncinate fasciculus... may play an important role in lexical retrieval, semantic associations,
      and aspects of naming that require connections from temporal to frontal components of the language
      network (e.g., the naming of actions).
    supports: claim
  - section: 'Beyond the arcuate fasciculus: the ventral pathways'
    page: 6
    quote: The relevance of this fasciculus to language is not fully understood
    supports: limitation
---
