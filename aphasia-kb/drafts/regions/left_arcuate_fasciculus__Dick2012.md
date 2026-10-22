---
schema_version: 2.3
id: left_arcuate_fasciculus
name: Left arcuate fasciculus
kind: tract
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
hemisphere: left
findings:
- id: f1
  target: phonological_production
  target_kind: impairment
  claim: The superior longitudinal fasciculus/arcuate fasciculus (SLF/AF) is involved in phonological
    processing during speech perception and production.
  direction: likely
  relationship: synthesis
  citation: '@Dick2012'
  method: narrative_review
  design: narrative-review
  strength: weak
  evidence_quality: narrative-review
  author_limitations:
  - Individual differences in anatomy contribute to the difficulty of determining precise trajectories
    of the pathways.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Fibre pathways of the dorsal stream, page 9
    confidence: high
    flags: []
  source_passages:
  - section: Fibre pathways of the dorsal stream
    page: 9
    quote: In summary, the role of the SLF/AF in phonological processing during speech perception and
      production is supported...
    supports: claim
  - section: Summary of methods
    page: 4
    quote: Across individuals, such anatomical differences are useful to establish functional correlates
      with specific pathways... but individual differences also contribute to the difficulty of determining
      precise trajectories of the pathways
    supports: limitation
---
