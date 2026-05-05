---
schema_version: 2.3
id: typicality_semantic_feature_analysis
name: Typicality-based Semantic Feature Analysis (SFA)
aliases:
- typicality-based SFA
- typicality SFA
- semantic feature analysis (typicality variant)
kind: therapy
status: approved
created_by: agent:claude-opus-4-7
created_on: 2026-05-01
short_description: An impairment-based naming intervention for anomic aphasia in which
  typical (e.g., pigeon) or atypical (e.g., penguin) exemplars of a semantic category
  (e.g., birds) are trained through category sorting, auditory and written feature
  verification, and feature review. A typicality-manipulation variant of classical
  Semantic Feature Analysis (Boyle 2004).
targets_impairments:
- anomia
dosage: 12 weeks, 2 sessions/week, 1.5 h/session (Barbieri et al. 2023; Johnson et
  al. 2019; Gilmore et al. 2019 protocol). Each participant trained on half of the
  items (n=36) in two combinations of semantic category × typicality.
findings:
- id: f1
  target: anomia
  target_kind: impairment
  claim: Twelve weeks of typicality-based semantic feature analysis treatment significantly
    improves naming accuracy on trained items in chronic anomic aphasia compared to
    a no-treatment natural history control group.
  direction: likely
  relationship: responder
  citation: '@Barbieri2023'
  method: clinical_RCT
  design: RCT
  imaging: none
  sample:
    n: 17
    population: chronic stroke-induced anomic aphasia (single left-hemisphere stroke
      ≥12 months post-onset; subgroup of n=58 analyzed cohort, recruited at Boston
      University)
    time_post_onset: mean 60.0 months (SD 53.1)
    age_range: mean 62.0 years (SD 8.8)
    handedness: all right-handed
    language: monolingual native English speakers
    recruitment: Aphasia Research Lab at Boston University; randomized to treatment
      vs. natural history at the site by a staff member other than the assessor.
    inclusion_criteria: age 35–80; education ≥high-school; WAB-AQ 45–95; anomia per
      a study-specific naming battery including natural and artificial objects from
      four semantic categories.
    exclusion_criteria: exclusively subcortical lesions; non-monolingual; developmental/psychiatric/other
      neurological history; MRI contraindications.
  statistics:
    threshold: mixed-effects regression with FDR correction; p<0.0001 for the Time
      effect within the naming treatment group
    cluster_extent: null
    effect_size: β = 1.447 (z-scored accuracy units), SE 0.178, t(16) = 8.121 (Time
      post- vs. pre-treatment within naming group); β = 1.308, SE 0.318, t(54) = 4.115
      for the Time × Group interaction (naming treatment vs. natural history)
    ci_95: not_reported
    p_value: <0.0001 (within-group); 0.0001 (Time × Group interaction)
  confounders_controlled:
  - age, education, proportion of lesioned left-hemisphere tissue (covariates)
  - natural history group (n=16) used as no-treatment control
  - groups matched on months post-onset, gender, handedness, WAB-AQ, lesion size
  confounders_not_controlled:
  - PI not blinded to treatment allocation
  - naming treatment group had lower education than sentence treatment group (t=2.124,
    p=0.038)
  - naming group had lower canonical sentence comprehension than spelling and natural
    history groups (residual heterogeneity from cross-site recruitment)
  region_definition:
    kind: not_reported
    description: Behavioral-only treatment efficacy finding — no specific brain region;
      treatment efficacy measured as the average change in proportion of correctly
      named items in the two trained category × typicality combinations.
  imaging_details:
    reference_space: not_reported
    atlases_used: []
  replications:
  - '@Boyle2004'
  contradictions: []
  author_limitations:
  - Pre-treatment heterogeneities across treatment groups (different impairment profiles,
    different recruitment sites).
  - Long-term maintenance not assessed.
  - Generalization to untrained items partially assessed (half of category items held
    out) but not the focus of this paper.
  evidence_quality: RCT
  strength: strong
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Results 3.1 + Table 2 (page 83); Methods 2.2 (page 80); Methods
      2.3.1 (page 80)
    confidence: high
    flags:
    - behavioural-only finding.
    - cohort overlaps with Gilmore et al. 2019 and Johnson et al. 2019 — same n=17
      anomic Boston University subgroup (trial NCT01927302); flag for downstream double-counting
      risk in interpret_overlap().
  source_passages:
  - section: Methods 2.2 — Treatment
    page: 80
    supports: method
    quote: At Boston University, the participants treated for anomia underwent a typicality-based
      semantic feature analysis treatment in which typical (e.g., pigeon) or atypical
      (e.g., penguin) exemplars of a certain semantic category (e.g., birds) were
      trained.
  - section: Methods 2.2 — Treatment
    page: 80
    supports: method
    quote: Treatment entailed several steps, including category sorting, auditory
      and written feature veriﬁcation, and feature review.
  - section: Methods 2.1 — Participants
    page: 78
    supports: sample
    quote: '70 met the inclusion criteria for the study: (1) presence of a single
      left-hemisphere stroke at least 12 months prior entering the study and affecting
      at least .1% of the cortical surface in the left hemisphere'
  - section: Methods 2.1 — Participants
    page: 78
    supports: sample
    quote: At Boston University, participants were selected for anomia based on a
      study-speciﬁc naming battery including natural and artiﬁcial objects that belonged
      to four different semantic categories
  - section: Results 3.1 — Treatment effects
    page: 82
    supports: claim
    quote: Post-hoc analyses revealed a signiﬁcant effect of Time, in the direction
      of greater accuracy post- than pre-testing, in all the three treatment groups
      (sentence production/comprehension, naming, spelling, all ps < .0001, Fig. 1),
      whereas no change in accuracy from pre-to post-testing was found in the natural
      history group.
  - section: Table 2 — Treatment effects
    page: 83
    supports: statistics
    quote: Time in Naming vs. Time in NH Group  1.308  .318  54  4.115  .0001
  - section: Methods 2.4.1 — Treatment effects
    page: 81
    supports: confounders
    quote: Mixed-effects regressions were then run using Time (pre-, post-testing)
      and Group (sentence processing treatment, naming treatment, spelling treatment,
      and natural history), as well as all their interaction, as ﬁxed effects, and
      Participant as the only random effect.
  - section: Limitations
    page: 96
    supports: limitation
    quote: participants were recruited from different research centers because they
      met criteria for different language deﬁcits, which resulted in pre-treatment
      heterogeneities across groups in terms of language proﬁles.
