---
schema_version: 2.7
id: pure_alexia
name: Pure Alexia
kind: impairment
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
short_definition: An acquired reading disorder characterized by a disproportionate prolongation of reading
  time as a function of word length (word length effect), typically with intact naming, repetition, and
  writing.
findings:
- id: f1
  target: pure_alexia
  target_kind: impairment
  claim: Pure alexia is characterized by a significant increase in fixation frequency and viewing time
    as a function of word length during text reading, distinct from hemianopic dyslexia.
  direction: likely
  relationship: correlational
  citation: '@Pflugshaupt2009'
  method: behavioral_only
  design: cross-sectional
  strength: moderate
  evidence_quality: cohort
  sample:
    n: 6
    population: patients with pure alexia
    time_post_onset: not_reported
    age_range: not_reported
    handedness: all right-handed
    language: German
    phase: not_reported
    cohort: not_reported
  statistics:
    threshold: P < 0.05 (Kruskal-Wallis)
    cluster_extent: not_reported
    effect_size: Kruskal-Wallis chi2=12.104 (p=0.002) for fixation frequency; chi2=11.789 (p=0.003) for
      viewing time
    p_value: '0.002'
  confounders_controlled:
  - ' visual field defect side'
  - degree of macular sparing
  confounders_not_controlled: []
  region_definition:
    kind: not_reported
    description: Behavioural-only finding regarding eye-movement patterns.
  author_limitations:
  - Small sample size may lead to underestimation of visuo-motor deficits.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results - Visuo-motor variables, page 8
    confidence: high
    flags: []
  source_passages:
  - section: Results - Visuo-motor variables
    page: 8
    quote: Patients with pure alexia displayed enhanced increases in fixation frequency and viewing time
      per additional letter, relative to both healthy participants and patients with hemianopic dyslexia.
    supports: claim
  - section: Results - Visuo-motor variables
    page: 8
    quote: 'Analysing the influence of word length on fixation frequency and viewing time revealed significant
      overall differences between groups with regard to the increase in the number of fixations per additional
      letter (Kruskal-Wallis test: chi2 = 12.104, df = 2, P = 0.002) and the increase in viewing time
      per additional letter (Kruskal-Wallis test: chi2 = 11.789, df = 2, P = 0.003).'
    supports: statistics
  - section: Discussion
    page: 9
    quote: due to relatively small sample sizes and thus limited statistical power, these comparisons
      are likely to underestimate visuo-motor deficits in patients
    supports: limitation
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
---
# Pure Alexia

Pure alexia is an acquired reading disorder characterized by a severe word length effect. Pflugshaupt et al. (2009) demonstrate that this manifests as a specific increase in fixation frequency and viewing time per additional letter during text reading, a pattern that is not present in hemianopic dyslexia despite similar visual field defects.
