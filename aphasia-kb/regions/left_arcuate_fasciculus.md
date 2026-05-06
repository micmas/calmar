---
schema_version: 2.3
id: left_arcuate_fasciculus
name: Left arcuate fasciculus
aliases:
- arcuate fasciculus (left)
- left AF
- left superior longitudinal fasciculus (arcuate component)
kind: tract
status: approved
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-06
hemisphere: left
members:
- left_posterior_superior_temporal_gyrus
- left_middle_temporal_gyrus
- left_inferior_frontal_gyrus_pars_opercularis
- left_temporoparietal_junction
networks:
- dorsal_language
findings:
- id: f1
  target: speech_production_rate
  target_kind: impairment
  claim: Lesion load of the left arcuate fasciculus (proportion of the tract damaged
    by a patient's stroke) significantly predicts rate of speech (words per minute),
    whereas overall lesion size, extreme capsule lesion load, and uncinate fasciculus
    lesion load do not.
  direction: likely
  relationship: correlational
  citation: '@Marchina2011'
  method: tractography
  design: cross-sectional
  imaging: multimodal
  sample:
    n: 30
    population: chronic stroke survivors with left-hemisphere MCA infarct and residual
      speech production impairments
    time_post_onset: '>=11 months post-stroke; mean 35.0 months (SD 28.7)'
    age_range: mean age 58.5 years (SD 10.0)
    handedness: all right-handed
    language: not_reported (Boston, MA recruitment — English assumed)
    recruitment: patients enrolled in Beth Israel Deaconess Medical Center / Harvard
      Medical School Stroke Recovery and Neuroimaging Laboratory
    inclusion_criteria: right-handed; left-hemispheric stroke in MCA territory; >=11
      months post-stroke; diagnosis of severe nonfluent aphasia in acute/subacute
      phase; auditory comprehension >=45th percentile on BDAE combined Auditory Comprehension
      subtests; Raven's Colored Progressive Matrices >=50th percentile.
    exclusion_criteria: bihemispheric or brain stem infarcts; primary intracerebral
      hemorrhages; previous or subsequent strokes; concomitant neurological diseases/disorders;
      pure anomia; aphasia syndromes with severe comprehension deficits (<45th percentile
      BDAE); cognitive impairment (<50th percentile Raven's CPM).
  statistics:
    threshold: multiple regression with all 4 predictors (lesion size, AF lesion load,
      EmC lesion load, UF lesion load); p<0.05 for partial R² of individual predictor.
    cluster_extent: null
    effect_size: partial R²=0.175, p=0.030 (AF lesion load predicting WPM); overall
      model adjusted R²=0.301, p=0.011
    ci_95: not_reported
    p_value: '0.030'
  confounders_controlled:
  - overall lesion size (entered as covariate in regression alongside AF, EmC, and
    UF lesion loads)
  - extreme capsule lesion load (entered as covariate)
  - uncinate fasciculus lesion load (entered as covariate)
  confounders_not_controlled:
  - age (mean 58.5 yrs; not entered as covariate)
  - time post-stroke (mean 35 months; not entered as covariate)
  - sex (6 female, 24 male; not controlled)
  - rehabilitation history not reported or controlled
  region_definition:
    kind: tract
    description: 'AF probabilistic map derived from DTI fiber-tracking in 10 age-matched
      healthy controls (3T GE scanner). ROIs drawn on FA maps: one in white matter
      underlying posterior middle/superior temporal gyri (~x=-50 mm MNI), one in white
      matter underlying pars opercularis of posterior IFG (same sagittal slice). Binary
      fiber tract images summed across 10 controls to create probabilistic map (voxel
      intensity 0–10 = number of subjects contributing). Lesion-tract overlap calculated
      as weighted sum (raw lesion load method from Zhu et al. 2010).'
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: T1
      sequence: not_reported (standard radiofrequency head coil, GE 3T)
      voxel_size_mm:
      - 0.9
      - 0.9
      - 1.5
      notes: Spatially normalized to 2x2x2mm isotropic using SPM5; cost-function masking
        applied for patients with extensive lesions.
    - modality: DTI
      sequence: single-shot spin-echo EPI
      voxel_size_mm:
      - 2.6
      - 2.6
      - 2.6
      TR_ms: 10000
      TE_ms: 86.9
      n_directions: 30
      b_values:
      - 0
      - 1000
      notes: 6 b=0 acquisitions; 56 slices covering whole brain including brainstem.
        DTI acquired in healthy controls only (n=10); lesion maps overlaid onto control-derived
        probabilistic tract maps.
    preprocessing_pipeline: SPM5 spatial normalization of T1 (isotropic 2mm³); lesion
      masking in MRIcro during normalization for large lesions; DTI postprocessing
      and fiber tracking per Zhu et al. 2010; binary tract images summed to probabilistic
      map; lesion-tract overlap calculated as weighted-sum (raw lesion load method).
    reference_space: Talairach
    atlases_used: []
    coordinates_reported:
    - region: AF ROI 1 (posterior MTG/STG white matter)
      mni:
      - -50
      - null
      - null
    - region: AF ROI 2 (pars opercularis white matter)
      mni:
      - -50
      - null
      - null
  replications:
  - '@Hosomi2009'
  - '@Breier2008'
  contradictions: []
  author_limitations:
  - Lesion load method uses probabilistic tracts from only 10 healthy controls; individual
    variability in tract anatomy not fully captured.
  - 'Cross-sectional design: cannot establish whether AF lesion load predicts recovery
    trajectory or only current impairment level.'
  - All patients had left-hemisphere MCA strokes and chronic aphasia — generalizability
    to acute stroke, subcortical hemorrhage, or right-hemisphere damage is limited.
  - Behavioral measures (WPM, %CIUs, CIUs/min) are not purely dissociable along the
    dorsal/ventral stream lines predicted by dual-stream models; all correlated with
    AF load but not EmC/UF load.
  - Study does not establish causation between AF damage and speech impairment in
    the strict experimental sense — it is a correlational lesion-load analysis.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results — Rate of Speech, page 2253
    confidence: high
    flags:
    - 'Relationship coded as `correlational` per KB rules: DTI tractography + lesion
      load analysis tracks structural integrity against behavior but is not a strict
      causal VLSM/LSM approach — the probabilistic tracts come from healthy controls,
      not directly from the patients'' own DTI.'
    - Talairach space used in paper (not MNI152); ROI coordinates reported are x-values
      only (sagittal slice positions).
    - 10 healthy controls contributed DTI data for probabilistic maps; patient n=30
      contributed behavioral and T1 lesion data only.
  source_passages:
  - section: Abstract
    page: 1
    quote: Regression analyses showed that arcuate fasciculus lesion load, but not
      extreme capsule or uncinate fasciculus lesion load or overall lesion size, significantly
      predicted rate, informativeness, and overall efficiency of speech as well as
      naming ability.
    supports: claim
  - section: Results — Rate of Speech
    page: 3
    quote: A regression analysis was first conducted using lesion size and lesion
      loads of all 3 tracts (ie, AF, EmC, and UF) as predictors of words/min (adjusted
      R²=0.301, P=0.011). AF lesion load proved to be the best variable (partial R²=0.175,
      P=0.030; Figure 2A), whereas EmC lesion load (partial R²=0.087, P=0.135), UF
      lesion load (partial R²=0.098, P=0.112), and lesion size (partial R²=0.002,
      P=0.829) were shown to be nonsignificant predictors.
    supports: statistics
  - section: Methods — Subjects
    page: 2
    quote: The study group consisted of 30 right-handed patients, all of whom had
      left-hemispheric strokes in the middle cerebral artery territory and were at
      least 11 months post stroke at the time of testing (6 females and 24 males;
      mean age 58.5 years [SD 10.0]; mean time poststroke 35.0 months [SD 28.7]).
    supports: sample
  - section: Methods — MRI and Diffusion Tensor Imaging Acquisition
    page: 2
    quote: 'The control subjects underwent diffusion tensor imaging using a single-shot,
      spin-echo echoplanar imaging sequence with the following parameters: TR=10 seconds;
      TE=86.9 ms; resolution 2.6×2.6×2.6 mm³; 30 noncollinear diffusion directions
      with a b-value of 1000 s/mm²; and 6 acquisitions with a value of 0 s/mm².'
    supports: imaging_details
  - section: Methods — MRI and Diffusion Tensor Imaging Acquisition
    page: 2
    quote: For the AF, a curved fiber bundle that connects the posterior portion of
      the temporoparietal junction with the frontal cortex, we drew 1 region of interest
      on the Fractional Anisotropy (FA) map in the white matter underlying the posterior
      middle and superior temporal gyri at approximately x=−50 mm (MNI space); a second
      region of interest was drawn on the same sagittal slice in the white matter
      underlying the pars opercularis of the posterior inferior frontal gyrus.
    supports: region_definition
  - section: Methods — Lesion Load Calculation
    page: 3
    quote: The binary fiber tracts of the 10 healthy control subjects were summed
      to generate a fiber map using Matlab (Figure 1). Voxel intensities ranged from
      I=0 (ie, voxel is not part of the tract in any of the subjects) to I=10 (ie,
      voxel is part of the tract in all 10 subjects); thus, the probability that a
      particular voxel would be part of the tract was calculated as one tenth of the
      voxel's intensity.
    supports: method
- id: f2
  target: speech_informativeness
  target_kind: impairment
  claim: Lesion load of the left arcuate fasciculus significantly predicts informativeness
    of speech (%CIUs — correct information units as a proportion of total words),
    with greater tract damage associated with lower informativeness. Overall lesion
    size, extreme capsule, and uncinate fasciculus lesion loads are not significant
    predictors.
  direction: likely
  relationship: correlational
  citation: '@Marchina2011'
  method: tractography
  design: cross-sectional
  imaging: multimodal
  sample:
    n: 30
    population: chronic stroke survivors with left-hemisphere MCA infarct and residual
      speech production impairments
    time_post_onset: '>=11 months post-stroke; mean 35.0 months (SD 28.7)'
    age_range: mean age 58.5 years (SD 10.0)
    handedness: all right-handed
    language: not_reported (Boston, MA recruitment — English assumed)
    recruitment: patients enrolled in Beth Israel Deaconess Medical Center / Harvard
      Medical School Stroke Recovery and Neuroimaging Laboratory
    inclusion_criteria: right-handed; left-hemispheric stroke in MCA territory; >=11
      months post-stroke; severe nonfluent aphasia in acute/subacute phase; BDAE auditory
      comprehension >=45th percentile; Raven's CPM >=50th percentile.
    exclusion_criteria: bihemispheric or brain stem infarcts; primary intracerebral
      hemorrhages; previous or subsequent strokes; concomitant neurological diseases/disorders;
      pure anomia; severe comprehension deficits; cognitive impairment.
  statistics:
    threshold: multiple regression with all 4 predictors; p<0.05 for partial R².
    cluster_extent: null
    effect_size: partial R²=0.336, p=0.002 (AF lesion load predicting %CIUs); overall
      model adjusted R²=0.496, p=0.001
    ci_95: not_reported
    p_value: '0.002'
  confounders_controlled:
  - overall lesion size
  - extreme capsule lesion load
  - uncinate fasciculus lesion load
  confounders_not_controlled:
  - age
  - time post-stroke
  - sex
  - rehabilitation history
  region_definition:
    kind: tract
    description: 'Same AF probabilistic map as f1: derived from DTI fiber-tracking
      in 10 healthy age-matched controls; ROIs on FA map in white matter of posterior
      MTG/STG (~x=-50 mm) and pars opercularis IFG.'
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: T1
      sequence: not_reported (standard radiofrequency head coil, GE 3T)
      voxel_size_mm:
      - 0.9
      - 0.9
      - 1.5
      notes: Spatially normalized to 2x2x2mm isotropic using SPM5.
    - modality: DTI
      sequence: single-shot spin-echo EPI
      voxel_size_mm:
      - 2.6
      - 2.6
      - 2.6
      TR_ms: 10000
      TE_ms: 86.9
      n_directions: 30
      b_values:
      - 0
      - 1000
      notes: Acquired in healthy controls only (n=10); used to create probabilistic
        tract maps.
    preprocessing_pipeline: SPM5 spatial normalization; cost-function masking; DTI
      postprocessing per Zhu et al. 2010; probabilistic AF map from 10 controls; weighted-sum
      lesion-load calculation.
    reference_space: Talairach
    atlases_used: []
  replications: []
  contradictions: []
  author_limitations:
  - Behavioral measures (WPM, %CIUs, CIUs/min) are not purely dissociable along dorsal/ventral
    stream lines; the authors acknowledge this may explain why all three correlated
    with AF rather than UF/EmC.
  - Small sample (n=30); regression with 4 predictors risks overfitting.
  - Cross-sectional design precludes recovery trajectory predictions.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results — Informativeness of Speech, page 2253
    confidence: high
    flags:
    - 'Relationship coded as `correlational` per KB rules: DTI tractography + lesion
      load analysis.'
    - Strongest statistical result of the paper (partial R²=0.336, p=0.002) — informativeness
      had the largest AF lesion-load effect size.
  source_passages:
  - section: Results — Informativeness of Speech
    page: 3
    quote: A second regression analysis was conducted using the same 4 variables to
      predict %CIUs (adjusted R²=0.496, P=0.001). Again, AF lesion load was shown
      to be a significant predictor (partial R²=0.336, P=0.002; Figure 2B), whereas
      EmC lesion load (partial R²=0.052, P=0.520), UF lesion load (partial R²=0.058,
      P=0.227), and lesion size (partial R²=0.002, P=0.844) were nonsignificant.
    supports: statistics
  - section: Abstract
    page: 1
    quote: Regression analyses showed that arcuate fasciculus lesion load, but not
      extreme capsule or uncinate fasciculus lesion load or overall lesion size, significantly
      predicted rate, informativeness, and overall efficiency of speech as well as
      naming ability.
    supports: claim
  - section: Methods — Behavioral Assessments
    page: 2
    quote: To be counted as CIUs, words had to be intelligible in context as well
      as accurate, relevant, and informative with respect to the stimulus; meaningless
      utterances, exclamations, inappropriate information, and perseverations were
      counted as words but not as CIUs.
    supports: method
- id: f3
  target: speech_efficiency
  target_kind: impairment
  claim: Lesion load of the left arcuate fasciculus is the strongest predictor of
    overall speech efficiency (CIUs per minute), explaining 45% of unique variance
    in a regression model that also includes overall lesion size and extreme capsule
    and uncinate fasciculus lesion loads.
  direction: likely
  relationship: correlational
  citation: '@Marchina2011'
  method: tractography
  design: cross-sectional
  imaging: multimodal
  sample:
    n: 30
    population: chronic stroke survivors with left-hemisphere MCA infarct and residual
      speech production impairments
    time_post_onset: '>=11 months post-stroke; mean 35.0 months (SD 28.7)'
    age_range: mean age 58.5 years (SD 10.0)
    handedness: all right-handed
    language: not_reported
    recruitment: Beth Israel Deaconess Medical Center / Harvard Medical School Stroke
      Recovery and Neuroimaging Laboratory
    inclusion_criteria: right-handed; left-hemispheric MCA stroke; >=11 months post-stroke;
      BDAE auditory comprehension >=45th percentile; Raven's CPM >=50th percentile.
    exclusion_criteria: bihemispheric or brain stem infarcts; primary intracerebral
      hemorrhages; previous or subsequent strokes; concomitant neurological diseases/disorders;
      pure anomia; severe comprehension deficits; cognitive impairment.
  statistics:
    threshold: multiple regression with all 4 predictors; p<0.05 for partial R².
    cluster_extent: null
    effect_size: partial R²=0.450, p=0.001 (AF lesion load predicting CIUs/min); overall
      model adjusted R²=0.610, p=0.001
    ci_95: not_reported
    p_value: '0.001'
  confounders_controlled:
  - overall lesion size
  - extreme capsule lesion load
  - uncinate fasciculus lesion load
  confounders_not_controlled:
  - age
  - time post-stroke
  - sex
  - rehabilitation history
  region_definition:
    kind: tract
    description: Same AF probabilistic map as f1 and f2.
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: T1
      voxel_size_mm:
      - 0.9
      - 0.9
      - 1.5
      sequence: not_reported
      notes: SPM5 normalized to 2mm isotropic.
    - modality: DTI
      sequence: single-shot spin-echo EPI
      voxel_size_mm:
      - 2.6
      - 2.6
      - 2.6
      TR_ms: 10000
      TE_ms: 86.9
      n_directions: 30
      b_values:
      - 0
      - 1000
      notes: Healthy controls n=10.
    preprocessing_pipeline: SPM5 spatial normalization; cost-function masking; probabilistic
      AF map from 10 controls; weighted-sum lesion-load calculation per Zhu et al.
      2010.
    reference_space: Talairach
    atlases_used: []
  replications: []
  contradictions: []
  author_limitations:
  - CIUs/min is a composite measure combining rate (articulatory) and informativeness
    (semantic-phonological) demands, which may explain why it shows the strongest
    association with AF load even though dual-stream models predict rate should be
    dorsal-stream dependent and informativeness ventral-stream dependent.
  - Small sample (n=30); regression overfitting possible.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results — Overall Efficiency of Speech, page 2253
    confidence: high
    flags:
    - 'Relationship coded as `correlational` per KB rules: DTI tractography + lesion
      load analysis.'
    - Highest partial R² of all four outcomes (0.450); overall model R²=0.610 is strongest
      in the paper.
  source_passages:
  - section: Results — Overall Efficiency of Speech
    page: 3
    quote: A third regression analysis was conducted using lesion size as well as
      AF, EmC, and UF lesion loads as predictors of CIUs/min (adjusted R²=0.610, P=0.001).
      Once again, AF lesion load proved to be a significant predictor (partial R²=0.450,
      P=0.001; Figure 2C), whereas EmC lesion load (partial R²=0.086, P=0.138), UF
      lesion load (partial R²=0.106, P=0.100), and lesion size (partial R²=0.034,
      P=0.358) remained nonsignificant.
    supports: statistics
  - section: Abstract
    page: 1
    quote: Regression analyses showed that arcuate fasciculus lesion load, but not
      extreme capsule or uncinate fasciculus lesion load or overall lesion size, significantly
      predicted rate, informativeness, and overall efficiency of speech as well as
      naming ability.
    supports: claim
- id: f4
  target: confrontation_naming
  target_kind: impairment
  claim: Lesion load of the left arcuate fasciculus significantly predicts confrontation
    naming ability (Boston Naming Test score), whereas extreme capsule lesion load
    and overall lesion size do not; uncinate fasciculus lesion load shows a nonsignificant
    trend.
  direction: likely
  relationship: correlational
  citation: '@Marchina2011'
  method: tractography
  design: cross-sectional
  imaging: multimodal
  sample:
    n: 30
    population: chronic stroke survivors with left-hemisphere MCA infarct and residual
      speech production impairments
    time_post_onset: '>=11 months post-stroke; mean 35.0 months (SD 28.7)'
    age_range: mean age 58.5 years (SD 10.0)
    handedness: all right-handed
    language: not_reported
    recruitment: Beth Israel Deaconess Medical Center / Harvard Medical School Stroke
      Recovery and Neuroimaging Laboratory
    inclusion_criteria: right-handed; left-hemispheric MCA stroke; >=11 months post-stroke;
      BDAE auditory comprehension >=45th percentile; Raven's CPM >=50th percentile.
    exclusion_criteria: bihemispheric or brain stem infarcts; intracerebral hemorrhages;
      prior or subsequent strokes; concomitant neurological diseases; pure anomia;
      severe comprehension deficits; cognitive impairment.
  statistics:
    threshold: multiple regression with all 4 predictors; p<0.05 for R².
    cluster_extent: null
    effect_size: 'R²=0.159, p=0.039 (AF lesion load predicting BNT); UF trend: R²=0.123,
      p=0.073; overall model adjusted R²=0.417, p=0.001'
    ci_95: not_reported
    p_value: '0.039'
  confounders_controlled:
  - overall lesion size
  - extreme capsule lesion load
  - uncinate fasciculus lesion load
  confounders_not_controlled:
  - age
  - time post-stroke
  - sex
  - education / premorbid vocabulary
  region_definition:
    kind: tract
    description: Same AF probabilistic map as f1–f3.
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: T1
      voxel_size_mm:
      - 0.9
      - 0.9
      - 1.5
      sequence: not_reported
    - modality: DTI
      sequence: single-shot spin-echo EPI
      voxel_size_mm:
      - 2.6
      - 2.6
      - 2.6
      TR_ms: 10000
      TE_ms: 86.9
      n_directions: 30
      b_values:
      - 0
      - 1000
      notes: Healthy controls n=10.
    preprocessing_pipeline: SPM5 spatial normalization; cost-function masking; probabilistic
      AF map from 10 controls; weighted-sum lesion-load per Zhu et al. 2010.
    reference_space: Talairach
    atlases_used: []
  replications: []
  contradictions: []
  author_limitations:
  - The finding that AF (a dorsal-stream tract) predicts naming, typically considered
    a ventral-stream function, is discussed by the authors as possibly reflecting
    that their behavioral measures do not purely capture one stream.
  - UF nonsignificant trend (p=0.073) is consistent with prior work suggesting UF
    involvement in naming, but the study is underpowered to confirm this.
  - BNT administered as untimed; partial credit scoring used (0.5 for cued response,
    0.25 for written-word identification) — this modified scoring may limit comparability.
  evidence_quality: cohort
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results — Naming Ability, page 2253
    confidence: high
    flags:
    - Relationship coded as `correlational` per KB rules.
    - 'Note: paper reports R² (not partial R²) for AF predicting BNT, while earlier
      outcomes used partial R². The paper text says ''AF lesion load (R²=0.159)''
      — coded as stated; may reflect total vs partial R² inconsistency in reporting.'
    - UF trend (p=0.073) not significant but noted — consistent with dual-stream predictions
      for naming; not coded as a separate finding given it did not reach threshold.
  source_passages:
  - section: Results — Naming Ability
    page: 3
    quote: A final regression analysis was conducted using the same 4 variables to
      predict naming ability (adjusted R²=0.417, P=0.001). AF lesion load (R²=0.159,
      P=0.039) significantly predicted Boston Naming Test score, and UF lesion load
      displayed a nonsignificant trend (R²=0.123, P=0.073). Neither EmC lesion load
      (partial R²=0.069, P=0.187) nor lesion size (partial R²=0.029, P=0.399) significantly
      predicted Boston Naming Test score.
    supports: statistics
  - section: Abstract
    page: 1
    quote: Regression analyses showed that arcuate fasciculus lesion load, but not
      extreme capsule or uncinate fasciculus lesion load or overall lesion size, significantly
      predicted rate, informativeness, and overall efficiency of speech as well as
      naming ability.
    supports: claim
  - section: Methods — Behavioral Assessments
    page: 2
    quote: In addition to assessing spontaneous speech, we also evaluated each patient's
      naming ability using an untimed version of the Boston Naming Test. Patients
      were given a full point (1.0) for items they could name unassisted, 0.5 points
      for items named with help of a semantic or phonemic cue, and 0.25 points for
      items they could identify by choosing the correct written word (from a set of
      4 words presented in conjunction with the picture stimulus).
    supports: method
- id: f5
  target: left_extreme_capsule
  target_kind: region
  claim: Extreme capsule lesion load does not significantly predict any measure of
    speech production (rate, informativeness, efficiency) or naming ability, contrary
    to predictions from dual-stream models in which the extreme capsule mediates sound-to-meaning
    mapping.
  direction: no_effect
  relationship: correlational
  citation: '@Marchina2011'
  method: tractography
  design: cross-sectional
  imaging: multimodal
  sample:
    n: 30
    population: chronic stroke survivors with left-hemisphere MCA infarct and residual
      speech production impairments
    time_post_onset: '>=11 months post-stroke; mean 35.0 months (SD 28.7)'
    age_range: mean age 58.5 years (SD 10.0)
    handedness: all right-handed
    language: not_reported
    recruitment: Beth Israel Deaconess Medical Center / Harvard Medical School
    inclusion_criteria: right-handed; left-hemispheric MCA stroke; >=11 months post-stroke;
      adequate comprehension and cognition.
    exclusion_criteria: as per f1.
  statistics:
    threshold: multiple regression; p>0.05 for all EmC partial R² values.
    cluster_extent: null
    effect_size: 'EmC partial R²: WPM=0.087 (p=0.135); %CIUs=0.052 (p=0.520); CIUs/min=0.086
      (p=0.138); BNT=0.069 (p=0.187) — all nonsignificant'
    ci_95: not_reported
    p_value: 0.135 (WPM); 0.520 (%CIUs); 0.138 (CIUs/min); 0.187 (BNT)
  confounders_controlled:
  - overall lesion size
  - AF lesion load
  - UF lesion load
  confounders_not_controlled:
  - age
  - time post-stroke
  - sex
  region_definition:
    kind: tract
    description: 'EmC probabilistic map from DTI tractography in 10 healthy controls.
      ROIs: sagittal slice (x=-37) in white matter underlying pars orbitalis and triangularis
      of IFG; same slice in midportion of white matter underlying superior temporal
      gyrus.'
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: DTI
      sequence: single-shot spin-echo EPI
      voxel_size_mm:
      - 2.6
      - 2.6
      - 2.6
      TR_ms: 10000
      TE_ms: 86.9
      n_directions: 30
      b_values:
      - 0
      - 1000
      notes: Healthy controls only; n=10.
    preprocessing_pipeline: SPM5; probabilistic EmC map from 10 controls; weighted-sum
      lesion-load per Zhu et al. 2010.
    reference_space: Talairach
    atlases_used: []
  replications: []
  contradictions: []
  author_limitations:
  - Authors suggest EmC null finding may reflect that behavioral measures used (WPM,
    %CIUs, CIUs/min) blend articulatory and semantic demands, making them more sensitive
    to AF damage overall.
  - The AF may be more vulnerable in MCA strokes (runs dorsal to sylvian fissure,
    in superior MCA division territory) while EmC and UF may be less consistently
    affected, producing floor effects in lesion load variability.
  - Bihemispheric redundancy of the ventral stream (UF/EmC) may mean unilateral damage
    is less functionally impactful.
  evidence_quality: cohort
  strength: weak
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results — Rate, Informativeness, Overall Efficiency, Naming sections,
      page 2253
    confidence: high
    flags:
    - 'Null finding coded for completeness. `direction: no_effect` — absence of significant
      EmC effect across all four speech outcomes.'
    - This null result is substantively meaningful as it contrasts with dual-stream
      predictions for a ventral-stream role of EmC in semantic processing.
  source_passages:
  - section: Results — Rate of Speech
    page: 3
    quote: EmC lesion load (partial R²=0.087, P=0.135), UF lesion load (partial R²=0.098,
      P=0.112), and lesion size (partial R²=0.002, P=0.829) were shown to be nonsignificant
      predictors.
    supports: statistics
  - section: Discussion
    page: 4
    quote: AF lesion load, but not EmC or UF lesion load, significantly predicted
      rate, informativeness, and overall efficiency of speech in patients with impairments
      of speech production after stroke.
    supports: claim
  - section: Discussion
    page: 4
    quote: the AF mainly runs dorsal to the sylvian fissure, which is supplied by
      the superior division of the middle cerebral artery, and the region of the brain
      supplied by the superior division of the middle cerebral artery is the area
      most frequently affected by a stroke.
    supports: confounders
notes: "This draft covers all primary findings from Marchina et al. 2011 (Stroke 42:2251-2256).\n\
  \nThe paper's central contribution is quantifying left AF lesion load (volume of\
  \ tract\ndamaged) using probabilistic DTI maps from healthy controls overlaid onto\
  \ patient lesion\nmaps. Four findings are extracted (f1–f4): AF lesion load predicts\
  \ speech rate (WPM),\ninformativeness (%CIUs), overall efficiency (CIUs/min), and\
  \ confrontation naming (BNT).\nA fifth finding (f5) captures the null result for\
  \ extreme capsule, which is substantively\nmeaningful for dual-stream model interpretation.\n\
  \nKey methodological notes:\n- Relationship coded `correlational` throughout: the\
  \ paper uses a tract-lesion overlap\n  approach (not VLSM/LSM), and the probabilistic\
  \ tract maps come from healthy controls,\n  not from the patients' own DTI. The\
  \ lesion-load method is more analogous to ROI-based\n  structural analysis than\
  \ to direct LSM.\n- All four behavioral outcomes correlate most strongly with AF\
  \ (not EmC or UF), which\n  the authors discuss as inconsistent with strict dual-stream\
  \ predictions.\n- Target IDs for impairments (`speech_production_rate`, `speech_informativeness`,\n\
  \  `speech_efficiency`, `confrontation_naming`) and for the null-finding region\n\
  \  (`left_extreme_capsule`) are forward-looking — stubs should be created at promotion\
  \ time.\n- @Marchina2011 is already listed in citations.md as [cited]; update to\
  \ [extracted]\n  after promotion.\n"
reviewer: claude-cowork
reviewed_on: '2026-05-06'
---
