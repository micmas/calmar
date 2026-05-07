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
short_description: An impairment-based naming intervention for anomic aphasia in which typical (e.g.,
  pigeon) or atypical (e.g., penguin) exemplars of a semantic category (e.g., birds) are trained through
  category sorting, auditory and written feature verification, and feature review. A typicality-manipulation
  variant of classical Semantic Feature Analysis (Boyle 2004).
targets_impairments:
- anomia
- anomic_aphasia
- form_to_meaning
- semantics
- wernickes_aphasia
dosage: 12 weeks, 2 sessions/week, 1.5 h/session (Barbieri et al. 2023; Johnson et al. 2019; Gilmore et
  al. 2019 protocol). Each participant trained on half of the items (n=36) in two combinations of semantic
  category × typicality.
atf_id: 2
atf_evidence_level: level_II
evidence_level: level_II
atf_aliases:
  - SFA
  - Semantic Feature Analysis
  - BOX lexical-semantic therapy
icf_domain:
  - body_function
  - activity
tidier:
  brief_name: Typicality-ordered Semantic Feature Analysis (Typicality-SFA)
  rationale: |-
    Semantic feature generation strengthens the lexical-semantic network by activating
        multiple feature nodes associated with a target word, facilitating convergent
        lexical access. Typicality ordering exploits preserved prototype structure:
        training highly typical exemplars first establishes robust feature representations
        that generalise to less typical items.
  materials: |-
    SFA feature chart (6 categories: is, does, has, properties, category, location);
        confrontation naming picture stimuli; typicality-rated word list (normed ratings);
        Kendall 2019 / Barbieri 2023 protocol materials.
  procedures: |-
    Patient shown target picture; prompted to generate semantic features across 6 chart
        categories. Features recorded on chart by patient/clinician. Naming attempt
        follows feature generation. Corrective feedback provided. Item ordering follows
        typicality ratings (most-typical exemplar trained before less-typical within each
        semantic category).
  who_provides: |-
    Speech-language pathologist (individual sessions); computer-delivered versions
        validated.
  delivery_mode: face_to_face or telehealth
  setting: Outpatient clinic or university aphasia lab.
  dosage: |-
    Kendall 2019 (standard SFA): 2 sessions/week × 10 weeks. Barbieri 2023 typicality arm:
        2 sessions/week × 8 weeks; ~60 min/session.
  tailoring: |-
    Item set tailored to patient's lexical gap profile from standardised naming test.
        Typicality ordering within each semantic category individualised to patient's
        error pattern. Feature chart prompt level adjusted to patient cognitive-linguistic
        capacity.
  modifications: |-
    Standard SFA (Boyle & Coelho 1995) does not use typicality ordering. Computer-based
        SFA (Fink et al.) validated for self-administration. BOX lexical-semantic therapy
        is a related procedure using semantic feature boxes.
  fidelity_planned: |-
    Per-session probe lists (trained + untrained items) administered to track
        generalisation. Clinician session logs; criterion-based item progression.
  fidelity_actual: |-
    Barbieri 2023: completion rates and probe-score trajectories reported per arm. Kendall
        2019: treatment fidelity checked by independent reviewer for 20% of sessions.
  confidence: medium
  flags:
    - Barbieri 2023 typicality subgroup is a naming subgroup within a larger RCT — not a
        standalone RCT of Typicality-SFA. Evidence level reflects this.
    - Kendall 2019 (standard SFA RCT) not formally extracted.
rtss_ingredients:
  - semantic_feature_generation
  - typicality_ordering
