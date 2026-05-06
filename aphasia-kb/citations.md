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
> `regions/ho-cort_44.md` entry was emptied of its previous placeholder
> finding on 2026-05-02 (worked-example artifact) so that
> `drafts/impairments/form_to_articulation__Fridriksson2018.md:f1`
> can be promoted into it as the new `f1`.

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

## @Mirman2015  [extracted]
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

## @Saur2008  [extracted]
Saur D, Kreher BW, Schnell S, Kümmerer D, Kellmeyer P, Vry M-S, et al.
Ventral and dorsal pathways for language.
*Proc Natl Acad Sci USA*. 2008;105(46):18035–18040.
doi:10.1073/pnas.0805234105

> Extracted 2026-05-06 with 4 region-anchored drafts covering 6 findings
> from a healthy-volunteer fMRI + DTI dual-stream study (n=33). Drafts:
> left_arcuate_fasciculus_slf__Saur2008.md (f1: dorsal pathway DTI
> connectivity; f2: dorsal pathway → speech_repetition recruitment),
> left_extreme_capsule__Saur2008.md (f1: ventral pathway DTI connectivity;
> f2: ventral pathway → auditory_comprehension recruitment),
> left_middle_temporal_gyrus__Saur2008.md (f1: MTG → auditory_comprehension
> fMRI recruitment), left_superior_temporal_gyrus__Saur2008.md (f1: STG →
> speech_repetition fMRI recruitment). NOTE: this is a healthy-volunteer
> study — all findings are correlational/recruitment, NOT causal. Speculative
> aphasia inferences (conduction aphasia → dorsal; transcortical sensory
> aphasia → ventral) are in the Discussion only; no patient data.

## @Marchina2011  [extracted]
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

## @Fridriksson2018BDNF  [extracted]
Fridriksson J, Elm J, Stark BC, Basilakos A, Rorden C, Sen S, George MS, Gottfried M, Bonilha L.
BDNF genotype and tDCS interaction in aphasia treatment.
*Brain Stimul*. 2018;11(6):1276–1281.
doi:10.1016/j.brs.2018.08.009

> RCT sub-analysis. Val/val BDNF genotype × anodal tDCS interaction predicts
> greater naming improvement in chronic aphasia treatment. Findings extracted
> into drafts/therapies/tdcs_aphasia_treatment__Fridriksson2018BDNF.md and
> drafts/predictors/bdnf_val66met__Fridriksson2018BDNF.md.

## @Dresang2022  [extracted]
Dresang HC, Harvey DY, Xie SX, Shah-Basak PP, DeLoretta L, Wurzman R, Parchure SY, Sacchetti D, Faseyitan O, Lohoff FW, Hamilton RH.
Genetic and Neurophysiological Biomarkers of Neuroplasticity Inform Post-Stroke Language Recovery.
*Neurorehabil Neural Repair*. 2022;36(6):371–380.
doi:10.1177/15459683221096391

> Cross-sectional cohort (n=17 chronic aphasia). BDNF Val66Met genotype main effect
> on WAB-AQ severity (controlling for lesion volume, age, time post-stroke); BDNF
> × cortical excitability and BDNF × stimulation-induced neuroplasticity interactions
> further improve severity predictions. Findings extracted into
> drafts/predictors/bdnf_val66met__Dresang2022.md.

## @Robson2019  [extracted]
Robson H, Griffiths TD, Grube M, Woollams AM.
Auditory, Phonological, and Semantic Factors in the Recovery From Wernicke's Aphasia Poststroke: Predictive Value and Implications for Rehabilitation.
*Neurorehabil Neural Repair*. 2019;33(10):800–812.
doi:10.1177/1545968319868709

> Prospective longitudinal cohort (n=12 WA, 2.5–9 MPO). Rapid auditory temporal
> processing (40-Hz FM detection) at 2.5 MPO predicts comprehension outcome at
> 9 MPO (r=−0.94). Lesion overlap maximal in left mid-posterior STG/STS. Findings
> extracted into drafts/regions/left_superior_temporal_gyrus_wernickes__Robson2019.md
> and drafts/predictors/auditory_temporal_processing__Robson2019.md.

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

