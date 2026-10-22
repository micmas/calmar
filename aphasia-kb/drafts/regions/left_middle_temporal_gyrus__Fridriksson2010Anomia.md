---
schema_version: 2.3
id: left_middle_temporal_gyrus
name: Left Middle Temporal Gyrus (Ventral Stream Node)
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
hemisphere: left
findings:
- id: f1
  target: anomic_aphasia
  target_kind: impairment
  claim: Damage to the posterior portion of the left middle temporal lobe and the temporal-occipital junction
    is associated with a reduced likelihood of improvement in naming following treatment.
  direction: unlikely
  relationship: responder
  citation: '@Fridriksson2010Anomia'
  method: LSM
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 26
    population: chronic stroke and concomitant aphasia
    time_post_onset: '>= 8 months'
    age_range: mean 59.7 (SD 12.3)
    handedness: not_reported
    language: not_reported
    phase: chronic
  statistics:
    threshold: p < 0.05 (uncorrected)
    effect_size: Z = 2.20
    p_value: not_reported
  confounders_controlled:
  - lesion size
  confounders_not_controlled: []
  region_definition:
    kind: data_driven_cluster
    description: Posterior portion of the left middle temporal lobe and the temporal-occipital junction,
      including Brodmann's areas 37, 39, and 19.
  imaging_details:
    reference_space: MNI152
    atlases_used:
    - Talairach Daemon
    - Brodmann's area map
    preprocessing_pipeline: T2-MRI lesions drawn in native space (MRIcron) and warped into standard space
      using the same transformation matrix generated to coregister the T2-MRI
  author_limitations:
  - The structural and functional MRI data were not included in the same analyses.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: 'Results - Secondary outcome: structural MRI results'
    confidence: high
    flags:
    - cohort overlaps with @Fridriksson2010 (as stated in paper)
  source_passages:
  - section: Results
    page: 1
    quote: damage to the posterior portion of the left middle temporal lobe and the temporal-occipital
      junction had a particularly negative effect on treatment outcome.
    supports: claim
  - section: Materials and Methods
    page: 2
    quote: Twenty-six patients (14 women) with chronic stroke and concomitant aphasia were included.
    supports: sample
  - section: Materials and Methods
    page: 3
    quote: a t test was performed on a voxel-by-voxel basis to examine the relationship between localized
      damage and change in correct naming when lesion size was entered as a cofactor
    supports: method
  - section: Results
    page: 4
    quote: The strongest lesion predictor (i.e., the voxel with the highest Z score) of limited improvement
      in correct naming was found at the junction of Brodmann's areas (BA) 37 and 39 in the posterior
      portion of the middle temporal lobe (Z = 2.20, uncorrected)
    supports: statistics
  - section: Discussion
    page: 5
    quote: Although the structural and functional MRI data were not included in the same analyses, the
      results from each suggest that patients' response to treatment relies on both structural integrity
      of specific brain regions... and recruitment of both the left frontal and parietal regions.
    supports: limitation
---
Finding f1 describes the negative impact of posterior left temporal lobe damage on the efficacy of anomia treatment.