findings:
- author_limitations:
  - Pre-treatment heterogeneities across treatment groups (different impairment profiles, different recruitment
    sites).
  - Long-term maintenance not assessed.
  - Generalization to untrained items partially assessed (half of category items held out) but not the
    focus of this paper.
  citation: '@Barbieri2023'
  claim: Twelve weeks of typicality-based semantic feature analysis treatment significantly improves naming
    accuracy on trained items in chronic anomic aphasia compared to a no-treatment natural history control
    group.
  confounders_controlled:
  - age, education, proportion of lesioned left-hemisphere tissue (covariates)
  - natural history group (n=16) used as no-treatment control
  - groups matched on months post-onset, gender, handedness, WAB-AQ, lesion size
  confounders_not_controlled:
  - PI not blinded to treatment allocation
  - naming treatment group had lower education than sentence treatment group (t=2.124, p=0.038)
  - naming group had lower canonical sentence comprehension than spelling and natural history groups (residual
    heterogeneity from cross-site recruitment)
  contradictions: []
  design: RCT
  direction: likely
  evidence_quality: RCT
  id: f1
  imaging: none
  imaging_details:
    atlases_used: []
    reference_space: not_reported
  method: clinical_RCT
  provenance:
    confidence: high
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    flags:
    - behavioural-only finding.
    - cohort overlaps with Gilmore et al. 2019 and Johnson et al. 2019 — same n=17 anomic Boston University
      subgroup (trial NCT01927302); flag for downstream double-counting risk in interpret_overlap().
    paper_section: Results 3.1 + Table 2 (page 83); Methods 2.2 (page 80); Methods 2.3.1 (page 80)
  region_definition:
    description: Behavioral-only treatment efficacy finding — no specific brain region; treatment efficacy
      measured as the average change in proportion of correctly named items in the two trained category
      × typicality combinations.
    kind: not_reported
  relationship: responder
  replications:
  - '@Boyle2004'
  sample:
    age_range: mean 62.0 years (SD 8.8)
    exclusion_criteria: exclusively subcortical lesions; non-monolingual; developmental/psychiatric/other
      neurological history; MRI contraindications.
    handedness: all right-handed
    inclusion_criteria: age 35–80; education ≥high-school; WAB-AQ 45–95; anomia per a study-specific naming
      battery including natural and artificial objects from four semantic categories.
    language: monolingual native English speakers
    n: 17
    population: chronic stroke-induced anomic aphasia (single left-hemisphere stroke ≥12 months post-onset;
      subgroup of n=58 analyzed cohort, recruited at Boston University)
    recruitment: Aphasia Research Lab at Boston University; randomized to treatment vs. natural history
      at the site by a staff member other than the assessor.
    time_post_onset: mean 60.0 months (SD 53.1)
  source_passages:
  - page: 80
    quote: At Boston University, the participants treated for anomia underwent a typicality-based semantic
      feature analysis treatment in which typical (e.g., pigeon) or atypical (e.g., penguin) exemplars
      of a certain semantic category (e.g., birds) were trained.
    section: Methods 2.2 — Treatment
    supports: method
  - page: 80
    quote: Treatment entailed several steps, including category sorting, auditory and written feature
      veriﬁcation, and feature review.
    section: Methods 2.2 — Treatment
    supports: method
  - page: 78
    quote: '70 met the inclusion criteria for the study: (1) presence of a single left-hemisphere stroke
      at least 12 months prior entering the study and affecting at least .1% of the cortical surface in
      the left hemisphere'
    section: Methods 2.1 — Participants
    supports: sample
  - page: 78
    quote: At Boston University, participants were selected for anomia based on a study-speciﬁc naming
      battery including natural and artiﬁcial objects that belonged to four different semantic categories
    section: Methods 2.1 — Participants
    supports: sample
  - page: 82
    quote: Post-hoc analyses revealed a signiﬁcant effect of Time, in the direction of greater accuracy
      post- than pre-testing, in all the three treatment groups (sentence production/comprehension, naming,
      spelling, all ps < .0001, Fig. 1), whereas no change in accuracy from pre-to post-testing was found
      in the natural history group.
    section: Results 3.1 — Treatment effects
    supports: claim
  - page: 83
    quote: Time in Naming vs. Time in NH Group  1.308  .318  54  4.115  .0001
    section: Table 2 — Treatment effects
    supports: statistics
  - page: 81
    quote: Mixed-effects regressions were then run using Time (pre-, post-testing) and Group (sentence
      processing treatment, naming treatment, spelling treatment, and natural history), as well as all
      their interaction, as ﬁxed effects, and Participant as the only random effect.
    section: Methods 2.4.1 — Treatment effects
    supports: confounders
  - page: 96
    quote: participants were recruited from different research centers because they met criteria for different
      language deﬁcits, which resulted in pre-treatment heterogeneities across groups in terms of language
      proﬁles.
    section: Limitations
    supports: limitation
  statistics:
    ci_95: not_reported
    cluster_extent: null
    effect_size: β = 1.447 (z-scored accuracy units), SE 0.178, t(16) = 8.121 (Time post- vs. pre-treatment
      within naming group); β = 1.308, SE 0.318, t(54) = 4.115 for the Time × Group interaction (naming
      treatment vs. natural history)
    p_value: <0.0001 (within-group); 0.0001 (Time × Group interaction)
    threshold: mixed-effects regression with FDR correction; p<0.0001 for the Time effect within the naming
      treatment group
  strength: strong
  target: anomia
  target_kind: impairment
