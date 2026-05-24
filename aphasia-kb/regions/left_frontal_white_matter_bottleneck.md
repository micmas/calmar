---
schema_version: 2.3
id: left_frontal_white_matter_bottleneck
name: Left Frontal White Matter Bottleneck
kind: tract
status: approved
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-06
hemisphere: left
aliases:
- left deep frontal white matter
- left periinsular white matter (medial to insula, lateral to basal ganglia)
- left uncinate/IFOF/ATR convergence zone
- Anterior corona radiata L
- Anterior corona radiata left
- Posterior limb of internal capsule L
- Posterior limb of internal capsule left
- Anterior limb of internal capsule L
- Anterior limb of internal capsule left
networks:
- ventral_semantic
- frontal_semantic_control
notes: 'Draft created 2026-05-06 from Mirman et al. 2015 (Nat Commun 6:6762).

  This entry captures the VLSM finding for the Semantic Recognition factor:

  damage to a white matter region medial to the insula and lateral to the

  basal ganglia (where the uncinate fasciculus, inferior fronto-occipital

  fasciculus, and anterior thalamic radiations converge) is associated with

  multimodal semantic recognition deficits. The authors call this a "frontal

  white matter bottleneck." MNI coordinates from Figure 3: cluster at

  approximately x = -19, z = 4, y = 28 (from panel labels in Figure 3 legend).

  This is a DISTINCT region from the left ATL — the two findings are

  dissociated in the same dataset.

  '
