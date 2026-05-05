---
schema_version: 2.3
id: treatment_of_underlying_forms
name: Treatment of Underlying Forms (TUF)
aliases:
- TUF
- sentence-level treatment
- thematic-syntactic mapping treatment
kind: therapy
status: approved
created_by: agent:claude-opus-4-7
created_on: 2026-05-01
short_description: A linguistically-motivated, impairment-based intervention for agrammatic
  aphasia that uses meta-linguistic steps focused on verbs, verb argument structure,
  and thematic-syntactic mapping in active and passive sentences. Designed to restore
  the processes of thematic role assignment and complex sentence processing.
targets_impairments:
- agrammatism
- sentence_comprehension
- sentence_production
dosage: '12 weeks, 2 sessions/week, 1.5 h/session (Barbieri et al. 2023 protocol).
  Original protocol: Thompson & Shapiro (2005).'
findings:
- id: f1
  target: agrammatism
  target_kind: impairment
  claim: Twelve weeks of Treatment of Underlying Forms (TUF) significantly improves
    production and comprehension of canonical and non-canonical sentences in chronic
    agrammatic aphasia compared to a no-treatment natural history control group.
  direction: likely
  relationship: responder
  citation: '@Barbieri2023'
  method: clinical_RCT
  design: RCT
  imaging: none
  sample:
    n: 12
    population: chronic stroke-induced agrammatic aphasia (single left-hemisphere
      stroke ≥12 months post-onset; subgroup of n=58 analyzed cohort, recruited at
      Northwestern University)
    time_post_onset: mean 42.3 months (SD 30.0)
    age_range: mean 50.0 years (SD 7.4); younger than other treatment groups
    handedness: 9 right-handed, 3 left-handed
    language: monolingual native English speakers
    recruitment: Aphasia and Neurolinguistics Research Lab at Northwestern University;
      randomized to treatment vs. natural history at each site by a staff member other
      than the assessor.
    inclusion_criteria: age 35–80; education ≥high-school; WAB-AQ 45–95; agrammatism
      (impaired non-canonical>canonical sentence production and comprehension on NAVS;
      <50% grammatical sentences in Cinderella retell; relatively spared single-word
      comprehension).
    exclusion_criteria: exclusively subcortical lesions; non-monolingual; developmental/psychiatric/other
      neurological history; MRI contraindications.
  statistics:
    threshold: mixed-effects regression with FDR correction; p<0.0001 for the Time
      effect within the sentence treatment group
    cluster_extent: null
    effect_size: β = 2.520 (z-scored accuracy units), SE 0.342, t(11) = 7.367 (Time
      post- vs. pre-treatment within sentence group); β = 2.381, SE 0.348, t(54) =
      6.832 for the Time × Group interaction (sentence treatment vs. natural history)
    ci_95: not_reported
    p_value: <0.0001
  confounders_controlled:
  - age, education, proportion of lesioned left-hemisphere tissue (entered as covariates)
  - natural history group (n=16) used as no-treatment control
  - groups matched on months post-onset, gender, handedness, WAB-AQ, lesion size
  confounders_not_controlled:
  - PI not blinded to treatment allocation at each site
  - scanner and recruitment-site differences (3 different MRI scanners across sites)
  - groups differed on age (sentence treatment group younger) and education (naming
    group lower)
  region_definition:
    kind: not_reported
    description: Behavioral-only treatment efficacy finding — no specific brain region;
      treatment-targeted behavioural measures only (sentence production priming task
      and picture verification task on 10 trained passive sentences).
  imaging_details:
    reference_space: not_reported
    atlases_used: []
  replications:
  - '@Schlaug2008'
  - '@Pulvermuller2001'
  contradictions: []
  author_limitations:
  - Pre-treatment heterogeneities across treatment groups (different impairment profiles,
    different recruitment sites).
  - Different MRI scanners across sites (Siemens Trio at NU, Siemens Skyra at BU,
    Philips Intera at JHU); harmonized via phantom scans but residual scanner variability
    cannot be excluded.
  - Long-term maintenance of treatment effects not assessed.
  evidence_quality: RCT
  strength: strong
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Results 3.1 + Table 2 (page 83); Methods 2.2 (page 80); Methods
      2.3.1 (page 80)
    confidence: high
    flags:
    - method coded as clinical_RCT given the randomized design with natural history
      controls; the paper is also primarily an fMRI study (subsequent findings use
      fMRI_activation method).
    - behavioural-only finding — imaging fields are minimal; flagged that this is
      a treatment-efficacy claim, not a region-tied claim.
    - 'cohort overlaps with Barbieri et al. 2019 (Cortex 120: 394-418) — same n=12
      agrammatic participants (trial NCT01927302); flag for downstream double-counting
      risk in interpret_overlap().'
  source_passages:
  - section: Methods 2.2 — Treatment
    page: 80
    supports: method
    quote: participants in the treatment group underwent Treatment of Underlying Forms
      (TUF, Thompson & Shapiro, 2005), a treatment approach that uses a series of
      meta-linguistic steps focused on verbs, verb argument structure, and thematic-syntactic
      mapping in active (e.g., The man was shaving the boy) and passive sentences
      (e.g., The boy was shaved by the man) to improve sentence comprehension and
      production.
  - section: Methods 2.1 — Participants
    page: 78
    supports: sample
    quote: '70 met the inclusion criteria for the study: (1) presence of a single
      left-hemisphere stroke at least 12 months prior entering the study and affecting
      at least .1% of the cortical surface in the left hemisphere'
  - section: Methods 2.1 — Participants
    page: 78
    supports: sample
    quote: 'participants recruited at Northwestern University were selected for agrammatism,
      which was deﬁned by: a) evidence of impaired production and comprehension of
      sentences (for syntactically complex (non-canonical) more than for simple (canonical)
      sentences) on the Northwestern Assessment of Verbs and Sentences (NAVS, Thompson,
      2011); b) production of less than 50% grammatical sentences on the re-telling
      of Cinderella''s story; and c) relatively spared single-word comprehension'
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
    quote: Time in Sentence Prod/Comp vs. Time in NH Group  2.381  .348  54  6.832  <.0001
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
  - section: Limitations
    page: 96
    supports: limitation
    quote: structural and functional images were collected using different scanners,
      anddalthough harmonization among scanners was carried out prior to undertaking
      the studydthe possibility that minor inconsistencies among scanners may have
      affected functional activation patterns cannot be excluded.
