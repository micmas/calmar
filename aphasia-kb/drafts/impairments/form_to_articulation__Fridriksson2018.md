---
schema_version: 2.3
id: form_to_articulation
name: "Form-to-articulation processing (dorsal stream)"
aliases:
  - dorsal stream (speech processing)
  - phonological-motor processing
  - motor-phonological speech processing
kind: impairment
status: draft
created_by: "agent:claude-opus-4-7"
created_on: 2026-05-01
short_definition: "Underlying processing component for the motor-phonological aspects of speech: articulation, phonological encoding for production, and motor planning. Operationally defined as the negative loadings of Principal Component 2 in Fridriksson et al. 2018, indexed by apraxia-of-speech severity, articulation errors during picture naming, total verbal output in connected speech, and spoken phonological errors."
assessment:
  - "Apraxia Battery for Adults, second edition (ABA-2)"
  - "Apraxia of Speech Rating Scale (ASRS)"
  - "Philadelphia Naming Test (PNT) — articulation/phonological error scoring"
  - "Connected speech analysis — total verbal output (Grandfather Passage, picture description)"

findings:
  - id: f1
    target: ho-cort_44
    target_kind: region
    claim: "Damage to the left inferior frontal gyrus pars opercularis loads strongly on the form-to-articulation (dorsal-stream) processing component in chronic post-stroke aphasia, identifying it as part of the dorsal speech-processing stream that supports motor-phonological aspects of speech production."
    direction: likely
    relationship: causal
    citation: "@Fridriksson2018"
    method: VLSM
    design: cross-sectional
    imaging: T1
    sample:
      n: 138
      population: "chronic stroke survivors with unilateral left-hemisphere stroke (subset n=138 with both behavioural and MRI data; per-test n ranged 38–138)"
      time_post_onset: ">=6 months post-stroke; mean 36.3 months (SD 43.6)"
      age_range: "mean age at stroke 57.31 years (SD 11.49)"
      handedness: "not_reported"
      language: "English (recruited at University of South Carolina, USA)"
      recruitment: "archival database of the Aphasia Laboratory, University of South Carolina; participants enrolled across multiple aphasia treatment and neuropsychological-research studies."
      inclusion_criteria: "unilateral left-hemisphere stroke; ≥6 months post-stroke; behavioural testing + MRI."
      exclusion_criteria: "not_reported beyond imaging-quality and lesion-mask review."
    statistics:
      threshold: "univariate VLSM with voxel-based permutation thresholding (1000 permutations) and family-wise-error multiple-comparison correction; voxels included only if ≥5 patients had damage. Component 2 explained 27% of total variance; voxelwise loadings range -0.003 to +0.003 (negative loadings index form-to-articulation)."
      cluster_extent: null
      effect_size: "voxelwise PCA loading on Component 2 (negative direction); exact peak Z not provided in main text — see Tables S3 and S4 of the paper for the per-region rank."
      ci_95: "not_reported"
      p_value: "not_reported per-region (PCA-derived loading)"
    confounders_controlled:
      - "lesion volume — Component 1 (47% variance) captured the lesion-volume / lesion-overlap pattern (r=-0.78 with the cohort lesion-overlap map); Component 2 is orthogonal to Component 1, so the form-to-articulation loadings are independent of overall lesion extent."
      - "vascular distribution — verified by multiplying the Component 2 brain map by a binary-lesion-only PCA component (Component 2b in Fig. 1), to show the loadings are not merely the anterior-vs-posterior MCA distribution."
    confounders_not_controlled:
      - "age, time post-stroke, sex (n=63 female of n=138 total)"
      - "behavioural battery completeness varied (per-test n 38–138)"
      - "vascular constraint — coverage limited to left-MCA territory"
    region_definition:
      kind: data_driven_cluster
      atlas: "anatomical labels from MNI-space atlases (paper Tables S3 and S4 list the AAL labels per cluster)"
      description: "Voxelwise PCA loading; pars opercularis is the highest-expression region of Component 2 negative loadings per the Discussion (page 4 of 6). Lesion damage measured as binarized lesion mask after enantiomorphic normalization (Nachev 2008) to MNI."
    imaging_details:
      field_strength: "3T"
      modalities:
        - modality: "T1"
          sequence: "MP-RAGE / TFE"
          voxel_size_mm: [1, 1, 1]
          TR_ms: 2250
          TI_ms: 925
          TE_ms: 4.15
          notes: "FOV 256×256, 192 sagittal slices, 9° flip, GRAPPA=2, 80 reference lines."
        - modality: "T2"
          sequence: "3D SPACE"
          voxel_size_mm: [1, 1, 1]
          TR_ms: 3200
          TE_ms: 352
          notes: "Lesions demarcated by neurologist (LB) on the T2 image in MRIcron; coregistered to T1 native; warped to MNI; binarized at 50% post-warp."
      preprocessing_pipeline: "dcm2niix → manual lesion drawing on T2 (MRIcron) → coregister T2→T1 → enantiomorphic normalization (Nachev 2008) using SPM unified segmentation-normalization (Ashburner & Friston 2005) and the Clinical Toolbox age-appropriate template → reslice lesion to 1mm³ MNI → binarize at 50%."
      reference_space: "MNI152"
      atlases_used:
        - "AAL (per Tables S3/S4 of the paper)"
        - "Clinical Toolbox age-appropriate template (Rorden et al. 2012)"
    replications:
      - "@Yourganov2015Predicting"
      - "@Saur2008"
    contradictions: []
    author_limitations:
      - "Lesion coverage limited to MCA territory; regions like precuneus rarely affected by stroke — limits generalisability beyond MCA."
      - "Chronic-stroke data may reflect cortical reorganisation, so 'damage to area X predicts impairment Y' partly reflects failed-recovery patterns rather than purely structure-function localisation."
      - "Single behavioural measures don't capture all aspects of comprehension/production — VLSM is therefore mapping a partial proxy."
      - "Acute diaschisis is not a concern for this chronic sample, but is a general caveat for the LSM literature."
    evidence_quality: cohort
    strength: strong
    provenance:
      extracted_by: "agent:claude-opus-4-7"
      extracted_on: 2026-05-01
      paper_section: "Results (Component Loadings + Cortical Loadings, page 3); Discussion (page 4); Tables S3 and S4 (referenced; not in the main text)"
      confidence: high
      flags:
        - "cohort overlaps with @Yourganov2015Predicting — same University of South Carolina Aphasia Lab archival database, overlapping enrolment 2007–2014; flag for downstream double-counting risk in interpret_overlap()."
        - "target uses legacy id `ho-cort_44` rather than the new `left_ifg_pars_opercularis` because the canonical entry already exists at `regions/ho-cort_44.md`; that canonical entry's f1 currently has [PLACEHOLDER] source passages — when promote.py runs, the placeholders should be replaced or this finding should append as `f2`."
    source_passages:
      - section: "Results — Cortical Loadings"
        page: 3
        supports: claim
        quote: "Negative loadings were primarily associated with damage involving the posterior inferior frontal gyrus, including pars opercularis and pars triangularis, lateral premotor cortex, pre- and postcentral gyri, and anterior aspects of the supramarginal gyrus (SMG) as well as the underlying white matter tracts"
      - section: "Discussion"
        page: 4
        supports: claim
        quote: "our cortical regions with the highest expression of negative Component 2 loadings (i.e., the dorsal stream) were the pars opercularis, a region classically considered as the posterior portion of Broca's area, the premotor cortex, and the middle frontal gyrus"
      - section: "Experimental Procedures — Participants"
        page: 5
        supports: sample
        quote: "Data from 165 persons with unilateral left hemisphere stroke were considered for analyses. Among these 165 persons, 138 (63 females) had both behavioral testing and MRI data."
      - section: "Experimental Procedures — Participants"
        page: 5
        supports: sample
        quote: "all participants were at least 6 mo poststroke, with a mean age at the time of stroke of 57.31 y old (SD = 11.49) and a mean time poststroke of 36.3 mo (SD = 43.6)."
      - section: "Experimental Procedures — VLSM Analyses"
        page: 5
        supports: method
        quote: "Seventy-one univariate VLSM analyses were completed to identify localized brain damage associated with speech processing impairments."
      - section: "Experimental Procedures — VLSM Analyses"
        page: 5
        supports: statistics
        quote: "voxelwise statistical significance was determined by voxel-based permutation thresholding (1,000 permutations) and multiple comparison correction (controlling for familywise error). Only voxels where at least five patients had damage were included in each analysis."
      - section: "Experimental Procedures — MRI Data Acquisition"
        page: 5
        supports: imaging_details
        quote: "MRI data were acquired using a Siemens 3T Trio System with a 12-channel head coil. All participants underwent scanning that included two MRI sequences: (i) T1-weighted imaging sequence using an MP-RAGE"
      - section: "Experimental Procedures — Preprocessing of Structural Images"
        page: 5
        supports: imaging_details
        quote: "Preprocessing began with the coregistration of the T2 MRI to match the T1 MRIs, aligning the lesions to native T1 space. Images were warped to standard space using the enantiomorphic"
      - section: "Results — Cortical Loadings"
        page: 3
        supports: confounders
        quote: "we correlated the statistical map representing Component 1 with a lesion overlay map from all 138 participants included in the study sample. The correlation between the two maps was r = −0.78. Correlation between the second component and the lesion overlap map was much smaller: r = 0.04."
      - section: "Discussion"
        page: 4
        supports: limitation
        quote: "lesion studies that rely on stroke data are limited to studying cortical areas where stroke is likely to occur (e.g., middle cerebral artery distribution)"

  - id: f2
    target: left_premotor_cortex
    target_kind: region
    claim: "Damage to the left lateral premotor cortex loads on the form-to-articulation (dorsal-stream) component, identifying it as a critical dorsal-stream speech-production region."
    direction: likely
    relationship: causal
    citation: "@Fridriksson2018"
    method: VLSM
    design: cross-sectional
    imaging: T1
    sample:
      n: 138
      population: "chronic stroke survivors with unilateral left-hemisphere stroke"
      time_post_onset: ">=6 months post-stroke (mean 36.3 months, SD 43.6)"
      age_range: "mean age at stroke 57.31 years (SD 11.49)"
      handedness: "not_reported"
      language: "English"
    statistics:
      threshold: "VLSM with permutation thresholding (1000) + FWE correction; PCA Component 2 negative loadings"
      effect_size: "voxelwise PCA loading; exact peak Z reported in Tables S3/S4 (supporting info)"
    confounders_controlled:
      - "lesion volume captured by Component 1 (orthogonal to Component 2)"
      - "vascular distribution verified via lesion-only PCA"
    confounders_not_controlled:
      - "MCA-territory coverage limit"
      - "chronic-stroke reorganisation"
    region_definition:
      kind: data_driven_cluster
      atlas: "AAL (per Tables S3/S4)"
      description: "Lateral premotor cortex — Brodmann area 6 lateral; named one of the three highest-expression regions of the dorsal-stream Component 2 in the Discussion (page 4)."
    imaging_details:
      field_strength: "3T"
      preprocessing_pipeline: "dcm2niix + manual T2 lesion drawing + enantiomorphic normalization (SPM, Clinical Toolbox)"
      reference_space: "MNI152"
      atlases_used:
        - "AAL"
    replications:
      - "@Saur2008"
    contradictions: []
    author_limitations:
      - "Damage to premotor cortex often co-occurs with damage to pars opercularis (both fed by the superior MCA division); cluster localisation may be partly driven by spatial autocorrelation of MCA-territory infarcts."
    evidence_quality: cohort
    strength: strong
    provenance:
      extracted_by: "agent:claude-opus-4-7"
      extracted_on: 2026-05-01
      paper_section: "Discussion (page 4) — 'highest expression of negative Component 2 loadings'; Results (page 3) — 'lateral premotor cortex'"
      confidence: high
      flags:
        - "cohort overlaps with @Yourganov2015Predicting (same USC archival database)."
    source_passages:
      - section: "Results — Cortical Loadings"
        page: 3
        supports: claim
        quote: "Negative loadings were primarily associated with damage involving the posterior inferior frontal gyrus, including pars opercularis and pars triangularis, lateral premotor cortex, pre- and postcentral gyri, and anterior aspects of the supramarginal gyrus (SMG) as well as the underlying white matter tracts"
      - section: "Discussion"
        page: 4
        supports: claim
        quote: "our cortical regions with the highest expression of negative Component 2 loadings (i.e., the dorsal stream) were the pars opercularis, a region classically considered as the posterior portion of Broca's area, the premotor cortex, and the middle frontal gyrus"
      - section: "Experimental Procedures — Participants"
        page: 5
        supports: sample
        quote: "Data from 165 persons with unilateral left hemisphere stroke were considered for analyses. Among these 165 persons, 138 (63 females) had both behavioral testing and MRI data."
      - section: "Experimental Procedures — VLSM Analyses"
        page: 5
        supports: method
        quote: "Seventy-one univariate VLSM analyses were completed to identify localized brain damage associated with speech processing impairments."
      - section: "Experimental Procedures — VLSM Analyses"
        page: 5
        supports: statistics
        quote: "voxelwise statistical significance was determined by voxel-based permutation thresholding (1,000 permutations) and multiple comparison correction (controlling for familywise error). Only voxels where at least five patients had damage were included in each analysis."
      - section: "Experimental Procedures — MRI Data Acquisition"
        page: 5
        supports: imaging_details
        quote: "MRI data were acquired using a Siemens 3T Trio System with a 12-channel head coil."

  - id: f3
    target: left_middle_frontal_gyrus
    target_kind: region
    claim: "Damage to the left middle frontal gyrus loads on the form-to-articulation (dorsal-stream) component."
    direction: likely
    relationship: causal
    citation: "@Fridriksson2018"
    method: VLSM
    design: cross-sectional
    imaging: T1
    sample:
      n: 138
      population: "chronic stroke survivors with unilateral left-hemisphere stroke"
      time_post_onset: ">=6 months post-stroke (mean 36.3 months)"
      age_range: "mean age at stroke 57.31 years"
      handedness: "not_reported"
      language: "English"
    statistics:
      threshold: "VLSM permutation + FWE; PCA Component 2 negative loadings"
      effect_size: "voxelwise loading per Tables S3/S4"
    confounders_controlled:
      - "lesion volume orthogonalised via Component 1"
      - "vascular pattern via lesion-only PCA"
    confounders_not_controlled:
      - "MCA-territory limit"
    region_definition:
      kind: atlas
      atlas: "AAL"
      description: "Left middle frontal gyrus (dorsolateral prefrontal cortex). Identified as one of the three highest-expression dorsal-stream regions in the Discussion."
    imaging_details:
      field_strength: "3T"
      preprocessing_pipeline: "Enantiomorphic normalization (SPM)"
      reference_space: "MNI152"
      atlases_used:
        - "AAL"
    replications: []
    contradictions: []
    author_limitations:
      - "Middle frontal gyrus is also predictive of global aphasia (Yourganov 2015 Z=2.51) — finding is non-specific to form-to-articulation."
    evidence_quality: cohort
    strength: moderate
    provenance:
      extracted_by: "agent:claude-opus-4-7"
      extracted_on: 2026-05-01
      paper_section: "Discussion (page 4)"
      confidence: high
      flags:
        - "cohort overlaps with @Yourganov2015Predicting."
    source_passages:
      - section: "Discussion"
        page: 4
        supports: claim
        quote: "our cortical regions with the highest expression of negative Component 2 loadings (i.e., the dorsal stream) were the pars opercularis, a region classically considered as the posterior portion of Broca's area, the premotor cortex, and the middle frontal gyrus"
      - section: "Experimental Procedures — Participants"
        page: 5
        supports: sample
        quote: "Data from 165 persons with unilateral left hemisphere stroke were considered for analyses. Among these 165 persons, 138 (63 females) had both behavioral testing and MRI data."
      - section: "Experimental Procedures — VLSM Analyses"
        page: 5
        supports: method
        quote: "Seventy-one univariate VLSM analyses were completed to identify localized brain damage associated with speech processing impairments."
      - section: "Experimental Procedures — VLSM Analyses"
        page: 5
        supports: statistics
        quote: "voxelwise statistical significance was determined by voxel-based permutation thresholding (1,000 permutations) and multiple comparison correction (controlling for familywise error)."
      - section: "Experimental Procedures — MRI Data Acquisition"
        page: 5
        supports: imaging_details
        quote: "MRI data were acquired using a Siemens 3T Trio System with a 12-channel head coil."

  - id: f4
    target: left_anterior_supramarginal_gyrus
    target_kind: region
    claim: "Damage to the anterior portion of the left supramarginal gyrus loads on the form-to-articulation (dorsal-stream) component, marking the inferior-parietal endpoint of the dorsal speech-processing stream."
    direction: likely
    relationship: causal
    citation: "@Fridriksson2018"
    method: VLSM
    design: cross-sectional
    imaging: T1
    sample:
      n: 138
      population: "chronic stroke survivors with unilateral left-hemisphere stroke"
      time_post_onset: ">=6 months post-stroke (mean 36.3 months)"
      age_range: "mean age at stroke 57.31 years"
      handedness: "not_reported"
      language: "English"
    statistics:
      threshold: "VLSM permutation + FWE; Component 2 negative loadings"
      effect_size: "voxelwise PCA loading per Tables S3/S4"
    confounders_controlled:
      - "Component 1 orthogonality"
      - "lesion-only PCA verification"
    confounders_not_controlled:
      - "MCA-territory limit"
      - "chronic-stroke reorganisation"
    region_definition:
      kind: atlas
      atlas: "AAL"
      description: "Anterior portion of the left supramarginal gyrus (inferior parietal lobule). The paper explicitly contrasts the anterior SMG (dorsal stream) with the posterior SMG (ventral stream) — see f4 of the form_to_meaning draft. Area Spt (Hickok & Poeppel 2007) is at the boundary between the two streams."
    imaging_details:
      field_strength: "3T"
      preprocessing_pipeline: "Enantiomorphic normalization (SPM)"
      reference_space: "MNI152"
      atlases_used:
        - "AAL"
    replications:
      - "@Yourganov2015Predicting"
    contradictions: []
    author_limitations:
      - "SMG anterior/posterior split is a key claim of this paper — the AAL atlas does not natively split SMG, so the anterior-vs-posterior division here is voxelwise rather than atlas-based."
    evidence_quality: cohort
    strength: strong
    provenance:
      extracted_by: "agent:claude-opus-4-7"
      extracted_on: 2026-05-01
      paper_section: "Results — Cortical Loadings (page 3)"
      confidence: high
      flags:
        - "cohort overlaps with @Yourganov2015Predicting."
        - "anterior-vs-posterior SMG split is voxelwise (not AAL); when promoting, note that left_anterior_supramarginal_gyrus and left_posterior_supramarginal_gyrus correspond to a within-AAL-SMG voxelwise division rather than separate AAL parcels."
    source_passages:
      - section: "Results — Cortical Loadings"
        page: 3
        supports: claim
        quote: "Negative loadings were primarily associated with damage involving the posterior inferior frontal gyrus, including pars opercularis and pars triangularis, lateral premotor cortex, pre- and postcentral gyri, and anterior aspects of the supramarginal gyrus (SMG) as well as the underlying white matter tracts"
      - section: "Conclusion"
        page: 5
        supports: claim
        quote: "The dorsal stream extends from anterior speech areas, including pars opercularis and premotor areas, to posterior regions in the SMG and straddles the edge of area Spt."
      - section: "Experimental Procedures — Participants"
        page: 5
        supports: sample
        quote: "Data from 165 persons with unilateral left hemisphere stroke were considered for analyses. Among these 165 persons, 138 (63 females) had both behavioral testing and MRI data."
      - section: "Experimental Procedures — VLSM Analyses"
        page: 5
        supports: method
        quote: "Seventy-one univariate VLSM analyses were completed to identify localized brain damage associated with speech processing impairments."
      - section: "Experimental Procedures — VLSM Analyses"
        page: 5
        supports: statistics
        quote: "voxelwise statistical significance was determined by voxel-based permutation thresholding (1,000 permutations) and multiple comparison correction (controlling for familywise error)."
      - section: "Experimental Procedures — MRI Data Acquisition"
        page: 5
        supports: imaging_details
        quote: "MRI data were acquired using a Siemens 3T Trio System with a 12-channel head coil."

  - id: f5
    target: left_precentral_gyrus
    target_kind: region
    claim: "Damage to the left precentral gyrus loads on the form-to-articulation (dorsal-stream) component, consistent with the role of primary motor cortex in articulatory speech output."
    direction: likely
    relationship: causal
    citation: "@Fridriksson2018"
    method: VLSM
    design: cross-sectional
    imaging: T1
    sample:
      n: 138
      population: "chronic stroke survivors with unilateral left-hemisphere stroke"
      time_post_onset: ">=6 months post-stroke (mean 36.3 months)"
      age_range: "mean age at stroke 57.31 years"
      handedness: "not_reported"
      language: "English"
    statistics:
      threshold: "VLSM permutation + FWE; Component 2 negative loadings"
      effect_size: "voxelwise PCA loading"
    confounders_controlled:
      - "lesion volume via Component 1"
    confounders_not_controlled:
      - "MCA-territory limit"
    region_definition:
      kind: atlas
      atlas: "AAL"
      description: "Left precentral gyrus (primary motor cortex)."
    imaging_details:
      field_strength: "3T"
      preprocessing_pipeline: "Enantiomorphic normalization (SPM)"
      reference_space: "MNI152"
      atlases_used:
        - "AAL"
    replications:
      - "@Yourganov2015Predicting"
    contradictions: []
    author_limitations:
      - "Primary motor cortex loadings may partly reflect motor-execution deficits rather than form-to-articulation processing per se — the paper does not separately model dysarthria from apraxia of speech."
    evidence_quality: cohort
    strength: moderate
    provenance:
      extracted_by: "agent:claude-opus-4-7"
      extracted_on: 2026-05-01
      paper_section: "Results — Cortical Loadings (page 3)"
      confidence: high
      flags:
        - "cohort overlaps with @Yourganov2015Predicting."
    source_passages:
      - section: "Results — Cortical Loadings"
        page: 3
        supports: claim
        quote: "Negative loadings were primarily associated with damage involving the posterior inferior frontal gyrus, including pars opercularis and pars triangularis, lateral premotor cortex, pre- and postcentral gyri, and anterior aspects of the supramarginal gyrus (SMG) as well as the underlying white matter tracts"
      - section: "Experimental Procedures — Participants"
        page: 5
        supports: sample
        quote: "Data from 165 persons with unilateral left hemisphere stroke were considered for analyses. Among these 165 persons, 138 (63 females) had both behavioral testing and MRI data."
      - section: "Experimental Procedures — VLSM Analyses"
        page: 5
        supports: method
        quote: "Seventy-one univariate VLSM analyses were completed to identify localized brain damage associated with speech processing impairments."
      - section: "Experimental Procedures — VLSM Analyses"
        page: 5
        supports: statistics
        quote: "voxelwise statistical significance was determined by voxel-based permutation thresholding (1,000 permutations) and multiple comparison correction (controlling for familywise error)."
      - section: "Experimental Procedures — MRI Data Acquisition"
        page: 5
        supports: imaging_details
        quote: "MRI data were acquired using a Siemens 3T Trio System with a 12-channel head coil."

