---
id: arcuate_fasciculus
name: "Arcuate fasciculus (left)"
kind: tract
hemisphere: left
aliases:
  - "AF"
  - "left arcuate"
  - "long segment of the SLF"
members:
  - ho-cort_44               # frontal terminations
  - ho-cort_45
  - ho-cort_22_posterior     # temporal terminations
  - ho-cort_supramarginal    # parietal/relay
networks: [dorsal_language]
findings:
  - target: repetition
    target_kind: impairment
    direction: likely
    strength: strong
    evidence_quality: cohort
    citation: "@Marchina2011"
    notes: "Arcuate fasciculus lesion load predicts speech-production impairment in stroke survivors."
  - target: fluency
    target_kind: impairment
    direction: likely
    strength: moderate
    evidence_quality: cohort
    citation: "@Marchina2011"
  - target: mit
    target_kind: therapy
    direction: likely_responder
    strength: moderate
    evidence_quality: cohort
    citation: "@Schlaug2008"
    notes: "Patients with relatively preserved right-hemisphere AF show greater MIT-related gains, consistent with a right-hemisphere compensation account."
source: curated
last_reviewed: 2026-04-29
notes: "Lesion overlap with a tract is more meaningful as 'percent of tract lesioned' than as a discrete region label; aphasia_kb.py treats tracts as soft regions."
---

# Arcuate fasciculus (left)

## Anatomical context

The principal long-range white-matter pathway of the dorsal language stream,
connecting posterior temporal cortex (pSTG), inferior parietal cortex (SMG),
and inferior frontal cortex (IFG). Often subdivided into long, anterior, and
posterior segments (Catani parcellation).

## Lesion-symptom evidence

Disruption of the arcuate fasciculus is consistently associated with
**repetition deficits** independent of cortical lesion location, supporting
the classic disconnection account of conduction aphasia. Quantitative
lesion-load metrics on the AF predict severity of speech-production deficits
beyond cortical lesion volume (Marchina 2011).

## Therapy implications

Right-hemisphere AF integrity is a positive prognostic indicator for MIT
response (Schlaug 2008). When the dominant-hemisphere AF is heavily damaged,
therapies that lean on right-hemisphere compensation (MIT, music-based
approaches) become more attractive than those that assume residual dorsal-
stream function.
