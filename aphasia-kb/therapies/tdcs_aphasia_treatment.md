---
schema_version: 2.3
id: tdcs_aphasia_treatment
name: Transcranial Direct Current Stimulation (tDCS) during aphasia treatment
kind: therapy
status: approved
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-06
short_description: Anodal tDCS applied to the intact left temporoparietal region for the first 20 min
  of each behavioral aphasia treatment session.
targets_impairments:
- anomia
- anomic_aphasia
- aphasia
- brocas_aphasia
- fluency
dosage: 1 mA anodal tDCS, 20 min per session, 15 sessions over 3 weeks (5 days/week)
atf_id: null
atf_evidence_level: null
evidence_level: level_II
atf_aliases:
  - tDCS aphasia
  - anodal tDCS
icf_domain:
  - body_function
tidier:
  brief_name: Anodal tDCS paired with naming therapy
  rationale: |-
    Anodal tDCS over perilesional left-hemisphere cortex (left IFG, left STG) increases
        neuronal membrane excitability via subthreshold depolarisation, facilitating LTP-
        like synaptic plasticity. When temporally coincident with active naming practice,
        tDCS is hypothesised to potentiate synapse-specific strengthening (Hebbian
        mechanism), augmenting language therapy gains beyond behavioural treatment alone.
  materials: |-
    tDCS device (e.g., Soterix Medical 1×1 CT or Neuroelectrics Starstim); 25 cm²
        conductive rubber electrodes; saline-soaked sponges or conductive gel;
        confrontation naming picture stimuli; electrode placement guide (MRI or 10-20
        landmarks).
  procedures: |-
    Motor threshold assessed (not applicable for tDCS but montage verified). Anodal
        electrode placed over target perilesional region (left IFG or left STG based on
        individual lesion anatomy); cathodal reference over contralateral supraorbital
        region. 1–2 mA delivered for 20 min concurrent with naming practice (online
        stimulation). Sham condition: identical setup with 30-second ramp-up then fade-off
        only.
  who_provides: |-
    SLP (naming therapy component) + trained technician or research nurse (device setup);
        combined SLP-technician role feasible in clinical settings.
  delivery_mode: face_to_face; device-assisted
  setting: Research clinic, hospital outpatient unit, or clinical trial site.
  dosage: |-
    Fridriksson 2018 (BDNF RCT): 1 mA × 20 min/session × 15 sessions over 3 weeks;
        concurrent naming therapy ~30–45 min/session.
  tailoring: |-
    Electrode placement over perilesional cortex individualised by MRI lesion anatomy.
        Stimulation site (left IFG vs left STG) selected based on spared perilesional
        tissue. Stimulation intensity (1 vs 2 mA) may be adjusted for tolerability.
  modifications: |-
    Online (concurrent) vs offline (preceding therapy) stimulation protocols — online now
        preferred based on evidence synthesis. HD-tDCS (high-definition, smaller
        electrodes) offers more focussed stimulation. BDNF Val66Met genotype shown to
        moderate tDCS response (Fridriksson 2018).
  fidelity_planned: |-
    Blinded sham-controlled design; current delivery logged by device; rater-blinded
        outcome assessment; adverse event monitoring log.
  fidelity_actual: |-
    Fridriksson 2018: blinding confirmed at end of study; sham break-blind rate NR; mild
        adverse events (tingling, headache) reported and monitored.
  confidence: medium
  flags:
    - Fridriksson 2018 RCT not formally extracted from papers/. TIDieR populated from
        published protocol. BDNF genotype moderator finding should be flagged in
        clinical application.
rtss_ingredients:
  - anodal_tdcs