findings:
- id: f1
  target: semantic_recognition_multimodal
  target_kind: impairment
  claim: 'Lesions in the left deep frontal white matter (medial to the insula, lateral
    to the basal ganglia), where the uncinate fasciculus, inferior fronto-occipital
    fasciculus, and anterior thalamic radiations converge, are associated with multimodal
    semantic recognition deficits (verbal and non-verbal) in chronic post-stroke aphasia.

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
      home; medically stable; no major psychiatric or neurological co-morbidities;
      CT or MRI-confirmed left hemisphere cortical lesion; completed all 17 tests.
    exclusion_criteria: left-handed premorbidly; right hemisphere or bilateral lesions;
      did not complete full battery.
  statistics:
    threshold: 'FDR q = 0.1 (relaxed threshold; note: all other factors used q = 0.05);
      isolated clusters ≤50 voxels removed'
    cluster_extent: null
    effect_size: not_reported (colour bar range not legible from text)
    ci_95: not_reported
    p_value: not_reported
  confounders_controlled:
  - 'total lesion volume (direct lesion-volume control: lesion maps normalised to
    unit norm before regression)'
  confounders_not_controlled:
  - time post-onset
  - age
  - education / premorbid IQ
  - aphasia subtype
  region_definition:
    kind: data_driven_cluster
    description: 'VLSM cluster for the Semantic Recognition factor located in white
      matter medial to the insula and lateral to the basal ganglia. Overlaps with
      the convergence zone of three major tracts: uncinate fasciculus, inferior fronto-occipital
      fasciculus (IFOF), and anterior thalamic radiations (ATR). The cluster does
      NOT include the superior longitudinal fasciculus / arcuate fasciculus. Figure
      3 shows approximate MNI coordinates z = 4, y = 28, x = -19 from panel labels.
      Tracts overlaid using ICBM-DTI white matter tractography atlas (FSL) at 20%
      probability threshold.

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
    preprocessing_pipeline: 'MRI registered to custom scanner-specific template, then
      to MNI152 ''Colin27'' volume. CT lesions drawn directly onto Colin27 after pitch
      rotation. Lesions manually segmented, blinded to behaviour. VLSM in SPM8 with
      1000-permutation test. White matter tracts rendered using ICBM-DTI tractography
      atlas from FSL (Mori et al. 2005; Wakana et al. 2007; Hua et al. 2008) at 20%
      probability threshold.

      '
    reference_space: MNI152
    atlases_used:
    - ICBM-DTI white matter tractography atlas (FSL)
    coordinates_reported:
    - region: left frontal white matter bottleneck (Semantic Recognition cluster)
      mni:
      - -19
      - 28
      - 4
      note: Approximate, read from Figure 3 panel labels (x, y, z). Verify against
        supplementary materials.
  replications: []
  contradictions: []
  author_limitations:
  - Only left hemisphere lesions studied; cannot address hemispheric lateralisation
    of this white matter region.
  - Results do not identify critical sub-regions within the functionally and anatomically
    heterogeneous inferior and middle portions of the frontal lobe.
  - Relaxed FDR threshold (q = 0.1) used for Semantic Recognition — results are less
    statistically conservative than the other three VLSM analyses.
  - Lesion coverage poor in ventral and inferolateral temporal cortex.
  - Anatomical alignment of lesions does not guarantee functional alignment due to
    individual differences in functional reorganisation.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results – Voxel-based lesion–symptom mapping (pages 3–4); Discussion
      (pages 4–5); Figure 3
    confidence: high
    flags:
    - Semantic Recognition factor used relaxed FDR q = 0.1 (vs q = 0.05 for other
      factors) — strength rated moderate not strong for this reason.
    - MNI coordinates (-19, 28, 4) read from Figure 3 panel labels (x, y, z slices);
      should be verified against supplementary data.
    - The effect size / t-value colour bar for this factor not clearly specified in
      text — flagged.
    - Whether the IFOF/uncinate/ATR cluster overlaps with the external capsule or
      corona radiata is not specified — future users should cross-reference with atlas.
  source_passages:
  - section: Results – Voxel-based lesion–symptom mapping
    page: 4
    supports: claim
    quote: 'VLSM of the Semantic Recognition factor identiﬁed no voxels in the ATL,
      even at a relaxed q ¼ 0.1 False Discovery Rate (FDR) threshold (Fig. 3), nor
      were there voxels in any other cortical region typically associated with semantic
      processing, such as the middle temporal gyrus or the angular gyrus. Instead,
      the identiﬁed voxels were primarily in the white matter medial to the insula
      and lateral to the basal ganglia.

      '
  - section: Results – Voxel-based lesion–symptom mapping
    page: 4
    supports: region_definition
    quote: 'Several white matter tracts converge in this region, including the inferior
      fronto-occipital fasciculus, the uncinate fasciculus and the anterior thalamic
      radiations. The region did not include the superior longitudinal fasciculus
      (SLF III, which on some accounts corresponds to the fronto-parietal portion
      of the arcuate fasciculus).

      '
  - section: Discussion
    page: 6
    supports: claim
    quote: 'they arise from damage to a frontal white matter bottleneck—a region where
      the uncinate fasciculus, inferior fronto-occipital fasciculus and anterior thalamic
      radiations all converge. We suggest that this convergence produces a vulnerable
      location where a small amount of damage can have large functional consequences
      affecting semantic processing of both verbal and non-verbal (visual) input.

      '
  - section: Results – Voxel-based lesion–symptom mapping
    page: 4
    supports: claim
    quote: 'The convergence of major white matter tracts in the identiﬁed area creates
      a ''bottleneck'' where a small amount of damage can cause a large degree of
      dysfunction in connections between frontal cortices and the rest of the brain.

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
    page: 8
    supports: statistics
    quote: 'The derived statistical p-map was thresholded with FDR q ¼ 0.05 (Semantic
      Recognition factor was thresholded with FDR q ¼ 0.1) and isolated clusters with
      voxel number no more than 50 after thresholding were removed.

      '
  - section: Methods – Lesion analysis
    page: 8
    supports: imaging_details
    quote: 'The white matter tracts in Fig. 3 were based on the ICBM-DTI white matter
      tractography atlas from FSL using a 20% probability threshold.

      '
  - section: Discussion – Limitations
    page: 6
    supports: limitation
    quote: 'the present results do not identify critical sub-regions within the functionally
      and anatomically heterogeneous inferior and middle portions of the frontal lobe.

      '
