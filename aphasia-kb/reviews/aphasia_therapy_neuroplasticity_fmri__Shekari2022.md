---
schema_version: 2.4
id: aphasia_therapy_neuroplasticity_fmri__Shekari2022
name: Mechanisms of Brain Activation Following Naming Therapy in Aphasia — Systematic
  Review of Task-Based fMRI Studies
kind: neuroplasticity
status: approved
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-07
short_description: 'Systematic review of 14 task-based fMRI studies (146 participants)
  examining brain reorganisation after semantic- and phonological-based anomia therapy
  in chronic post-stroke aphasia. Data synthesised narratively (no meta-analysis conducted
  due to study heterogeneity). Both left and right hemisphere areas are implicated
  in naming improvement; greater improvement is associated with left hemisphere cortical
  activation increase, particularly in IFG, MFG and perilesional areas. Lesion size
  and severity modulate hemispheric recruitment pattern.

  '
findings:
- id: f1
  target: left_hemisphere_language_network
  target_kind: region
  claim: 'Following anomia therapy, naming improvement is predominantly associated
    with increased activation in left hemisphere language-related areas (inferior
    frontal gyrus, middle frontal gyrus, superior frontal gyrus, supramarginal gyrus),
    with more significant naming gains linked to greater left-hemisphere cortical
    activation increases relative to right-hemisphere recruitment.

    '
  direction: likely
  relationship: synthesis
  citation: '@Shekari2022'
  method: narrative_review
  design: systematic-review
  evidence_quality: narrative-review
  strength: weak
  source_passages:
  - section: \'narrative synthesis\'
    quote: more significant improvement in successful naming is associated with a
      tremendous increase in left hemisphere cortical
    page: 9
    supports: claim
  - section: \'narrative synthesis\'
    quote: activation of left language-related areas. On the other hand, larger lesion
      size was associated with slight naming
    page: 9
    supports: claim
  - section: \'narrative synthesis\'
    quote: activation of left IFG and its right homologs was associated with naming
      improvement after both semantic and phonemic
    page: 13
    supports: claim
  primary_papers_cited:
  - Fridriksson2007
  - Fridriksson2012
  - Marcotte2012
  - vanHees2014
  - Vitali2007
  - Abel2014
  - Abel2015
  author_limitations:
  - Only 14 studies included; small corpus limits generalisability.
  - Studies used diverse therapies (SFA, PCA, phonological cueing), acquisition protocols,
    and statistical thresholds — heterogeneity precluded meta-analysis.
  - None of the studies reported random sampling, blinding, or treatment fidelity.
  - All participants were in chronic aphasia stage; results may not generalise to
    acute/subacute phases.
  - No studies conducted on multilingual participants.
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-07
    paper_section: Results — Relationship between LH and RH activation (pp. 9–10);
      Brain areas related to naming improvement (pp. 13–16)
    confidence: high
    flags: []
- id: f2
  target: lesion_size_hemispheric_lateralisation
  target_kind: predictor
  claim: 'Lesion size moderates hemispheric recruitment during anomia therapy: smaller
    lesions are associated with naming improvement linked to left hemisphere perilesional
    activation, whereas larger lesions are associated with weaker naming gains involving
    right hemisphere recruitment. Severity of word-finding difficulty and the level
    of impaired word retrieval processing further modulate which brain areas are recruited.

    '
  direction: mixed
  relationship: synthesis
  citation: '@Shekari2022'
  method: narrative_review
  design: systematic-review
  evidence_quality: narrative-review
  strength: weak
  source_passages:
  - section: \'narrative synthesis\'
    quote: small lesion size is associated with more significant improvements after
      anomia therapy
    page: 9
    supports: claim
  - section: \'narrative synthesis\'
    quote: larger lesion size was associated with slight naming improvement. This
      improvement was related to the activation of the right areas
    page: 9
    supports: claim
  - section: \'narrative synthesis\'
    quote: severity of word-finding difficulties, impaired levels of word retrieval
      processing may also be related to response
    page: 10
    supports: claim
  primary_papers_cited:
  - Vitali2007
  - Fridriksson2007
  - Abel2015
  - Marcotte2012
  - Menke2009
  - vanHees2014
  author_limitations:
  - Lesion size reported inconsistently or not at all across primary studies — quantitative
    comparison not possible.
  - Direction of lesion-size effects inferred from across-study comparison rather
    than within-study analysis.
  - Confounding by aphasia type and severity not systematically controlled.
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-07
    paper_section: Relationship between RH and LH activation (pp. 9–10); Subcortical
      structures (pp. 16–17)
    confidence: medium
    flags: []
- id: f3
  target: treatment_type_neural_specificity
  target_kind: therapy
  claim: 'The type of anomia therapy (semantic vs. phonological cueing) is associated
    with partially dissociable patterns of brain activation: phonological therapies
    tend to increase activation in phonological processing areas (MFG, SMG, IFG pars
    opercularis), while semantic therapies engage semantic processing regions (IFG
    pars triangularis, angular gyrus, STG), though overlap is substantial and findings
    are not fully consistent across studies.

    '
  direction: likely
  relationship: synthesis
  citation: '@Shekari2022'
  method: narrative_review
  design: systematic-review
  evidence_quality: narrative-review
  strength: weak
  source_passages:
  - section: \'narrative synthesis\'
    quote: pars opercularis after phonemic-based therapy is probably due to the role
      of this
    page: 14
    supports: claim
  - section: \'narrative synthesis\'
    quote: pars triangularis with semantic treatment outcomes
    page: 14
    supports: claim
  - section: \'narrative synthesis\'
    quote: need for a more systematic investigation of the association
    page: 2
    supports: limitation
  primary_papers_cited:
  - Abel2014
  - Abel2015
  - Marcotte2010
  - vanHees2014
  author_limitations:
  - Findings on therapy-type dissociations are based on a very small number of studies
    and should be considered preliminary.
  - Diverse outcome measures and task contrasts across fMRI studies limit comparability.
  - Studies used different control tasks, making brain activation contrasts non-equivalent.
  - Lack of randomised controlled designs; most are pre-post without adequate control
    groups.
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-07
    paper_section: Table 5 (p. 10); IFG discussion (pp. 13–14); MFG discussion (p.
      14)
    confidence: medium
    flags: []
reviewer: michele
reviewed_on: '2026-05-07'
---
