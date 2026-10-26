---
schema_version: 2.7
id: therapy_intensity
name: Therapy Intensity
kind: predictor
predictor_type: clinical
status: draft
created_by: agent:ollama-extract-cli/gemma4:31b-it-q8_0
created_on: 2026-10-20
short_definition: The dosage of speech and language therapy, measured by hours per week, total hours,
  or duration in weeks.
assessment:
- Hours per week
- Total hours of therapy
- Duration of therapy (weeks)
units: hours / weeks
typical_range: 2 to 10 hours/week; 40 to 120 total hours
direction_of_severity: not_applicable
findings:
- id: f1
  target: severity_metric
  target_kind: predictor
  claim: A higher number of therapy hours provided per week is associated with greater improvement on
    the PICA.
  direction: likely
  relationship: correlational
  citation: '@Bhogal2003'
  method: meta-analysis
  design: meta-analysis
  strength: moderate
  evidence_quality: meta-analysis
  instrument: PICA
  sample:
    n: 864
    population: stroke survivors suffering from aphasia
    time_post_onset: not_reported
    age_range: not_reported
    handedness: not_reported
    language: English
    phase: not_reported
    cohort: not_reported
  statistics:
    threshold: p=0.001
    effect_size: r=0.957
  confounders_controlled: []
  confounders_not_controlled:
  - lesion volume
  - age
  - baseline severity
  author_limitations:
  - Only 3 studies were rated to be of 'good' quality (PEDro score=6), whereas the rest were either of
    fair quality or did not qualify for a PEDro rating.
  - Many of the studies were under-powered with small sample sizes.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 991
    confidence: high
    flags:
    - correlation is performed at the study level (n=9 studies) rather than the patient level (n=864)
  source_passages:
  - section: Results
    page: 5
    quote: the hours of therapy provided in a week was significantly correlated to greater improvement
      on the PICA (r=0.957, P=0.001, n=9)
    supports: claim
  - section: Results
    page: 2
    quote: Ten studies investigating the SLT for stroke patients suffering from aphasia met criteria...
      These 10 studies represented 864 individual patients.
    supports: sample
  - section: Methods
    page: 1
    quote: Pearson correlation was used to assess the relationship between changes in mean scores of outcome
      measures and intensity of therapy.
    supports: method
  - section: Discussion
    page: 5
    quote: Only 3 studies were rated to be of 'good' quality (PEDro score=6), whereas the rest were either
      of fair quality (PEDro scores=4 and 5) or did not qualify for a PEDro rating
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
  target: severity_metric
  target_kind: predictor
  claim: A greater total number of therapy hours is associated with greater improvement on the PICA.
  direction: likely
  relationship: correlational
  citation: '@Bhogal2003'
  method: meta-analysis
  design: meta-analysis
  strength: moderate
  evidence_quality: meta-analysis
  instrument: PICA
  sample:
    n: 864
    population: stroke survivors suffering from aphasia
    time_post_onset: not_reported
    age_range: not_reported
    handedness: not_reported
    language: English
    phase: not_reported
    cohort: not_reported
  statistics:
    threshold: p=0.0001
    effect_size: r=0.958
  confounders_controlled: []
  confounders_not_controlled:
  - lesion volume
  - age
  - baseline severity
  author_limitations:
  - Only 3 studies were rated to be of 'good' quality (PEDro score=6), whereas the rest were either of
    fair quality or did not qualify for a PEDro rating.
  - Many of the studies were under-powered with small sample sizes.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 991
    confidence: high
    flags:
    - correlation is performed at the study level (n=9 studies) rather than the patient level (n=864)
  source_passages:
  - section: Results
    page: 1
    quote: Total hours of therapy were significantly correlated with mean change in PICA (r=0.958, P=0.0001,
      n=9)
    supports: claim
  - section: Results
    page: 2
    quote: Ten studies investigating the SLT for stroke patients suffering from aphasia met criteria...
      These 10 studies represented 864 individual patients.
    supports: sample
  - section: Methods
    page: 1
    quote: Pearson correlation was used to assess the relationship between changes in mean scores of outcome
      measures and intensity of therapy.
    supports: method
  - section: Discussion
    page: 5
    quote: Many of the studies were under-powered with small sample sizes.
    supports: limitation
  region_definition:
    kind: not_reported
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
- id: f3
  target: severity_metric
  target_kind: predictor
  claim: A greater total number of therapy hours is associated with greater improvement on the Token Test.
  direction: likely
  relationship: correlational
  citation: '@Bhogal2003'
  method: meta-analysis
  design: meta-analysis
  strength: moderate
  evidence_quality: meta-analysis
  instrument: Token Test
  sample:
    n: 864
    population: stroke survivors suffering from aphasia
    time_post_onset: not_reported
    age_range: not_reported
    handedness: not_reported
    language: English
    phase: not_reported
    cohort: not_reported
  statistics:
    threshold: p=0.0001
    effect_size: r=0.963
  confounders_controlled: []
  confounders_not_controlled:
  - lesion volume
  - age
  - baseline severity
  author_limitations:
  - Only 3 studies were rated to be of 'good' quality (PEDro score=6), whereas the rest were either of
    fair quality or did not qualify for a PEDro rating.
  - Many of the studies were under-powered with small sample sizes.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 991
    confidence: high
    flags:
    - correlation is performed at the study level (n=7 studies) rather than the patient level (n=864)
  source_passages:
  - section: Results
    page: 1
    quote: Total hours of therapy were significantly correlated with mean change in... Token Test scores
      (r=0.963, P=0.0001, n=7)
    supports: claim
  - section: Results
    page: 2
    quote: Ten studies investigating the SLT for stroke patients suffering from aphasia met criteria...
      These 10 studies represented 864 individual patients.
    supports: sample
  - section: Methods
    page: 1
    quote: Pearson correlation was used to assess the relationship between changes in mean scores of outcome
      measures and intensity of therapy.
    supports: method
  - section: Discussion
    page: 5
    quote: Only 3 studies were rated to be of 'good' quality (PEDro score=6), whereas the rest were either
      of fair quality... or did not qualify for a PEDro rating
    supports: limitation
  region_definition:
    kind: not_reported
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
- id: f4
  target: severity_metric
  target_kind: predictor
  claim: A longer total length of therapy (in weeks) is inversely correlated with improvement on the PICA.
  direction: unlikely
  relationship: correlational
  citation: '@Bhogal2003'
  method: meta-analysis
  design: meta-analysis
  strength: moderate
  evidence_quality: meta-analysis
  instrument: PICA
  sample:
    n: 864
    population: stroke survivors suffering from aphasia
    time_post_onset: not_reported
    age_range: not_reported
    handedness: not_reported
    language: English
    phase: not_reported
    cohort: not_reported
  statistics:
    threshold: p=0.0001
    effect_size: r=-0.948
  confounders_controlled: []
  confounders_not_controlled:
  - lesion volume
  - age
  - baseline severity
  author_limitations:
  - Only 3 studies were rated to be of 'good' quality (PEDro score=6), whereas the rest were either of
    fair quality or did not qualify for a PEDro rating.
  - Many of the studies were under-powered with small sample sizes.
  provenance:
    extracted_by: agent
    extracted_on: 2026-01-01
    paper_section: Results, page 991
    confidence: high
    flags:
    - correlation is performed at the study level (n=9 studies) rather than the patient level (n=864)
  source_passages:
  - section: Results
    page: 1
    quote: total length of therapy was significantly inversely correlated with mean change in PICA scores
      (r=-0.948, P=0.0001, n=9)
    supports: claim
  - section: Results
    page: 2
    quote: Ten studies investigating the SLT for stroke patients suffering from aphasia met criteria...
      These 10 studies represented 864 individual patients.
    supports: sample
  - section: Methods
    page: 1
    quote: Pearson correlation was used to assess the relationship between changes in mean scores of outcome
      measures and intensity of therapy.
    supports: method
  - section: Discussion
    page: 5
    quote: Many of the studies were under-powered with small sample sizes.
    supports: limitation
  region_definition:
    kind: not_reported
  filled:
    by: model:gemma4:31b-it-q8_0
    date: '2026-10-26'
    tool: backfill.py
    fields:
    - cohort
---
This meta-analysis of 10 clinical trials demonstrates that higher therapy intensity (measured by hours per week and total hours) is strongly correlated with greater improvement in aphasia recovery as measured by the PICA and Token Test, while longer overall duration in weeks is inversely correlated with improvement.