- id: f2
  target: semantic_recognition_multimodal
  target_kind: impairment
  claim: 'Lesions in the left deep frontal white matter (medial to the insula, lateral
    to the basal ganglia), where the uncinate fasciculus, inferior fronto-occipital
    fasciculus, and anterior thalamic radiations converge, are associated with multimodal
    semantic recognition deficits (verbal and non-verbal) in chronic post-stroke aphasia.

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
      home; medically stable; no major psychiatric or neurological co-morbidities;
      CT or MRI-confirmed left hemisphere cortical lesion; completed all 17 tests.
    exclusion_criteria: left-handed premorbidly; right hemisphere or bilateral lesions;
      did not complete full battery.
  statistics:
    threshold: 'FDR q = 0.1 (relaxed threshold; note: all other factors used q = 0.05);
      isolated clusters ≤50 voxels removed'
    cluster_extent: null
    effect_size: not_reported (colour bar range not legible from text)
    ci_95: not_reported
    p_value: not_reported
  confounders_controlled:
  - 'total lesion volume (direct lesion-volume control: lesion maps normalised to
    unit norm before regression)'
  confounders_not_controlled:
  - time post-onset
  - age
  - education / premorbid IQ
  - aphasia subtype
  region_definition:
    kind: data_driven_cluster
    description: 'VLSM cluster for the Semantic Recognition factor located in white
      matter medial to the insula and lateral to the basal ganglia. Overlaps with
      the convergence zone of three major tracts: uncinate fasciculus, inferior fronto-occipital
      fasciculus (IFOF), and anterior thalamic radiations (ATR). The cluster does
      NOT include the superior longitudinal fasciculus / arcuate fasciculus. Figure
      3 shows approximate MNI coordinates z = 4, y = 28, x = -19 from panel labels.
      Tracts overlaid using ICBM-DTI white matter tractography atlas (FSL) at 20%
      probability threshold.

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
    preprocessing_pipeline: 'MRI registered to custom scanner-specific template, then
      to MNI152 ''Colin27'' volume. CT lesions drawn directly onto Colin27 after pitch
      rotation. Lesions manually segmented, blinded to behaviour. VLSM in SPM8 with
      1000-permutation test. White matter tracts rendered using ICBM-DTI tractography
      atlas from FSL (Mori et al. 2005; Wakana et al. 2007; Hua et al. 2008) at 20%
      probability threshold.

      '
    reference_space: MNI152
    atlases_used:
    - ICBM-DTI white matter tractography atlas (FSL)
    coordinates_reported:
    - region: left frontal white matter bottleneck (Semantic Recognition cluster)
      mni:
      - -19
      - 28
      - 4
      note: Approximate, read from Figure 3 panel labels (x, y, z). Verify against
        supplementary materials.
  replications: []
  contradictions: []
  author_limitations:
  - Only left hemisphere lesions studied; cannot address hemispheric lateralisation
    of this white matter region.
  - Results do not identify critical sub-regions within the functionally and anatomically
    heterogeneous inferior and middle portions of the frontal lobe.
  - Relaxed FDR threshold (q = 0.1) used for Semantic Recognition — results are less
    statistically conservative than the other three VLSM analyses.
  - Lesion coverage poor in ventral and inferolateral temporal cortex.
  - Anatomical alignment of lesions does not guarantee functional alignment due to
    individual differences in functional reorganisation.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results – Voxel-based lesion–symptom mapping (pages 3–4); Discussion
      (pages 4–5); Figure 3
    confidence: high
    flags:
    - Semantic Recognition factor used relaxed FDR q = 0.1 (vs q = 0.05 for other
      factors) — strength rated moderate not strong for this reason.
    - MNI coordinates (-19, 28, 4) read from Figure 3 panel labels (x, y, z slices);
      should be verified against supplementary data.
    - The effect size / t-value colour bar for this factor not clearly specified in
      text — flagged.
    - Whether the IFOF/uncinate/ATR cluster overlaps with the external capsule or
      corona radiata is not specified — future users should cross-reference with atlas.
  source_passages:
  - section: Results – Voxel-based lesion–symptom mapping
    page: 4
    supports: claim
    quote: 'VLSM of the Semantic Recognition factor identiﬁed no voxels in the ATL,
      even at a relaxed q ¼ 0.1 False Discovery Rate (FDR) threshold (Fig. 3), nor
      were there voxels in any other cortical region typically associated with semantic
      processing, such as the middle temporal gyrus or the angular gyrus. Instead,
      the identiﬁed voxels were primarily in the white matter medial to the insula
      and lateral to the basal ganglia.

      '
  - section: Results – Voxel-based lesion–symptom mapping
    page: 4
    supports: region_definition
    quote: 'Several white matter tracts converge in this region, including the inferior
      fronto-occipital fasciculus, the uncinate fasciculus and the anterior thalamic
      radiations. The region did not include the superior longitudinal fasciculus
      (SLF III, which on some accounts corresponds to the fronto-parietal portion
      of the arcuate fasciculus).

      '
  - section: Discussion
    page: 6
    supports: claim
    quote: 'they arise from damage to a frontal white matter bottleneck—a region where
      the uncinate fasciculus, inferior fronto-occipital fasciculus and anterior thalamic
      radiations all converge. We suggest that this convergence produces a vulnerable
      location where a small amount of damage can have large functional consequences
      affecting semantic processing of both verbal and non-verbal (visual) input.

      '
  - section: Results – Voxel-based lesion–symptom mapping
    page: 4
    supports: claim
    quote: 'The convergence of major white matter tracts in the identiﬁed area creates
      a ''bottleneck'' where a small amount of damage can cause a large degree of
      dysfunction in connections between frontal cortices and the rest of the brain.

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
    page: 8
    supports: statistics
    quote: 'The derived statistical p-map was thresholded with FDR q ¼ 0.05 (Semantic
      Recognition factor was thresholded with FDR q ¼ 0.1) and isolated clusters with
      voxel number no more than 50 after thresholding were removed.

      '
  - section: Methods – Lesion analysis
    page: 8
    supports: imaging_details
    quote: 'The white matter tracts in Fig. 3 were based on the ICBM-DTI white matter
      tractography atlas from FSL using a 20% probability threshold.

      '
  - section: Discussion – Limitations
    page: 6
    supports: limitation
    quote: 'the present results do not identify critical sub-regions within the functionally
      and anatomically heterogeneous inferior and middle portions of the frontal lobe.

      '
