---
schema_version: 2.3
id: left_supramarginal_gyrus_premotor
name: Left Supramarginal Gyrus and Premotor Cortex (supra-Sylvian)
kind: classical
status: approved
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-06
hemisphere: left
aliases:
- left supramarginal gyrus
- left SMG
- left inferior postcentral gyrus
- left premotor cortex (speech production)
- left supra-Sylvian speech production region
- dorsal speech production route
networks:
- dorsal_language
notes: 'Draft created 2026-05-06 from Mirman et al. 2015 (Nat Commun 6:6762).

  This entry captures the VLSM finding for the Speech Production factor:

  a supra-Sylvian cluster centered on the supramarginal gyrus, extending

  anteriorly into inferior postcentral, precentral, and premotor cortex.

  This is part of the dorsal language pathway. Figure 4 shows this cluster

  in blue-green, with approximate coronal slices from y = 18 to y = -49,

  z = 5 to z = 20.

  '
findings:
- id: f1
  target: speech_production_phonological
  target_kind: impairment
  claim: 'Lesions in the left supramarginal gyrus and adjacent supra-Sylvian cortex
    (extending anteriorly into inferior postcentral, precentral, and premotor cortex)
    are associated with phonological/articulatory speech production deficits in chronic
    post-stroke aphasia, as captured by a Speech Production factor loading on word
    repetition, nonword repetition, and phonological error rate in picture naming.

    '
  direction: likely
  relationship: causal
  citation: '@Mirman2015'
  method: VLSM
  design: cross-sectional
  imaging: multimodal
  sample:
    n: 99
    population: chronic left-hemisphere stroke survivors with aphasia
    time_post_onset: mean 53 months post-onset (SD 68; range 1–381); 83% chronic (≥6
      months)
    age_range: mean 58 years (SD 11; range 26–79)
    handedness: premorbid right-handed
    language: English as primary language
    recruitment: Philadelphia aphasia registry (Moss Rehabilitation Research Institute
      / University of Pennsylvania).
    inclusion_criteria: ≥1 month post aphasia onset secondary to stroke; living at
      home; medically stable; CT or MRI-confirmed left hemisphere cortical lesion;
      completed all 17 tests.
    exclusion_criteria: left-handed premorbidly; right hemisphere or bilateral lesions;
      did not complete full battery.
  statistics:
    threshold: FDR q = 0.05; isolated clusters ≤50 voxels removed
    cluster_extent: null
    effect_size: t-range approximately -2.73 to -5.75 (from Figure 4 colour bar)
    ci_95: not_reported
    p_value: not_reported
  confounders_controlled:
  - total lesion volume (direct lesion-volume control)
  confounders_not_controlled:
  - time post-onset
  - age
  - education / premorbid IQ
  - aphasia subtype
  region_definition:
    kind: data_driven_cluster
    description: 'VLSM cluster for Speech Production factor located superior to the
      Sylvian fissure, centred on the supramarginal gyrus and extending anteriorly
      into inferior postcentral, precentral, and premotor cortex. Shown in blue-green
      in Figure 4. Approximate coronal extent y ≈ -49 to 18 (MNI); approximate z ≈
      5 to 20. Note: the cluster does NOT include inferior prefrontal cortex (Broca''s
      area / pars triangularis/opercularis) or posterior planum temporale or posterior
      superior temporal gyrus (Wernicke''s area), which were not found to be part
      of the dorsal production route in this study.

      '
  imaging_details:
    field_strength: 3T (primary); 1.5T for 6 participants; CT for 37 participants
    acquisition:
      sequence: MPRAGE (MRI) or CT (60 axial slices, 3 mm thick)
      voxel_size_mm:
      - 1
      - 1
      - 1
      TR_ms: 1620
      TE_ms: 3.87
    preprocessing_pipeline: 'MRI registered to custom scanner-specific template then
      MNI152 ''Colin27''. CT drawn on Colin27 after pitch rotation. Lesions manually
      segmented blinded to behaviour. VLSM in SPM8, 1000 permutations, FDR q = 0.05.

      '
    reference_space: MNI152
    atlases_used: []
    coordinates_reported:
    - region: left supramarginal gyrus / premotor (Speech Production cluster)
      mni:
      - null
      - null
      - null
      note: Exact MNI peak not reported numerically. Approximate range visible in
        Figure 4.
  replications:
  - '@Schwartz2012'
  - '@Buchsbaum2011'
  - '@Fridriksson2010'
  contradictions: []
  author_limitations:
  - Did not find evidence for inferior prefrontal cortex (Broca's area) in the dorsal
    production route — differs from some influential dual-pathway models.
  - Cross-sectional design; cannot infer recovery trajectory.
  - Only left hemisphere studied.
  - Anatomical alignment of lesions does not guarantee functional alignment.
  - VLSM lesion overlap requires ≥10 participants; low-coverage regions may be undetectable.
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results – Voxel-based lesion–symptom mapping (page 3); Discussion
      (pages 4–5); Figure 4
    confidence: high
    flags:
    - Exact MNI peak coordinates not reported numerically; approximate range read
      from Figure 4 panel labels.
    - t-statistic range read from Figure 4 colour bar (blue-green scale); verify in
      supplementary.
    - Replication citations (Schwartz 2012, Buchsbaum 2011, Fridriksson 2010) cited
      by Mirman et al. in Discussion — check exact citation keys in citations.md.
    - Note that Broca's area was specifically NOT found in this VLSM — important negative
      finding documented in region_definition.description.
  source_passages:
  - section: Results – Voxel-based lesion–symptom mapping
    page: 4
    supports: claim
    quote: 'VLSM of the Speech Production factor identiﬁed a region superior to the
      Sylvian ﬁssure, primarily in the supramarginal gyrus and extending anteriorly
      into inferior postcentral, pre- central and premotor cortex (Fig. 4, blue–green).
      These regions form part of the dorsal language pathway of dual-pathway models
      and have been shown in other reports to be involved in speech production.

      '
  - section: Discussion
    page: 5
    supports: claim
    quote: 'In the present study, the dorsal speech production route extends superior
      to the Sylvian ﬁssure, from the supramarginal gyrus through inferior postcentral
      and precentral sensorimotor regions to premotor cortical regions involved in
      articulatory motor control.

      '
  - section: Discussion
    page: 5
    supports: region_definition
    quote: 'We did not ﬁnd evidence to support the inclusion of inferior prefrontal
      cortex (Broca''s area), posterior planum temporale or posterior superior temporal
      gyrus (Wernicke''s area) in the dorsal speech production route.

      '
  - section: Discussion
    page: 5
    supports: claim
    quote: 'The peri-Sylvian regions involved in phonological processing were further
      subdivided into supra-Sylvian regions for speech production and infra-Sylvian
      regions for speech recognition.

      '
  - section: Methods – Participants
    page: 7
    supports: sample
    quote: 'The sample consisted of 43 women and 56 men, 48 African Americans and
      51 Caucasians. They averaged 58 years of age (s.d. ¼ 11; range ¼ 26–79), 14
      years of education (s.d. ¼ 3; range ¼ 10–21) and 53 months post onset of stroke
      (s.d. ¼ 68; range ¼ 1–381).

      '
  - section: Methods – Lesion analysis
    page: 7
    supports: method
    quote: 'VLSM analysis was performed by running a simple regression analysis at
      each voxel, with the lesion status as the independent variable and the factor
      score as the dependent variable. To control the effect of total lesion volume,
      each lesion map was normalized to have a unit norm.

      '
  - section: Methods – Lesion analysis
    page: 8
    supports: statistics
    quote: 'The derived statistical p-map was thresholded with FDR q ¼ 0.05 (Semantic
      Recognition factor was thresholded with FDR q ¼ 0.1) and isolated clusters with
      voxel number no more than 50 after thresholding were removed.

      '
  - section: Discussion – Limitations
    page: 7
    supports: limitation
    quote: 'Anatomical alignment of lesions does not guarantee functional alignment
      due to individual differences in functional organization and re-organization
      following stroke; however, large-scale studies such as this one provide the
      best evidence regarding aspects of functional organization that are consistent
      across individuals.

      '