## @Bonilha2014  [extracted]
Bonilha L, Rorden C, Fridriksson J.
Assessing the clinical impact of residual cortical disconnection after ischemic strokes.
*Stroke*. 2014;45(4):988–993.
doi:10.1161/STROKEAHA.113.004137

> Extracted 2026-05-06. Disconnectome paper (DTI + T1; n=39 chronic LH stroke aphasia patients,
> USC/MUSC). Primary claim: structural disconnection of BA 45 (pars triangularis) and BA 22
> independently predicts naming, fluency, and comprehension beyond cortical necrosis alone.
> Three findings: (f1) BA45 disconnection -> naming (beta=1.21, p<0.001; necrosis also significant
> beta=0.43, p=0.03); (f2) BA45 disconnection -> fluency (beta=7.52, p=0.025; necrosis NOT
> significant); (f3) BA22 disconnection -> comprehension (p=0.01; necrosis NOT significant).
> Draft: drafts/regions/left_ifg_pars_triangularis__Bonilha2014.md (3 findings).
> Cohort overlaps with @Fridriksson2018Anatomy (same USC/MUSC lab group).
> Note: the published title is "Assessing the clinical impact of residual cortical disconnection"
> (not "effect" as cited in the seed entry; verify against journal).

## @Baldo2006  [extracted]
Baldo JV, Schwartz S, Wilkins D, Dronkers NF.
Role of frontal versus temporal cortex in verbal fluency as revealed by voxel-based lesion symptom mapping.
*J Int Neuropsychol Soc*. 2006;12(6):896–900.
doi:10.1017/S1355617706061078

> Extracted 2026-05-06. VLSM paper (n=48 chronic LH stroke patients, VA Northern California /
> Dronkers lab). Primary dissociation: letter fluency -> left frontal (BA 4, 6, 44 + parietal +
> insula/putamen); category fluency -> left temporal (BA 22, 37, 41, 42 + parietal + insula/putamen).
> Subtraction maps sharpen the frontal/temporal dissociation. Important caveats: uncorrected p<.05
> threshold; Talairach 2D template lesion tracing; mixed MRI/CT imaging.
> 2 findings in draft: drafts/regions/left_ifg_pars_opercularis__Baldo2006.md (f1: letter fluency,
> f2: category fluency).

## @Fridriksson2018Anatomy  [extracted]
Fridriksson J, den Ouden DB, Hillis AE, Hickok G, Rorden C, Basilakos A, Yourganov G, Bonilha L.
Anatomy of aphasia revisited.
*Brain*. 2018;141(3):848–862.
doi:10.1093/brain/awx363

> Extracted 2026-05-06. RLSM + CLSM (connectome-LSM) paper (n=159 chronic LH stroke patients,
> USC/MUSC Aphasia Lab). Examines 16 clinical aphasia tests in relation to damage within the
> dual-stream (dorsal + ventral) framework. Key findings: (1) IFG pars opercularis is the strongest
> single independent predictor of speech fluency (multivariate RLSM R2=0.40); (2) posterior STG is
> the most widely-implicated region (top predictor on 8/16 tests) and strongest predictor of sentence
> comprehension (R2=0.60); (3) naming (PNT correct) involves both dorsal and ventral stream regions
> with no single dominant lesion location. PCA of production/comprehension tasks maps cleanly onto
> dorsal/ventral streams. CLSM reveals IFG opercularis-triangularis connection as top hub link for
> AQ and speech fluency.
> 3 findings in 2 drafts:
>   drafts/regions/left_ifg_pars_opercularis__Fridriksson2018Anatomy.md (f1: speech fluency R2=0.40;
>     f2: aphasia quotient network)
>   drafts/regions/left_posterior_stg__Fridriksson2018Anatomy.md (f1: sentence comprehension R2=0.60;
>     f2: auditory word recognition R2=0.31; f3: naming/PNT network)
> Cohort overlaps with @Fridriksson2018 (same USC Aphasia Lab archival database; n=138 vs n=159).

