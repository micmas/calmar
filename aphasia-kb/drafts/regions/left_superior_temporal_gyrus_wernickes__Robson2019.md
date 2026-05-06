---
schema_version: 2.3
id: left_superior_temporal_gyrus_wernickes
name: "Left Superior Temporal Gyrus (Wernicke's region, mid-posterior)"
kind: classical
status: draft
created_by: "agent:claude-sonnet-4-6"
created_on: 2026-05-06
hemisphere: left
aliases:
  - "left mid-posterior STG"
  - "left posterior superior temporal gyrus"
  - "Wernicke's area (posterior STG)"
networks: [ventral_language]
tracts_adjacent: [arcuate_fasciculus]

findings:
  - id: f1
    target: auditory_comprehension
    target_kind: impairment
    claim: "Lesions to the left mid-posterior superior temporal gyrus (and adjacent STS and white matter) are associated with the comprehension deficits characterizing Wernicke's aphasia, with maximal lesion overlap in this region across a group of 12 WA patients."
    direction: likely
    relationship: causal
    citation: "@Robson2019"

    method: LSM
    design: longitudinal
    imaging: not_reported  # research-MRI MPRAGE for some patients; clinical CT/MRI for others — no single modality describes the cohort

    sample:
      n: 12
      population: "adults with Wernicke's aphasia recruited from NHS in-patient services in the south of England, 0–2 months post-onset"
      time_post_onset: "recruited subacute (0–2 MPO); assessments at 2.5, 5, 9 MPO"
      age_range: "46–93 years (see Table 1)"
      handedness: "right-handed (all except participant 2)"
      language: "monolingual English speakers"
      recruitment: "Referred by NHS practitioners or speech-language therapists if presenting with any error on single-word language comprehension and repetition screening assessments."
      inclusion_criteria: "Classical WA (fluent speech, impaired comprehension, impaired repetition) or disproportionately impaired spoken vs written comprehension; BDAE Short Form errors."
      exclusion_criteria: "Significant history of previous neurological disorder including previous stroke (TIAs excepted)."

    statistics:
      threshold: "not_reported (lesion overlap map only; no voxel-wise statistical threshold)"
      cluster_extent: null
      effect_size: "not_reported"
      ci_95: "not_reported"
      p_value: "not_reported"

    confounders_controlled: []
    confounders_not_controlled:
      - "lesion volume (correlated with comprehension at group level but not statistically with outcome at 9 MPO: r not significant)"
      - "age (correlated with RCPM but not comprehension outcome)"
      - "hearing (measured but not significantly correlated with outcome)"
      - "therapy received (monitored; amount not correlated with outcome)"

    region_definition:
      kind: data_driven_cluster
      description: "Manual lesion tracing in native space (MRIcron); SPM Clinical Toolbox normalization to CT/MRI template. Lesion overlap map showed maximal overlap in mid-posterior STG, high overlap in STS and MTG (temporoparietal junction), and anterior STS involvement in half the group."

    imaging_details:
      field_strength: "3T (for participants with research MRI; clinical CT/MRI used for others)"
      acquisition:
        voxel_size_mm: [1, 1, 1]
        TR_ms: 2020
        TE_ms: 302
        sequence: "MPRAGE (2 averages, 192 slices, 250 mm FOV, Inversion Time 900 ms)"
      preprocessing_pipeline: "Manual lesion tracing in MRIcron (native space); SPM Clinical Toolbox for normalization to CT or MRI template with cost-function masking; normalization parameters applied to native-space lesion image; binary lesion images compared with normalized scans."
      reference_space: "MNI152"
      atlases_used: []
      coordinates_reported: []

    replications: []
    contradictions: []

    author_limitations:
      - "Small sample (n=12); a priori power calculation was based on chronic WA data and may not be fully applicable to the longitudinal subacute-to-chronic design."
      - "Three participants' CT scans showed no clear lesion evidence and were excluded from imaging analysis."
      - "Therapy involvement was not an exclusion criterion and varied widely; could account for some variance in recovery, though amount of therapy was not correlated with outcome."
      - "Potential for neural atrophy or small-vessel disease (especially in older participants) was not controlled."

    evidence_quality: cohort
    strength: weak

    provenance:
      extracted_by: "agent:claude-sonnet-4-6"
      extracted_on: 2026-05-06
      paper_section: "Methods – Participant Neuroimaging; Introduction; Fig. 1 (lesion overlap map)"
      confidence: medium
      flags:
        - "No voxel-wise statistical lesion-symptom mapping performed; lesion overlap is a descriptive map only. Finding is inferential from region description, not from formal LSM analysis. method=LSM is the closest controlled-vocab fit (LSM is broader than VLSM and includes overlap-map approaches); reference_space=MNI152 because lesions were normalised before being overlapped."
        - "Lesion volumes reported in Table 1 as voxels, not mm³; cannot compute absolute volumes without voxel size information for clinical imaging participants."
        - "TE_ms=302 verbatim from the published Methods section is implausibly large for an MPRAGE at 3T (typical ≈3 ms); the value is almost certainly a paper typo for 3.02 ms or 2.30 ms — kept verbatim per source-passage policy but flagged as a paper-side error."

    source_passages:
      - section: "Introduction"
        page: 800
        supports: claim
        quote: "WA results from lesions to the left temporoparietal region, which supports a range of functions related to language comprehension"
      - section: "Methods – Participant Neuroimaging"
        page: 801
        supports: region_definition
        quote: "the group displayed a relatively homogeneous lesion distribution, with high overlap in the white matter of the left superior temporal lobe. There was maximal overlap in the midposterior STG, high overlap in temporoparietal junction regions (STS, MTG)"
      - section: "Methods – Participants"
        page: 801
        supports: sample
        quote: "Twelve individuals were recruited to the subacute group; 10 displayed classical WA at the point of recruitment"
      - section: "Methods – Participant Neuroimaging"
        page: 801
        supports: imaging_details
        quote: "Data were collected on a GE x750 3.0-T MRI Scanner with a 12-channel head coil. An MPRAGE sequence with 2 averages: 192 slices, 1 mm3 resolution, 250 mm FOV, TR 2020 ms, TE 302 ms, Inversion Time 900 ms."
      - section: "Methods – Participant Neuroimaging"
        page: 801
        supports: imaging_details
        quote: "The SPM Clinical Toolbox was used for scan and lesion normalization. Scans were normalized to a CT or MRI template using cost-function masking"
      - section: "Discussion – Limitations"
        page: 810
        supports: limitation
        quote: "The current study recruited 12 participants with WA. This sample size reflected an a priori power calculation; however, this calculation was conducted on chronic WA data, and the sample remains small."

  - id: f2
    target: auditory_comprehension
    target_kind: impairment
    claim: "Language comprehension in Wernicke's aphasia shows strong and consistent recovery from 2.5 to 9 months post-onset, with significant improvement between each successive time point, but residual comprehension impairments remain in all participants at 9 MPO."
    direction: likely
    relationship: correlational
    citation: "@Robson2019"

    method: behavioral_only
    design: longitudinal
    imaging: none

    sample:
      n: 12
      population: "adults with Wernicke's aphasia, subacute to chronic stage, south of England NHS services"
      time_post_onset: "assessments at 2.5, 5, and 9 months post-onset"
      age_range: "46–93 years"
      handedness: "right-handed (all except participant 2)"
      language: "monolingual English speakers"
      recruitment: "NHS referral from south of England in-patient services."
      inclusion_criteria: "WA diagnosis criteria; monolingual English."
      exclusion_criteria: "Previous neurological disorder."

    statistics:
      threshold: "p < .001"
      cluster_extent: null
      effect_size: "BDAE: F(2, 20) = 22.2, P < .001, η = 0.69; sWPM: F(2, 20) = 34.5, P < .001, η = 0.78"
      ci_95: "not_reported"
      p_value: "< .001"

    confounders_controlled: []
    confounders_not_controlled:
      - "therapy type and amount"
      - "age"
      - "hearing thresholds"

    region_definition:
      kind: not_reported
      description: "Longitudinal behavioral finding — no region-specific analysis. Outcome measured by BDAE auditory comprehension subtests and spoken-word picture matching (sWPM)."

    replications: []
    contradictions: []

    author_limitations:
      - "Small sample (n=12); further associations may have been revealed with a larger sample."
      - "Therapy involvement not controlled and could account for some variance."

    evidence_quality: cohort
    strength: weak

    provenance:
      extracted_by: "agent:claude-sonnet-4-6"
      extracted_on: 2026-05-06
      paper_section: "Results – Recovery"
      confidence: high
      flags: []

    source_passages:
      - section: "Results – Recovery"
        page: 804
        supports: claim
        quote: "A significant improvement in comprehension over time was found (BDAE: F(2, 20) = 22.2, P < .001, η = 0.69; sWPM: F(2, 20) = 34.5, P < .001, η = 0.78"
      - section: "Results – Recovery"
        page: 804
        supports: statistics
        quote: "Post hoc paired t-tests showed that significant improvements were made between 2.5 and 5 MPO and 5 and 9 MPO for both assessments (BDAE t(11) > 3.2 and sWPM t(11) > 5.2 for all pairwise comparisons)."
      - section: "Conclusions"
        page: 810
        supports: limitation
        quote: "Although all individuals in this study had residual comprehension impairments at 9 MPO, improvements in language comprehension occurred for all but 1 participant."