- author_limitations:
  - Voxel-based finding may have been driven by some participants or accounted for by age/education/lesion
    size — see f3 for the corresponding ROI-level result with covariates.
  - Pre-treatment heterogeneities and scanner differences.
  citation: '@Barbieri2023'
  claim: Typicality-based semantic feature analysis treatment for anomia produces post-treatment voxel-level
    activation in right anterior temporal regions (aMTG, aSTG, temporal pole, pMTG) on a naturalistic
    auditory story comprehension fMRI task — pre-treatment activation in these regions was not significant;
    post-treatment is.
  confounders_controlled:
  - natural history group (n=16) as no-treatment control
  confounders_not_controlled:
  - age, education, lesion size — entered as covariates ONLY in the ROI-based analysis (f3), not in this
    voxel-based one (this is the source of the voxel/ROI disagreement)
  - scanner differences across 3 sites (Siemens Skyra at BU; harmonized via phantom scans)
  - control condition (reversed speech) not duration-matched to active condition
  contradictions: []
  design: RCT
  direction: likely
  evidence_quality: RCT
  id: f2
  imaging: fMRI
  imaging_details:
    acquisition:
      TE_ms: 20
      TR_ms: 2400
      sequence: gradient-echo T2*-weighted EPI
      voxel_size_mm:
      - 1.72
      - 1.72
      - 3.0
    atlases_used:
    - Harvard-Oxford
    coordinates_reported:
    - mni:
      - 64
      - -4
      - -18
      region: right anterior MTG (extending aSTG, pMTG)
    - mni:
      - 54
      - 16
      - -18
      region: right temporal pole
    field_strength: 3T
    modalities:
    - TE_ms: 2.91
      TR_ms: 2300
      modality: T1
      sequence: 3D T1-weighted MPRAGE
      voxel_size_mm:
      - 1.0
      - 1.0
      - 1.0
    - TE_ms: 20
      TR_ms: 2400
      modality: fMRI
      sequence: gradient-echo T2*-weighted EPI
      volumes: 192
      voxel_size_mm:
      - 1.72
      - 1.72
      - 3.0
    preprocessing_pipeline: AFNI 3dDespike + 3dvolreg motion correction; FD>0.5mm and DVARS>50 motion
      regressors; CompCor; SPM-DARTEL normalization to MNI152 (2×2×2 mm); 6 mm FWHM smoothing; SPM12 first-level
      GLM with HRF + time and dispersion derivatives; enantiomorphic replacement of left-hemisphere lesion
      (Nachev 2008)
    reference_space: MNI152
    task:
      baseline: Time-reversed speech
      contrasts:
      - Stories > Control
      description: Block design auditory story comprehension vs reversed-speech control; 24-s story blocks
        alternating with 18-s reversed-speech blocks.
      name: Auditory story comprehension
  method: fMRI_activation
  provenance:
    confidence: high
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    flags:
    - 'Voxel-level positive finding; the corresponding ROI-level analysis with covariates (f3) found a
      null effect — the two findings are split per schema convention rather than coded as `direction:
      mixed`.'
    - cohort overlaps with Gilmore et al. 2019 and Johnson et al. 2019 — same n=17 anomic Boston University
      subgroup (trial NCT01927302); flag for downstream double-counting risk in interpret_overlap().
    paper_section: Results 3.3.2.2 + Table 5 (pages 86–87)
  region_definition:
    atlas: Harvard-Oxford
    description: 'Voxel-based clusters: right aMTG (extending aSTG and pMTG; peak MNI [64,-4,-18], k=170
      voxels) and right temporal pole (peak MNI [54,16,-18], k=87 voxels). The voxel-based analysis was
      constrained to ROIs that were active in healthy participants on the same task or to their right-hemisphere
      homologues.'
    kind: atlas
  relationship: treatment_response
  replications: []
  sample:
    age_range: mean 62.0 years (SD 8.8)
    handedness: all right-handed
    language: monolingual native English speakers
    n: 17
    population: chronic stroke-induced anomic aphasia (Boston University subgroup of the n=58 analyzed
      cohort)
    time_post_onset: mean 60.0 months (SD 53.1)
  source_passages:
  - page: 87
    quote: In both the naming and spelling treatment groups, post-treatment activation was limited to
      right temporal regions, including the aSTG and temporal pole (for both groups), and the aMTG and
      pMTG (for the naming treatment group only).
    section: Results 3.3.2.2
    supports: claim
  - page: 81
    quote: Structural and functional MR images were collected using 3T scanners (Siemens Trio at Northwestern
      University, Siemens Skyra at Boston University, and Philips Intera at Johns Hopkins University)
    section: Methods 2.3.2.2 — Data acquisition
    supports: imaging_details
  - page: 78
    quote: '70 met the inclusion criteria for the study: (1) presence of a single left-hemisphere stroke
      at least 12 months prior entering the study and affecting at least .1% of the cortical surface in
      the left hemisphere'
    section: Methods 2.1 — Participants
    supports: sample
  - page: 81
    quote: T-maps were obtained by applying a p < .001 threshold at the voxel-level. Cluster-level correction
      was carried out using the family-wise error (FWE) correction provided by SPM12, at a threshold of
      p < .05
    section: Methods 2.4.2.3 — Voxel-level analyses
    supports: method
  - page: 87
    quote: Naming treatment (k  87)
    section: Table 5 — naming treatment post-treatment
    supports: statistics
  statistics:
    ci_95: not_reported
    cluster_extent: 257
    effect_size: 'Peak Story>Control activation post-treatment: T=5.590 (right aMTG, k=170, MNI [64,-4,-18]),
      T=5.912 (right temporal pole, k=87, MNI [54,16,-18]).'
    p_value: <0.001 voxel-level, FWE-corrected p<0.05 cluster-level
    threshold: voxel-level p<0.001, FWE-corrected p<0.05 cluster-level (k≥87 voxels for naming-treatment
      group post-treatment)
  strength: moderate
  target: right_anterior_middle_temporal_gyrus
  target_kind: region
