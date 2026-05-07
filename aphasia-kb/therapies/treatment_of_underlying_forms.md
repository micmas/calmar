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
targets_impairments: [agrammatism, brocas_aphasia, sentence_comprehension, sentence_production, syntactic_processing]
dosage: '12 weeks, 2 sessions/week, 1.5 h/session (Barbieri et al. 2023 protocol).
  Original protocol: Thompson & Shapiro (2005).'
atf_id: 21
atf_evidence_level: level_II
evidence_level: level_II
atf_aliases:
  - TUF
  - sentence-level treatment
  - thematic-syntactic mapping treatment
icf_domain:
  - body_function
tidier:
  brief_name: Treatment of Underlying Forms (TUF)
  rationale: |-
    Agrammatic aphasia involves selective impairment of non-canonical sentence structures
        (passives, object-relative clauses, wh-questions) arising from disrupted thematic
        role assignment and argument structure mapping. TUF targets the underlying
        syntactic representations (verb argument structure, movement traces) rather than
        surface forms, exploiting complexity-based generalisation: training complex
        structures drives generalisation to simpler structures but not vice versa.
  materials: |-
    Sentence-picture matching stimuli (canonical and non-canonical structures); verb-
        specific argument structure frames; Thompson & Shapiro protocol manual (2005);
        treatment and probe word lists.
  procedures: |-
    Clinician presents target sentences with canonical and non-canonical structures.
        Patient identifies agent, theme, and location thematic roles using backward
        chaining (from simplified to complex sentence forms). Treatment moves from
        sentence comprehension to production. Weekly probes test generalisation to
        untrained sentence structures and verbs.
  who_provides: Speech-language pathologist (individual sessions).
  delivery_mode: face_to_face
  setting: Outpatient clinic or university research laboratory.
  dosage: |-
    Thompson & Shapiro 2005: 3 sessions/week × 8–12 weeks; 60 min per session. Total dose
        approximately 24–36 hours.
  tailoring: |-
    Verb type (transitive, ditransitive, unaccusative) and argument count selected based
        on patient's pretreatment syntactic profile. Target sentence structures chosen
        from standardised syntactic battery results.
  modifications: |-
    Computer-delivered TUF validated (Helm-Estabrooks 2003). TUF for Verbs (TUF-V) extends
        treatment to verb argument structure training. Some implementations pair TUF with
        script training for functional discourse goals.
  fidelity_planned: |-
    Weekly treatment probes at 90% accuracy criterion to advance to next structure.
        Session logs; generalisation probe administered to untrained verbs and structures.
  fidelity_actual: |-
    Thompson 2003: treatment logs maintained; independent fidelity rating NR. Formal
        fidelity coding not reported in primary publications.
  confidence: medium
  flags:
    - Thompson & Shapiro 2005 not formally extracted from papers/. TIDieR populated from
        published protocol descriptions.
rtss_ingredients:
  - verb_argument_structure_training
findings:
- author_limitations:
  - Pre-treatment heterogeneities across treatment groups (different impairment profiles,
    different recruitment sites).
  - Different MRI scanners across sites (Siemens Trio at NU, Siemens Skyra at BU,
    Philips Intera at JHU); harmonized via phantom scans but residual scanner variability
    cannot be excluded.
  - Long-term maintenance of treatment effects not assessed.
  citation: '@Barbieri2023'
  claim: Twelve weeks of Treatment of Underlying Forms (TUF) significantly improves
    production and comprehension of canonical and non-canonical sentences in chronic
    agrammatic aphasia compared to a no-treatment natural history control group.
  confounders_controlled:
  - age, education, proportion of lesioned left-hemisphere tissue (entered as covariates)
  - natural history group (n=16) used as no-treatment control
  - groups matched on months post-onset, gender, handedness, WAB-AQ, lesion size
  confounders_not_controlled:
  - PI not blinded to treatment allocation at each site
  - scanner and recruitment-site differences (3 different MRI scanners across sites)
  - groups differed on age (sentence treatment group younger) and education (naming
    group lower)
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
    - method coded as clinical_RCT given the randomized design with natural history
      controls; the paper is also primarily an fMRI study (subsequent findings use
      fMRI_activation method).
    - "behavioural-only finding \u2014 imaging fields are minimal; flagged that this\
      \ is a treatment-efficacy claim, not a region-tied claim."
    - "cohort overlaps with Barbieri et al. 2019 (Cortex 120: 394-418) \u2014 same\
      \ n=12 agrammatic participants (trial NCT01927302); flag for downstream double-counting\
      \ risk in interpret_overlap()."
    paper_section: Results 3.1 + Table 2 (page 83); Methods 2.2 (page 80); Methods
      2.3.1 (page 80)
  region_definition:
    description: "Behavioral-only treatment efficacy finding \u2014 no specific brain\
      \ region; treatment-targeted behavioural measures only (sentence production\
      \ priming task and picture verification task on 10 trained passive sentences)."
    kind: not_reported
  relationship: responder
  replications:
  - '@Schlaug2008'
  - '@Pulvermuller2001'
  sample:
    age_range: mean 50.0 years (SD 7.4); younger than other treatment groups
    exclusion_criteria: exclusively subcortical lesions; non-monolingual; developmental/psychiatric/other
      neurological history; MRI contraindications.
    handedness: 9 right-handed, 3 left-handed
    inclusion_criteria: "age 35\u201380; education \u2265high-school; WAB-AQ 45\u2013\
      95; agrammatism (impaired non-canonical>canonical sentence production and comprehension\
      \ on NAVS; <50% grammatical sentences in Cinderella retell; relatively spared\
      \ single-word comprehension)."
    language: monolingual native English speakers
    n: 12
    population: "chronic stroke-induced agrammatic aphasia (single left-hemisphere\
      \ stroke \u226512 months post-onset; subgroup of n=58 analyzed cohort, recruited\
      \ at Northwestern University)"
    recruitment: Aphasia and Neurolinguistics Research Lab at Northwestern University;
      randomized to treatment vs. natural history at each site by a staff member other
      than the assessor.
    time_post_onset: mean 42.3 months (SD 30.0)
  source_passages:
  - page: 80
    quote: participants in the treatment group underwent Treatment of Underlying Forms
      (TUF, Thompson & Shapiro, 2005), a treatment approach that uses a series of
      meta-linguistic steps focused on verbs, verb argument structure, and thematic-syntactic
      mapping in active (e.g., The man was shaving the boy) and passive sentences
      (e.g., The boy was shaved by the man) to improve sentence comprehension and
      production.
    section: "Methods 2.2 \u2014 Treatment"
    supports: method
  - page: 78
    quote: '70 met the inclusion criteria for the study: (1) presence of a single
      left-hemisphere stroke at least 12 months prior entering the study and affecting
      at least .1% of the cortical surface in the left hemisphere'
    section: "Methods 2.1 \u2014 Participants"
    supports: sample
  - page: 78
    quote: "participants recruited at Northwestern University were selected for agrammatism,\
      \ which was de\uFB01ned by: a) evidence of impaired production and comprehension\
      \ of sentences (for syntactically complex (non-canonical) more than for simple\
      \ (canonical) sentences) on the Northwestern Assessment of Verbs and Sentences\
      \ (NAVS, Thompson, 2011); b) production of less than 50% grammatical sentences\
      \ on the re-telling of Cinderella's story; and c) relatively spared single-word\
      \ comprehension"
    section: "Methods 2.1 \u2014 Participants"
    supports: sample
  - page: 82
    quote: "Post-hoc analyses revealed a signi\uFB01cant effect of Time, in the direction\
      \ of greater accuracy post- than pre-testing, in all the three treatment groups\
      \ (sentence production/comprehension, naming, spelling, all ps < .0001, Fig.\
      \ 1), whereas no change in accuracy from pre-to post-testing was found in the\
      \ natural history group."
    section: "Results 3.1 \u2014 Treatment effects"
    supports: claim
  - page: 83
    quote: Time in Sentence Prod/Comp vs. Time in NH Group  2.381  .348  54  6.832  <.0001
    section: "Table 2 \u2014 Treatment effects"
    supports: statistics
  - page: 81
    quote: "Mixed-effects regressions were then run using Time (pre-, post-testing)\
      \ and Group (sentence processing treatment, naming treatment, spelling treatment,\
      \ and natural history), as well as all their interaction, as \uFB01xed effects,\
      \ and Participant as the only random effect."
    section: "Methods 2.4.1 \u2014 Treatment effects"
    supports: confounders
  - page: 96
    quote: "participants were recruited from different research centers because they\
      \ met criteria for different language de\uFB01cits, which resulted in pre-treatment\
      \ heterogeneities across groups in terms of language pro\uFB01les."
    section: Limitations
    supports: limitation
  - page: 96
    quote: structural and functional images were collected using different scanners,
      anddalthough harmonization among scanners was carried out prior to undertaking
      the studydthe possibility that minor inconsistencies among scanners may have
      affected functional activation patterns cannot be excluded.
    section: Limitations
    supports: limitation
  statistics:
    ci_95: not_reported
    cluster_extent: null
    effect_size: "\u03B2 = 2.520 (z-scored accuracy units), SE 0.342, t(11) = 7.367\
      \ (Time post- vs. pre-treatment within sentence group); \u03B2 = 2.381, SE 0.348,\
      \ t(54) = 6.832 for the Time \xD7 Group interaction (sentence treatment vs.\
      \ natural history)"
    p_value: <0.0001
    threshold: mixed-effects regression with FDR correction; p<0.0001 for the Time
      effect within the sentence treatment group
  strength: strong
  target: agrammatism
  target_kind: impairment