source: draft
last_reviewed: null
reviewer: claude-cowork
reviewed_on: '2026-05-06'
---
# Left Supramarginal Gyrus and Premotor Cortex (supra-Sylvian)

## Anatomical context

The supramarginal gyrus (SMG) sits at the junction of the inferior parietal
lobule and the posterior superior temporal gyrus, just superior to the Sylvian
fissure. The VLSM cluster in Mirman et al. 2015 extends anteriorly from the
SMG into inferior postcentral gyrus (primary somatosensory cortex for the
mouth/larynx), precentral gyrus (primary motor cortex), and premotor cortex.
This is the anatomical substrate of the dorsal speech production pathway.

## Lesion-symptom evidence

Finding f1 (Mirman et al. 2015, n = 99, VLSM): damage to this supra-Sylvian
cluster is associated with phonological/articulatory speech production deficits.
The Speech Production factor captured by PCA loaded on word repetition, nonword
repetition, and phonological error rate in picture naming.

## Key negative finding

The paper explicitly reports that Broca's area (inferior prefrontal cortex),
posterior planum temporale, and posterior superior temporal gyrus (Wernicke's
area) were NOT part of this dorsal production cluster. This represents a
significant departure from some classical dual-pathway models that place the
dorsal route through these frontal regions.

## Comparison to adjacent region

The infra-Sylvian complement (left superior temporal gyrus / Wernicke's area)
is captured in a separate draft entry and was associated with the Speech
Recognition factor — not speech production. Together, the two clusters provide
a superior/inferior dissociation within peri-Sylvian cortex.
