# Citations

Bibliography for `@Key` references that appear in any entry's frontmatter.
Add a new block below whenever you cite a new paper. Keep the `## @Key`
header exactly as it is referenced from frontmatter (case-sensitive).

## Status tags

Each entry below carries a status tag indicating how it's used:

  - **[extracted]** — The paper has been read and findings have been
    written into `drafts/` or canonical entries (i.e., at least one
    finding has `citation: "@Key"`). The paper's PDF should also be
    in `papers/` with a corresponding `_annotated.pdf`.
  - **[cited]** — The paper is referenced as a replication or
    contradiction by an extracted finding, but it has not itself been
    read or extracted. Useful as a forward pointer.
  - **[seed]** — Starter reference picked for canonical status in the
    aphasia / aphasia-therapy literature, not yet cited by any
    finding. Available for future extractions to use without having
    to re-add to this file.

The status of each entry is shown in the `## @Key  [tag]` header.

---

## Extracted papers

> Findings have been written from these papers. The annotated PDFs
> are in `papers/`. Update the status tag to `[extracted]` whenever a
> new extraction is performed against an entry.

## @Fridriksson2018  [extracted]
Fridriksson J, Yourganov G, Bonilha L, Basilakos A, Den Ouden DB, Rorden C.
Revealing the dual streams of speech processing.
*Proc Natl Acad Sci USA*. 2018;115(7):1432–1437.
doi:10.1073/pnas.1614038114

> Properly extracted 2026-05-01 with two impairment-anchored drafts
> (`form_to_articulation` + `form_to_meaning`) covering 12 findings
> from the VLSM-then-PCA dual-stream analysis on n=138 chronic LH
> stroke patients (USC Aphasia Lab archival database). The paper's
> primary contribution is the data-driven empirical localization of
> the dorsal speech-processing stream (Component 2 negative loadings:
> pars opercularis, premotor, MFG, anterior SMG, precentral) and the
> ventral stream (Component 2 positive loadings: posterior MTG/STG,
> uncinate fasciculus, posterior SMG, angular gyrus, pars orbitalis,
> anterior MTG). Cohort substantially overlaps with
> @Yourganov2015Predicting (same lab, n=98).
>
> Also referenced extensively (33 `replications:` links) across the
> Yourganov, Alyahya, and Barbieri drafts. The canonical
> `regions/ho-cort_44.md` entry already cites this paper but with
> `[PLACEHOLDER]` source passages from the original worked example;
> when promote.py runs, those placeholders should be replaced or
> superseded by the real source_passages from
> `drafts/impairments/form_to_articulation__Fridriksson2018.md:f1`.

## @Yourganov2015Predicting  [extracted]
Yourganov G, Smith KG, Fridriksson J, Rorden C.
Predicting aphasia type from brain damage measured with structural MRI.
*Cortex*. 2015;73:203–215.
doi:10.1016/j.cortex.2015.09.005

> Re-extracted 2026-05-01 under v2.4 conventions. 5 impairment-anchored
> drafts (Broca's, conduction, Wernicke's, global, anomic) covering
> 25 findings via MLPA on 98 chronic LH stroke patients. Cohort
> overlaps with @Fridriksson2018.

## @Alyahya2018NounVerb  [extracted]
Alyahya RSW, Halai AD, Conroy P, Lambon Ralph MA.
Noun and verb processing in aphasia: Behavioural profiles and neural correlates.
*NeuroImage: Clinical*. 2018;18:215–230.
doi:10.1016/j.nicl.2018.01.023

> 6 drafts (5 PCA-factor impairment-anchored: phonological_production,
> semantics, fluency, phonological_recognition, executive_functions;
> + lesion_volume predictor draft) covering 25 findings via VBCM on
> 48 chronic post-stroke aphasia patients (Manchester / NARU cohort).

## @Barbieri2023  [extracted]
Barbieri E, Thompson CK, Higgins J, Caplan D, Kiran S, Rapp B, Parrish T.
Treatment-induced neural reorganization in aphasia is language-domain specific:
Evidence from a large-scale fMRI study.
*Cortex*. 2023;159:75–100.
doi:10.1016/j.cortex.2022.11.008

> 3 therapy-anchored drafts (treatment_of_underlying_forms,
> typicality_semantic_feature_analysis, spell_study_spell) covering
> 8 findings on 58 chronic stroke aphasia patients across 3 sites
> (NU + BU + JHU; trial NCT01927302). Cohort overlaps with Barbieri
> et al. 2019, Gilmore et al. 2019, Johnson et al. 2019, Purcell et
> al. 2019, and Wiley & Rapp 2019.

---

## Referenced papers (cited but not extracted)