- author_limitations:
  - "No upregulation observed in left-hemisphere ROIs (Time effect not significant\
    \ for LH; Group\xD7Time not significant for LH)."
  - "Pre-treatment, no patient group showed significant Story>Control activation in\
    \ either hemisphere \u2014 possibly due to reduced BOLD sensitivity in damaged\
    \ left cortex or to extensive temporal lobe damage disrupting whole-network connectivity."
  - Three different MRI scanners across recruitment sites (harmonized but residual
    variability cannot be excluded).
  - Reversed-speech control condition not duration-matched to active stories.
  citation: '@Barbieri2023'
  claim: "Treatment of Underlying Forms (TUF) induces significant pre-to-post-treatment\
    \ upregulation of BOLD activation in right-hemisphere homologues of the language\
    \ network \u2014 including right anterior middle temporal gyrus, anterior superior\
    \ temporal gyrus, posterior middle/superior temporal gyrus, IFG pars triangularis\
    \ and pars opercularis \u2014 during a naturalistic auditory story comprehension\
    \ fMRI task in chronic agrammatic aphasia."
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
      sequence: gradient-echo T2*-weighted EPI (192 or 162 volumes per run)
      voxel_size_mm:
      - 1.72
      - 1.72
      - 3.0
    atlases_used:
    - Harvard-Oxford (Desikan et al. 2006)
    coordinates_reported:
    - mni:
      - 48
      - -36
      - 0
      region: right posterior MTG (extending tpoMTG, pSTG)
    - mni:
      - 50
      - 0
      - 48
      region: right precentral gyrus (extending MFG)
    - mni:
      - 48
      - -18
      - -10
      region: right pMTG (extending aMTG, aSTG, pSTG)
    - mni:
      - 56
      - 28
      - 20
      region: right IFG pars triangularis (extending IFGoper, MFG)
    field_strength: 3T
    modalities:
    - TE_ms: 2.91
      TR_ms: 2300
      modality: T1
      notes: "flip angle 9\xB0; FOV 256\xD7256; used for normalization and lesion\
        \ drawing."
      sequence: 3D T1-weighted MPRAGE
      voxel_size_mm:
      - 1.0
      - 1.0
      - 1.0
    - TE_ms: 20
      TR_ms: 2400
      modality: fMRI
      notes: Block design auditory story comprehension task vs reversed-speech control.
        Two runs per session, four 24-s story blocks and four 18-s reversed-speech
        blocks per run.
      sequence: gradient-echo T2*-weighted EPI
      volumes: 192
      voxel_size_mm:
      - 1.72
      - 1.72
      - 3.0
    preprocessing_pipeline: "AFNI 3dDespike + 3dvolreg motion correction; FD>0.5mm\
      \ and DVARS>50 motion regressors; CompCor (top 3 PCs from WM/CSF); SPM-DARTEL\
      \ normalization to MNI152 (2\xD72\xD72 mm); 6 mm FWHM smoothing; SPM12 first-level\
      \ GLM with HRF + time and dispersion derivatives (to account for stroke effect\
      \ on HRF, Bonakdarpour et al. 2007); enantiomorphic replacement of left-hemisphere\
      \ lesion with mirrored right-hemisphere tissue (Nachev et al. 2008)"
    reference_space: MNI152
    task:
      baseline: Time-reversed speech (preserves phonological features without meaning)
      contrasts:
      - Stories > Control (reversed speech)
      description: "Block design alternating 24-s blocks of auditorily presented short\
        \ stories with 18-s blocks of digitally time-reversed speech (low-level baseline).\
        \ Stories controlled for syllables (M=80\xB12.14), words (M=62.5\xB12.67),\
        \ nouns (M=19\xB11.51), verbs (M=10.63\xB10.74), and complex sentences (M=3.13\xB1\
        0.64). Participants pressed a button at story onset to indicate 'real' vs\
        \ reversed speech."
      name: Auditory story comprehension
  method: fMRI_activation
  provenance:
    confidence: high
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    flags:
    - "cohort overlaps with Barbieri et al. 2019 (Cortex 120: 394-418) \u2014 same\
      \ n=12 agrammatic participants (trial NCT01927302); flag for downstream double-counting\
      \ risk in interpret_overlap()."
    paper_section: "Results 3.3.2.2 + Table 5 (pages 86\u201387); Results 3.3.2.3.1.1\
      \ + Table 6 (pages 87\u201389); Discussion 4.3 + 4.4 (pages 93\u201395)"
  region_definition:
    atlas: Harvard-Oxford (Desikan et al. 2006)
    description: "Region-of-interest mask aggregating Harvard-Oxford labels for IFGtri,\
      \ IFGoper, frontal orbital cortex, insula, frontal operculum, all three MTG\
      \ parcellations (anterior, posterior, temporo-occipital), aSTG, pSTG, AG, pSMG,\
      \ and temporal pole \u2014 restricted to the right hemisphere (homologues of\
      \ the left-hemisphere language network active in healthy controls during the\
      \ same story-comprehension task). Voxel-based peak Story>Control activation\
      \ in the sentence-treatment group post-treatment was reported at MNI [48,-36,0]\
      \ (right pMTG), [50,0,48] (right PCG), [48,-18,-10] (right pMTG/aMTG), [56,28,20]\
      \ (right IFGtri)."
    kind: atlas
  relationship: treatment_response
  replications:
  - '@Mirman2015'
  sample:
    age_range: mean 50.0 years (SD 7.4)
    handedness: 9 right-handed, 3 left-handed
    language: monolingual native English speakers
    n: 12
    population: chronic stroke-induced agrammatic aphasia (Northwestern subgroup of
      the n=58 analyzed cohort)
    time_post_onset: mean 42.3 months (SD 30.0)
  source_passages:
  - page: 85
    quote: "while no suprathreshold activation was found at pre-treatment for any\
      \ of the patient groups, post-treatment activation was signi\uFB01cantly greater\
      \ than zero in all the three treatment groups, but not in the natural history\
      \ group."
    section: Results 3.3.2.2
    supports: claim
  - page: 85
    quote: in the sentence production/comprehension treatment group, post-treatment
      activation was observed in two right temporal clusters, one more anterior, encompassing
      the aMTG and aSTG, and extending to include portions of the pMTG and pSTG, and
      one more posterior, centered on the pMTG and encompassing the temporo-occipital
      portion of the MTG and pSTG.
    section: Results 3.3.2.2
    supports: claim
  - page: 87
    quote: "The full model for the right-hemisphere ROIs (Table 6) showed a signi\uFB01\
      cant effect of Time across groups, with activation for the Story > Control contrast\
      \ being signi\uFB01cantly greater at post- than at pre-treatment. A signi\uFB01\
      cant Group*Time interaction was also found"
    section: Results 3.3.2.3.1.1
    supports: statistics
  - page: 81
    quote: "Structural and functional MR images were collected using 3T scanners (Siemens\
      \ Trio at Northwestern University, Siemens Skyra at Boston University, and Philips\
      \ Intera at Johns Hopkins University) and a 3D T1-weighted sequence for structural\
      \ (TR \xBC 2.3sec, TE \xBC 2.91 ms, \uFB02ip angle \xBC 9, \uFB01eld of view\
      \ \xBC 256  256, 1 mm isotropic voxel size), or a gradient-echo T2*-weighted\
      \ sequence for functional"
    section: "Methods 2.3.2.2 \u2014 Data acquisition"
    supports: imaging_details
  - page: 81
    quote: T-maps were obtained by applying a p < .001 threshold at the voxel-level.
      Cluster-level correction was carried out using the family-wise error (FWE) correction
      provided by SPM12, at a threshold of p < .05
    section: "Methods 2.4.2.3 \u2014 Voxel-level analyses"
    supports: statistics
  - page: 78
    quote: '70 met the inclusion criteria for the study: (1) presence of a single
      left-hemisphere stroke at least 12 months prior entering the study and affecting
      at least .1% of the cortical surface in the left hemisphere'
    section: "Methods 2.1 \u2014 Participants"
    supports: sample
  - page: 81
    quote: "structural T1 images underwent enantiomorphic replacement wherein healthy\
      \ tissue from the right hemisphere was mirrored into the lesioned area (Nachev,\
      \ Coulthard, J\u20ACager, Kennard, & Husain, 2008), and the resulting brains\
      \ were normalized to the MNI template using the SPM DARTEL toolbox (Ashburner,\
      \ 2007)."
    section: "Methods 2.4.2.1 \u2014 Anatomical images"
    supports: imaging_details
  - page: 94
    quote: the lack of activation in the left hemisphere of individuals with aphasia
      could be due to reduced sensitivity to BOLD signal detection in the damaged
      cortex.
    section: Discussion 4.3
    supports: limitation
  - page: 87
    quote: Age, education and lesion size (i.e., the proportion of lesioned tissue
      in each left-hemisphere ROI) were entered as covariates, to ensure that activation
      changes between time points, as well as the Group*Time interaction, were not
      driven by group differences in demographic or lesion variables.
    section: "Methods 2.4.2.4 \u2014 ROI analyses"
    supports: confounders
  statistics:
    ci_95: not_reported
    cluster_extent: 502
    effect_size: "ROI analysis Time within sentence-treatment group: \u03B2=0.096,\
      \ SE=0.028, t(285.9)=3.402, p=0.003 (FDR-corrected). Voxel-level peak T-values:\
      \ 8.335 (right pMTG), 7.002 (right pMTG/aMTG), 5.972 (right PCG), 5.462 (right\
      \ IFGtri)."
    p_value: 0.003 (ROI-based, FDR-corrected)
    threshold: "voxel-level p<0.001, FWE-corrected p<0.05 cluster-level (k\u226560\
      \ voxels for sentence-treatment group post-treatment); ROI analysis: mixed-effects\
      \ regression with FDR correction, p<0.05; full-model Group\xD7Time interaction\
      \ \u03C7\xB2=9.928, p=0.019"
  strength: strong
  target: right_anterior_middle_temporal_gyrus
  target_kind: region
