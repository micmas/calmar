---
schema_version: 2
id: ho-cort_44
name: Inferior Frontal Gyrus, pars opercularis
kind: atlas
status: approved
created_by: agent:claude-opus-4-7
created_on: 2026-04-29
atlas: HarvardOxford-cort-maxprob-thr25-2mm
atlas_index: 44
hemisphere: left
aliases:
- Broca's area (posterior)
- BA 44
- IFG opercularis
- left pars opercularis
networks:
- dorsal_language
tracts_adjacent:
- arcuate_fasciculus
findings:
- id: f1
  target: fluency
  target_kind: impairment
  claim: Damage to the left inferior frontal gyrus pars opercularis is associated
    with reduced speech fluency in chronic stroke.
  direction: likely
  citation: '@Fridriksson2018'
  method: LSM
  design: cross-sectional
  imaging: multimodal
  sample:
    n: 132
    population: chronic left-hemisphere stroke survivors with aphasia
    time_post_onset: '>=6 months post-onset (chronic)'
    age_range: not_reported
    handedness: premorbid right-handed
    language: English-speaking
    recruitment: recruited from a larger longitudinal aphasia cohort at the University
      of South Carolina.
    inclusion_criteria: single left-hemisphere ischemic stroke; no other neurological
      diagnosis; native English speaker.
    exclusion_criteria: bilateral lesions; non-ischemic etiology; contraindications
      to MRI.
  statistics:
    threshold: permutation-based whole-brain correction, p<.05
    cluster_extent: null
    effect_size: not_reported
    ci_95: not_reported
    p_value: not_reported
  confounders_controlled:
  - lesion volume
  confounders_not_controlled:
  - time post-onset (range only)
  - education / premorbid IQ
  region_definition:
    kind: data_driven_cluster
    description: Voxel-wise lesion-symptom mapping cluster maximally associated with
      the speech-fluency factor; the cluster centered on left posterior inferior frontal
      gyrus.
  replications:
  - '@Mirman2015'
  contradictions: []
  author_limitations:
  - Cross-sectional design — cannot infer recovery trajectory.
  - Lesion-load sampling biased against deep subcortical-only strokes.
  - Behavioral factors derived from PCA may not map cleanly onto classical aphasia
    subtypes.
  evidence_quality: cohort
  strength: strong
  provenance:
    extracted_by: human:michele
    extracted_on: 2026-04-29
    paper_section: Results, Figure 2 + Table 2
    confidence: medium
    flags:
    - exact effect size not reported in this paper for this cluster — verify against
      supplementary materials
    - atlas_index 44 was assumed from HarvardOxford labels file; verify against your
      local install
  source_passages:
  - section: Results
    page: 1434
    quote: '[PLACEHOLDER — paste the exact sentence(s) from the paper supporting the
      claim once you have the PDF in front of you. The agent should fill this when
      it has access to the source.]'
source: curated
last_reviewed: 2026-04-29
notes: "This is the canonical worked example of a v2 region entry. It demonstrates:\n\
  \  1. Honest \"not_reported\" markers where the paper doesn't say.\n  2. A `provenance.flags`\
  \ list capturing the extractor's uncertainties.\n  3. A `confidence: medium` rather\
  \ than `high` because two flags exist.\n  4. `strength: strong` (extractor's read)\
  \ but `confidence: medium`\n     (extractor's confidence in the *extraction*) —\
  \ these are independent.\n  5. Author-acknowledged limitations transcribed from\
  \ the paper itself.\n  6. A `source_passages` placeholder showing where the exact\
  \ quote goes."
reviewer: michele
reviewed_on: '2026-04-29'
---
# Inferior Frontal Gyrus, pars opercularis (Broca's area, posterior)

## How to read this entry

This entry is a **worked example** under schema v2. Every field in the
frontmatter is a deliberate extraction decision — see `provenance.flags`
for what's uncertain and `author_limitations` for what the original paper
itself flagged.

Two things to notice that v1 did not capture:

- The agent's confidence in the *extraction* (`provenance.confidence`) is
  separate from the agent's read of the *claim's strength* (`strength`).
  A claim can be strongly supported by a paper that the agent has only read
  partially — that's `strength: strong, confidence: medium`.
- `confounders_not_controlled` makes the gaps in the original analysis
  visible to a downstream interpreter. A second-line interpreter can then
  weight findings by what was vs wasn't controlled for.

## Anatomical context

Posterior third of the left inferior frontal gyrus, corresponding roughly
to Brodmann area 44. Sits anterior to ventral premotor cortex and lateral
to the insula. Densely connected to posterior temporal cortex via the
arcuate fasciculus.

## Lesion-symptom evidence

See the finding above (`f1`). The Fridriksson 2018 paper uses voxel-wise
LSM and identifies a cluster centered on posterior IFG as one of two
maximally-associated peaks for a "speech-fluency" behavioral factor
derived by PCA over the WAB.

## Therapy implications

Therapy-related findings should be added as additional `findings` entries
(e.g., `f2`, `f3`) referencing therapy ids and citing therapy-specific
papers. They were not extracted from Fridriksson 2018 and so are absent
here.

## What's *not* in this entry yet

- An effect size for the cluster (the paper reports the t-statistic in
  Figure 2 but not, in the main text, an effect size that's portable to
  other studies). Flagged in `provenance.flags`.
- The verbatim quote in `source_passages` — placeholder pending PDF
  access.