- author_limitations:
  - 'The discrepancy with f2 (voxel-level positive) is interpreted by the authors as: voxel-level findings
    may have been driven by some participants, or accounted for by age, education, or lesion size.'
  - The naturalistic story comprehension task may not be sensitive to single-word semantic processes targeted
    by the naming treatment — a different fMRI task (e.g., overt naming) might yield different results.
  - Pre-treatment heterogeneities and scanner differences.
  citation: '@Barbieri2023'
  claim: Typicality-based semantic feature analysis treatment for anomia does NOT produce a significant
    ROI-level upregulation of activation in right-hemisphere language network homologues during a naturalistic
    auditory story comprehension fMRI task, after controlling for age, education, and lesion size — i.e.,
    the voxel-level activation in f2 is not robust once individual variability and demographic covariates
    are accounted for.
  confounders_controlled:
  - age, education, proportion of lesioned left-hemisphere tissue (covariates in mixed-effects regression)
  - Participant and ROI as random effects
  - natural history group (n=16) as no-treatment control
  confounders_not_controlled:
  - scanner differences across 3 sites (Siemens Skyra at BU; harmonized via phantom scans)
  - lower education and lower canonical sentence comprehension in naming group (residual cross-site heterogeneity)
  - control condition (reversed speech) not duration-matched to active condition
  contradictions: []
  design: RCT
  direction: no_effect
  evidence_quality: RCT
  id: f3
  imaging: fMRI
  imaging_details:
    acquisition:
      TE_ms: 20
      TR_ms: 2400
      sequence: gradient-echo T2*-weighted EPI
      voxel_size_mm:
      - 1.72
      - 1.72
      - 3.0
    atlases_used:
    - Harvard-Oxford
    field_strength: 3T
    preprocessing_pipeline: AFNI 3dDespike + 3dvolreg motion correction; FD>0.5mm and DVARS>50 motion
      regressors; CompCor; SPM-DARTEL normalization to MNI152 (2×2×2 mm); 6 mm FWHM smoothing; SPM12 first-level
      GLM with HRF + time and dispersion derivatives; enantiomorphic replacement (Nachev 2008)
    reference_space: MNI152
    task:
      baseline: Time-reversed speech
      contrasts:
      - Stories > Control
      description: Block design auditory story comprehension vs reversed-speech control; 24-s story blocks
        alternating with 18-s reversed-speech blocks.
      name: Auditory story comprehension
  method: fMRI_activation
  provenance:
    confidence: high
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    flags:
    - ROI-level null finding paired with f2 (voxel-level positive). The pair is the canonical example
      of the 'split into two findings' rule for cross-analysis disagreement (per EXTRACTION_SKILL §6b).
    - cohort overlaps with Gilmore et al. 2019 and Johnson et al. 2019 — same n=17 anomic Boston University
      subgroup (trial NCT01927302); flag for downstream double-counting risk in interpret_overlap().
    paper_section: Results 3.3.2.3.1.1 + Table 6 (pages 87–89); Discussion 4.3 (page 94)
  region_definition:
    atlas: Harvard-Oxford
    description: ROI-based analysis on aggregated right-hemisphere language network homologues (RH IFGtri,
      IFGoper, frontal orbital cortex, insula, frontal operculum, three MTG parcellations, aSTG, pSTG,
      AG, pSMG, temporal pole) — null Time effect within the naming treatment group.
    kind: atlas
  relationship: treatment_response
  replications: []
  sample:
    age_range: mean 62.0 years (SD 8.8)
    handedness: all right-handed
    language: monolingual native English speakers
    n: 17
    population: chronic stroke-induced anomic aphasia (Boston University subgroup of the n=58 analyzed
      cohort)
    time_post_onset: mean 60.0 months (SD 53.1)
  source_passages:
  - page: 87
    quote: Separate analyses conducted within each group (Table 6) revealed a signiﬁcant increase in activation
      from pre- to post-treatment (i.e., upregulation) only in the sentence production/comprehension and
      the spelling treatment groups, and no changes between time points for the naming treatment group
      or for the natural history (no treatment) group.
    section: Results 3.3.2.3.1.1
    supports: claim
  - page: 94
    quote: For the naming treatment group, although voxel-based analyses showed activation of right anterior
      temporal regions at post- (and not pre-) treatment, the lack of signiﬁcant upregulation on the ROI-based
      analyses suggests that the ﬁndings of the voxel-based analyses may have been either driven by some
      participants, or accounted for by age, education or lesion size.
    section: Discussion 4.3
    supports: claim
  - page: 94
    quote: Results obtained from this group, which were not in line with our predictions, suggest that
      language interventions targeting lexical-semantics may not yield robust, group-level upregulation
      of activation on a naturalistic task that engages processes beyond single-word comprehension. This
      also indicates that the task employed as primary measure of neural plasticity may have a substantial
      effect on the outcome and should be carefully chosen.
    section: Discussion 4.3
    supports: limitation
  - page: 88
    quote: Time (Post- vs. Pre-treatment)  .016  .025  410.8  .653  .655
    section: Table 6 — naming group
    supports: statistics
  - page: 87
    quote: Age, education and lesion size (i.e., the proportion of lesioned tissue in each left-hemisphere
      ROI) were entered as covariates, to ensure that activation changes between time points, as well
      as the Group*Time interaction, were not driven by group differences in demographic or lesion variables.
    section: Methods 2.4.2.4 — ROI analyses
    supports: confounders
  - page: 78
    quote: '70 met the inclusion criteria for the study: (1) presence of a single left-hemisphere stroke
      at least 12 months prior entering the study and affecting at least .1% of the cortical surface in
      the left hemisphere'
    section: Methods 2.1 — Participants
    supports: sample
  statistics:
    ci_95: not_reported
    effect_size: β = 0.016 (essentially zero); ROI-level Time effect not significant
    p_value: 0.655 (ROI-level Time effect, n.s. after FDR correction)
    threshold: 'ROI-based mixed-effects regression with FDR correction; Time effect within naming-treatment
      group: β=0.016, SE=0.025, t(410.8)=0.653, p=0.655 (n.s.)'
  strength: moderate
  target: right_anterior_middle_temporal_gyrus
  target_kind: region
