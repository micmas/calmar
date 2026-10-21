---
schema_version: 2.3
id: dysarthria_interventions
name: Interventions for Dysarthria due to Stroke and Brain Injury
kind: review
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
findings:
- id: f1
  target: dysarthria
  target_kind: impairment
  claim: There is limited evidence suggesting that dysarthria interventions may provide an immediate beneficial
    effect on impairment-level measures, such as muscle movement, but there is no evidence that these
    effects persist long-term.
  direction: mixed
  relationship: synthesis
  citation: '@Mitchell2017'
  method: narrative_review
  design: systematic-review
  evidence_quality: narrative-review
  strength: weak
  author_limitations:
  - The evidence base is limited, consisting of only five small trials that were not adequately powered.
  - There is a lack of consensus on outcome measures and time points for measurement.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Abstract and Authors' Conclusions
    confidence: high
    flags: []
  source_passages:
  - section: Abstract
    page: 5
    quote: 'There was a statistically significant eﬀect favouring intervention at the immediate, impairment
      level of measurement (SMD 0.47, 95% CI 0.02 to 0.92, P = 0.04, I2 = 0%; 4 trials, 99 participants,
      GRADE: very low quality)'
    supports: claim
  - section: Abstract
    page: 5
    quote: Our primary analysis of a persisting (three to nine months post-intervention) eﬀect at the
      activity level of measurement found no evidence in favour of dysarthria intervention compared with
      any control
    supports: claim
  - section: Authors' Conclusions
    page: 5
    quote: We found limited evidence to suggest there may be an immediate beneficial eﬀect on impairment
      level measures; more, higher quality research is needed to confirm this finding.
    supports: claim
  - section: Discussion
    page: 19
    quote: The one significant finding at the impairment level immediately post-intervention... means
      that clinically there may be some improvement of tongue and lip movement for example but there is
      no evidence that these persist long-term
    supports: claim
  - section: Discussion
    page: 19
    quote: We only identified five, small trials which indicates the evidence base is limited. In addition
      to the limited number of trials there were only small numbers of participants within the trials
    supports: limitation
  - section: Discussion
    page: 19
    quote: The wide variety of outcome measures, where none of the five trials used any of the same outcome
      measures, indicates a need for consensus amongst researchers
    supports: limitation
---
This systematic review evaluates the efficacy of various interventions for dysarthria following stroke and other non-progressive brain injuries. The authors conclude that while some immediate improvements in impairment-level measures (e.g., oromotor control) were observed, there is no robust evidence for long-term functional improvement at the activity or participation levels.
