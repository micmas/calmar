---
schema_version: 2.3
id: left_precentral_gyrus
name: Left Precentral Gyrus
kind: classical
status: approved
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-06
hemisphere: left
aliases:
- left precentral gyrus
- left motor cortex (speech face area)
- left primary motor cortex
notes: 'Basilakos et al. 2015 (Stroke), USC/MUSC cohort (n=43 chronic stroke survivors).

  COHORT_OVERLAP_FLAG: USC/MUSC lab (Rorden, Bonilha, Fridriksson); likely overlaps
  with

  other USC papers including @DenOuden2019, @Fridriksson2018.

  Paper uses VLSM with continuous T1 signal intensity (not binary lesions) as damage
  measure.

  Key finding: left precentral/postcentral gyrus damage predicts AOS-specific errors;

  insula and IFGpo damage predicts aphasia-related speech errors (not AOS-specific).

  Directly contests Dronkers (1996) insula-AOS localization.

  '
findings:
- id: f1
  target: apraxia_of_speech
  target_kind: impairment
  claim: Damage to left precentral gyrus (and adjacent postcentral gyrus) specifically
    predicts speech production errors characteristic of AOS, independent of aphasia-related
    speech errors.
  direction: likely
  relationship: causal
  citation: '@Basilakos2015'
  method: VLSM
  design: cross-sectional
  imaging: structural_MRI
  sample:
    n: 43
    population: chronic left-hemisphere ischemic stroke survivors (with and without
      aphasia)
    time_post_onset: mean 52.5 months (SD 38.9); all >6 months post-stroke
    age_range: mean 59.2 years (SD 10.7)
    handedness: not_reported (likely right-handed per USC inclusion criteria)
    language: not_reported
    recruitment: USC stroke study; single-event left-hemisphere stroke
    inclusion_criteria: Single-event ischemic stroke; left-hemisphere stroke; chronic
      phase (>6 months post-stroke); no history of other neurological disease or developmental
      language abnormalities.
    exclusion_criteria: Multiple strokes; right-hemisphere stroke; history of neurological
      disease; developmental language abnormalities.
  statistics:
    threshold: p<0.05 permutation-corrected (4000 permutations); TFCE (threshold-free
      cluster enhancement)
    cluster_extent: 2508 voxels survived thresholding for AOS errors (TFCE threshold
      12.49)
    effect_size: not_reported
    ci_95: not_reported
    p_value: p<0.05 familywise error controlled
  confounders_controlled:
  - Aphasia-related speech severity entered as nuisance regressor for AOS analysis
    (Freedman-Lane regression)
  - AOS severity entered as nuisance regressor for aphasia analysis
  - TFCE for spatial smoothing/multiple comparisons
  - Continuous T1 signal intensity used rather than binary lesion (greater sensitivity)
  confounders_not_controlled:
  - Handedness not explicitly reported
  - Overall lesion size not explicitly covaried
  - Dysarthria rated but not analyzed (excluded from main analyses)
  - Cohort overlap with other USC/MUSC papers
  region_definition:
    kind: atlas
    atlas: Johns Hopkins University (JHU) atlas (Faria et al., 2012); precentral gyrus
      ROI
  imaging_details:
    reference_space: MNI152
    atlases_used:
    - JHU atlas (Faria et al., 2012; Mori et al., 2008)
    modalities:
    - modality: T1
    - modality: T2
  author_limitations:
  - JHU atlas does not subdivide insula into subregions (SPGI vs. other); limits comparison
    with Dronkers (1996)
  - Continuous T1 signal analysis may introduce error if right-hemisphere diaschisis
    altered signal
  - Cohort includes patients with dysarthria (rated but excluded from main analysis)
  - Single rater for behavioral scoring (though ICC=0.884 established)
  evidence_quality: cohort
  strength: moderate
  cohort_overlap_flag: true
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Abstract; Results – Neuroimaging; Discussion; Table 2
    confidence: high
    flags:
    - USC/MUSC cohort; likely overlaps with @DenOuden2019 and @Fridriksson2018 (same
      lab group)
    - Continuous T1 signal intensity used rather than binary lesion masks — unusual
      method, reduces comparability
    - No separate JHU insula subregion; Dronkers SPGI cannot be directly tested
  source_passages:
  - section: Results – Neuroimaging
    quote: The cluster common to AOS-specific speech errors was distributed across
      the precentral and postcentral gyri
    page: 3
    supports: claim
  - section: Results – Neuroimaging
    quote: 2508 voxels survived thresholding for severity of speech errors associated
      with AOS
    page: 3
    supports: statistics
  - section: Methods – Participants
    quote: Forty-three patients who incurred a single-event left-hemisphere stroke
    page: 2
    supports: sample
  - section: Methods – Lesion Symptom Mapping Analysis
    quote: Freedman–Lane regression where each behavioral variable acted as a nuisance
      regressor for the other
    page: 3
    supports: method
  - section: Discussion
    quote: we did not find evidence of insula involvement in predicting AOS, similar
      to recent studies with primary progressive apraxia of speech
    page: 5
    supports: claim