- author_limitations:
  - Pre-treatment heterogeneities across treatment groups (different impairment profiles, different recruitment
    sites).
  - Long-term maintenance not assessed.
  - Generalization to untrained items partially assessed (half of category items held out) but not the
    focus of this paper.
  citation: '@Barbieri2023'
  claim: Twelve weeks of typicality-based semantic feature analysis treatment significantly improves naming
    accuracy on trained items in chronic anomic aphasia compared to a no-treatment natural history control
    group.
  confounders_controlled:
  - age, education, proportion of lesioned left-hemisphere tissue (covariates)
  - natural history group (n=16) used as no-treatment control
  - groups matched on months post-onset, gender, handedness, WAB-AQ, lesion size
  confounders_not_controlled:
  - PI not blinded to treatment allocation
  - naming treatment group had lower education than sentence treatment group (t=2.124, p=0.038)
  - naming group had lower canonical sentence comprehension than spelling and natural history groups (residual
    heterogeneity from cross-site recruitment)
  contradictions: []
  design: RCT
  direction: likely_responder
  evidence_quality: RCT
  id: f4
  imaging: none
  imaging_details:
    atlases_used: []
    reference_space: not_reported
  method: clinical_RCT
  provenance:
    confidence: high
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    flags:
    - behavioural-only finding.
    - cohort overlaps with Gilmore et al. 2019 and Johnson et al. 2019 — same n=17 anomic Boston University
      subgroup (trial NCT01927302); flag for downstream double-counting risk in interpret_overlap().
    paper_section: Results 3.1 + Table 2 (page 83); Methods 2.2 (page 80); Methods 2.3.1 (page 80)
  region_definition:
    description: Behavioral-only treatment efficacy finding — no specific brain region; treatment efficacy
      measured as the average change in proportion of correctly named items in the two trained category
      × typicality combinations.
    kind: not_reported
  relationship: responder
  replications:
  - '@Boyle2004'
  sample:
    age_range: mean 62.0 years (SD 8.8)
    exclusion_criteria: exclusively subcortical lesions; non-monolingual; developmental/psychiatric/other
      neurological history; MRI contraindications.
    handedness: all right-handed
    inclusion_criteria: age 35–80; education ≥high-school; WAB-AQ 45–95; anomia per a study-specific naming
      battery including natural and artificial objects from four semantic categories.
    language: monolingual native English speakers
    n: 17
    population: chronic stroke-induced anomic aphasia (single left-hemisphere stroke ≥12 months post-onset;
      subgroup of n=58 analyzed cohort, recruited at Boston University)
    recruitment: Aphasia Research Lab at Boston University; randomized to treatment vs. natural history
      at the site by a staff member other than the assessor.
    time_post_onset: mean 60.0 months (SD 53.1)
  source_passages:
  - page: 80
    quote: At Boston University, the participants treated for anomia underwent a typicality-based semantic
      feature analysis treatment in which typical (e.g., pigeon) or atypical (e.g., penguin) exemplars
      of a certain semantic category (e.g., birds) were trained.
    section: Methods 2.2 — Treatment
    supports: method
  - page: 80
    quote: Treatment entailed several steps, including category sorting, auditory and written feature
      veriﬁcation, and feature review.
    section: Methods 2.2 — Treatment
    supports: method
  - page: 78
    quote: '70 met the inclusion criteria for the study: (1) presence of a single left-hemisphere stroke
      at least 12 months prior entering the study and affecting at least .1% of the cortical surface in
      the left hemisphere'
    section: Methods 2.1 — Participants
    supports: sample
  - page: 78
    quote: At Boston University, participants were selected for anomia based on a study-speciﬁc naming
      battery including natural and artiﬁcial objects that belonged to four different semantic categories
    section: Methods 2.1 — Participants
    supports: sample
  - page: 82
    quote: Post-hoc analyses revealed a signiﬁcant effect of Time, in the direction of greater accuracy
      post- than pre-testing, in all the three treatment groups (sentence production/comprehension, naming,
      spelling, all ps < .0001, Fig. 1), whereas no change in accuracy from pre-to post-testing was found
      in the natural history group.
    section: Results 3.1 — Treatment effects
    supports: claim
  - page: 83
    quote: Time in Naming vs. Time in NH Group  1.308  .318  54  4.115  .0001
    section: Table 2 — Treatment effects
    supports: statistics
  - page: 81
    quote: Mixed-effects regressions were then run using Time (pre-, post-testing) and Group (sentence
      processing treatment, naming treatment, spelling treatment, and natural history), as well as all
      their interaction, as ﬁxed effects, and Participant as the only random effect.
    section: Methods 2.4.1 — Treatment effects
    supports: confounders
  - page: 96
    quote: participants were recruited from different research centers because they met criteria for different
      language deﬁcits, which resulted in pre-treatment heterogeneities across groups in terms of language
      proﬁles.
    section: Limitations
    supports: limitation
  statistics:
    ci_95: not_reported
    cluster_extent: null
    effect_size: β = 1.447 (z-scored accuracy units), SE 0.178, t(16) = 8.121 (Time post- vs. pre-treatment
      within naming group); β = 1.308, SE 0.318, t(54) = 4.115 for the Time × Group interaction (naming
      treatment vs. natural history)
    p_value: <0.0001 (within-group); 0.0001 (Time × Group interaction)
    threshold: mixed-effects regression with FDR correction; p<0.0001 for the Time effect within the naming
      treatment group
  strength: strong
  target: anomia
  target_kind: impairment
