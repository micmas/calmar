---
schema_version: 2.3
id: left_posterior_temporal_bottleneck
name: Left Posterior Temporal White Matter Bottleneck
kind: network
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
hemisphere: left
members:
- left_arcuate_fasciculus
- left_inferior_longitudinal_fasciculus
- left_inferior_fronto_occipital_fasciculus
findings:
- id: f1
  target: fluency
  target_kind: impairment
  claim: Damage to the left posterior temporal bottleneck uniquely predicts deficits in verbal fluency
    beyond cortical and tract lesion loads.
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
    effect_size: delta R2 = 0.20
  confounders_controlled:
  - lesion volume
  - tract lesion load
  - cortical lesion load
  confounders_not_controlled: []
  region_definition:
    kind: data_driven_cluster
    description: Intersection of left ILF, IFOF, and SLF/AF at 20% probability threshold
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
    quote: The full model explained significantly more variance than the lesion load control model (R2
      = 0.84, ΔR2 = 0.20, F3,25 = 10.42, p < 0.001, corrected)
    supports: statistics
  - section: Results
    page: 6
    quote: indicating that bottleneck lesion status provided unique information about verbal fluency scores
      even after accounting for concomitant cortical and tract damage.
    supports: claim
  - section: Discussion
    page: 12
    quote: bottleneck ROIs were defined using thresholded tract probability maps
    supports: limitation
- id: f2
  target: anomic_aphasia
  target_kind: impairment
  claim: Damage to the left posterior temporal bottleneck uniquely predicts naming deficits beyond cortical
    and tract lesion loads.
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
    effect_size: delta R2 = 0.23
  confounders_controlled:
  - lesion volume
  - tract lesion load
  - cortical lesion load
  confounders_not_controlled: []
  region_definition:
    kind: data_driven_cluster
    description: Intersection of left ILF, IFOF, and SLF/AF at 20% probability threshold
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
    paper_section: Results, page 8
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 8
    quote: The full model explained significantly more variance than the lesion load control model (R2
      = 0.72, ΔR2 = 0.23, F1,33 = 28.03, p < 0.001, corrected)
    supports: statistics
  - section: Results
    page: 8
    quote: indicating that posterior ROI lesion status provided unique information about naming scores
      even after accounting for concomitant cortical and tract damage.
    supports: claim
  - section: Discussion
    page: 12
    quote: bottleneck ROIs were defined using thresholded tract probability maps
    supports: limitation
- id: f3
  target: semantics
  target_kind: impairment
  claim: Damage to the left posterior temporal bottleneck uniquely predicts auditory semantic decision
    deficits beyond cortical and tract lesion loads.
  direction: likely
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
    threshold: Bonferroni-Holm corrected p < 0.05
    effect_size: delta R2 = 0.16
  confounders_controlled:
  - lesion volume
  - tract lesion load
  - cortical lesion load
  confounders_not_controlled: []
  region_definition:
    kind: data_driven_cluster
    description: Intersection of left ILF, IFOF, and SLF/AF at 20% probability threshold
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
    paper_section: Results, page 8
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 8
    quote: The full model explained significantly more variance than the lesion load control model (R2
      = 0.50, ΔR2 = 0.16, F1,29 = 9.28, p = 0.005, corrected)
    supports: statistics
  - section: Results
    page: 8
    quote: indicating that ROI lesion status provided unique information about auditory semantic decision
      scores even after accounting for concomitant cortical and tract damage.
    supports: claim
  - section: Discussion
    page: 12
    quote: bottleneck ROIs were defined using thresholded tract probability maps
    supports: limitation
---
Findings from @Griffis2017 regarding the posterior temporal white matter bottleneck.