## @MassonTrottier2021  [extracted]
Masson-Trottier M, Sontheimer A, Durand E, Ansaldo AI.
Resting-State Functional Connectivity following Phonological Component Analysis: The Combined Action of Phonology and Visual Orthographic Cues.
*Brain Sci*. 2021;11(11):1458.
doi:10.3390/brainsci11111458

> Extracted 2026-05-06. rs-fMRI pre/post therapy study (n=10 chronic LH stroke, francophone Quebec).
> Therapy: Phonological Component Analysis in French (Fr-PCA), 15 sessions over 5 weeks.
> Method: ROI-to-ROI rsFC analysis (CONN toolbox v18.b; 106 Harvard-Oxford atlas ROIs; paired t-test post>pre; p-FDR<0.05).
> Key findings: (1) Increased rsFC between ant. left temporal fusiform cortex (BA20) and bilateral
> supracalcarine cortex (BA17), and between left SCC and ant. left ITG (BA20) — interpreted as
> therapy-induced strengthening of visual-semantic network links; (2) Decreased rsFC between right
> lingual gyrus (BA18) and right SFG (BA8-9) — interpreted as reduction of maladaptive RH recruitment.
> Behavioral: significant naming improvement on trained (r=0.89, p=0.005) and untrained items (r=0.89, p=0.005).
> No significant correlation between rsFC changes and naming gains.
> 2 findings in 1 therapy-anchored draft:
>   drafts/therapies/phonological_component_analysis__MassonTrottier2021.md
>   (f1: increased LH visual-semantic FC; f2: decreased RH FC)

## @Harvey2022  [extracted]
Harvey DY, Parchure S, Hamilton RH.
Factors predicting long-term recovery from post-stroke aphasia.
*Aphasiology*. 2022;36(11):1351–1372.
doi:10.1080/02687038.2021.1966374

> Extracted 2026-05-06. Longitudinal cohort study (n=18 chronic LH stroke, Moss Rehabilitation /
> UPenn; initial assessment 5–133 MPO; follow-up 21–94 months later; WAB-R AQ as outcome).
> Method: multiple linear regression (predictor variables: lesion volume, MPO, age at stroke,
> education); backward stepwise regression (psychosocial: ALA subdomains, SLT amount); lesion
> subtraction analysis + uncorrected VLSM.
> Key findings: (1) Lesion volume was the only significant stroke/demographic predictor — smaller
> lesion → greater AQ gain [R²=0.52, F(4,13)=3.51, p=.037]; (2) ALA participation domain
> (satisfaction with life participation) significantly predicted better outcome; ALA aphasia domain
> (self-perceived impairment) negatively predicted outcome (counterintuitive); combined model
> [lesion vol + ALA participation + ALA aphasia]: R²=0.68, F(4,13)=6.96, p=.003.
> Lesion location (exploratory, uncorrected): temporoparietal (posterior STG/MTG/ITG, angular gyrus,
> supramarginal gyrus, inferior/superior parietal) and frontal (IFG opercularis/triangularis/orbitalis,
> MFG, precentral, insula) and white matter (AF, IFOF, ILF, UF, internal capsule) regions associated
> with non-improvement group.
> 2 findings in 1 predictor-anchored draft:
>   drafts/predictors/lesion_volume__Harvey2022.md
>   (f1: lesion volume → WAB-R AQ gain; f2: ALA participation → WAB-R AQ gain)

## @Breining2022  [extracted]
Breining BL, Faria AV, Caffo B, Meier EL, Sheppard SM, Sebastian R, Tippett DC, Hillis AE.
Neural regions underlying object and action naming: complementary evidence from acute stroke and primary progressive aphasia.
*Aphasiology*. 2022;36(6):732–760.
doi:10.1080/02687038.2021.1907291

