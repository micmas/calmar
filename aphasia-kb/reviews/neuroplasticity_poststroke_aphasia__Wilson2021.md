---
schema_version: 2.4
id: neuroplasticity_poststroke_aphasia__Wilson2021
name: Neuroplasticity in Post-Stroke Aphasia — Systematic Review and Meta-Analysis
  of Functional Imaging Studies
kind: neuroplasticity
status: approved
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-07
short_description: 'PRISMA-registered systematic review and meta-analysis (PROSPERO
  CRD42018116295) of 86 fMRI/PET studies (1995–2020) examining functional reorganisation
  of language processing in post-stroke aphasia. Identified 561 relevant analyses
  across cross-sectional and longitudinal designs. Three critical methodological issues
  evaluated: task performance confounds, contrast validity, and correction for multiple
  comparisons — found to be pervasive limitations. Meta-analytic synthesis identified
  two strongly supported claims: (1) reduced LH language region activation in aphasia
  vs. controls; (2) positive correlation between LH language activation and language
  function. Evidence for right hemisphere homotopic recruitment is modest and equivocal;
  no compelling evidence for longitudinal dynamic reorganisation.

  '
findings:
- id: f1
  target: left_hemisphere_language_network_aphasia
  target_kind: predictor
  claim: 'Left hemisphere language regions (particularly IFG pars opercularis, pars
    triangularis, and posterior superior temporal gyrus) are consistently less activated
    in individuals with aphasia compared to neurologically normal controls. This pattern
    was confirmed across 24 methodologically robust cross-sectional analyses from
    12 studies, with statistically significant predominance of activation decreases
    in left IFGop, left IFGtri, and left pSTG after correction for multiple comparisons.

    '
  direction: likely
  relationship: synthesis
  citation: '@Wilson2021'
  method: narrative_review
  design: systematic-review
  evidence_quality: narrative-review
  strength: moderate
  source_passages:
  - section: \'narrative synthesis\'
    quote: left hemisphere language regions are less activated in individuals with
      aphasia than in neurologically normal controls
    page: 1
    supports: claim
  - section: \'narrative synthesis\'
    quote: more prevalent than increases throughout the left IFG and left posterior
      temporal cortex
    page: 39
    supports: claim
  - section: \'narrative synthesis\'
    quote: statistically significant after correction for multiple comparisons in
      the pars opercularis
    page: 39
    supports: claim
  primary_papers_cited:
  - Sharp2004
  - CrinionPrice2005
  - vanOers2010
  - Szaflarski2014
  - GriffisNenert2017
  author_limitations:
  - 84% of 204 voxelwise analyses had major limitations in multiple-comparisons correction;
    only 18% used satisfactory approaches.
  - Task performance confounds (accuracy and RT mismatches) were present in approximately
    75% of second-level analyses.
  - Contrast validity demonstrated in neurologically normal individuals in only 12%
    of 129 contrasts.
  - Activation decreases in aphasia vs. controls may partly reflect failure to engage
    the language network rather than true reorganisation.
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-07
    paper_section: Abstract; Results — Cross-sectional aphasia vs. control (pp. 59–61);
      Discussion (pp. 64–66)
    confidence: high
    flags: []
- id: f2
  target: left_hemisphere_activation_language_function_correlation
  target_kind: predictor
  claim: 'Within-group correlations in individuals with aphasia show that left hemisphere
    language region activation is positively associated with language function. This
    was supported by 42 methodologically robust cross-sectional correlational analyses
    from 14 studies. The strongest and most consistent finding was in the left IFG
    pars triangularis (positive correlation with language function significant after
    correction, p < 0.0001). Positive correlations were also found in the left IFG
    pars orbitalis and left anterior temporal lobe. A right mid temporal region (undamaged)
    showed positive correlations in three methodologically robust analyses, though
    this may reflect premorbid rather than compensatory capacity.

    '
  direction: likely
  relationship: synthesis
  citation: '@Wilson2021'
  method: narrative_review
  design: systematic-review
  evidence_quality: narrative-review
  strength: moderate
  source_passages:
  - section: \'narrative synthesis\'
    quote: activity in left hemisphere language regions, and possibly a temporal lobe
      region in the right hemisphere, is positively correlated with language function
    page: 1
    supports: claim
  - section: \'narrative synthesis\'
    quote: left IFG pars triangularis was the region with the greatest relative prevalence
      of positive over negative correlations
    page: 40
    supports: claim
  - section: \'narrative synthesis\'
    quote: observed in three methodologically robust analyses
    page: 49
    supports: claim
  primary_papers_cited:
  - CrinionPrice2005
  - Crinion2006
  - Warren2009
  - Fridriksson2010
  - Tyler2011
  - Papoutsi2011
  - Nenert2018
  author_limitations:
  - Positive correlations between LH activation and language function may in part
    directly reflect lesion effects (damaged regions show both reduced activation
    and worse language).
  - Right mid temporal positive correlations are equivocal — may reflect premorbid
    individual differences rather than compensatory reorganisation.
  - Many correlational analyses (75%) were not matched for accuracy at the second
    level — potential task performance confounds.
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-07
    paper_section: Results — Cross-sectional correlation (pp. 61–63); Discussion (pp.
      65–67)
    confidence: high
    flags: []
