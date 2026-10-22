---
schema_version: 2.6
id: thalamic_aphasia__Fritsch2022
name: Thalamic Aphasia
kind: impairment
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
findings:
- id: f1
  target: semantics
  target_kind: impairment
  claim: Thalamic aphasia is typically characterized as a mild disorder with a predominance of lexical-semantic
    deficits, including anomia and semantic paraphasias.
  direction: likely
  relationship: synthesis
  citation: '@Fritsch2022'
  method: narrative_review
  design: narrative-review
  evidence_quality: narrative-review
  strength: moderate
  primary_papers_cited:
  - '@Crosson1984'
  - '@Radanovic2021'
  author_limitations:
  - Standard language testing might often not pick up on subtle symptoms, leading to underdiagnosis.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Clinical Presentation and Phenotypes of Thalamic Aphasia, page 2
    confidence: high
    flags: []
  source_passages:
  - section: Clinical Presentation and Phenotypes of Thalamic Aphasia
    page: 2
    quote: Overall, aphasia after thalamic lesions has mostly been described as mild, with predominantly
      lexical-semantic deficits [35, 39]. This means that patients exhibit anomia, or naming deficits,
      in speaking and writing while substituting with semantic paraphasias...
    supports: claim
  - section: Summary
    page: 1
    quote: Additionally, as standard language testing might oftentimes not pick up on its subtle symptoms,
      thalamic aphasia might be underdiagnosed.
    supports: limitation
- id: f2
  target: left_anterior_thalamus
  target_kind: region
  claim: Lesions to the left anterior thalamic nuclei are associated with more severe aphasia, specifically
    characterized by naming difficulties and reduced verbal fluency.
  direction: likely
  relationship: synthesis
  citation: '@Fritsch2022'
  method: narrative_review
  design: narrative-review
  evidence_quality: narrative-review
  strength: moderate
  primary_papers_cited:
  - '@Rangus2022'
  author_limitations:
  - Most studies are based on small samples with differing quality of language assessment and imaging
    techniques.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Lateralization, page 4
    confidence: high
    flags:
    - target region left_anterior_thalamus is forward-looking
  source_passages:
  - section: Lateralization
    page: 4
    quote: Intriguingly, however, left anterior lesion location resulted in the most severe deficits,
      with a predominance of naming difficulties and reduced verbal fluency [30].
    supports: claim
  - section: Involved Thalamic Nuclei
    page: 4
    quote: Most of the aforementioned studies are based on small samples with differing quality of language
      assessment and imaging techniques, rendering specific differentiations of phenotypes difficult.
    supports: limitation
- id: f3
  target: left_pulvinar
  target_kind: region
  claim: Lesions to the pulvinar are more frequently associated with a fluent aphasia phenotype including
    naming deficits and semantic paraphasias.
  direction: likely
  relationship: synthesis
  citation: '@Fritsch2022'
  method: narrative_review
  design: narrative-review
  evidence_quality: narrative-review
  strength: moderate
  primary_papers_cited:
  - '@Rangus2022'
  author_limitations:
  - Selection bias may exist as stimulation studies focus on nuclei relevant to Parkinson's and Essential
    Tremor.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Involved Thalamic Nuclei, page 4
    confidence: high
    flags:
    - target region left_pulvinar is forward-looking
  source_passages:
  - section: Involved Thalamic Nuclei
    page: 4
    quote: While lesions to the pulvinar are described to rather result in a fluent aphasia with semantic
      paraphasias and naming deficits...
    supports: claim
  - section: Involved Thalamic Nuclei
    page: 4
    quote: stimulation studies are mostly reporting on nuclei that are of interest in the pathology and
      treatment of Parkinson's and Essential Tremor, a selection bias must be expected [16, 23].
    supports: limitation
- id: f4
  target: semantics
  target_kind: impairment
  claim: The thalamus is thought to function as a moderator or conductor within cortico-thalamic networks,
    where its dysfunction leads to a disconnection (diachisis) that impairs lexical-semantic retrieval.
  direction: likely
  relationship: synthesis
  citation: '@Fritsch2022'
  method: narrative_review
  design: narrative-review
  evidence_quality: narrative-review
  strength: moderate
  primary_papers_cited:
  - '@Nadeau2021'
  - '@Crosson2021'
  author_limitations:
  - An exact mode of action has yet to be discovered; mechanisms remain hypothetical.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Mechanisms of Thalamic Aphasia, page 5
    confidence: high
    flags: []
  source_passages:
  - section: Mechanisms of Thalamic Aphasia
    page: 5
    quote: most concepts on thalamic aphasia have suggested the role of the thalamus in language to be
      that of a monitor or conductor in a thalamo-cortical language network, with lesions of the thalamus
      leading to a disconnection between network structures and thereby to aphasia [45, 49, 83].
    supports: claim
  - section: Mechanistic Models
    page: 6
    quote: However, an exact mode of action has yet to be discovered. Therefore, further research is needed
      to show the exact role of the thalamus in language processing...
    supports: limitation
---
