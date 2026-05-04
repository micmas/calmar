---
schema_version: 2
id: left_anterior_arcuate_fasciculus
name: Left anterior arcuate fasciculus
kind: tract
status: approved
created_by: human:michele
created_on: 2026-05-04
atlas: natbrainlab white-matter atlas (Catani et al. 2012)
hemisphere: left
aliases:
- anterior segment of arcuate fasciculus
- arcuate-direct (dual-stream)
- long anterior segment
- left_frontal_aslant_tract
- frontal_aslant_tract
- FAT
networks:
- dorsal_language
findings: []
source: curated
last_reviewed: '2026-05-04'
notes: |
  Region stub created on 2026-05-04 to support promotion of
  drafts/impairments/fluency__Alyahya2018NounVerb.md:f1.

  Aliases include the frontal aslant tract (FAT). The natbrainlab
  white-matter atlas (Catani et al. 2012) does not resolve FAT from
  the anterior arcuate, so studies that use natbrainlab labels for
  the "anterior arcuate" cluster may actually be picking up FAT
  fibres. Discussion in Alyahya et al. 2018 (page 228), Catani 2013,
  and Rojkova et al. 2015 argue the relevant tract for speech
  fluency is FAT rather than arcuate-proper.

  When extracting from a paper that uses a higher-resolution tract
  atlas separating these two systems (e.g., one based on diffusion
  tractography that distinguishes FAT from arcuate segments), keep
  the FAT alias here so cross-paper findings can still be merged
  under a single canonical region id. If the field eventually
  converges on FAT-as-distinct-tract, this entry can be split into
  two (left_anterior_arcuate_fasciculus + left_frontal_aslant_tract)
  and the alias removed.
reviewer: michele
reviewed_on: '2026-05-04'
---
# Left anterior arcuate fasciculus

## Anatomical context

Anterior segment of the left arcuate fasciculus, sometimes referred
to as the "long anterior segment" or as "arcuate-direct" in
dual-stream language models. Connects ventral premotor / inferior
frontal cortex to inferior parietal regions.

The natbrainlab white-matter atlas (Catani et al. 2012) used in many
chronic-aphasia studies does not separate this tract from the
frontal aslant tract (FAT) (Catani 2013; Rojkova et al. 2015).
Studies that report findings in "anterior arcuate" using natbrainlab
labels may be identifying either tract — see the `aliases:` list
above.

## Lesion-symptom evidence

No findings extracted yet. Findings will appear in the `findings:`
list in the frontmatter as relevant drafts are promoted into this
file.
