---
schema_version: 2.7
id: virtual_reality_rehabilitation
name: Virtual Reality Rehabilitation
kind: therapy
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-21
short_description: Use of computer-generated environments (immersive or non-immersive) to provide interactive,
  goal-oriented tasks for stroke recovery.
targets_impairments:
- upper_limb_function
- balance
- activity_limitation
- cognitive_function
notes: This is a Cochrane systematic review covering a wide range of VR applications (gaming consoles,
  customised systems, immersive HMDs).
findings:
- id: f1
  target: upper_limb_function
  target_kind: impairment
  claim: Virtual reality is slightly more beneficial than alternative therapy approaches for improving
    upper limb function and activity.
  direction: likely
  relationship: responder
  citation: '@Laver2025'
  method: meta-analysis
  design: systematic-review
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 2830
    population: people receiving stroke rehabilitation
    time_post_onset: acute to chronic
    age_range: 34 to 75 years
    handedness: not_reported
    language: mostly English
    phase: chronic
    cohort: not_reported
  statistics:
    threshold: fixed-effect model
    effect_size: SMD 0.20
    ci_95: '[0.12, 0.28]'
    p_value: not_reported
  confounders_controlled:
  - amount of therapy
  confounders_not_controlled:
  - cognitive impairment
  - aphasia
  - visual impairment
  author_limitations:
  - Evidence remains mostly low or moderate certainty due to small study sizes and risk of bias.
  - Exclusion of people with cognitive, communication, or visual deficits limits generalisability.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Abstract, page 1
    confidence: high
    flags: []
  source_passages:
  - section: Abstract
    page: 4
    quote: When comparing virtual reality with alternative therapy approaches, results suggest that virtual
      reality may be beneficial in slightly improving upper limb function and activity (SMD 0.20, 95%
      CI 0.12 to 0.28; 67 studies, 2830 participants; low-certainty evidence).
    supports: claim
  - section: Methods
    page: 3
    quote: We included randomised trials in adults afer stroke comparing virtual reality [...] with alternative
      or usual care.
    supports: method
  - section: Results
    page: 18
    quote: A total of 7188 participants poststroke were included in the trials. [...] all studies reporting
      the average age of participants ranging from 34 to 75 years.
    supports: sample
  - section: Discussion
    page: 30
    quote: the quality of evidence in the field is limited due to small sample sizes and risk of bias
      present in the majority of studies.
    supports: limitation
  - section: Discussion
    page: 31
    quote: People with cognitive impairment, or communication or visual deficits, remain excluded in many
      studies, thereby raising questions about how applicable this intervention is to a wide range of
      stroke survivors.
    supports: limitation
  region_definition:
    kind: not_reported
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
- id: f2
  target: upper_limb_function
  target_kind: impairment
  claim: Adding virtual reality to usual care (increasing total therapy time) provides a moderate benefit
    for upper limb function compared to usual care alone.
  direction: likely
  relationship: responder
  citation: '@Laver2025'
  method: meta-analysis
  design: systematic-review
  strength: strong
  evidence_quality: cohort
  sample:
    n: 689
    population: people receiving stroke rehabilitation
    time_post_onset: acute to chronic
    age_range: not_reported
    handedness: not_reported
    language: not_reported
    phase: chronic
    cohort: not_reported
  statistics:
    threshold: fixed-effect model
    effect_size: SMD 0.42
    ci_95: '[0.26, 0.58]'
    p_value: not_reported
  confounders_controlled:
  - usual care baseline
  confounders_not_controlled: []
  author_limitations:
  - Evidence certainty is moderate; results may be influenced by the increased total dose of therapy.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Abstract, page 1
    confidence: high
    flags: []
  source_passages:
  - section: Abstract
    page: 4
    quote: The addition of virtual reality to usual care or rehabilitation (resulting in an increased
      amount of time spent in therapy for those in the intervention group) probably increases upper limb
      function and activity compared to usual care alone (SMD 0.42, 95% CI 0.26 to 0.58; 21 studies, 689
      participants; moderate-certainty evidence).
    supports: claim
  - section: Discussion
    page: 32
    quote: a moderate effect on upper limb function when virtual reality was used to augment usual care
      (standardised mean difference (SMD) 0.42, moderate-certainty evidence)
    supports: statistics
  region_definition:
    kind: not_reported
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
- id: f3
  target: balance
  target_kind: impairment
  claim: Virtual reality is slightly more beneficial than alternative therapy for improving balance.
  direction: likely
  relationship: responder
  citation: '@Laver2025'
  method: meta-analysis
  design: systematic-review
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 871
    population: people receiving stroke rehabilitation
    time_post_onset: not_reported
    age_range: not_reported
    handedness: not_reported
    language: not_reported
    phase: not_reported
    cohort: not_reported
  statistics:
    threshold: fixed-effect model
    effect_size: SMD 0.26
    ci_95: '[0.12, 0.40]'
    p_value: not_reported
  confounders_controlled:
  - amount of therapy
  confounders_not_controlled: []
  author_limitations:
  - Low certainty of evidence due to study limitations and inconsistency.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Abstract, page 1
    confidence: high
    flags: []
  source_passages:
  - section: Abstract
    page: 4
    quote: Compared to alternative therapy approaches, virtual reality may be slightly beneficial for
      balance (SMD 0.26, 95% CI 0.12 to 0.40; 24 studies, 871 participants; low-certainty evidence)
    supports: claim
  region_definition:
    kind: not_reported
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
- id: f4
  target: activity_limitation
  target_kind: impairment
  claim: Virtual reality probably reduces activity limitation more effectively than alternative therapy
    approaches.
  direction: likely
  relationship: responder
  citation: '@Laver2025'
  method: meta-analysis
  design: systematic-review
  strength: strong
  evidence_quality: cohort
  sample:
    n: 1495
    population: people receiving stroke rehabilitation
    time_post_onset: not_reported
    age_range: not_reported
    handedness: not_reported
    language: not_reported
    phase: not_reported
    cohort: not_reported
  statistics:
    threshold: fixed-effect model
    effect_size: SMD 0.21
    ci_95: '[0.11, 0.32]'
    p_value: not_reported
  confounders_controlled:
  - amount of therapy
  confounders_not_controlled: []
  author_limitations:
  - Moderate certainty evidence; results are based on pooled different outcome measurement tools.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Abstract, page 1
    confidence: high
    flags: []
  source_passages:
  - section: Abstract
    page: 4
    quote: probably reduces activity limitation (SMD 0.21, 95% CI 0.11 to 0.32; 33 studies, 1495 participants;
      moderate-certainty evidence).
    supports: claim
  region_definition:
    kind: not_reported
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
- id: f5
  target: cognitive_function
  target_kind: impairment
  claim: Virtual reality shows a beneficial effect on cognitive function compared to alternative therapy.
  direction: likely
  relationship: responder
  citation: '@Laver2025'
  method: meta-analysis
  design: systematic-review
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 279
    population: people receiving stroke rehabilitation
    time_post_onset: not_reported
    age_range: not_reported
    handedness: not_reported
    language: not_reported
    phase: not_reported
    cohort: not_reported
  statistics:
    threshold: fixed-effect model
    effect_size: SMD 0.32
    ci_95: '[0.08, 0.56]'
    p_value: not_reported
  confounders_controlled: []
  confounders_not_controlled: []
  author_limitations:
  - Small number of studies (n=9) compared to motor outcomes.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 25
    confidence: high
    flags: []
  source_passages:
  - section: Results
    page: 27
    quote: We examined the eﬀect of virtual reality on cognitive function [...] by pooling nine studies
      with 279 participants. There was an eﬀect in favour of virtual reality (SMD 0.32, 95% CI 0.08 to
      0.56; heterogeneity I2 = 47%; Analysis 1.12).
    supports: claim
  region_definition:
    kind: not_reported
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
---