source: draft
last_reviewed: '2026-05-06'
reviewer: claude-cowork
reviewed_on: '2026-05-06'
---
# Left Frontal White Matter Bottleneck

## Anatomical context

A region of deep white matter in the left hemisphere, medial to the insula
and lateral to the basal ganglia. Three major white matter tracts converge
here: the uncinate fasciculus (connecting temporal and frontal cortex), the
inferior fronto-occipital fasciculus (connecting frontal to occipital/temporal
cortex), and the anterior thalamic radiations (connecting thalamus to frontal
cortex). The superior longitudinal fasciculus / arcuate fasciculus passes
dorsally to this region and was NOT included in the identified cluster.

This region is NOT the same as the left ATL finding. In the same dataset,
lesions of the left ATL predicted semantic error production, while lesions of
this white matter bottleneck predicted multimodal semantic recognition deficits.
The two findings were statistically dissociated.

## Lesion-symptom evidence

Finding f1 (Mirman et al. 2015, n = 99, VLSM at relaxed FDR q = 0.1): damage
to this convergence zone impairs verbal and non-verbal semantic recognition.
The authors interpret this as disruption of frontal connectivity with the
distributed semantic network, consistent with a semantic control account
(Jefferies & Lambon Ralph 2006) or a multimodal semantic integration account.

## Key mechanistic interpretation

The authors propose two possible mechanisms for the bottleneck effect:
(1) disruption of multimodal integration critical for semantic cognition, or
(2) disruption of frontal semantic control and selection. The paper does not
distinguish between these mechanisms — both remain viable.
