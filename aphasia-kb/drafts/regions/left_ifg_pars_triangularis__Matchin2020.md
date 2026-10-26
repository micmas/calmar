---
schema_version: 2.7
id: left_ifg_pars_triangularis
name: Left IFG Pars Triangularis (BA 45)
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
hemisphere: left
findings:
- id: f1
  target: syntactic_processing
  target_kind: impairment
  claim: Damage to the left inferior frontal gyrus pars triangularis is significantly associated with
    agrammatism, independent of speech rate.
  direction: likely
  relationship: causal
  citation: '@Matchin2020'
  method: LSM
  design: cross-sectional
  strength: strong
  evidence_quality: cohort
  sample:
    n: 53
    population: chronic left-hemisphere stroke aphasia
    time_post_onset: '>= 6 months'
    age_range: mean 59.2 (SD 11.15)
    handedness: all right-handed
    language: English
    phase: chronic
    cohort: not_reported
  statistics:
    threshold: uncorrected voxel-wise p < 0.05
    effect_size: t(51) = 3.133 (LV covariate), t(51) = 2.458 (LV + WPM covariates)
    p_value: '0.001'
  confounders_controlled:
  - lesion volume
  - speech rate (words per minute)
  confounders_not_controlled: []
  region_definition:
    kind: atlas
    atlas: Johns Hopkins University atlas (Faria et al., 2012)
    description: Broca's area ROI combining left IFGtri and pars opercularis.
  imaging_details:
    field_strength: not_reported
    preprocessing_pipeline: warped to standard space
    reference_space: MNI152
    atlases_used:
    - Johns Hopkins University atlas
    coordinates_reported:
    - region: Inferior frontal gyrus (pars triangularis)
      mni:
      - -53
      - 22
      - 26
  author_limitations:
  - Omitting subjects with low speech output likely precludes analysis of patients with both severe agrammatic
    and nonfluent speech.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 216
    confidence: high
    flags:
    - cohort overlaps with @Fridriksson2018 (USC/MUSC Aphasia Lab)
  source_passages:
  - section: Results
    page: 9
    quote: 'AGRAMMATISM was significantly associated with damage to Broca''s area, t(51) = 3.133, p =
      0.001... These results also held when adding speech rate as a covariate: AGRAMMATISM was significantly
      associated with damage to Broca''s area, t(51) = 2.458, p = 0.009'
    supports: claim
  - section: Procedure
    page: 3
    quote: All subjects had a single ischemic stroke to the left hemisphere at least six months prior
      to study inclusion and were also premorbidly right-handed
    supports: sample
  - section: ROI Analyses
    page: 215
    quote: The Broca's area ROI was created by combining the left IFGtri, and pars opercularis.
    supports: region_definition
  - section: Discussion
    page: 15
    quote: Omitting subjects with low speech output also likely precludes analysis of patients with both
      severe agrammatic and nonfluent speech.
    supports: limitation
  - section: added by backfill
    page: 4
    quote: Of the 53 successfully classified subjects, 21 were assigned to the PARAGRAMMATIC group, 11
      to the AGRAMMATIC group, and 17 to the NGD group.
    supports: method
  - section: added by backfill
    page: 4
    quote: all of our lesion-symptom mapping analyses included lesion volume as a covariate.
    supports: method
  - section: added by backfill
    page: not_reported
    quote: Only voxels that were damaged in at least 5 subjects (~10% of sample) were included in the
      analyses.
    supports: method
  lesion_mapping:
    analysis: univariate
    n_analysed: 53
    min_lesion_overlap: '>= 5 patients'
    lesion_volume_correction: covariate
    multiple_comparisons: not_reported
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
    - lesion_mapping
---