- author_limitations:
  - Voxel-based finding may have been driven by some participants or accounted for by age/education/lesion
    size — see f3 for the corresponding ROI-level result with covariates.
  - Pre-treatment heterogeneities and scanner differences.
  citation: '@Barbieri2023'
  claim: Typicality-based semantic feature analysis treatment for anomia produces post-treatment voxel-level
    activation in right anterior temporal regions (aMTG, aSTG, temporal pole, pMTG) on a naturalistic
    auditory story comprehension fMRI task — pre-treatment activation in these regions was not significant;
    post-treatment is.
  confounders_controlled:
  - natural history group (n=16) as no-treatment control
  confounders_not_controlled:
  - age, education, lesion size — entered as covariates ONLY in the ROI-based analysis (f3), not in this
    voxel-based one (this is the source of the voxel/ROI disagreement)
  - scanner differences across 3 sites (Siemens Skyra at BU; harmonized via phantom scans)
  - control condition (reversed speech) not duration-matched to active condition
  contradictions: []
  design: RCT
  direction: likely
  evidence_quality: RCT
  id: f5
  imaging: fMRI
  imaging_details:
    acquisition:
      TE_ms: 20
      TR_ms: 2400
      sequence: gradient-echo T2*-weighted EPI
      voxel_size_mm:
      - 1.72
      - 1.72
      - 3.0
    atlases_used:
    - Harvard-Oxford
    coordinates_reported:
    - mni:
      - 64
      - -4
      - -18
      region: right anterior MTG (extending aSTG, pMTG)
    - mni:
      - 54
      - 16
      - -18
      region: right temporal pole
    field_strength: 3T
    modalities:
    - TE_ms: 2.91
      TR_ms: 2300
      modality: T1
      sequence: 3D T1-weighted MPRAGE
      voxel_size_mm:
      - 1.0
      - 1.0
      - 1.0
    - TE_ms: 20
      TR_ms: 2400
      modality: fMRI
      sequence: gradient-echo T2*-weighted EPI
      volumes: 192
      voxel_size_mm:
      - 1.72
      - 1.72
      - 3.0
    preprocessing_pipeline: AFNI 3dDespike + 3dvolreg motion correction; FD>0.5mm and DVARS>50 motion
      regressors; CompCor; SPM-DARTEL normalization to MNI152 (2×2×2 mm); 6 mm FWHM smoothing; SPM12 first-level
      GLM with HRF + time and dispersion derivatives; enantiomorphic replacement of left-hemisphere lesion
      (Nachev 2008)
    reference_space: MNI152
    task:
      baseline: Time-reversed speech
      contrasts:
      - Stories > Control
      description: Block design auditory story comprehension vs reversed-speech control; 24-s story blocks
        alternating with 18-s reversed-speech blocks.
      name: Auditory story comprehension
  method: fMRI_activation
  provenance:
    confidence: high
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    flags:
    - 'Voxel-level positive finding; the corresponding ROI-level analysis with covariates (f3) found a
      null effect — the two findings are split per schema convention rather than coded as `direction:
      mixed`.'
    - cohort overlaps with Gilmore et al. 2019 and Johnson et al. 2019 — same n=17 anomic Boston University
      subgroup (trial NCT01927302); flag for downstream double-counting risk in interpret_overlap().
    paper_section: Results 3.3.2.2 + Table 5 (pages 86–87)
  region_definition:
    atlas: Harvard-Oxford
    description: 'Voxel-based clusters: right aMTG (extending aSTG and pMTG; peak MNI [64,-4,-18], k=170
      voxels) and right temporal pole (peak MNI [54,16,-18], k=87 voxels). The voxel-based analysis was
      constrained to ROIs that were active in healthy participants on the same task or to their right-hemisphere
      homologues.'
    kind: atlas
  relationship: treatment_response
  replications: []
  sample:
    age_range: mean 62.0 years (SD 8.8)
    handedness: all right-handed
    language: monolingual native English speakers
    n: 17
    population: chronic stroke-induced anomic aphasia (Boston University subgroup of the n=58 analyzed
      cohort)
    time_post_onset: mean 60.0 months (SD 53.1)
  source_passages:
  - page: 87
    quote: In both the naming and spelling treatment groups, post-treatment activation was limited to
      right temporal regions, including the aSTG and temporal pole (for both groups), and the aMTG and
      pMTG (for the naming treatment group only).
    section: Results 3.3.2.2
    supports: claim
  - page: 81
    quote: Structural and functional MR images were collected using 3T scanners (Siemens Trio at Northwestern
      University, Siemens Skyra at Boston University, and Philips Intera at Johns Hopkins University)
    section: Methods 2.3.2.2 — Data acquisition
    supports: imaging_details
  - page: 78
    quote: '70 met the inclusion criteria for the study: (1) presence of a single left-hemisphere stroke
      at least 12 months prior entering the study and affecting at least .1% of the cortical surface in
      the left hemisphere'
    section: Methods 2.1 — Participants
    supports: sample
  - page: 81
    quote: T-maps were obtained by applying a p < .001 threshold at the voxel-level. Cluster-level correction
      was carried out using the family-wise error (FWE) correction provided by SPM12, at a threshold of
      p < .05
    section: Methods 2.4.2.3 — Voxel-level analyses
    supports: method
  - page: 87
    quote: Naming treatment (k  87)
    section: Table 5 — naming treatment post-treatment
    supports: statistics
  statistics:
    ci_95: not_reported
    cluster_extent: 257
    effect_size: 'Peak Story>Control activation post-treatment: T=5.590 (right aMTG, k=170, MNI [64,-4,-18]),
      T=5.912 (right temporal pole, k=87, MNI [54,16,-18]).'
    p_value: <0.001 voxel-level, FWE-corrected p<0.05 cluster-level
    threshold: voxel-level p<0.001, FWE-corrected p<0.05 cluster-level (k≥87 voxels for naming-treatment
      group post-treatment)
  strength: moderate
  target: right_anterior_middle_temporal_gyrus
  target_kind: region
