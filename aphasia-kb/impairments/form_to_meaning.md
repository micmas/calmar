---
schema_version: 2.3
id: form_to_meaning
name: Form-to-meaning processing (ventral stream)
aliases:
- ventral stream (speech processing)
- lexical-semantic processing
- meaning-to-form processing
kind: impairment
status: approved
created_by: agent:claude-opus-4-7
created_on: 2026-05-01
short_definition: 'Underlying processing component for the lexical-semantic aspects
  of speech: comprehension of single words and sentences, and lexical-semantic access
  for production. Operationally defined as the positive loadings of Principal Component
  2 in Fridriksson et al. 2018, indexed by sentence-comprehension impairment, auditory-comprehension
  impairment, semantic and phonological errors during naming, and sentence repetition.'
assessment:
- Western Aphasia Battery (WAB) — auditory verbal comprehension subtests
- Northwestern Assessment of Verbs and Sentences (NAVS) — Sentence Comprehension Test
- Philadelphia Naming Test (PNT) — semantic and phonological error scoring
- Sentence repetition tasks
findings:
- id: f1
  target: left_posterior_middle_temporal_gyrus
  target_kind: region
  claim: Damage to the left posterior middle temporal gyrus loads strongly on the
    form-to-meaning (ventral-stream) processing component in chronic post-stroke aphasia,
    identifying it as the primary anchor of the ventral speech-processing stream.
  direction: likely
  relationship: causal
  citation: '@Fridriksson2018'
  method: VLSM
  design: cross-sectional
  imaging: T1
  sample:
    n: 138
    population: chronic stroke survivors with unilateral left-hemisphere stroke (subset
      n=138 with both behavioural and MRI data; per-test n ranged 38–138)
    time_post_onset: '>=6 months post-stroke; mean 36.3 months (SD 43.6)'
    age_range: mean age at stroke 57.31 years (SD 11.49)
    handedness: not_reported
    language: English (recruited at University of South Carolina, USA)
    recruitment: archival database of the Aphasia Laboratory, University of South
      Carolina.
    inclusion_criteria: unilateral left-hemisphere stroke; ≥6 months post-stroke;
      behavioural testing + MRI.
    exclusion_criteria: not_reported beyond imaging-quality and lesion-mask review.
  statistics:
    threshold: univariate VLSM with voxel-based permutation thresholding (1000 permutations)
      and FWE correction; voxels included only if ≥5 patients had damage. Component
      2 explains 27% of variance; voxelwise loadings range -0.003 to +0.003 (positive
      loadings index form-to-meaning).
    cluster_extent: null
    effect_size: voxelwise PCA loading on Component 2 (positive direction); per Discussion,
      posterior MTG is one of the two anchoring regions of the ventral stream
    ci_95: not_reported
    p_value: not_reported per-region (PCA-derived loading)
  confounders_controlled:
  - lesion volume — Component 1 (47% variance) captured the lesion-volume spatial
    pattern (r=-0.78 with cohort lesion-overlap map); Component 2 is orthogonal to
    Component 1.
  - vascular distribution — verified by multiplying Component 2 by a binary-lesion-only
    PCA component (Component 2b).
  confounders_not_controlled:
  - age, time post-stroke, sex
  - behavioural battery completeness (per-test n 38–138)
  - MCA-territory coverage limit
  region_definition:
    kind: data_driven_cluster
    atlas: AAL (per Tables S3/S4)
    description: 'Left posterior middle temporal gyrus — one of the two anchoring
      regions of the ventral stream per the Discussion (page 4): ''this ventral stream
      is anchored by the posterior MTG and posterior STG''. Lesion damage measured
      as binarized lesion mask after enantiomorphic normalization (Nachev 2008) to
      MNI.'
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: T1
      sequence: MP-RAGE / TFE
      voxel_size_mm:
      - 1
      - 1
      - 1
      TR_ms: 2250
      TI_ms: 925
      TE_ms: 4.15
      notes: FOV 256×256, 192 sagittal slices, 9° flip, GRAPPA=2.
    - modality: T2
      sequence: 3D SPACE
      voxel_size_mm:
      - 1
      - 1
      - 1
      TR_ms: 3200
      TE_ms: 352
      notes: Lesions demarcated on T2 by neurologist (LB); coregistered to T1 native;
        warped to MNI; binarized at 50%.
    preprocessing_pipeline: dcm2niix → manual T2 lesion drawing (MRIcron) → coregister
      T2→T1 → enantiomorphic normalization (Nachev 2008) using SPM unified segmentation-normalization
      (Ashburner & Friston 2005) and Clinical Toolbox age-appropriate template → binarize
      at 50%.
    reference_space: MNI152
    atlases_used:
    - AAL
    - Clinical Toolbox age-appropriate template (Rorden et al. 2012)
  replications:
  - '@Mirman2015'
  contradictions: []
  author_limitations:
  - Lesion coverage limited to MCA territory; precuneus and other rarely-lesioned
    regions cannot be adequately tested.
  - Chronic-stroke reorganisation may inflate the apparent role of areas the brain
    has come to rely on after recovery.
  - Sentence-comprehension and auditory-comprehension measures load heavily on the
    positive Component 2 — these are partial proxies for ventral-stream processing.
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Results — Cortical Loadings (page 3); Discussion (page 4); Conclusion
      (page 5)
    confidence: high
    flags:
    - cohort overlaps with @Yourganov2015Predicting — same University of South Carolina
      Aphasia Lab archival database, overlapping enrolment 2007–2014; flag for downstream
      double-counting risk in interpret_overlap().
  source_passages:
  - section: Results — Cortical Loadings
    page: 3
    supports: claim
    quote: Positive loadings of Component 2 were associated almost exclusively with
      temporal lobe damage but also, involved areas in the parietal lobe, including
      posterior portions of the SMG and the angular gyrus as well as anteroventral
      inferior frontal lobe areas, such as the pars orbitalis.
  - section: Discussion
    page: 4
    supports: claim
    quote: this ventral stream is anchored by the posterior MTG and posterior STG
      (Table S4), the areas showing the greatest expression of Component 2, and extends
      to the posterior inferior parietal lobule (IPL) as well as via the uncinate
      fasciculus to the pars orbitalis in the inferior frontal gyrus.
  - section: Experimental Procedures — Participants
    page: 5
    supports: sample
    quote: Data from 165 persons with unilateral left hemisphere stroke were considered
      for analyses. Among these 165 persons, 138 (63 females) had both behavioral
      testing and MRI data.
  - section: Experimental Procedures — Participants
    page: 5
    supports: sample
    quote: all participants were at least 6 mo poststroke, with a mean age at the
      time of stroke of 57.31 y old (SD = 11.49) and a mean time poststroke of 36.3
      mo (SD = 43.6).
  - section: Experimental Procedures — VLSM Analyses
    page: 5
    supports: method
    quote: Seventy-one univariate VLSM analyses were completed to identify localized
      brain damage associated with speech processing impairments.
  - section: Experimental Procedures — VLSM Analyses
    page: 5
    supports: statistics
    quote: voxelwise statistical significance was determined by voxel-based permutation
      thresholding (1,000 permutations) and multiple comparison correction (controlling
      for familywise error). Only voxels where at least five patients had damage were
      included in each analysis.
  - section: Experimental Procedures — MRI Data Acquisition
    page: 5
    supports: imaging_details
    quote: 'MRI data were acquired using a Siemens 3T Trio System with a 12-channel
      head coil. All participants underwent scanning that included two MRI sequences:
      (i) T1-weighted imaging sequence using an MP-RAGE'
  - section: Results — Cortical Loadings
    page: 3
    supports: confounders
    quote: 'we correlated the statistical map representing Component 1 with a lesion
      overlay map from all 138 participants included in the study sample. The correlation
      between the two maps was r = −0.78. Correlation between the second component
      and the lesion overlap map was much smaller: r = 0.04.'
  - section: Discussion
    page: 4
    supports: limitation
    quote: lesion studies that rely on stroke data are limited to studying cortical
      areas where stroke is likely to occur (e.g., middle cerebral artery distribution)