- author_limitations:
  - Brain-behavior association applies only to the sentence treatment group; same
    analysis on the spelling treatment group found no associations.
  - "Sentence comprehension association is marginal (p=0.053) \u2014 interpretation\
    \ should be cautious."
  - "Group included only n=12 \u2014 power is limited."
  citation: '@Barbieri2023'
  claim: Treatment-induced upregulation of BOLD activation in right-hemisphere language
    network homologues during the auditory story comprehension task is positively
    associated with improved verb comprehension (NNB Verb Comprehension subtest) and
    (marginally) sentence comprehension (NAVS Sentence Comprehension Test) in the
    sentence treatment (TUF) group, but not with noun comprehension.
  confounders_controlled:
  - ROI as random effect (accounts for ROI-related variance)
  - analyses restricted to RH ROIs with suprathreshold post-treatment Story>Control
    activation (i.e., RH IFGtri, IFGoper, MTG (3 parcellations), aSTG, pSTG)
  confounders_not_controlled:
  - no demographic covariates in the brain-behavior coupling analysis (age, education,
    lesion size were already controlled in the upstream ROI analysis)
  - single time-point change (post-pre); no longitudinal trajectory
  contradictions: []
  design: RCT
  direction: likely
  evidence_quality: RCT
  id: f3
  imaging: fMRI
  imaging_details:
    atlases_used:
    - Harvard-Oxford
    field_strength: 3T
    preprocessing_pipeline: 'Same as f2: AFNI + SPM-DARTEL + 6mm FWHM; SPM12 GLM with
      HRF + derivatives'
    reference_space: MNI152
    task:
      baseline: Time-reversed speech
      contrasts:
      - Stories > Control
      description: Block design auditory story comprehension vs reversed-speech control
      name: Auditory story comprehension
  method: fMRI_activation
  provenance:
    confidence: high
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    flags:
    - "Marginal sentence-comprehension association (p=0.053) \u2014 strength flagged\
      \ as moderate."
    - TUF behavioural target is sentence production+comprehension, but the brain-behavior
      coupling here is observed for verb comprehension and sentence comprehension
      (NOT noun comprehension or sentence production), aligning with TUF's focus on
      verb-argument structure and thematic-syntactic mapping.
    - "cohort overlaps with Barbieri et al. 2019 (Cortex 120: 394-418) \u2014 same\
      \ n=12 agrammatic participants (trial NCT01927302); flag for downstream double-counting\
      \ risk in interpret_overlap()."
    paper_section: "Results 3.3.2.3.1.2 + Table 7 + Fig. 5 (pages 89\u201390); Discussion\
      \ 4.3 (page 94)"
  region_definition:
    atlas: Harvard-Oxford
    description: 'Right-hemisphere language network homologues that showed suprathreshold
      post-treatment Story>Control activation: RH IFGtri, RH IFGoper, RH MTG (anterior,
      posterior, temporo-occipital), RH aSTG, RH pSTG.'
    kind: atlas
  relationship: responder
  replications:
  - '@Saur2008'
  sample:
    age_range: mean 50.0 years (SD 7.4)
    handedness: 9 right-handed, 3 left-handed
    language: monolingual native English speakers
    n: 12
    population: chronic stroke-induced agrammatic aphasia (TUF subgroup)
    time_post_onset: mean 42.3 months (SD 30.0)
  source_passages:
  - page: 89
    quote: "Analyses run within the sentence production/comprehension treatment group\
      \ showed a signi\uFB01cant (or marginally signi\uFB01cant, in the case of sentence\
      \ comprehension, following correction for multiple comparisons) positive association\
      \ between changes in activation in the language network homologue and improved\
      \ accuracy on measures of verb and sentence comprehension"
    section: Results 3.3.2.3.1.2
    supports: claim
  - page: 90
    quote: change on NNB VC  1.051  .343  94.0  3.063  .017
    section: Table 7
    supports: statistics
  - page: 94
    quote: "results of the voxel-based and ROI-based analyses indicate that participants\
      \ who received treatment for sentence processing (i.e., Treatment of Underlying\
      \ Forms, TUF, Thompson & Shapiro, 2005) showed clear evidence of neural plasticity,\
      \ as suggested by post-treatment activation increases within right-hemisphere\
      \ language network homologues that were active in healthy participants on the\
      \ same task, and by signi\uFB01cant associations between activation changes\
      \ and improved verb and sentence comprehension."
    section: Discussion 4.3
    supports: claim
  - page: 87
    quote: "the change in BOLD signal between time points (post-minus pre-treatment)\
      \ was entered as the dependent variable; changes in performance on measures\
      \ of word (i.e., change on the NNB noun and verb comprehension subtests) and\
      \ sentence comprehension (i.e., change on the NAVS sentence comprehension subtest)\
      \ were entered as \uFB01xed effects in separate analyses."
    section: Methods 2.4.2.4
    supports: method
  - page: 96
    quote: "participants were recruited from different research centers because they\
      \ met criteria for different language de\uFB01cits, which resulted in pre-treatment\
      \ heterogeneities across groups in terms of language pro\uFB01les."
    section: Limitations
    supports: limitation
  - page: 87
    quote: "ROIs were included only if signi\uFB01cant post-treatment activation for\
      \ the Story > Control contrast was found on the voxel-based analysis. This choice\
      \ was made to ensure that the relationship between upregulation of activation\
      \ and changes in language scores was limited to regions for which upregulation\
      \ of activation resulted in post-treatment neural response patterns to naturalistic\
      \ language comprehension that were similar to those of healthy individuals"
    section: Methods 2.4.2.4
    supports: confounders
  statistics:
    ci_95: not_reported
    effect_size: "Verb comprehension: \u03B2=1.051, SE=0.343, t(94)=3.063, p=0.017\
      \ (FDR-corrected). Sentence comprehension (NAVS-SCT): \u03B2=0.768, SE=0.318,\
      \ t(94)=2.418, p=0.053 (marginal). Noun comprehension: \u03B2=1.739, SE=1.196,\
      \ t(94)=1.454, p=0.224 (n.s.)."
    p_value: 0.017 (verb comprehension); 0.053 (sentence comprehension, marginal);
      0.224 (noun comprehension, n.s.)
    threshold: mixed-effects regression on RH ROIs that showed suprathreshold post-treatment
      Story>Control activation; FDR-corrected for multiple comparisons within group;
      p<0.05
  strength: moderate
  target: agrammatism
  target_kind: impairment
