---
schema_version: 2.4
id: aphasia_prognosis_predictors__Watila2015
name: Factors Predicting Post-Stroke Aphasia Recovery — Narrative Review
kind: prognosis
status: approved
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-07
short_description: 'Narrative review of PubMed/MEDLINE literature on factors predicting
  recovery from post-stroke aphasia. Covers lesion-related (size, location, aphasia
  type and severity, stroke subtype, metabolic factors) and non-lesion-related (age,
  gender, handedness, education, cognitive deficits, environmental support) prognostic
  factors, as well as treatment effects and neuroplasticity mechanisms. Concludes
  that predicting aphasia recovery is difficult due to multi-factorial interplay;
  lesion size/location and initial severity are the most robust predictors, while
  age and gender have inconsistent effects.

  '
findings:
- id: f1
  target: lesion_size_location
  target_kind: predictor
  claim: 'Larger lesion size is consistently associated with poorer aphasia recovery.
    Lesion location within critical language areas is an additional key predictor:
    lesions involving the posterior superior temporal gyrus (particularly pSTG) produce
    more persistent aphasia and poor prognosis, while subcortical lesions generally
    have a better prognosis than cortical lesions. A small lesion in a speech area
    is more likely to impact severity and recovery than a large lesion elsewhere.

    '
  direction: likely
  relationship: synthesis
  citation: '@Watila2015'
  method: narrative_review
  design: narrative-review
  evidence_quality: narrative-review
  strength: moderate
  source_passages:
  - section: \'narrative synthesis\'
    quote: negative influence of larger lesion on post-stroke aphasia recovery; and
      considered lesion size to be an important predictor
    page: 2
    supports: claim
  - section: \'narrative synthesis\'
    quote: Lesions in the superior temporal gyrus (STG) produce a more persistent
      global aphasia
    page: 2
    supports: claim
  - section: \'narrative synthesis\'
    quote: subcortically located aphasias often have a better prognosis
    page: 2
    supports: claim
  primary_papers_cited:
  - Goldenberg1994
  - Hanlon1999
  - Demeurisse1987
  author_limitations:
  - Narrative review without systematic search protocol or PRISMA documentation; risk
    of selection bias.
  - Studies cited use variable lesion measurement methods (CT, MRI, post-mortem);
    not directly comparable.
  - Lesion size and location are correlated — their independent contributions difficult
    to disentangle from reviewed studies.
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-07
    paper_section: Section 2.1.1 (p. 13/p. 2 of article)
    confidence: high
    flags: []
- id: f2
  target: initial_aphasia_severity
  target_kind: predictor
  claim: 'Initial aphasia type and severity are strong predictors of recovery. Global
    aphasia with superior temporal gyrus involvement is associated with particularly
    poor prognosis. Lazar et al.''s WAB-based prediction model showed that by 90 days,
    patients improve to approximately 70% of their maximum potential recovery regardless
    of specific deficits, but initial severity sets the ceiling. The hierarchical
    model of recovery posits that smaller LH lesions allow perilesional restitution
    (good recovery), larger lesions require broader LH recruitment (partial), and
    if LH is severely damaged, right hemisphere homotopic regions are recruited (limited
    recovery).

    '
  direction: likely
  relationship: synthesis
  citation: '@Watila2015'
  method: narrative_review
  design: narrative-review
  evidence_quality: narrative-review
  strength: moderate
  source_passages:
  - section: \'narrative synthesis\'
    quote: by 90 days, patients would have improved to approximately 70% of their
      maximum potential recovery
    page: 5
    supports: claim
  - section: \'narrative synthesis\'
    quote: good recovery can be anticipated when perilesional left hemisphere areas
      compensate for damaged language regions
    page: 5
    supports: claim
  - section: \'narrative synthesis\'
    quote: limited recovery is achieved when the right hemisphere is recruited for
      language tasks
    page: 5
    supports: claim
  primary_papers_cited:
  - Lazar2010
  author_limitations:
  - The 70% proportional recovery estimate is drawn from a single study (Lazar et
    al.) with a restricted sample.
  - The hierarchical neuroplasticity model is theoretical and not derived from a systematic
    review of longitudinal imaging data.
  - Aphasia type classification varies across cited studies, limiting comparability.
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-07
    paper_section: Section 2.1.2–2.1.3 (pp. 13–14); Section 3 (p. 5 of article)
    confidence: high
    flags: []
- id: f3
  target: age_gender_education
  target_kind: predictor
  claim: 'Demographic factors (gender, age, handedness, education) are not robust
    predictors of post-stroke aphasia recovery. Gender evidence is weak and inconsistent.
    Age has a tendency toward worse outcomes in older patients but is not consistently
    significant across studies. Handedness has no demonstrated influence. Education
    may confer some protection against language disruption but does not consistently
    predict recovery.

    '
  direction: no_effect
  relationship: synthesis
  citation: '@Watila2015'
  method: narrative_review
  design: narrative-review
  evidence_quality: narrative-review
  strength: weak
  source_passages:
  - section: \'narrative synthesis\'
    quote: weak and inconclusive evidence that gender predicts functional recovery
      from aphasia
    page: 3
    supports: claim
  - section: \'narrative synthesis\'
    quote: influence of age on aphasia recovery still remains unclear, with a tendency
      for older patients to have a poorer recovery
    page: 3
    supports: claim
  - section: \'narrative synthesis\'
    quote: not shown any influence between handedness and aphasia recovery
    page: 4
    supports: claim
  primary_papers_cited:
  - Pedersen2004
  - Lazar2010
  - Laska2001
  author_limitations:
  - Studies disagree substantially on age effects; no systematic weighting by study
    quality.
  - Most studies on demographic predictors are older observational cohorts with variable
    aphasia assessment tools.
  - Education and socioeconomic status are highly correlated and their independent
    effects are unclear.
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-07
    paper_section: Section 2.2.1–2.2.5 (pp. 14–15)
    confidence: high
    flags: []
reviewer: michele
reviewed_on: '2026-05-07'
---