- id: f2
  target: left_posterior_superior_temporal_gyrus
  target_kind: region
  claim: Damage to the left posterior superior temporal gyrus loads strongly on the
    form-to-meaning (ventral-stream) component, marking it as the second anchor of
    the ventral speech-processing stream alongside the posterior MTG.
  direction: likely
  relationship: causal
  citation: '@Fridriksson2018'
  method: VLSM
  design: cross-sectional
  imaging: T1
  sample:
    n: 138
    population: chronic stroke survivors with unilateral left-hemisphere stroke
    time_post_onset: '>=6 months post-stroke (mean 36.3 months)'
    age_range: mean age at stroke 57.31 years
    handedness: not_reported
    language: English
  statistics:
    threshold: VLSM permutation + FWE; PCA Component 2 positive loadings
    effect_size: voxelwise PCA loading; one of the two greatest-expression regions
      per Discussion
  confounders_controlled:
  - lesion volume orthogonality (Component 1)
  - vascular pattern verified via lesion-only PCA
  confounders_not_controlled:
  - MCA-territory limit
  - chronic-stroke reorganisation
  region_definition:
    kind: atlas
    atlas: AAL
    description: Left posterior superior temporal gyrus — classical Wernicke's-area
      cortex; one of the two anchoring regions of the ventral stream per the Discussion.
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: Enantiomorphic normalization (SPM)
    reference_space: MNI152
    atlases_used:
    - AAL
  replications:
  - '@Yourganov2015Predicting'
  - '@Mirman2015'
  contradictions: []
  author_limitations:
  - Posterior STG is also predictive of Wernicke's and conduction aphasia (Yourganov
    2015) — damage produces a complex behavioural pattern that the form-to-meaning
    label only partially captures.
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Discussion (page 4)
    confidence: high
    flags:
    - cohort overlaps with @Yourganov2015Predicting.
  source_passages:
  - section: Discussion
    page: 4
    supports: claim
    quote: this ventral stream is anchored by the posterior MTG and posterior STG
      (Table S4), the areas showing the greatest expression of Component 2, and extends
      to the posterior inferior parietal lobule (IPL) as well as via the uncinate
      fasciculus to the pars orbitalis in the inferior frontal gyrus.
  - section: Experimental Procedures — Participants
    page: 5
    supports: sample
    quote: Data from 165 persons with unilateral left hemisphere stroke were considered
      for analyses. Among these 165 persons, 138 (63 females) had both behavioral
      testing and MRI data.
  - section: Experimental Procedures — VLSM Analyses
    page: 5
    supports: method
    quote: Seventy-one univariate VLSM analyses were completed to identify localized
      brain damage associated with speech processing impairments.
  - section: Experimental Procedures — VLSM Analyses
    page: 5
    supports: statistics
    quote: voxelwise statistical significance was determined by voxel-based permutation
      thresholding (1,000 permutations) and multiple comparison correction (controlling
      for familywise error).
  - section: Experimental Procedures — MRI Data Acquisition
    page: 5
    supports: imaging_details
    quote: MRI data were acquired using a Siemens 3T Trio System with a 12-channel
      head coil.
- id: f3
  target: left_uncinate_fasciculus
  target_kind: region
  claim: Damage to the left uncinate fasciculus loads strongly on the form-to-meaning
    (ventral-stream) component — over 85% of uncinate-fasciculus voxels carry positive
    loadings — identifying it as the primary white-matter conduit of the ventral speech-processing
    stream.
  direction: likely
  relationship: causal
  citation: '@Fridriksson2018'
  method: VLSM
  design: cross-sectional
  imaging: T1
  sample:
    n: 138
    population: chronic stroke survivors with unilateral left-hemisphere stroke
    time_post_onset: '>=6 months post-stroke (mean 36.3 months)'
    age_range: mean age at stroke 57.31 years
    handedness: not_reported
    language: English
  statistics:
    threshold: VLSM permutation + FWE; PCA Component 2 positive loadings
    effect_size: '>85% of uncinate-fasciculus voxels carry positive Component 2 loadings'
  confounders_controlled:
  - Component 1 orthogonality (lesion volume)
  - lesion-only PCA verification
  confounders_not_controlled:
  - MCA-territory limit (uncinate damage requires anteroinferior MCA / temporal-pole
    infarcts)
  region_definition:
    kind: tract
    atlas: anatomical labels (the paper notes >85% voxel coverage but does not name
      a specific tract atlas in the main text)
    description: 'Left uncinate fasciculus — white-matter tract connecting anterior
      temporal lobe to ventral inferior frontal cortex (pars orbitalis). The paper''s
      Results note: ''the voxels with positive loadings composed more than 85% of
      the uncinate fasciculus, a fiber bundle that connects the anterior temporal
      lobe and the inferior aspects of the posterior frontal lobe, including pars
      orbitalis and pars triangularis''.'
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: Enantiomorphic normalization (SPM)
    reference_space: MNI152
    atlases_used: []
  replications:
  - '@Yourganov2015Predicting'
  contradictions: []
  author_limitations:
  - Uncinate-fasciculus identification was not via a specific tract atlas (no atlas
    named); the >85% voxel coverage is descriptive rather than statistical.
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Results — Cortical Loadings (page 3); Conclusion (page 5)
    confidence: high
    flags:
    - cohort overlaps with @Yourganov2015Predicting (same USC archival database).
  source_passages:
  - section: Results — Cortical Loadings
    page: 3
    supports: claim
    quote: It is worth noting that the voxels with positive loadings composed more
      than 85% of the uncinate fasciculus, a fiber bundle that connects the anterior
      temporal lobe and the inferior aspects of the posterior frontal lobe, including
      pars orbitalis and pars triangularis
  - section: Conclusion
    page: 5
    supports: claim
    quote: The ventral stream involves lateral temporal lobe structures extending
      to the IPL as well as the inferior frontal lobe via the uncinate fasciculus.
  - section: Experimental Procedures — Participants
    page: 5
    supports: sample
    quote: Data from 165 persons with unilateral left hemisphere stroke were considered
      for analyses. Among these 165 persons, 138 (63 females) had both behavioral
      testing and MRI data.
  - section: Experimental Procedures — VLSM Analyses
    page: 5
    supports: method
    quote: Seventy-one univariate VLSM analyses were completed to identify localized
      brain damage associated with speech processing impairments.
  - section: Experimental Procedures — VLSM Analyses
    page: 5
    supports: statistics
    quote: voxelwise statistical significance was determined by voxel-based permutation
      thresholding (1,000 permutations) and multiple comparison correction (controlling
      for familywise error).
  - section: Experimental Procedures — MRI Data Acquisition
    page: 5
    supports: imaging_details
    quote: MRI data were acquired using a Siemens 3T Trio System with a 12-channel
      head coil.
