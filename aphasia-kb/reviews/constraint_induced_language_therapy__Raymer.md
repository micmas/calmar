---
schema_version: 2.4
id: constraint_induced_language_therapy__Raymer
name: Effectiveness of Constraint-Induced Language Therapy (CILT) for Aphasia — Systematic
  Review of Reviews
kind: therapy
status: approved
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-07
short_description: 'A review of six systematic reviews (three with meta-analysis)
  summarising constraint-induced language therapy (CILT) for post-stroke aphasia.
  Appraises SR quality using AMSTAR 2 and synthesises findings on CILT efficacy relative
  to comparison treatments. All six SRs were rated "critically low" on AMSTAR 2 due
  to missing critical domains. Synthesised conclusions: CILT produces language improvements,
  but when compared against matched-intensity multimodality treatments, effects are
  similar — suggesting treatment intensity, not verbal constraint per se, is the active
  ingredient.

  '
findings:
- id: f1
  target: constraint_induced_language_therapy
  target_kind: therapy
  claim: 'CILT produces improvements in language and communication measures (naming,
    comprehension, repetition, aphasia batteries, communication logs) in individuals
    with post-stroke aphasia, with positive findings reported across the majority
    of original studies included in six systematic reviews spanning 2008–2020.

    '
  direction: likely
  relationship: synthesis
  citation: '@Raymer'
  method: narrative_review
  design: systematic-review
  evidence_quality: narrative-review
  strength: moderate
  source_passages:
  - section: \'narrative synthesis\'
    quote: CILT led to improvements in a variety of language
    page: 1
    supports: claim
  - section: \'narrative synthesis\'
    quote: Positive CILT findings were reported in the majority of original studies
    page: 4
    supports: claim
  - section: \'narrative synthesis\'
    quote: precluded quantitative
    page: 7
    supports: claim
  primary_papers_cited:
  - Cherney2008
  - Cherney2010
  - Balardin2009
  - Zhang2017
  - Pierce2019
  - Wang2020
  author_limitations:
  - All six SRs rated "critically low" on AMSTAR 2 — each lacking two or more critical
    domains (no registered protocol, no list of excluded studies, no investigation
    of publication bias).
  - Search string may have missed some SRs; only published academic papers searched.
  - One reviewer is co-author of two of the reviewed SRs (Cherney et al. 2008, 2010),
    creating potential bias despite high inter-rater reliability.
  - Varied designs across primary studies (RCTs vs single-subject) limit direct comparisons.
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-07
    paper_section: Abstract; Results (pp. 2397–2398); Discussion (pp. 2399–2400)
    confidence: high
    flags: []
- id: f2
  target: constraint_induced_language_therapy
  target_kind: therapy
  claim: 'When CILT is compared to comparison treatments delivered at the same high-intensity
    schedule, meta-analyses show that CILT effects for standardised language measures
    (naming, comprehension, repetition, aphasia batteries) are largely not significantly
    superior to intensive multimodality treatments, suggesting that treatment intensity
    rather than verbal constraint is the potent factor in CILT outcomes.

    '
  direction: no_effect
  relationship: synthesis
  citation: '@Raymer'
  method: narrative_review
  design: systematic-review
  evidence_quality: narrative-review
  strength: moderate
  source_passages:
  - section: \'narrative synthesis\'
    quote: effects of CILT often did not surpass those of comparison treatments
    page: 1
    supports: claim
  - section: \'narrative synthesis\'
    quote: training intensity may be the potent factor in CILT outcomes
    page: 1
    supports: claim
  - section: \'narrative synthesis\'
    quote: two of the MAs showed that effects of CILT often did not surpass
    page: 4
    supports: claim
  primary_papers_cited:
  - Zhang2017
  - Wang2020
  - Pierce2019
  author_limitations:
  - MAs limited to RCT designs (Zhang et al., Wang et al.) included few primary studies
    (8 and 12 CILT studies respectively), reducing statistical power.
  - Heterogeneity in comparison treatments across SRs makes interpretation of superiority
    vs. equivalence claims difficult.
  - Generalisation to trained stimuli (Pierce et al., Tau-U = 0.374) was significant,
    but generalisation to untrained standardised measures was not.
  - All six SRs lacked investigation of publication bias — potential inflation of
    positive CILT effects.
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-07
    paper_section: Results (Table 3, p. 2398); Discussion (pp. 2399–2400)
    confidence: high
    flags: []
- id: f3
  target: constraint_induced_language_therapy
  target_kind: therapy
  claim: 'CILT effects for trained naming stimuli are potent (large effect sizes in
    single-subject and group designs), and positive effects on communication activity/participation
    outcomes (communication logs, rating scales) have been consistently reported across
    SRs, even where standardised language measure effects were equivocal in meta-analyses.

    '
  direction: likely
  relationship: synthesis
  citation: '@Raymer'
  method: narrative_review
  design: systematic-review
  evidence_quality: narrative-review
  strength: weak
  source_passages:
  - section: \'narrative synthesis\'
    quote: CILT treatment effects may be potent for trained language
    page: 7
    supports: claim
  - section: \'narrative synthesis\'
    quote: positive outcomes have been reported
    page: 7
    supports: claim
  - section: \'narrative synthesis\'
    quote: showed powerful CILT effects for trained naming stimuli
    page: 7
    supports: claim
  primary_papers_cited:
  - Pierce2019
  - Zhang2017
  author_limitations:
  - Variety of activity/participation measures across SRs precluded quantitative pooling.
  - Single-subject designs provide limited generalisability compared to RCTs.
  - Positive findings for trained stimuli do not necessarily generalise to untrained
    items or standardised batteries.
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-07
    paper_section: Discussion (pp. 2399–2400); Results (Table 3, p. 2398)
    confidence: medium
    flags: []
reviewer: michele
reviewed_on: '2026-05-07'
---
