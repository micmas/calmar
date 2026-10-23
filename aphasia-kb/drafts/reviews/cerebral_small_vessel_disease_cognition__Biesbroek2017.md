---
schema_version: 2.6
id: cerebral_small_vessel_disease_cognition__Biesbroek2017
name: Cerebral Small Vessel Disease and Cognitive Impact
kind: review
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-23
findings:
- id: f1
  target: executive_functions
  target_kind: impairment
  claim: White matter hyperintensity (WMH) and lacunar volume in the anterior thalamic radiation (ATR),
    forceps minor, and superior longitudinal fasciculus (SLF) are associated with poor executive functioning,
    independent of total lesion burden.
  direction: likely
  relationship: synthesis
  citation: '@Biesbroek2017'
  method: narrative_review
  design: systematic-review
  evidence_quality: narrative-review
  strength: moderate
  primary_papers_cited:
  - '@Biesbroek2013'
  - '@Biesbroek2016'
  author_limitations:
  - Most studies still had limited lesion coverage throughout the brain.
  - Observed associations in cross-sectional lesion-symptom mapping studies do not prove causality.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Strategic white matter tracts in SVD-related cognitive impairment, page 6
    confidence: high
    flags: []
  source_passages:
  - section: Strategic white matter tracts in SVD-related cognitive impairment
    page: 6
    quote: Lesion–symptom mapping studies reported a relationship between WMH and lacunar volume in the
      ATR, forceps minor and superior longitudinal fasciculus (SLF) and poor executive functioning, again
      independent of total lesion burden [35,64].
    supports: claim
  - section: Clinical implications and future perspectives
    page: 9
    quote: Yet, despite substantial sample sizes, most of these studies still had limited lesion coverage
      throughout the brain.
    supports: limitation
  - section: Cross-sectional compared with longitudinal study design
    page: 6
    quote: As such, the observed associations between WMH and lacune location and cognitive function–ing
      in cross-sectional lesion–symptom mapping studies do not prove causality.
    supports: limitation
- id: f2
  target: processing_speed
  target_kind: impairment
  claim: WMH or lacunar volume in the anterior thalamic radiation (ATR) and the forceps minor is consistently
    linked to poor processing speed, independent of total lesion burden.
  direction: likely
  relationship: synthesis
  citation: '@Biesbroek2017'
  method: narrative_review
  design: systematic-review
  evidence_quality: narrative-review
  strength: moderate
  primary_papers_cited:
  - '@Duering2011'
  - '@Duering2013'
  - '@Duering2014'
  - '@Biesbroek2016'
  author_limitations:
  - Most studies still had limited lesion coverage throughout the brain.
  - Observed associations in cross-sectional lesion-symptom mapping studies do not prove causality.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Strategic white matter tracts in SVD-related cognitive impairment, page 5
    confidence: high
    flags: []
  source_passages:
  - section: Strategic white matter tracts in SVD-related cognitive impairment
    page: 5
    quote: Lesion–symptom mapping studies consistently report a relationship between WMH or lacunar volume
      in the ATR and the forceps minor and poor processing speed, independent of total lesion burden [61–64].
    supports: claim
  - section: Clinical implications and future perspectives
    page: 9
    quote: Yet, despite substantial sample sizes, most of these studies still had limited lesion coverage
      throughout the brain.
    supports: limitation
  - section: Cross-sectional compared with longitudinal study design
    page: 6
    quote: As such, the observed associations between WMH and lacune location and cognitive function–ing
      in cross-sectional lesion–symptom mapping studies do not prove causality.
    supports: limitation
---

This narrative review synthesizes the impact of cerebral small vessel disease (SVD) lesion location on cognition, specifically highlighting the role of strategic white matter tracts like the ATR and forceps minor.