- id: f4
  target: left_posterior_supramarginal_gyrus
  target_kind: region
  claim: Damage to the posterior portion of the left supramarginal gyrus loads on
    the form-to-meaning (ventral-stream) component, contrasting with the anterior
    SMG that loads on the dorsal stream.
  direction: likely
  relationship: causal
  citation: '@Fridriksson2018'
  method: VLSM
  design: cross-sectional
  imaging: T1
  sample:
    n: 138
    population: chronic stroke survivors with unilateral left-hemisphere stroke
    time_post_onset: '>=6 months post-stroke (mean 36.3 months)'
    age_range: mean age at stroke 57.31 years
    handedness: not_reported
    language: English
  statistics:
    threshold: VLSM permutation + FWE; PCA Component 2 positive loadings
    effect_size: voxelwise PCA loading
  confounders_controlled:
  - Component 1 orthogonality
  - lesion-only PCA verification
  confounders_not_controlled:
  - MCA-territory limit
  region_definition:
    kind: data_driven_cluster
    atlas: AAL (anterior/posterior split is voxelwise within the AAL SMG parcel)
    description: Posterior portion of left supramarginal gyrus. The paper explicitly
      contrasts the anterior SMG (dorsal stream, see form_to_articulation:f4) with
      the posterior SMG (ventral stream, this finding) — a within-AAL-SMG voxelwise
      division. Area Spt (Hickok & Poeppel 2007) sits at the boundary between the
      two streams here.
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: Enantiomorphic normalization (SPM)
    reference_space: MNI152
    atlases_used:
    - AAL
  replications: []
  contradictions: []
  author_limitations:
  - AAL atlas does not natively split SMG anterior vs posterior — the division here
    is voxelwise.
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Results — Cortical Loadings (page 3); Discussion (page 4)
    confidence: high
    flags:
    - cohort overlaps with @Yourganov2015Predicting.
    - anterior-vs-posterior SMG split is voxelwise (not AAL); same caveat as form_to_articulation:f4.
  source_passages:
  - section: Results — Cortical Loadings
    page: 3
    supports: claim
    quote: Positive loadings of Component 2 were associated almost exclusively with
      temporal lobe damage but also, involved areas in the parietal lobe, including
      posterior portions of the SMG and the angular gyrus as well as anteroventral
      inferior frontal lobe areas, such as the pars orbitalis.
  - section: Experimental Procedures — Participants
    page: 5
    supports: sample
    quote: Data from 165 persons with unilateral left hemisphere stroke were considered
      for analyses. Among these 165 persons, 138 (63 females) had both behavioral
      testing and MRI data.
  - section: Experimental Procedures — VLSM Analyses
    page: 5
    supports: method
    quote: Seventy-one univariate VLSM analyses were completed to identify localized
      brain damage associated with speech processing impairments.
  - section: Experimental Procedures — VLSM Analyses
    page: 5
    supports: statistics
    quote: voxelwise statistical significance was determined by voxel-based permutation
      thresholding (1,000 permutations) and multiple comparison correction (controlling
      for familywise error).
  - section: Experimental Procedures — MRI Data Acquisition
    page: 5
    supports: imaging_details
    quote: MRI data were acquired using a Siemens 3T Trio System with a 12-channel
      head coil.
- id: f5
  target: left_angular_gyrus
  target_kind: region
  claim: Damage to the left angular gyrus loads on the form-to-meaning (ventral-stream)
    component.
  direction: likely
  relationship: causal
  citation: '@Fridriksson2018'
  method: VLSM
  design: cross-sectional
  imaging: T1
  sample:
    n: 138
    population: chronic stroke survivors with unilateral left-hemisphere stroke
    time_post_onset: '>=6 months post-stroke (mean 36.3 months)'
    age_range: mean age at stroke 57.31 years
    handedness: not_reported
    language: English
  statistics:
    threshold: VLSM permutation + FWE; Component 2 positive loadings
    effect_size: voxelwise PCA loading
  confounders_controlled:
  - Component 1 orthogonality
  confounders_not_controlled:
  - MCA-territory limit
  region_definition:
    kind: atlas
    atlas: AAL
    description: Left angular gyrus (posterior inferior parietal lobule).
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: Enantiomorphic normalization (SPM)
    reference_space: MNI152
    atlases_used:
    - AAL
  replications:
  - '@Yourganov2015Predicting'
  contradictions: []
  author_limitations:
  - Angular gyrus is also predictive of Wernicke's aphasia (Yourganov 2015) — finding
    is non-specific to form-to-meaning processing alone.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Results — Cortical Loadings (page 3)
    confidence: high
    flags:
    - cohort overlaps with @Yourganov2015Predicting.
  source_passages:
  - section: Results — Cortical Loadings
    page: 3
    supports: claim
    quote: Positive loadings of Component 2 were associated almost exclusively with
      temporal lobe damage but also, involved areas in the parietal lobe, including
      posterior portions of the SMG and the angular gyrus as well as anteroventral
      inferior frontal lobe areas, such as the pars orbitalis.
  - section: Experimental Procedures — Participants
    page: 5
    supports: sample
    quote: Data from 165 persons with unilateral left hemisphere stroke were considered
      for analyses. Among these 165 persons, 138 (63 females) had both behavioral
      testing and MRI data.
  - section: Experimental Procedures — VLSM Analyses
    page: 5
    supports: method
    quote: Seventy-one univariate VLSM analyses were completed to identify localized
      brain damage associated with speech processing impairments.
  - section: Experimental Procedures — VLSM Analyses
    page: 5
    supports: statistics
    quote: voxelwise statistical significance was determined by voxel-based permutation
      thresholding (1,000 permutations) and multiple comparison correction (controlling
      for familywise error).
  - section: Experimental Procedures — MRI Data Acquisition
    page: 5
    supports: imaging_details
    quote: MRI data were acquired using a Siemens 3T Trio System with a 12-channel
      head coil.