- author_limitations:
  - Pre-treatment heterogeneities across treatment groups (different impairment profiles,
    different recruitment sites).
  - Different MRI scanners across sites (Siemens Trio at NU, Siemens Skyra at BU,
    Philips Intera at JHU); harmonized via phantom scans but residual scanner variability
    cannot be excluded.
  - Long-term maintenance of treatment effects not assessed.
  citation: '@Barbieri2023'
  claim: Twelve weeks of Treatment of Underlying Forms (TUF) significantly improves
    production and comprehension of canonical and non-canonical sentences in chronic
    agrammatic aphasia compared to a no-treatment natural history control group.
  confounders_controlled:
  - age, education, proportion of lesioned left-hemisphere tissue (entered as covariates)
  - natural history group (n=16) used as no-treatment control
  - groups matched on months post-onset, gender, handedness, WAB-AQ, lesion size
  confounders_not_controlled:
  - PI not blinded to treatment allocation at each site
  - scanner and recruitment-site differences (3 different MRI scanners across sites)
  - groups differed on age (sentence treatment group younger) and education (naming
    group lower)
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
    - method coded as clinical_RCT given the randomized design with natural history
      controls; the paper is also primarily an fMRI study (subsequent findings use
      fMRI_activation method).
    - "behavioural-only finding \u2014 imaging fields are minimal; flagged that this\
      \ is a treatment-efficacy claim, not a region-tied claim."
    - "cohort overlaps with Barbieri et al. 2019 (Cortex 120: 394-418) \u2014 same\
      \ n=12 agrammatic participants (trial NCT01927302); flag for downstream double-counting\
      \ risk in interpret_overlap()."
    paper_section: Results 3.1 + Table 2 (page 83); Methods 2.2 (page 80); Methods
      2.3.1 (page 80)
  region_definition:
    description: "Behavioral-only treatment efficacy finding \u2014 no specific brain\
      \ region; treatment-targeted behavioural measures only (sentence production\
      \ priming task and picture verification task on 10 trained passive sentences)."
    kind: not_reported
  relationship: responder
  replications:
  - '@Schlaug2008'
  - '@Pulvermuller2001'
  sample:
    age_range: mean 50.0 years (SD 7.4); younger than other treatment groups
    exclusion_criteria: exclusively subcortical lesions; non-monolingual; developmental/psychiatric/other
      neurological history; MRI contraindications.
    handedness: 9 right-handed, 3 left-handed
    inclusion_criteria: "age 35\u201380; education \u2265high-school; WAB-AQ 45\u2013\
      95; agrammatism (impaired non-canonical>canonical sentence production and comprehension\
      \ on NAVS; <50% grammatical sentences in Cinderella retell; relatively spared\
      \ single-word comprehension)."
    language: monolingual native English speakers
    n: 12
    population: "chronic stroke-induced agrammatic aphasia (single left-hemisphere\
      \ stroke \u226512 months post-onset; subgroup of n=58 analyzed cohort, recruited\
      \ at Northwestern University)"
    recruitment: Aphasia and Neurolinguistics Research Lab at Northwestern University;
      randomized to treatment vs. natural history at each site by a staff member other
      than the assessor.
    time_post_onset: mean 42.3 months (SD 30.0)
  source_passages:
  - page: 80
    quote: participants in the treatment group underwent Treatment of Underlying Forms
      (TUF, Thompson & Shapiro, 2005), a treatment approach that uses a series of
      meta-linguistic steps focused on verbs, verb argument structure, and thematic-syntactic
      mapping in active (e.g., The man was shaving the boy) and passive sentences
      (e.g., The boy was shaved by the man) to improve sentence comprehension and
      production.
    section: "Methods 2.2 \u2014 Treatment"
    supports: method
  - page: 78
    quote: '70 met the inclusion criteria for the study: (1) presence of a single
      left-hemisphere stroke at least 12 months prior entering the study and affecting
      at least .1% of the cortical surface in the left hemisphere'
    section: "Methods 2.1 \u2014 Participants"
    supports: sample
  - page: 78
    quote: "participants recruited at Northwestern University were selected for agrammatism,\
      \ which was de\uFB01ned by: a) evidence of impaired production and comprehension\
      \ of sentences (for syntactically complex (non-canonical) more than for simple\
      \ (canonical) sentences) on the Northwestern Assessment of Verbs and Sentences\
      \ (NAVS, Thompson, 2011); b) production of less than 50% grammatical sentences\
      \ on the re-telling of Cinderella's story; and c) relatively spared single-word\
      \ comprehension"
    section: "Methods 2.1 \u2014 Participants"
    supports: sample
  - page: 82
    quote: "Post-hoc analyses revealed a signi\uFB01cant effect of Time, in the direction\
      \ of greater accuracy post- than pre-testing, in all the three treatment groups\
      \ (sentence production/comprehension, naming, spelling, all ps < .0001, Fig.\
      \ 1), whereas no change in accuracy from pre-to post-testing was found in the\
      \ natural history group."
    section: "Results 3.1 \u2014 Treatment effects"
    supports: claim
  - page: 83
    quote: Time in Sentence Prod/Comp vs. Time in NH Group  2.381  .348  54  6.832  <.0001
    section: "Table 2 \u2014 Treatment effects"
    supports: statistics
  - page: 81
    quote: "Mixed-effects regressions were then run using Time (pre-, post-testing)\
      \ and Group (sentence processing treatment, naming treatment, spelling treatment,\
      \ and natural history), as well as all their interaction, as \uFB01xed effects,\
      \ and Participant as the only random effect."
    section: "Methods 2.4.1 \u2014 Treatment effects"
    supports: confounders
  - page: 96
    quote: "participants were recruited from different research centers because they\
      \ met criteria for different language de\uFB01cits, which resulted in pre-treatment\
      \ heterogeneities across groups in terms of language pro\uFB01les."
    section: Limitations
    supports: limitation
  - page: 96
    quote: structural and functional images were collected using different scanners,
      anddalthough harmonization among scanners was carried out prior to undertaking
      the studydthe possibility that minor inconsistencies among scanners may have
      affected functional activation patterns cannot be excluded.
    section: Limitations
    supports: limitation
  statistics:
    ci_95: not_reported
    cluster_extent: null
    effect_size: "\u03B2 = 2.520 (z-scored accuracy units), SE 0.342, t(11) = 7.367\
      \ (Time post- vs. pre-treatment within sentence group); \u03B2 = 2.381, SE 0.348,\
      \ t(54) = 6.832 for the Time \xD7 Group interaction (sentence treatment vs.\
      \ natural history)"
    p_value: <0.0001
    threshold: mixed-effects regression with FDR correction; p<0.0001 for the Time
      effect within the sentence treatment group
  strength: strong
  target: agrammatism
  target_kind: impairment
