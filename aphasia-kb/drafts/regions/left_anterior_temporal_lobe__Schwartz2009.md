---
schema_version: 2.3
id: left_anterior_temporal_lobe
name: Left Anterior Temporal Lobe
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
hemisphere: left
findings:
- id: f1
  target: semantics
  target_kind: impairment
  claim: Damage to the left anterior temporal lobe is associated with an increased rate of semantic naming
    errors.
  direction: likely
  relationship: causal
  citation: '@Schwartz2009'
  method: VLSM
  design: cross-sectional
  strength: strong
  evidence_quality: cohort
  sample:
    n: 64
    population: post-stroke aphasia
    time_post_onset: mean 68 months (range 1-381)
    age_range: mean 58 (range 26-78)
    handedness: pre-morbid right handedness
    language: English as primary language
    phase: chronic
  statistics:
    threshold: FDR q = 0.01
    effect_size: not_reported
  confounders_controlled: []
  confounders_not_controlled:
  - lesion volume
  region_definition:
    kind: data_driven_cluster
    description: Voxels in the anterior temporal lobe and temporal pole (Brodmann areas 21 and 38).
  imaging_details:
    field_strength: 3T
    preprocessing_pipeline: Symmetric diffeomorphic registration algorithm (ANTS) to MNI space Colin27
      volume
    reference_space: MNI152
    atlases_used:
    - AAL
  author_limitations:
  - Vascular anatomy of MCA strokes limits coverage of the inferior temporal and fusiform gyri.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 3417
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 7
    quote: In the analysis performed to explore the anatomic basis of the variable SemErr, we found 35
      466 voxels for which a signiﬁcant correlation between lesion status and impaired performance on
      the SemErr measure was identiﬁed. As indicated in Fig. 4, the voxels with the highest t-values were
      located in the anterior temporal lobe.
    supports: claim
  - section: Methods
    page: 4
    quote: The 64 who were included in the study (42% females; 48% African American) had a mean age of
      58 (range 26-78), mean years of education of 14 (10-21) and mean months post-onset of 68 (1-381).
    supports: sample
  - section: Voxel-based lesion-symptom mapping methods
    page: 5
    quote: The resulting t-map was thresholded to control the false discovery rate (Genovese et al., 2002)
      at q = 0.01
    supports: statistics
  - section: Lesion segmentation and warping to template
    page: 5
    quote: The structural scans were registered to a common template using a symmetric diffeomorphic registration
      algorithm (Avants et al., 2006...)
    supports: imaging_details
  - section: Discussion
    page: 12
    quote: It must be emphasized that the region within the left anterior temporal lobe that our analysis
      picked out almost certainly underestimates the extent of the temporal lobe involvement. As noted
      earlier, there were too few patients with lesions in the inferior temporal or fusiform gyri to detect
      effects there.
    supports: limitation
- id: f2
  target: semantics
  target_kind: impairment
  claim: The association between the left anterior temporal lobe and semantic naming errors persists after
    controlling for non-verbal semantic comprehension, suggesting a specific role in the production stage
    of lexical access.
  direction: likely
  relationship: causal
  citation: '@Schwartz2009'
  method: VLSM
  design: cross-sectional
  strength: strong
  evidence_quality: cohort
  sample:
    n: 64
    population: post-stroke aphasia
    phase: not_reported
  statistics:
    threshold: FDR q = 0.01
  confounders_controlled:
  - non-verbal semantic comprehension (NVcomp)
  confounders_not_controlled: []
  region_definition:
    kind: data_driven_cluster
    description: Portion of the temporal lobe anterior to a y-value of -35.
  imaging_details:
    reference_space: MNI152
    atlases_used: []
  author_limitations:
  - Vascular anatomy of MCA strokes limits coverage of the inferior temporal and fusiform gyri.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 3417
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 8
    quote: Filtering out NVcomp had a more substantial impact on the strength and pattern of results (Fig.
      6). No voxels exceeded threshold in either Brodmann area 45/46 or Brodmann area 37. Of the 6366
      voxels exceeding threshold, the majority (4361) were in the anterior temporal lobe region described
      above.
    supports: claim
  - section: Discussion
    page: 10
    quote: Thus, the conclusion from the main analyses is that the symptom of interest—semantic errors
      generated at the word production stage—arises from damage to anterior temporal lobe.
    supports: claim
  - section: Discussion
    page: 12
    quote: It must be emphasized that the region within the left anterior temporal lobe that our analysis
      picked out almost certainly underestimates the extent of the temporal lobe involvement.
    supports: limitation
---
# Left Anterior Temporal Lobe

Findings from @Schwartz2009 indicate that the left anterior temporal lobe is critical for the production of semantic word retrieval, specifically the mapping from concepts to lemmas.
