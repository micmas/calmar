---
schema_version: 2.3
id: left_posterior_stg
name: "Left Posterior Superior Temporal Gyrus (BA 22 / Wernicke's area)"
kind: classical
status: draft
created_by: "agent:claude-sonnet-4-6"
created_on: 2026-05-06
hemisphere: left
aliases:
  - "BA 22"
  - "left posterior STG"
  - "Wernicke's area"

notes: |
  Bonilha 2014 disconnectome finding for BA 22 — split out from
  drafts/regions/left_ifg_pars_triangularis__Bonilha2014.md (where it
  originally lived as f3) because anatomically it belongs in the
  posterior STG (BA 22 / Wernicke's area) draft, not the pars
  triangularis (BA 45) draft. Cohort (n=39) is the same as the
  pars-triangularis Bonilha 2014 draft. May overlap with
  @Fridriksson2018Anatomy and other USC/MUSC lab papers.

findings:
  - id: f1
    target: auditory_comprehension
    target_kind: impairment
    claim: "Structural disconnection of left BA 22 (posterior superior temporal gyrus / Wernicke's area) is independently associated with impaired auditory comprehension of sequential commands; BA 22 cortical necrosis alone is not an independent predictor of comprehension."
    direction: likely
    relationship: causal
    citation: "@Bonilha2014"

    method: disconnectome
    design: cross-sectional
    imaging: multimodal

    sample:
      n: 39
      population: "chronic left-hemisphere ischemic stroke survivors with aphasia"
      time_post_onset: ">=6 months"
      age_range: "mean 62.7 years (SD 12.8)"
      handedness: "all right-handed"
      language: not_reported
      recruitment: "MUSC and USC local community."

    statistics:
      threshold: "p<0.05 Bonferroni-corrected"
      cluster_extent: not_reported
      effect_size: "necrosis: beta=-0.35, p=0.43 (not independently significant); disconnection: beta=0.47 [see flag], p=0.01"
      ci_95: not_reported
      p_value: "F=3.05, p=0.047 (overall model)"

    confounders_controlled:
      - "BA 22 cortical necrosis (entered simultaneously)"
      - "Bonferroni correction"
    confounders_not_controlled:
      - "overall lesion volume"
      - "age"
      - "time post-onset"

    region_definition:
      kind: atlas
      atlas: "Brodmann area atlas (probabilistic grey matter segmentation)"
      description: "BA 22 (posterior superior temporal gyrus / Wernicke's area) defined via probabilistic Brodmann parcellation; connectivity as normalized DTI streamlines."

    imaging_details:
      field_strength: "3T"
      acquisition:
        sequence: "T1-weighted MPRAGE + DTI deterministic tractography"
        voxel_size_mm: not_reported
        TR_ms: not_reported
        TE_ms: not_reported
      preprocessing_pipeline: "SPM-based Brodmann parcellation; deterministic tractography connectome; necrotic tissue excluded"
      reference_space: not_reported
      atlases_used:
        - "Brodmann area atlas (probabilistic)"
      coordinates_reported: []

    replications: []
    contradictions: []

    author_limitations:
      - "BA 22 necrosis was NOT independently associated with comprehension (p=0.43) — only disconnection reached significance."
      - "Small sample (n=39)."

    evidence_quality: cohort
    strength: moderate

    provenance:
      extracted_by: "agent:claude-sonnet-4-6"
      extracted_on: 2026-05-06
      paper_section: "Results – Regional necrosis and connectivity and language impairment"
      confidence: medium
      flags:
        - "disconnection beta reported as 'beta=47' in the author manuscript (likely OCR/formatting artifact — probable value is beta=0.47); verify against published Stroke journal PDF"
        - "necrosis NOT independently associated with comprehension (p=0.43); only disconnection significant (p=0.01)"
        - "cohort overlaps with @Fridriksson2018Anatomy and @Bonilha2014 (left_ifg_pars_triangularis draft) — flag for double-counting risk"
        - "split out from drafts/regions/left_ifg_pars_triangularis__Bonilha2014.md (originally f3) on 2026-05-06 because the finding is anatomically about BA22, not BA45"

    source_passages:
      - section: "Results – Regional necrosis and connectivity and language impairment"
        page: 5
        supports: claim
        quote: "We also observed a significant relationship between comprehension and a model composed by BA 22 necrosis and BA 22 disconnection (F=3.05, p=0.047; necrosis: beta=-0.35; p=0.43; disconnection beta=47; p=0.01). However, in this model, necrosis was not independently associated with comprehension."
      - section: "Methods – Subjects"
        page: 2
        supports: sample
        quote: "We studied thirty-nine individuals (mean age 62.7 +/-12.8 years, 22 male, 16 female) who suffered a left hemisphere ischemic stroke at least six months prior to enrolling in this study"
      - section: "Methods – Statistical Analyses"
        page: 4
        supports: method
        quote: "We performed multiple linear regression analyses with the performance on naming measures defined as the dependent variable, with the following independent variables: 1) percentage of damage to each BA area, 2) percentage number of fibers of each BA area."
      - section: "Methods – MRI acquisition"
        page: 3
        supports: imaging_details
        quote: "MRI scanning was performed using the same type of MRI scanner, i.e., a 3T Siemens Trio equipped with a 12-channel head coil."
      - section: "Discussion"
        page: 7
        supports: limitation
        quote: "cortical disconnection is an independent form of damage, which may not be readily appreciated by measurement of cortical necrosis"
---

# Left Posterior STG (BA 22 / Wernicke's area) — Bonilha 2014 (Disconnectome)

Bonilha et al. 2014 demonstrates that structural disconnection of BA 22 predicts auditory
comprehension performance beyond what is explained by cortical necrosis alone in 39 chronic
aphasia patients. The disconnection signal reaches significance (p=0.01) while necrosis does not
(p=0.43) in the same simultaneous model — making BA 22 disconnection a *novel* class of damage
not captured by traditional lesion-volume mapping.

This finding was originally extracted as f3 of the left_ifg_pars_triangularis Bonilha 2014 draft
on 2026-05-06 and split out into its own region-anchored draft on the same date so that the
canonical entry sits in the posterior STG file rather than the pars triangularis file.
