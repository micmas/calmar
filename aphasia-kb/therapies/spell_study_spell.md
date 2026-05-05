---
schema_version: 2.3
id: spell_study_spell
name: Spell-study-spell training
aliases:
- spell-study-spell procedure
- spell-study-spell training
- SSS spelling treatment
kind: therapy
status: approved
created_by: agent:claude-opus-4-7
created_on: 2026-05-01
short_description: An impairment-based treatment for acquired dysgraphia in which
  patients listen to a target word, repeat it, spell it, copy it, and spell it again,
  working through a pre-determined individually tailored 40-word list. Emphasizes
  listening and repetition alongside the spelling task.
targets_impairments:
- dysgraphia
dosage: 12 weeks, 2 sessions/week, 1.5 h/session (Barbieri et al. 2023; Purcell et
  al. 2019; Wiley & Rapp 2019 protocol). 40-word individually tailored training list.
findings:
- id: f1
  target: dysgraphia
  target_kind: impairment
  claim: Twelve weeks of spell-study-spell training significantly improves spelling
    accuracy on trained words in chronic acquired dysgraphia compared to a no-treatment
    natural history control group.
  direction: likely
  relationship: responder
  citation: '@Barbieri2023'
  method: clinical_RCT
  design: RCT
  imaging: none
  sample:
    n: 13
    population: chronic stroke-induced acquired dysgraphia (single left-hemisphere
      stroke ≥12 months post-onset; subgroup of n=58 analyzed cohort, recruited at
      Johns Hopkins University)
    time_post_onset: mean 67.9 months (SD 41.1)
    age_range: mean 60.2 years (SD 10.2)
    handedness: 10 right-handed, 2 left-handed, 1 ambidextrous
    language: monolingual native English speakers
    recruitment: Cognitive and Brain Sciences Lab at Johns Hopkins University; randomized
      to treatment vs. natural history at the site by a staff member other than the
      assessor.
    inclusion_criteria: 'age 35–80; education ≥high-school; WAB-AQ 45–95; dysgraphia
      defined as <80% letter accuracy on the Johns Hopkins University Dysgraphia Battery
      and on PALPA subtests #40 and #54.'
    exclusion_criteria: exclusively subcortical lesions; non-monolingual; developmental/psychiatric/other
      neurological history; MRI contraindications.
  statistics:
    threshold: mixed-effects regression with FDR correction; p<0.0001 for the Time
      effect within the spelling treatment group
    cluster_extent: null
    effect_size: β = 2.742 (z-scored letter accuracy units), SE 0.318, t(12) = 8.636
      (Time post- vs. pre-treatment within spelling group); β = 2.603, SE 0.341, t(54)
      = 7.640 for the Time × Group interaction (spelling treatment vs. natural history)
    ci_95: not_reported
    p_value: <0.0001 (within-group); <0.0001 (Time × Group interaction)
  confounders_controlled:
  - age, education, proportion of lesioned left-hemisphere tissue (covariates)
  - natural history group (n=16) used as no-treatment control
  - groups matched on months post-onset, gender, handedness, WAB-AQ, lesion size
  confounders_not_controlled:
  - PI not blinded to treatment allocation
  - sentence treatment group had non-canonical sentence comprehension lower than spelling
    group (residual cross-site heterogeneity)
  region_definition:
    kind: not_reported
    description: Behavioral-only treatment efficacy finding — no specific brain region;
      treatment efficacy measured as the average change (post-pre) in proportion of
      correctly spelled letters out of total letters across all trained words.
  imaging_details:
    reference_space: not_reported
    atlases_used: []
  replications: []
  contradictions: []
  author_limitations:
  - Pre-treatment heterogeneities across treatment groups.
  - Long-term maintenance not assessed.
  - Generalization to untrained words not the focus of this paper (see Purcell et
    al. 2019 and Wiley & Rapp 2019 for generalization details).
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
    - cohort overlaps with Purcell et al. 2019 and Wiley & Rapp 2019 — same n=13 dysgraphic
      Johns Hopkins subgroup (trial NCT01927302); flag for downstream double-counting
      risk in interpret_overlap().
  source_passages:
  - section: Methods 2.2 — Treatment
    page: 80
    supports: method
    quote: at Johns Hopkins University, training employed a spell-study-spell procedure
      for participants with dysgraphia. Treatment procedures required participants
      to listen, repeat, spell, copy and spell again each word from a pre-determined,
      individually tailored, list of words (n ¼ 40).
  - section: Methods 2.1 — Participants
    page: 78
    supports: sample
    quote: '70 met the inclusion criteria for the study: (1) presence of a single
      left-hemisphere stroke at least 12 months prior entering the study and affecting
      at least .1% of the cortical surface in the left hemisphere'
  - section: Methods 2.1 — Participants
    page: 78
    supports: sample
    quote: 'Participants at Johns Hopkins University were recruited if they showed
      evidence of dysgraphia (deﬁned as <80% letter accuracy) on the Johns Hopkins
      University Dysgraphia Battery (Goodman & Caramazza, 1985), as well as on selected
      subtests (#40 and #54) of the Psycholinguistic Assessment of Language Processing
      in Aphasia (PALPA; Kay, Lesser, & Coltheart, 1992).'
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
    quote: Time in Spelling vs. Time in NH Group  2.603  .341  54  7.640  <.0001
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
  target: right_anterior_superior_temporal_gyrus
  target_kind: region
  claim: Spell-study-spell training for dysgraphia produces unexpected pre-to-post-treatment
    upregulation of BOLD activation in right-hemisphere homologues of the language
    network — including right anterior superior temporal gyrus and temporal pole —
    during a naturalistic auditory story comprehension fMRI task; this upregulation
    is NOT associated with changes in word or sentence comprehension performance,
    suggesting it may reflect treatment-induced phonological-discrimination improvements
    rather than language-comprehension gains.
  direction: likely
  relationship: treatment_response
  citation: '@Barbieri2023'
  method: fMRI_activation
  design: RCT
  imaging: fMRI
  sample:
    n: 13
    population: chronic stroke-induced dysgraphia (Johns Hopkins University subgroup
      of the n=58 analyzed cohort)
    time_post_onset: mean 67.9 months (SD 41.1)
    age_range: mean 60.2 years (SD 10.2)
    handedness: 10 right-handed, 2 left-handed, 1 ambidextrous
    language: monolingual native English speakers
  statistics:
    threshold: 'voxel-level p<0.001, FWE-corrected p<0.05 cluster-level (k≥57 voxels
      for spelling-treatment group post-treatment); ROI analysis: mixed-effects regression
      Time within spelling-treatment group: β=0.087, SE=0.032, t(306.4)=2.670, p=0.016
      (FDR-corrected); full-model Group×Time interaction χ²=9.928, p=0.019'
    cluster_extent: 57
    effect_size: 'Voxel-level peak Story>Control activation: T=6.066 (right aSTG,
      k=57, MNI [52,4,-20]). ROI-level Time within group: β=0.087, p=0.016. Brain-behavior
      coupling: noun comprehension β=1.657, SE=1.576, t=1.051, p=0.364 (n.s.); verb
      comprehension β=0.690, SE=0.458, t=1.505, p=0.223 (n.s.); sentence comprehension
      (NAVS-SCT) β=0.598, SE=1.222, t=0.490, p=0.629 (n.s.).'
    ci_95: not_reported
    p_value: 0.016 (ROI-level Time effect); all brain-behavior coupling associations
      n.s.
  confounders_controlled:
  - age, education, proportion of lesioned left-hemisphere tissue (covariates)
  - Participant and ROI as random effects
  - natural history group (n=16) as no-treatment control
  - ROI-level analysis restricted to RH ROIs with suprathreshold post-treatment Story>Control
    activation (right aSTG, temporal pole)
  confounders_not_controlled:
  - scanner differences across 3 sites (Philips Intera at JHU; harmonized via phantom
    scans)
  - control condition (reversed speech) not duration-matched to active condition
  region_definition:
    kind: atlas
    atlas: Harvard-Oxford
    description: 'Voxel-based cluster: right aSTG extending to right temporal pole;
      peak MNI [52,4,-20], k=57 voxels. ROI-based analysis on aggregated RH language
      network homologues found a significant Time effect (p=0.016 FDR-corrected).'
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
      description: Block design auditory story comprehension vs reversed-speech control
        (same task as TUF and SFA drafts); 24-s story blocks alternating with 18-s
        reversed-speech blocks.
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
    - region: right anterior superior temporal gyrus (extending temporal pole)
      mni:
      - 52
      - 4
      - -20
  replications: []
  contradictions: []
  author_limitations:
  - Upregulation in this group is NOT associated with any measured language-comprehension
    outcome — the functional significance of the activation change is unclear.
  - Findings of right-hemisphere upregulation following spelling treatment were unexpected
    based on prior literature (De Marco et al. 2018; Purcell et al. 2017, 2019), which
    has implicated left perilesional regions for spelling recovery.
  - The story comprehension task may be sensitive to phonological discrimination (real
    vs. reversed speech) rather than spelling-specific processing.
  - Pre-treatment heterogeneities and scanner differences.
  evidence_quality: RCT
  strength: moderate
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Results 3.3.2.2 + Table 5 (pages 86–87); Results 3.3.2.3.1.1 +
      Table 6 (pages 87–89); Results 3.3.2.3.1.2 + Table 7 (page 90); Discussion 4.3
      (page 94)
    confidence: high
    flags:
    - Authors interpret the RH upregulation as possibly reflecting phonological-discrimination
      improvements (since spell-study-spell emphasizes listening + repetition), enabling
      better discrimination of real vs. reversed speech rather than enhanced narrative
      comprehension. This interpretation is post-hoc and should be flagged for verification
      with a non-speech control task in future studies.
    - cohort overlaps with Purcell et al. 2019 and Wiley & Rapp 2019 — same n=13 dysgraphic
      Johns Hopkins subgroup (trial NCT01927302); flag for downstream double-counting
      risk in interpret_overlap().
  source_passages:
  - section: Results 3.3.2.2
    page: 87
    supports: claim
    quote: In both the naming and spelling treatment groups, post-treatment activation
      was limited to right temporal regions, including the aSTG and temporal pole
      (for both groups), and the aMTG and pMTG (for the naming treatment group only).
  - section: Results 3.3.2.3.1.1
    page: 87
    supports: claim
    quote: Separate analyses conducted within each group (Table 6) revealed a signiﬁcant
      increase in activation from pre- to post-treatment (i.e., upregulation) only
      in the sentence production/comprehension and the spelling treatment groups,
      and no changes between time points for the naming treatment group or for the
      natural history (no treatment) group.
  - section: Results 3.3.2.3.1.2
    page: 89
    supports: claim
    quote: No associations were found in the spelling treatment group (Table 7).
  - section: Discussion 4.3
    page: 94
    supports: limitation
    quote: Upregulation of right hemisphere homologues of the language network was
      also observed in the spelling treatment group. This ﬁnding was unexpected, both
      based on our predictions and on the ﬁndings of previous studies (De Marco et
      al., 2018; Purcell et al., 2017, 2019), in which evidence of neural plasticity
      following spelling treatment was found in left perilesional regions.
  - section: Discussion 4.3
    page: 94
    supports: limitation
    quote: Importantly, upregulation of activation in this group was not signiﬁcantly
      associated with performance on word or sentence comprehension, suggesting that
      activation changes in this group did not result from improved lexical, sentence,
      or discourse-level comprehension following language intervention. One possible
      interpretation of these results is that the spelling treatment, which also emphasized
      listening and repetition, may have improved phonological processing, thereby
      resulting in better discrimination of real speech from reversed speech and increased
      post-treatment BOLD signal for the Story > Control contrast.
  - section: Table 6 — Spelling Group
    page: 88
    supports: statistics
    quote: Time (Post- vs. Pre-treatment)  .087  .032  306.4  2.670  .016
  - section: Methods 2.4.2.4 — ROI analyses
    page: 87
    supports: confounders
    quote: Age, education and lesion size (i.e., the proportion of lesioned tissue
      in each left-hemisphere ROI) were entered as covariates, to ensure that activation
      changes between time points, as well as the Group*Time interaction, were not
      driven by group differences in demographic or lesion variables.
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
source: agent_draft
last_reviewed: null
notes: "First-extraction draft from Barbieri et al. 2023. Spell-study-spell\nis an\
  \ impairment-based treatment for acquired dysgraphia in which\nparticipants listen\
  \ to, repeat, spell, copy, and re-spell each word\nfrom an individually tailored\
  \ 40-word list. Two findings recorded:\n\n- f1 (behavioural efficacy): spelling\
  \ treatment significantly\n  improved letter-level accuracy on trained words compared\
  \ to\n  natural history (β=2.742 z-scored, p<.0001).\n- f2 (RH neural reorganization\
  \ without behavioral coupling):\n  significant ROI-level upregulation in RH language\
  \ network\n  homologues (β=0.087, p=0.016 FDR-corrected) AND voxel-level\n  activation\
  \ in right aSTG + temporal pole (k=57). However, this\n  upregulation was NOT associated\
  \ with changes in word or sentence\n  comprehension, prompting the authors to suggest\
  \ a phonological-\n  discrimination interpretation: the listen-repeat component\
  \ of\n  spell-study-spell may have improved phonological processing,\n  leading\
  \ to better real-vs-reversed-speech discrimination on the\n  fMRI task — a phonological\
  \ side-effect rather than a\n  comprehension gain.\n\nAnchored on therapy because\
  \ the paper's claims are about treatment\neffects.\n\nNotable contrast with TUF:\
  \ TUF produced robust RH upregulation\nthat DID correlate with comprehension changes\
  \ (verb and sentence);\nspell-study-spell produced RH upregulation that did NOT\
  \ correlate\nwith comprehension changes. The authors use this contrast to argue\n\
  that \"specificity rebuilds language networks\" (Kleim & Jones 2008;\nKiran & Thompson\
  \ 2019) — sentence-level treatment produces\nsentence-comprehension-relevant neural\
  \ changes, whereas word-level\ntreatments (naming, spelling) produce different (or\
  \ no) neural\nchanges that don't track comprehension."
