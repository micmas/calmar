---
schema_version: 2.3
id: left_anterior_temporal_lobe__Robson2014
name: Left Anterior Temporal Lobe (Residual Comprehension Substrate in Wernicke's
  Aphasia)
kind: region
status: approved
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-06
hemisphere: left
aliases:
- left ATL
- left temporal pole
- left anterior fusiform gyrus
- left anterior superior temporal gyrus
- left anterior middle temporal gyrus
networks:
- ventral_language
- semantic_network
- anterior_temporal_hub
notes: 'Draft created 2026-05-06 from Robson et al. 2014 (Brain 137:931-943, doi:10.1093/brain/awt373).
  Manchester cohort (NARU), n=12 chronic Wernicke''s aphasia patients. Distortion-corrected
  spin-echo fMRI (important: avoids ATL signal dropout). The ATL activation in Wernicke''s
  aphasia is characterised as "overactivation" relative to controls — representing
  enhanced recruitment after posterior temporal damage (disinhibition or increased
  cognitive demand), not wholesale novel recruitment.

  THEORETICAL NOTE: This entry contrasts with Mirman2015 (Robson2019 in KB), which
  implicates the ATL in semantic errors. Robson2014 positions the ATL as a residual
  comprehension resource — consistent with hub-and-spoke models (Patterson, Lambon
  Ralph). The right anterior STG additionally recruited for written word processing
  in Wernicke''s aphasia overlaps with the Crinion & Price (2005) recovery finding.

  IMPORTANT DISTINCTION from Robson2019 (already in KB): This is Holly Robson et al.
  2014 — a different study from the same first author. Robson2019 addresses auditory-phonological
  and semantic processing. Robson2014 addresses fMRI of residual comprehension in
  Wernicke''s aphasia using a visual semantic judgement task.

  '