> Extracted 2026-05-06. Cross-sectional study with acute stroke (N=37 with imaging) and PPA (N=31
> with imaging; N=138 behaviorally). PPA findings NOT extracted (non-stroke etiology per KB scope).
> Method (acute stroke): LASSO regression on %ROI damaged (13 left hemisphere MRICloud atlas ROIs)
> predicting BNT (object naming) and HANA (action naming). DWI lesion tracing; MRICloud 289-ROI
> parcellation; total lesion volume as covariate.
> Key acute stroke findings:
>   Object naming (BNT): left angular gyrus independently significant (LASSO=−0.524, p<.001);
>     left MTG also selected (LASSO=−0.121, p=.397, not independent).
>   Action naming (HANA): left angular gyrus selected (LASSO=−0.405, p=.728, not independent);
>     left insula selected (LASSO=−0.015, p=.92, not independent); total lesion volume trend (p=.072).
>   Left angular gyrus is the only region associated with BOTH object and action naming in stroke.
> 2 findings in 1 region-anchored draft:
>   drafts/regions/left_angular_gyrus__Breining2022.md
>   (f1: left AG → object naming p<.001; f2: left AG → action naming p=.728 [in model, not independent])
> NOTE: PPA exclusion documented in draft provenance.flags.

## @Kristinsson2025  [extracted]
Kristinsson S, den Ouden DB, Rorden C, Newman-Norlund R, Johnson L, Wilmskoetter J, Gleichgerrcht E, Hillis AE, Hickok G, Fridriksson J, Bonilha L.
Partial least squares multimodal analysis of brain network correlates of language deficits in aphasia.
*Brain Communications*. 2025;7(4):fcaf246.
doi:10.1093/braincomms/fcaf246

> Multimodal PLSR study on n=86 chronic (≥12 months post-stroke) left-hemisphere stroke patients
> with aphasia from the POLAR trial (NCT03416738; USC + MUSC). Neuroimaging modalities: lesion
> anatomy (manual T2 tracing; enantiomorphic normalization to MNI via AICHA atlas), structural
> and functional connectivity (DTI, rsfMRI), VBM, task-fMRI (picture-naming; real>abstract),
> ASL (CBF). PLSR decomposed shared vs. unique lesion-behaviour covariance across WAB-R subtests
> (spontaneous speech, naming, repetition, auditory comprehension). Left perisylvian regions
> (rolandic operculum in 7/11 modality models, STG, ITG) accounted for shared variance (R²=22–25%).
> Unique variance: right putamen → naming (p=0.013) and repetition (p=0.021); left superior
> temporal lobe + right precuneus → auditory comprehension (p=0.049, 0.045). Highest single-model
> prediction: auditory comprehension DTI r=0.45; spontaneous speech DTI r=0.42.
> 2 findings in 1 predictor-anchored draft:
>   drafts/predictors/severity_metric__Kristinsson2025.md (f1: shared perisylvian; f2: unique regional)
> Possible cohort overlap with @Fridriksson2018, @Yourganov2015Predicting (USC/MUSC Aphasia Lab).

## @Teghipco2024  [extracted]
Teghipco A, Newman-Norlund R, Fridriksson J, Rorden C, Bonilha L.
Distinct brain morphometry patterns revealed by deep learning improve prediction of post-stroke aphasia severity.
*Communications Medicine*. 2024;4(1):115.
doi:10.1038/s43856-024-00541-8