- author_limitations:
  - 'The discrepancy with f2 (voxel-level positive) is interpreted by the authors as: voxel-level findings
    may have been driven by some participants, or accounted for by age, education, or lesion size.'
  - The naturalistic story comprehension task may not be sensitive to single-word semantic processes targeted
    by the naming treatment — a different fMRI task (e.g., overt naming) might yield different results.
  - Pre-treatment heterogeneities and scanner differences.
  citation: '@Barbieri2023'
  claim: Typicality-based semantic feature analysis treatment for anomia does NOT produce a significant
    ROI-level upregulation of activation in right-hemisphere language network homologues during a naturalistic
    auditory story comprehension fMRI task, after controlling for age, education, and lesion size — i.e.,
    the voxel-level activation in f2 is not robust once individual variability and demographic covariates
    are accounted for.
  confounders_controlled:
  - age, education, proportion of lesioned left-hemisphere tissue (covariates in mixed-effects regression)
  - Participant and ROI as random effects
  - natural history group (n=16) as no-treatment control
  confounders_not_controlled:
  - scanner differences across 3 sites (Siemens Skyra at BU; harmonized via phantom scans)
  - lower education and lower canonical sentence comprehension in naming group (residual cross-site heterogeneity)
  - control condition (reversed speech) not duration-matched to active condition
  contradictions: []
  design: RCT
  direction: no_effect
  evidence_quality: RCT
  id: f6
  imaging: fMRI
  imaging_details:
    acquisition:
      TE_ms: 20
      TR_ms: 2400
      sequence: gradient-echo T2*-weighted EPI
      voxel_size_mm:
      - 1.72
      - 1.72
      - 3.0
    atlases_used:
    - Harvard-Oxford
    field_strength: 3T
    preprocessing_pipeline: AFNI 3dDespike + 3dvolreg motion correction; FD>0.5mm and DVARS>50 motion
      regressors; CompCor; SPM-DARTEL normalization to MNI152 (2×2×2 mm); 6 mm FWHM smoothing; SPM12 first-level
      GLM with HRF + time and dispersion derivatives; enantiomorphic replacement (Nachev 2008)
    reference_space: MNI152
    task:
      baseline: Time-reversed speech
      contrasts:
      - Stories > Control
      description: Block design auditory story comprehension vs reversed-speech control; 24-s story blocks
        alternating with 18-s reversed-speech blocks.
      name: Auditory story comprehension
  method: fMRI_activation
  provenance:
    confidence: high
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    flags:
    - ROI-level null finding paired with f2 (voxel-level positive). The pair is the canonical example
      of the 'split into two findings' rule for cross-analysis disagreement (per EXTRACTION_SKILL §6b).
    - cohort overlaps with Gilmore et al. 2019 and Johnson et al. 2019 — same n=17 anomic Boston University
      subgroup (trial NCT01927302); flag for downstream double-counting risk in interpret_overlap().
    paper_section: Results 3.3.2.3.1.1 + Table 6 (pages 87–89); Discussion 4.3 (page 94)
  region_definition:
    atlas: Harvard-Oxford
    description: ROI-based analysis on aggregated right-hemisphere language network homologues (RH IFGtri,
      IFGoper, frontal orbital cortex, insula, frontal operculum, three MTG parcellations, aSTG, pSTG,
      AG, pSMG, temporal pole) — null Time effect within the naming treatment group.
    kind: atlas
  relationship: treatment_response
  replications: []
  sample:
    age_range: mean 62.0 years (SD 8.8)
    handedness: all right-handed
    language: monolingual native English speakers
    n: 17
    population: chronic stroke-induced anomic aphasia (Boston University subgroup of the n=58 analyzed
      cohort)
    time_post_onset: mean 60.0 months (SD 53.1)
  source_passages:
  - page: 87
    quote: Separate analyses conducted within each group (Table 6) revealed a signiﬁcant increase in activation
      from pre- to post-treatment (i.e., upregulation) only in the sentence production/comprehension and
      the spelling treatment groups, and no changes between time points for the naming treatment group
      or for the natural history (no treatment) group.
    section: Results 3.3.2.3.1.1
    supports: claim
  - page: 94
    quote: For the naming treatment group, although voxel-based analyses showed activation of right anterior
      temporal regions at post- (and not pre-) treatment, the lack of signiﬁcant upregulation on the ROI-based
      analyses suggests that the ﬁndings of the voxel-based analyses may have been either driven by some
      participants, or accounted for by age, education or lesion size.
    section: Discussion 4.3
    supports: claim
  - page: 94
    quote: Results obtained from this group, which were not in line with our predictions, suggest that
      language interventions targeting lexical-semantics may not yield robust, group-level upregulation
      of activation on a naturalistic task that engages processes beyond single-word comprehension. This
      also indicates that the task employed as primary measure of neural plasticity may have a substantial
      effect on the outcome and should be carefully chosen.
    section: Discussion 4.3
    supports: limitation
  - page: 88
    quote: Time (Post- vs. Pre-treatment)  .016  .025  410.8  .653  .655
    section: Table 6 — naming group
    supports: statistics
  - page: 87
    quote: Age, education and lesion size (i.e., the proportion of lesioned tissue in each left-hemisphere
      ROI) were entered as covariates, to ensure that activation changes between time points, as well
      as the Group*Time interaction, were not driven by group differences in demographic or lesion variables.
    section: Methods 2.4.2.4 — ROI analyses
    supports: confounders
  - page: 78
    quote: '70 met the inclusion criteria for the study: (1) presence of a single left-hemisphere stroke
      at least 12 months prior entering the study and affecting at least .1% of the cortical surface in
      the left hemisphere'
    section: Methods 2.1 — Participants
    supports: sample
  statistics:
    ci_95: not_reported
    effect_size: β = 0.016 (essentially zero); ROI-level Time effect not significant
    p_value: 0.655 (ROI-level Time effect, n.s. after FDR correction)
    threshold: 'ROI-based mixed-effects regression with FDR correction; Time effect within naming-treatment
      group: β=0.016, SE=0.025, t(410.8)=0.653, p=0.655 (n.s.)'
  strength: moderate
  target: right_anterior_middle_temporal_gyrus
  target_kind: region