findings:
- id: f1
  target: semantic_comprehension_residual
  target_kind: impairment
  claim: 'In chronic Wernicke''s aphasia (left posterior temporoparietal lesions),
    the left anterior temporal lobe — including the anterior fusiform gyrus, temporal
    pole, and anterior middle temporal gyrus — shows significantly greater activation
    than controls during semantic animate-inanimate judgements of pictures and written
    words, indicating that ATL regions become the primary substrate supporting residual
    multimodal semantic comprehension when posterior temporal resources are damaged.

    '
  direction: likely
  relationship: recruitment
  citation: '@Robson2014'
  method: fMRI_activation
  design: cross-sectional
  imaging: fMRI
  sample:
    n: 12
    population: chronic Wernicke's aphasia patients (left hemisphere stroke); 12 age-matched
      controls
    time_post_onset: range 7–84 months (5 participants < 12 months at scan)
    age_range: mean 70.1 (SD 8.7) years (WA group); mean 71 (SD 6.9) years (controls)
    handedness: all right-handed (wrote with right hand)
    language: native English speakers
    recruitment: NHS referrals, North of England speech and language therapists (Manchester
      NARU)
    inclusion_criteria: classical Wernicke's aphasia (BDAE confirmed); single left
      hemisphere stroke; right-handed; native English
    exclusion_criteria: non-right-handed; non-native English; bilateral or right hemisphere
      lesions; cognitive impairment pre-stroke
  statistics:
    threshold: 'Whole brain: p < 0.005 uncorrected, minimum 4-voxel extent. ROI: one-sample
      t-test, one-tailed p < 0.05'
    cluster_extent: 4 voxels minimum
    effect_size: not_reported
    ci_95: not_reported
    p_value: 'Left anterior fusiform: pictures t(11)=2.8 p=0.009; words t(11)=2.0
      p=0.034. Right anterior fusiform: pictures t(11)=2.9 p=0.008; words t(11)=1.9
      p=0.04. Left temporal pole: pictures t(11)=2.0 p=0.034; words t(11)=1.9 p=0.04.
      Group ANOVA left temporal pole F(1,22)=4.65 p=0.042 (WA > control). Left ventral
      OT: pictures t(11)=3.6 p=0.004; words t(11)=2.8 p=0.017. Group ANOVA left vOT
      F(1,22)=10.14 p=0.004; right vOT F(1,22)=5.81 p=0.025.

      '
  confounders_controlled:
  - dual-baseline contrast (active visual baseline + rest) to control motor, executive,
    visual, and default-mode contributions
  - distortion correction for anterior temporal signal dropout (spin-echo EPI with
    post-acquisition remapping)
  - haemodynamic response function time-to-peak analysed with finite impulse response
  - time derivatives in GLM to account for HRF deviations
  - multiple analysis versions: all trials; above-chance participants only; correct
      trials only (convergent results)
  confounders_not_controlled:
  - no active control group performing equally impaired version of same task
  - performance differences between groups not fully equated (WA group significantly
    slower and less accurate)
  - 5 participants < 12 months post-onset (some may still be in rapid recovery phase)
  - lesion volume not covaried in fMRI GLM
  - no anatomical lesion masking of activation maps
  region_definition:
    kind: atlas
    atlas: MarsBar ROIs from literature coordinates (Sharp et al. 2004, Scott et al.
      2000, Visser & Lambon Ralph 2011)
    description: 'Five bilateral ROI pairs: (1) anterior fusiform gyri [±38, 18, -32],
      r=5mm; (2) temporal poles [L:-42,16,-32; R:-40,20,-34], r=5mm; (3) anterior
      superior temporal gyri/sulci [±54, -6, -16], r=7mm; (4) ventral occipital-temporal
      lobe [L:-38,-44,-18; R:42,-44,-18], r=7mm; (5) inferior frontal gyri [L:-51,30,6;
      R:50,30,6], r=7mm. Whole-brain analysis also performed (SPM8, MNI space).

      '
  imaging_details:
    field_strength: 3T (Philips Achieva, 8-element SENSE head coil)
    modalities:
    - modality: fMRI
      sequence: spin-echo EPI (distortion-corrected)
      voxel_size_mm:
      - 2.5
      - 2.5
      - 3.0
      TR_ms: 4150
      TE_ms: 70
    - modality: T1
      sequence: inversion recovery 3D
      voxel_size_mm:
      - 1
      - 1
      - 1
    preprocessing_pipeline: 'SPM8; distortion correction via dual phase-encoding;
      co-registration to T1; unified segmentation-normalisation to MNI (medium regularisation
      for lesioned brains, per Crinion et al. 2007); 8mm FWHM smoothing; haemodynamic
      response function with time derivatives; 2×2 mixed-effects ANOVA (group × condition)
      at second level.

      '
    reference_space: MNI152
    atlases_used:
    - HarvardOxford (implicit via MarsBar)
    coordinates_reported:
    - region: Left uncus (WA > control, whole brain)
      mni:
      - -32
      - -14
      - -26
      note: Z=3.69
    - region: Left anterior middle temporal gyrus (WA > control)
      mni:
      - -48
      - -2
      - -28
      note: Z=3.29
    - region: Left anterior fusiform gyrus (WA > control)
      mni:
      - -54
      - -6
      - -24
      note: Z=3.05
    - region: Right temporal pole (WA > control)
      mni:
      - 48
      - 12
      - -26
      note: Z=2.99
    - region: Right anterior superior temporal gyrus (WA > control)
      mni:
      - 58
      - 10
      - -16
      note: Z=2.72
  replications:
  - '@Sharp2004'
  - '@Crinion2005'
  - '@Warren2009'
  contradictions: []
  author_limitations:
  - Task performance was significantly worse in WA group even on active baseline —
    confound with general attention/executive deficits.
  - Five participants < 12 months post-onset; some plasticity-related changes may
    still be occurring.
  - Overactivation could reflect disinhibition (deafferentation) rather than functional
    recruitment — both accounts consistent with data.
  - Low-demand animate-inanimate task may underestimate reorganisation capacity at
    higher semantic complexity.
  - Thresholded at p<0.005 uncorrected (not FWE/FDR) for whole-brain results — inflated
    false positive risk.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results (pp. 936–939, Tables 5–7, Figure 2–3); Discussion (pp.
      939–941)
    confidence: high
    flags:
    - Whole-brain threshold p<0.005 uncorrected — not corrected for multiple comparisons;
      interpret with caution.
    - ROI results are one-tailed one-sample t-tests (significance of activation within
      group) — not a between-group test for the activation itself.
    - Spin-echo EPI used specifically to enable ATL coverage — results may differ
      with gradient-echo sequences (usual limitation of ATL fMRI).
    - Five participants < 1 year post-stroke — some may not represent stable chronic
      state.
    - Overactivation interpretation is theory-laden; alternative account (de-inhibition)
      is not ruled out.
  source_passages:
  - section: Abstract
    page: 1
    supports: claim
    quote: Wernicke's aphasia group displayed an 'over-activation' in comparison with
      control participants, indicating that anterior temporal lobe regions become
      increasingly influential following reduction in posterior semantic resources
  - section: Results — Whole brain
    page: 6
    supports: claim
    quote: main effect of group was reflected in significantly greater activation
      in the Wernicke's aphasia group than the control group throughout the ventral
      and middle temporal lobes
  - section: Discussion
    page: 10
    supports: claim
    quote: activation increased in the anterior temporal lobe and other regions following
      lesions to posterior temporal regions classically associated with semantic representation
      access
  - section: Conclusion
    page: 12
    supports: claim
    quote: patients' reduction in posterior temporal semantic and phonological processing
      resources increased reliance on extra-sylvian temporal regions
  - section: Results — ROI
    page: 8
    supports: statistics
    quote: 'Wernicke''s aphasia group showed significant activation for both picture
      and word conditions in the left anterior fusiform gyrus [pictures: t(11) = 2.8,
      P = 0.009'
  - section: Methods — Participants
    page: 3
    supports: sample
    quote: Twelve participants with chronic Wernicke's aphasia [two female, mean age
      70.1, standard deviation (SD) 8.7]