> CNN vs SVM classification of severe aphasia (WAB-AQ <50) using whole-brain morphometry
> (T1/T2 tissue volumes + lesion anatomy; 8mm downsampled, MNI152) in n=231 chronic stroke
> patients from USC/MUSC (Siemens 3T Prisma). 3D CNN with Grad-CAM++ outperformed linear SVM:
> balanced accuracy CNN 0.77 vs SVM 0.73, F1 0.70 vs 0.65 (t(19)=−10, p=5.26e−9, d=2.24).
> Saliency maps: right hemisphere morphometry strongly predicted severe aphasia; left hemisphere
> predicted non-severe. Consensus clustering of Grad-CAM++ maps: 7 severe + 6 non-severe
> morphometry subgroups implicating language, attention, and aging networks.
> 2 findings in 1 predictor-anchored draft:
>   drafts/predictors/severity_metric__Teghipco2024.md (f1: CNN>SVM performance; f2: lateralization)
> Possible cohort overlap with @Fridriksson2018, @Yourganov2015Predicting, @Kristinsson2025
> (USC/MUSC Aphasia Lab infrastructure).

## @White2024  [extracted]
White A, Saranti M, d'Avila Garcez A, Hope TMH, Price CJ, Bowman H.
Predicting recovery following stroke: Deep learning, multimodal data and feature selection using explainable AI.
*NeuroImage: Clinical*. 2024;43:103638.
doi:10.1016/j.nicl.2024.103638

> CNN-based binary classification (aphasic vs non-aphasic spoken picture description) in n=758
> English-speaking stroke survivors from the PLORAS database (UCL Wellcome Centre; Seghier et al.
> 2016). Architectures evaluated: logistic regression (baseline), ResNet-18, lightweight CNN,
> 3D ResNet10, early fusion, DAFT, ROI and hybrid ROI variants. Best model: ResNet-18 Hybrid ROI
> (MRI ROIs + symbolic tabular representations), balanced accuracy ~0.85 (statistically significant
> improvement over baseline). Baseline logistic regression (left lesion size + initial severity +
> recovery time): balanced accuracy 0.813. Explainable AI: CLEAR Image (perturbation-based;
> brain atlas ROI parcellation). Key finding: tabular features (initial severity, lesion size,
> recovery time) drive logistic regression well; adding MRI ROIs provides incremental but
> significant improvement.
> 2 findings in 1 predictor-anchored draft:
>   drafts/predictors/severity_metric__White2024.md (f1: tabular predictors baseline; f2: best CNN)
> PLORAS cohort is distinct from USC/MUSC and Boston University cohorts — no overlap expected.

## @Hu2025  [extracted]
Hu X, Varkanitsa M, Kropp E, Betke M, Ishwar P, Kiran S.
Aphasia severity prediction using a multi-modal machine learning approach.
*NeuroImage*. 2025;317:121300.
doi:10.1016/j.neuroimage.2025.121300

> Multimodal ML (SVR + Random Forest) predicting WAB-R AQ (0–100; continuous) in n=76
> post-stroke aphasia patients from Boston University CBR (Kiran lab; Siemens 3T Prisma).
> Seven predictor classes: lesion volume (LV), percent spared grey matter (PSG; AAL3; 83 LH
> regions), percent spared white matter (PSW; BCBToolkit; 36 tracts), fractional anisotropy (FA;
> 10 tracts via DSI Studio), resting-state FC (rsFMRI-FC; 50 AAL3 ROIs; 625 Fisher-z features),
> resting-state transitivity (rsFMRI-trans), demographics (DM). Optimal SVR: DM+PSW+rsFMRI-FC
> (r=0.73, RMSE=15.82). rsFMRI-FC had highest SHAP (3.65). Most consistently selected WM:
> left arcuate fasciculus posterior segment + fronto-insular tract (11/11 outer folds); FA:
> left arcuate + left uncinate (11/11 folds).
> Note: citation key is @Hu2025 (not @Hu2023) — NeuroImage 317(2025)121300; received Dec 2024,
> published June 2025.
> 2 findings in 1 predictor-anchored draft:
>   drafts/predictors/severity_metric__Hu2025.md (f1: multimodal superiority; f2: feature selection)
> Boston University CBR cohort — distinct from USC/MUSC and PLORAS cohorts.

## @Stefaniak2022  [extracted]
Stefaniak JD, Geranmayeh F, Lambon Ralph MA.
The multidimensional nature of aphasia recovery post-stroke.
*Brain*. 2022;145(4):1354–1367.
doi:10.1093/brain/awab377

