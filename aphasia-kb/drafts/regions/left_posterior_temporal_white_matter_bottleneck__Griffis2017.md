---
schema_version: 2.7
id: left_posterior_temporal_white_matter_bottleneck
name: Left Posterior Temporal White Matter Bottleneck
kind: network
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-22
hemisphere: left
members:
- left_arcuate_fasciculus
- left_inferior_longitudinal_fasciculus
- left_inferior_fronto_occipital_fasciculus
notes: This region is defined as the intersection of the SLF/AF, ILF, and IFOF.
findings:
- id: f1
  target: fluency
  target_kind: impairment
  claim: Damage to the left posterior temporal white matter bottleneck predicts deficits in verbal fluency
    in chronic stroke patients.
  direction: likely
  relationship: causal
  citation: '@Griffis2017'
  method: LSM
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 43
    population: chronic left hemispheric stroke
    time_post_onset: at least 1 year
    phase: chronic
    age_range: mean 53 (SD = 15; range = 23-90)
    handedness: mean 0.85 (SD = 0.43)
    language: English
    cohort: not_reported
  statistics:
    threshold: Bonferroni-Holm correction to control the FWE at 0.05
    effect_size: not_reported
  confounders_controlled:
  - lesion volume
  - tract lesion loads
  - cortical lesion loads
  confounders_not_controlled: []
  region_definition:
    kind: data_driven_cluster
    description: Intersection of left ILF, IFOF, and SLF/AF probabilistic atlas labels thresholded at
      20%.
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: SPM12 unified normalization procedure
    reference_space: MNI152
    atlases_used:
    - ICBM-DTI atlas
  author_limitations:
  - The bottleneck ROIs were defined using thresholded tract probability maps, and results might differ
    depending on threshold choice.
  - Only chronic patients were included, preventing conclusions about recovery vs. chronic severity.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 6
    confidence: high
    flags: []
  source_passages:
  - section: Abstract
    page: 1
    quote: Damage to the posterior temporal bottleneck predicted deficits on all tasks...
    supports: claim
  - section: Methods - Participants
    page: 2
    quote: Data were collected from 43 patients with chronic left hemispheric stroke... which occurred
      at least 1 year prior to data collection.
    supports: sample
  - section: Methods - White matter bottleneck ROIs
    page: 3
    quote: 'Next, we defined a posterior bottleneck ROI according to the same procedure, but using labels
      for three of the language-relevant tracts previously identified in the posterior temporal WM: the
      left ILF, IFOF, and SLF/AF...'
    supports: region_definition
  - section: Methods - Multiple regression analyses
    page: 5
    quote: Parameter estimates for the variables in each of these models were considered significant if
      the p-value of the test statistic survived Bonferroni-Holm correction to control the FWE at 0.05
      across all 4 variables in each model.
    supports: statistics
  - section: Discussion - Limitations and conclusions
    page: 12
    quote: A limitation of the current study is that the bottleneck ROIs were defined using thresholded
      tract probability maps.
    supports: limitation
  - section: added by backfill
    page: 2
    quote: Data were collected from 43 patients with chronic left hemispheric stroke participating in
      different studies by our laboratory.
    supports: method
  - section: added by backfill
    page: 5
    quote: Thus, we ﬁt a 4-predictor model to each task that included (1) lesion status for the posterior
      bottleneck, (2) lesion status for the anterior bottleneck, (3) the interaction of the lesion status
      terms (i.e. to account for the possibility that the effect of damage to both regions was not additive),
      and (4) total lesion volume as predictors.
    supports: method
  - section: added by backfill
    page: 5
    quote: These models were considered signiﬁcant if the p-value for the F-test against the intercept-only
      model survived Bonferroni-Holm correction to control the FWE at 0.05 across all three (i.e. one
      for each task) models (Aickin and Gensler, 1996).
    supports: method
  lesion_mapping:
    analysis: region_based
    n_analysed: 43
    min_lesion_overlap: not_reported
    lesion_volume_correction: covariate
    multiple_comparisons: bonferroni
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
    - lesion_mapping
- id: f2
  target: semantics
  target_kind: impairment
  claim: Damage to the left posterior temporal white matter bottleneck predicts deficits in picture naming
    and auditory semantic processing in chronic stroke patients.
  direction: likely
  relationship: causal
  citation: '@Griffis2017'
  method: LSM
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 43
    population: chronic left hemispheric stroke
    time_post_onset: at least 1 year
    phase: chronic
    age_range: mean 53 (SD = 15; range = 23-90)
    handedness: mean 0.85 (SD = 0.43)
    language: English
    cohort: not_reported
  statistics:
    threshold: Bonferroni-Holm correction to control the FWE at 0.05
    effect_size: not_reported
  confounders_controlled:
  - lesion volume
  - tract lesion loads
  - cortical lesion loads
  confounders_not_controlled: []
  region_definition:
    kind: data_driven_cluster
    description: Intersection of left ILF, IFOF, and SLF/AF probabilistic atlas labels thresholded at
      20%.
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: SPM12 unified normalization procedure
    reference_space: MNI152
    atlases_used:
    - ICBM-DTI atlas
  author_limitations:
  - The bottleneck ROIs were defined using thresholded tract probability maps, and results might differ
    depending on threshold choice.
  - Only chronic patients were included, preventing conclusions about recovery vs. chronic severity.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 8
    confidence: high
    flags: []
  source_passages:
  - section: Abstract
    page: 1
    quote: Damage to the posterior temporal bottleneck predicted deficits on all tasks...
    supports: claim
  - section: Methods - Participants
    page: 2
    quote: Data were collected from 43 patients with chronic left hemispheric stroke... which occurred
      at least 1 year prior to data collection.
    supports: sample
  - section: Methods - White matter bottleneck ROIs
    page: 3
    quote: 'Next, we defined a posterior bottleneck ROI according to the same procedure, but using labels
      for three of the language-relevant tracts previously identified in the posterior temporal WM: the
      left ILF, IFOF, and SLF/AF...'
    supports: region_definition
  - section: Methods - Multiple regression analyses
    page: 5
    quote: Parameter estimates for the variables in each of these models were considered significant if
      the p-value of the test statistic survived Bonferroni-Holm correction to control the FWE at 0.05
      across all 4 variables in each model.
    supports: statistics
  - section: Discussion - Limitations and conclusions
    page: 12
    quote: A limitation of the current study is that the bottleneck ROIs were defined using thresholded
      tract probability maps.
    supports: limitation
  - section: added by backfill
    page: 2
    quote: Data were collected from 43 patients with chronic left hemispheric stroke participating in
      different studies by our laboratory.
    supports: method
  - section: added by backfill
    page: 5
    quote: Thus, we ﬁt a 4-predictor model to each task that included (1) lesion status for the posterior
      bottleneck, (2) lesion status for the anterior bottleneck, (3) the interaction of the lesion status
      terms (i.e. to account for the possibility that the effect of damage to both regions was not additive),
      and (4) total lesion volume as predictors.
    supports: method
  - section: added by backfill
    page: 5
    quote: These models were considered signiﬁcant if the p-value for the F-test against the intercept-only
      model survived Bonferroni-Holm correction to control the FWE at 0.05 across all three (i.e. one
      for each task) models (Aickin and Gensler, 1996).
    supports: method
  lesion_mapping:
    analysis: region_based
    n_analysed: 43
    min_lesion_overlap: not_reported
    lesion_volume_correction: covariate
    multiple_comparisons: bonferroni
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
    - lesion_mapping
---
