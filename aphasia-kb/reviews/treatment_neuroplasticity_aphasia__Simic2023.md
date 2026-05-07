---
schema_version: 2.4
id: treatment_neuroplasticity_aphasia__Simic2023
name: Treatment-Induced Neuroplasticity After Anomia Therapy in Post-Stroke Aphasia
  — Systematic Review of Neuroimaging Studies
kind: neuroplasticity
status: approved
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-07
short_description: 'PRISMA-compliant systematic review of 33 studies (43 articles;
  N=161 in group studies) examining MRI-detected neural changes following behavioural
  anomia treatment in post-stroke aphasia. Searched CINAHL, Cochrane, Embase, Ovid
  MEDLINE, MEDLINE-in-Process, PsycINFO (yielded 2481 unique citations). Most studies
  used fMRI; methodological quality of neuroimaging reporting was variable. Post-treatment
  activation increases were primarily in left supramarginal gyrus (SMG) and bilateral
  precunei. Connectivity data linked naming improvement most robustly to left-hemisphere
  and perilesional changes. Highlights paucity of robust evidence for direct brain-behaviour
  links in anomia rehabilitation.

  '
findings:
- id: f1
  target: left_supramarginal_gyrus
  target_kind: region
  claim: 'Across both group- and case-level task-based fMRI studies, the left rostral
    inferior parietal lobule (supramarginal gyrus, SMG) is the most consistently reported
    region showing increased activation following anomia therapy, and increases in
    left SMG activation are correlated with behavioural naming improvements. The SMG
    is implicated in the dorsal auditory-motor integration stream supporting phonological
    production.

    '
  direction: likely
  relationship: synthesis
  citation: '@Simic2023'
  method: narrative_review
  design: systematic-review
  evidence_quality: narrative-review
  strength: moderate
  source_passages:
  - section: \'narrative synthesis\'
    quote: left rostral IPL (i.e., SMG) consistently demonstrated increased activation
      in both case- and group-level data
    page: 18
    supports: claim
  - section: \'narrative synthesis\'
    quote: was also correlated with behavioural naming improvements
    page: 18
    supports: claim
  - section: \'narrative synthesis\'
    quote: significant increases in activation following therapy
    page: 1
    supports: claim
  primary_papers_cited:
  - Abel2014
  - Abel2015
  - vanHees2014
  - Fridriksson2012
  author_limitations:
  - Fewer than 40% of eligible studies corrected for multiple comparisons, limiting
    strength of activation conclusions.
  - Very few studies correlated pre-to-post neural changes with behavioural naming
    improvements — direct brain-behaviour links remain sparse.
  - Methodological heterogeneity in MRI preprocessing, lesion masking, statistical
    thresholds was substantial and variable across reports.
  - Most participants were in chronic stages of recovery; findings may not generalise
    to acute/subacute phases.
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-07
    paper_section: Abstract; Results (pp. 14–15); Discussion 4.3.1 (pp. 18–19)
    confidence: high
    flags: []
- id: f2
  target: left_hemisphere_connectivity_naming_improvement
  target_kind: predictor
  claim: 'Pre-to-post treatment improvements in naming are more frequently associated
    with neural change when measured via functional or structural connectivity than
    via activation alone. Naming improvement is predominantly linked to increased
    connectivity of left hemisphere ROIs and perilesional areas within the language
    network, including the left IFG, left MTG, and left SMG. Microstructural improvements
    in the left arcuate fasciculus (dorsal stream) and left inferior longitudinal
    fasciculus (ventral stream) have also been correlated with naming gains.

    '
  direction: likely
  relationship: synthesis
  citation: '@Simic2023'
  method: narrative_review
  design: systematic-review
  evidence_quality: narrative-review
  strength: weak
  source_passages:
  - section: \'narrative synthesis\'
    quote: improvements in naming were more frequently associated with neural change
      in studies reporting measures of structural and functional connectivity
    page: 21
    supports: claim
  - section: \'narrative synthesis\'
    quote: predominantly associated with increased connectivity of left hemisphere
      ROIs and perilesional areas
    page: 21
    supports: claim
  - section: \'narrative synthesis\'
    quote: FA of the left arcuate fasciculus following alternating semantic and phonological
      cueing treatments
    page: 21
    supports: claim
  primary_papers_cited:
  - Abel2015
  - Abutalebi2009
  - Kiran2015
  - Sandberg2015
  - vanHees2014c
  - McKinnon2017
  author_limitations:
  - Structural and functional connectivity studies are few in number, limiting generalisability
    of connectivity findings.
  - Most connectivity studies lacked correction for multiple comparisons or employed
    ROI-based approaches without clear anatomical justification.
  - Co-registration of anatomical and functional images and lesion masking during
    normalisation were reported in fewer than half of studies.
  - Treatment protocols varied (SFA, PCA, phonological cueing, CILT variants), making
    it impossible to attribute connectivity changes to specific therapies.
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-07
    paper_section: Results 3.4.2 (pp. 15–16); Discussion 4.3.2 (pp. 21–22)
    confidence: high
    flags: []
- id: f3
  target: left_ifg_disconnection_treatment_response
  target_kind: predictor
  claim: 'Disconnection of the left IFG is associated with poorer treatment gains
    after anomia therapy, not only by disrupting anterior-posterior left-hemisphere
    language network communication, but also by limiting activation of right hemisphere
    homotopic compensatory areas. Greater rsFC in left MTG, left SMG, and right IFG
    pars triangularis at baseline predicted better naming improvement after phonological
    cueing treatment.

    '
  direction: likely
  relationship: synthesis
  citation: '@Simic2023'
  method: narrative_review
  design: systematic-review
  evidence_quality: narrative-review
  strength: weak
  source_passages:
  - section: \'narrative synthesis\'
    quote: disconnection of the left IFG was associated with poorer treatment gains
      after alternating semantic and phonological
    page: 16
    supports: claim
  - section: \'narrative synthesis\'
    quote: rsFC in the left MTG, left SMG and right IFG pars triangularis was significantly
      correlated with naming improvements
    page: 16
    supports: claim
  - section: \'narrative synthesis\'
    quote: large lesions of the left IFG disconnect not only anterior and posterior
      language areas but may also disrupt
    page: 16
    supports: claim
  primary_papers_cited:
  - Abel2015
  - vanHees2014c
  author_limitations:
  - Only one study reported left IFG disconnection as a treatment predictor; single-study
    inference.
  - rsFC predictor finding comes from a single study (van Hees et al. 2014c) with
    a small sample.
  - Causal direction of the connectivity-treatment response relationship cannot be
    established from pre-post designs.
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-07
    paper_section: Discussion 3.4.2.2 Connectivity findings (pp. 15–16)
    confidence: medium
    flags: []
reviewer: michele
reviewed_on: '2026-05-07'
---