- id: f2
  target: aphasia_speech_production_errors
  target_kind: impairment
  claim: Damage to left temporal lobe (superior temporal gyrus, posterior middle temporal
    gyrus) and inferior prefrontal regions (insula, IFG orbitalis/triangularis) predicts
    speech production errors that can occur in aphasia but not specifically in AOS.
  direction: likely
  relationship: causal
  citation: '@Basilakos2015'
  method: VLSM
  design: cross-sectional
  imaging: structural_MRI
  sample:
    n: 43
    population: chronic left-hemisphere ischemic stroke survivors (with and without
      aphasia)
    time_post_onset: mean 52.5 months (SD 38.9); all >6 months post-stroke
    age_range: mean 59.2 years (SD 10.7)
    handedness: not_reported
    language: not_reported
    recruitment: USC stroke study
    inclusion_criteria: Single-event ischemic stroke; left-hemisphere stroke; chronic
      phase.
    exclusion_criteria: Multiple strokes; right-hemisphere stroke; history of neurological
      disease.
  statistics:
    threshold: p<0.05 permutation-corrected (4000 permutations); TFCE threshold 12.86
    cluster_extent: 15639 voxels survived thresholding for aphasia-related errors
    effect_size: not_reported
    ci_95: not_reported
    p_value: p<0.05 familywise error controlled
  confounders_controlled:
  - AOS severity entered as nuisance regressor for aphasia analysis (Freedman-Lane
    regression)
  - TFCE for multiple comparisons
  confounders_not_controlled:
  - Overall lesion size not explicitly covaried
  - Cohort overlap with other USC/MUSC papers
  region_definition:
    kind: atlas
    atlas: JHU atlas; top ROIs include superior temporal gyrus (9.66%), posterior
      middle temporal gyrus (8.53%), posterior superior temporal gyrus (5.73%), insula
      (4.74%)
  imaging_details:
    reference_space: MNI152
    atlases_used:
    - JHU atlas (Faria et al., 2012; Mori et al., 2008)
    modalities:
    - modality: T1
    - modality: T2
  author_limitations:
  - Aphasia-related speech errors overlap substantially with general aphasia lesion
    distribution; large cluster (15639 voxels) suggests non-specific pattern
  - Cohort overlap with other USC/MUSC papers
  evidence_quality: cohort
  strength: moderate
  cohort_overlap_flag: true
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results – Neuroimaging; Discussion; Table 1
    confidence: high
    flags:
    - USC/MUSC cohort; likely overlaps with @DenOuden2019 and @Fridriksson2018
    - Large cluster (15639 voxels) for aphasia-related errors; may be non-specific
  source_passages:
  - section: Results – Neuroimaging
    quote: cluster associated with aphasic speech errors was distributed across many
      anatomic regions in the inferior prefrontal and temporal regions
    page: 3
    supports: claim
  - section: Results – Neuroimaging
    quote: 2508 voxels survived thresholding for severity of speech errors associated
      with AOS
    page: 3
    supports: statistics
  - section: Discussion
    quote: damage to this area was a significant predictor for speech errors that
      can occur in aphasia but did not survive thresholding for severity of speech
      errors that are characteristic of AOS
    page: 5
    supports: claim
