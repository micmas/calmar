---
schema_version: 2.6
id: affective_prosody_localization__Durfee2021
name: Affective Prosody Localization in the Right Hemisphere
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-23
hemisphere: right
findings:
- id: f1
  target: affective_prosody_production
  target_kind: impairment
  claim: Damage to right antero-superior (dorsal stream) regions, particularly the inferior frontal lobe
    and insula, is associated with impaired affective prosody production.
  direction: likely
  relationship: synthesis
  citation: '@Durfee2021'
  method: narrative_review
  design: systematic-review
  evidence_quality: narrative-review
  strength: moderate
  primary_papers_cited:
  - '@Ross1981'
  - '@Patel2018'
  - '@Ross2008'
  author_limitations:
  - Data quality in available studies is a main limitation, with most studies being small (<100 patients)
    and providing qualitative descriptions of lesions.
  - Heterogeneous presentation of study findings renders cross-study statistical comparisons a challenge.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results and Discussion
    confidence: high
    flags: []
  source_passages:
  - section: Abstract
    page: 1
    quote: Localized right antero-superior (i.e., dorsal stream) regions contributed to affective prosody
      production impairments
    supports: claim
  - section: Discussion
    page: 9
    quote: damage to frontal regions, particularly the (inferior) frontal lobe and insula, was more consistently
      observed with expressive over receptive aprosodia.
    supports: claim
  - section: Discussion
    page: 10
    quote: The main limitation of this review is data quality in available studies. Most affective prosody
      studies have been small (<100 patients) and provide qualitative descriptions of lesions
    supports: limitation
- id: f2
  target: affective_prosody_comprehension
  target_kind: impairment
  claim: Damage to right postero-lateral (ventral stream) regions, especially the posterior superior temporal
    gyrus and subcortical nuclei, is associated with impaired affective prosody comprehension.
  direction: likely
  relationship: synthesis
  citation: '@Durfee2021'
  method: narrative_review
  design: systematic-review
  evidence_quality: narrative-review
  strength: moderate
  primary_papers_cited:
  - '@Sheppard2020'
  - '@Starkstein1994'
  - '@Ross1981'
  author_limitations:
  - Impaired blood flow to non-lesioned tissue (hypoperfusion) may confound reported lesion data.
  - Stimuli-related factors, such as the use of decontextualized tasks, may obscure true processing abilities.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results and Discussion
    confidence: high
    flags: []
  source_passages:
  - section: Abstract
    page: 1
    quote: damage to more postero-lateral (i.e., ventral stream) regions resulted in affective prosody
      comprehension deficits.
    supports: claim
  - section: Discussion
    page: 9
    quote: Receptive aprosodia was more often associated with posterior damage to the temporal lobe and
      subcortical nuclei, including the basal ganglia, thalamus, and amygdala
    supports: claim
  - section: Discussion
    page: 10
    quote: Impaired blood flow to non-lesioned tissue may also confound reported lesion data.
    supports: limitation
- id: f3
  target: affective_prosody_shared_processes
  target_kind: impairment
  claim: The right parietal lobe serves as a shared substrate for both the production and comprehension
    of affective prosody.
  direction: likely
  relationship: synthesis
  citation: '@Durfee2021'
  method: narrative_review
  design: systematic-review
  evidence_quality: narrative-review
  strength: weak
  primary_papers_cited: []
  author_limitations:
  - The proportions of parietal damage associated with receptive vs expressive aprosodia were similar,
    but these findings should be interpreted cautiously.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Discussion
    confidence: high
    flags: []
  source_passages:
  - section: Discussion
    page: 9
    quote: the parietal lobe serves as shared ground for language production and comprehension processes
    supports: claim
  - section: Discussion
    page: 9
    quote: We acknowledge that continued work is vital to validate these claims and that these findings
      should be interpreted cautiously.
    supports: limitation
---

This systematic review synthesizes 50 years of evidence on the localization of affective prosody in the right hemisphere following stroke, supporting a dual-stream organization mirroring the left hemisphere's propositional language system.
