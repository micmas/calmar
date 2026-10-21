---
schema_version: 2.3
id: left_angular_gyrus
name: Left Angular Gyrus
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
hemisphere: left
findings:
- id: f1
  target: cross_modal_association
  target_kind: impairment
  claim: The left angular gyrus is a specialized region for forming and storing cross-modal associations,
    particularly between visual and auditory modalities.
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
    paper_section: Pure Word-blindness Without Agraphia, page 479
    confidence: high
    flags:
    - target impairment id cross_modal_association is forward-looking
  source_passages:
  - section: Pure Word-blindness Without Agraphia
    page: 43
    quote: It is a region specifically designed for carrying on visual-auditory cross-modal associations
      in both directions and indeed for storing the memory of the 'rules of translation' from written
      to spoken language.
    supports: claim
  - section: Introduction
    page: 5
    quote: There are many facts recorded in the following pages; there is also much speculation which
      is, however, nearly all subject to the checks of future experiment and clinical observation.
    supports: limitation
- id: f2
  target: pure_alexia_without_agraphia
  target_kind: impairment
  claim: Pure word-blindness without agraphia results from the disconnection of the intact right visual
    cortex from the left angular gyrus.
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
    paper_section: Pure Word-blindness Without Agraphia, page 442
    confidence: high
    flags:
    - target impairment id pure_alexia_without_agraphia is forward-looking
  source_passages:
  - section: Pure Word-blindness Without Agraphia
    page: 42
    quote: Dejerine therefore argued that pure word-blindness without agraphia resulted from disconnection
      of the intact right visual cortex from the left angular gyrus in a patient in whom the left visual
      cortex had been destroyed.
    supports: claim
  - section: Introduction
    page: 5
    quote: There are many facts recorded in the following pages; there is also much speculation which
      is, however, nearly all subject to the checks of future experiment and clinical observation.
    supports: limitation
---