- id: f3
  target: apraxia_of_speech
  target_kind: impairment
  claim: Damage to the posterior wall of the left precentral gyrus (central sulcus
    face area) is the critical lesion site for AOS in acute ischemic stroke, particularly
    for pure AOS without accompanying aphasia.
  direction: likely
  relationship: causal
  citation: '@Itabashi2015'
  method: VLSM
  design: cross-sectional
  imaging: structural_MRI
  sample:
    n: 136
    population: consecutive acute left MCA territory ischemic stroke patients; Japanese-speaking
    time_post_onset: median 7 days to speech/language evaluation (IQR 5-10); acute/subacute
      phase
    age_range: mean 70.5 years (SD 12.9); median NIHSS 5 (IQR 2-10)
    handedness: all right-handed (inclusion criterion)
    language: Japanese (native speakers)
    recruitment: Consecutive admissions to Kohnan Hospital (Sendai, Japan), April
      2007-March 2012
    inclusion_criteria: First-ever stroke; isolated nonlacunar infarcts in left MCA
      territory on MRI; right-handed; no prior dementia; speech-language evaluation
      during hospital stay.
    exclusion_criteria: Severely reduced spontaneous speech (motor assessment not
      feasible); inadequate brain imaging (3 cases excluded); lacunar infarct; bilateral
      or right-hemisphere lesion.
  statistics:
    threshold: 5% familywise error rate; 3000 permutations; Liebermeister test
    cluster_extent: minimum 3% of subjects with lesion per voxel included
    effect_size: Z_max=4.247 (all AOS vs non-AOS); Z_max=3.482 (pure AOS vs non-AOS)
    ci_95: not_reported
    p_value: threshold Z>=2.838 (all AOS vs non-AOS); Z>=2.995 (pure AOS vs non-AOS)
  confounders_controlled:
  - Group comparisons use Liebermeister test (nonparametric)
  - 5% familywise error with permutation testing
  - Pure AOS group isolated from AOS+aphasia to avoid confounding by aphasia
  confounders_not_controlled:
  - Qualitative (not quantitative) AOS assessment; no inter-rater reliability formally
    reported
  - Acute assessment: lesion extent on T2/FLAIR may underestimate final infarct
  - Age differences between groups (not statistically significant but trend)
  - Japanese language (agglutinative); agrammatism assessment differs from English
    studies
  region_definition:
    kind: atlas
    atlas: Automated Anatomic Labeling (AAL; Tzourio-Mazoyer et al., 2002) and Anatomy
      toolbox (Eickhoff et al., 2005); posterior wall of precentral gyrus in central
      sulcus
  imaging_details:
    reference_space: MNI152
    atlases_used:
    - AAL (Tzourio-Mazoyer et al., 2002)
    - Anatomy toolbox (Eickhoff et al., 2005)
    modalities:
    - modality: T2
    - modality: FLAIR
  author_limitations:
  - Speech-language assessments qualitative; inter-rater reliability not formally
    examined
  - T2/FLAIR at acute stage may underestimate lesion extent compared to later imaging
  - AOS diagnosis complicated in patients with concomitant aphasia (phonemic paraphasia
    shares features with AOS)
  - Lesion functional effects may extend beyond visible infarction area (diaschisis)
  evidence_quality: cohort
  strength: moderate
  cohort_overlap_flag: false
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Abstract; Results; Discussion; Table
    confidence: high
    flags:
    - Japanese-speaking cohort; acute/subacute phase (median 7 days); no cohort overlap
      with USC papers
    - Qualitative AOS assessment only; no standardized rating scale (unlike Basilakos
      2015)
    - Independent replication of Basilakos (2015) left precentral gyrus finding
  source_passages:
  - section: Results
    quote: The regions associated with all AOS (pure AOS plus AOSaphasia) were centered
      on the posterior wall of the left precentral gyrus in the central sulcus
    page: 3
    supports: claim
  - section: Results
    quote: posterior wall of the left precentral gyrus predicted the presence of AOS
      in the comparison between pure AOS and non-AOS
    page: 3
    supports: claim
  - section: Abstract
    quote: 136 patients with isolated nonlacunar infarcts in the left middle cerebral
      artery territory
    page: 1
    supports: sample
  - section: Methods – Voxel-Based Lesion-Symptom Mapping
    quote: voxels in which ≥3% of the subjects had lesions were included in the analysis.
      A 5% family-wise thresholding with 3000 permutations
    page: 2
    supports: method
  - section: Discussion
    quote: The regions associated with pure AOS were confined to the left precentral
      gyrus in the VLSM
    page: 4
    supports: claim
