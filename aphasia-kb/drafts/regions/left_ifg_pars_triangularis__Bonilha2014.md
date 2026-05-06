---
schema_version: 2.3
id: left_ifg_pars_triangularis
name: Left IFG Pars Triangularis (BA 45)
kind: classical
status: draft
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-06
hemisphere: left
aliases:
- BA 45
- pars triangularis
- left BA45
notes: 'Forward-looking target ID left_ifg_pars_triangularis — not yet a canonical entry.

  This draft covers disconnectome findings from Bonilha 2014, which examines cortical necrosis

  AND cortical disconnection (via DTI connectome) as independent predictors of naming and fluency.

  Method coded as `disconnectome` per the EXTRACTION_SKILL controlled vocabulary.

  Cohort (n=39) is from USC and MUSC (Bonilha, Rorden, Fridriksson lab group); may overlap with

  @Fridriksson2018Anatomy and other USC-lab papers — flag for double-counting risk.

  The original f3 (BA22 disconnection → auditory comprehension) was split out on 2026-05-06

  into drafts/regions/left_posterior_stg__Bonilha2014.md because that finding is anatomically

  about BA22, not BA45.

  '
findings:
- id: f1
  target: naming
  target_kind: impairment
  claim: Structural disconnection of left BA 45 (pars triangularis), independent of BA 45 cortical necrosis,
    is associated with poorer naming performance on the Philadelphia Naming Test in chronic aphasia after
    left-hemisphere stroke.
  direction: likely
  relationship: causal
  citation: '@Bonilha2014'
  method: disconnectome
  design: cross-sectional
  imaging: multimodal
  sample:
    n: 39
    population: chronic left-hemisphere ischemic stroke survivors with aphasia
    time_post_onset: '>=6 months prior to enrollment'
    age_range: mean 62.7 years (SD 12.8)
    handedness: all right-handed prior to stroke
    language: not_reported
    recruitment: Recruited from local community at Medical University of South Carolina (MUSC) and University
      of South Carolina (USC).
    inclusion_criteria: Left hemisphere ischemic stroke >=6 months prior; right-handed; able to ambulate;
      no history of other neurological illness or learning disability.
    exclusion_criteria: History of learning disability; uncontrolled seizures; severe motor impairment
      (unable to ambulate).
  statistics:
    threshold: p<0.05 Bonferroni-corrected for number of regressions
    cluster_extent: not_reported
    effect_size: 'necrosis: beta=0.43, p=0.03; disconnection: beta=1.21, p<0.001'
    ci_95: not_reported
    p_value: F=4.62, p<0.01 (overall model)
  confounders_controlled:
  - BA 45 cortical necrosis (entered simultaneously in multiple linear regression)
  - Bonferroni correction for number of regressions across BAs tested
  confounders_not_controlled:
  - 'overall lesion volume (not independently associated with naming: r=-0.07, p=0.67)'
  - time post-onset
  - age
  - education
  - aphasia type
  region_definition:
    kind: atlas
    atlas: Brodmann area atlas (probabilistic grey matter segmentation)
    description: BA 45 defined using probabilistic grey matter parcellation from T1-weighted images segmented
      into Brodmann areas. Connectivity quantified as number of DTI streamlines between BA 45 and all
      other cortical BAs, normalized for region volume.
  imaging_details:
    field_strength: 3T
    acquisition:
      sequence: T1-weighted MPRAGE + T2-weighted + DTI deterministic fiber tractography
      voxel_size_mm: not_reported
      TR_ms: not_reported
      TE_ms: not_reported
    modalities:
    - modality: T1
      sequence: MPRAGE
      notes: Siemens Trio 3T with 12-channel head coil at USC and MUSC
    - modality: DTI
      notes: Deterministic fiber tractography; full acquisition parameters in Online Supplement (not in
        main text)
    preprocessing_pipeline: SPM-based cortical segmentation into Brodmann areas; T1-to-DTI registration;
      deterministic tractography for pairwise connectome reconstruction; necrotic tissue excluded from
      tractography seeding and waypoint masks
    reference_space: not_reported
    atlases_used:
    - Brodmann area atlas (probabilistic)
    coordinates_reported: []
  replications: []
  contradictions: []
  author_limitations:
  - MRI tractography has known technical limitations; structural connectome mapping is a novel methodological
    approach and results should be interpreted cautiously.
  - Study focused on a small set of cortical BAs (22, 37, 45) — disconnection in other regions may also
    contribute.
  - Physiological hemispheric asymmetries were not fully accounted for, though none of the ROIs tested
    (except part of BA 45) showed significant asymmetry in healthy subjects.
  - Small sample (n=39) limits statistical power.
  - DTI acquisition parameters (b-value, number of directions, voxel size) available in Online Supplement
    only.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Abstract; Results – Regional necrosis and connectivity; Methods – Subjects, MRI acquisition,
      Statistical Analyses; Discussion
    confidence: high
    flags:
    - cohort overlaps with @Fridriksson2018Anatomy (same USC/MUSC lab group; Bonilha 2014 n=39; Fridriksson
      2018Anatomy n=159); flag for downstream double-counting risk in interpret_overlap()
    - DTI acquisition parameters (b-values, directions, voxel size) are in Online Supplement only — verify
      against supplement for imaging_details completeness
    - reference_space not explicitly stated in main text — likely native Brodmann-atlas space; verify
    - disconnection beta (1.21) exceeds necrosis beta (0.43) — paper interprets disconnection as having
      greater predictive weight than necrosis for naming
  source_passages:
  - section: Abstract
    page: 1
    supports: claim
    quote: 'structural disconnection of BA 45 (spared by the necrotic tissue) was independently associated
      with naming performance, controlling for the extent of BA 45 necrosis (F=4.62, p<0.01; necrosis:
      beta=0.43; p=0.03; disconnection beta=1.21; p<0.001).'
  - section: Methods – Subjects
    page: 2
    supports: sample
    quote: We studied thirty-nine individuals (mean age 62.7 +/-12.8 years, 22 male, 16 female) who suffered
      a left hemisphere ischemic stroke at least six months prior to enrolling in this study
  - section: Methods – MRI acquisition
    page: 3
    supports: imaging_details
    quote: MRI scanning was performed using the same type of MRI scanner, i.e., a 3T Siemens Trio equipped
      with a 12-channel head coil.
  - section: Methods – Statistical Analyses
    page: 4
    supports: method
    quote: 'We performed multiple linear regression analyses with the performance on naming measures defined
      as the dependent variable, with the following independent variables: 1) percentage of damage to
      each BA area, 2) percentage number of fibers of each BA area.'
  - section: Methods – Statistical Analyses
    page: 4
    supports: statistics
    quote: The level of statistical significance was set at p<0.05, adjusted through Bonferroni correction
      based on the number of regressions investigated.
  - section: Results – Regional necrosis and connectivity and language impairment
    page: 5
    supports: statistics
    quote: 'We observed a significant relationship between number of correctly named items on the PNT
      and a model composed of BA 45 necrotic damage and BA 45 disconnection (F=4.62, p<0.01; necrosis:
      beta=0.43; p=0.03; disconnection beta=1.21; p<0.001)'
  - section: Discussion
    page: 6
    supports: limitation
    quote: Although MRI tractography has the advantage of providing in-vivo information about structural
      brain integrity, it is not without technical limitations.
