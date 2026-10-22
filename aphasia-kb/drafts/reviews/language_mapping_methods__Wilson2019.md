---
schema_version: 2.3
id: language_mapping_methods__Wilson2019
name: Language Mapping Methods in Aphasia
kind: review
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
findings:
- id: f1
  target: language_mapping_paradigms
  target_kind: impairment
  claim: Adaptive language mapping paradigms that dynamically adjust to individual performance are more
    feasible, reliable, and valid for identifying language regions in individuals with aphasia than fixed
    paradigms like picture naming or narrative comprehension.
  direction: likely
  relationship: synthesis
  citation: '@Wilson2019'
  method: narrative_review
  design: narrative-review
  evidence_quality: narrative-review
  strength: moderate
  primary_papers_cited:
  - '@Wilson2017'
  - '@Wilson2018'
  - '@Yen2019'
  author_limitations:
  - The review focuses on paradigms developed within a single lab; broader validation across different
    centers is needed.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Abstract, Introduction
    confidence: high
    flags: []
  source_passages:
  - section: Abstract
    page: 1
    quote: Adaptive language mapping paradigms offer a promising approach for future research on the neural
      basis of recovery from aphasia.
    supports: claim
  - section: Introduction
    page: 3
    quote: We propose that adaptive paradigms that dynamically adjust to individual performance offer
      the most promising approach at present...
    supports: claim
  - section: Discussion
    page: 5
    quote: The mean Dice coefficient of similarity... significantly exceeded the reliability of the narrative
      comprehension (Dice coefficient = .47) and picture naming (Dice coefficient = .43) paradigms.
    supports: statistics
  - section: Discussion
    page: 8
    quote: Whether researchers use our paradigms or other paradigms, we hope to have demonstrated the
      importance of investigating the feasibility, reliability, and validity of any potential approach
      for identifying language regions in individuals with aphasia.
    supports: limitation
---

This review article synthesizes the development and validation of adaptive fMRI paradigms for language mapping in aphasia, arguing that adaptive designs minimize performance confounds and increase test-retest reliability compared to traditional fixed tasks.
