---
schema_version: 2.7
id: right_hemisphere_communication_profiles__Cote2007
name: Right Hemisphere Communication Impairment Profiles
kind: classical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-23
findings:
- id: f1
  target: right_hemisphere_damage
  target_kind: impairment
  claim: Communication impairments following right-hemisphere damage are heterogeneous and can manifest
    as distinct clinical profiles involving prosodic, lexical-semantic, discourse, and pragmatic deficits.
  direction: likely
  relationship: causal
  citation: '@Cote2007'
  method: behavioral_only
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 28
    population: French-speaking individuals with a right-hemisphere lesion
    time_post_onset: 3 to 14 weeks post-onset (average 6 weeks)
    phase: early_subacute
    age_range: 26 to 90 years
    handedness: mostly right-handed
    language: French
    cohort: not_reported
  statistics:
    threshold: z score < -1.5 and > 50% of cluster members below -2
    effect_size: not_reported
  confounders_controlled:
  - â– age and education (via z-score normalization)
  confounders_not_controlled:
  - â– lesion site (not significantly associated with specific clusters)
  region_definition:
    kind: not_reported
    description: Right hemisphere lesions (CT or MRI confirmed)
  author_limitations:
  - Small number of participants restricting generalisation of results.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, pages 744-746
    confidence: high
    flags:
    - â– target_id right_hemisphere_damage is forward-looking
  source_passages:
  - section: Abstract
    page: 1
    quote: Four subgroups of RHD individuals were identified on the basis of the overall similarities
      of performance on the 14 tasks of the Protocole MEC.
    supports: claim
  - section: Method - Participants
    page: 4
    quote: A total of 28 French-speaking volunteer participants (15 men and 13 women) were evaluated.
      [...] All were 3 to 14 weeks post-onset (with an average of 6 weeks post-onset).
    supports: sample
  - section: Results
    page: 6
    quote: 'The performance of all participants with RHD for all tasks was submitted to a hierarchical
      cluster analysis [...] the result for each task was considered impaired for a given subgroup under
      the following two conditions: (1) the overall mean z score of the cluster was below -1.5; and (2)
      more than 50% of the members of the cluster had a z score below -2.'
    supports: method
  - section: Discussion
    page: 10
    quote: The main limitation of the present study is surely the small number of participants evaluated,
      restricting the generalisation of results to the population of RHD.
    supports: limitation
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
- id: f2
  target: right_hemisphere_damage
  target_kind: impairment
  claim: A right-hemisphere lesion does not automatically result in communication disorders; a significant
    minority of patients may show globally normal communication abilities.
  direction: unlikely
  relationship: causal
  citation: '@Cote2007'
  method: behavioral_only
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 28
    population: French-speaking individuals with a right-hemisphere lesion
    time_post_onset: 3 to 14 weeks post-onset (average 6 weeks)
    phase: early_subacute
    age_range: 26 to 90 years
    handedness: mostly right-handed
    language: French
    cohort: not_reported
  statistics:
    threshold: z scores within normal range
    effect_size: not_reported
  confounders_controlled:
  - â– age and education
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: Right hemisphere lesions
  author_limitations:
  - Small number of participants restricting generalisation of results.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Discussion, page 9
    confidence: high
    flags: []
  source_passages:
  - section: Discussion
    page: 9
    quote: results confirm that a right-hemisphere lesion does not result in communication disorders in
      all individuals. Out of the 28 participants with RHD, a subgroup of 11 was identified by the cluster
      analysis as presenting with communication abilities globally comparable to that of age- and education-matched
      normal control participants
    supports: claim
  - section: Discussion
    page: 10
    quote: The main limitation of the present study is surely the small number of participants evaluated,
      restricting the generalisation of results to the population of RHD.
    supports: limitation
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
---
This study explored communication impairment profiles in individuals with right-hemisphere damage (RHD) using the Protocole MEC. The authors identified heterogeneous profiles of deficits across prosodic, lexical-semantic, discourse, and pragmatic domains, while also noting that some individuals with RHD maintain normal communication abilities.