- id: f2
  target: fluency
  target_kind: impairment
  claim: Structural disconnection of left BA 45 (pars triangularis), independent of BA 45 cortical necrosis,
    is independently associated with reduced speech fluency in chronic aphasia after left-hemisphere stroke;
    BA 45 necrosis alone is not an independent predictor of fluency.
  direction: likely
  relationship: causal
  citation: '@Bonilha2014'
  method: disconnectome
  design: cross-sectional
  imaging: multimodal
  sample:
    n: 39
    population: chronic left-hemisphere ischemic stroke survivors with aphasia
    time_post_onset: '>=6 months'
    age_range: mean 62.7 years (SD 12.8)
    handedness: all right-handed
    language: not_reported
    recruitment: MUSC and USC local community.
  statistics:
    threshold: p<0.05 Bonferroni-corrected
    cluster_extent: not_reported
    effect_size: 'necrosis: beta=2.89, p=0.13 (not independently significant); disconnection: beta=7.52,
      p=0.025'
    ci_95: not_reported
    p_value: F=4.62, p<0.01 (overall model)
  confounders_controlled:
  - BA 45 cortical necrosis (entered simultaneously in multiple linear regression)
  - Bonferroni correction
  confounders_not_controlled:
  - overall lesion volume
  - age
  - time post-onset
  region_definition:
    kind: atlas
    atlas: Brodmann area atlas (probabilistic grey matter segmentation)
    description: BA 45 defined via probabilistic Brodmann parcellation; connectivity as number of normalized
      DTI streamlines.
  imaging_details:
    field_strength: 3T
    acquisition:
      sequence: T1-weighted MPRAGE + DTI deterministic tractography
      voxel_size_mm: not_reported
      TR_ms: not_reported
      TE_ms: not_reported
    preprocessing_pipeline: SPM-based Brodmann parcellation; deterministic tractography connectome; necrotic
      tissue excluded from tractography
    reference_space: not_reported
    atlases_used:
    - Brodmann area atlas (probabilistic)
    coordinates_reported: []
  replications: []
  contradictions: []
  author_limitations:
  - BA 45 necrosis alone was not independently associated with fluency (p=0.13) — the full model is significant
    only via the disconnection term.
  - Small sample (n=39); DTI tractography technical limitations.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results – Regional necrosis and connectivity and language impairment
    confidence: high
    flags:
    - necrosis alone NOT independently associated with fluency (p=0.13); only disconnection significant
      (p=0.025) — important distinction from the naming finding where necrosis was also significant
    - cohort overlaps with @Fridriksson2018Anatomy — flag for downstream double-counting risk
    - F=4.62 p<0.01 identical to naming model F-value — this appears as coincidental rounding in the manuscript;
      verify against published Table
  source_passages:
  - section: Results – Regional necrosis and connectivity and language impairment
    page: 5
    supports: claim
    quote: 'we also observed significant relationship between fluency and a model composed by BA 45 necrosis
      and BA 45 disconnection F=4.62, p<0.01; necrosis: beta=2.89; p=0.13; disconnection beta=7.52; p=0.025).
      Similarly, in this model, necrosis alone was not an independent predictor of fluency'
  - section: Methods – Subjects
    page: 2
    supports: sample
    quote: We studied thirty-nine individuals (mean age 62.7 +/-12.8 years, 22 male, 16 female) who suffered
      a left hemisphere ischemic stroke at least six months prior to enrolling in this study
  - section: Methods – Statistical Analyses
    page: 4
    supports: method
    quote: 'We performed multiple linear regression analyses with the performance on naming measures defined
      as the dependent variable, with the following independent variables: 1) percentage of damage to
      each BA area, 2) percentage number of fibers of each BA area.'
  - section: Methods – MRI acquisition
    page: 3
    supports: imaging_details
    quote: MRI scanning was performed using the same type of MRI scanner, i.e., a 3T Siemens Trio equipped
      with a 12-channel head coil.
  - section: Discussion
    page: 6
    supports: limitation
    quote: our study focused on a small set of cortical regions, including BA 45, to clearly demonstrate
      how disconnection contributes to behavioral impairment.
source: draft
---

# Left IFG Pars Triangularis (BA 45) — Bonilha 2014 (Disconnectome)

Bonilha et al. 2014 demonstrates that structural disconnection of BA 45 predicts naming and fluency
performance beyond what is explained by cortical necrosis alone in 39 chronic aphasia patients.
(BA 22 disconnection — comprehension finding — moved to left_posterior_stg__Bonilha2014.md.) The primary methodological contribution is
the connectome-based approach to quantifying white matter connectivity separate from frank lesion necrosis.

Key finding: disconnection beta weights exceed necrosis beta weights for both naming and fluency,
suggesting that "invisible" white matter damage beyond the visible lesion is a clinically significant
independent predictor of aphasia severity.
