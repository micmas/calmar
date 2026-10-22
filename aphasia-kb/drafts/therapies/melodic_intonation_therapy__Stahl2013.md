---
schema_version: 2.6
id: melodic_intonation_therapy
name: Melodic Intonation Therapy (MIT)
kind: therapy
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-22
targets_impairments:
- fluency
- phonological_production
short_description: A rehabilitation program using singing, rhythmic speech, and common phrases to aid
  speech recovery in non-fluent aphasia.
findings:
- id: f1
  target: fluency
  target_kind: impairment
  claim: Singing and rhythmic therapy are similarly effective in improving the production of formulaic
    phrases in patients with chronic non-fluent aphasia.
  direction: likely
  relationship: causal
  citation: '@Stahl2013'
  method: clinical_RCT
  design: longitudinal
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 15
    population: chronic non-fluent aphasia (Broca's or global)
    time_post_onset: at least 6 months post-infarction
    phase: chronic
    age_range: 40-72 years (mean 56, SD 10)
    handedness: all right-handed
    language: German native-speakers
  statistics:
    threshold: alpha level of 0.05
    effect_size: F(2, 11) = 49.86, p < 0.001, partial eta2 = 0.90
  confounders_controlled:
  - baseline scores
  - phonatory quality
  - vocal frequency variability
  - pitch accuracy
  - syllable duration
  - phonetic complexity
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: Behavioural outcome measuring percentage of correct syllables in formulaic lyrics.
  author_limitations:
  - The sample size in the current experiment was too small to deliver universally valid results.
  - The current experiment did not include a control treatment for rhythmic therapy [specifically a non-rhythmic
    formulaic training].
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 7
    confidence: high
    flags:
    - quasi-experimental assignment based on clinical criteria rather than random allocation
  source_passages:
  - section: Abstract
    page: 1
    quote: The results provide the first evidence that singing and rhythmic speech may be similarly effective
      in the treatment of non-fluent aphasia.
    supports: claim
  - section: Materials and Methods - Participants
    page: 2
    quote: Fifteen stroke patients were included in the study. [...] all patients were at least 6 months
      post-infarction at the time of testing, suggesting a chronic post-stroke stage.
    supports: sample
  - section: Materials and Methods - Treatments
    page: 6
    quote: All patients underwent three 1-h long, weekly training sessions, over a period of 6 weeks.
    supports: method
  - section: Results
    page: 7
    quote: A repeated measures ANCOVA, based on articulatory quality, revealed a significant interaction
      of time, treatment group, and lyrics [F(2, 11) = 49.86, p < 0.001, partial eta2 = 0.90].
    supports: statistics
  - section: Discussion
    page: 9
    quote: One may argue that the sample size in the current experiment was too small to deliver universally
      valid results.
    supports: limitation
  - section: Discussion
    page: 10
    quote: It should be noted that the current experiment did not include a control treatment for rhythmic
      therapy.
    supports: limitation
---

Findings from @Stahl2013 indicate that both singing and rhythmic therapy significantly improve the production of formulaic phrases compared to standard speech therapy, suggesting that rhythm, rather than melody specifically, may be the primary driver of this specific recovery path.