- id: f4
  target: apraxia_of_speech_with_aphasia
  target_kind: impairment
  claim: AOS co-occurring with aphasia (AOS-aphasia) is associated with more widespread
    subcortical lesions (basal ganglia, corona radiata, centrum semiovale) in addition
    to precentral gyrus damage, reflecting larger total lesion burden.
  direction: likely
  relationship: causal
  citation: '@Itabashi2015'
  method: VLSM
  design: cross-sectional
  imaging: structural_MRI
  sample:
    n: 136
    population: consecutive acute left MCA territory ischemic stroke patients; Japanese-speaking
    time_post_onset: median 7 days (IQR 5-10); acute/subacute phase
    age_range: mean 70.5 years (SD 12.9)
    handedness: all right-handed
    language: Japanese
    recruitment: Kohnan Hospital consecutive admissions
    inclusion_criteria: First-ever stroke; isolated nonlacunar infarcts in left MCA
      territory; right-handed; no prior dementia.
    exclusion_criteria: Severely reduced spontaneous speech; inadequate imaging; lacunar
      infarct.
  statistics:
    threshold: 5% familywise error rate; 3000 permutations; Z>=3.005
    cluster_extent: scattered clusters across basal ganglia, corona radiata, centrum
      semiovale, precentral gyrus
    effect_size: Z_max=4.806 (AOS-aphasia vs non-AOS)
    ci_95: not_reported
    p_value: corrected alpha=0.05
  confounders_controlled:
  - Statistical comparison against non-AOS group
  - Permutation familywise error correction
  confounders_not_controlled:
  - Overall lesion size (AOS-aphasia group tends to have larger lesions)
  - Subcortical patterns may reflect white matter pathway damage rather than region-specific
    effect
  region_definition:
    kind: atlas
    atlas: AAL and Anatomy toolbox; subcortical regions including basal ganglia, corona
      radiata
  imaging_details:
    reference_space: MNI152
    atlases_used:
    - AAL (Tzourio-Mazoyer et al., 2002)
    - Anatomy toolbox (Eickhoff et al., 2005)
    modalities:
    - modality: T2
    - modality: FLAIR
  author_limitations:
  - AOS+aphasia patients have larger lesions on average; VLSM may detect lesion-size-driven
    spatial extent rather than functionally specific regions
  - Differential diagnosis of AOS in presence of aphasia is more difficult
  evidence_quality: cohort
  strength: moderate
  cohort_overlap_flag: false
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results; Discussion
    confidence: medium
    flags:
    - AOS+aphasia finding reflects lesion size confound; interpret with caution
    - Subcortical involvement may indicate white matter pathway disruption rather
      than grey matter specificity
  source_passages:
  - section: Results
    quote: AOS-aphasia and non-AOS indicated scattered lesions, including the basal
      ganglia, corona radiata
    page: 4
    supports: claim
  - section: Discussion
    quote: patients who have both AOS and aphasia tend to have larger size of lesions
      and greater involvement of subcortical structures
    page: 4
    supports: claim
  - section: Discussion
    quote: diagnosis of AOS is more problematic in patients with both AOS and aphasia
      compared with pure AOS
    page: 4
    supports: limitation
