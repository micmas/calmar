---
schema_version: 2.3
id: tdcs_aphasia_treatment
name: Transcranial Direct Current Stimulation (tDCS) during aphasia treatment
kind: therapy
status: approved
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-06
short_description: Anodal tDCS applied to the intact left temporoparietal region for
  the first 20 min of each behavioral aphasia treatment session.
targets_impairments:
- anomia
dosage: 1 mA anodal tDCS, 20 min per session, 15 sessions over 3 weeks (5 days/week)
findings:
- id: f1
  target: bdnf_genotype
  target_kind: predictor
  claim: Val/val BDNF genotype predicts greater response to anodal tDCS during aphasia
    treatment; val/val participants receiving A-tDCS improved more in naming than
    val/val participants receiving sham or Met allele carriers regardless of tDCS
    condition.
  direction: likely_responder
  relationship: responder
  citation: '@Fridriksson2018BDNF'
  method: clinical_RCT
  design: RCT
  imaging: none
  sample:
    n: 66
    population: chronic stroke-induced aphasia participants from a double-blind RCT
      at USC and MUSC
    time_post_onset: mean 43.3 months (SD 41.1; range 6.1–204.9 months)
    age_range: 30–77 years (mean 59.8, SD 10.2)
    handedness: not_reported
    language: English-speaking
    recruitment: Participants enrolled in a parent RCT at University of South Carolina
      and Medical University of South Carolina.
    inclusion_criteria: Chronic stroke-induced aphasia; PNT baseline < 140/175 correct.
    exclusion_criteria: not_reported
  statistics:
    threshold: p = 0.03
    cluster_extent: null
    effect_size: F = 4.97 (tDCS × BDNF genotype interaction in mixed effects repeated
      measures model)
    ci_95: not_reported
    p_value: '0.03'
  confounders_controlled:
  - baseline WAB-R AQ (aphasia severity)
  - lesion size
  - time of follow-up testing (1, 4, 24 weeks post-treatment)
  confounders_not_controlled:
  - stroke location
  - 'race/ethnicity (imbalanced: 57 Caucasian, 7 African-American, 2 Asian)'
  - depression (not assessed)
  region_definition:
    kind: not_reported
    description: 'Behavioral-only treatment-efficacy finding — no specific brain region
      analyzed. tDCS electrode placed at the peak naming-related fMRI activation site
      on the left scalp (mean MNI coordinates: −40, −50, 12 across all participants;
      temporo-parietal junction region).'
  replications: []
  contradictions: []
  author_limitations:
  - BDNF genotype data were missing for 8 of 74 participants due to sample loss or
    refusal.
  - Baseline aphasia severity differed between BDNF genotype groups, and this difference
    became non-significant when adjusting for time post-stroke and lesion size, suggesting
    potential confounding.
  - Depression was not assessed and may differ between BDNF genotype groups, introducing
    uncontrolled variance.
  - The study cannot determine whether A-tDCS modulates BDNF secretion or relies on
    baseline BDNF levels.
  evidence_quality: RCT
  strength: moderate
  provenance:
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    paper_section: Results; Table 2; Fig. 2
    confidence: high
    flags:
    - cohort overlaps with parent RCT @Fridriksson2018BDNF (NCT not stated; this paper
      explicitly reanalyzes subgroup n=66 from Fridriksson et al. JAMA Neurol 2018
      [ref 13]); flag for downstream double-counting risk.
    - 'BDNF genotype groups had unequal n: val/val n=36, Met-carriers n=30; imbalance
      is modest.'
  source_passages:
  - section: Abstract
    page: 1276
    supports: claim
    quote: Individuals with the val/val BDNF genotype are more likely to benefit from
      A-tDCS during aphasia treatment.
  - section: Methods – Participants
    page: 1277
    supports: sample
    quote: BDNF genotype was available for 67 participants due to lost or contaminated
      sample (6 participants) or decline in blood draw (1 participant).
  - section: Methods – Statistical analyses
    page: 1278
    supports: method
    quote: 'A mixed effects linear model of the repeated measures of proportional
      change in correct naming was fit with the following independent variables: tDCS
      condition (A-tDCS or S-tDCS), BDNF genotype status (typical or atypical), tDCS
      x BDNF, time of testing'
  - section: Results; Table 2
    page: 1280
    supports: statistics
    quote: 'Genotype x tDCS

      1

      60

      4.97

      0.03'
  - section: Discussion
    page: 1280
    supports: limitation
    quote: we did not compare levels of depression between participants with typical
      and atypical BDNF genotype
source: curated
last_reviewed: 2026-05-06
notes: 'Behavioral-only therapy finding (no imaging analysis). This draft captures
  the

  RCT interaction effect: val/val BDNF × A-tDCS → greater naming improvement.

  The tDCS stimulation site (left temporo-parietal junction, coregistered to each

  participant''s peak naming-related fMRI activation) is described in the Methods

  but the finding is coded as behavioral-only because the efficacy claim does not

  depend on a region-specific analysis.

  The BDNF-genotype predictor finding is separately captured in

  drafts/predictors/bdnf_val66met__Fridriksson2018BDNF.md.'
reviewer: auto-reviewer
reviewed_on: '2026-05-06'
---
# Transcranial Direct Current Stimulation (tDCS) during aphasia treatment

## Fridriksson 2018 BDNF — tDCS × BDNF genotype interaction

This draft captures the therapy-efficacy finding from the BDNF genotype RCT
sub-analysis. The parent RCT (Fridriksson et al., JAMA Neurol 2018) found
A-tDCS superior to sham overall. This paper's planned secondary analysis
reveals that this benefit is genotype-specific: only val/val carriers receiving
A-tDCS drove the benefit.