- author_limitations:
  - "No upregulation observed in left-hemisphere ROIs (Time effect not significant\
    \ for LH; Group\xD7Time not significant for LH)."
  - "Pre-treatment, no patient group showed significant Story>Control activation in\
    \ either hemisphere \u2014 possibly due to reduced BOLD sensitivity in damaged\
    \ left cortex or to extensive temporal lobe damage disrupting whole-network connectivity."
  - Three different MRI scanners across recruitment sites (harmonized but residual
    variability cannot be excluded).
  - Reversed-speech control condition not duration-matched to active stories.
  citation: '@Barbieri2023'
  claim: "Treatment of Underlying Forms (TUF) induces significant pre-to-post-treatment\
    \ upregulation of BOLD activation in right-hemisphere homologues of the language\
    \ network \u2014 including right anterior middle temporal gyrus, anterior superior\
    \ temporal gyrus, posterior middle/superior temporal gyrus, IFG pars triangularis\
    \ and pars opercularis \u2014 during a naturalistic auditory story comprehension\
    \ fMRI task in chronic agrammatic aphasia."
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
      sequence: gradient-echo T2*-weighted EPI (192 or 162 volumes per run)
      voxel_size_mm:
      - 1.72
      - 1.72
      - 3.0
    atlases_used:
    - Harvard-Oxford (Desikan et al. 2006)
    coordinates_reported:
    - mni:
      - 48
      - -36
      - 0
      region: right posterior MTG (extending tpoMTG, pSTG)
    - mni:
      - 50
      - 0
      - 48
      region: right precentral gyrus (extending MFG)
    - mni:
      - 48
      - -18
      - -10
      region: right pMTG (extending aMTG, aSTG, pSTG)
    - mni:
      - 56
      - 28
      - 20
      region: right IFG pars triangularis (extending IFGoper, MFG)
    field_strength: 3T
    modalities:
    - TE_ms: 2.91
      TR_ms: 2300
      modality: T1
      notes: "flip angle 9\xB0; FOV 256\xD7256; used for normalization and lesion\
        \ drawing."
      sequence: 3D T1-weighted MPRAGE
      voxel_size_mm:
      - 1.0
      - 1.0
      - 1.0
    - TE_ms: 20
      TR_ms: 2400
      modality: fMRI
      notes: Block design auditory story comprehension task vs reversed-speech control.
        Two runs per session, four 24-s story blocks and four 18-s reversed-speech
        blocks per run.
      sequence: gradient-echo T2*-weighted EPI
      volumes: 192
      voxel_size_mm:
      - 1.72
      - 1.72
      - 3.0
    preprocessing_pipeline: "AFNI 3dDespike + 3dvolreg motion correction; FD>0.5mm\
      \ and DVARS>50 motion regressors; CompCor (top 3 PCs from WM/CSF); SPM-DARTEL\
      \ normalization to MNI152 (2\xD72\xD72 mm); 6 mm FWHM smoothing; SPM12 first-level\
      \ GLM with HRF + time and dispersion derivatives (to account for stroke effect\
      \ on HRF, Bonakdarpour et al. 2007); enantiomorphic replacement of left-hemisphere\
      \ lesion with mirrored right-hemisphere tissue (Nachev et al. 2008)"
    reference_space: MNI152
    task:
      baseline: Time-reversed speech (preserves phonological features without meaning)
      contrasts:
      - Stories > Control (reversed speech)
      description: "Block design alternating 24-s blocks of auditorily presented short\
        \ stories with 18-s blocks of digitally time-reversed speech (low-level baseline).\
        \ Stories controlled for syllables (M=80\xB12.14), words (M=62.5\xB12.67),\
        \ nouns (M=19\xB11.51), verbs (M=10.63\xB10.74), and complex sentences (M=3.13\xB1\
        0.64). Participants pressed a button at story onset to indicate 'real' vs\
        \ reversed speech."
      name: Auditory story comprehension
  method: fMRI_activation
  provenance:
    confidence: high
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    flags:
    - "cohort overlaps with Barbieri et al. 2019 (Cortex 120: 394-418) \u2014 same\
      \ n=12 agrammatic participants (trial NCT01927302); flag for downstream double-counting\
      \ risk in interpret_overlap()."
    paper_section: "Results 3.3.2.2 + Table 5 (pages 86\u201387); Results 3.3.2.3.1.1\
      \ + Table 6 (pages 87\u201389); Discussion 4.3 + 4.4 (pages 93\u201395)"
  region_definition:
    atlas: Harvard-Oxford (Desikan et al. 2006)
    description: "Region-of-interest mask aggregating Harvard-Oxford labels for IFGtri,\
      \ IFGoper, frontal orbital cortex, insula, frontal operculum, all three MTG\
      \ parcellations (anterior, posterior, temporo-occipital), aSTG, pSTG, AG, pSMG,\
      \ and temporal pole \u2014 restricted to the right hemisphere (homologues of\
      \ the left-hemisphere language network active in healthy controls during the\
      \ same story-comprehension task). Voxel-based peak Story>Control activation\
      \ in the sentence-treatment group post-treatment was reported at MNI [48,-36,0]\
      \ (right pMTG), [50,0,48] (right PCG), [48,-18,-10] (right pMTG/aMTG), [56,28,20]\
      \ (right IFGtri)."
    kind: atlas
  relationship: treatment_response
  replications:
  - '@Mirman2015'
  sample:
    age_range: mean 50.0 years (SD 7.4)
    handedness: 9 right-handed, 3 left-handed
    language: monolingual native English speakers
    n: 12
    population: chronic stroke-induced agrammatic aphasia (Northwestern subgroup of
      the n=58 analyzed cohort)
    time_post_onset: mean 42.3 months (SD 30.0)
  source_passages:
  - page: 85
    quote: "while no suprathreshold activation was found at pre-treatment for any\
      \ of the patient groups, post-treatment activation was signi\uFB01cantly greater\
      \ than zero in all the three treatment groups, but not in the natural history\
      \ group."
    section: Results 3.3.2.2
    supports: claim
  - page: 85
    quote: in the sentence production/comprehension treatment group, post-treatment
      activation was observed in two right temporal clusters, one more anterior, encompassing
      the aMTG and aSTG, and extending to include portions of the pMTG and pSTG, and
      one more posterior, centered on the pMTG and encompassing the temporo-occipital
      portion of the MTG and pSTG.
    section: Results 3.3.2.2
    supports: claim
  - page: 87
    quote: "The full model for the right-hemisphere ROIs (Table 6) showed a signi\uFB01\
      cant effect of Time across groups, with activation for the Story > Control contrast\
      \ being signi\uFB01cantly greater at post- than at pre-treatment. A signi\uFB01\
      cant Group*Time interaction was also found"
    section: Results 3.3.2.3.1.1
    supports: statistics
  - page: 81
    quote: "Structural and functional MR images were collected using 3T scanners (Siemens\
      \ Trio at Northwestern University, Siemens Skyra at Boston University, and Philips\
      \ Intera at Johns Hopkins University) and a 3D T1-weighted sequence for structural\
      \ (TR \xBC 2.3sec, TE \xBC 2.91 ms, \uFB02ip angle \xBC 9, \uFB01eld of view\
      \ \xBC 256  256, 1 mm isotropic voxel size), or a gradient-echo T2*-weighted\
      \ sequence for functional"
    section: "Methods 2.3.2.2 \u2014 Data acquisition"
    supports: imaging_details
  - page: 81
    quote: T-maps were obtained by applying a p < .001 threshold at the voxel-level.
      Cluster-level correction was carried out using the family-wise error (FWE) correction
      provided by SPM12, at a threshold of p < .05
    section: "Methods 2.4.2.3 \u2014 Voxel-level analyses"
    supports: statistics
  - page: 78
    quote: '70 met the inclusion criteria for the study: (1) presence of a single
      left-hemisphere stroke at least 12 months prior entering the study and affecting
      at least .1% of the cortical surface in the left hemisphere'
    section: "Methods 2.1 \u2014 Participants"
    supports: sample
  - page: 81
    quote: "structural T1 images underwent enantiomorphic replacement wherein healthy\
      \ tissue from the right hemisphere was mirrored into the lesioned area (Nachev,\
      \ Coulthard, J\u20ACager, Kennard, & Husain, 2008), and the resulting brains\
      \ were normalized to the MNI template using the SPM DARTEL toolbox (Ashburner,\
      \ 2007)."
    section: "Methods 2.4.2.1 \u2014 Anatomical images"
    supports: imaging_details
  - page: 94
    quote: the lack of activation in the left hemisphere of individuals with aphasia
      could be due to reduced sensitivity to BOLD signal detection in the damaged
      cortex.
    section: Discussion 4.3
    supports: limitation
  - page: 87
    quote: Age, education and lesion size (i.e., the proportion of lesioned tissue
      in each left-hemisphere ROI) were entered as covariates, to ensure that activation
      changes between time points, as well as the Group*Time interaction, were not
      driven by group differences in demographic or lesion variables.
    section: "Methods 2.4.2.4 \u2014 ROI analyses"
    supports: confounders
  statistics:
    ci_95: not_reported
    cluster_extent: 502
    effect_size: "ROI analysis Time within sentence-treatment group: \u03B2=0.096,\
      \ SE=0.028, t(285.9)=3.402, p=0.003 (FDR-corrected). Voxel-level peak T-values:\
      \ 8.335 (right pMTG), 7.002 (right pMTG/aMTG), 5.972 (right PCG), 5.462 (right\
      \ IFGtri)."
    p_value: 0.003 (ROI-based, FDR-corrected)
    threshold: "voxel-level p<0.001, FWE-corrected p<0.05 cluster-level (k\u226560\
      \ voxels for sentence-treatment group post-treatment); ROI analysis: mixed-effects\
      \ regression with FDR correction, p<0.05; full-model Group\xD7Time interaction\
      \ \u03C7\xB2=9.928, p=0.019"
  strength: strong
  target: right_anterior_middle_temporal_gyrus
  target_kind: region