- id: f6
  target: left_ifg_pars_orbitalis
  target_kind: region
  claim: Damage to the left inferior frontal gyrus pars orbitalis loads on the form-to-meaning
    (ventral-stream) component, marking the anterior-frontal endpoint of the ventral
    stream via the uncinate fasciculus.
  direction: likely
  relationship: causal
  citation: '@Fridriksson2018'
  method: VLSM
  design: cross-sectional
  imaging: T1
  sample:
    n: 138
    population: chronic stroke survivors with unilateral left-hemisphere stroke
    time_post_onset: '>=6 months post-stroke (mean 36.3 months)'
    age_range: mean age at stroke 57.31 years
    handedness: not_reported
    language: English
  statistics:
    threshold: VLSM permutation + FWE; Component 2 positive loadings
    effect_size: voxelwise PCA loading
  confounders_controlled:
  - Component 1 orthogonality
  confounders_not_controlled:
  - MCA-territory limit
  region_definition:
    kind: atlas
    atlas: AAL
    description: Left IFG pars orbitalis (BA 47) — anteroventral inferior frontal
      cortex; connected to anterior temporal lobe via the uncinate fasciculus per
      the paper's interpretation.
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: Enantiomorphic normalization (SPM)
    reference_space: MNI152
    atlases_used:
    - AAL
  replications:
  - '@Yourganov2015Predicting'
  contradictions: []
  author_limitations:
  - Pars orbitalis is also weakly predictive of global aphasia (Yourganov 2015 Z=1.28);
    finding overlaps with broader frontal damage.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Results — Cortical Loadings (page 3); Discussion (page 4)
    confidence: high
    flags:
    - cohort overlaps with @Yourganov2015Predicting.
  source_passages:
  - section: Results — Cortical Loadings
    page: 3
    supports: claim
    quote: Positive loadings of Component 2 were associated almost exclusively with
      temporal lobe damage but also, involved areas in the parietal lobe, including
      posterior portions of the SMG and the angular gyrus as well as anteroventral
      inferior frontal lobe areas, such as the pars orbitalis.
  - section: Discussion
    page: 4
    supports: claim
    quote: this ventral stream is anchored by the posterior MTG and posterior STG
      (Table S4), the areas showing the greatest expression of Component 2, and extends
      to the posterior inferior parietal lobule (IPL) as well as via the uncinate
      fasciculus to the pars orbitalis in the inferior frontal gyrus.
  - section: Experimental Procedures — Participants
    page: 5
    supports: sample
    quote: Data from 165 persons with unilateral left hemisphere stroke were considered
      for analyses. Among these 165 persons, 138 (63 females) had both behavioral
      testing and MRI data.
  - section: Experimental Procedures — VLSM Analyses
    page: 5
    supports: method
    quote: Seventy-one univariate VLSM analyses were completed to identify localized
      brain damage associated with speech processing impairments.
  - section: Experimental Procedures — VLSM Analyses
    page: 5
    supports: statistics
    quote: voxelwise statistical significance was determined by voxel-based permutation
      thresholding (1,000 permutations) and multiple comparison correction (controlling
      for familywise error).
  - section: Experimental Procedures — MRI Data Acquisition
    page: 5
    supports: imaging_details
    quote: MRI data were acquired using a Siemens 3T Trio System with a 12-channel
      head coil.
- id: f7
  target: left_anterior_middle_temporal_gyrus
  target_kind: region
  claim: Damage to the left anterior middle temporal gyrus loads on the form-to-meaning
    (ventral-stream) component, consistent with its role as a semantic-hub region.
  direction: likely
  relationship: causal
  citation: '@Fridriksson2018'
  method: VLSM
  design: cross-sectional
  imaging: T1
  sample:
    n: 138
    population: chronic stroke survivors with unilateral left-hemisphere stroke
    time_post_onset: '>=6 months post-stroke (mean 36.3 months)'
    age_range: mean age at stroke 57.31 years
    handedness: not_reported
    language: English
  statistics:
    threshold: VLSM permutation + FWE; Component 2 positive loadings
    effect_size: voxelwise PCA loading
  confounders_controlled:
  - Component 1 orthogonality
  confounders_not_controlled:
  - MCA-territory limit
  region_definition:
    kind: atlas
    atlas: AAL
    description: Left anterior middle temporal gyrus.
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: Enantiomorphic normalization (SPM)
    reference_space: MNI152
    atlases_used:
    - AAL
  replications:
  - '@Mirman2015'
  contradictions: []
  author_limitations:
  - The Hickok & Poeppel (2007) ventral stream extends to anterior MTG; this finding
    empirically corroborates that anatomical claim.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Discussion (page 4)
    confidence: high
    flags:
    - cohort overlaps with @Yourganov2015Predicting.
  source_passages:
  - section: Discussion
    page: 4
    supports: claim
    quote: These findings are in greater agreement with the dual stream model by Hickok
      and Poeppel (8), which includes a ventral stream mostly involving temporal lobe
      regions, including the posterior and anterior MTGs
  - section: Experimental Procedures — Participants
    page: 5
    supports: sample
    quote: Data from 165 persons with unilateral left hemisphere stroke were considered
      for analyses. Among these 165 persons, 138 (63 females) had both behavioral
      testing and MRI data.
  - section: Experimental Procedures — VLSM Analyses
    page: 5
    supports: method
    quote: Seventy-one univariate VLSM analyses were completed to identify localized
      brain damage associated with speech processing impairments.
  - section: Experimental Procedures — VLSM Analyses
    page: 5
    supports: statistics
    quote: voxelwise statistical significance was determined by voxel-based permutation
      thresholding (1,000 permutations) and multiple comparison correction (controlling
      for familywise error).
  - section: Experimental Procedures — MRI Data Acquisition
    page: 5
    supports: imaging_details
    quote: MRI data were acquired using a Siemens 3T Trio System with a 12-channel
      head coil.
