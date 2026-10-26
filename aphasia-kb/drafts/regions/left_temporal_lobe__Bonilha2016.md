---
schema_version: 2.7
id: left_temporal_lobe
name: Left Temporal Lobe
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-22
hemisphere: left
findings:
- id: f1
  target: anomic_aphasia
  target_kind: therapy
  claim: Preservation of the structural network influence (betweenness centrality) of the left temporal
    lobe is associated with greater improvement in naming after speech therapy.
  direction: likely
  relationship: responder
  citation: '@Bonilha2016'
  method: DTI
  design: cross-sectional
  strength: strong
  evidence_quality: cohort
  sample:
    n: 24
    population: chronic left-hemisphere ischemic stroke
    time_post_onset: at least 6 months
    phase: chronic
    age_range: mean 60.2 (SD 11.9)
    handedness: all right-handed
    language: not_reported
    cohort: not_reported
  statistics:
    threshold: P < .008
    effect_size: model R2 = .74
    p_value: '.00077'
  confounders_controlled:
  - age
  - time since the stroke
  - stroke lesion size
  - WAB-AQ
  confounders_not_controlled: []
  region_definition:
    kind: atlas
    atlas: Brodmann
    description: Left temporal ROIs (BA = [20, 21, 22, 37, 38])
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: T1
      sequence: 3D MP-RAGE
      voxel_size_mm: not_reported
      TR_ms: 2250
      TE_ms: 4.15
    - modality: DTI
      sequence: Diffusion EPI
      voxel_size_mm:
      - 2.7
      - 2.7
      - 2.7
      n_directions: 30
      b_values:
      - 1000
      - 2000
      TR_ms: 6100
      TE_ms: 101
    preprocessing_pipeline: Probabilistic gray/white matter segmentation, registration to DTI space, probabilistic
      fiber tracking, and correction for ROI volume and distance.
    reference_space: native
    atlases_used:
    - Brodmann
  author_limitations:
  - The ROIs of this atlas are large, usually encompassing different brain regions that serve distinct
    functions.
  - Evaluation occurred within a week after a 2-week intense intervention; longitudinal follow-up is needed.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 271
    confidence: high
    flags:
    - cohort overlaps with @Fridriksson2010 (n=20 subgroup); flag for downstream double-counting risk
      in interpret_overlap()
  source_passages:
  - section: Results
    page: 271
    quote: We observed a robust relationship between treatment-related improvement in naming and a higher
      left temporal BC (controlling for age, time since the stroke, stroke lesion size, and WAB-AQ) (model
      F = 6.79, P = .00077, model R = .86, model R2 = .74; Figure 5, Supplemental Table 2).
    supports: claim
  - section: Subjects
    page: 268
    quote: We studied 24 individuals recruited from the local community with chronic aphasia as a result
      of a left hemisphere ischemic stroke that occurred at least 6 months prior to enrolling in this
      study.
    supports: sample
  - section: Involvement of Temporal and Frontal Nodes in the Global Network
    page: 270
    quote: left temporal ROIs (BA = [20, 21, 22, 37, 38]).
    supports: region_definition
  - section: Baseline MRI Scanning
    page: 268
    quote: All subjects underwent MRI scanning at USC in a 3T Siemens Trio... (a) T1-weighted images (3D
      MP-RAGE, TR = 2250 ms, TE = 4.15 ms...); (b) Diffusion EPI scan (30-directions with b = 1000 s/mm2
      and b = 2000 s/mm2, TR = 6100 ms, TE = 101 ms... 45 contiguous 2.7 mm axial slices...)
    supports: imaging_details
  - section: Limitations and Future Studies
    page: 276
    quote: We acknowledge, nonetheless, that the ROIs of this atlas are large, usually encompassing different
      brain regions that serve distinct functions (eg, anterior and posterior aspects of the temporal
      gyri).
    supports: limitation
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
---