- id: f2
  target: right_anterior_middle_temporal_gyrus
  target_kind: region
  claim: Typicality-based semantic feature analysis treatment for anomia produces
    post-treatment voxel-level activation in right anterior temporal regions (aMTG,
    aSTG, temporal pole, pMTG) on a naturalistic auditory story comprehension fMRI
    task — pre-treatment activation in these regions was not significant; post-treatment
    is.
  direction: likely
  relationship: treatment_response
  citation: '@Barbieri2023'
  method: fMRI_activation
  design: RCT
  imaging: fMRI
  sample:
    n: 17
    population: chronic stroke-induced anomic aphasia (Boston University subgroup
      of the n=58 analyzed cohort)
    time_post_onset: mean 60.0 months (SD 53.1)
    age_range: mean 62.0 years (SD 8.8)
    handedness: all right-handed
    language: monolingual native English speakers
  statistics:
    threshold: voxel-level p<0.001, FWE-corrected p<0.05 cluster-level (k≥87 voxels
      for naming-treatment group post-treatment)
    cluster_extent: 257
    effect_size: 'Peak Story>Control activation post-treatment: T=5.590 (right aMTG,
      k=170, MNI [64,-4,-18]), T=5.912 (right temporal pole, k=87, MNI [54,16,-18]).'
    ci_95: not_reported
    p_value: <0.001 voxel-level, FWE-corrected p<0.05 cluster-level
  confounders_controlled:
  - natural history group (n=16) as no-treatment control
  confounders_not_controlled:
  - age, education, lesion size — entered as covariates ONLY in the ROI-based analysis
    (f3), not in this voxel-based one (this is the source of the voxel/ROI disagreement)
  - scanner differences across 3 sites (Siemens Skyra at BU; harmonized via phantom
    scans)
  - control condition (reversed speech) not duration-matched to active condition
  region_definition:
    kind: atlas
    atlas: Harvard-Oxford
    description: 'Voxel-based clusters: right aMTG (extending aSTG and pMTG; peak
      MNI [64,-4,-18], k=170 voxels) and right temporal pole (peak MNI [54,16,-18],
      k=87 voxels). The voxel-based analysis was constrained to ROIs that were active
      in healthy participants on the same task or to their right-hemisphere homologues.'
  imaging_details:
    field_strength: 3T
    acquisition:
      voxel_size_mm:
      - 1.72
      - 1.72
      - 3.0
      TR_ms: 2400
      TE_ms: 20
      sequence: gradient-echo T2*-weighted EPI
    modalities:
    - modality: T1
      sequence: 3D T1-weighted MPRAGE
      voxel_size_mm:
      - 1.0
      - 1.0
      - 1.0
      TR_ms: 2300
      TE_ms: 2.91
    - modality: fMRI
      sequence: gradient-echo T2*-weighted EPI
      voxel_size_mm:
      - 1.72
      - 1.72
      - 3.0
      TR_ms: 2400
      TE_ms: 20
      volumes: 192
    task:
      name: Auditory story comprehension
      description: Block design auditory story comprehension vs reversed-speech control;
        24-s story blocks alternating with 18-s reversed-speech blocks.
      contrasts:
      - Stories > Control
      baseline: Time-reversed speech
    preprocessing_pipeline: AFNI 3dDespike + 3dvolreg motion correction; FD>0.5mm
      and DVARS>50 motion regressors; CompCor; SPM-DARTEL normalization to MNI152
      (2×2×2 mm); 6 mm FWHM smoothing; SPM12 first-level GLM with HRF + time and dispersion
      derivatives; enantiomorphic replacement of left-hemisphere lesion (Nachev 2008)
    reference_space: MNI152
    atlases_used:
    - Harvard-Oxford
    coordinates_reported:
    - region: right anterior MTG (extending aSTG, pMTG)
      mni:
      - 64
      - -4
      - -18
    - region: right temporal pole
      mni:
      - 54
      - 16
      - -18
  replications: []
  contradictions: []
  author_limitations:
  - Voxel-based finding may have been driven by some participants or accounted for
    by age/education/lesion size — see f3 for the corresponding ROI-level result with
    covariates.
  - Pre-treatment heterogeneities and scanner differences.
  evidence_quality: RCT
  strength: moderate
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Results 3.3.2.2 + Table 5 (pages 86–87)
    confidence: high
    flags:
    - 'Voxel-level positive finding; the corresponding ROI-level analysis with covariates
      (f3) found a null effect — the two findings are split per schema convention
      rather than coded as `direction: mixed`.'
    - cohort overlaps with Gilmore et al. 2019 and Johnson et al. 2019 — same n=17
      anomic Boston University subgroup (trial NCT01927302); flag for downstream double-counting
      risk in interpret_overlap().
  source_passages:
  - section: Results 3.3.2.2
    page: 87
    supports: claim
    quote: In both the naming and spelling treatment groups, post-treatment activation
      was limited to right temporal regions, including the aSTG and temporal pole
      (for both groups), and the aMTG and pMTG (for the naming treatment group only).
  - section: Methods 2.3.2.2 — Data acquisition
    page: 81
    supports: imaging_details
    quote: Structural and functional MR images were collected using 3T scanners (Siemens
      Trio at Northwestern University, Siemens Skyra at Boston University, and Philips
      Intera at Johns Hopkins University)
  - section: Methods 2.1 — Participants
    page: 78
    supports: sample
    quote: '70 met the inclusion criteria for the study: (1) presence of a single
      left-hemisphere stroke at least 12 months prior entering the study and affecting
      at least .1% of the cortical surface in the left hemisphere'
  - section: Methods 2.4.2.3 — Voxel-level analyses
    page: 81
    supports: method
    quote: T-maps were obtained by applying a p < .001 threshold at the voxel-level.
      Cluster-level correction was carried out using the family-wise error (FWE) correction
      provided by SPM12, at a threshold of p < .05
  - section: Table 5 — naming treatment post-treatment
    page: 87
    supports: statistics
    quote: Naming treatment (k  87)
