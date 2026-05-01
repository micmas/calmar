---
schema_version: 2.3
id: conduction_aphasia
name: "Conduction aphasia"
kind: impairment
status: draft
created_by: "agent:claude-opus-4-7"
created_on: 2026-05-01
short_definition: "Aphasia syndrome characterized by relatively preserved auditory comprehension and fluent speech, with frequent phonemic paraphasic errors and disproportionately impaired repetition. Historically attributed to arcuate fasciculus damage; modern evidence implicates supramarginal gyrus and posterior superior temporal gyrus."
assessment:
  - "Western Aphasia Battery (WAB / WAB-R)"
  - "Boston Diagnostic Aphasia Examination (BDAE)"

findings:
  - id: f1
    target: left_posterior_arcuate_fasciculus
    target_kind: region
    claim: "Damage to the posterior segment of the left arcuate fasciculus is the strongest predictor of conduction aphasia in a multivariate SVM classification of 98 chronic stroke aphasia patients (predictive relevance Z = 2.48)."
    direction: likely
    relationship: causal
    citation: "@Yourganov2015Predicting"
    method: MLPA
    design: cross-sectional
    imaging: T1
    sample:
      n: 98
      population: "chronic left-hemisphere stroke patients with aphasia (Broca's n=33; Wernicke's n=7; conduction n=13; global n=10; anomic n=35)"
      time_post_onset: ">=6 months post-stroke; mean 40.1 months (SD 49.6, range 6–276)"
      age_range: "mean 58 years (SD 11.9, range 31–80)"
      handedness: "all right-handed"
      language: "English (recruited in South Carolina, USA)"
      recruitment: "referrals from local neurologists and print/radio advertisements; behavioural assessment May 2007–Oct 2014 at the University of South Carolina."
      inclusion_criteria: "right-handed; chronic left-hemisphere stroke; aphasia present"
      exclusion_criteria: "absence of aphasia; MRI contraindications; apraxia-of-speech-driven deficit; bilateral lesion; multiple sclerosis."
    statistics:
      threshold: "binomial-distribution test, FDR-corrected (p<0.05)"
      effect_size: "predictive relevance Z = 2.48 (Table 3)"
      ci_95: "not_reported"
      p_value: "not_reported per-region"
    confounders_controlled:
      - "balanced training set via resampling"
      - "8-fold CV for SVM hyperparameters"
    confounders_not_controlled:
      - "lesion volume"
      - "age / time post-stroke"
      - "WAB-defined aphasia types (categorical thresholding)"
    region_definition:
      kind: tract
      atlas: "Catani–Thiebaut de Schotten 2008 (CTS); arcuate split into long, anterior, and posterior segments"
      description: "Posterior segment of arcuate fasciculus — the parieto-temporal arc connecting inferior parietal cortex to posterior temporal cortex; historically associated with conduction aphasia (Geschwind 1965), though modern evidence implicates the gray matter at the temporo-parietal junction more than the white matter alone (Damasio 1980; Hickok 2000; Buchsbaum 2011)."
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
        - "AALCTS (custom union; 150 areas; best-performing for most contrasts)"
    replications:
      - "@Geschwind1965"
    contradictions: []
    author_limitations:
      - "Conduction vs Wernicke's aphasia could not be classified above chance with any atlas (Table 1) — both syndromes share temporo-parietal junction damage."
      - "Atlas-based parcellation has lower spatial resolution than voxel-wise approaches."
      - "CTS atlas built from 12 healthy adults at 1.5T."
    evidence_quality: cohort
    strength: strong
    provenance:
      extracted_by: "agent:claude-opus-4-7"
      extracted_on: 2026-05-01
      paper_section: "Results page 12; Table 3 (Conduction column); Discussion page 13"
      confidence: high
      flags:
        - "cohort overlaps with @Fridriksson2018 (same USC registry); flag for downstream double-counting risk in interpret_overlap()."
    source_passages:
      - section: "Results"
        page: 12
        supports: claim
        quote: "Conduction aphasia is associated with damage to the posterior segment of the arcuate fasciculus, Heschl's gyrus, and optical tracts."
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
      - section: "Methods 2.3 — Segmentation"
        page: 7
        supports: region_definition
        quote: "An atlas of white-matter tracts (Catani & Thiebaut de Schotten, 2008), which we refer to as CTS (Catani - Thiebaut de Schotten) atlas for the sake of brevity; 34 areas"
      - section: "Methods 2.6"
        page: 9
        supports: statistics
        quote: "False discovery rate (Genovese et al., 2002) was used to correct for multiple comparisons."
      - section: "Discussion"
        page: 13
        supports: limitation
        quote: "Conduction aphasia is thought to be linked to damage of regions in the neighbourhood of temporo-parietal junction (Damasio, 1992; Hickok et al., 2000; Dick & Tremblay, 2012). Our results are consistent with this picture: in our sample, conduction aphasia is associated with damage to Heschl's gyrus and the adjacent white-matter tracts (posterior segment of the arcuate fasciculus; optic radiations)."

  - id: f2
    target: left_heschls_gyrus
    target_kind: region
    claim: "Damage to the left Heschl's gyrus contributes to conduction aphasia classification (predictive relevance Z = 1.47)."
    direction: likely
    relationship: causal
    citation: "@Yourganov2015Predicting"
    method: MLPA
    design: cross-sectional
    imaging: T1
    sample:
      n: 98
      population: "chronic left-hemisphere stroke patients with aphasia"
      time_post_onset: ">=6 months post-stroke (mean 40.1 months)"
      age_range: "mean 58 years (SD 11.9)"
      handedness: "all right-handed"
      language: "English"
    statistics:
      threshold: "binomial test, FDR-corrected"
      effect_size: "predictive relevance Z = 1.47 (Table 3)"
    confounders_controlled:
      - "balanced training via resampling"
    confounders_not_controlled:
      - "lesion volume"
      - "age / time post-stroke"
    region_definition:
      kind: atlas
      atlas: "AAL"
      description: "Left Heschl's gyrus (transverse temporal gyrus; primary auditory cortex)."
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
      - "Heschl's gyrus is also predictive of Broca's, Wernicke's, and global aphasia — finding is non-specific to conduction aphasia."
    evidence_quality: cohort
    strength: moderate
    provenance:
      extracted_by: "agent:claude-opus-4-7"
      extracted_on: 2026-05-01
      paper_section: "Table 3 (Conduction column)"
      confidence: high
      flags:
        - "cohort overlaps with @Fridriksson2018 (same USC registry); flag for downstream double-counting risk in interpret_overlap()."
    source_passages:
      - section: "Results"
        page: 12
        supports: claim
        quote: "Conduction aphasia is associated with damage to the posterior segment of the arcuate fasciculus, Heschl's gyrus, and optical tracts."
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
    target: left_optic_radiations
    target_kind: region
    claim: "Damage to the left optic radiations contributes to conduction aphasia classification (predictive relevance Z = 1.14)."
    direction: likely
    relationship: causal
    citation: "@Yourganov2015Predicting"
    method: MLPA
    design: cross-sectional
    imaging: T1
    sample:
      n: 98
      population: "chronic left-hemisphere stroke patients with aphasia"
      time_post_onset: ">=6 months post-stroke (mean 40.1 months)"
      age_range: "mean 58 years (SD 11.9)"
      handedness: "all right-handed"
      language: "English"
    statistics:
      threshold: "binomial test, FDR-corrected"
      effect_size: "predictive relevance Z = 1.14 (Table 3)"
    confounders_controlled:
      - "balanced training via resampling"
    confounders_not_controlled:
      - "lesion volume"
      - "age / time post-stroke"
    region_definition:
      kind: tract
      atlas: "Catani–Thiebaut de Schotten 2008 (CTS)"
      description: "Left optic radiations — the visual white-matter tract connecting LGN to primary visual cortex; passes through the temporal lobe near the temporo-parietal junction. Likely picked up because conduction-aphasia lesions tend to extend posteriorly into the temporal stem."
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
      - "Optic radiations are not part of the canonical language network — likely a 'passing-through' lesion artifact rather than a functional language predictor."
      - "Predictive relevance Z = 1.14 is just over the threshold (1.0) for inclusion in Table 3 — interpretation should be cautious."
    evidence_quality: cohort
    strength: weak
    provenance:
      extracted_by: "agent:claude-opus-4-7"
      extracted_on: 2026-05-01
      paper_section: "Table 3 (Conduction column)"
      confidence: high
      flags:
        - "cohort overlaps with @Fridriksson2018 (same USC registry); flag for downstream double-counting risk in interpret_overlap()."
        - "optic radiations are not a canonical language tract; this finding likely reflects spatial overlap with the temporal-stem lesion pattern of conduction aphasia rather than a functional contribution to language."
    source_passages:
      - section: "Results"
        page: 12
        supports: claim
        quote: "Conduction aphasia is associated with damage to the posterior segment of the arcuate fasciculus, Heschl's gyrus, and optical tracts."
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
      - section: "Discussion"
        page: 13
        supports: limitation
        quote: "in our sample, conduction aphasia is associated with damage to Heschl's gyrus and the adjacent white-matter tracts (posterior segment of the arcuate fasciculus; optic radiations)."

source: agent_draft
last_reviewed: null
notes: |
  Re-extraction draft from Yourganov 2015. Three findings recorded —
  exactly the regions in Table 3's Conduction column with predictive
  relevance > 1. The optic-radiations finding (f3) is included for
  completeness but flagged as likely-incidental given that optic
  radiations are not a canonical language tract.
---

# Conduction aphasia

## Clinical definition

Conduction aphasia is characterized by relatively preserved auditory
comprehension and fluent speech, with frequent phonemic paraphasic
errors and disproportionately impaired repetition. Historically
attributed to arcuate fasciculus damage (Geschwind 1965); modern
evidence implicates the temporo-parietal junction grey matter
(supramarginal gyrus, posterior superior temporal gyrus, Heschl's
gyrus).

## Lesion correlates (per Yourganov 2015)

  - Posterior segment of arcuate fasciculus (Z = 2.48) — f1
  - Heschl's gyrus (Z = 1.47) — f2
  - Optic radiations (Z = 1.14) — f3 (probably incidental)

## Important caveat

Conduction vs Wernicke's classification accuracy was at chance with
all atlases (Table 1, page 22) — these two fluent syndromes share
extensive temporo-parietal lesion territory.
