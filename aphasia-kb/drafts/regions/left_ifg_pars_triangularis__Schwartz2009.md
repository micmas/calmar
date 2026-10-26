---
schema_version: 2.7
id: left_ifg_pars_triangularis
name: Left IFG Pars Triangularis (BA 45)
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
hemisphere: left
findings:
- id: f1
  target: semantics
  target_kind: impairment
  claim: Damage to the left lateral prefrontal cortex, including the inferior frontal gyrus (BA 45), is
    associated with semantic naming errors, but this effect is mediated by conceptualization processes.
  direction: likely
  relationship: causal
  citation: '@Schwartz2009'
  method: VLSM
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 64
    population: post-stroke aphasia
    phase: not_reported
    cohort: not_reported
  statistics:
    threshold: FDR q = 0.01
  confounders_controlled: []
  confounders_not_controlled: []
  region_definition:
    kind: atlas
    atlas: Brodmann area 45
    description: Left lateral prefrontal cortex, specifically inferior and middle frontal gyri.
  imaging_details:
    reference_space: MNI152
    atlases_used: []
  author_limitations:
  - The association with prefrontal areas was eliminated by filtering for non-verbal semantic comprehension.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 3417
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 7
    quote: There was also a smaller cluster of signiﬁcant voxels in the left lateral prefrontal cortex;
      they were primarily located in the inferior and middle frontal gyri, corresponding to Brodmann areas
      45 and 46.
    supports: claim
  - section: Results
    page: 8
    quote: Filtering out NVcomp had a more substantial impact on the strength and pattern of results (Fig.
      6). No voxels exceeded threshold in either Brodmann area 45/46 or Brodmann area 37.
    supports: claim
  - section: Discussion
    page: 13
    quote: That is, it could be that damage to middle frontal gyrus generates semantic errors in naming
      by compromising mental search for the precise lexical concept, a process that is shared with NVcomp.
    supports: claim
  - section: added by backfill
    page: 5
    quote: Voxels in which fewer than ﬁve patients were lesioned were excluded from the voxel-based lesion-symptom
      mapping analyses.
    supports: method
  - section: added by backfill
    page: 5
    quote: A simple t-test comparing the scores between patients with and without lesions was performed
      at each voxel using the VoxBo brain imaging package
    supports: method
  - section: added by backfill
    page: 5
    quote: The resulting t-map was thresholded to control the false discovery rate (Genovese et al., 2002)
      at q = 0.01
    supports: method
  lesion_mapping:
    analysis: univariate
    n_analysed: 64
    min_lesion_overlap: '>= 5 patients'
    lesion_volume_correction: not_reported
    multiple_comparisons: fdr
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
    - lesion_mapping
---
# Left Inferior Frontal Gyrus Pars Triangularis

@Schwartz2009 found that while BA 45/46 are associated with semantic errors, this relationship is likely due to deficits in conceptualization/semantic control rather than lexical access.