source: curated
last_reviewed: 2026-05-06
notes: |
  This draft captures two findings from Robson 2019 anchored to the left mid-posterior
  STG region (Wernicke's area):

  f1: Descriptive lesion overlap — maximal lesion overlap in left mid-posterior STG
      and STS across 12 WA patients. Not a formal LSM analysis (no voxel-wise statistics).
      Relationship: causal (lesion → comprehension impairment in WA), strength: weak
      (no formal statistical LSM).

  f2: Longitudinal comprehension recovery — significant improvement from 2.5 to 9 MPO.
      This is a behavioral finding coded as correlational (trajectory tracking), not
      region-specific.

  The key prognostic finding (rapid auditory temporal processing at 2.5 MPO predicts
  comprehension at 9 MPO) is captured separately in
  drafts/predictors/auditory_temporal_processing__Robson2019.md, as it is a
  predictor-anchored finding, not a region-anchored one.

  The entry id is left_superior_temporal_gyrus_wernickes — this forward-looking ID
  overlaps with the existing draft left_superior_temporal_gyrus_wernicke__Mirman2015.md
  (note: Mirman draft uses singular 'wernicke'); promote.py should check for this
  potential ID collision and consolidate if appropriate.
---

# Left Superior Temporal Gyrus (Wernicke's region, mid-posterior)

## Robson 2019 — Wernicke's aphasia lesion distribution and longitudinal comprehension recovery

This draft captures findings from a prospective longitudinal study of 12 WA patients.
The lesion overlap mapping confirms the classical WA lesion site (left mid-posterior
STG and STS), while the longitudinal behavioral data document the pattern of
comprehension recovery from subacute (2.5 MPO) to near-chronic (9 MPO) stages.