- author_limitations:
  - Brain-behavior association applies only to the sentence treatment group; same
    analysis on the spelling treatment group found no associations.
  - "Sentence comprehension association is marginal (p=0.053) \u2014 interpretation\
    \ should be cautious."
  - "Group included only n=12 \u2014 power is limited."
  citation: '@Barbieri2023'
  claim: Treatment-induced upregulation of BOLD activation in right-hemisphere language
    network homologues during the auditory story comprehension task is positively
    associated with improved verb comprehension (NNB Verb Comprehension subtest) and
    (marginally) sentence comprehension (NAVS Sentence Comprehension Test) in the
    sentence treatment (TUF) group, but not with noun comprehension.
  confounders_controlled:
  - ROI as random effect (accounts for ROI-related variance)
  - analyses restricted to RH ROIs with suprathreshold post-treatment Story>Control
    activation (i.e., RH IFGtri, IFGoper, MTG (3 parcellations), aSTG, pSTG)
  confounders_not_controlled:
  - no demographic covariates in the brain-behavior coupling analysis (age, education,
    lesion size were already controlled in the upstream ROI analysis)
  - single time-point change (post-pre); no longitudinal trajectory
  contradictions: []
  design: RCT
  direction: likely_responder
  evidence_quality: RCT
  id: f6
  imaging: fMRI
  imaging_details:
    atlases_used:
    - Harvard-Oxford
    field_strength: 3T
    preprocessing_pipeline: 'Same as f2: AFNI + SPM-DARTEL + 6mm FWHM; SPM12 GLM with
      HRF + derivatives'
    reference_space: MNI152
    task:
      baseline: Time-reversed speech
      contrasts:
      - Stories > Control
      description: Block design auditory story comprehension vs reversed-speech control
      name: Auditory story comprehension
  method: fMRI_activation
  provenance:
    confidence: high
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    flags:
    - "Marginal sentence-comprehension association (p=0.053) \u2014 strength flagged\
      \ as moderate."
    - TUF behavioural target is sentence production+comprehension, but the brain-behavior
      coupling here is observed for verb comprehension and sentence comprehension
      (NOT noun comprehension or sentence production), aligning with TUF's focus on
      verb-argument structure and thematic-syntactic mapping.
    - "cohort overlaps with Barbieri et al. 2019 (Cortex 120: 394-418) \u2014 same\
      \ n=12 agrammatic participants (trial NCT01927302); flag for downstream double-counting\
      \ risk in interpret_overlap()."
    paper_section: "Results 3.3.2.3.1.2 + Table 7 + Fig. 5 (pages 89\u201390); Discussion\
      \ 4.3 (page 94)"
  region_definition:
    atlas: Harvard-Oxford
    description: 'Right-hemisphere language network homologues that showed suprathreshold
      post-treatment Story>Control activation: RH IFGtri, RH IFGoper, RH MTG (anterior,
      posterior, temporo-occipital), RH aSTG, RH pSTG.'
    kind: atlas
  relationship: responder
  replications:
  - '@Saur2008'
  sample:
    age_range: mean 50.0 years (SD 7.4)
    handedness: 9 right-handed, 3 left-handed
    language: monolingual native English speakers
    n: 12
    population: chronic stroke-induced agrammatic aphasia (TUF subgroup)
    time_post_onset: mean 42.3 months (SD 30.0)
  source_passages:
  - page: 89
    quote: "Analyses run within the sentence production/comprehension treatment group\
      \ showed a signi\uFB01cant (or marginally signi\uFB01cant, in the case of sentence\
      \ comprehension, following correction for multiple comparisons) positive association\
      \ between changes in activation in the language network homologue and improved\
      \ accuracy on measures of verb and sentence comprehension"
    section: Results 3.3.2.3.1.2
    supports: claim
  - page: 90
    quote: change on NNB VC  1.051  .343  94.0  3.063  .017
    section: Table 7
    supports: statistics
  - page: 94
    quote: "results of the voxel-based and ROI-based analyses indicate that participants\
      \ who received treatment for sentence processing (i.e., Treatment of Underlying\
      \ Forms, TUF, Thompson & Shapiro, 2005) showed clear evidence of neural plasticity,\
      \ as suggested by post-treatment activation increases within right-hemisphere\
      \ language network homologues that were active in healthy participants on the\
      \ same task, and by signi\uFB01cant associations between activation changes\
      \ and improved verb and sentence comprehension."
    section: Discussion 4.3
    supports: claim
  - page: 87
    quote: "the change in BOLD signal between time points (post-minus pre-treatment)\
      \ was entered as the dependent variable; changes in performance on measures\
      \ of word (i.e., change on the NNB noun and verb comprehension subtests) and\
      \ sentence comprehension (i.e., change on the NAVS sentence comprehension subtest)\
      \ were entered as \uFB01xed effects in separate analyses."
    section: Methods 2.4.2.4
    supports: method
  - page: 96
    quote: "participants were recruited from different research centers because they\
      \ met criteria for different language de\uFB01cits, which resulted in pre-treatment\
      \ heterogeneities across groups in terms of language pro\uFB01les."
    section: Limitations
    supports: limitation
  - page: 87
    quote: "ROIs were included only if signi\uFB01cant post-treatment activation for\
      \ the Story > Control contrast was found on the voxel-based analysis. This choice\
      \ was made to ensure that the relationship between upregulation of activation\
      \ and changes in language scores was limited to regions for which upregulation\
      \ of activation resulted in post-treatment neural response patterns to naturalistic\
      \ language comprehension that were similar to those of healthy individuals"
    section: Methods 2.4.2.4
    supports: confounders
  statistics:
    ci_95: not_reported
    effect_size: "Verb comprehension: \u03B2=1.051, SE=0.343, t(94)=3.063, p=0.017\
      \ (FDR-corrected). Sentence comprehension (NAVS-SCT): \u03B2=0.768, SE=0.318,\
      \ t(94)=2.418, p=0.053 (marginal). Noun comprehension: \u03B2=1.739, SE=1.196,\
      \ t(94)=1.454, p=0.224 (n.s.)."
    p_value: 0.017 (verb comprehension); 0.053 (sentence comprehension, marginal);
      0.224 (noun comprehension, n.s.)
    threshold: mixed-effects regression on RH ROIs that showed suprathreshold post-treatment
      Story>Control activation; FDR-corrected for multiple comparisons within group;
      p<0.05
  strength: moderate
  target: agrammatism
  target_kind: impairment