- id: f5
  target: apraxia_of_speech
  target_kind: impairment
  claim: Damage to the posterior wall of the left precentral gyrus (central sulcus
    face area) is the critical lesion site for AOS in acute ischemic stroke, particularly
    for pure AOS without accompanying aphasia.
  direction: likely
  relationship: causal
  citation: '@Itabashi2015'
  method: VLSM
  design: cross-sectional
  imaging: structural_MRI
  sample:
    n: 136
    population: consecutive acute left MCA territory ischemic stroke patients; Japanese-speaking
    time_post_onset: median 7 days to speech/language evaluation (IQR 5-10); acute/subacute
      phase
    age_range: mean 70.5 years (SD 12.9); median NIHSS 5 (IQR 2-10)
    handedness: all right-handed (inclusion criterion)
    language: Japanese (native speakers)
    recruitment: Consecutive admissions to Kohnan Hospital (Sendai, Japan), April
      2007-March 2012
    inclusion_criteria: First-ever stroke; isolated nonlacunar infarcts in left MCA
      territory on MRI; right-handed; no prior dementia; speech-language evaluation
      during hospital stay.
    exclusion_criteria: Severely reduced spontaneous speech (motor assessment not
      feasible); inadequate brain imaging (3 cases excluded); lacunar infarct; bilateral
      or right-hemisphere lesion.
  statistics:
    threshold: 5% familywise error rate; 3000 permutations; Liebermeister test
    cluster_extent: minimum 3% of subjects with lesion per voxel included
    effect_size: Z_max=4.247 (all AOS vs non-AOS); Z_max=3.482 (pure AOS vs non-AOS)
    ci_95: not_reported
    p_value: threshold Z>=2.838 (all AOS vs non-AOS); Z>=2.995 (pure AOS vs non-AOS)
  confounders_controlled:
  - Group comparisons use Liebermeister test (nonparametric)
  - 5% familywise error with permutation testing
  - Pure AOS group isolated from AOS+aphasia to avoid confounding by aphasia
  confounders_not_controlled:
  - Qualitative (not quantitative) AOS assessment; no inter-rater reliability formally
    reported
  - Acute assessment: lesion extent on T2/FLAIR may underestimate final infarct
  - Age differences between groups (not statistically significant but trend)
  - Japanese language (agglutinative); agrammatism assessment differs from English
    studies
  region_definition:
    kind: atlas
    atlas: Automated Anatomic Labeling (AAL; Tzourio-Mazoyer et al., 2002) and Anatomy
      toolbox (Eickhoff et al., 2005); posterior wall of precentral gyrus in central
      sulcus
  imaging_details:
    reference_space: MNI152
    atlases_used:
    - AAL (Tzourio-Mazoyer et al., 2002)
    - Anatomy toolbox (Eickhoff et al., 2005)
    modalities:
    - modality: T2
    - modality: FLAIR
  author_limitations:
  - Speech-language assessments qualitative; inter-rater reliability not formally
    examined
  - T2/FLAIR at acute stage may underestimate lesion extent compared to later imaging
  - AOS diagnosis complicated in patients with concomitant aphasia (phonemic paraphasia
    shares features with AOS)
  - Lesion functional effects may extend beyond visible infarction area (diaschisis)
  evidence_quality: cohort
  strength: moderate
  cohort_overlap_flag: false
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Abstract; Results; Discussion; Table
    confidence: high
    flags:
    - Japanese-speaking cohort; acute/subacute phase (median 7 days); no cohort overlap
      with USC papers
    - Qualitative AOS assessment only; no standardized rating scale (unlike Basilakos
      2015)
    - Independent replication of Basilakos (2015) left precentral gyrus finding
  source_passages:
  - section: Results
    quote: The regions associated with all AOS (pure AOS plus AOSaphasia) were centered
      on the posterior wall of the left precentral gyrus in the central sulcus
    page: 3
    supports: claim
  - section: Results
    quote: posterior wall of the left precentral gyrus predicted the presence of AOS
      in the comparison between pure AOS and non-AOS
    page: 3
    supports: claim
  - section: Abstract
    quote: 136 patients with isolated nonlacunar infarcts in the left middle cerebral
      artery territory
    page: 1
    supports: sample
  - section: Methods – Voxel-Based Lesion-Symptom Mapping
    quote: voxels in which ≥3% of the subjects had lesions were included in the analysis.
      A 5% family-wise thresholding with 3000 permutations
    page: 2
    supports: method
  - section: Discussion
    quote: The regions associated with pure AOS were confined to the left precentral
      gyrus in the VLSM
    page: 4
    supports: claim
