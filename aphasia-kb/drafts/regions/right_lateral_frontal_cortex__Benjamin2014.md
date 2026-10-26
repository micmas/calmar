---
schema_version: 2.7
id: right_lateral_frontal_cortex
name: Right Lateral Frontal Cortex
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
hemisphere: right
findings:
- id: f1
  target: intention_treatment
  target_kind: therapy
  claim: Initiating word-finding trials with complex left-hand movements (Intention Treatment) induces
    a significant rightward shift in lateral frontal cortex activity during word production that persists
    for 3 months.
  direction: likely
  relationship: treatment_response
  citation: '@Benjamin2014'
  method: fMRI_activation
  design: longitudinal
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 14
    population: chronic left-hemisphere stroke aphasia
    time_post_onset: '>6 months'
    age_range: mean 67.5 (SD not reported)
    handedness: all right-handed
    language: English
    phase: chronic
    cohort: not_reported
  statistics:
    threshold: P < .05
    effect_size: t = -2.602 (posttreatment), t = -2.332 (3-month follow-up)
  confounders_controlled:
  - ' picture-naming impairment (BNT)'
  - frontal lesion extent (beyond precentral sulcus)
  confounders_not_controlled:
  - ' gender composition'
  - education level
  region_definition:
    kind: atlas
    atlas: Harvard-Oxford
    description: Lateral frontal ROI constructed by combining regions from the Harvard-Oxford atlas, excluding
      the anterior most portion of frontal polar cortex.
  imaging_details:
    field_strength: 3T
    modalities:
    - modality: fMRI
      sequence: gradient echo-echo planar
      voxel_size_mm:
      - null
      - null
      - 4
      TR_ms: 1700
      TE_ms: 30
      volumes: 60
    - modality: T1
      sequence: turbo field echo
      voxel_size_mm:
      - null
      - null
      - 1.0
      TR_ms: 8.1
      TE_ms: 3.7
    preprocessing_pipeline: ITK-Snap masking + FSL FNIRT nonlinear warping to MNI152
    reference_space: MNI152
    atlases_used:
    - Harvard-Oxford
    task:
      name: Category member generation
      description: Patients heard and read a category and attempted to generate aloud a single member.
      contrasts:
      - Task > Baseline
      baseline: intertrial intervals
  author_limitations:
  - Small sample size (n=14) limits statistical power.
  - Marginal differences in gender and education between groups.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 548
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 548
    quote: One-tailed t tests indicated that IT patients demonstrated a significant rightward shift in
      lateral frontal activity from pretreatment to both posttreatment (t = -2.602, df = 6, P < .05) and
      3-month follow-up (t = -2.332, df = 5, P < .05).
    supports: claim
  - section: Method
    page: 2
    quote: Fourteen chronic (>6 months) aphasia patients participated. [...] Patients were premorbidly
      right-handed, used English as a first language, and had single or multiple left-hemisphere ischemic
      or hemorrhagic strokes.
    supports: sample
  - section: Data Analyses
    page: 4
    quote: Three regions of interest (ROIs; medial frontal, lateral frontal, and posterior perisylvian)
      were constructed for each hemisphere by combining regions from the Harvard-Oxford atlas distributed
      with FSL...
    supports: region_definition
  - section: Data Analyses
    page: 4
    quote: Lesions were masked on T1-weighted images using ITK-Snap [...] and then warped into MNI-152
      atlas space using the nonlinear FNIRT algorithm from FSL.
    supports: imaging_details
  - section: Discussion
    page: 6
    quote: Small number of subjects in the groups...
    supports: limitation
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
---
# Right Lateral Frontal Cortex

This region is involved in the relateralization of language production following Intention Treatment.
