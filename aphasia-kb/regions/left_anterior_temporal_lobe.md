---
schema_version: 2.3
id: left_anterior_temporal_lobe
name: Left Anterior Temporal Lobe
kind: classical
status: approved
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-06
hemisphere: left
aliases:
- left ATL
- left temporal pole
- anterior temporal lobe (left)
networks:
- ventral_semantic
notes: 'Draft created 2026-05-06 from Mirman et al. 2015 (Nat Commun 6:6762).

  The left ATL finding (semantic errors in picture naming) is the primary

  anchor for this entry. The paper reports a focal VLSM cluster in the

  left ATL — superior and middle portions — associated specifically with

  semantic error production but NOT with multimodal semantic recognition.

  The region spans approximately y = -12 to -65 on coronal slices shown

  in Figure 2.

  '
findings:
- id: f1
  target: semantic_errors_in_naming
  target_kind: impairment
  claim: 'Focal lesions of the left anterior temporal lobe (superior and middle portions)
    are associated with increased production of semantic errors in picture naming
    in patients with post-stroke aphasia, independently of multimodal semantic recognition
    ability.

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
      / University of Pennsylvania); ongoing longitudinal project.
    inclusion_criteria: ≥1 month post aphasia onset secondary to stroke; living at
      home; medically stable; no major psychiatric or neurological co-morbidities;
      CT or MRI-confirmed left hemisphere cortical lesion; completed all 17 tests.
    exclusion_criteria: left-handed premorbidly; right hemisphere or bilateral lesions;
      did not complete full battery.
  statistics:
    threshold: FDR q = 0.05 (two-tailed); isolated clusters ≤50 voxels removed after
      thresholding
    cluster_extent: null
    effect_size: t-range approximately -2.66 to -6.38 (from Figure 2 colour bar)
    ci_95: not_reported
    p_value: not_reported
  confounders_controlled:
  - 'total lesion volume (direct lesion-volume control: lesion maps normalised to
    unit norm before regression)'
  confounders_not_controlled:
  - time post-onset (wide range; included in sample description but not a covariate
    in VLSM)
  - age
  - education / premorbid IQ
  - aphasia subtype
  region_definition:
    kind: data_driven_cluster
    description: 'VLSM cluster identified by regression of lesion status (lesion normalised
      by total volume) against the Semantic Errors factor score derived from PCA of
      17 language measures. Cluster located in left anterior temporal lobe, superior
      and middle portions; coronal slices shown in Figure 2 at approximately y = -65
      to -12 (MNI approximate). Replicates earlier left ATL finding from the same
      group (Schwartz et al. 2009; Walker et al. 2011) in a larger sample (99 vs 64
      patients).

      '
  imaging_details:
    field_strength: 3T (primary); 1.5T for 6 participants with metal implants
    acquisition:
      sequence: MPRAGE (MRI) or CT (37 participants, 60 axial slices, 3 mm thick)
      voxel_size_mm:
      - 1
      - 1
      - 1
      TR_ms: 1620
      TE_ms: 3.87
    preprocessing_pipeline: 'MRI registered to custom scanner-specific template, then
      to MNI152 ''Colin27'' volume. CT lesions drawn directly onto Colin27 after pitch
      rotation to match patient slice plane. Lesions manually segmented by trained
      technician or experienced neurologist (blinded to behavioural data); reviewed
      by neurologist. VLSM run in SPM8 with 1000-permutation permutation test + FDR
      q = 0.05 threshold.

      '
    reference_space: MNI152
    atlases_used: []
    coordinates_reported:
    - region: left anterior temporal lobe (Semantic Errors cluster peak)
      mni:
      - null
      - null
      - null
      note: Exact MNI peak not reported numerically; approximate range visible in
        Figure 2 coronal slices.
  replications:
  - '@Schwartz2009'
  - '@Walker2011'
  contradictions: []
  author_limitations:
  - Only left hemisphere lesions studied; cannot speak to hemispheric asymmetry between
    ATLs.
  - Lesion coverage poor in ventral and inferolateral temporal cortex; cannot rule
    out bilaterally redundant multimodal semantic hubs in those ATL sectors.
  - Cross-sectional design — cannot infer recovery trajectory.
  - Anatomical alignment of lesions does not guarantee functional alignment due to
    individual differences in functional organisation and re-organisation following
    stroke.
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results – Voxel-based lesion–symptom mapping (pages 2–3); Discussion
      (pages 4–5); Figure 2
    confidence: high
    flags:
    - Exact MNI peak coordinates for the left ATL cluster not reported numerically
      in text or tables — only visible from Figure 2 colour maps. Mark for manual
      verification from figure.
    - t-statistic range read from Figure 2 colour bar (approximately -2.66 to -6.38);
      should be confirmed from supplementary materials.
    - Replication papers (Schwartz 2009, Walker 2011) not confirmed in citations.md
      — citation keys may differ.
  source_passages:
  - section: Results – Voxel-based lesion–symptom mapping
    page: 3
    supports: claim
    quote: 'previous ﬁndings that focal lesions of the left anterior temporal lobe
      (ATL) are associated with increased semantic errors in picture naming

      '
  - section: Discussion
    page: 6
    supports: claim
    quote: 'the superior and middle portions of the left ATL appear to be speciﬁcally
      critical for semantically driven word retrieval—lesions here cause semantic
      errors in production but do not disrupt more general multimodal semantic processing.

      '
  - section: Discussion
    page: 6
    supports: claim
    quote: 'The Semantic Errors factor was associated with lesions in the ATL, consistent
      with other neuropsychological ﬁndings that implicate this region in semantically
      driven retrieval of verbal labels.

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
  - section: Methods – Lesion analysis
    page: 7
    supports: imaging_details
    quote: 'High-resolution whole-brain T1-weighted images (magnetization- prepared
      rapid acquisition gradient echo) were acquired for the 50 participants undergoing
      MRI.

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
reviewer: auto-reviewer
reviewed_on: '2026-05-06'
---
# Left Anterior Temporal Lobe

## Anatomical context

The left anterior temporal lobe (ATL) encompasses the superior and middle
temporal gyri at their most rostral extent, anterior to approximately y = -10
(MNI). Anatomically adjacent to the temporal pole, it lies outside the
classical peri-Sylvian language territory and is considered a key node in the
ventral semantic network.

## Lesion-symptom evidence

Finding f1 (Mirman et al. 2015, n = 99 chronic aphasia, VLSM): focal lesions
of the left ATL are associated with elevated rates of semantic errors in
picture naming. This association is specific to semantic error production and
does NOT extend to multimodal semantic recognition (see white matter bottleneck
entry for that dissociated finding). The result replicates earlier work by the
same Philadelphia group (Schwartz et al. 2009; Walker et al. 2011) in a larger
sample.

## Key dissociation

The Mirman 2015 paper makes an important point: the same left ATL region that
drives semantic error production did NOT predict Semantic Recognition factor
scores, even at a relaxed FDR q = 0.1 threshold. This indicates the left ATL
supports semantically driven word retrieval specifically, not general multimodal
semantic cognition.
