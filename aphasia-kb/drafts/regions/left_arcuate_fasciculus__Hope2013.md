---
schema_version: 2.3
id: left_arcuate_fasciculus
name: Left Arcuate Fasciculus
kind: tract
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
hemisphere: left
findings:
- id: f1
  target: fluency
  target_kind: impairment
  claim: Damage to the superior longitudinal fasciculus is a significant predictor of speech production
    impairment.
  direction: likely
  relationship: causal
  citation: '@Hope2013'
  method: MLPA
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 270
    population: stroke patients
    time_post_onset: less than a month to more than 30 years
    age_range: 20 to 90 years
    handedness: 242 right handed
    language: English
    phase: chronic
  statistics:
    threshold: p < 0.001
    effect_size: R2 = 0.59 (model total)
  confounders_controlled:
  - lesion volume
  - time post-stroke
  confounders_not_controlled: []
  region_definition:
    kind: atlas
    atlas: ICBM-DTI-81 / JHU
    description: Superior longitudinal fasciculus
  imaging_details:
    reference_space: MNI152
    preprocessing_pipeline: unified segmentation algorithm optimized for patients with focal brain lesions
    atlases_used:
    - Anatomy Toolbox
    - ICBM-DTI-81
    - JHU white-matter tractography atlas
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Table 1
    confidence: high
    flags:
    - target fluency used as proxy for composite speech production score
  source_passages:
  - section: Table 1
    page: 6
    quote: Superior longitudinal fasciculus
    supports: claim
  - section: Method
    page: 3
    quote: The images were spatially normalised into standard Montreal Neurological Institute (MNI) space
      using a uniﬁed segmentation algorithm
    supports: imaging_details
  - section: Discussion
    page: 8
    quote: our preferred predictor configuration systematically under-estimates the severity of the impairments
      suffered by the most impaired patients
    supports: limitation
  author_limitations:
  - The model systematically underestimates severity for the most impaired patients.
---
