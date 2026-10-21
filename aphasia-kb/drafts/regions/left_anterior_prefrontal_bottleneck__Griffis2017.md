---
schema_version: 2.3
id: left_anterior_prefrontal_bottleneck
name: Left Anterior Prefrontal White Matter Bottleneck
kind: network
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
hemisphere: left
members:
- left_uncinate_fasciculus
- left_inferior_fronto_occipital_fasciculus
- left_anterior_thalamic_radiations
findings:
- id: f1
  target: fluency
  target_kind: impairment
  claim: Damage to the left anterior prefrontal bottleneck uniquely predicts deficits in verbal fluency.
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
    phase: not_reported
  statistics:
    threshold: Bonferroni-Holm corrected p < 0.05
    effect_size: not_reported
  confounders_controlled:
  - lesion volume
  confounders_not_controlled: []
  region_definition:
    kind: data_driven_cluster
    description: Intersection of left UF, IFOF, and ATR at 20% probability threshold
  imaging_details:
    reference_space: MNI152
    atlases_used:
    - ICBM-DTI
    preprocessing_pipeline: SPM12 unified normalization
    field_strength: 3T
  author_limitations:
  - bottleneck ROIs were defined using thresholded tract probability maps
  provenance:
    extracted_by: agent
    extracted_on: '2026-01-01'
    paper_section: Results, page 6
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 6
    quote: Anterior lesion status, posterior lesion status, and the interaction term each uniquely predicted
      verbal fluency scores
    supports: claim
  - section: Discussion
    page: 12
    quote: bottleneck ROIs were defined using thresholded tract probability maps
    supports: limitation
- id: f2
  target: anomic_aphasia
  target_kind: impairment
  claim: Damage to the left anterior prefrontal bottleneck does not significantly predict deficits in
    picture naming.
  direction: no_effect
  relationship: causal
  citation: '@Griffis2017'
  method: LSM
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 43
    population: chronic left hemispheric stroke
    phase: not_reported
  statistics:
    threshold: not_reported
    effect_size: not_reported
  confounders_controlled:
  - lesion volume
  confounders_not_controlled: []
  region_definition:
    kind: data_driven_cluster
    description: Intersection of left UF, IFOF, and ATR at 20% probability threshold
  imaging_details:
    reference_space: MNI152
    atlases_used:
    - ICBM-DTI
    preprocessing_pipeline: SPM12 unified normalization
    field_strength: 3T
  author_limitations:
  - bottleneck ROIs were defined using thresholded tract probability maps
  provenance:
    extracted_by: agent
    extracted_on: '2026-01-01'
    paper_section: Discussion, page 10
    confidence: high
    flags: []
  source_passages:
  - section: Discussion
    page: 10
    quote: we did not find a relationship between damage to this region and deficits in picture naming
    supports: claim
  - section: Discussion
    page: 12
    quote: bottleneck ROIs were defined using thresholded tract probability maps
    supports: limitation
- id: f3
  target: semantics
  target_kind: impairment
  claim: Damage to the left anterior prefrontal bottleneck does not significantly predict deficits in
    auditory semantic processing.
  direction: no_effect
  relationship: causal
  citation: '@Griffis2017'
  method: LSM
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 39
    population: chronic left hemispheric stroke
    phase: not_reported
  statistics:
    threshold: not_reported
    effect_size: not_reported
  confounders_controlled:
  - lesion volume
  confounders_not_controlled: []
  region_definition:
    kind: data_driven_cluster
    description: Intersection of left UF, IFOF, and ATR at 20% probability threshold
  imaging_details:
    reference_space: MNI152
    atlases_used:
    - ICBM-DTI
    preprocessing_pipeline: SPM12 unified normalization
    field_strength: 3T
  author_limitations:
  - bottleneck ROIs were defined using thresholded tract probability maps
  provenance:
    extracted_by: agent
    extracted_on: '2026-01-01'
    paper_section: Discussion, page 10
    confidence: high
    flags: []
  source_passages:
  - section: Discussion
    page: 10
    quote: we did not find a relationship between damage to this region and deficits in... auditory semantic
      processing
    supports: claim
  - section: Discussion
    page: 12
    quote: bottleneck ROIs were defined using thresholded tract probability maps
    supports: limitation
---
Findings from @Griffis2017 regarding the anterior prefrontal white matter bottleneck.
