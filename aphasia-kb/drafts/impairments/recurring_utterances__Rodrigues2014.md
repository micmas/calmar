---
schema_version: 2.6
id: recurring_utterances
name: "Recurring Utterances"
kind: impairment
short_definition: "The production of a neologism, word, or phrase not related to the communication context and produced against the patient's presumed intention."
assessment: ["BAAL", "Token test"]
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-23

findings:
  - id: f1
    target: severity_metric
    target_kind: predictor
    claim: "Patients with recurring utterances exhibit significantly lower overall language severity (AQ), naming, and repetition scores compared to matched aphasic controls."
    direction: likely
    relationship: causal
    citation: "@Rodrigues2014"
    method: behavioral_only
    design: cross-sectional
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 19
      population: "aphasia patients with recurring utterances"
      time_post_onset: "M = 3.15 months; range 2-5 months"
      phase: early_subacute
      age_range: "47-78 years"
      handedness: "right-handed"
      language: "Portuguese"
    statistics:
      threshold: "p <= .01"
      effect_size: "AQ (U = 209.00, p = .000), naming (U = 174.0, p = .002), repetition (U = 196.0, p = .000)"
    confounders_controlled: ["age", "gender", "time since onset", "handedness", "hours of therapy", "aphasia classification"]
    confounders_not_controlled: []
    region_definition:
      kind: not_reported
      description: "behavioral comparison between RU and non-RU groups"
    author_limitations:
      - "Small number of milder forms of aphasia due to hospitalization bias."
      - "No follow-up performed after discharge."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 6"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 6
        quote: "Patients with RU scored considerably less than the control group in aphasia quotient (U = 209.00; p = .000), in naming task (U = 174.0; p = .002) and in word repetition (U = 196.0; p = .000)."
        supports: claim
      - section: "Methods"
        page: 4
        quote: "Inclusion criteria were as follows: aphasia resulting from a single left stroke, absence of psychiatric or other neurological diseases previous to stroke, living at home before stroke and right-handedness."
        supports: sample
      - section: "Results"
        page: 5
        quote: "Time post-stroke onset was similar in all patients (M = 3.15 months; range 2-5 months)"
        supports: sample
      - section: "Methods"
        page: 4
        quote: "A significance level of p <= .01 was adopted."
        supports: statistics
      - section: "Discussion"
        page: 11
        quote: "Some limitations of the current study included a relatively small number of milder forms of aphasia because the most severe cases are more in need of hospitalisation."
        supports: limitation

  - id: f2
    target: severity_metric
    target_kind: predictor
    claim: "Patients with recurring utterances show significant recovery in oral comprehension and Token test scores over time, but maintain severe deficits in fluency, naming, and repetition."
    direction: likely
    relationship: causal
    citation: "@Rodrigues2014"
    method: behavioral_only
    design: longitudinal
    strength: moderate
    evidence_quality: cohort
    sample:
      n: 19
      population: "aphasia patients with recurring utterances"
      time_post_onset: "initial 2-5 months; follow-up 3 months later"
      phase: longitudinal
      age_range: "47-78 years"
      handedness: "right-handed"
      language: "Portuguese"
    statistics:
      threshold: "p <= .01"
      effect_size: "BAAL comprehension (U = 140.0, p = .001), Token test (U = 96.0, p = .001)"
    confounders_controlled: []
    confounders_not_controlled: []
    region_definition:
      kind: not_reported
      description: "longitudinal behavioral tracking"
    author_limitations:
      - "Absence of formal neuropsychology assessments to evaluate cognitive control."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 8"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 8
        quote: "the differences between the two assessment moments, for RU patients, were significant for BAAL comprehension task (U = 140.0; p = .001) and Token test scores (U = 96.0; p = .001)."
        supports: claim
      - section: "Results"
        page: 8
        quote: "Despite this recovery, improvement in fluency was extremely limited or even non-existent."
        supports: claim
      - section: "Discussion"
        page: 10
        quote: "We found some recovery of verbal comprehension in our RU sample, but it was not possible to relate it to attentional improvement or some establishment of inhibitory control due to the absence of formal neuropsychology assessments."
        supports: limitation
---
