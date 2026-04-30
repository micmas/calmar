---
id: ho-cort_45
name: "Inferior Frontal Gyrus, pars triangularis"
kind: atlas
atlas: HarvardOxford-cort-maxprob-thr25-2mm
atlas_index: 45
hemisphere: left
aliases:
  - "Broca's area (anterior)"
  - "BA 45"
  - "IFG triangularis"
  - "left pars triangularis"
networks: [dorsal_language, ventral_language]
findings:
  - target: naming
    target_kind: impairment
    direction: likely
    strength: moderate
    evidence_quality: cohort
    citation: "@Mirman2015"
    notes: "Anterior IFG damage contributes to semantic naming errors."
  - target: fluency
    target_kind: impairment
    direction: likely
    strength: moderate
    evidence_quality: meta-analysis
    citation: "@Fridriksson2018"
    notes: "Less specific to fluency than pars opercularis but still contributes."
  - target: sfa
    target_kind: therapy
    direction: likely_responder
    strength: weak
    evidence_quality: cohort
    citation: "@Boyle2004"
    notes: "Patients with anomia of any aphasia subtype, including those with anterior IFG lesions, may benefit from SFA — evidence is broader than this region alone."
source: curated
last_reviewed: 2026-04-29
---

# Inferior Frontal Gyrus, pars triangularis (Broca's area, anterior)

## Anatomical context

Anterior third of the left IFG (BA 45), positioned between pars opercularis
posteriorly and pars orbitalis anteriorly. Implicated in semantic selection
and controlled retrieval of lexical information; participates in both the
dorsal phonological pathway and the ventral semantic pathway.

## Lesion-symptom evidence

Damage to BA 45 is more consistently associated with **semantic-level
selection difficulty** (e.g., choosing among competing word candidates) than
with the gross fluency loss seen in pars opercularis lesions. Naming errors
in this group are more likely to be semantically related substitutions
("cat" → "dog") than phonological distortions.

## Therapy implications

Semantic Feature Analysis (SFA) is a reasonable first-line therapy when
naming impairment is the dominant feature; see `therapies/sfa.md`. Evidence
for region-specific responsiveness is weaker than for impairment-specific
responsiveness — this finding is included as a candidate for clinician
review.