- id: f2
  target: right_anterior_middle_temporal_gyrus
  target_kind: region
  claim: Treatment of Underlying Forms (TUF) induces significant pre-to-post-treatment
    upregulation of BOLD activation in right-hemisphere homologues of the language
    network — including right anterior middle temporal gyrus, anterior superior temporal
    gyrus, posterior middle/superior temporal gyrus, IFG pars triangularis and pars
    opercularis — during a naturalistic auditory story comprehension fMRI task in
    chronic agrammatic aphasia.
  direction: likely
  relationship: treatment_response
  citation: '@Barbieri2023'
  method: fMRI_activation
  design: RCT
  imaging: fMRI
  sample:
    n: 12
    population: chronic stroke-induced agrammatic aphasia (Northwestern subgroup of
      the n=58 analyzed cohort)
    time_post_onset: mean 42.3 months (SD 30.0)
    age_range: mean 50.0 years (SD 7.4)
    handedness: 9 right-handed, 3 left-handed
    language: monolingual native English speakers
  statistics:
    threshold: 'voxel-level p<0.001, FWE-corrected p<0.05 cluster-level (k≥60 voxels
      for sentence-treatment group post-treatment); ROI analysis: mixed-effects regression
      with FDR correction, p<0.05; full-model Group×Time interaction χ²=9.928, p=0.019'
    cluster_extent: 502
    effect_size: 'ROI analysis Time within sentence-treatment group: β=0.096, SE=0.028,
      t(285.9)=3.402, p=0.003 (FDR-corrected). Voxel-level peak T-values: 8.335 (right
      pMTG), 7.002 (right pMTG/aMTG), 5.972 (right PCG), 5.462 (right IFGtri).'
    ci_95: not_reported
    p_value: 0.003 (ROI-based, FDR-corrected)
  confounders_controlled:
  - age, education, proportion of lesioned left-hemisphere tissue (covariates in mixed-effects
    regression)
  - Participant and ROI as random effects (account for individual variability and
    ROI-related variance)
  - natural history group (n=16) as no-treatment control
  confounders_not_controlled:
  - scanner differences across 3 sites (Siemens Trio, Siemens Skyra, Philips Intera;
    harmonized via phantom scans)
  - TR difference between two participants (2 s) vs. rest (2.4 s)
  - control condition (reversed speech) not duration-matched to active condition (real
    stories)
  region_definition:
    kind: atlas
    atlas: Harvard-Oxford (Desikan et al. 2006)
    description: Region-of-interest mask aggregating Harvard-Oxford labels for IFGtri,
      IFGoper, frontal orbital cortex, insula, frontal operculum, all three MTG parcellations
      (anterior, posterior, temporo-occipital), aSTG, pSTG, AG, pSMG, and temporal
      pole — restricted to the right hemisphere (homologues of the left-hemisphere
      language network active in healthy controls during the same story-comprehension
      task). Voxel-based peak Story>Control activation in the sentence-treatment group
      post-treatment was reported at MNI [48,-36,0] (right pMTG), [50,0,48] (right
      PCG), [48,-18,-10] (right pMTG/aMTG), [56,28,20] (right IFGtri).
  imaging_details:
    field_strength: 3T
    acquisition:
      voxel_size_mm:
      - 1.72
      - 1.72
      - 3.0
      TR_ms: 2400
      TE_ms: 20
      sequence: gradient-echo T2*-weighted EPI (192 or 162 volumes per run)
    modalities:
    - modality: T1
      sequence: 3D T1-weighted MPRAGE
      voxel_size_mm:
      - 1.0
      - 1.0
      - 1.0
      TR_ms: 2300
      TE_ms: 2.91
      notes: flip angle 9°; FOV 256×256; used for normalization and lesion drawing.
    - modality: fMRI
      sequence: gradient-echo T2*-weighted EPI
      voxel_size_mm:
      - 1.72
      - 1.72
      - 3.0
      TR_ms: 2400
      TE_ms: 20
      volumes: 192
      notes: Block design auditory story comprehension task vs reversed-speech control.
        Two runs per session, four 24-s story blocks and four 18-s reversed-speech
        blocks per run.
    task:
      name: Auditory story comprehension
      description: Block design alternating 24-s blocks of auditorily presented short
        stories with 18-s blocks of digitally time-reversed speech (low-level baseline).
        Stories controlled for syllables (M=80±2.14), words (M=62.5±2.67), nouns (M=19±1.51),
        verbs (M=10.63±0.74), and complex sentences (M=3.13±0.64). Participants pressed
        a button at story onset to indicate 'real' vs reversed speech.
      contrasts:
      - Stories > Control (reversed speech)
      baseline: Time-reversed speech (preserves phonological features without meaning)
    preprocessing_pipeline: AFNI 3dDespike + 3dvolreg motion correction; FD>0.5mm
      and DVARS>50 motion regressors; CompCor (top 3 PCs from WM/CSF); SPM-DARTEL
      normalization to MNI152 (2×2×2 mm); 6 mm FWHM smoothing; SPM12 first-level GLM
      with HRF + time and dispersion derivatives (to account for stroke effect on
      HRF, Bonakdarpour et al. 2007); enantiomorphic replacement of left-hemisphere
      lesion with mirrored right-hemisphere tissue (Nachev et al. 2008)
    reference_space: MNI152
    atlases_used:
    - Harvard-Oxford (Desikan et al. 2006)
    coordinates_reported:
    - region: right posterior MTG (extending tpoMTG, pSTG)
      mni:
      - 48
      - -36
      - 0
    - region: right precentral gyrus (extending MFG)
      mni:
      - 50
      - 0
      - 48
    - region: right pMTG (extending aMTG, aSTG, pSTG)
      mni:
      - 48
      - -18
      - -10
    - region: right IFG pars triangularis (extending IFGoper, MFG)
      mni:
      - 56
      - 28
      - 20
  replications:
  - '@Mirman2015'
  contradictions: []
  author_limitations:
  - No upregulation observed in left-hemisphere ROIs (Time effect not significant
    for LH; Group×Time not significant for LH).
  - Pre-treatment, no patient group showed significant Story>Control activation in
    either hemisphere — possibly due to reduced BOLD sensitivity in damaged left cortex
    or to extensive temporal lobe damage disrupting whole-network connectivity.
  - Three different MRI scanners across recruitment sites (harmonized but residual
    variability cannot be excluded).
  - Reversed-speech control condition not duration-matched to active stories.
  evidence_quality: RCT
  strength: strong
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Results 3.3.2.2 + Table 5 (pages 86–87); Results 3.3.2.3.1.1 +
      Table 6 (pages 87–89); Discussion 4.3 + 4.4 (pages 93–95)
    confidence: high
    flags:
    - 'cohort overlaps with Barbieri et al. 2019 (Cortex 120: 394-418) — same n=12
      agrammatic participants (trial NCT01927302); flag for downstream double-counting
      risk in interpret_overlap().'
  source_passages:
  - section: Results 3.3.2.2
    page: 85
    supports: claim
    quote: while no suprathreshold activation was found at pre-treatment for any of
      the patient groups, post-treatment activation was signiﬁcantly greater than
      zero in all the three treatment groups, but not in the natural history group.
  - section: Results 3.3.2.2
    page: 85
    supports: claim
    quote: in the sentence production/comprehension treatment group, post-treatment
      activation was observed in two right temporal clusters, one more anterior, encompassing
      the aMTG and aSTG, and extending to include portions of the pMTG and pSTG, and
      one more posterior, centered on the pMTG and encompassing the temporo-occipital
      portion of the MTG and pSTG.
  - section: Results 3.3.2.3.1.1
    page: 87
    supports: statistics
    quote: The full model for the right-hemisphere ROIs (Table 6) showed a signiﬁcant
      effect of Time across groups, with activation for the Story > Control contrast
      being signiﬁcantly greater at post- than at pre-treatment. A signiﬁcant Group*Time
      interaction was also found
  - section: Methods 2.3.2.2 — Data acquisition
    page: 81
    supports: imaging_details
    quote: Structural and functional MR images were collected using 3T scanners (Siemens
      Trio at Northwestern University, Siemens Skyra at Boston University, and Philips
      Intera at Johns Hopkins University) and a 3D T1-weighted sequence for structural
      (TR ¼ 2.3sec, TE ¼ 2.91 ms, ﬂip angle ¼ 9, ﬁeld of view ¼ 256  256, 1 mm isotropic
      voxel size), or a gradient-echo T2*-weighted sequence for functional
  - section: Methods 2.4.2.3 — Voxel-level analyses
    page: 81
    supports: statistics
    quote: T-maps were obtained by applying a p < .001 threshold at the voxel-level.
      Cluster-level correction was carried out using the family-wise error (FWE) correction
      provided by SPM12, at a threshold of p < .05
  - section: Methods 2.1 — Participants
    page: 78
    supports: sample
    quote: '70 met the inclusion criteria for the study: (1) presence of a single
      left-hemisphere stroke at least 12 months prior entering the study and affecting
      at least .1% of the cortical surface in the left hemisphere'
  - section: Methods 2.4.2.1 — Anatomical images
    page: 81
    supports: imaging_details
    quote: structural T1 images underwent enantiomorphic replacement wherein healthy
      tissue from the right hemisphere was mirrored into the lesioned area (Nachev,
      Coulthard, J€ager, Kennard, & Husain, 2008), and the resulting brains were normalized
      to the MNI template using the SPM DARTEL toolbox (Ashburner, 2007).
  - section: Discussion 4.3
    page: 94
    supports: limitation
    quote: the lack of activation in the left hemisphere of individuals with aphasia
      could be due to reduced sensitivity to BOLD signal detection in the damaged
      cortex.
  - section: Methods 2.4.2.4 — ROI analyses
    page: 87
    supports: confounders
    quote: Age, education and lesion size (i.e., the proportion of lesioned tissue
      in each left-hemisphere ROI) were entered as covariates, to ensure that activation
      changes between time points, as well as the Group*Time interaction, were not
      driven by group differences in demographic or lesion variables.
