---
schema_version: 2.3
id: dual_stream_speech_processing__Hickok2007
name: Dual-Stream Model of Speech Processing
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
findings:
- id: f1
  target: ventral_stream
  target_kind: region
  claim: The ventral stream, involving the superior and middle temporal lobe, is bilaterally organized
    and processes speech signals for comprehension (speech recognition).
  direction: likely
  relationship: synthesis
  citation: '@Hickok2007'
  method: narrative_review
  design: narrative-review
  evidence_quality: narrative-review
  strength: moderate
  author_limitations:
  - The precise mechanisms and regions involved in the ventral stream remain subject to outstanding issues.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Dual-stream model of speech processing, page 2
    confidence: high
    flags: []
  source_passages:
  - section: Dual-stream model of speech processing
    page: 2
    quote: this model proposes that a ventral stream, which involves structures in the superior and middle
      portions of the temporal lobe, is involved in processing speech signals for comprehension (speech
      recognition).
    supports: claim
  - section: Dual-stream model of speech processing
    page: 2
    quote: the model suggests that the ventral stream is bilaterally organized
    supports: claim
  - section: 'Dorsal stream: sound to action'
    page: 7
    quote: there are a number of outstanding issues concerning the precise mechanisms and regions involved
    supports: limitation
- id: f2
  target: dorsal_stream
  target_kind: region
  claim: The dorsal stream, involving the posterior frontal lobe, posterior dorsal temporal lobe, and
    parietal operculum, is strongly left-dominant and translates acoustic speech signals into articulatory
    representations.
  direction: likely
  relationship: synthesis
  citation: '@Hickok2007'
  method: narrative_review
  design: narrative-review
  evidence_quality: narrative-review
  strength: moderate
  author_limitations: []
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Dual-stream model of speech processing, page 2
    confidence: high
    flags: []
  source_passages:
  - section: Dual-stream model of speech processing
    page: 2
    quote: A dorsal stream, which involves structures in the posterior frontal lobe and the posterior
      dorsal-most aspect of the temporal lobe and parietal operculum, is involved in translating acoustic
      speech signals into articulatory representations in the frontal lobe
    supports: claim
  - section: Dual-stream model of speech processing
    page: 2
    quote: The dorsal stream, however, is strongly left-dominant
    supports: claim
- id: f3
  target: conduction_aphasia
  target_kind: impairment
  claim: Conduction aphasia results from a disruption of the auditory-motor interface system, particularly
    at the segment sequence level, rather than a simple disconnection of the arcuate fasciculus.
  direction: likely
  relationship: synthesis
  citation: '@Hickok2007'
  method: narrative_review
  design: narrative-review
  evidence_quality: narrative-review
  strength: moderate
  author_limitations: []
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Lesion evidence for a sensorimotor dorsal stream, page 8
    confidence: high
    flags: []
  source_passages:
  - section: Lesion evidence for a sensorimotor dorsal stream
    page: 8
    quote: We have suggested that conduction aphasia represents a disruption of the auditory-motor interface
      system, particularly at the segment sequence level.
    supports: claim
  - section: Lesion evidence for a sensorimotor dorsal stream
    page: 8
    quote: Conduction aphasia has classically been considered to be a disconnection syndrome involving
      damage to the arcuate fasciculus. However, there is now good evidence that this syndrome results
      from cortical dysfunction.
    supports: claim
- id: f4
  target: left_posterior_stg
  target_kind: region
  claim: The left posterior superior temporal gyrus (specifically area Spt) acts as a sensorimotor interface
    translating sensory speech codes into motor representations for the vocal tract.
  direction: likely
  relationship: synthesis
  citation: '@Hickok2007'
  method: narrative_review
  design: narrative-review
  evidence_quality: narrative-review
  strength: moderate
  author_limitations: []
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Functional imaging evidence for a sensorimotor dorsal stream, page 8
    confidence: high
    flags: []
  source_passages:
  - section: Functional imaging evidence for a sensorimotor dorsal stream
    page: 8
    quote: a left-dominant site in the Sylvian fissure at the boundary between the parietal and temporal
      lobes (area Spt), and left posterior frontal regions
    supports: claim
  - section: Functional imaging evidence for a sensorimotor dorsal stream
    page: 8
    quote: We propose that the posterior STS (bilaterally) supports sensory coding of speech, and that
      area Spt is involved in translation between those sensory codes and the motor system
    supports: claim
notes: 'This is a theoretical framework paper. Findings are synthesized claims (relationship: synthesis)
  rather than primary data. Target IDs ''ventral_stream'' and ''dorsal_stream'' are forward-looking.'
---