source: agent_draft
last_reviewed: null
notes: |
  First-extraction draft from Fridriksson et al. 2018 (PNAS). The
  paper's primary finding is a data-driven empirical localization of
  the DORSAL stream of speech processing — the negative loadings of
  Principal Component 2 from a VLSM-then-PCA pipeline on 71
  behavioural subscores in n=138 chronic LH stroke. The dorsal
  stream is characterized as supporting "form-to-articulation"
  processing.

  Five findings extracted: pars opercularis (ho-cort_44 — legacy id
  retained), lateral premotor cortex, middle frontal gyrus (the
  three "highest expression" regions per the Discussion), anterior
  supramarginal gyrus (the inferior-parietal endpoint of the dorsal
  stream), and precentral gyrus.

  Component 1 of the same PCA was essentially the lesion-volume
  spatial pattern (47% variance, r=-0.78 with cohort lesion-overlap
  map) — that's a strong replication of "lesion volume → severity"
  but not a region-specific finding, so it is captured in the
  file-level notes here rather than as a separate finding.

  Cohort: USC Aphasia Lab archival database, n=138 chronic LH
  stroke, ≥6 months post-stroke. Substantially overlaps with
  @Yourganov2015Predicting (same lab, n=98, same enrolment window
  2007–2014). The flag for cross-paper cohort overlap is on every
  finding here.

  Important note for promote.py: the canonical `regions/ho-cort_44.md`
  already cites @Fridriksson2018 in its `f1` finding but with
  `[PLACEHOLDER]` source passages. When promoting f1 of THIS draft,
  the placeholders in the canonical entry should be replaced with the
  real source_passages from this draft (or this draft's f1 should
  append as a new finding `f2` and the placeholder `f1` should be
  flagged for deletion or completion).