- id: f3
  target: agrammatism
  target_kind: impairment
  claim: Treatment-induced upregulation of BOLD activation in right-hemisphere language
    network homologues during the auditory story comprehension task is positively
    associated with improved verb comprehension (NNB Verb Comprehension subtest) and
    (marginally) sentence comprehension (NAVS Sentence Comprehension Test) in the
    sentence treatment (TUF) group, but not with noun comprehension.
  direction: likely
  relationship: responder
  citation: '@Barbieri2023'
  method: fMRI_activation
  design: RCT
  imaging: fMRI
  sample:
    n: 12
    population: chronic stroke-induced agrammatic aphasia (TUF subgroup)
    time_post_onset: mean 42.3 months (SD 30.0)
    age_range: mean 50.0 years (SD 7.4)
    handedness: 9 right-handed, 3 left-handed
    language: monolingual native English speakers
  statistics:
    threshold: mixed-effects regression on RH ROIs that showed suprathreshold post-treatment
      Story>Control activation; FDR-corrected for multiple comparisons within group;
      p<0.05
    effect_size: 'Verb comprehension: β=1.051, SE=0.343, t(94)=3.063, p=0.017 (FDR-corrected).
      Sentence comprehension (NAVS-SCT): β=0.768, SE=0.318, t(94)=2.418, p=0.053 (marginal).
      Noun comprehension: β=1.739, SE=1.196, t(94)=1.454, p=0.224 (n.s.).'
    ci_95: not_reported
    p_value: 0.017 (verb comprehension); 0.053 (sentence comprehension, marginal);
      0.224 (noun comprehension, n.s.)
  confounders_controlled:
  - ROI as random effect (accounts for ROI-related variance)
  - analyses restricted to RH ROIs with suprathreshold post-treatment Story>Control
    activation (i.e., RH IFGtri, IFGoper, MTG (3 parcellations), aSTG, pSTG)
  confounders_not_controlled:
  - no demographic covariates in the brain-behavior coupling analysis (age, education,
    lesion size were already controlled in the upstream ROI analysis)
  - single time-point change (post-pre); no longitudinal trajectory
  region_definition:
    kind: atlas
    atlas: Harvard-Oxford
    description: 'Right-hemisphere language network homologues that showed suprathreshold
      post-treatment Story>Control activation: RH IFGtri, RH IFGoper, RH MTG (anterior,
      posterior, temporo-occipital), RH aSTG, RH pSTG.'
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: 'Same as f2: AFNI + SPM-DARTEL + 6mm FWHM; SPM12 GLM with
      HRF + derivatives'
    reference_space: MNI152
    atlases_used:
    - Harvard-Oxford
    task:
      name: Auditory story comprehension
      description: Block design auditory story comprehension vs reversed-speech control
      contrasts:
      - Stories > Control
      baseline: Time-reversed speech
  replications:
  - '@Saur2008'
  contradictions: []
  author_limitations:
  - Brain-behavior association applies only to the sentence treatment group; same
    analysis on the spelling treatment group found no associations.
  - Sentence comprehension association is marginal (p=0.053) — interpretation should
    be cautious.
  - Group included only n=12 — power is limited.
  evidence_quality: RCT
  strength: moderate
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Results 3.3.2.3.1.2 + Table 7 + Fig. 5 (pages 89–90); Discussion
      4.3 (page 94)
    confidence: high
    flags:
    - Marginal sentence-comprehension association (p=0.053) — strength flagged as
      moderate.
    - TUF behavioural target is sentence production+comprehension, but the brain-behavior
      coupling here is observed for verb comprehension and sentence comprehension
      (NOT noun comprehension or sentence production), aligning with TUF's focus on
      verb-argument structure and thematic-syntactic mapping.
    - 'cohort overlaps with Barbieri et al. 2019 (Cortex 120: 394-418) — same n=12
      agrammatic participants (trial NCT01927302); flag for downstream double-counting
      risk in interpret_overlap().'
  source_passages:
  - section: Results 3.3.2.3.1.2
    page: 89
    supports: claim
    quote: Analyses run within the sentence production/comprehension treatment group
      showed a signiﬁcant (or marginally signiﬁcant, in the case of sentence comprehension,
      following correction for multiple comparisons) positive association between
      changes in activation in the language network homologue and improved accuracy
      on measures of verb and sentence comprehension
  - section: Table 7
    page: 90
    supports: statistics
    quote: change on NNB VC  1.051  .343  94.0  3.063  .017
  - section: Discussion 4.3
    page: 94
    supports: claim
    quote: results of the voxel-based and ROI-based analyses indicate that participants
      who received treatment for sentence processing (i.e., Treatment of Underlying
      Forms, TUF, Thompson & Shapiro, 2005) showed clear evidence of neural plasticity,
      as suggested by post-treatment activation increases within right-hemisphere
      language network homologues that were active in healthy participants on the
      same task, and by signiﬁcant associations between activation changes and improved
      verb and sentence comprehension.
  - section: Methods 2.4.2.4
    page: 87
    supports: method
    quote: the change in BOLD signal between time points (post-minus pre-treatment)
      was entered as the dependent variable; changes in performance on measures of
      word (i.e., change on the NNB noun and verb comprehension subtests) and sentence
      comprehension (i.e., change on the NAVS sentence comprehension subtest) were
      entered as ﬁxed effects in separate analyses.
  - section: Limitations
    page: 96
    supports: limitation
    quote: participants were recruited from different research centers because they
      met criteria for different language deﬁcits, which resulted in pre-treatment
      heterogeneities across groups in terms of language proﬁles.
  - section: Methods 2.4.2.4
    page: 87
    supports: confounders
    quote: ROIs were included only if signiﬁcant post-treatment activation for the
      Story > Control contrast was found on the voxel-based analysis. This choice
      was made to ensure that the relationship between upregulation of activation
      and changes in language scores was limited to regions for which upregulation
      of activation resulted in post-treatment neural response patterns to naturalistic
      language comprehension that were similar to those of healthy individuals