> Extracted 2026-05-06. Longitudinal fMRI study (n=26 chronic LH stroke;
> mean age 59.0 years SD 11.0; English premorbidly fluent) scanned at
> 2 weeks (T1) and 4 months (T2) post-stroke. Task: overt speech production
> (Speech+Count > Rest). Mass univariate SPM with voxelwise activation change
> correlated with PC score change, controlled for baseline PC score
> (proportional-recovery confound). Three orthogonal PCA components: PC1=fluency,
> PC2=semantic/executive, PC3=phonology — with non-overlapping bilateral neural
> substrates for each component's recovery trajectory. Key finding: bilateral
> middle frontal gyri + right temporo-occipital MTG activation increase predicts
> fluency recovery (β=0.29-0.30 pre-control, β=0.38 after baseline-severity control).
> 4 findings in 1 region-anchored draft:
>   drafts/regions/bilateral_mfg_temporal_recovery__Stefaniak2022.md
>   (f1: bilateral MFG + RH temporo-occipital → fluency recovery longitudinal;
>    f2: bilateral ATL → semantic/executive recovery; f3: bilateral precentral
>    + vmPFC + precuneus → phonology recovery; f4: RH SMG/insula/MTG →
>    fluency cross-sectional T1).
> Cohort note: co-author Geranmayeh's prior work (Geranmayeh 2016, 2017) likely
> uses overlapping subacute aphasia cohort — flagged in draft provenance.

---

## Citation-only references (forward-pointing replications/contradictions)

> These papers are referenced from drafts via `replications:` or
> `contradictions:` lists but have not themselves been read or extracted.
> Promote a paper to `[extracted]` status by reading its PDF and writing
> draft findings against it.

## @Schwartz2009  [cited]
Schwartz MF, Kimberg DY, Walker GM, Faseyitan O, Brecher A, Dell GS, Coslett HB.
Anterior temporal involvement in semantic word retrieval: voxel-based
lesion-symptom mapping evidence from aphasia.
*Brain*. 2009;132(Pt 12):3411–3427.
doi:10.1093/brain/awp284

> Cited from `drafts/regions/left_anterior_temporal_lobe__Mirman2015.md` (f1
> replication). Penn aphasia registry VLSM paper establishing anterior
> temporal lobe involvement in semantic word retrieval — direct
> methodological precursor to Mirman 2015.

## @Walker2011  [cited]
Walker GM, Schwartz MF, Kimberg DY, Hamilton RH, Faseyitan O, Brecher A, Dell GS, Coslett HB.
Support for anterior temporal involvement in semantic error production in aphasia:
new evidence from VLSM.
*Brain Lang*. 2011;117(3):110–122.
doi:10.1016/j.bandl.2011.02.005

> Cited from `drafts/regions/left_anterior_temporal_lobe__Mirman2015.md` (f1
> replication). Penn aphasia registry follow-up VLSM paper providing
> additional evidence for ATL → semantic-error production link.

## @DeWitt2012  [cited]
DeWitt I, Rauschecker JP.
Phoneme and word recognition in the auditory ventral stream.
*Proc Natl Acad Sci USA*. 2012;109(8):E505–E514.
doi:10.1073/pnas.1113427109

> Cited from `drafts/regions/left_superior_temporal_gyrus_wernicke__Mirman2015.md`
> (f1 replication). Meta-analytic neuroimaging review establishing the auditory
> ventral stream's role in phoneme/word recognition along STG/STS — supports
> the LH STG factor in Mirman's speech-recognition model.

## @Schwartz2012  [cited]
Schwartz MF, Faseyitan O, Kim J, Coslett HB.
The dorsal stream contribution to phonological retrieval in object naming.
*Brain*. 2012;135(Pt 12):3799–3814.
doi:10.1093/brain/aws300

> Cited from `drafts/regions/left_supramarginal_gyrus_premotor__Mirman2015.md`
> (f1 replication). Penn aphasia registry VLSM paper localising phonological
> retrieval to dorsal-stream supramarginal/premotor regions.

