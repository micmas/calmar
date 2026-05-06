---
schema_version: 2.3
id: lesion_volume
name: "Lesion Volume"
predictor_type: imaging_metric
kind: predictor
status: draft
created_by: "agent:claude-sonnet-4-6"
created_on: 2026-05-06
short_definition: "Total lesion volume (ml) on structural MRI, used as a predictor of aphasia severity and recovery outcome."

findings:
  - id: f1
    target: severity_metric
    target_kind: predictor
    claim: >
      Smaller total lesion volume is associated with greater long-term WAB-R AQ
      improvement in chronic aphasia patients retested at least one year after initial
      chronic-stage assessment; lesion volume was the only significant demographic or
      stroke-related predictor in the regression model.
    direction: likely
    relationship: correlational
    citation: "@Harvey2022"

    method: VLSM
    design: longitudinal
    imaging: multimodal

    sample:
      n: 18
      population: "chronic left-hemisphere stroke survivors with aphasia initially assessed at 5+ months post-onset"
      time_post_onset: "5–133 months at initial assessment (mean 39.8 months); follow-up 21–94 months after initial testing (mean 61 months)"
      age_range: "mean 52.9 ± 12.7 years; range 30–77"
      handedness: "premorbid right-handed"
      language: "native English speakers"
      recruitment: "Neuro-Cognitive Rehabilitation Research Patient Registry, Moss Rehabilitation Research Institute / University of Pennsylvania"
      inclusion_criteria: "initial language assessment at 5+ MPO; native English speaker; premorbid right-handed; normal/corrected vision and hearing; no comorbid neurological/psychiatric disorders; 1+ year interval between initial and follow-up testing; CT or MRI at initial assessment"
      exclusion_criteria: "did not meet above criteria; moved before completing testing; ongoing life stressors affecting language performance"

    statistics:
      threshold: "multiple linear regression, F(4,13)=3.51, p=.037, R²=0.519 (unadjusted), R²adj=0.37"
      cluster_extent: not_reported
      effect_size: "Lesion Volume coefficient (Table 2): b = −0.11, SE = 0.05, β = −0.53 (the only significant predictor; negative weight ⇒ smaller lesion → larger AQ gain)"
      ci_95: not_reported
      p_value: "p < .05"

    confounders_controlled:
      - "months post-onset (MPO) at initial assessment"
      - "age at stroke"
      - "years of education"
    confounders_not_controlled:
      - "sex (removed from model due to violation of normality assumption)"
      - "leukoaraiosis / white matter hyperintensity severity"
      - "specific lesion location (covaried separately via lesion subtraction and VLSM, not in regression)"
      - "amount of speech-language therapy received (entered separately in psychosocial model)"

    region_definition:
      kind: not_reported
      description: "Behavioural-only predictor finding — lesion volume is the imaging metric; no specific brain region targeted in this finding. Lesions manually segmented from T1 MRI or CT, warped to MNI Colin27 template via symmetric diffeomorphic registration (ANTs); volume computed with VoxBo."

    imaging_details:
      field_strength: "3T (15/18 participants); CT (3/18 participants who were MRI ineligible)"
      acquisition:
        sequence: "T1-weighted MPRAGE (MRI) or CT"
        voxel_size_mm: not_reported
      preprocessing_pipeline: "manual lesion segmentation on T1 structural by trained technician; reviewed by neurologist blinded to behavioral data; warped to MNI Colin27 template via ANTs symmetric diffeomorphic registration; VoxBo for lesion volume"
      reference_space: "MNI152"
      atlases_used:
        - "AAL (Tzourio-Mazoyer 2002) for gray matter region identification in lesion subtraction"
        - "Catani atlas for white matter pathway identification"
      coordinates_reported: []

    replications: []
    contradictions:
      - "@Basilakos2019 — lesion volume not significant after controlling for leukoaraiosis"
      - "@Hope2017 — no significant lesion volume difference between improved/not-improved groups"

    author_limitations:
      - "Small convenience sample (n=18); retrospective design limits causal inference."
      - "Sex violated normality assumption and was removed from the regression model."
      - "Three participants imaged via CT rather than MRI, reducing lesion volume precision."
      - "Psychosocial measures collected only at follow-up, not initial assessment, precluding temporal inference about these predictors."
      - "Two participants initially assessed at the cusp of the chronic threshold (5 MPO); excluding them attenuated psychosocial predictor effects."

    evidence_quality: cohort
    strength: moderate

    provenance:
      extracted_by: "agent:claude-sonnet-4-6"
      extracted_on: 2026-05-06
      paper_section: "Results – Regression results (pp. 9–10); Methods – Participants (p. 4–5); Neuroimaging Data (p. 6)"
      confidence: high
      flags:
        - "3 of 18 participants had CT not MRI — lesion volume measure heterogeneous"

    source_passages:
      - section: "Results – Regression results"
        page: 9
        supports: claim
        quote: >
          lesion volume was the only significant predictor of proportion change in AQ.
          The negative regression weight indicates that smaller lesions yield larger language
          gains in the long term, after controlling for other predictors included in the model.
      - section: "Methods – Participants"
        page: 5
        supports: sample
        quote: >
          The 18 individuals included in the study (12 male) had a mean age of 52.9
          (standard deviation (SD) = ±12.7; range = 30–77), years of education of 15
          (SD = ±3.2; range = 12–21), and MPO of 39.8 (SD = ±39.2; range = 5–133)
          at the initial assessment.
      - section: "Methods – Neuroimaging Data"
        page: 6
        supports: imaging_details
        quote: >
          Lesions obtained via MRI were manually segmented on the structural image by a
          trained technician, and checked for accuracy by an experienced neurologist blinded
          to the behavioral data. Lesion tracings were then warped to a standard atlas space
          (i.e., the Montreal Neurological Institute (MNI) Colin27 template) using a symmetric
          diffeomorphic registration algorithm.
      - section: "Results – Regression results"
        page: 9
        supports: statistics
        quote: >
          The final regression model with four predictor variables explained 51.9% (unadjusted
          R2) of the variance, F(4, 13) = 3.51, p = .037, R2Adjusted = .37.
      - section: "Discussion – Limitations / Conclusion"
        page: 14
        supports: limitation
        quote: >
          because this study was conducted retrospectively on a small group of people with
          aphasia who represent a self-selected sample of "convenience," it will be important
          for future studies to replicate these findings using a prospective approach in a
          larger sample.

  - id: f2
    target: severity_metric
    target_kind: predictor
    claim: >
      Greater satisfaction with life participation (ALA participation domain) is
      associated with better long-term aphasia recovery (WAB-R AQ gain), independent
      of lesion volume, in chronic aphasia.
    direction: likely
    relationship: correlational
    citation: "@Harvey2022"

    method: behavioral_only
    design: longitudinal
    imaging: none

    sample:
      n: 18
      population: "chronic left-hemisphere stroke survivors with aphasia"
      time_post_onset: "5–133 months at initial assessment; follow-up 21–94 months later"
      age_range: "mean 52.9 ± 12.7 years"
      handedness: "premorbid right-handed"
      language: "native English speakers"
      recruitment: "Moss Rehabilitation Research Institute / University of Pennsylvania registry"
      inclusion_criteria: "as above for f1"
      exclusion_criteria: "as above for f1"

    statistics:
      threshold: "backward stepwise regression, F(3,14)=5.96, p=.008, R²=0.561 (unadjusted), R²adj=0.47"
      cluster_extent: not_reported
      effect_size: "ALA Participation Domain (Table 3): b = 22.94, SE = 6.34, β = 0.94; ALA Aphasia Domain: b = −25.34, SE = 6.26, β = −0.97 (negative weight on perceived impairment; positive weight on participation satisfaction)"
      ci_95: not_reported
      p_value: "ALA Participation: p < .05; ALA Aphasia: p < .01; SLT amount trended (NS)"

    confounders_controlled:
      - "ALA aphasia domain (self-perceived impairment severity) controlled in same model"
      - "amount of SLT received"
    confounders_not_controlled:
      - "lesion volume (entered in separate regression model; combined model shows lesion volume + ALA participation + ALA aphasia explain 68.2% variance)"
      - "psychosocial measures collected only at follow-up"
      - "time post-onset at follow-up assessment"

    region_definition:
      kind: not_reported
      description: "Behavioral/psychosocial predictor finding — no brain region; ALA is a pictographic self-report questionnaire assessing participation, environment, personal, and aphasia domains."

    imaging_details:
      reference_space: not_reported
      atlases_used: []

    replications: []
    contradictions: []

    author_limitations:
      - "ALA collected only at follow-up — cannot determine whether participation satisfaction is stable or situational."
      - "Counterintuitive finding: ALA aphasia domain (perceived impairment severity) negatively related to outcome — more perceived severity associated with better gains. May reflect baseline severity or personal attitudes."
      - "Excluding the 2 participants at the cusp of chronic threshold attenuated psychosocial predictor significance."

    evidence_quality: cohort
    strength: weak

    provenance:
      extracted_by: "agent:claude-sonnet-4-6"
      extracted_on: 2026-05-06
      paper_section: "Results – Regression results (pp. 9–10); Discussion (p.12)"
      confidence: medium
      flags:
        - "Exact coefficients pulled from Table 3 (b/SE/β); paper reports per-coefficient p-values via asterisk-coding (** = p<.05, *** = p<.01) rather than numeric p"
        - "Psychosocial measures assessed only at follow-up, not at initial assessment — temporal directionality of this predictor is uncertain"
        - "Combined model (lesion vol + ALA participation + ALA aphasia) F(4,13)=6.96, p=.003, R²adj=0.58 — strongest model in paper"

    source_passages:
      - section: "Results – Regression results"
        page: 9
        supports: claim
        quote: >
          ALA aphasia and participation domain scores significantly related to proportion
          change in AQ. The positive regression weight for ALA participation domain indicates
          that greater satisfaction with life participation was related to better long-term
          outcomes.
      - section: "Results – Regression results"
        page: 10
        supports: statistics
        quote: >
          The final model explained 68.2% (unadjusted R2) of the variance, F(4, 13) = 6.96,
          p = .003, R2Adjusted = .58, which retained three factors: lesion volume as well as
          ALA scores on the aphasia and participation domains.
      - section: "Discussion"
        page: 12
        supports: limitation
        quote: >
          because we did not obtain these data at initial assessment, we cannot address
          whether the relationship between these psychosocial variables and aphasia recovery
          reflects attitudes that were stable across the chronic period or specific to the
          follow-up assessment.

source: extracted
notes: |
  This paper has two main classes of finding: (1) lesion volume as an imaging-metric predictor
  (f1), and (2) psychosocial participation as a patient-related predictor (f2). Both are anchored
  in the predictor bucket per the extraction rules because the paper's main claim is "X predicts
  long-term WAB-R AQ change" with no specific region-anchored LSM finding driving the primary
  hypothesis. The VLSM and lesion subtraction analyses are supplementary; they identified
  temporoparietal and frontal regions as associated with poor long-term recovery but these were
  uncorrected and exploratory. A separate region draft is not written for those lesion location
  findings because (a) they are uncorrected, (b) n=6 in the "not improved" group is very small,
  and (c) the paper's abstract emphasizes the regression findings. If the user wants the lesion
  location findings extracted, a separate region draft for
  left_temporoparietal_language_network__Harvey2022 could be added.
  
  Instrument for outcome: Western Aphasia Battery-Revised (WAB-R) Aphasia Quotient (AQ).
  Clinically meaningful improvement threshold: >5-point AQ increase (12/18 participants improved).
---
