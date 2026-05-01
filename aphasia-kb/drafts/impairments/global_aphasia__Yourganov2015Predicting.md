---
schema_version: 2.3
id: global_aphasia
name: "Global aphasia"
kind: impairment
status: draft
created_by: "agent:claude-opus-4-7"
created_on: 2026-05-01
short_definition: "The most severe aphasia syndrome, characterized by profoundly impaired comprehension and production across all language modalities, often with spared automatic speech. Associated with extensive cortical damage in the territory supplied by the middle cerebral artery, typically encompassing both Broca's and Wernicke's areas."
assessment:
  - "Western Aphasia Battery (WAB / WAB-R)"
  - "Boston Diagnostic Aphasia Examination (BDAE)"

findings:
  - id: f1
    target: left_middle_frontal_gyrus
    target_kind: region
    claim: "Damage to the left middle frontal gyrus is the strongest predictor of global aphasia in a multivariate SVM classification (predictive relevance Z = 2.51)."
    direction: likely
    relationship: causal
    citation: "@Yourganov2015Predicting"
    method: MLPA
    design: cross-sectional
    imaging: T1
    sample:
      n: 98
      population: "chronic left-hemisphere stroke patients with aphasia (global subgroup n=10)"
      time_post_onset: ">=6 months post-stroke; mean 40.1 months (SD 49.6, range 6–276)"
      age_range: "mean 58 years (SD 11.9, range 31–80)"
      handedness: "all right-handed"
      language: "English (recruited in South Carolina, USA)"
      recruitment: "referrals from local neurologists and print/radio advertisements; behavioural assessment May 2007–Oct 2014 at the University of South Carolina."
      inclusion_criteria: "right-handed; chronic left-hemisphere stroke; aphasia present"
      exclusion_criteria: "absence of aphasia; MRI contraindications; apraxia-of-speech-driven deficit; bilateral lesion; multiple sclerosis."
    statistics:
      threshold: "binomial-distribution test, FDR-corrected (p<0.05)"
      effect_size: "predictive relevance Z = 2.51 (Table 3)"
      ci_95: "not_reported"
      p_value: "not_reported per-region"
    confounders_controlled:
      - "balanced training set via resampling"
      - "8-fold CV for SVM hyperparameters"
    confounders_not_controlled:
      - "lesion volume (global aphasia patients have systematically larger lesions; this is not regressed out)"
      - "age / time post-stroke"
      - "WAB-defined aphasia types (categorical thresholding)"
    region_definition:
      kind: atlas
      atlas: "AAL"
      description: "Left middle frontal gyrus as defined by AAL — the cortex between superior and inferior frontal sulci, dorsolateral prefrontal cortex."
    imaging_details:
      field_strength: "3T"
      modalities:
        - modality: "T1"
          sequence: "MP-RAGE"
          voxel_size_mm: [1, 1, 1]
          TR_ms: 2250
          TI_ms: 900
          TE_ms: 4.52
          notes: "First 25 patients used 160-slice sequence (TI=900, TE=4.52); subsequent 72 patients used 192-slice sequence (TI=925, TE=4.15) with GRAPPA=2."
        - modality: "T2"
          sequence: "3D-SPACE"
          TR_ms: 2800
          TE_ms: 402
          notes: "Lesions manually drawn on the T2 image by a trained neurologist; resliced to T1 native space; smoothed (3mm FWHM)."
      preprocessing_pipeline: "Enantiomorphic normalization (Nachev et al., 2008) using SPM12 unified segmentation + Clinical Toolbox (Rorden et al., 2012); lesion binarized at 50% probability after warping."
      reference_space: "MNI152"
      atlases_used:
        - "Speculative Brodmann (82 areas)"
        - "JHU/Faria 2012 (189 areas)"
        - "AAL (Tzourio-Mazoyer 2002; 116 areas)"
        - "Catani–Thiebaut de Schotten 2008 (CTS; 34 white-matter tracts)"
        - "AALCTS (custom union; 150 areas)"
    replications: []
    contradictions: []
    author_limitations:
      - "Global vs Broca's aphasia could not be classified above chance with any atlas (Table 1) — extensive lesion overlap between the two non-fluent syndromes."
      - "Global aphasia often resolves to Broca's during recovery (Pedersen 2003) — the two syndromes may represent stages of the same process rather than distinct conditions."
    evidence_quality: cohort
    strength: strong
    provenance:
      extracted_by: "agent:claude-opus-4-7"
      extracted_on: 2026-05-01
      paper_section: "Results page 12; Table 3 (Global column); Discussion page 12–13"
      confidence: high
      flags:
        - "cohort overlaps with @Fridriksson2018 (same USC registry); flag for downstream double-counting risk in interpret_overlap()."
        - "Global aphasia patients have systematically larger lesions; without lesion-volume control, the multivariate classifier may be partially detecting 'big lesion' rather than 'global-syndrome-specific pattern'."
    source_passages:
      - section: "Results"
        page: 12
        supports: claim
        quote: "Global aphasia is associated with extensive cortical damage. Middle and inferior frontal gyri, temporal regions (temporal pole; Heschl's and superior temporal gyri), insula and rolandic operculum, pre- and postcentral gyri, and putamen all had high predictive relevance for global aphasia."
      - section: "Methods 2.1 — Participants"
        page: 6
        supports: sample
        quote: "Of the 98 participants whose data constituted the final study sample, 5 aphasia types were observed: Anomic aphasia: 35 patients; Broca's aphasia: 33 patients; Wernicke's aphasia: 7 patients; conduction aphasia: 13 patients; global aphasia: 10 patients."
      - section: "Methods 2.4"
        page: 8
        supports: method
        quote: "Support vector machines (SVMs) were used to predict the aphasia type from brain damage."
      - section: "Methods 2.2"
        page: 6
        supports: imaging_details
        quote: "Images were acquired on a Siemens Trio 3T scanner equipped with a 12-element head coil located at the University of South Carolina."
      - section: "Methods 2.6"
        page: 9
        supports: statistics
        quote: "False discovery rate (Genovese et al., 2002) was used to correct for multiple comparisons."
      - section: "Discussion"
        page: 12
        supports: limitation
        quote: "the classification accuracy for the pairing of the two non-fluent aphasia types (global versus Broca's aphasia) was at chance level. This poor result could be driven by the similarity in the patterns of brain damage in non-fluent aphasia."

  - id: f2
    target: left_ifg_pars_triangularis
    target_kind: region
    claim: "Damage to the left inferior frontal gyrus pars triangularis (BA 45) contributes to global aphasia classification (predictive relevance Z = 2.18)."
    direction: likely
    relationship: causal
    citation: "@Yourganov2015Predicting"
    method: MLPA
    design: cross-sectional
    imaging: T1
    sample:
      n: 98
      population: "chronic left-hemisphere stroke patients with aphasia (global subgroup n=10)"
      time_post_onset: ">=6 months post-stroke (mean 40.1 months)"
      age_range: "mean 58 years (SD 11.9)"
      handedness: "all right-handed"
      language: "English"
    statistics:
      threshold: "binomial test, FDR-corrected"
      effect_size: "predictive relevance Z = 2.18 (Table 3)"
    confounders_controlled:
      - "balanced training via resampling"
    confounders_not_controlled:
      - "lesion volume"
      - "age / time post-stroke"
    region_definition:
      kind: atlas
      atlas: "AAL"
      description: "Left IFG pars triangularis as defined by AAL — corresponds to BA 45 / anterior Broca's-area cortex."
    imaging_details:
      field_strength: "3T"
      preprocessing_pipeline: "Enantiomorphic normalization (SPM12)"
      reference_space: "MNI152"
      atlases_used:
        - "AAL"
        - "AALCTS"
    replications: []
    contradictions: []
    author_limitations:
      - "Pars triangularis is also predictive of Broca's aphasia (related to the Broca's-vs-global non-separability)."
    evidence_quality: cohort
    strength: strong
    provenance:
      extracted_by: "agent:claude-opus-4-7"
      extracted_on: 2026-05-01
      paper_section: "Table 3 (Global column)"
      confidence: high
      flags:
        - "cohort overlaps with @Fridriksson2018 (same USC registry); flag for downstream double-counting risk in interpret_overlap()."
    source_passages:
      - section: "Results"
        page: 12
        supports: claim
        quote: "Middle and inferior frontal gyri, temporal regions (temporal pole; Heschl's and superior temporal gyri), insula and rolandic operculum, pre- and postcentral gyri, and putamen all had high predictive relevance for global aphasia."
      - section: "Methods 2.1 — Participants"
        page: 6
        supports: sample
        quote: "Of the 98 participants whose data constituted the final study sample, 5 aphasia types were observed"
      - section: "Methods 2.4"
        page: 8
        supports: method
        quote: "Support vector machines (SVMs) were used to predict the aphasia type from brain damage."
      - section: "Methods 2.2"
        page: 6
        supports: imaging_details
        quote: "Images were acquired on a Siemens Trio 3T scanner equipped with a 12-element head coil located at the University of South Carolina."
      - section: "Methods 2.6"
        page: 9
        supports: statistics
        quote: "False discovery rate (Genovese et al., 2002) was used to correct for multiple comparisons."

  - id: f3
    target: left_temporal_pole_mtg
    target_kind: region
    claim: "Damage to the left temporal pole (middle temporal gyrus subdivision) contributes to global aphasia classification (predictive relevance Z = 2.15)."
    direction: likely
    relationship: causal
    citation: "@Yourganov2015Predicting"
    method: MLPA
    design: cross-sectional
    imaging: T1
    sample:
      n: 98
      population: "chronic left-hemisphere stroke patients with aphasia (global subgroup n=10)"
      time_post_onset: ">=6 months post-stroke (mean 40.1 months)"
      age_range: "mean 58 years (SD 11.9)"
      handedness: "all right-handed"
      language: "English"
    statistics:
      threshold: "binomial test, FDR-corrected"
      effect_size: "predictive relevance Z = 2.15 (Table 3)"
    confounders_controlled:
      - "balanced training via resampling"
    confounders_not_controlled:
      - "lesion volume"
      - "age / time post-stroke"
    region_definition:
      kind: atlas
      atlas: "AAL"
      description: "Left temporal pole (MTG subdivision)."
    imaging_details:
      field_strength: "3T"
      preprocessing_pipeline: "Enantiomorphic normalization (SPM12)"
      reference_space: "MNI152"
      atlases_used:
        - "AAL"
        - "AALCTS"
    replications: []
    contradictions: []
    author_limitations: []
    evidence_quality: cohort
    strength: strong
    provenance:
      extracted_by: "agent:claude-opus-4-7"
      extracted_on: 2026-05-01
      paper_section: "Table 3 (Global column)"
      confidence: high
      flags:
        - "cohort overlaps with @Fridriksson2018 (same USC registry); flag for downstream double-counting risk in interpret_overlap()."
    source_passages:
      - section: "Results"
        page: 12
        supports: claim
        quote: "Middle and inferior frontal gyri, temporal regions (temporal pole; Heschl's and superior temporal gyri), insula and rolandic operculum, pre- and postcentral gyri, and putamen all had high predictive relevance for global aphasia."
      - section: "Methods 2.1 — Participants"
        page: 6
        supports: sample
        quote: "Of the 98 participants whose data constituted the final study sample, 5 aphasia types were observed"
      - section: "Methods 2.4"
        page: 8
        supports: method
        quote: "Support vector machines (SVMs) were used to predict the aphasia type from brain damage."
      - section: "Methods 2.2"
        page: 6
        supports: imaging_details
        quote: "Images were acquired on a Siemens Trio 3T scanner equipped with a 12-element head coil located at the University of South Carolina."
      - section: "Methods 2.6"
        page: 9
        supports: statistics
        quote: "False discovery rate (Genovese et al., 2002) was used to correct for multiple comparisons."

  - id: f4
    target: left_precentral_gyrus
    target_kind: region
    claim: "Damage to the left precentral gyrus contributes to global aphasia classification (predictive relevance Z = 2.05)."
    direction: likely
    relationship: causal
    citation: "@Yourganov2015Predicting"
    method: MLPA
    design: cross-sectional
    imaging: T1
    sample:
      n: 98
      population: "chronic left-hemisphere stroke patients with aphasia (global subgroup n=10)"
      time_post_onset: ">=6 months post-stroke (mean 40.1 months)"
      age_range: "mean 58 years (SD 11.9)"
      handedness: "all right-handed"
      language: "English"
    statistics:
      threshold: "binomial test, FDR-corrected"
      effect_size: "predictive relevance Z = 2.05 (Table 3)"
    confounders_controlled:
      - "balanced training via resampling"
    confounders_not_controlled:
      - "lesion volume"
      - "age / time post-stroke"
    region_definition:
      kind: atlas
      atlas: "AAL"
      description: "Left precentral gyrus (primary motor cortex)."
    imaging_details:
      field_strength: "3T"
      preprocessing_pipeline: "Enantiomorphic normalization (SPM12)"
      reference_space: "MNI152"
      atlases_used:
        - "AAL"
        - "AALCTS"
    replications: []
    contradictions: []
    author_limitations:
      - "Precentral gyrus is also weakly predictive of Wernicke's (Z=1.06) and the fluency PCA factor (Alyahya 2018)."
    evidence_quality: cohort
    strength: strong
    provenance:
      extracted_by: "agent:claude-opus-4-7"
      extracted_on: 2026-05-01
      paper_section: "Table 3 (Global column)"
      confidence: high
      flags:
        - "cohort overlaps with @Fridriksson2018 (same USC registry); flag for downstream double-counting risk in interpret_overlap()."
    source_passages:
      - section: "Results"
        page: 12
        supports: claim
        quote: "Middle and inferior frontal gyri, temporal regions (temporal pole; Heschl's and superior temporal gyri), insula and rolandic operculum, pre- and postcentral gyri, and putamen all had high predictive relevance for global aphasia."
      - section: "Methods 2.1 — Participants"
        page: 6
        supports: sample
        quote: "Of the 98 participants whose data constituted the final study sample, 5 aphasia types were observed"
      - section: "Methods 2.4"
        page: 8
        supports: method
        quote: "Support vector machines (SVMs) were used to predict the aphasia type from brain damage."
      - section: "Methods 2.2"
        page: 6
        supports: imaging_details
        quote: "Images were acquired on a Siemens Trio 3T scanner equipped with a 12-element head coil located at the University of South Carolina."
      - section: "Methods 2.6"
        page: 9
        supports: statistics
        quote: "False discovery rate (Genovese et al., 2002) was used to correct for multiple comparisons."

  - id: f5
    target: left_putamen
    target_kind: region
    claim: "Damage to the left putamen contributes to global aphasia classification (predictive relevance Z = 2.02)."
    direction: likely
    relationship: causal
    citation: "@Yourganov2015Predicting"
    method: MLPA
    design: cross-sectional
    imaging: T1
    sample:
      n: 98
      population: "chronic left-hemisphere stroke patients with aphasia (global subgroup n=10)"
      time_post_onset: ">=6 months post-stroke (mean 40.1 months)"
      age_range: "mean 58 years (SD 11.9)"
      handedness: "all right-handed"
      language: "English"
    statistics:
      threshold: "binomial test, FDR-corrected"
      effect_size: "predictive relevance Z = 2.02 (Table 3)"
    confounders_controlled:
      - "balanced training via resampling"
    confounders_not_controlled:
      - "lesion volume"
      - "age / time post-stroke"
    region_definition:
      kind: atlas
      atlas: "AAL"
      description: "Left putamen (basal ganglia)."
    imaging_details:
      field_strength: "3T"
      preprocessing_pipeline: "Enantiomorphic normalization (SPM12)"
      reference_space: "MNI152"
      atlases_used:
        - "AAL"
        - "AALCTS"
    replications: []
    contradictions: []
    author_limitations:
      - "Basal ganglia damage is also predictive of Wernicke's aphasia in this study (cross-syndromic finding)."
    evidence_quality: cohort
    strength: strong
    provenance:
      extracted_by: "agent:claude-opus-4-7"
      extracted_on: 2026-05-01
      paper_section: "Table 3 (Global column)"
      confidence: high
      flags:
        - "cohort overlaps with @Fridriksson2018 (same USC registry); flag for downstream double-counting risk in interpret_overlap()."
    source_passages:
      - section: "Results"
        page: 12
        supports: claim
        quote: "Middle and inferior frontal gyri, temporal regions (temporal pole; Heschl's and superior temporal gyri), insula and rolandic operculum, pre- and postcentral gyri, and putamen all had high predictive relevance for global aphasia."
      - section: "Methods 2.1 — Participants"
        page: 6
        supports: sample
        quote: "Of the 98 participants whose data constituted the final study sample, 5 aphasia types were observed"
      - section: "Methods 2.4"
        page: 8
        supports: method
        quote: "Support vector machines (SVMs) were used to predict the aphasia type from brain damage."
      - section: "Methods 2.2"
        page: 6
        supports: imaging_details
        quote: "Images were acquired on a Siemens Trio 3T scanner equipped with a 12-element head coil located at the University of South Carolina."
      - section: "Methods 2.6"
        page: 9
        supports: statistics
        quote: "False discovery rate (Genovese et al., 2002) was used to correct for multiple comparisons."

  - id: f6
    target: left_uncinate_fasciculus
    target_kind: region
    claim: "Damage to the left uncinate fasciculus contributes to global aphasia classification (predictive relevance Z = 1.71)."
    direction: likely
    relationship: causal
    citation: "@Yourganov2015Predicting"
    method: MLPA
    design: cross-sectional
    imaging: T1
    sample:
      n: 98
      population: "chronic left-hemisphere stroke patients with aphasia (global subgroup n=10)"
      time_post_onset: ">=6 months post-stroke (mean 40.1 months)"
      age_range: "mean 58 years (SD 11.9)"
      handedness: "all right-handed"
      language: "English"
    statistics:
      threshold: "binomial test, FDR-corrected"
      effect_size: "predictive relevance Z = 1.71 (Table 3)"
    confounders_controlled:
      - "balanced training via resampling"
    confounders_not_controlled:
      - "lesion volume"
      - "age / time post-stroke"
    region_definition:
      kind: tract
      atlas: "Catani–Thiebaut de Schotten 2008 (CTS)"
      description: "Left uncinate fasciculus — the white-matter tract connecting anterior temporal lobe to ventral prefrontal cortex; part of the ventral language stream."
    imaging_details:
      field_strength: "3T"
      preprocessing_pipeline: "Enantiomorphic normalization (SPM12)"
      reference_space: "MNI152"
      atlases_used:
        - "CTS"
        - "AALCTS"
    replications: []
    contradictions: []
    author_limitations: []
    evidence_quality: cohort
    strength: moderate
    provenance:
      extracted_by: "agent:claude-opus-4-7"
      extracted_on: 2026-05-01
      paper_section: "Table 3 (Global column)"
      confidence: high
      flags:
        - "cohort overlaps with @Fridriksson2018 (same USC registry); flag for downstream double-counting risk in interpret_overlap()."
    source_passages:
      - section: "Results"
        page: 12
        supports: claim
        quote: "Among the white-matter tracts, uncinate and arcuate fasciculi, particularly the long and anterior segments of the latter, were also found to be predictive of global aphasia."
      - section: "Methods 2.1 — Participants"
        page: 6
        supports: sample
        quote: "Of the 98 participants whose data constituted the final study sample, 5 aphasia types were observed"
      - section: "Methods 2.4"
        page: 8
        supports: method
        quote: "Support vector machines (SVMs) were used to predict the aphasia type from brain damage."
      - section: "Methods 2.2"
        page: 6
        supports: imaging_details
        quote: "Images were acquired on a Siemens Trio 3T scanner equipped with a 12-element head coil located at the University of South Carolina."
      - section: "Methods 2.6"
        page: 9
        supports: statistics
        quote: "False discovery rate (Genovese et al., 2002) was used to correct for multiple comparisons."

  - id: f7
    target: left_insula
    target_kind: region
    claim: "Damage to the left insula contributes to global aphasia classification (predictive relevance Z = 1.66)."
    direction: likely
    relationship: causal
    citation: "@Yourganov2015Predicting"
    method: MLPA
    design: cross-sectional
    imaging: T1
    sample:
      n: 98
      population: "chronic left-hemisphere stroke patients with aphasia (global subgroup n=10)"
      time_post_onset: ">=6 months post-stroke (mean 40.1 months)"
      age_range: "mean 58 years (SD 11.9)"
      handedness: "all right-handed"
      language: "English"
    statistics:
      threshold: "binomial test, FDR-corrected"
      effect_size: "predictive relevance Z = 1.66 (Table 3)"
    confounders_controlled:
      - "balanced training via resampling"
    confounders_not_controlled:
      - "lesion volume"
      - "age / time post-stroke"
    region_definition:
      kind: atlas
      atlas: "AAL"
      description: "Left insula — the cortex buried within the lateral sulcus."
    imaging_details:
      field_strength: "3T"
      preprocessing_pipeline: "Enantiomorphic normalization (SPM12)"
      reference_space: "MNI152"
      atlases_used:
        - "AAL"
        - "AALCTS"
    replications: []
    contradictions: []
    author_limitations:
      - "Insula is consistently implicated in language production but is also part of the broader MCA-territory damage pattern in global aphasia."
    evidence_quality: cohort
    strength: moderate
    provenance:
      extracted_by: "agent:claude-opus-4-7"
      extracted_on: 2026-05-01
      paper_section: "Table 3 (Global column); Discussion page 13"
      confidence: high
      flags:
        - "cohort overlaps with @Fridriksson2018 (same USC registry); flag for downstream double-counting risk in interpret_overlap()."
    source_passages:
      - section: "Discussion"
        page: 13
        supports: claim
        quote: "Consistent with previous reports (Damasio, 1992; Marshall et al., 1998), we have found this type of aphasia to be associated with damage to areas predictive for Broca's and Wernicke's aphasia, as well as insular regions."
      - section: "Methods 2.1 — Participants"
        page: 6
        supports: sample
        quote: "Of the 98 participants whose data constituted the final study sample, 5 aphasia types were observed"
      - section: "Methods 2.4"
        page: 8
        supports: method
        quote: "Support vector machines (SVMs) were used to predict the aphasia type from brain damage."
      - section: "Methods 2.2"
        page: 6
        supports: imaging_details
        quote: "Images were acquired on a Siemens Trio 3T scanner equipped with a 12-element head coil located at the University of South Carolina."
      - section: "Methods 2.6"
        page: 9
        supports: statistics
        quote: "False discovery rate (Genovese et al., 2002) was used to correct for multiple comparisons."

  - id: f8
    target: left_anterior_arcuate_fasciculus
    target_kind: region
    claim: "Damage to the anterior segment of the left arcuate fasciculus contributes to global aphasia classification (predictive relevance Z = 1.65)."
    direction: likely
    relationship: causal
    citation: "@Yourganov2015Predicting"
    method: MLPA
    design: cross-sectional
    imaging: T1
    sample:
      n: 98
      population: "chronic left-hemisphere stroke patients with aphasia (global subgroup n=10)"
      time_post_onset: ">=6 months post-stroke (mean 40.1 months)"
      age_range: "mean 58 years (SD 11.9)"
      handedness: "all right-handed"
      language: "English"
    statistics:
      threshold: "binomial test, FDR-corrected"
      effect_size: "predictive relevance Z = 1.65 (Table 3)"
    confounders_controlled:
      - "balanced training via resampling"
    confounders_not_controlled:
      - "lesion volume"
      - "age / time post-stroke"
    region_definition:
      kind: tract
      atlas: "Catani–Thiebaut de Schotten 2008 (CTS)"
      description: "Anterior segment of arcuate fasciculus — same target as Broca's f1 (Z=3.2 there). Lower predictive relevance for global because the segment alone is shared with Broca's; the global classifier weighs additional regions."
    imaging_details:
      field_strength: "3T"
      preprocessing_pipeline: "Enantiomorphic normalization (SPM12)"
      reference_space: "MNI152"
      atlases_used:
        - "CTS"
        - "AALCTS"
    replications: []
    contradictions: []
    author_limitations:
      - "Same anterior-arcuate finding appears for Broca's aphasia (f1, Z=3.2). The smaller relevance here (Z=1.65) reflects the fact that Broca's-vs-global classification is at chance — this region is one of the shared lesion features."
    evidence_quality: cohort
    strength: moderate
    provenance:
      extracted_by: "agent:claude-opus-4-7"
      extracted_on: 2026-05-01
      paper_section: "Table 3 (Global column); Discussion page 12"
      confidence: high
      flags:
        - "cohort overlaps with @Fridriksson2018 (same USC registry); flag for downstream double-counting risk in interpret_overlap()."
        - "shared target with brocas_aphasia:f1 — when promote.py consolidates the canonical left_anterior_arcuate_fasciculus region entry, it should keep both findings (Broca's Z=3.2 and global Z=1.65) and cross-link via replications."
    source_passages:
      - section: "Results"
        page: 12
        supports: claim
        quote: "Among the white-matter tracts, uncinate and arcuate fasciculi, particularly the long and anterior segments of the latter, were also found to be predictive of global aphasia."
      - section: "Discussion"
        page: 12
        supports: limitation
        quote: "if we look at the areas that are predictive of Broca's and global aphasia (Table 3), we see that the vast majority of the brain areas that are predictive of Broca's aphasia are also predictive of global aphasia."
      - section: "Methods 2.1 — Participants"
        page: 6
        supports: sample
        quote: "Of the 98 participants whose data constituted the final study sample, 5 aphasia types were observed"
      - section: "Methods 2.4"
        page: 8
        supports: method
        quote: "Support vector machines (SVMs) were used to predict the aphasia type from brain damage."
      - section: "Methods 2.2"
        page: 6
        supports: imaging_details
        quote: "Images were acquired on a Siemens Trio 3T scanner equipped with a 12-element head coil located at the University of South Carolina."
      - section: "Methods 2.6"
        page: 9
        supports: statistics
        quote: "False discovery rate (Genovese et al., 2002) was used to correct for multiple comparisons."

