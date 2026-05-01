# Extraction log

A running, append-only audit log of every agent extraction run and every
human review action. Every entry is one line, pipe-separated, in this
format:

```
<ISO date> | <ACTION> | <citation> | <entry id> | <metadata...>
```

Actions:

- `EXTRACTED` — agent wrote one or more drafts from a paper.
- `APPROVED`  — human moved a draft to the canonical folder.
- `REJECTED`  — human marked a draft as rejected (it stays in `drafts/`
                with `status: rejected` for the audit trail).
- `EDITED`    — human manually edited a canonical entry without going
                through `promote.py` (please add this manually if so).

This log is appended to automatically by `promote.py`. The agent should
add an `EXTRACTED` line for every run.

---

<!-- New entries are appended below this line -->
2026-04-30 | EXTRACTED | @Yourganov2015Predicting | brocas_aphasia, wernickes_aphasia, conduction_aphasia, global_aphasia, anomic_aphasia | 5 drafts (impairment-anchored) | 9 findings | confidence: high (4) / medium (1, Wernicke's small n) | annotator: 20/36 quotes placed (16 missed due to Unicode/line-break artifacts in PDF text extraction) | agent: claude-opus-4-7
2026-05-01 | EXTRACTED | @Alyahya2018NounVerb | phonological_production, semantics, fluency, phonological_recognition, executive_functions, lesion_volume | 6 drafts (5 impairment-anchored PCA-factor drafts + 1 predictor-anchored lesion_volume draft) | 24 findings | confidence: high (all) | flags: many target_ids do not yet exist as canonical region entries (anterior/posterior arcuate, angular gyrus, parietal operculum, posterior supramarginal gyrus, ILF, anterior MTG, temporal pole, superior lateral occipital cortex, precuneus, central opercular cortex, pre-central gyrus, Heschl's gyrus, planum temporale, posterior STG, superior frontal gyrus, paracingulate gyrus, supplementary motor area); method 'VBCM' coded as VLSM throughout (controlled-vocab limitation); fluency findings flagged as lesion-volume-confounded; semantics findings flagged for partial cluster shrinkage under lesion-volume covariate | agent: claude-opus-4-7
2026-05-01 | EXTRACTED | @Barbieri2023 | treatment_of_underlying_forms, typicality_semantic_feature_analysis, spell_study_spell | 3 drafts (therapy-anchored) | 7 findings | confidence: high (all) | flags: target_ids for impairments (agrammatism, anomia, dysgraphia, sentence_comprehension, sentence_production) and right-hemisphere regions (right_anterior_middle_temporal_gyrus, right_anterior_superior_temporal_gyrus) do not yet exist as canonical entries; behavioural-efficacy findings coded as method=clinical_RCT; fMRI-activation findings include enantiomorphic-replacement preprocessing; spell-study-spell f2 has unexpected RH upregulation without behavioral coupling, interpreted post-hoc as phonological-discrimination side effect; sentence-treatment f3 (brain-behavior coupling) is the headline finding linking RH activation change to verb comprehension improvement | agent: claude-opus-4-7
2026-05-01 | RE-EXTRACTED | @Yourganov2015Predicting | brocas_aphasia, conduction_aphasia, wernickes_aphasia, global_aphasia, anomic_aphasia | 5 drafts (impairment-anchored, refresh of 2026-04-30 extraction under v2.4 conventions) | 25 findings (Broca's 7, conduction 3, Wernicke's 7, global 8, anomic 0 null) | confidence: high (Broca's, conduction, global) / medium (Wernicke's, n=7) | conventions applied: hemisphere-prefixed target IDs (left_*); cross-paper cohort-overlap flag pointing to @Fridriksson2018 on every finding (shared USC registry); legacy ho-cort_44 retained for the IFG pars opercularis target since the canonical entry already exists; no per-finding flags about non-existent target IDs (forward-looking convention); anomic_aphasia uses the empty-findings null pattern (paper specifically reports no regions reach Z>1) | annotator: 131/139 quotes placed; 8 missed (line-break artifacts in PDF text) | agent: claude-opus-4-7
2026-05-01 | EXTRACTED | @Fridriksson2018 | form_to_articulation, form_to_meaning | 2 drafts (impairment-anchored; first proper extraction — the canonical regions/ho-cort_44.md previously cited this paper with [PLACEHOLDER] source passages from the worked example) | 12 findings (form_to_articulation 5: pars opercularis, premotor, MFG, anterior SMG, precentral; form_to_meaning 7: posterior MTG, posterior STG, uncinate, posterior SMG, angular, pars orbitalis, anterior MTG) | confidence: high (all) | method: VLSM (the paper's actual analysis is VLSM-then-PCA: 71 univariate VLSMs are stacked into a PCA, where Component 2's positive vs negative loadings define the dual-stream split) | sample n=138 chronic LH stroke patients from USC Aphasia Lab archival database, ≥6 months post-stroke; cohort substantially overlaps with @Yourganov2015Predicting (cohort-overlap flag on every finding) | conventions applied: hemisphere-prefixed target IDs (left_*); legacy ho-cort_44 retained; no per-finding non-existent-target flags; cohort-overlap flag pattern; flag on form_to_articulation:f1 noting that the canonical ho-cort_44.md placeholder source passages should be replaced when promote.py runs | DOI corrected in citations.md (was 10.1073/pnas.1714922115; actual is 10.1073/pnas.1614038114 per the PDF) | agent: claude-opus-4-7