> These papers are referenced by extracted findings via `replications:`
> or `contradictions:` lists. They have not themselves been read or
> extracted. Promote a paper to `[extracted]` status by reading its
> PDF and writing draft findings against it.

## @Mirman2015  [cited]
Mirman D, Chen Q, Zhang Y, Wang Z, Faseyitan OK, Coslett HB, Schwartz MF.
Neural organization of spoken language revealed by lesion-symptom mapping.
*Nat Commun*. 2015;6:6762.
doi:10.1038/ncomms7762

> Referenced as a replication for several findings (Heschl's gyrus,
> planum temporale, anterior MTG, temporal pole). Worth extracting —
> a large-cohort (n=99) VLSM study on the Philadelphia aphasia
> registry that maps multiple language components.

## @Schlaug2008  [cited]
Schlaug G, Marchina S, Norton A.
From singing to speaking: why singing may lead to recovery of expressive
language function in patients with Broca's aphasia.
*Music Percept*. 2008;25(4):315–323.
doi:10.1525/mp.2008.25.4.315

> Referenced as a replication for the TUF behavioural-efficacy
> finding (sentence-level treatment improves language production in
> chronic agrammatic aphasia). MIT (Melodic Intonation Therapy) is a
> distinct therapy from TUF — would yield its own therapy-anchored
> draft if extracted.

## @Boyle2004  [cited]
Boyle M.
Semantic feature analysis treatment for anomia in two fluent aphasia syndromes.
*Am J Speech Lang Pathol*. 2004;13(3):236–249.
doi:10.1044/1058-0360(2004/025)

> Original Semantic Feature Analysis paper, referenced as a
> replication for the typicality-based SFA finding (Barbieri 2023).
> Would extract as the parent therapy entry for SFA-family treatments.

## @Pulvermuller2001  [cited]
Pulvermüller F, Neininger B, Elbert T, Mohr B, Rockstroh B, Koebbel P, Taub E.
Constraint-induced therapy of chronic aphasia after stroke.
*Stroke*. 2001;32(7):1621–1626.
doi:10.1161/01.str.32.7.1621

> Referenced as a replication for the TUF behavioural-efficacy
> finding. Constraint-Induced Aphasia Therapy (CIAT) is its own
> therapy class — distinct from TUF — and would warrant its own
> therapy-anchored draft if extracted.

## @Saur2008  [cited]
Saur D, Kreher BW, Schnell S, Kümmerer D, Kellmeyer P, Vry M-S, et al.
Ventral and dorsal pathways for language.
*Proc Natl Acad Sci USA*. 2008;105(46):18035–18040.
doi:10.1073/pnas.0805234105

> Foundational dual-stream paper for language pathways. Referenced
> as a replication for posterior arcuate / phonological production
> and ILF / semantic findings. Worth extracting as the canonical
> reference for the dorsal-vs-ventral language-pathway distinction.

## @Marchina2011  [cited]
Marchina S, Zhu LL, Norton A, Zipse L, Wan CY, Schlaug G.
Impairment of speech production predicted by lesion load of the left arcuate
fasciculus.
*Stroke*. 2011;42(8):2251–2256.
doi:10.1161/STROKEAHA.110.606103

> Referenced as a replication for arcuate-fasciculus / fluency
> findings. Tractography study of arcuate lesion load → speech
> production deficits.

## @Geschwind1965  [cited]
Geschwind N.
Disconnexion syndromes in animals and man.
*Brain*. 1965;88(2):237–294.
doi:10.1093/brain/88.2.237

> Historical reference for the disconnection model of conduction
> aphasia (arcuate fasciculus → repetition deficit). Cited from the
> Yourganov 2015 conduction_aphasia draft. Not extractable in the
> usual sense (theoretical paper without primary patient data per
> EXTRACTION_SKILL §2 refusal rule), but legitimately cited as
> historical replication.

---

## Seed references (not yet cited)

> Hand-picked starter references for the aphasia literature, not yet
> cited by any finding. Available for future extractions to use.
> If they remain uncited indefinitely, consider removing.

## @Hillis2007  [seed]
Hillis AE.
Aphasia: progress in the last quarter of a century.
*Neurology*. 2007;69(2):200–213.
doi:10.1212/01.wnl.0000265600.69385.6f

> Comprehensive review. Cited internally by Yourganov 2015 and
> Barbieri 2023 papers but not yet referenced from any KB finding.

## @Bonilha2014  [seed]
Bonilha L, Rorden C, Fridriksson J.
Assessing the clinical effect of residual cortical disconnection after ischemic
strokes.
*Stroke*. 2014;45(4):988–993.
doi:10.1161/STROKEAHA.113.004137

> Disconnectome / residual-connectivity study. Could be extracted as
> a `disconnectome` method paper (the controlled vocabulary already
> includes `disconnectome` as a method value).