---

# Form-to-articulation processing (dorsal stream)

## Component definition

Form-to-articulation processing is the data-driven dorsal-stream
component recovered by Fridriksson et al. 2018 from a VLSM-then-PCA
analysis on n=138 chronic LH stroke patients. It is operationalized
as the negative loadings of Principal Component 2 (which together
with positive loadings explains 27% of variance after Component 1
captures lesion volume).

The component loads heavily on:
  - Apraxia-of-speech severity (ABA-2; Apraxia of Speech Rating Scale)
  - Articulation errors during picture naming (PNT)
  - Total verbal output in connected speech (Cookie theft, Grandfather Passage)
  - Spoken phonological errors

## Lesion correlates (per Fridriksson 2018)

The dorsal stream is anchored on (Discussion page 4 highlights the
top three):

  - IFG pars opercularis (the canonical Broca's area, `ho-cort_44`) — f1
  - Lateral premotor cortex — f2
  - Middle frontal gyrus — f3

Plus extending to:
  - Anterior supramarginal gyrus (inferior parietal endpoint) — f4
  - Precentral gyrus (primary motor cortex) — f5

Adjacent white-matter tracts also load on the dorsal stream but are
not extracted here as separate findings (the paper does not name
specific tracts in its main text — see Tables S3/S4 for the full
voxelwise list).

## Relationship to the ventral stream (form-to-meaning)

The same Component 2's positive loadings identify the VENTRAL
stream (form-to-meaning processing), captured in
`drafts/impairments/form_to_meaning__Fridriksson2018.md`. The two
streams are anatomically distinct but functionally interactive — the
paper notes that conduction aphasia (impaired interaction between
the streams at area Spt) and Wernicke's aphasia (ventral damage with
secondary production effects) both illustrate the cross-stream
interaction.

## Notes for next extraction round

  - The canonical `regions/ho-cort_44.md` has placeholder source
    passages for its existing Fridriksson 2018 finding. promote.py
    should replace the placeholders with the real passages from this
    draft.
  - Tables S3 and S4 (paper supplement) contain the full voxelwise
    loadings per region. A future, more thorough extraction could
    add additional findings for any S3/S4 region with a strong
    Component 2 negative loading.
