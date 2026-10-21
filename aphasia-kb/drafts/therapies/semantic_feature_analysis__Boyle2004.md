---
schema_version: 2.3
id: semantic_feature_analysis
name: Semantic Feature Analysis
kind: therapy
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-19
short_description: A treatment that guides the client to produce semantically related features of a target
  word to strengthen the semantic network and improve lexical retrieval.
targets_impairments:
- anomic_aphasia
- wernickes_aphasia
notes: This entry is created for standard SFA; it is distinct from typicality_semantic_feature_analysis.
findings:
- id: f1
  target: anomic_aphasia
  target_kind: impairment
  claim: SFA treatment improves confrontation naming of both treated and untreated nouns in patients with
    anomic aphasia.
  direction: likely
  relationship: responder
  citation: '@Boyle2004'
  method: behavioral_only
  design: case-series
  strength: weak
  evidence_quality: case-study
  sample:
    n: 1
    population: right-handed man with anomic aphasia
    time_post_onset: 15 months
    age_range: '70'
    handedness: right
    language: English
    phase: chronic
  statistics:
    threshold: generalized improvement defined as ability to name at least 3 more probe items than the
      maximum number named during baseline
    effect_size: not_reported
  confounders_controlled: []
  confounders_not_controlled:
  - lack of randomized control group
  region_definition:
    kind: not_reported
    description: behavioural-only treatment-efficacy finding
  imaging: none
  imaging_details:
    reference_space: not_reported
    atlases_used: []
  author_limitations:
  - The present experiment is a Phase II outcomes research study aiming to refine the participant selection
    criteria, treatment protocol, and outcome measures.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 241
    confidence: high
    flags: []
  source_passages:
  - section: Abstract
    page: 1
    quote: Results indicated that confrontation naming of treated nouns improved and generalized to untreated
      nouns for both participants...
    supports: claim
  - section: Participants
    page: 2
    quote: Two right-handed men with aphasia participated in the study.
    supports: sample
  - section: Experimental Design
    page: 4
    quote: A multiple-baseline design across behaviors, replicated across conditions for 1 participant,
      was used to examine acquisition of treated items, generalization to untreated items, and change
      in discourse production.
    supports: method
  - section: Generalization to Probe Nouns
    page: 6
    quote: A generalized improvement in naming was defined as ability to name at least 3 more probe items
      than the maximum number named during baseline sessions.
    supports: statistics
  - section: Introduction
    page: 2
    quote: The present experiment is a Phase II outcomes research study aiming to refine the participant
      selection criteria, treatment protocol, and outcome measures...
    supports: limitation
- id: f2
  target: wernickes_aphasia
  target_kind: impairment
  claim: SFA treatment improves confrontation naming of both treated and untreated nouns in patients with
    Wernicke's aphasia.
  direction: likely
  relationship: responder
  citation: '@Boyle2004'
  method: behavioral_only
  design: case-series
  strength: weak
  evidence_quality: case-study
  sample:
    n: 1
    population: right-handed man with Wernicke's aphasia
    time_post_onset: 14 months
    age_range: '80'
    handedness: right
    language: English
    phase: chronic
  statistics:
    threshold: generalized improvement defined as ability to name at least 3 more probe items than the
      maximum number named during baseline
    effect_size: not_reported
  confounders_controlled: []
  confounders_not_controlled:
  - lack of randomized control group
  region_definition:
    kind: not_reported
    description: behavioural-only treatment-efficacy finding
  imaging: none
  imaging_details:
    reference_space: not_reported
    atlases_used: []
  author_limitations:
  - The present experiment is a Phase II outcomes research study aiming to refine the participant selection
    criteria, treatment protocol, and outcome measures.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 241
    confidence: high
    flags: []
  source_passages:
  - section: Abstract
    page: 1
    quote: Results indicated that confrontation naming of treated nouns improved and generalized to untreated
      nouns for both participants...
    supports: claim
  - section: Participants
    page: 2
    quote: Two right-handed men with aphasia participated in the study.
    supports: sample
  - section: Experimental Design
    page: 4
    quote: A multiple-baseline design across behaviors, replicated across conditions for 1 participant,
      was used to examine acquisition of treated items, generalization to untreated items, and change
      in discourse production.
    supports: method
  - section: Generalization to Probe Nouns
    page: 6
    quote: A generalized improvement in naming was defined as ability to name at least 3 more probe items
      than the maximum number named during baseline sessions.
    supports: statistics
  - section: Introduction
    page: 2
    quote: The present experiment is a Phase II outcomes research study aiming to refine the participant
      selection criteria, treatment protocol, and outcome measures...
    supports: limitation