source: agent_draft
last_reviewed: '2026-05-06'
notes: "First-extraction draft from Barbieri et al. 2023. Typicality-based\nSemantic Feature Analysis\
  \ is a naming intervention for anomic\naphasia in which typical (e.g., pigeon) or atypical (e.g., penguin)\n\
  exemplars of a semantic category (e.g., birds) are trained through\ncategory sorting, feature verification,\
  \ and feature review. Two\nfindings recorded:\n\n- f1 (behavioural efficacy): naming treatment significantly\n\
  \  improved trained-item naming accuracy compared to natural history\n  control (p<.0001, β=1.447 z-scored).\n\
  - f2 (mixed neural evidence): voxel-level analyses showed RH\n  anterior-temporal activation post-treatment,\
  \ but ROI-level\n  analyses with covariates showed NO significant upregulation —\n  interpreted by the\
  \ authors as evidence that lexical-semantic\n  treatment may not produce robust group-level reorganization\
  \ on a\n  naturalistic story comprehension task (and that the choice of\n  fMRI task substantially affects\
  \ the outcome).\n\nThis draft anchors on therapy because the paper's claims are about\ntreatment effects.\
  \ The naming-treatment group is the n=17 BU\nsubgroup of the n=58 analyzed cohort.\n\nCaveat for downstream\
  \ interpretation: the voxel-level positive\nfinding is a real (FWE-corrected) result. The ROI-level\
  \ null is\nthe more conservative test (controlling for covariates and\nindividual variability). The\
  \ two findings are not contradictory in\na strict sense — they reflect different sensitivities — but\
  \ they\njointly produce a `mixed` direction at the level of the therapy claim.\n"
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