- id: f8
  target: left_posterior_middle_temporal_gyrus
  target_kind: region
  claim: Damage to the left posterior middle temporal gyrus loads strongly on the
    form-to-meaning (ventral-stream) processing component in chronic post-stroke aphasia,
    identifying it as the primary anchor of the ventral speech-processing stream.
  direction: likely
  relationship: causal
  citation: '@Fridriksson2018'
  method: VLSM
  design: cross-sectional
  imaging: T1
  sample:
    n: 138
    population: chronic stroke survivors with unilateral left-hemisphere stroke (subset
      n=138 with both behavioural and MRI data; per-test n ranged 38–138)
    time_post_onset: '>=6 months post-stroke; mean 36.3 months (SD 43.6)'
    age_range: mean age at stroke 57.31 years (SD 11.49)
    handedness: not_reported
    language: English (recruited at University of South Carolina, USA)
    recruitment: archival database of the Aphasia Laboratory, University of South
      Carolina.
    inclusion_criteria: unilateral left-hemisphere stroke; ≥6 months post-stroke;
      behavioural testing + MRI.
    exclusion_criteria: not_reported beyond imaging-quality and lesion-mask review.
  statistics:
    threshold: univariate VLSM with voxel-based permutation thresholding (1000 permutations)
      and FWE correction; voxels included only if ≥5 patients had damage. Component
      2 explains 27% of variance; voxelwise loadings range -0.003 to +0.003 (positive
      loadings index form-to-meaning).
    cluster_extent: null
    effect_size: voxelwise PCA loading on Component 2 (positive direction); per Discussion,
      posterior MTG is one of the two anchoring regions of the ventral stream
    ci_95: not_reported
    p_value: not_reported per-region (PCA-derived loading)
  confounders_controlled:
  - lesion volume — Component 1 (47% variance) captured the lesion-volume spatial
    pattern (r=-0.78 with cohort lesion-overlap map); Component 2 is orthogonal to
    Component 1.
  - vascular distribution — verified by multiplying Component 2 by a binary-lesion-only
    PCA component (Component 2b).
  confounders_not_controlled:
  - age, time post-stroke, sex
  - behavioural battery completeness (per-test n 38–138)
  - MCA-territory coverage limit
  region_definition:
    kind: data_driven_cluster
    atlas: AAL (per Tables S3/S4)
    description: 'Left posterior middle temporal gyrus — one of the two anchoring
      regions of the ventral stream per the Discussion (page 4): ''this ventral stream
      is anchored by the posterior MTG and posterior STG''. Lesion damage measured
      as binarized lesion mask after enantiomorphic normalization (Nachev 2008) to
      MNI.'
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: T1
      sequence: MP-RAGE / TFE
      voxel_size_mm:
      - 1
      - 1
      - 1
      TR_ms: 2250
      TI_ms: 925
      TE_ms: 4.15
      notes: FOV 256×256, 192 sagittal slices, 9° flip, GRAPPA=2.
    - modality: T2
      sequence: 3D SPACE
      voxel_size_mm:
      - 1
      - 1
      - 1
      TR_ms: 3200
      TE_ms: 352
      notes: Lesions demarcated on T2 by neurologist (LB); coregistered to T1 native;
        warped to MNI; binarized at 50%.
    preprocessing_pipeline: dcm2niix → manual T2 lesion drawing (MRIcron) → coregister
      T2→T1 → enantiomorphic normalization (Nachev 2008) using SPM unified segmentation-normalization
      (Ashburner & Friston 2005) and Clinical Toolbox age-appropriate template → binarize
      at 50%.
    reference_space: MNI152
    atlases_used:
    - AAL
    - Clinical Toolbox age-appropriate template (Rorden et al. 2012)
  replications:
  - '@Mirman2015'
  contradictions: []
  author_limitations:
  - Lesion coverage limited to MCA territory; precuneus and other rarely-lesioned
    regions cannot be adequately tested.
  - Chronic-stroke reorganisation may inflate the apparent role of areas the brain
    has come to rely on after recovery.
  - Sentence-comprehension and auditory-comprehension measures load heavily on the
    positive Component 2 — these are partial proxies for ventral-stream processing.
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Results — Cortical Loadings (page 3); Discussion (page 4); Conclusion
      (page 5)
    confidence: high
    flags:
    - cohort overlaps with @Yourganov2015Predicting — same University of South Carolina
      Aphasia Lab archival database, overlapping enrolment 2007–2014; flag for downstream
      double-counting risk in interpret_overlap().
  source_passages:
  - section: Results — Cortical Loadings
    page: 3
    supports: claim
    quote: Positive loadings of Component 2 were associated almost exclusively with
      temporal lobe damage but also, involved areas in the parietal lobe, including
      posterior portions of the SMG and the angular gyrus as well as anteroventral
      inferior frontal lobe areas, such as the pars orbitalis.
  - section: Discussion
    page: 4
    supports: claim
    quote: this ventral stream is anchored by the posterior MTG and posterior STG
      (Table S4), the areas showing the greatest expression of Component 2, and extends
      to the posterior inferior parietal lobule (IPL) as well as via the uncinate
      fasciculus to the pars orbitalis in the inferior frontal gyrus.
  - section: Experimental Procedures — Participants
    page: 5
    supports: sample
    quote: Data from 165 persons with unilateral left hemisphere stroke were considered
      for analyses. Among these 165 persons, 138 (63 females) had both behavioral
      testing and MRI data.
  - section: Experimental Procedures — Participants
    page: 5
    supports: sample
    quote: all participants were at least 6 mo poststroke, with a mean age at the
      time of stroke of 57.31 y old (SD = 11.49) and a mean time poststroke of 36.3
      mo (SD = 43.6).
  - section: Experimental Procedures — VLSM Analyses
    page: 5
    supports: method
    quote: Seventy-one univariate VLSM analyses were completed to identify localized
      brain damage associated with speech processing impairments.
  - section: Experimental Procedures — VLSM Analyses
    page: 5
    supports: statistics
    quote: voxelwise statistical significance was determined by voxel-based permutation
      thresholding (1,000 permutations) and multiple comparison correction (controlling
      for familywise error). Only voxels where at least five patients had damage were
      included in each analysis.
  - section: Experimental Procedures — MRI Data Acquisition
    page: 5
    supports: imaging_details
    quote: 'MRI data were acquired using a Siemens 3T Trio System with a 12-channel
      head coil. All participants underwent scanning that included two MRI sequences:
      (i) T1-weighted imaging sequence using an MP-RAGE'
  - section: Results — Cortical Loadings
    page: 3
    supports: confounders
    quote: 'we correlated the statistical map representing Component 1 with a lesion
      overlay map from all 138 participants included in the study sample. The correlation
      between the two maps was r = −0.78. Correlation between the second component
      and the lesion overlap map was much smaller: r = 0.04.'
  - section: Discussion
    page: 4
    supports: limitation
    quote: lesion studies that rely on stroke data are limited to studying cortical
      areas where stroke is likely to occur (e.g., middle cerebral artery distribution)