- id: f3
  target: fluency
  target_kind: impairment
  claim: SFA treatment for confrontation naming leads to mixed improvements in discourse production, increasing
    information units or efficiency but not reducing overall lexical retrieval difficulty.
  direction: mixed
  relationship: responder
  citation: '@Boyle2004'
  method: behavioral_only
  design: case-series
  strength: weak
  evidence_quality: case-study
  sample:
    n: 2
    population: right-handed men with fluent aphasia
    time_post_onset: mean 14.5 months
    age_range: 70-80
    handedness: right
    language: English
    phase: chronic
  statistics:
    threshold: not_reported
    effect_size: not_reported
  confounders_controlled: []
  confounders_not_controlled:
  - lack of randomized control group
  region_definition:
    kind: not_reported
    description: behavioural-only treatment-efficacy finding
  imaging: none
  imaging_details:
    reference_space: not_reported
    atlases_used: []
  author_limitations:
  - The present experiment is a Phase II outcomes research study aiming to refine the participant selection
    criteria, treatment protocol, and outcome measures.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Abstract, page 1
    confidence: high
    flags: []
  source_passages:
  - section: Abstract
    page: 1
    quote: Both participants demonstrated improvement in some aspects of discourse production associated
      with the confrontation naming SFA treatment. However, there was no change in most manifestations
      of lexical retrieval difficulty during discourse for either participant.
    supports: claim
  - section: Participants
    page: 2
    quote: Two right-handed men with aphasia participated in the study.
    supports: sample
  - section: Experimental Design
    page: 4
    quote: A multiple-baseline design across behaviors, replicated across conditions for 1 participant,
      was used to examine acquisition of treated items, generalization to untreated items, and change
      in discourse production.
    supports: method
  - section: Introduction
    page: 2
    quote: The present experiment is a Phase II outcomes research study aiming to refine the participant
      selection criteria, treatment protocol, and outcome measures...
    supports: limitation
- id: f4
  target: semantic_feature_analysis
  target_kind: therapy
  claim: Increasing the number of stimulus exemplars in SFA treatment does not significantly enhance the
    generalization of naming to untrained items.
  direction: no_effect
  relationship: responder
  citation: '@Boyle2004'
  method: behavioral_only
  design: case-series
  strength: weak
  evidence_quality: case-study
  sample:
    n: 1
    population: right-handed man with Wernicke's aphasia
    time_post_onset: 14 months
    age_range: '80'
    handedness: right
    language: English
    phase: chronic
  statistics:
    threshold: not_reported
    effect_size: not_reported
  confounders_controlled: []
  confounders_not_controlled:
  - lack of randomized control group
  region_definition:
    kind: not_reported
    description: behavioural-only treatment-efficacy finding
  imaging: none
  imaging_details:
    reference_space: not_reported
    atlases_used: []
  author_limitations:
  - The present experiment is a Phase II outcomes research study aiming to refine the participant selection
    criteria, treatment protocol, and outcome measures.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 241
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 11
    quote: However, adding 60 items to his treatment protocol did not improve generalization to untreated
      items above levels that had been achieved with the same 20 items used repeatedly.
    supports: claim
  - section: Participants
    page: 2
    quote: Two right-handed men with aphasia participated in the study.
    supports: sample
  - section: Experimental Design
    page: 4
    quote: A multiple-baseline design across behaviors, replicated across conditions for 1 participant,
      was used to examine acquisition of treated items, generalization to untreated items, and change
      in discourse production.
    supports: method
  - section: Introduction
    page: 2
    quote: The present experiment is a Phase II outcomes research study aiming to refine the participant
      selection criteria, treatment protocol, and outcome measures...
    supports: limitation
---