- id: f3
  target: right_anterior_middle_temporal_gyrus
  target_kind: region
  claim: Typicality-based semantic feature analysis treatment for anomia does NOT
    produce a significant ROI-level upregulation of activation in right-hemisphere
    language network homologues during a naturalistic auditory story comprehension
    fMRI task, after controlling for age, education, and lesion size — i.e., the voxel-level
    activation in f2 is not robust once individual variability and demographic covariates
    are accounted for.
  direction: no_effect
  relationship: treatment_response
  citation: '@Barbieri2023'
  method: fMRI_activation
  design: RCT
  imaging: fMRI
  sample:
    n: 17
    population: chronic stroke-induced anomic aphasia (Boston University subgroup
      of the n=58 analyzed cohort)
    time_post_onset: mean 60.0 months (SD 53.1)
    age_range: mean 62.0 years (SD 8.8)
    handedness: all right-handed
    language: monolingual native English speakers
  statistics:
    threshold: 'ROI-based mixed-effects regression with FDR correction; Time effect
      within naming-treatment group: β=0.016, SE=0.025, t(410.8)=0.653, p=0.655 (n.s.)'
    effect_size: β = 0.016 (essentially zero); ROI-level Time effect not significant
    ci_95: not_reported
    p_value: 0.655 (ROI-level Time effect, n.s. after FDR correction)
  confounders_controlled:
  - age, education, proportion of lesioned left-hemisphere tissue (covariates in mixed-effects
    regression)
  - Participant and ROI as random effects
  - natural history group (n=16) as no-treatment control
  confounders_not_controlled:
  - scanner differences across 3 sites (Siemens Skyra at BU; harmonized via phantom
    scans)
  - lower education and lower canonical sentence comprehension in naming group (residual
    cross-site heterogeneity)
  - control condition (reversed speech) not duration-matched to active condition
  region_definition:
    kind: atlas
    atlas: Harvard-Oxford
    description: ROI-based analysis on aggregated right-hemisphere language network
      homologues (RH IFGtri, IFGoper, frontal orbital cortex, insula, frontal operculum,
      three MTG parcellations, aSTG, pSTG, AG, pSMG, temporal pole) — null Time effect
      within the naming treatment group.
  imaging_details:
    field_strength: 3T
    acquisition:
      voxel_size_mm:
      - 1.72
      - 1.72
      - 3.0
      TR_ms: 2400
      TE_ms: 20
      sequence: gradient-echo T2*-weighted EPI
    task:
      name: Auditory story comprehension
      description: Block design auditory story comprehension vs reversed-speech control;
        24-s story blocks alternating with 18-s reversed-speech blocks.
      contrasts:
      - Stories > Control
      baseline: Time-reversed speech
    preprocessing_pipeline: AFNI 3dDespike + 3dvolreg motion correction; FD>0.5mm
      and DVARS>50 motion regressors; CompCor; SPM-DARTEL normalization to MNI152
      (2×2×2 mm); 6 mm FWHM smoothing; SPM12 first-level GLM with HRF + time and dispersion
      derivatives; enantiomorphic replacement (Nachev 2008)
    reference_space: MNI152
    atlases_used:
    - Harvard-Oxford
  replications: []
  contradictions: []
  author_limitations:
  - 'The discrepancy with f2 (voxel-level positive) is interpreted by the authors
    as: voxel-level findings may have been driven by some participants, or accounted
    for by age, education, or lesion size.'
  - The naturalistic story comprehension task may not be sensitive to single-word
    semantic processes targeted by the naming treatment — a different fMRI task (e.g.,
    overt naming) might yield different results.
  - Pre-treatment heterogeneities and scanner differences.
  evidence_quality: RCT
  strength: moderate
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Results 3.3.2.3.1.1 + Table 6 (pages 87–89); Discussion 4.3 (page
      94)
    confidence: high
    flags:
    - ROI-level null finding paired with f2 (voxel-level positive). The pair is the
      canonical example of the 'split into two findings' rule for cross-analysis disagreement
      (per EXTRACTION_SKILL §6b).
    - cohort overlaps with Gilmore et al. 2019 and Johnson et al. 2019 — same n=17
      anomic Boston University subgroup (trial NCT01927302); flag for downstream double-counting
      risk in interpret_overlap().
  source_passages:
  - section: Results 3.3.2.3.1.1
    page: 87
    supports: claim
    quote: Separate analyses conducted within each group (Table 6) revealed a signiﬁcant
      increase in activation from pre- to post-treatment (i.e., upregulation) only
      in the sentence production/comprehension and the spelling treatment groups,
      and no changes between time points for the naming treatment group or for the
      natural history (no treatment) group.
  - section: Discussion 4.3
    page: 94
    supports: claim
    quote: For the naming treatment group, although voxel-based analyses showed activation
      of right anterior temporal regions at post- (and not pre-) treatment, the lack
      of signiﬁcant upregulation on the ROI-based analyses suggests that the ﬁndings
      of the voxel-based analyses may have been either driven by some participants,
      or accounted for by age, education or lesion size.
  - section: Discussion 4.3
    page: 94
    supports: limitation
    quote: Results obtained from this group, which were not in line with our predictions,
      suggest that language interventions targeting lexical-semantics may not yield
      robust, group-level upregulation of activation on a naturalistic task that engages
      processes beyond single-word comprehension. This also indicates that the task
      employed as primary measure of neural plasticity may have a substantial effect
      on the outcome and should be carefully chosen.
  - section: Table 6 — naming group
    page: 88
    supports: statistics
    quote: Time (Post- vs. Pre-treatment)  .016  .025  410.8  .653  .655
  - section: Methods 2.4.2.4 — ROI analyses
    page: 87
    supports: confounders
    quote: Age, education and lesion size (i.e., the proportion of lesioned tissue
      in each left-hemisphere ROI) were entered as covariates, to ensure that activation
      changes between time points, as well as the Group*Time interaction, were not
      driven by group differences in demographic or lesion variables.
  - section: Methods 2.1 — Participants
    page: 78
    supports: sample
    quote: '70 met the inclusion criteria for the study: (1) presence of a single
      left-hemisphere stroke at least 12 months prior entering the study and affecting
      at least .1% of the cortical surface in the left hemisphere'