- id: f2
  target: right_anterior_superior_temporal_gyrus
  target_kind: region
  claim: 'Written word semantic processing in Wernicke''s aphasia — but not picture
    processing — additionally recruits the right anterior superior temporal gyrus
    and sulcus, a region associated with recovery from auditory-verbal comprehension
    impairment. This suggests right ATL recruitment is specifically linked to residual
    phonological pathway engagement during written word processing.

    '
  direction: likely
  relationship: recruitment
  citation: '@Robson2014'
  method: fMRI_activation
  design: cross-sectional
  imaging: fMRI
  sample:
    n: 12
    population: chronic Wernicke's aphasia (same as f1)
    time_post_onset: range 7–84 months
    age_range: mean 70.1 years
    handedness: right-handed
    language: native English
    recruitment: same as f1
    inclusion_criteria: same as f1
    exclusion_criteria: same as f1
  statistics:
    threshold: 'ROI: one-sample t-test, one-tailed p < 0.05'
    cluster_extent: not_reported
    effect_size: not_reported
    ci_95: not_reported
    p_value: 'Right anterior STG/sulcus for words: t(11)=2.27, p=0.022'
  confounders_controlled:
  - same dual-baseline and preprocessing as f1
  confounders_not_controlled:
  - same as f1
  region_definition:
    kind: peak_coord_sphere
    description: 'Right anterior superior temporal gyrus/sulcus ROI centred on [54,
      -6, -16], r=7mm (homologue of left aSTG, derived from Scott et al. 2000). Whole-brain
      coordinate: right anterior STG at [58, 10, -16], Z=2.72 (WA > control contrast).

      '
  imaging_details:
    field_strength: 3T (Philips Achieva)
    modalities:
    - modality: fMRI
      sequence: spin-echo EPI (distortion-corrected)
      voxel_size_mm:
      - 2.5
      - 2.5
      - 3.0
      TR_ms: 4150
      TE_ms: 70
    preprocessing_pipeline: Same as f1.
    reference_space: MNI152
    atlases_used: []
    coordinates_reported:
    - region: Right anterior superior temporal gyrus/sulcus (WA > control)
      mni:
      - 58
      - 10
      - -16
      note: Z=2.72, whole-brain WA>control contrast
  replications:
  - '@Crinion2005'
  - '@Warren2009'
  contradictions: []
  author_limitations:
  - Modality-specific finding (words but not pictures) — could reflect phonological
    pathway use during written word reading rather than genuine ATL reorganisation.
  - Only one significant modality interaction observed; no Group × Condition interaction
    at whole-brain level.
  - Same statistical limitations as f1 (uncorrected threshold for whole-brain; one-tailed
    ROI t-tests).
  evidence_quality: cohort
  strength: weak
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results — ROI analysis (p. 938–939); Discussion — Reorganization
      of semantic processing (pp. 940–941)
    confidence: medium
    flags:
    - Modality-specific effect (words only, not pictures) is theoretically interesting
      but based on a single ROI t-test; needs replication.
    - No Group × Condition interaction at whole-brain level despite hypothesis; ROI
      finding may not generalise.
  source_passages:
  - section: Results — ROI
    page: 8
    supports: claim
    quote: Wernicke's aphasia group displayed additional activation in the right anterior
      superior temporal gyrus/sulcus for word stimuli [t(11) = 2.27, P = 0.022]
  - section: Discussion
    page: 10
    supports: claim
    quote: importance of the right anterior superior temporal gyrus/sulcus in language
      comprehension subsequent to left posterior temporal lesions has been demonstrated
      in previous studies
  - section: Abstract
    page: 1
    supports: claim
    quote: Semantic processing of written words in Wernicke's aphasia was additionally
      supported by recruitment of the right anterior superior temporal lobe, a region
      previously associated with recovery from auditory-verbal comprehension impairments