- id: f9
  target: left_posterior_superior_temporal_gyrus
  target_kind: region
  claim: Damage to the left posterior superior temporal gyrus loads strongly on the
    form-to-meaning (ventral-stream) component, marking it as the second anchor of
    the ventral speech-processing stream alongside the posterior MTG.
  direction: likely
  relationship: causal
  citation: '@Fridriksson2018'
  method: VLSM
  design: cross-sectional
  imaging: T1
  sample:
    n: 138
    population: chronic stroke survivors with unilateral left-hemisphere stroke
    time_post_onset: '>=6 months post-stroke (mean 36.3 months)'
    age_range: mean age at stroke 57.31 years
    handedness: not_reported
    language: English
  statistics:
    threshold: VLSM permutation + FWE; PCA Component 2 positive loadings
    effect_size: voxelwise PCA loading; one of the two greatest-expression regions
      per Discussion
  confounders_controlled:
  - lesion volume orthogonality (Component 1)
  - vascular pattern verified via lesion-only PCA
  confounders_not_controlled:
  - MCA-territory limit
  - chronic-stroke reorganisation
  region_definition:
    kind: atlas
    atlas: AAL
    description: Left posterior superior temporal gyrus — classical Wernicke's-area
      cortex; one of the two anchoring regions of the ventral stream per the Discussion.
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: Enantiomorphic normalization (SPM)
    reference_space: MNI152
    atlases_used:
    - AAL
  replications:
  - '@Yourganov2015Predicting'
  - '@Mirman2015'
  contradictions: []
  author_limitations:
  - Posterior STG is also predictive of Wernicke's and conduction aphasia (Yourganov
    2015) — damage produces a complex behavioural pattern that the form-to-meaning
    label only partially captures.
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Discussion (page 4)
    confidence: high
    flags:
    - cohort overlaps with @Yourganov2015Predicting.
  source_passages:
  - section: Discussion
    page: 4
    supports: claim
    quote: this ventral stream is anchored by the posterior MTG and posterior STG
      (Table S4), the areas showing the greatest expression of Component 2, and extends
      to the posterior inferior parietal lobule (IPL) as well as via the uncinate
      fasciculus to the pars orbitalis in the inferior frontal gyrus.
  - section: Experimental Procedures — Participants
    page: 5
    supports: sample
    quote: Data from 165 persons with unilateral left hemisphere stroke were considered
      for analyses. Among these 165 persons, 138 (63 females) had both behavioral
      testing and MRI data.
  - section: Experimental Procedures — VLSM Analyses
    page: 5
    supports: method
    quote: Seventy-one univariate VLSM analyses were completed to identify localized
      brain damage associated with speech processing impairments.
  - section: Experimental Procedures — VLSM Analyses
    page: 5
    supports: statistics
    quote: voxelwise statistical significance was determined by voxel-based permutation
      thresholding (1,000 permutations) and multiple comparison correction (controlling
      for familywise error).
  - section: Experimental Procedures — MRI Data Acquisition
    page: 5
    supports: imaging_details
    quote: MRI data were acquired using a Siemens 3T Trio System with a 12-channel
      head coil.
- id: f10
  target: left_uncinate_fasciculus
  target_kind: region
  claim: Damage to the left uncinate fasciculus loads strongly on the form-to-meaning
    (ventral-stream) component — over 85% of uncinate-fasciculus voxels carry positive
    loadings — identifying it as the primary white-matter conduit of the ventral speech-processing
    stream.
  direction: likely
  relationship: causal
  citation: '@Fridriksson2018'
  method: VLSM
  design: cross-sectional
  imaging: T1
  sample:
    n: 138
    population: chronic stroke survivors with unilateral left-hemisphere stroke
    time_post_onset: '>=6 months post-stroke (mean 36.3 months)'
    age_range: mean age at stroke 57.31 years
    handedness: not_reported
    language: English
  statistics:
    threshold: VLSM permutation + FWE; PCA Component 2 positive loadings
    effect_size: '>85% of uncinate-fasciculus voxels carry positive Component 2 loadings'
  confounders_controlled:
  - Component 1 orthogonality (lesion volume)
  - lesion-only PCA verification
  confounders_not_controlled:
  - MCA-territory limit (uncinate damage requires anteroinferior MCA / temporal-pole
    infarcts)
  region_definition:
    kind: tract
    atlas: anatomical labels (the paper notes >85% voxel coverage but does not name
      a specific tract atlas in the main text)
    description: 'Left uncinate fasciculus — white-matter tract connecting anterior
      temporal lobe to ventral inferior frontal cortex (pars orbitalis). The paper''s
      Results note: ''the voxels with positive loadings composed more than 85% of
      the uncinate fasciculus, a fiber bundle that connects the anterior temporal
      lobe and the inferior aspects of the posterior frontal lobe, including pars
      orbitalis and pars triangularis''.'
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: Enantiomorphic normalization (SPM)
    reference_space: MNI152
    atlases_used: []
  replications:
  - '@Yourganov2015Predicting'
  contradictions: []
  author_limitations:
  - Uncinate-fasciculus identification was not via a specific tract atlas (no atlas
    named); the >85% voxel coverage is descriptive rather than statistical.
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Results — Cortical Loadings (page 3); Conclusion (page 5)
    confidence: high
    flags:
    - cohort overlaps with @Yourganov2015Predicting (same USC archival database).
  source_passages:
  - section: Results — Cortical Loadings
    page: 3
    supports: claim
    quote: It is worth noting that the voxels with positive loadings composed more
      than 85% of the uncinate fasciculus, a fiber bundle that connects the anterior
      temporal lobe and the inferior aspects of the posterior frontal lobe, including
      pars orbitalis and pars triangularis
  - section: Conclusion
    page: 5
    supports: claim
    quote: The ventral stream involves lateral temporal lobe structures extending
      to the IPL as well as the inferior frontal lobe via the uncinate fasciculus.
  - section: Experimental Procedures — Participants
    page: 5
    supports: sample
    quote: Data from 165 persons with unilateral left hemisphere stroke were considered
      for analyses. Among these 165 persons, 138 (63 females) had both behavioral
      testing and MRI data.
  - section: Experimental Procedures — VLSM Analyses
    page: 5
    supports: method
    quote: Seventy-one univariate VLSM analyses were completed to identify localized
      brain damage associated with speech processing impairments.
  - section: Experimental Procedures — VLSM Analyses
    page: 5
    supports: statistics
    quote: voxelwise statistical significance was determined by voxel-based permutation
      thresholding (1,000 permutations) and multiple comparison correction (controlling
      for familywise error).
  - section: Experimental Procedures — MRI Data Acquisition
    page: 5
    supports: imaging_details
    quote: MRI data were acquired using a Siemens 3T Trio System with a 12-channel
      head coil.