source: agent_draft
last_reviewed: null
notes: |
  Re-extraction draft from Yourganov 2015. Eight findings extracted —
  the highest-relevance regions in Table 3's Global column. The
  remaining Table 3 entries for global aphasia (rolandic operculum
  Z=1.96, IFG opercular Z=1.78, Heschl's gyrus Z=1.78, long-segment
  arcuate Z=1.47, IFG orbital Z=1.28, arcuate combined Z=1.21,
  superior frontal gyrus Z=1.21, cortico-spinal tract Z=1.08,
  superior temporal gyrus Z=1.31) are not extracted as separate
  findings here to keep the draft within ~10 findings; the file-level
  notes capture them and the full Table 3 is in the source PDF.

  Critical caveat: global aphasia could not be classified above
  chance versus Broca's aphasia in this study. Many of these eight
  findings are shared with the brocas_aphasia draft; cross-link via
  `replications` when promoted.
---

# Global aphasia

## Clinical definition

Global aphasia is the most severe aphasia syndrome, characterized
by profoundly impaired comprehension and production across all
language modalities. Associated with extensive cortical damage in
the territory supplied by the middle cerebral artery, typically
encompassing both Broca's and Wernicke's areas plus surrounding
cortex.

## Lesion correlates (per Yourganov 2015)

Top eight regions extracted (Table 3, Global column, predictive
relevance Z > 1.5):

  - Middle frontal gyrus (Z = 2.51) — f1
  - IFG pars triangularis (Z = 2.18) — f2
  - Temporal pole, MTG (Z = 2.15) — f3
  - Precentral gyrus (Z = 2.05) — f4
  - Putamen (Z = 2.02) — f5
  - Uncinate fasciculus (Z = 1.71) — f6
  - Insula (Z = 1.66) — f7
  - Anterior segment of arcuate fasciculus (Z = 1.65) — f8

Additional Table 3 regions with predictive relevance > 1 not
extracted as separate findings: rolandic operculum (1.96),
IFG opercular = `ho-cort_44` (1.78), Heschl's gyrus (1.78),
long-segment arcuate (1.47), IFG orbital (1.28), arcuate combined
(1.21), superior frontal gyrus (1.21), superior temporal gyrus
(1.31), cortico-spinal tract (1.08).

## Important caveat

Global vs Broca's classification was at chance (Table 1). Many
predictive regions overlap with Broca's aphasia. The two non-fluent
syndromes are not clearly separable on lesion pattern alone.