source: agent_draft
last_reviewed: null
notes: "First-extraction draft from Barbieri et al. 2023. TUF (Treatment of\nUnderlying\
  \ Forms) is a linguistically-motivated sentence-level\ntreatment focused on verb\
  \ argument structure and thematic-syntactic\nmapping. Three findings recorded:\n\
  \n- f1 (behavioural efficacy): TUF improves sentence production and\n  comprehension\
  \ over 12 weeks compared to a no-treatment control.\n- f2 (neural reorganization):\
  \ TUF induces upregulation of right-\n  hemisphere language network homologues during\
  \ a naturalistic\n  auditory story comprehension fMRI task. Right-hemisphere clusters\n\
  \  encompass anterior and posterior MTG, aSTG, pSTG, IFGtri,\n  IFGoper, and PCG.\n\
  - f3 (brain-behavior coupling): TUF-induced RH upregulation\n  correlates with improved\
  \ verb comprehension (p=.017) and\n  marginally with sentence comprehension (p=.053),\
  \ but NOT with\n  noun comprehension. This pattern is theoretically consistent with\n\
  \  TUF's focus on verb argument structure.\n\nImportantly, NO comparable upregulation\
  \ was observed in left-\nhemisphere ROIs (Group×Time interaction n.s. for LH); pre-treatment,\n\
  no patient group showed significant Story>Control activation in\neither hemisphere.\
  \ The authors interpret this as either reduced\nBOLD sensitivity in damaged left\
  \ cortex or extensive temporal-lobe\ndamage disrupting whole-network connectivity.\n\
  \nAnchored on therapy because the paper's main claims are about\ntreatment efficacy\
  \ and treatment-induced neural reorganization. The\nbrain-behavior coupling finding\
  \ (f3) is a `responder` finding (a\nmoderator claim about which patients respond\
  \ to TUF, indexed by\nRH activation change).\n\nAll three findings come from the\
  \ same n=12 sentence-treatment\nsubgroup of the n=58 analyzed cohort. Effect sizes\
  \ for behavioural\nimprovement are large (β>2 in z-score units) but the imaging\n\
  findings come from a small sample with limited power."