findings:
- author_limitations:
  - BDNF genotype data were missing for 8 of 74 participants due to sample loss or refusal.
  - Baseline aphasia severity differed between BDNF genotype groups, and this difference became non-significant
    when adjusting for time post-stroke and lesion size, suggesting potential confounding.
  - Depression was not assessed and may differ between BDNF genotype groups, introducing uncontrolled
    variance.
  - The study cannot determine whether A-tDCS modulates BDNF secretion or relies on baseline BDNF levels.
  citation: '@Fridriksson2018BDNF'
  claim: Val/val BDNF genotype predicts greater response to anodal tDCS during aphasia treatment; val/val
    participants receiving A-tDCS improved more in naming than val/val participants receiving sham or
    Met allele carriers regardless of tDCS condition.
  confounders_controlled:
  - baseline WAB-R AQ (aphasia severity)
  - lesion size
  - time of follow-up testing (1, 4, 24 weeks post-treatment)
  confounders_not_controlled:
  - stroke location
  - 'race/ethnicity (imbalanced: 57 Caucasian, 7 African-American, 2 Asian)'
  - depression (not assessed)
  contradictions: []
  design: RCT
  direction: likely_responder
  evidence_quality: RCT
  id: f1
  imaging: none
  method: clinical_RCT
  provenance:
    confidence: high
    extracted_by: agent:claude-sonnet-4-6
    extracted_on: 2026-05-06
    flags:
    - cohort overlaps with parent RCT @Fridriksson2018BDNF (NCT not stated; this paper explicitly reanalyzes
      subgroup n=66 from Fridriksson et al. JAMA Neurol 2018 [ref 13]); flag for downstream double-counting
      risk.
    - 'BDNF genotype groups had unequal n: val/val n=36, Met-carriers n=30; imbalance is modest.'
    paper_section: Results; Table 2; Fig. 2
  region_definition:
    description: 'Behavioral-only treatment-efficacy finding — no specific brain region analyzed. tDCS
      electrode placed at the peak naming-related fMRI activation site on the left scalp (mean MNI coordinates:
      −40, −50, 12 across all participants; temporo-parietal junction region).'
    kind: not_reported
  relationship: responder
  replications: []
  sample:
    age_range: 30–77 years (mean 59.8, SD 10.2)
    exclusion_criteria: not_reported
    handedness: not_reported
    inclusion_criteria: Chronic stroke-induced aphasia; PNT baseline < 140/175 correct.
    language: English-speaking
    n: 66
    population: chronic stroke-induced aphasia participants from a double-blind RCT at USC and MUSC
    recruitment: Participants enrolled in a parent RCT at University of South Carolina and Medical University
      of South Carolina.
    time_post_onset: mean 43.3 months (SD 41.1; range 6.1–204.9 months)
  source_passages:
  - page: 1276
    quote: Individuals with the val/val BDNF genotype are more likely to benefit from A-tDCS during aphasia
      treatment.
    section: Abstract
    supports: claim
  - page: 1277
    quote: BDNF genotype was available for 67 participants due to lost or contaminated sample (6 participants)
      or decline in blood draw (1 participant).
    section: Methods – Participants
    supports: sample
  - page: 1278
    quote: 'A mixed effects linear model of the repeated measures of proportional change in correct naming
      was fit with the following independent variables: tDCS condition (A-tDCS or S-tDCS), BDNF genotype
      status (typical or atypical), tDCS x BDNF, time of testing'
    section: Methods – Statistical analyses
    supports: method
  - page: 1280
    quote: 'Genotype x tDCS

      1

      60

      4.97

      0.03'
    section: Results; Table 2
    supports: statistics
  - page: 1280
    quote: we did not compare levels of depression between participants with typical and atypical BDNF
      genotype
    section: Discussion
    supports: limitation
  statistics:
    ci_95: not_reported
    cluster_extent: null
    effect_size: F = 4.97 (tDCS × BDNF genotype interaction in mixed effects repeated measures model)
    p_value: '0.03'
    threshold: p = 0.03
  strength: moderate
  target: bdnf_genotype
  target_kind: predictor
source: curated
last_reviewed: 2026-05-06
notes: 'Behavioral-only therapy finding (no imaging analysis). This draft captures the

  RCT interaction effect: val/val BDNF × A-tDCS → greater naming improvement.

  The tDCS stimulation site (left temporo-parietal junction, coregistered to each

  participant''s peak naming-related fMRI activation) is described in the Methods

  but the finding is coded as behavioral-only because the efficacy claim does not

  depend on a region-specific analysis.

  The BDNF-genotype predictor finding is separately captured in

  drafts/predictors/bdnf_val66met__Fridriksson2018BDNF.md.

  '
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