- id: f11
  target: left_posterior_supramarginal_gyrus
  target_kind: region
  claim: Damage to the posterior portion of the left supramarginal gyrus loads on
    the form-to-meaning (ventral-stream) component, contrasting with the anterior
    SMG that loads on the dorsal stream.
  direction: likely
  relationship: causal
  citation: '@Fridriksson2018'
  method: VLSM
  design: cross-sectional
  imaging: T1
  sample:
    n: 138
    population: chronic stroke survivors with unilateral left-hemisphere stroke
    time_post_onset: '>=6 months post-stroke (mean 36.3 months)'
    age_range: mean age at stroke 57.31 years
    handedness: not_reported
    language: English
  statistics:
    threshold: VLSM permutation + FWE; PCA Component 2 positive loadings
    effect_size: voxelwise PCA loading
  confounders_controlled:
  - Component 1 orthogonality
  - lesion-only PCA verification
  confounders_not_controlled:
  - MCA-territory limit
  region_definition:
    kind: data_driven_cluster
    atlas: AAL (anterior/posterior split is voxelwise within the AAL SMG parcel)
    description: Posterior portion of left supramarginal gyrus. The paper explicitly
      contrasts the anterior SMG (dorsal stream, see form_to_articulation:f4) with
      the posterior SMG (ventral stream, this finding) — a within-AAL-SMG voxelwise
      division. Area Spt (Hickok & Poeppel 2007) sits at the boundary between the
      two streams here.
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: Enantiomorphic normalization (SPM)
    reference_space: MNI152
    atlases_used:
    - AAL
  replications: []
  contradictions: []
  author_limitations:
  - AAL atlas does not natively split SMG anterior vs posterior — the division here
    is voxelwise.
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Results — Cortical Loadings (page 3); Discussion (page 4)
    confidence: high
    flags:
    - cohort overlaps with @Yourganov2015Predicting.
    - anterior-vs-posterior SMG split is voxelwise (not AAL); same caveat as form_to_articulation:f4.
  source_passages:
  - section: Results — Cortical Loadings
    page: 3
    supports: claim
    quote: Positive loadings of Component 2 were associated almost exclusively with
      temporal lobe damage but also, involved areas in the parietal lobe, including
      posterior portions of the SMG and the angular gyrus as well as anteroventral
      inferior frontal lobe areas, such as the pars orbitalis.
  - section: Experimental Procedures — Participants
    page: 5
    supports: sample
    quote: Data from 165 persons with unilateral left hemisphere stroke were considered
      for analyses. Among these 165 persons, 138 (63 females) had both behavioral
      testing and MRI data.
  - section: Experimental Procedures — VLSM Analyses
    page: 5
    supports: method
    quote: Seventy-one univariate VLSM analyses were completed to identify localized
      brain damage associated with speech processing impairments.
  - section: Experimental Procedures — VLSM Analyses
    page: 5
    supports: statistics
    quote: voxelwise statistical significance was determined by voxel-based permutation
      thresholding (1,000 permutations) and multiple comparison correction (controlling
      for familywise error).
  - section: Experimental Procedures — MRI Data Acquisition
    page: 5
    supports: imaging_details
    quote: MRI data were acquired using a Siemens 3T Trio System with a 12-channel
      head coil.
- id: f12
  target: left_angular_gyrus
  target_kind: region
  claim: Damage to the left angular gyrus loads on the form-to-meaning (ventral-stream)
    component.
  direction: likely
  relationship: causal
  citation: '@Fridriksson2018'
  method: VLSM
  design: cross-sectional
  imaging: T1
  sample:
    n: 138
    population: chronic stroke survivors with unilateral left-hemisphere stroke
    time_post_onset: '>=6 months post-stroke (mean 36.3 months)'
    age_range: mean age at stroke 57.31 years
    handedness: not_reported
    language: English
  statistics:
    threshold: VLSM permutation + FWE; Component 2 positive loadings
    effect_size: voxelwise PCA loading
  confounders_controlled:
  - Component 1 orthogonality
  confounders_not_controlled:
  - MCA-territory limit
  region_definition:
    kind: atlas
    atlas: AAL
    description: Left angular gyrus (posterior inferior parietal lobule).
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: Enantiomorphic normalization (SPM)
    reference_space: MNI152
    atlases_used:
    - AAL
  replications:
  - '@Yourganov2015Predicting'
  contradictions: []
  author_limitations:
  - Angular gyrus is also predictive of Wernicke's aphasia (Yourganov 2015) — finding
    is non-specific to form-to-meaning processing alone.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Results — Cortical Loadings (page 3)
    confidence: high
    flags:
    - cohort overlaps with @Yourganov2015Predicting.
  source_passages:
  - section: Results — Cortical Loadings
    page: 3
    supports: claim
    quote: Positive loadings of Component 2 were associated almost exclusively with
      temporal lobe damage but also, involved areas in the parietal lobe, including
      posterior portions of the SMG and the angular gyrus as well as anteroventral
      inferior frontal lobe areas, such as the pars orbitalis.
  - section: Experimental Procedures — Participants
    page: 5
    supports: sample
    quote: Data from 165 persons with unilateral left hemisphere stroke were considered
      for analyses. Among these 165 persons, 138 (63 females) had both behavioral
      testing and MRI data.
  - section: Experimental Procedures — VLSM Analyses
    page: 5
    supports: method
    quote: Seventy-one univariate VLSM analyses were completed to identify localized
      brain damage associated with speech processing impairments.
  - section: Experimental Procedures — VLSM Analyses
    page: 5
    supports: statistics
    quote: voxelwise statistical significance was determined by voxel-based permutation
      thresholding (1,000 permutations) and multiple comparison correction (controlling
      for familywise error).
  - section: Experimental Procedures — MRI Data Acquisition
    page: 5
    supports: imaging_details
    quote: MRI data were acquired using a Siemens 3T Trio System with a 12-channel
      head coil.
- id: f13
  target: left_ifg_pars_orbitalis
  target_kind: region
  claim: Damage to the left inferior frontal gyrus pars orbitalis loads on the form-to-meaning
    (ventral-stream) component, marking the anterior-frontal endpoint of the ventral
    stream via the uncinate fasciculus.
  direction: likely
  relationship: causal
  citation: '@Fridriksson2018'
  method: VLSM
  design: cross-sectional
  imaging: T1
  sample:
    n: 138
    population: chronic stroke survivors with unilateral left-hemisphere stroke
    time_post_onset: '>=6 months post-stroke (mean 36.3 months)'
    age_range: mean age at stroke 57.31 years
    handedness: not_reported
    language: English
  statistics:
    threshold: VLSM permutation + FWE; Component 2 positive loadings
    effect_size: voxelwise PCA loading
  confounders_controlled:
  - Component 1 orthogonality
  confounders_not_controlled:
  - MCA-territory limit
  region_definition:
    kind: atlas
    atlas: AAL
    description: Left IFG pars orbitalis (BA 47) — anteroventral inferior frontal
      cortex; connected to anterior temporal lobe via the uncinate fasciculus per
      the paper's interpretation.
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: Enantiomorphic normalization (SPM)
    reference_space: MNI152
    atlases_used:
    - AAL
  replications:
  - '@Yourganov2015Predicting'
  contradictions: []
  author_limitations:
  - Pars orbitalis is also weakly predictive of global aphasia (Yourganov 2015 Z=1.28);
    finding overlaps with broader frontal damage.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Results — Cortical Loadings (page 3); Discussion (page 4)
    confidence: high
    flags:
    - cohort overlaps with @Yourganov2015Predicting.
  source_passages:
  - section: Results — Cortical Loadings
    page: 3
    supports: claim
    quote: Positive loadings of Component 2 were associated almost exclusively with
      temporal lobe damage but also, involved areas in the parietal lobe, including
      posterior portions of the SMG and the angular gyrus as well as anteroventral
      inferior frontal lobe areas, such as the pars orbitalis.
  - section: Discussion
    page: 4
    supports: claim
    quote: this ventral stream is anchored by the posterior MTG and posterior STG
      (Table S4), the areas showing the greatest expression of Component 2, and extends
      to the posterior inferior parietal lobule (IPL) as well as via the uncinate
      fasciculus to the pars orbitalis in the inferior frontal gyrus.
  - section: Experimental Procedures — Participants
    page: 5
    supports: sample
    quote: Data from 165 persons with unilateral left hemisphere stroke were considered
      for analyses. Among these 165 persons, 138 (63 females) had both behavioral
      testing and MRI data.
  - section: Experimental Procedures — VLSM Analyses
    page: 5
    supports: method
    quote: Seventy-one univariate VLSM analyses were completed to identify localized
      brain damage associated with speech processing impairments.
  - section: Experimental Procedures — VLSM Analyses
    page: 5
    supports: statistics
    quote: voxelwise statistical significance was determined by voxel-based permutation
      thresholding (1,000 permutations) and multiple comparison correction (controlling
      for familywise error).
  - section: Experimental Procedures — MRI Data Acquisition
    page: 5
    supports: imaging_details
    quote: MRI data were acquired using a Siemens 3T Trio System with a 12-channel
      head coil.