- id: f3
  target: right_hemisphere_homotopic_recruitment
  target_kind: predictor
  claim: 'Evidence for differential recruitment of right hemisphere homotopic regions
    in individuals with aphasia (relative to controls) is modest and equivocal. Only
    three methodologically robust cross-sectional analyses from two studies (Leff
    et al. 2002, Blank et al. 2003) provided compelling evidence for right hemisphere
    homotopic increases, specifically in the right pSTS and right IFG pars opercularis.
    Consideration of all analyses without regard for limitations shows a consistent
    trend of more activation increases than decreases in right homotopic regions,
    but the clinical significance of right hemisphere recruitment for recovery remains
    uncertain.

    '
  direction: mixed
  relationship: synthesis
  citation: '@Wilson2021'
  method: narrative_review
  design: systematic-review
  evidence_quality: narrative-review
  strength: weak
  source_passages:
  - section: \'narrative synthesis\'
    quote: modest, equivocal evidence for the claim that individuals with aphasia
      differentially recruit right hemisphere homotopic regions
    page: 1
    supports: claim
  - section: \'narrative synthesis\'
    quote: a quarter century of research has produced only three moderately compelling
      analyses suggesting increased activity in right hemisphere regions
    page: 50
    supports: claim
  - section: \'narrative synthesis\'
    quote: increases were more prevalent than decreases in right hemisphere homotopic
      regions, reaching significance in the right IFG pars opercularis
    page: 39
    supports: claim
  primary_papers_cited:
  - Leff2002
  - Blank2003
  author_limitations:
  - The classical lesion-disruption evidence for right hemisphere role in recovery
    (Barlow 1877; Kinsbourne 1971) is indirect and decades old.
  - Leff et al. and Blank et al. had small samples (6–12 patients) and used contrasts
    of only moderate validity.
  - Right hemisphere activation in aphasia may reflect task difficulty and increased
    domain-general effort rather than language reorganisation.
  - No longitudinal methodologically robust analyses demonstrated dynamic right hemisphere
    upregulation over time.
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-07
    paper_section: Discussion — Right homotopic recruitment (pp. 66–68)
    confidence: high
    flags: []
- id: f4
  target: longitudinal_language_network_reorganisation
  target_kind: predictor
  claim: 'There is essentially no methodologically robust longitudinal evidence for
    dynamic reorganisation of the language network after stroke. Of 132 longitudinal
    analyses, only 5 were methodologically robust and only 2 had positive findings
    (from Saur et al. 2006): increased activation from 2 days to 2 weeks in right
    insula/SMA (interpreted as transient upregulation), and increased activation from
    2 days to 1 year in left pMTG (interpreted as left hemisphere return-to-function,
    not reorganisation). No robust longitudinal correlation analyses supported dynamic
    reorganisation.

    '
  direction: no_effect
  relationship: synthesis
  citation: '@Wilson2021'
  method: narrative_review
  design: systematic-review
  evidence_quality: narrative-review
  strength: moderate
  source_passages:
  - section: \'narrative synthesis\'
    quote: essentially no evidence for dynamic reorganization of the language network
      over time
    page: 51
    supports: claim
  - section: \'narrative synthesis\'
    quote: 5 out of 132 longitudinal analyses were appraised as methodologically robust,
      and only 2 of those 5 analyses had positive findings
    page: 51
    supports: claim
  - section: \'narrative synthesis\'
    quote: 77 analyses in which correlations were computed within a group of individuals
      with aphasia
    page: 42
    supports: claim
  primary_papers_cited:
  - Saur2006
  author_limitations:
  - Paucity of robust longitudinal findings may reflect true absence of macroscopic
    reorganisation, high individual variability, or methodological limitations of
    existing studies.
  - Small sample sizes dominate the literature: 37% of 86 studies had fewer than 12
      participants.
  - Future large collaborative studies with proper correction for multiple comparisons
    are needed to definitively address longitudinal reorganisation.
  - Task performance changes over time confound longitudinal activation comparisons
    in nearly all studies.
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-07
    paper_section: Results — Longitudinal analyses (pp. 62–65); Discussion (pp. 68–69)
    confidence: high
    flags: []
reviewer: michele
reviewed_on: '2026-05-07'
---