source: agent_draft
last_reviewed: null
notes: "First-extraction draft from Barbieri et al. 2023. Typicality-based\nSemantic\
  \ Feature Analysis is a naming intervention for anomic\naphasia in which typical\
  \ (e.g., pigeon) or atypical (e.g., penguin)\nexemplars of a semantic category (e.g.,\
  \ birds) are trained through\ncategory sorting, feature verification, and feature\
  \ review. Two\nfindings recorded:\n\n- f1 (behavioural efficacy): naming treatment\
  \ significantly\n  improved trained-item naming accuracy compared to natural history\n\
  \  control (p<.0001, β=1.447 z-scored).\n- f2 (mixed neural evidence): voxel-level\
  \ analyses showed RH\n  anterior-temporal activation post-treatment, but ROI-level\n\
  \  analyses with covariates showed NO significant upregulation —\n  interpreted\
  \ by the authors as evidence that lexical-semantic\n  treatment may not produce\
  \ robust group-level reorganization on a\n  naturalistic story comprehension task\
  \ (and that the choice of\n  fMRI task substantially affects the outcome).\n\nThis\
  \ draft anchors on therapy because the paper's claims are about\ntreatment effects.\
  \ The naming-treatment group is the n=17 BU\nsubgroup of the n=58 analyzed cohort.\n\
  \nCaveat for downstream interpretation: the voxel-level positive\nfinding is a real\
  \ (FWE-corrected) result. The ROI-level null is\nthe more conservative test (controlling\
  \ for covariates and\nindividual variability). The two findings are not contradictory\
  \ in\na strict sense — they reflect different sensitivities — but they\njointly\
  \ produce a `mixed` direction at the level of the therapy claim."