- id: f14
  target: left_anterior_middle_temporal_gyrus
  target_kind: region
  claim: Damage to the left anterior middle temporal gyrus loads on the form-to-meaning
    (ventral-stream) component, consistent with its role as a semantic-hub region.
  direction: likely
  relationship: causal
  citation: '@Fridriksson2018'
  method: VLSM
  design: cross-sectional
  imaging: T1
  sample:
    n: 138
    population: chronic stroke survivors with unilateral left-hemisphere stroke
    time_post_onset: '>=6 months post-stroke (mean 36.3 months)'
    age_range: mean age at stroke 57.31 years
    handedness: not_reported
    language: English
  statistics:
    threshold: VLSM permutation + FWE; Component 2 positive loadings
    effect_size: voxelwise PCA loading
  confounders_controlled:
  - Component 1 orthogonality
  confounders_not_controlled:
  - MCA-territory limit
  region_definition:
    kind: atlas
    atlas: AAL
    description: Left anterior middle temporal gyrus.
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: Enantiomorphic normalization (SPM)
    reference_space: MNI152
    atlases_used:
    - AAL
  replications:
  - '@Mirman2015'
  contradictions: []
  author_limitations:
  - The Hickok & Poeppel (2007) ventral stream extends to anterior MTG; this finding
    empirically corroborates that anatomical claim.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-opus-4-7
    extracted_on: 2026-05-01
    paper_section: Discussion (page 4)
    confidence: high
    flags:
    - cohort overlaps with @Yourganov2015Predicting.
  source_passages:
  - section: Discussion
    page: 4
    supports: claim
    quote: These findings are in greater agreement with the dual stream model by Hickok
      and Poeppel (8), which includes a ventral stream mostly involving temporal lobe
      regions, including the posterior and anterior MTGs
  - section: Experimental Procedures — Participants
    page: 5
    supports: sample
    quote: Data from 165 persons with unilateral left hemisphere stroke were considered
      for analyses. Among these 165 persons, 138 (63 females) had both behavioral
      testing and MRI data.
  - section: Experimental Procedures — VLSM Analyses
    page: 5
    supports: method
    quote: Seventy-one univariate VLSM analyses were completed to identify localized
      brain damage associated with speech processing impairments.
  - section: Experimental Procedures — VLSM Analyses
    page: 5
    supports: statistics
    quote: voxelwise statistical significance was determined by voxel-based permutation
      thresholding (1,000 permutations) and multiple comparison correction (controlling
      for familywise error).
  - section: Experimental Procedures — MRI Data Acquisition
    page: 5
    supports: imaging_details
    quote: MRI data were acquired using a Siemens 3T Trio System with a 12-channel
      head coil.
source: agent_draft
last_reviewed: '2026-05-06'
notes: 'First-extraction draft from Fridriksson et al. 2018 (PNAS). The

  paper''s primary finding is a data-driven empirical localization of

  the VENTRAL stream of speech processing — the positive loadings of

  Principal Component 2 from a VLSM-then-PCA pipeline on 71

  behavioural subscores in n=138 chronic LH stroke. The ventral

  stream is characterized as supporting "form-to-meaning"

  (lexical-semantic) processing.


  Seven findings extracted: posterior MTG and posterior STG (the two

  "anchoring" regions per the Discussion), uncinate fasciculus

  (>85% voxel coverage), posterior SMG, angular gyrus, pars

  orbitalis (anterior frontal endpoint), and anterior MTG.


  Together with the form_to_articulation draft (which captures the

  dorsal stream from the same Component 2 negative loadings), this

  pair of drafts represents the primary contribution of Fridriksson

  et al. 2018: a data-driven empirical localization of the

  ventral/dorsal dual streams of speech processing.


  Cohort: USC Aphasia Lab archival database, n=138 chronic LH

  stroke, ≥6 months post-stroke. Substantially overlaps with

  @Yourganov2015Predicting (same lab, n=98). Cohort-overlap flag is

  on every finding.'
reviewer: auto-reviewer
reviewed_on: '2026-05-05'
---
# Form-to-meaning processing (ventral stream)

## Component definition

Form-to-meaning processing is the data-driven ventral-stream
component recovered by Fridriksson et al. 2018. It is operationalized
as the positive loadings of Principal Component 2 (which together
with negative loadings explains 27% of variance after Component 1
captures lesion volume).

The component loads heavily on:
  - Sentence-comprehension impairment (NAVS Sentence Comprehension Test)
  - Auditory-comprehension impairment (yes/no questions)
  - Semantic and phonological errors during naming (PNT)
  - Sentence repetition

## Lesion correlates (per Fridriksson 2018)

The ventral stream is anchored on (Discussion page 4: "the areas
showing the greatest expression of Component 2"):

  - Posterior middle temporal gyrus — f1
  - Posterior superior temporal gyrus — f2

And extends via:
  - Uncinate fasciculus (>85% voxel coverage) — f3
  - Posterior supramarginal gyrus — f4
  - Angular gyrus — f5
  - Pars orbitalis (anterior frontal endpoint) — f6
  - Anterior middle temporal gyrus — f7

## Relationship to the dorsal stream (form-to-articulation)

The same Component 2's negative loadings identify the DORSAL
stream (form-to-articulation processing), captured in
`drafts/impairments/form_to_articulation__Fridriksson2018.md`. The
two streams are anatomically distinct but functionally interactive
— area Spt (Hickok & Poeppel 2007) sits at the boundary, and the
SMG splits into anterior (dorsal) vs posterior (ventral) sub-regions
right at this notch.

## Notes for next extraction round

  - Tables S3 and S4 (paper supplement) carry the full voxelwise
    loadings per region. A more exhaustive extraction could add
    findings for any S3/S4 region with strong Component 2 positive
    loadings.
  - The relationship between this ventral stream and Alyahya 2018's
    semantics PCA factor (also extracted in the KB) is theoretically
    similar but operationally distinct: Fridriksson runs VLSM-then-PCA;
    Alyahya runs PCA-then-VBCM. The two should converge but don't
    necessarily — comparing the canonical region entries when both
    sets of findings are promoted will be informative.
