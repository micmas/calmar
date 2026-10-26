---
schema_version: 2.7
id: bilateral_middle_frontal_gyrus_recovery
name: Bilateral Middle Frontal Gyrus and Right Temporo-Occipital MTG — Fluency Recovery
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
hemisphere: left
findings:
- id: f1
  target: anomic_aphasia
  target_kind: impairment
  claim: Increased activation in the left middle frontal gyrus following treatment is associated with
    improved naming performance.
  direction: likely
  relationship: treatment_response
  citation: '@Fridriksson2010Anomia'
  method: fMRI_activation
  design: longitudinal
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 19
    population: chronic stroke and concomitant aphasia
    time_post_onset: '>= 8 months'
    age_range: mean 59.7 (SD 12.3)
    handedness: not_reported
    language: not_reported
    phase: chronic
    cohort: not_reported
  statistics:
    threshold: Z = 2.3, p < 0.05 (corrected)
    effect_size: Z = 2.96
    p_value: not_reported
  confounders_controlled: []
  confounders_not_controlled: []
  region_definition:
    kind: data_driven_cluster
    description: Part of the anterior cluster associated with naming improvement, specifically the middle
      frontal gyrus (BA 36).
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: fMRI
      sequence: T2*-MRI echoplanar imaging
      voxel_size_mm:
      - 3.25
      - 3.25
      - 3.25
      TR_ms: 10000
      TE_ms: 30
      volumes: 120
    task:
      name: Picture naming
      description: Overt naming of 80 pictures randomly selected from treatment sets, contrasted with
        40 abstract pictures.
      contrasts:
      - correctly named pictures versus viewed abstract pictures
      baseline: abstract pictures
    preprocessing_pipeline: 'FSL 4.1: motion correction, non-brain removal, 8mm Gaussian smoothing, grand-mean
      intensity normalization, high-pass temporal filtering (80s)'
    reference_space: MNI152
    atlases_used:
    - Talairach Daemon
    - Brodmann's area map
    coordinates_reported:
    - region: Middle frontal gyrus
      mni:
      - 20
      - 28
      - 36
  author_limitations:
  - the current fMRI analysis did not deduce which of these areas is more important than others or the
    dynamics of change needed to support recovery.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: 'Results - Primary outcome: fMRI results'
    confidence: high
    flags:
    - cohort overlaps with @Fridriksson2010 (as stated in paper)
  source_passages:
  - section: Results
    page: 4
    quote: A positive relationship was revealed between treatment-assisted increase in correct naming
      and modulation of cortical areas in the left posterior and anterior hemisphere
    supports: claim
  - section: Materials and Methods
    page: 2
    quote: Twenty-six patients (14 women) with chronic stroke and concomitant aphasia were included.
    supports: sample
  - section: Materials and Methods
    page: 3
    quote: The third and final level included a regression analysis in which data from all participants
      were combined to predict treatment outcome (i.e., change in correct naming).
    supports: method
  - section: Materials and Methods
    page: 3
    quote: Z (Gaussianised T/F) statistic images were thresholded using clusters determined by Z = 2.3
      and a (corrected) cluster significance threshold of p = 0.05
    supports: statistics
  - section: Discussion
    page: 5
    quote: the current fMRI analysis did not deduce which of these areas is more important than others
      or the dynamics of change needed to support recovery.
    supports: limitation
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
---
Finding f1 links increased activation in the left middle frontal gyrus to improved naming outcomes following intensive treatment.
