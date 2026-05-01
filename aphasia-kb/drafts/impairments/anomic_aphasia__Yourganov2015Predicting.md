---
schema_version: 2.3
id: anomic_aphasia
name: "Anomic aphasia"
kind: impairment
status: draft
created_by: "agent:claude-opus-4-7"
created_on: 2026-05-01
short_definition: "The mildest aphasia syndrome, characterized predominantly by word-finding difficulty (anomia) with relatively preserved fluency, comprehension, and repetition. Often the residual stage that other aphasia types resolve into during recovery."
assessment:
  - "Western Aphasia Battery (WAB / WAB-R)"
  - "Boston Naming Test (BNT)"
  - "Philadelphia Naming Test (PNT)"

# NOTE: deliberately empty findings list — Yourganov 2015 reports a
# meaningful NULL result for this entry. The paper specifically tested
# whether brain regions could predict anomic aphasia and found that NO
# regions reached the predictive-relevance threshold of 1 across the
# cross-validation splits. This null finding is captured in the prose
# body and in the entry-level `notes` field rather than as
# `direction: no_effect` on a specific region (which would require an
# arbitrary target).
findings: []

source: agent_draft
last_reviewed: null
notes: |
  Re-extraction draft from Yourganov 2015. Anomic aphasia is a
  meaningful NULL result: the multivariate SVM classifier could
  distinguish anomic aphasia from other aphasia types with high
  accuracy in pairwise contrasts (e.g., 89% accuracy for anomic vs
  Broca's with the JHU atlas; Table 1) — but NO brain regions
  reached the predictive-relevance threshold (Z > 1) across the
  cross-validation splits.

  The authors interpret this as: anomic aphasia is reliably
  diagnosable behaviourally but does not have a stereotyped lesion
  signature. This is consistent with the clinical picture of anomic
  aphasia as a residual / heterogeneous category rather than a
  distinct anatomically-localized syndrome. Henseler et al. (2014)
  reported the same null in a VLSM study (cited by Yourganov 2015).

  Cohort: same n=98 chronic LH stroke USC cohort as the other
  Yourganov 2015 drafts; cohort overlaps with @Fridriksson2018 — flag
  for downstream double-counting risk when interpret_overlap()
  consolidates evidence about anomic aphasia.

  This entry uses the unconventional empty-findings pattern. The
  schema doesn't currently have a clean way to encode "no region
  reaches the predictive-relevance threshold" as a finding (which
  would require an arbitrary target). The prose-only encoding is
  the cleanest representation; reviewer should preserve this on
  promotion.
---

# Anomic aphasia

## Clinical definition

The mildest aphasia syndrome, characterized predominantly by
word-finding difficulty (anomia) with relatively preserved fluency,
single-word auditory comprehension, and repetition. Often the
residual stage that other aphasia types resolve into during recovery
(e.g., Broca's or conduction aphasia improving over months/years).
Diagnosed via the Western Aphasia Battery (WAB) when WAB scores fall
above thresholds for Broca's, Wernicke's, conduction, and global
aphasia but below the cutoff for "no aphasia."

## Lesion correlates (per Yourganov 2015)

**A meaningful null finding.** Yourganov 2015 specifically tested
whether the multivariate SVM classifier could identify lesion
locations predictive of anomic aphasia, and found that **no brain
regions reached the predictive-relevance threshold (Z > 1)** across
the cross-validation splits — despite the classifier being able to
distinguish anomic from other aphasia types with high accuracy in
pairwise contrasts (Table 1, page 22; e.g., 89% accuracy for anomic
vs Broca's with the JHU atlas).

Authors' interpretation: anomic aphasia is reliably diagnosable
behaviourally but does not have a stereotyped lesion signature. This
is consistent with the clinical picture of anomic aphasia as a
residual / heterogeneous category rather than a distinct
anatomically-localized syndrome.

This null finding has been replicated in the VLSM study by Henseler
et al. (2014), cited by Yourganov 2015.

## Implications

  - Anomic aphasia should not be expected to map to a specific lesion
    location in the LINDA pipeline's atlas-overlap reports.
  - Naming impairment (which IS lesion-mappable; see `naming.md` if
    one is created) is a more useful interpretive target than the
    syndrome label "anomic aphasia" when reasoning about
    lesion-symptom relationships.

## Source quote

Yourganov 2015, page 13: *"anomic aphasia, the least severe of
aphasia types, could be easily distinguished, but no brain areas
were found to be strongly predictive (a similar result was reported
in a voxel-based lesion symptoms mapping study of Henseler et al.,
2014)."*