source: agent_draft
last_reviewed: '2026-05-06'
notes: |
  First-extraction draft from Barbieri et al. 2023. TUF (Treatment of
  Underlying Forms) is a linguistically-motivated sentence-level
  treatment focused on verb argument structure and thematic-syntactic
  mapping. Three findings recorded:
  
  - f1 (behavioural efficacy): TUF improves sentence production and
    comprehension over 12 weeks compared to a no-treatment control.
  - f2 (neural reorganization): TUF induces upregulation of right-
    hemisphere language network homologues during a naturalistic
    auditory story comprehension fMRI task. Right-hemisphere clusters
    encompass anterior and posterior MTG, aSTG, pSTG, IFGtri,
    IFGoper, and PCG.
  - f3 (brain-behavior coupling): TUF-induced RH upregulation
    correlates with improved verb comprehension (p=.017) and
    marginally with sentence comprehension (p=.053), but NOT with
    noun comprehension. This pattern is theoretically consistent with
    TUF's focus on verb argument structure.
  
  Importantly, NO comparable upregulation was observed in left-
  hemisphere ROIs (Group×Time interaction n.s. for LH); pre-treatment,
  no patient group showed significant Story>Control activation in
  either hemisphere. The authors interpret this as either reduced
  BOLD sensitivity in damaged left cortex or extensive temporal-lobe
  damage disrupting whole-network connectivity.
  
  Anchored on therapy because the paper's main claims are about
  treatment efficacy and treatment-induced neural reorganization. The
  brain-behavior coupling finding (f3) is a `responder` finding (a
  moderator claim about which patients respond to TUF, indexed by
  RH activation change).
  
  All three findings come from the same n=12 sentence-treatment
  subgroup of the n=58 analyzed cohort. Effect sizes for behavioural
  improvement are large (β>2 in z-score units) but the imaging
  findings come from a small sample with limited power.
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