- id: f3
  target: semantic_comprehension_residual
  target_kind: impairment
  claim: 'In chronic Wernicke''s aphasia (left posterior temporoparietal lesions),
    the left anterior temporal lobe — including the anterior fusiform gyrus, temporal
    pole, and anterior middle temporal gyrus — shows significantly greater activation
    than controls during semantic animate-inanimate judgements of pictures and written
    words, indicating that ATL regions become the primary substrate supporting residual
    multimodal semantic comprehension when posterior temporal resources are damaged.

    '
  direction: likely
  relationship: recruitment
  citation: '@Robson2014'
  method: fMRI_activation
  design: cross-sectional
  imaging: fMRI
  sample:
    n: 12
    population: chronic Wernicke's aphasia patients (left hemisphere stroke); 12 age-matched
      controls
    time_post_onset: range 7–84 months (5 participants < 12 months at scan)
    age_range: mean 70.1 (SD 8.7) years (WA group); mean 71 (SD 6.9) years (controls)
    handedness: all right-handed (wrote with right hand)
    language: native English speakers
    recruitment: NHS referrals, North of England speech and language therapists (Manchester
      NARU)
    inclusion_criteria: classical Wernicke's aphasia (BDAE confirmed); single left
      hemisphere stroke; right-handed; native English
    exclusion_criteria: non-right-handed; non-native English; bilateral or right hemisphere
      lesions; cognitive impairment pre-stroke
  statistics:
    threshold: 'Whole brain: p < 0.005 uncorrected, minimum 4-voxel extent. ROI: one-sample
      t-test, one-tailed p < 0.05'
    cluster_extent: 4 voxels minimum
    effect_size: not_reported
    ci_95: not_reported
    p_value: 'Left anterior fusiform: pictures t(11)=2.8 p=0.009; words t(11)=2.0
      p=0.034. Right anterior fusiform: pictures t(11)=2.9 p=0.008; words t(11)=1.9
      p=0.04. Left temporal pole: pictures t(11)=2.0 p=0.034; words t(11)=1.9 p=0.04.
      Group ANOVA left temporal pole F(1,22)=4.65 p=0.042 (WA > control). Left ventral
      OT: pictures t(11)=3.6 p=0.004; words t(11)=2.8 p=0.017. Group ANOVA left vOT
      F(1,22)=10.14 p=0.004; right vOT F(1,22)=5.81 p=0.025.

      '
  confounders_controlled:
  - dual-baseline contrast (active visual baseline + rest) to control motor, executive,
    visual, and default-mode contributions
  - distortion correction for anterior temporal signal dropout (spin-echo EPI with
    post-acquisition remapping)
  - haemodynamic response function time-to-peak analysed with finite impulse response
  - time derivatives in GLM to account for HRF deviations
  - multiple analysis versions: all trials; above-chance participants only; correct
      trials only (convergent results)
  confounders_not_controlled:
  - no active control group performing equally impaired version of same task
  - performance differences between groups not fully equated (WA group significantly
    slower and less accurate)
  - 5 participants < 12 months post-onset (some may still be in rapid recovery phase)
  - lesion volume not covaried in fMRI GLM
  - no anatomical lesion masking of activation maps
  region_definition:
    kind: atlas
    atlas: MarsBar ROIs from literature coordinates (Sharp et al. 2004, Scott et al.
      2000, Visser & Lambon Ralph 2011)
    description: 'Five bilateral ROI pairs: (1) anterior fusiform gyri [±38, 18, -32],
      r=5mm; (2) temporal poles [L:-42,16,-32; R:-40,20,-34], r=5mm; (3) anterior
      superior temporal gyri/sulci [±54, -6, -16], r=7mm; (4) ventral occipital-temporal
      lobe [L:-38,-44,-18; R:42,-44,-18], r=7mm; (5) inferior frontal gyri [L:-51,30,6;
      R:50,30,6], r=7mm. Whole-brain analysis also performed (SPM8, MNI space).

      '
  imaging_details:
    field_strength: 3T (Philips Achieva, 8-element SENSE head coil)
    modalities:
    - modality: fMRI
      sequence: spin-echo EPI (distortion-corrected)
      voxel_size_mm:
      - 2.5
      - 2.5
      - 3.0
      TR_ms: 4150
      TE_ms: 70
    - modality: T1
      sequence: inversion recovery 3D
      voxel_size_mm:
      - 1
      - 1
      - 1
    preprocessing_pipeline: 'SPM8; distortion correction via dual phase-encoding;
      co-registration to T1; unified segmentation-normalisation to MNI (medium regularisation
      for lesioned brains, per Crinion et al. 2007); 8mm FWHM smoothing; haemodynamic
      response function with time derivatives; 2×2 mixed-effects ANOVA (group × condition)
      at second level.

      '
    reference_space: MNI152
    atlases_used:
    - HarvardOxford (implicit via MarsBar)
    coordinates_reported:
    - region: Left uncus (WA > control, whole brain)
      mni:
      - -32
      - -14
      - -26
      note: Z=3.69
    - region: Left anterior middle temporal gyrus (WA > control)
      mni:
      - -48
      - -2
      - -28
      note: Z=3.29
    - region: Left anterior fusiform gyrus (WA > control)
      mni:
      - -54
      - -6
      - -24
      note: Z=3.05
    - region: Right temporal pole (WA > control)
      mni:
      - 48
      - 12
      - -26
      note: Z=2.99
    - region: Right anterior superior temporal gyrus (WA > control)
      mni:
      - 58
      - 10
      - -16
      note: Z=2.72
  replications:
  - '@Sharp2004'
  - '@Crinion2005'
  - '@Warren2009'
  contradictions: []
  author_limitations:
  - Task performance was significantly worse in WA group even on active baseline —
    confound with general attention/executive deficits.
  - Five participants < 12 months post-onset; some plasticity-related changes may
    still be occurring.
  - Overactivation could reflect disinhibition (deafferentation) rather than functional
    recruitment — both accounts consistent with data.
  - Low-demand animate-inanimate task may underestimate reorganisation capacity at
    higher semantic complexity.
  - Thresholded at p<0.005 uncorrected (not FWE/FDR) for whole-brain results — inflated
    false positive risk.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results (pp. 936–939, Tables 5–7, Figure 2–3); Discussion (pp.
      939–941)
    confidence: high
    flags:
    - Whole-brain threshold p<0.005 uncorrected — not corrected for multiple comparisons;
      interpret with caution.
    - ROI results are one-tailed one-sample t-tests (significance of activation within
      group) — not a between-group test for the activation itself.
    - Spin-echo EPI used specifically to enable ATL coverage — results may differ
      with gradient-echo sequences (usual limitation of ATL fMRI).
    - Five participants < 1 year post-stroke — some may not represent stable chronic
      state.
    - Overactivation interpretation is theory-laden; alternative account (de-inhibition)
      is not ruled out.
  source_passages:
  - section: Abstract
    page: 1
    supports: claim
    quote: Wernicke's aphasia group displayed an 'over-activation' in comparison with
      control participants, indicating that anterior temporal lobe regions become
      increasingly influential following reduction in posterior semantic resources
  - section: Results — Whole brain
    page: 6
    supports: claim
    quote: main effect of group was reflected in significantly greater activation
      in the Wernicke's aphasia group than the control group throughout the ventral
      and middle temporal lobes
  - section: Discussion
    page: 10
    supports: claim
    quote: activation increased in the anterior temporal lobe and other regions following
      lesions to posterior temporal regions classically associated with semantic representation
      access
  - section: Conclusion
    page: 12
    supports: claim
    quote: patients' reduction in posterior temporal semantic and phonological processing
      resources increased reliance on extra-sylvian temporal regions
  - section: Results — ROI
    page: 8
    supports: statistics
    quote: 'Wernicke''s aphasia group showed significant activation for both picture
      and word conditions in the left anterior fusiform gyrus [pictures: t(11) = 2.8,
      P = 0.009'
  - section: Methods — Participants
    page: 3
    supports: sample
    quote: Twelve participants with chronic Wernicke's aphasia [two female, mean age
      70.1, standard deviation (SD) 8.7]