reviewer: auto-reviewer
reviewed_on: '2026-05-05'
---
# Treatment of Underlying Forms (TUF)

## How to read this entry

First-extraction draft from Barbieri et al. 2023. Defines TUF as a
draft therapy entry and lists three findings: behavioural efficacy
(f1), right-hemisphere neural reorganization (f2), and brain-behavior
coupling (f3).

## Therapy description

TUF is a meta-linguistic, impairment-based intervention for
agrammatic aphasia developed by Thompson & Shapiro (2005). It
focuses on verbs, verb argument structure (Agent / Theme thematic
roles), and thematic-syntactic mapping in active and passive
sentences. Treatment steps include identification of thematic roles
in target action pictures, guided construction of an active
sentence, clinician-demonstrated derivation of the passive form,
and participant-initiated passive sentence construction.

In Barbieri et al. 2023, TUF was administered to 12 chronic
agrammatic aphasic individuals on a fixed schedule (12 weeks,
2 sessions/week, 1.5 h/session), with treatment efficacy measured
on a sentence production priming task and a picture verification
task using 10 trained passive sentences.

## Notes for next extraction round

  - Add agrammatism, sentence_comprehension, sentence_production as
    impairment entries (currently only referenced as target IDs).
  - The right-hemisphere region targets in f2 (right_anterior_middle_
    temporal_gyrus etc.) do not yet exist as canonical region entries;
    reviewer should decide whether to:
      a) create hemisphere-prefixed region entries (right_*) for
         this and future therapy-induced-reorganization findings, or
      b) use the same atlas IDs as left-hemisphere counterparts and
         note hemisphere in the region_definition.description.
  - The Barbieri 2023 cohort overlaps with Barbieri et al. 2019
    (NCT01927302); future extractions of the 2019 paper may produce
    additional findings on the same participants.
