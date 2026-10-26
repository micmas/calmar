---
schema_version: 2.7
id: left_uncinate_fasciculus
name: Left Uncinate Fasciculus
kind: tract
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
hemisphere: left
findings:
- id: f1
  target: fluency
  target_kind: impairment
  claim: Damage to the left uncinate fasciculus is associated with deficits in both semantic and phonological
    verbal fluency.
  direction: likely
  relationship: causal
  citation: '@Li2017'
  method:
  - LSM
  - DTI
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 51
    population: right-handed stroke patients
    time_post_onset: at least 1-month post-onset
    phase: chronic
    age_range: mean 46.8 years
    handedness: all right-handed
    language: native Chinese speakers
    cohort: not_reported
  statistics:
    threshold: Bonferroni corrected (p < 0.0026 for lesion; p < 0.0023 for FA)
    effect_size: lesion r=-0.41 to -0.52; FA r=0.50 to 0.71
  confounders_controlled:
  - total lesion volume
  - type of aphasia
  - duration of illness
  - nonverbal control tasks
  confounders_not_controlled: []
  region_definition:
    kind: atlas
    atlas: JHU white-matter tractography atlas
    description: Left uncinate fasciculus (UF)
  imaging_details:
    field_strength: 1.5T
    modalities:
    - modality: T1
      sequence: MPRAGE
      voxel_size_mm:
      - 0.49
      - 0.49
      - 0.7
    - modality: DWI
      voxel_size_mm:
      - 1.95
      - 1.95
      - 2.6
      b_values:
      - 1000
    preprocessing_pipeline: Manual registration to Talairach space via BrainVoyager QX v2.0, then to MNI
      space
    reference_space: MNI152
    atlases_used:
    - JHU white-matter tractography atlas
  author_limitations:
  - Uneven distribution of patients across different tracts.
  - Results based on a Chinese population.
  - High proportion of aphasic patients in the sample.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, pages 5-6
    confidence: high
    flags: []
  source_passages:
  - section: Abstract
    page: 1
    quote: We found five left-lateralized tracts including the [...] uncinate fasciculus (UF) [...] were
      significantly correlated with the scores of both semantic and phonological fluencies.
    supports: claim
  - section: Results
    page: 5
    quote: 'Performance on each of the three cues in semantic fluency task was significantly correlated
      with the lesion percentages of four tracts: [...] left UF (r=-0.52 to -0.41, corrected p-values
      < 0.05) [and phonological fluency].'
    supports: statistics
  - section: added by backfill
    page: 4
    quote: the lesion percentage (number of voxels with lesion divided by total number of voxels on the
      tract) was correlated with the corrected t scores of each cue of semantic (and phonological) fluency
      tasks across 51 patients.
    supports: method
  - section: added by backfill
    page: 4
    quote: The results for each cue were adjusted for the 19 tracts with the Bonferroni correction method
      (p < 0.0026, corrected p < 0.05).
    supports: method
  - section: added by backfill
    page: 6
    quote: When the values were treated as covariate, the lesion percentages of the above ﬁve tracts were
      signiﬁcantly correlated with semantic or phonological ﬂuency composite scores
    supports: method
  lesion_mapping:
    analysis: univariate
    n_analysed: 51
    min_lesion_overlap: not_reported
    lesion_volume_correction: not_reported
    multiple_comparisons: bonferroni
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
    - lesion_mapping
---