- id: f4
  target: right_anterior_superior_temporal_gyrus
  target_kind: region
  claim: 'Written word semantic processing in Wernicke''s aphasia — but not picture
    processing — additionally recruits the right anterior superior temporal gyrus
    and sulcus, a region associated with recovery from auditory-verbal comprehension
    impairment. This suggests right ATL recruitment is specifically linked to residual
    phonological pathway engagement during written word processing.

    '
  direction: likely
  relationship: recruitment
  citation: '@Robson2014'
  method: fMRI_activation
  design: cross-sectional
  imaging: fMRI
  sample:
    n: 12
    population: chronic Wernicke's aphasia (same as f1)
    time_post_onset: range 7–84 months
    age_range: mean 70.1 years
    handedness: right-handed
    language: native English
    recruitment: same as f1
    inclusion_criteria: same as f1
    exclusion_criteria: same as f1
  statistics:
    threshold: 'ROI: one-sample t-test, one-tailed p < 0.05'
    cluster_extent: not_reported
    effect_size: not_reported
    ci_95: not_reported
    p_value: 'Right anterior STG/sulcus for words: t(11)=2.27, p=0.022'
  confounders_controlled:
  - same dual-baseline and preprocessing as f1
  confounders_not_controlled:
  - same as f1
  region_definition:
    kind: peak_coord_sphere
    description: 'Right anterior superior temporal gyrus/sulcus ROI centred on [54,
      -6, -16], r=7mm (homologue of left aSTG, derived from Scott et al. 2000). Whole-brain
      coordinate: right anterior STG at [58, 10, -16], Z=2.72 (WA > control contrast).

      '
  imaging_details:
    field_strength: 3T (Philips Achieva)
    modalities:
    - modality: fMRI
      sequence: spin-echo EPI (distortion-corrected)
      voxel_size_mm:
      - 2.5
      - 2.5
      - 3.0
      TR_ms: 4150
      TE_ms: 70
    preprocessing_pipeline: Same as f1.
    reference_space: MNI152
    atlases_used: []
    coordinates_reported:
    - region: Right anterior superior temporal gyrus/sulcus (WA > control)
      mni:
      - 58
      - 10
      - -16
      note: Z=2.72, whole-brain WA>control contrast
  replications:
  - '@Crinion2005'
  - '@Warren2009'
  contradictions: []
  author_limitations:
  - Modality-specific finding (words but not pictures) — could reflect phonological
    pathway use during written word reading rather than genuine ATL reorganisation.
  - Only one significant modality interaction observed; no Group × Condition interaction
    at whole-brain level.
  - Same statistical limitations as f1 (uncorrected threshold for whole-brain; one-tailed
    ROI t-tests).
  evidence_quality: cohort
  strength: weak
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results — ROI analysis (p. 938–939); Discussion — Reorganization
      of semantic processing (pp. 940–941)
    confidence: medium
    flags:
    - Modality-specific effect (words only, not pictures) is theoretically interesting
      but based on a single ROI t-test; needs replication.
    - No Group × Condition interaction at whole-brain level despite hypothesis; ROI
      finding may not generalise.
  source_passages:
  - section: Results — ROI
    page: 8
    supports: claim
    quote: Wernicke's aphasia group displayed additional activation in the right anterior
      superior temporal gyrus/sulcus for word stimuli [t(11) = 2.27, P = 0.022]
  - section: Discussion
    page: 10
    supports: claim
    quote: importance of the right anterior superior temporal gyrus/sulcus in language
      comprehension subsequent to left posterior temporal lesions has been demonstrated
      in previous studies
  - section: Abstract
    page: 1
    supports: claim
    quote: Semantic processing of written words in Wernicke's aphasia was additionally
      supported by recruitment of the right anterior superior temporal lobe, a region
      previously associated with recovery from auditory-verbal comprehension impairments