- id: f6
  target: apraxia_of_speech_with_aphasia
  target_kind: impairment
  claim: AOS co-occurring with aphasia (AOS-aphasia) is associated with more widespread
    subcortical lesions (basal ganglia, corona radiata, centrum semiovale) in addition
    to precentral gyrus damage, reflecting larger total lesion burden.
  direction: likely
  relationship: causal
  citation: '@Itabashi2015'
  method: VLSM
  design: cross-sectional
  imaging: structural_MRI
  sample:
    n: 136
    population: consecutive acute left MCA territory ischemic stroke patients; Japanese-speaking
    time_post_onset: median 7 days (IQR 5-10); acute/subacute phase
    age_range: mean 70.5 years (SD 12.9)
    handedness: all right-handed
    language: Japanese
    recruitment: Kohnan Hospital consecutive admissions
    inclusion_criteria: First-ever stroke; isolated nonlacunar infarcts in left MCA
      territory; right-handed; no prior dementia.
    exclusion_criteria: Severely reduced spontaneous speech; inadequate imaging; lacunar
      infarct.
  statistics:
    threshold: 5% familywise error rate; 3000 permutations; Z>=3.005
    cluster_extent: scattered clusters across basal ganglia, corona radiata, centrum
      semiovale, precentral gyrus
    effect_size: Z_max=4.806 (AOS-aphasia vs non-AOS)
    ci_95: not_reported
    p_value: corrected alpha=0.05
  confounders_controlled:
  - Statistical comparison against non-AOS group
  - Permutation familywise error correction
  confounders_not_controlled:
  - Overall lesion size (AOS-aphasia group tends to have larger lesions)
  - Subcortical patterns may reflect white matter pathway damage rather than region-specific
    effect
  region_definition:
    kind: atlas
    atlas: AAL and Anatomy toolbox; subcortical regions including basal ganglia, corona
      radiata
  imaging_details:
    reference_space: MNI152
    atlases_used:
    - AAL (Tzourio-Mazoyer et al., 2002)
    - Anatomy toolbox (Eickhoff et al., 2005)
    modalities:
    - modality: T2
    - modality: FLAIR
  author_limitations:
  - AOS+aphasia patients have larger lesions on average; VLSM may detect lesion-size-driven
    spatial extent rather than functionally specific regions
  - Differential diagnosis of AOS in presence of aphasia is more difficult
  evidence_quality: cohort
  strength: moderate
  cohort_overlap_flag: false
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results; Discussion
    confidence: medium
    flags:
    - AOS+aphasia finding reflects lesion size confound; interpret with caution
    - Subcortical involvement may indicate white matter pathway disruption rather
      than grey matter specificity
  source_passages:
  - section: Results
    quote: AOS-aphasia and non-AOS indicated scattered lesions, including the basal
      ganglia, corona radiata
    page: 4
    supports: claim
  - section: Discussion
    quote: patients who have both AOS and aphasia tend to have larger size of lesions
      and greater involvement of subcortical structures
    page: 4
    supports: claim
  - section: Discussion
    quote: diagnosis of AOS is more problematic in patients with both AOS and aphasia
      compared with pure AOS
    page: 4
    supports: limitation
reviewer: auto-reviewer
reviewed_on: '2026-05-06'
last_reviewed: '2026-05-07'
---
## Summary

Basilakos et al. (2015) used VLSM with continuous T1-signal-intensity damage maps in 43 chronic left-hemisphere stroke survivors (USC cohort) to dissociate brain lesion patterns underlying AOS-specific speech errors from those underlying speech errors also seen in aphasia. AOS-specific errors mapped to left precentral/postcentral gyrus and associated white matter (superior corona radiata, superior longitudinal fasciculus, supramarginal gyrus). Aphasia-related speech errors mapped to left temporal lobe and inferior prefrontal regions. The insula and IFGpo did not predict AOS-specific errors. This paper directly challenges the Dronkers (1996) insula localization.