## @Buchsbaum2011  [cited]
Buchsbaum BR, Baldo J, Okada K, Berman KF, Dronkers N, D'Esposito M, Hickok G.
Conduction aphasia, sensory-motor integration, and phonological short-term memory —
an aggregate analysis of lesion and fMRI data.
*Brain Lang*. 2011;119(3):119–128.
doi:10.1016/j.bandl.2010.12.001

> Cited from `drafts/regions/left_supramarginal_gyrus_premotor__Mirman2015.md`
> (f1 replication). Aggregate lesion + fMRI analysis localising phonological
> short-term memory and sensory-motor integration to area Spt
> (sylvian-parietal-temporal junction) — supports the dorsal-stream
> phonological retrieval finding.

## @Fridriksson2010  [cited]
Fridriksson J, Kjartansson O, Morgan PS, Hjaltason H, Magnusdottir S, Bonilha L, Rorden C.
Impaired speech repetition and left parietal lobe damage.
*J Neurosci*. 2010;30(33):11057–11061.
doi:10.1523/JNEUROSCI.1120-10.2010

> Cited from `drafts/regions/left_supramarginal_gyrus_premotor__Mirman2015.md`
> (f1 replication). LSM study linking left parietal lobe damage to impaired
> speech repetition — independent USC-cohort replication of dorsal-stream
> phonological retrieval finding.

## @Hosomi2009  [cited]
Hosomi A, Nagakane Y, Yamada K, Kuriyama N, Mizuno T, Nishimura T, et al.
Assessment of arcuate fasciculus with diffusion-tensor tractography may predict
the prognosis of aphasia in patients with left middle cerebral artery infarcts.
*Neuroradiology*. 2009;51(9):549–555.
doi:10.1007/s00234-009-0534-7

> Cited from `drafts/regions/left_arcuate_fasciculus__Marchina2011.md` (f1
> replication). DTI tractography study in LH MCA infarct patients linking
> arcuate fasciculus integrity to aphasia prognosis — direct precursor to
> Marchina 2011's lesion-load approach.

## @Breier2008  [cited]
Breier JI, Hasan KM, Zhang W, Men D, Papanicolaou AC.
Language dysfunction after stroke and damage to white matter tracts evaluated
using diffusion tensor imaging.
*Am J Neuroradiol*. 2008;29(3):483–487.
doi:10.3174/ajnr.A0846

> Cited from `drafts/regions/left_arcuate_fasciculus__Marchina2011.md` (f1
> replication). DTI study linking white-matter tract damage (including arcuate
> fasciculus) to post-stroke language dysfunction.

## @Basilakos2019  [cited]
Basilakos A, Stark BC, Johnson L, Rorden C, Yourganov G, Bonilha L, Fridriksson J.
Leukoaraiosis is associated with a decline in language abilities in chronic aphasia.
*Neurorehabil Neural Repair*. 2019;33(9):718–729.
doi:10.1177/1545968319862561

> Cited from `drafts/predictors/lesion_volume__Harvey2022.md` (f1 contradiction:
> "lesion volume not significant after controlling for leukoaraiosis"). Chronic
> aphasia longitudinal study finding leukoaraiosis (white-matter
> hyperintensity) burden — not lesion volume — predicts language decline.

## @Hope2017  [cited]
Hope TM, Leff AP, Prejawa S, Bruce R, Haigh Z, Lim L, et al., Seghier ML.
Right hemisphere structural adaptation and changing language skills years after
left hemisphere stroke.
*Brain*. 2017;140(6):1718–1728.
doi:10.1093/brain/awx086

> Cited from `drafts/predictors/lesion_volume__Harvey2022.md` (f1 contradiction:
> "no significant lesion volume difference between improved/not-improved
> groups"). PLORAS-cohort longitudinal study finding right-hemisphere
> structural adaptation rather than lesion-volume differences predicts
> long-term language change.