source: draft
last_reviewed: '2026-05-07'
reviewer: claude-cowork
reviewed_on: '2026-05-06'
---
# Left Anterior Temporal Lobe — Residual Comprehension in Wernicke's Aphasia (Robson et al. 2014)

## Anatomical context

The anterior temporal lobe (ATL) — including temporal pole, anterior fusiform gyrus,
and anterior middle/superior temporal gyri — lies anterior to the core Wernicke's aphasia
lesion zone (posterior STG/TPJ). This region falls mostly outside the MCA territory and
is therefore typically spared in Wernicke's aphasia, making it a candidate residual
comprehension resource.

## Key findings (Robson et al. 2014, n=12 WA, Manchester/NARU)

**Finding f1**: Distortion-corrected fMRI reveals that Wernicke's aphasia patients
show significantly greater activation than controls in the left ATL (anterior fusiform,
temporal pole, anterior MTG) and bilateral ventral OT during semantic judgements.
This "overactivation" is consistent with increased reliance on these regions after
posterior temporal damage — not necessarily novel recruitment, but enhanced engagement
of normally-present ATL semantic processing.

**Finding f2**: Written word processing additionally recruits the right anterior
superior temporal gyrus/sulcus in Wernicke's aphasia (t=2.27, p=0.022), consistent
with right hemisphere compensation for left posterior STG damage affecting phonological
processing of written words.

## Theoretical context

Supports hub-and-spoke models (Patterson et al. 2007; Lambon Ralph et al. 2010)
positioning the ATL as a transmodal semantic hub. Contrasts with Mirman2015 (Robson2019
in KB) which attributes semantic errors to ATL damage — here the ATL is the SURVIVING
resource in Wernicke's aphasia, not the damaged one.

## Methodological note

Distortion-corrected spin-echo EPI is critical here: standard gradient-echo fMRI
suffers from signal dropout in ATL regions, causing systematic underestimation of
ATL activation in most fMRI aphasia studies. The Robson2014 ATL findings are therefore
more reliable than those from studies using standard sequences.