reviewer: auto-reviewer
reviewed_on: '2026-05-05'
---
# Typicality-based Semantic Feature Analysis (SFA)

## Therapy description

Typicality-based SFA is an extension of Boyle (2004)'s classical
Semantic Feature Analysis treatment in which the manipulation of
typical vs. atypical category exemplars is used to drive
generalization. Each participant is trained on half of the items in
two combinations of semantic category (chosen from birds, clothing,
furniture, vegetables, fruits) and typicality condition (typical or
atypical: e.g., typical birds + atypical furniture). The other half
of items is used to assess generalization. Treatment steps include
category sorting, auditory and written feature verification, and
feature review.

In Barbieri et al. 2023, typicality-based SFA was administered on
the same fixed schedule as the other treatments (12 weeks,
2 sessions/week, 1.5 h/session).

## Notes for next extraction round

  - Add `anomia` as an impairment entry (currently only referenced
    as a target ID; the Yourganov 2015 extraction has a draft for
    `anomic_aphasia` but that's a syndrome label, not the same
    construct).
  - The mixed voxel-level vs. ROI-level evidence is an important
    pattern that recurs in the spelling treatment finding too — the
    KB schema doesn't have a clean way to mark `direction: mixed`
    and explain why; the finding's `claim` field carries that nuance.
  - For region-side mirroring, consider whether to capture the
    voxel-level RH aMTG / temporal pole peaks as separate
    `recruitment` findings rather than `causal` (since the activation
    is treatment-induced rather than damage-induced).
