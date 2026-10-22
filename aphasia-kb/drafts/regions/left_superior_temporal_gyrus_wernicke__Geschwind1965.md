---
schema_version: 2.3
id: left_superior_temporal_gyrus_wernicke
name: Left Superior Temporal Gyrus (Wernicke's Area and Planum Temporale)
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
hemisphere: left
findings:
- id: f1
  target: pure_word_deafness
  target_kind: impairment
  claim: Pure word-deafness results from the disconnection of Wernicke's area from auditory stimulation.
  direction: likely
  relationship: synthesis
  citation: '@Geschwind1965'
  method: narrative_review
  design: narrative-review
  strength: moderate
  evidence_quality: narrative-review
  author_limitations:
  - The author notes that the synthesis contains much speculation subject to future experimental checks.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Pure Word-deafness, page 487
    confidence: high
    flags:
    - target impairment id pure_word_deafness is forward-looking
  source_passages:
  - section: Pure Word-deafness
    page: 487
    quote: Pure word-deafness probably has a similar pathogenesis to that of pure word-blindness without
      agraphia. [...] Pure word-deafness probably results from the disconnexion of Wernicke's area from
      auditory stimulation.
    supports: claim
  - section: Introduction
    page: 5
    quote: There are many facts recorded in the following pages; there is also much speculation which
      is, however, nearly all subject to the checks of future experiment and clinical observation.
    supports: limitation
---