reviewer: auto-reviewer
reviewed_on: '2026-05-05'
---
# Spell-study-spell training

## Therapy description

Spell-study-spell is an impairment-based treatment for acquired
dysgraphia. Each session, the patient is presented with a target
word from a pre-determined, individually tailored 40-word list; the
clinician guides them through listening, repeating, spelling,
copying, and spelling again each target word.

In Barbieri et al. 2023, spell-study-spell was administered on the
same fixed schedule as the other treatments (12 weeks, 2 sessions/
week, 1.5 h/session), and treatment efficacy was measured as the
average change (post-pre) in proportion of correctly spelled letters
across all trained words.

## Notes for next extraction round

  - Add `dysgraphia` as an impairment entry (currently only
    referenced as a target ID).
  - The right-hemisphere region target in f2 (right_anterior_superior
    _temporal_gyrus) does not yet exist as a region entry; reviewer
    should decide on the hemisphere-prefixing convention (see same
    note in the TUF draft).
  - The "phonological discrimination side-effect" interpretation in
    f2 is a post-hoc explanation. A future study with a non-speech
    control (e.g., music or environmental sounds) would test whether
    the RH upregulation reflects general auditory discrimination
    improvement vs. story-comprehension-specific recovery.
  - The Barbieri et al. 2019 paper, on the same agrammatic
    participants but with a sentence-picture verification task, found
    additional RH and bilateral domain-general (Dorsal Attention
    Network) upregulation. Future extraction of the 2019 paper may
    yield additional findings for the TUF therapy entry.
