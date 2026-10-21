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
  - **[refused]** — Deliberately not extracted (see the note under
    the entry); `extract.py --batch` skips it.

The status of each entry is shown in the `## @Key  [tag]` header.
Within each section entries are ordered by year, then alphabetically
by first author.

---

## Extracted papers

> Findings have been written from these papers. The annotated PDFs
> are in `papers/`. Update the status tag to `[extracted]` whenever a
> new extraction is performed against an entry.

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

> Extracted 2026-05-06. Tractography study (n=30 chronic LH MCA stroke).
> Lesion load of the left arcuate fasciculus predicts speech-production
> rate (words/min) significantly, while overall lesion size, extreme
> capsule lesion load, and uncinate fasciculus lesion load do not.
> Promoted into canonical regions/left_arcuate_fasciculus.md as f1.

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

## @Mirman2015  [extracted]
Mirman D, Chen Q, Zhang Y, Wang Z, Faseyitan OK, Coslett HB, Schwartz MF.
Neural organization of spoken language revealed by lesion-symptom mapping.
*Nat Commun*. 2015;6:6762.
doi:10.1038/ncomms7762

> Extracted 2026-05-06. Large-cohort (n=99) VLSM study on the Philadelphia
> aphasia registry mapping multiple language components (Heschl's gyrus,
> planum temporale, anterior MTG, temporal pole, supramarginal/premotor
> dorsal-stream phonological retrieval, frontal white-matter bottleneck).
> Promoted across multiple region entries.

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

## @Fridriksson2018BDNF  [extracted]
Fridriksson J, Elm J, Stark BC, Basilakos A, Rorden C, Sen S, George MS, Gottfried M, Bonilha L.
BDNF genotype and tDCS interaction in aphasia treatment.
*Brain Stimul*. 2018;11(6):1276–1281.
doi:10.1016/j.brs.2018.08.009

> RCT sub-analysis. Val/val BDNF genotype × anodal tDCS interaction predicts
> greater naming improvement in chronic aphasia treatment. Findings extracted
> into drafts/therapies/tdcs_aphasia_treatment__Fridriksson2018BDNF.md and
> drafts/predictors/bdnf_val66met__Fridriksson2018BDNF.md.

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

---

## Cited references (forward-pointing replications/contradictions)

> These papers are referenced by extracted findings via `replications:`
> or `contradictions:` lists. They have not themselves been read or
> extracted. Promote a paper to `[extracted]` status by reading its
> PDF and writing draft findings against it.

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

## @Pulvermuller2001  [cited]
Pulvermüller F, Neininger B, Elbert T, Mohr B, Rockstroh B, Koebbel P, Taub E.
Constraint-induced therapy of chronic aphasia after stroke.
*Stroke*. 2001;32(7):1621–1626.
doi:10.1161/01.str.32.7.1621

> Referenced as a replication for the TUF behavioural-efficacy
> finding. Constraint-Induced Aphasia Therapy (CIAT) is its own
> therapy class — distinct from TUF — and would warrant its own
> therapy-anchored draft if extracted.

## @Boyle2004  [cited]
Boyle M.
Semantic feature analysis treatment for anomia in two fluent aphasia syndromes.
*Am J Speech Lang Pathol*. 2004;13(3):236–249.
doi:10.1044/1058-0360(2004/025)

> Original Semantic Feature Analysis paper, referenced as a
> replication for the typicality-based SFA finding (Barbieri 2023).
> Would extract as the parent therapy entry for SFA-family treatments.

## @Breier2008  [cited]
Breier JI, Hasan KM, Zhang W, Men D, Papanicolaou AC.
Language dysfunction after stroke and damage to white matter tracts evaluated
using diffusion tensor imaging.
*Am J Neuroradiol*. 2008;29(3):483–487.
doi:10.3174/ajnr.A0846

> Cited from `drafts/regions/left_arcuate_fasciculus__Marchina2011.md` (f1
> replication). DTI study linking white-matter tract damage (including arcuate
> fasciculus) to post-stroke language dysfunction.

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

## @Fridriksson2010  [cited]
Fridriksson J, Kjartansson O, Morgan PS, Hjaltason H, Magnusdottir S, Bonilha L, Rorden C.
Impaired speech repetition and left parietal lobe damage.
*J Neurosci*. 2010;30(33):11057–11061.
doi:10.1523/JNEUROSCI.1120-10.2010

> Cited from `drafts/regions/left_supramarginal_gyrus_premotor__Mirman2015.md`
> (f1 replication). LSM study linking left parietal lobe damage to impaired
> speech repetition — independent USC-cohort replication of dorsal-stream
> phonological retrieval finding.

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

## @Basilakos2019  [cited]
Basilakos A, Stark BC, Johnson L, Rorden C, Yourganov G, Bonilha L, Fridriksson J.
Leukoaraiosis is associated with a decline in language abilities in chronic aphasia.
*Neurorehabil Neural Repair*. 2019;33(9):718–729.
doi:10.1177/1545968319862561

> Cited from `drafts/predictors/lesion_volume__Harvey2022.md` (f1 contradiction:
> "lesion volume not significant after controlling for leukoaraiosis"). Chronic
> aphasia longitudinal study finding leukoaraiosis (white-matter
> hyperintensity) burden — not lesion volume — predicts language decline.

---

## @Maher2006  [cited]
Maher LM, Kendall D, Swearengin JA, Rodriguez A, Leon SA, Pingel K, Holland AL,
Rothi LJG.
A pilot study of use-dependent learning in the context of Constraint Induced
Language Therapy.
*J Int Neuropsychol Soc*. 2006;12(6):843–852.
doi:10.1017/S1355617706061029

> Cited by `therapies/constraint_induced_aphasia_therapy.md` f2, which was
> written from clinical knowledge in 2026-05 without the paper (its only
> passage is a placeholder). Added 2026-10-19 with the PDF in `papers/`
> so the finding can be re-extracted properly (GOVERNANCE.md §5).

## @Stahl2013  [cited]
Stahl B, Henseler I, Turner R, Geyer S, Kotz SA.
How to engage the right brain hemisphere in aphasics without even singing:
evidence for two paths of speech recovery.
*Front Hum Neurosci*. 2013;7:35.
doi:10.3389/fnhum.2013.00035

> Cited by `therapies/melodic_intonation_therapy.md` f3 (placeholder
> passage; see @Maher2006 note). Added 2026-10-19 with the PDF.

## @vanderMeulen2012  [cited]
van der Meulen I, van de Sandt-Koenderman WME, Ribbers GM.
Melodic Intonation Therapy: present controversies and future opportunities.
*Arch Phys Med Rehabil*. 2012;93(1 Suppl):S46–S52.
doi:10.1016/j.apmr.2011.05.029

> Cited by `therapies/melodic_intonation_therapy.md` f2 (placeholder
> passage; see @Maher2006 note). Added 2026-10-19 with the PDF. The
> finding also mentions RCT evidence, which is van der Meulen et al.
> 2014 *Neurorehabil Neural Repair* (doi:10.1177/1545968313517754), not
> this paper — resolve when re-extracting.

## @Raymer  [extracted-as-review]
Raymer AM, Roitsch J.
Effectiveness of Constraint-Induced Language Therapy for Aphasia: Evidence
From Systematic Reviews and Meta-Analyses.
*Am J Speech Lang Pathol*. 2022.
doi:10.1044/2022_AJSLP-22-00248

> Key kept as `@Raymer` (no year) to match the existing
> `reviews/constraint_induced_language_therapy__Raymer.md`; entry added
> 2026-10-19 so the DOI is on record. PDF: `papers/Raymer.pdf`.

## Extracted papers (added 2026-05-06, batch 3)

## @DenOuden2019  [extracted]
den Ouden DB, Malyutina S, Basilakos A, Bonilha L, Gleichgerrcht E, Yourganov G, Hillis AE, Hickok G, Rorden C, Fridriksson J.
Cortical and structural-connectivity damage correlated with impaired syntactic processing in aphasia.
*Hum Brain Mapp*. 2019;40(7):2153–2173.
doi:10.1002/hbm.24514

> Extracted 2026-05-06. VLSM + CLSM (connectome-LSM) study on n=71 chronic LH stroke
> aphasia patients (68 with imaging) from the USC/MUSC Aphasia Lab. Decomposes morphosyntactic
> production deficits via VLSM (k=47, lesion-size controlled) and structural-connectivity
> damage via CLSM (not lesion-size controlled). 3 findings:
>   f1 left IFG pars triangularis (BA45) → morphosyntactic production (causal, VLSM)
>   f2 left pSTG/angular gyrus → verb argument structure production (causal, VLSM)
>   f3 ventral IFG–temporal connectivity → noncanonical sentence production (correlational, CLSM)
> Cohort overlaps with @Fridriksson2018, @Yourganov2015Predicting, @Basilakos2015 (USC/MUSC).

## @Pedersen2004  [extracted]
Pedersen PM, Vinter K, Olsen TS.
Aphasia after Stroke: Type, Severity and Prognosis. The Copenhagen Aphasia Study.
*Cerebrovasc Dis*. 2004;17(1):35–43.
doi:10.1159/000073896

> Extracted 2026-05-06. Prospective community-based stroke registry (n=270 acute aphasia,
> 203 first-ever stroke; Copenhagen Aphasia Study). Initial WAB-AQ + modified Scandinavian
> Stroke Scale (SSS) jointly predict R²=0.60 of 1-year WAB-AQ; WAB-AQ alone R²=0.47;
> age, sex, and aphasia type are NOT significant predictors. Foundational paper for
> "initial severity predicts recovery" in aphasiology — heavily cited prognostic study.

## @Robson2014  [extracted]
Robson H, Zahn R, Keidel JL, Binney RJ, Sage K, Lambon Ralph MA.
The anterior temporal lobes support residual comprehension in Wernicke's aphasia.
*Brain*. 2014;137(Pt 3):931–943.
doi:10.1093/brain/awt373

> Extracted 2026-05-06. Distortion-corrected fMRI study in n=12 chronic Wernicke's aphasia.
> Reveals left anterior temporal lobe (anterior fusiform, temporal pole) and right anterior
> STG overactivation for written-word comprehension as residual substrate. 2 findings.
> NOTE: distinct from @Robson2019 (auditory temporal processing predictor) — different cohort,
> different paradigm.

## @Itabashi2015  [extracted]
Itabashi R, Nishio Y, Kataoka Y, Yazawa Y, Furui E, Matsuda M, Mori E.
Damage to the Left Precentral Gyrus Is Associated With Apraxia of Speech in Acute Stroke.
*Stroke*. 2016;47(1):31–36.
doi:10.1161/STROKEAHA.115.010402

> Extracted 2026-05-06. VLSM (Liebermeister) study on n=136 acute/subacute LH MCA stroke
> patients from Kohnan Hospital, Japan. 2 findings:
>   f1 left precentral gyrus posterior wall → pure AOS (causal, Z_max=3.482)
>   f2 basal ganglia + corona radiata + precentral → AOS+aphasia (causal, larger lesion burden)
> Independent replication of @Basilakos2015 in an acute Japanese cohort. NO cohort overlap
> with USC/MUSC papers. Note: paper labelled 2015 by acceptance date; published in Stroke
> 2016 (volume 47, issue 1).

## @Leff2009  [extracted]
Leff AP, Schofield TM, Crinion JT, Seghier ML, Grogan A, Green DW, Price CJ.
The left superior temporal gyrus is a shared substrate for auditory short-term memory and
speech comprehension: evidence from 210 patients with stroke.
*Brain*. 2009;132(Pt 12):3401–3410.
doi:10.1093/brain/awp273

> Extracted 2026-05-06. VBM (VBCM) study on n=210 stroke patients from the UCL PLORAS
> cohort (Wellcome Centre, London). Identifies left posterior STG/STS at peak [-66, -32, 4]
> as a shared neural substrate for auditory short-term memory (digit span) and spoken
> sentence comprehension. 2 findings.

## @Naeser2005  [extracted]
Naeser MA, Martin PI, Nicholas M, Baker EH, Seekins H, Kobayashi M, Theoret H, Fregni F,
Maria-Tormos J, Kurland J, Doron KW, Pascual-Leone A.
Improved picture naming in chronic aphasia after TMS to part of right Broca's area:
An open-protocol study.
*Brain Lang*. 2005;93(1):95–105.
doi:10.1016/j.bandl.2004.08.004

> Extracted 2026-05-06. Open-protocol case-series (n=4) on slow (1 Hz) repetitive TMS to
> right pars triangularis (BA45) for 10 days in chronic non-fluent aphasia. Significant
> Boston Naming Test improvement at 2 months (p=0.003) lasting at 8 months in 3/4
> participants. 1 finding (therapy-anchored: tms_right_ifg).

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

## @Dronkers1996  [extracted]
Dronkers NF.
A new brain region for coordinating speech articulation.
*Nature*. 1996;384(6605):159–161.
doi:10.1038/384159a0

> Extracted 2026-05-06 (auto-approved). Foundational LSM paper localising apraxia
> of speech to the left precentral gyrus of the insula: 25/25 AOS patients had
> lesions encompassing this region; 0/19 non-AOS patients did. Promoted to
> `regions/left_precentral_gyrus_insula.md`.

## @Lazar2010  [extracted]
Lazar RM, Minzer B, Antoniello D, Festa JR, Krakauer JW, Marshall RS.
Improvement in aphasia scores after stroke is well predicted by initial severity.
*Stroke*. 2010;41(7):1485–1488.
doi:10.1161/STROKEAHA.109.577338

> Extracted 2026-05-06 (auto-approved). Establishes that initial WAB composite
> score within 24–72h post-stroke is a strong predictor of WAB recovery
> trajectory, independent of demographics and treatment intensity. Promoted to
> `predictors/initial_aphasia_severity.md`.

## @Basilakos2015  [cited]
Basilakos A, Rorden C, Bonilha L, Moser D, Fridriksson J.
Patterns of poststroke brain damage that predict speech production errors in
apraxia of speech and aphasia dissociate.
*Stroke*. 2015;46(6):1561–1566.
doi:10.1161/STROKEAHA.115.009211

> Cited as a replication target by `drafts/impairments/syntactic_processing__DenOuden2019.md`
> and `drafts/regions/left_precentral_gyrus__Itabashi2015.md` (independent USC-cohort
> replication of left precentral / insular AOS localisation; further dissociates AOS
> errors from aphasia-related speech errors). Available in `papers/Basilakos2015.pdf`
> for future primary extraction.

## @Goldenberg1994  [cited]
Goldenberg G, Spatt J.
Influence of size and site of cerebral lesions on spontaneous recovery
of aphasia and on success of language therapy.
*Brain Lang*. 1994;47(4):684–698.
doi:10.1006/brln.1994.1067

> Identified 2026-05-07 via OCR (Tesseract 4.1.1) of a scanned PDF that
> previously had no extractable text. Original filename
> `1-s2.0-S0093934X84710637-main.pdf`; the "84" is an Elsevier internal
> sequence (NOT the year — the paper is 1994). Searchable PDF saved as
> `papers/Goldenberg1994.pdf` (image background + invisible OCR layer,
> PDF/A-2b). Referenced in
> `drafts/reviews/aphasia_prognosis_predictors__Watila2015.md`
> (`primary_papers_cited` list) but not yet directly extracted as findings.
> Aachen Aphasia Test on n=18 patients across spontaneous-recovery and
> therapy phases; CT lesion size + temporobasal involvement predict
> therapy success while leaving spontaneous recovery intact — a
> potentially extractable predictor finding.

---

## Refused papers

> In 2026-05 papers without a primary patient dataset were refused.
> Schema v2.4 added the `reviews/` bucket (`method: narrative_review`,
> `relationship: synthesis`), which made that rule obsolete: reviews,
> meta-analyses and opinion pieces are extracted as review entries.
> The entries below were re-tagged on 2026-10-21 accordingly; the
> original refusal notes are kept for the audit trail. `[refused]` now
> means only "not extractable as it stands" (see Brady2022RELEASE).

## @NadeauCrosson1997  [re-extracted-as-review]
Nadeau SE, Crosson B (1997).
Subcortical aphasia.
*Brain and Language*. 58:355–402.

> Refused 2026-05-06. 48-page critical review of subcortical aphasia
> literature — no primary patient cohort; purely secondary synthesis.
> PDF: renamed to NadeauCrosson1997.pdf
>
> Re-extracted 2026-05-06 as narrative_review under schema v2.4.
> Draft: drafts/reviews/subcortical_aphasia__NadeauCrosson1997.md
> Annotation: papers/NadeauCrosson1997_annotated.pdf (12/12 quotes placed)

## @Radanovic2017  [re-extracted-as-review]
Radanovic M, Mansur LL (2017).
Aphasia in vascular lesions of the basal ganglia: A comprehensive review.
*Brain and Language*. 173:20–35.

> Refused 2026-05-06. Comprehensive narrative review of aphasia in
> basal ganglia vascular lesions — no primary dataset; secondary
> synthesis of published case reports and studies.
> PDF: renamed to Radanovic2017.pdf
>
> Re-extracted 2026-05-06 as narrative_review under schema v2.4.
> Draft: drafts/reviews/basal_ganglia_aphasia__Radanovic2017.md
> Annotation: papers/Radanovic2017_annotated.pdf (9/9 quotes placed)

## @Crosson1999  [re-extracted-as-review]
Crosson B (1999).
Subcortical mechanisms in language: Lexical-semantic mechanisms and the thalamus.
*Brain and Cognition*. 40:414–438.

> Refused 2026-05-06. Review of four previously-published thalamic
> lesion cases — secondary re-analysis of own published data; no new
> primary dataset.
> PDF: renamed to Crosson1999.pdf
>
> Re-extracted 2026-05-06 as narrative_review under schema v2.4.
> Draft: drafts/reviews/thalamic_language_mechanisms__Crosson1999.md
> Annotation: papers/Crosson1999_annotated.pdf (8/8 quotes placed)

## @MirmanThye2018  [extracted-as-review]
Mirman D, Thye M (2018).
Uncovering the neuroanatomy of core language systems using lesion-symptom mapping.
*Current Directions in Psychological Science*. 27(6):455–461.
doi:10.1177/0963721418787486

> Extracted 2026-05-06 as narrative_review under schema v2.4.
> Draft: drafts/reviews/lsm_language_systems_review__MirmanThye2018.md
> Annotation: papers/MirmanThye2018_annotated.pdf (11/11 quotes placed)
> PDF: MirmanThye2018.pdf (renamed from mirman-thye-2018-uncovering-the-neuroanatomy-of-core-language-systems-using-lesion-symptom-mapping.pdf)

## @Wallentin2018  [seed]
Wallentin M.
Sex differences in post-stroke aphasia rates are caused by age. A meta-analysis and database query.
*PLoS One*. 2018;13(12):e0209571.
doi:10.1371/journal.pone.0209571

> Refused 2026-05-06 under the primary-dataset rule (meta-analysis and
> database query, no own cohort). Re-tagged 2026-10-21: it is the
> evidence the `sex` and `age` predictor entries need, extractable as a
> review. Key given its year (was `@Wallentin`); PDF renamed to match.

## @Brady2022RELEASE  [refused]
Brady MC, Ali M, VandenBerg K, Williams LJ, Williams LR, Abo M, et al.
(REhabilitation and recovery of peopLE with Aphasia after StrokE — RELEASE Collaborators).
Precision rehabilitation for aphasia: REhabilitation and recovery of peopLE with
Aphasia after StrokE; an individual participant data network meta-analysis (PROSPERO CRD42018110947).
*International Journal of Stroke*. 2022.

> Refused 2026-05-06 under the primary-dataset rule. Still refused on
> 2026-10-21, for a different reason: `papers/Brady2022RELEASE.pdf` is
> the 322-page NIHR HTA monograph (doi:10.3310/RTLH7522), far beyond
> one extraction pass. The citable version is the journal article
> (Int J Stroke 2022, a separate DOI); fetch that, register it, and
> extract it as a review. The monograph stays for reference.

## @Mohr2017  [seed]
Mohr B.
Neuroplasticity and functional recovery after intensive language therapy in chronic post stroke aphasia.
*Front Hum Neurosci*. 2017;11:332.
doi:10.3389/fnhum.2017.00332

> Refused 2026-05-06 under the primary-dataset rule (opinion article).
> Re-tagged 2026-10-21: a short position piece on intensive therapy
> and plasticity; extractable as a review entry alongside
> Breitenstein2017 and Bhogal2003.

## @Shekari2022  [extracted-as-review]
Shekari E, Seyfi M, Modarres Zadeh A, Batouli SA, Valinejad V, Goudarzi S, Joghataei MT.
Mechanisms of brain activation following naming therapy in aphasia: a systematic review on task-based fMRI studies.
*Appl Neuropsychol Adult*. 2022.
doi:10.1080/23279095.2022.2074849

> Refused 2026-05-06 under the primary-dataset rule, then extracted as a
> review: `reviews/aphasia_therapy_neuroplasticity_fmri__Shekari2022.md`.
> Tag and bibliographic details corrected 2026-10-21 (the block had
> carried another paper's title and authors).

## @Simic2023  [re-extracted-as-review]
Simic T, Rochon E, Greco E, Martino R.
Treatment-induced neuroplasticity after anomia therapy in post-stroke aphasia:
A systematic review of neuroimaging studies.
*Brain and Language*. 2023.

> Refused 2026-05-06 for primary extraction (systematic review — no original
> dataset). Re-extracted 2026-05-06 as `narrative_review` under schema v2.4.
> Draft: `drafts/reviews/treatment_neuroplasticity_aphasia__Simic2023.md`.
> Available in `papers/Simic2023.pdf`.

## @Watila2015  [extracted-as-review]
Watila MM, Balarabe SA.
Factors predicting post-stroke aphasia recovery.
*Journal of the Neurological Sciences*. 2015.

> Refused 2026-05-06 for primary extraction (narrative review — no primary data).
> Extracted as review on 2026-05-06 under schema v2.4 narrative_review.
> Draft: `drafts/reviews/aphasia_prognosis_predictors__Watila2015.md`. Cites
> @Goldenberg1994 (now in citations.md as [cited]) and other primary papers.
> Available in `papers/Watila2015.pdf`.

## @Wilson2021  [extracted-as-review]
Wilson SM, Schneck SM.
Neuroplasticity in post-stroke aphasia: A systematic review and meta-analysis
of functional imaging studies of reorganization of language processing.
*Neurobiology of Language*. 2021.

> Refused 2026-05-06 for primary extraction (systematic review — PROSPERO
> CRD42018116295 — and meta-analysis of 86 fMRI/PET studies; no primary data).
> Extracted as review on 2026-05-06 under schema v2.4 narrative_review.
> Draft: `drafts/reviews/neuroplasticity_poststroke_aphasia__Wilson2021.md`.
> Available in `papers/Wilson2021.pdf`.

---

## Seed references (added 2026-10-20)

> Fetched after the 2026-10-19 gap analysis; none has findings yet.
> The note under each entry says which KB entry it is meant to
> strengthen. `extract.py --batch` picks them up in `papers/`.

## @Dronkers2004  [seed]
Dronkers NF, Wilkins DP, Van Valin RD, Redfern BB, Jaeger JJ.
Lesion analysis of the brain areas involved in language comprehension.
*Cognition*. 2004;92(1–2):145–177.
doi:10.1016/j.cognition.2003.11.002

> A. Sentence comprehension VLSM (n=64): posterior MTG, anterior STG,
> STS, BA 39, BA 47 — not BA 44/45. The counterweight the
> `syntactic_processing` and `brocas_aphasia` entries lack.

## @Hillis2004  [seed]
Hillis AE, Work M, Barker PB, Jacobs MA, Breese EL, Maurer K.
Re-examining the brain regions crucial for orchestrating speech articulation.
*Brain*. 2004;127(7):1479–1487.
doi:10.1093/brain/awh172

> A. Acute hypoperfusion study (n=80) placing apraxia of speech in
> posterior IFG, not insula — the direct reply to Dronkers 1996 that
> `left_precentral_gyrus_insula` currently cites alone.

## @Kummerer2013  [seed]
Kümmerer D, Hartwigsen G, Kellmeyer P, Glauche V, Mader I, Klöppel S, Suchan J, Karnath H-O, Weiller C, Saur D.
Damage to ventral and dorsal language pathways in acute aphasia.
*Brain*. 2013;136(2):619–629.
doi:10.1093/brain/aws354

> A. Acute-stage VLSM (n=100): repetition → dorsal (AF/SLF),
> comprehension → ventral (extreme capsule). Primary evidence for
> `left_extreme_capsule` and `left_arcuate_fasciculus_slf`, which rest
> on Saur2008 (healthy DTI) and Fridriksson2018.

## @Fridriksson2013  [seed]
Fridriksson J, Guo D, Fillmore P, Holland A, Rorden C.
Damage to the anterior arcuate fasciculus predicts non-fluent speech production in aphasia.
*Brain*. 2013;136(11):3451–3460.
doi:10.1093/brain/awt267

> A. The paper behind `left_anterior_arcuate_fasciculus`, which the KB
> currently supports only second-hand.

## @Henseler2014  [seed]
Henseler I, Regenbrecht F, Obrig H.
Lesion correlates of patholinguistic profiles in chronic aphasia: comparisons of syndrome-, modality- and symptom-level assessment.
*Brain*. 2014;137(3):918–930.
doi:10.1093/brain/awt374

> A. VLSM (n=102) at syndrome, modality and symptom level — the one
> study that maps classical syndromes (`brocas_aphasia`,
> `wernickes_aphasia`, `global_aphasia`, `anomic_aphasia`) with the
> same method as symptom-level maps.

## @Butler2014  [seed]
Butler RA, Lambon Ralph MA, Woollams AM.
Capturing multidimensionality in stroke aphasia: mapping principal behavioural components to neural structures.
*Brain*. 2014;137(12):3248–3266.
doi:10.1093/brain/awu286

> A. PCA of a broad battery (n=31) → phonology (dorsal), semantics
> (ventral ATL), cognition. Origin of the multidimensional framing in
> Stefaniak2022 and Alyahya2018; pairs with Mirman2015's
> form-to-meaning / form-to-articulation split.

## @Halai2017  [seed]
Halai AD, Woollams AM, Lambon Ralph MA.
Using principal component analysis to capture individual differences within a unified neuropsychological model of chronic post-stroke aphasia: revealing the unique neural correlates of speech fluency, phonology and semantics.
*Cortex*. 2017;86:275–289.
doi:10.1016/j.cortex.2016.04.016

> A. Extends Butler2014 (n=70) with a separate fluency factor →
> insular–motor cortex. Primary for `fluency` and `semantics`.

## @Alyahya2020  [seed]
Alyahya RSW, Halai AD, Conroy P, Lambon Ralph MA.
A unified model of post-stroke language deficits including discourse production and their neural correlates.
*Brain*. 2020;143(5):1541–1554.
doi:10.1093/brain/awaa074

> A. Same programme, adds discourse; the KB has no connected-speech
> finding at all.

## @Griffis2017  [seed]
Griffis JC, Nenert R, Allendorfer JB, Szaflarski JP.
Damage to white matter bottlenecks contributes to language impairments after left hemispheric stroke.
*NeuroImage Clin*. 2017;14:552–565.
doi:10.1016/j.nicl.2017.02.019

> A. The origin of the "bottleneck" concept in
> `left_frontal_white_matter_bottleneck`, which currently cites only
> Fridriksson2018Anatomy.

## @Thye2018  [seed]
Thye M, Mirman D.
Relative contributions of lesion location and lesion size to predictions of varied language deficits in post-stroke aphasia.
*NeuroImage Clin*. 2018;20:1129–1138.
doi:10.1016/j.nicl.2018.10.017

> A/C. Location vs volume for each deficit type (n=128) — exactly the
> question CALMaR's `lesion_volume` predictor and region findings
> must answer together.

## @GajardoVidal2021  [seed]
Gajardo-Vidal A, Lorca-Puls DL, PLORAS team, Warner H, Dhanjal NS, Erbs J, et al. (Price CJ, senior).
Damage to Broca's area does not contribute to long-term speech production outcome after stroke.
*Brain*. 2021;144(3):817–832.
doi:10.1093/brain/awaa460

> A. PLORAS (n=134): long-term speech production outcome depends on
> underlying white matter and insula, not BA 44/45 damage per se. The
> contradiction `left_ifg_pars_opercularis` should carry.

## @Rogalsky2018  [seed]
Rogalsky C, LaCroix AN, Chen K-H, Anderson SW, Damasio H, Love T, Hickok G.
The neurobiology of agrammatic sentence comprehension: a lesion study.
*J Cogn Neurosci*. 2018;30(2):234–255.
doi:10.1162/jocn_a_01200

> A. Sentence comprehension VLSM (n=57): temporal–parietal, not
> Broca's area, for non-canonical sentences. Pairs with Dronkers2004.

## @Ivanova2016  [seed]
Ivanova MV, Isaev DY, Dragoy OV, Akinina YS, Petrushevskiy AG, Fedina ON, Shklovsky VM, Dronkers NF.
Diffusion-tensor imaging of major white matter tracts and their role in language processing in aphasia.
*Cortex*. 2016;85:165–181.
doi:10.1016/j.cortex.2016.04.019

> A. Tract integrity (AF, IFOF, ILF, UF) vs comprehension,
> repetition, naming (n=37). Needed once `decode_lesion.py` gains the
> JHU tract labels.

## @Breitenstein2017  [seed]
Breitenstein C, Grewe T, Flöel A, Ziegler W, Springer L, Martus P, et al.; FCET2EC study group.
Intensive speech and language therapy in patients with chronic aphasia after stroke: a randomised, open-label, blinded-endpoint, controlled trial in a health-care setting.
*Lancet*. 2017;389(10078):1528–1538.
doi:10.1016/S0140-6736(17)30067-3

> B. The largest RCT of intensive therapy in chronic aphasia (n=158).
> Primary evidence for the `massed_practice` ingredient and the
> intensity claim behind CIAT.

## @Bhogal2003  [seed]
Bhogal SK, Teasell R, Speechley M.
Intensity of aphasia therapy, impact on recovery.
*Stroke*. 2003;34(4):987–993.
doi:10.1161/01.STR.0000062343.64383.D0

> B. The dose–response review every therapy entry cites for
> intensity; belongs in `reviews/`.

## @Brady2016  [seed]
Brady MC, Kelly H, Godwin J, Enderby P, Campbell P.
Speech and language therapy for aphasia following stroke.
*Cochrane Database Syst Rev*. 2016;(6):CD000425.
doi:10.1002/14651858.CD000425.pub4

> B. The Cochrane review (57 RCTs). Brady2022RELEASE was refused as
> an IPD meta-analysis; this is the citable summary of trial-level
> evidence for `reviews/`.

## @Efstratiadou2018  [seed]
Efstratiadou EA, Papathanasiou I, Holland R, Archonti A, Hilari K.
A systematic review of semantic feature analysis therapy studies for aphasia.
*J Speech Lang Hear Res*. 2018;61(5):1261–1278.
doi:10.1044/2018_JSLHR-L-16-0330

> B. Boyle2004 is the single SFA primary in the KB; this review gives
> the effect range and the responder profile for
> `typicality_semantic_feature_analysis` / `semantic_feature_generation`.

## @Leonard2008  [seed]
Leonard C, Rochon E, Laird L.
Treating naming impairments in aphasia: findings from a phonological components analysis treatment.
*Aphasiology*. 2008;22(9):923–947.
doi:10.1080/02687030701831474

> B. The original PCA treatment study; `phonological_component_analysis`
> currently cites only MassonTrottier2021 (an fMRI follow-up).

## @Zumbansen2014  [seed]
Zumbansen A, Peretz I, Hébert S.
Melodic intonation therapy: back to basics for future research.
*Front Neurol*. 2014;5:7.
doi:10.3389/fneur.2014.00007

> B. Separates the melodic and rhythmic ingredients of MIT — the
> evidence behind `melodic_intoning` vs `rhythmic_hand_tapping`.

## @Thompson2003  [seed]
Thompson CK, Shapiro LP, Kiran S, Sobecks J.
The role of syntactic complexity in treatment of sentence deficits in agrammatic aphasia: the complexity account of treatment efficacy (CATE).
*J Speech Lang Hear Res*. 2003;46(3):591–607.
doi:10.1044/1092-4388(2003/047)

> B. The primary behind `treatment_of_underlying_forms` and the
> `verb_argument_structure_training` ingredient.

## @Fridriksson2018JAMA  [seed]
Fridriksson J, Rorden C, Elm J, Sen S, George MS, Bonilha L.
Transcranial direct current stimulation vs sham stimulation to treat aphasia after stroke: a randomized clinical trial.
*JAMA Neurol*. 2018;75(12):1470–1476.
doi:10.1001/jamaneurol.2018.2287

> B. The futility-design tDCS RCT (n=74) that Fridriksson2018BDNF is
> the secondary analysis of; `tdcs_aphasia_treatment` needs the
> primary outcome.

## @Elsner2019  [seed]
Elsner B, Kugler J, Pohl M, Mehrholz J.
Transcranial direct current stimulation (tDCS) for improving aphasia in adults with aphasia after stroke.
*Cochrane Database Syst Rev*. 2019;(5):CD009760.
doi:10.1002/14651858.CD009760.pub4

> B. Cochrane tDCS review: naming improves, functional communication
> does not. The calibration `anodal_tdcs` needs.

## @Thiel2013  [seed]
Thiel A, Hartmann A, Rubi-Fessen I, Anglade C, Kracht L, Weiduschat N, Kessler J, Rommel T, Heiss W-D.
Effects of noninvasive brain stimulation on language networks and recovery in early poststroke aphasia.
*Stroke*. 2013;44(8):2240–2246.
doi:10.1161/STROKEAHA.111.000574

> B. Inhibitory rTMS over right IFG in subacute aphasia (n=24) with
> PET: the trial-level primary for `inhibitory_rtms`, which rests on
> Naeser2005's open-protocol series.

## @Meinzer2010  [seed]
Meinzer M, Mohammadi S, Kugel H, Schiffbauer H, Flöel A, Albers J, et al.
Integrity of the hippocampus and surrounding white matter is correlated with language training success in aphasia.
*NeuroImage*. 2010;53(1):283–290.
doi:10.1016/j.neuroimage.2010.06.004

> B/C. Responder predictor outside the language network; the
> decoder reaches the hippocampus (HO subcortical).

## @Bonilha2016  [seed]
Bonilha L, Gleichgerrcht E, Nesland T, Rorden C, Fridriksson J.
Success of anomia treatment in aphasia is associated with preserved architecture of global and left temporal lobe structural networks.
*Neurorehabil Neural Repair*. 2016;30(3):266–279.
doi:10.1177/1545968315593808

> B/C. Connectome predictor of naming-treatment response (n=24).

## @Forkel2014  [seed]
Forkel SJ, Thiebaut de Schotten M, Dell'Acqua F, Kalra L, Murphy DGM, Williams SCR, Catani M.
Anatomical predictors of aphasia recovery: a tractography study of bilateral perisylvian language networks.
*Brain*. 2014;137(7):2027–2039.
doi:10.1093/brain/awu113

> C. Right-hemisphere arcuate volume predicts 6-month recovery
> (n=16); the right-hemisphere predictor Hope2017 and
> `bilateral_middle_frontal_gyrus_recovery` need alongside them.

## @Hope2013  [seed]
Hope TMH, Seghier ML, Leff AP, Price CJ.
Predicting outcome and recovery after stroke with lesions extracted from MRI images.
*NeuroImage Clin*. 2013;2:424–433.
doi:10.1016/j.nicl.2013.03.005

> C. PLORAS prediction from lesion images (n=270): lesion site +
> time post-stroke explain most variance. The benchmark for
> `time_post_onset` and `lesion_volume`.

## @Hope2018  [seed]
Hope TMH, Leff AP, Price CJ.
Predicting language outcomes after stroke: is structural disconnection a useful predictor?
*NeuroImage Clin*. 2018;19:22–29.
doi:10.1016/j.nicl.2018.03.037

> C. Tests whether disconnection adds to lesion-location prediction
> (it adds little) — directly relevant to what `decode_lesion.py`
> should compute.

## @Benghanem2019  [seed]
Benghanem S, Rosso C, Arbizu C, Moulton E, Dormont D, Leger A, Pires C, Samson Y.
Aphasia outcome: the interactions between initial severity, lesion size and location.
*J Neurol*. 2019;266(6):1303–1309.
doi:10.1007/s00415-019-09259-3

> C. Initial severity × lesion size × site in one model (n=88);
> ties together `initial_aphasia_severity`, `lesion_volume` and the
> region findings.

## @Plowman2012  [seed]
Plowman E, Hentz B, Ellis C Jr.
Post-stroke aphasia prognosis: a review of patient-related and stroke-related factors.
*J Eval Clin Pract*. 2012;18(3):689–694.
doi:10.1111/j.1365-2753.2011.01650.x

> C. Prognosis review preceding Watila2015; covers age, sex,
> handedness, education, lesion variables. Belongs in `reviews/`.

## @Kristinsson2021  [seed]
Kristinsson S, Zhang W, Rorden C, Newman-Norlund R, Basilakos A, Bonilha L, Yourganov G, Xiao F, Hillis A, Fridriksson J.
Machine learning-based multimodal prediction of language improvements in chronic aphasia.
*Hum Brain Mapp*. 2021;42(6):1682–1698.
doi:10.1002/hbm.25321

> C. Treatment-gain prediction from lesion, connectome and fMRI
> (n=55); the predecessor of Kristinsson2025 and Teghipco2024.

## @Billot2022  [seed]
Billot A, Lai S, Varkanitsa M, Braun EJ, Rapp B, Parrish TB, Higgins J, Kurani AS, Caplan D, Thompson CK, Ishwar P, Betke M, Kiran S.
Multimodal neural and behavioral data predict response to rehabilitation in chronic poststroke aphasia.
*Stroke*. 2022;53(5):1606–1614.
doi:10.1161/STROKEAHA.121.036749

> C. Independent-cohort replication of multimodal response prediction
> (n=55, Boston).

## @Saur2006  [seed]
Saur D, Lange R, Baumgaertner A, Schraknepper V, Willmes K, Rijntjes M, Weiller C.
Dynamics of language reorganization after stroke.
*Brain*. 2006;129(6):1371–1384.
doi:10.1093/brain/awl090

> C. The three-phase recovery model (acute left hypoactivation →
> subacute right upregulation → chronic left re-normalisation,
> n=14). Framework for every recovery-phase finding.

## @Turkeltaub2011  [seed]
Turkeltaub PE, Messing S, Norise C, Hamilton RH.
Are networks for residual language function and recovery consistent across aphasic patients?
*Neurology*. 2011;76(20):1726–1734.
doi:10.1212/WNL.0b013e31821a44c1

> C. ALE meta-analysis of recovery activations (12 studies): spared
> left IFG, right IFG homologue, bilateral MTG. Belongs in `reviews/`.

## @Stockert2020  [seed]
Stockert A, Wawrzyniak M, Klingbeil J, Wrede K, Kümmerer D, Hartwigsen G, Kaller CP, Weiller C, Saur D.
Dynamics of language reorganization after left temporo-parietal and frontal stroke.
*Brain*. 2020;143(3):844–861.
doi:10.1093/brain/awaa023

> C. Longitudinal fMRI (n=34) showing reorganisation differs by
> lesion site — frontal vs temporo-parietal. Lets region entries carry
> a recovery-trajectory finding.

## @Hartwigsen2019  [seed]
Hartwigsen G, Saur D.
Neuroimaging of stroke recovery from aphasia – insights into plasticity of the human language network.
*NeuroImage*. 2019;190:14–31.
doi:10.1016/j.neuroimage.2017.11.056

> D. Review of recovery imaging; the narrative source for the RAG
> report's recovery paragraph.

## @Hickok2007  [seed]
Hickok G, Poeppel D.
The cortical organization of speech processing.
*Nat Rev Neurosci*. 2007;8(5):393–402.
doi:10.1038/nrn2113

> D. The dual-stream model Fridriksson2018 tests; `reviews/` should
> hold the framework the region entries are organised by.

## @Catani2008  [seed]
Catani M, Mesulam M.
The arcuate fasciculus and the disconnection theme in language and aphasia: history and current state.
*Cortex*. 2008;44(8):953–961.
doi:10.1016/j.cortex.2008.04.002

> D. Direct and indirect arcuate segments; the anatomical basis for
> splitting `left_arcuate_fasciculus` from `left_anterior_arcuate_fasciculus`
> and for the Geschwind1965 lineage.

## @Dick2012  [seed]
Dick AS, Tremblay P.
Beyond the arcuate fasciculus: consensus and controversy in the connectional anatomy of language.
*Brain*. 2012;135(12):3529–3550.
doi:10.1093/brain/aws222

> D. Tract-by-tract review (AF/SLF, IFOF, UF, ILF, MdLF, ECFS) — the
> glossary the JHU-tract extension of the decoder will need.

## @Binder2009  [seed]
Binder JR, Desai RH, Graves WW, Conant LL.
Where is the semantic system? A critical review and meta-analysis of 120 functional neuroimaging studies.
*Cereb Cortex*. 2009;19(12):2767–2796.
doi:10.1093/cercor/bhp055

> D. The semantic-network meta-analysis that Neurosynth term decoding
> in `decode_lesion.py` implicitly leans on; lets `semantics` cite a
> convergence source.

## @Benjamin2014  [seed]
Benjamin ML, Towler S, Garcia A, Park H, Sudhyadhom A, Harnish S, McGregor KM, Zlatar Z, Reilly JJ, Rosenbek JC, Gonzalez Rothi LJ, Crosson B.
A behavioral manipulation engages right frontal cortex during aphasia therapy.
*Neurorehabil Neural Repair*. 2014;28(6):545–553.
doi:10.1177/1545968313517754

> Added 2026-10-20. Intention (left-hand movement) manipulation during
> naming therapy shifts activity to right frontal cortex (fMRI, n=14).
> Candidate `ingredients/` entry; the lesion–response link for the
> `bilateral_middle_frontal_gyrus_recovery` region entry.

## @Brookshire2014  [seed]
Brookshire CE, Wilson JP, Nadeau SE, Gonzalez Rothi LJ, Kendall DL.
Frequency, nature, and predictors of alexia in a convenience sample of individuals with chronic aphasia.
*Aphasiology*. 2014;28(12):1464–1480.
doi:10.1080/02687038.2014.945389

> Added 2026-10-20. Alexia in 68 % of a chronic aphasia sample;
> predicted by aphasia severity and phonological impairment. The
> behavioural anchor for a future `alexia` impairment entry.

## @Wilson2019  [seed]
Wilson SM, Eriksson DK, Yen M, Demarco AT, Schneck SM, Lucanie JM.
Language mapping in aphasia.
*J Speech Lang Hear Res*. 2019;62(11):3937–3946.
doi:10.1044/2019_JSLHR-L-RSNP-19-0031

> Added 2026-10-20. Review of fMRI language mapping in aphasia and the
> methodological problems of recovery studies; belongs in `reviews/`.

## @WilsonHula2019  [seed]
Wilson SM, Hula WD.
Multivariate approaches to understanding aphasia and its neural substrates.
*Curr Neurol Neurosci Rep*. 2019;19(8):53.
doi:10.1007/s11910-019-0971-6

> Added 2026-10-20. Review of multivariate (PCA / factor) approaches to
> aphasia and their lesion correlates — the framework behind Butler2014,
> Halai2017, Alyahya2020 and Stefaniak2022. `reviews/`.

## @Mitchell2017  [seed]
Mitchell C, Bowen A, Tyson S, Butterfint Z, Conroy P.
Interventions for dysarthria due to stroke and other adult-acquired, non-progressive brain injury.
*Cochrane Database Syst Rev*. 2017;(1):CD002088.
doi:10.1002/14651858.CD002088.pub3

> Added 2026-10-20. Post-stroke dysarthria is the motor-speech
> neighbour of aphasia and co-occurs with it; a `reviews/` entry so the
> RAG report can separate the two when a lesion touches motor cortex.

## @Hazelton2022  [seed]
Hazelton C, Thomson K, Todhunter-Brown A, Campbell P, Chung CSY, Dorris L, Gillespie DC, Hunter SM, McGill K, Nicolson DJ, Williams LJ, Brady MC.
Interventions for perceptual disorders following stroke.
*Cochrane Database Syst Rev*. 2022;(11):CD007039.
doi:10.1002/14651858.CD007039.pub3

> Added 2026-10-20. Perceptual disorders (agnosias, neglect) after
> stroke — co-morbidities the lesion decoder will meet in the same
> masks. `reviews/`.

## @Laver2025  [seed]
Laver KE, Lange B, George S, Deutsch JE, Saposnik G, Chapman M, Crotty M.
Virtual reality for stroke rehabilitation.
*Cochrane Database Syst Rev*. 2025;(6):CD008349.
doi:10.1002/14651858.CD008349.pub5

> Added 2026-10-20. Post-stroke rehabilitation delivery; `reviews/`.

## @Pflugshaupt2009  [extracted]
Pflugshaupt T, Gutbrod K, Wurtz P, von Wartburg R, Nyffeler T, de Haan B, Karnath H-O, Müri RM.
About the role of visual field defects in pure alexia.
*Brain*. 2009;132(7):1907–1917.
doi:10.1093/brain/awp141

> Added 2026-10-20. Pure alexia after left occipito-temporal lesions
> (fusiform, inferior temporal, occipito-temporal sulcus), with the
> right hemianopia confound controlled. Extracted 2026-10-19 by
> `extract.py --batch`; drafts in `drafts/regions/`. Reading
> impairment, not aphasia proper — pairs with Brookshire2014.

## @Bates2003  [seed]
Bates E, Wilson SM, Saygin AP, Dick F, Sereno MI, Knight RT, Dronkers NF.
Voxel-based lesion–symptom mapping.
*Nat Neurosci*. 2003;6(5):448–450.
doi:10.1038/nn1050

> A. The method paper and the first fluency / comprehension VLSM
> (n=101): insula and anterior frontal for fluency, MTG for
> comprehension. Needed as the primary behind `fluency` and the
> `left_middle_temporal_gyrus` entry.

## @Baldo2011  [seed]
Baldo JV, Wilkins DP, Ogar J, Willock S, Dronkers NF.
Role of the precentral gyrus of the insula in complex articulatory movements.
*Cortex*. 2011;47:800–807.
doi:10.1016/j.cortex.2010.07.001

> A. VLSM (n=33) replicating Dronkers 1996 with a quantitative method;
> completes the insula pair with Hillis2004.

## @Yourganov2016  [seed]
Yourganov G, Fridriksson J, Rorden C, Gleichgerrcht E, Bonilha L.
Multivariate connectome-based symptom mapping in post-stroke patients: networks supporting language and speech.
*J Neurosci*. 2016;36(25):6668–6679.
doi:10.1523/JNEUROSCI.4396-15.2016

> A. Connectome-based LSM (n=90) for naming, fluency, comprehension,
> repetition. Primary for the white-matter entries, and the method
> Bonilha2014 relies on.

## @Matchin2020  [seed]
Matchin W, Basilakos A, Stark BC, den Ouden D-B, Fridriksson J, Hickok G.
Agrammatism and paragrammatism: a cortical double dissociation revealed by lesion-symptom mapping.
*Neurobiol Lang*. 2020;1(2):208–225.
doi:10.1162/nol_a_00010

> A. Agrammatism → IFG/insula, paragrammatism → posterior temporal
> (n=53). Splits `syntactic_processing` into the two deficits the
> decoder can actually tell apart.

## @Rapcsak2009  [seed]
Rapcsak SZ, Beeson PM, Henry ML, Leyden A, Kim E, Rising K, Andersen S, Cho H.
Phonological dyslexia and dysgraphia: cognitive mechanisms and neural substrates.
*Cortex*. 2009;45(5):575–591.
doi:10.1016/j.cortex.2008.04.006

> A. The KB has no reading or writing impairment; this is the
> lesion-anatomy anchor (perisylvian phonological network) for an
> `alexia` / `agraphia` entry.

## @Fridriksson2010Anomia  [seed]
Fridriksson J.
Preservation and modulation of specific left hemisphere regions is vital for treated recovery from anomia in stroke.
*J Neurosci*. 2010;30(35):11558–11564.
doi:10.1523/JNEUROSCI.2227-10.2010

> B/C. Anomia-treatment response predicted by preserved left frontal
> and temporal tissue (n=26). The region→treatment-response link
> CALMaR exists to make.

## @Karnath2018  [seed]
Karnath H-O, Sperber C, Rorden C.
Mapping human brain lesions and their functional consequences.
*NeuroImage*. 2018;165:180–189.
doi:10.1016/j.neuroimage.2017.10.028

> D. Methods review: what lesion–symptom mapping can and cannot
> infer (vascular bias, displacement of peaks). The caveat text the
> RAG report's research-only notice should be able to cite.

## @vanderMeulen2014  [seed]
van der Meulen I, van de Sandt-Koenderman WME, Heijenbrok-Kal MH, Visch-Brink EG, Ribbers GM.
The efficacy and timing of melodic intonation therapy in subacute aphasia.
*Neurorehabil Neural Repair*. 2014;28(6):536–544.
doi:10.1177/1545968313517753

> Added 2026-10-20. The MIT RCT (n=27, subacute) that vanderMeulen2012
> announced; the treatment-response primary `melodic_intonation_therapy`
> lacks. (DOI corrected from the 2026-10-19 list, which pointed at the
> adjacent article, Benjamin2014.)

## @Kasdan2025  [seed]
Kasdan AV, Casilio M, Bryan K, Jacoby N, Fram NR, Walljasper L, Levy DF, de Riesthal M, Gordon RL, Wilson SM.
Neural correlates of rhythm in post-stroke aphasia.
*Neurobiol Lang*. 2025;6:nol.a.9.
doi:10.1162/nol.a.9

> Added 2026-10-20. Lesion correlates of rhythm perception and
> production in aphasia — the lesion side of the `rhythmic_hand_tapping`
> / `melodic_intoning` ingredients.

---

## Seed references (added 2026-10-21): atlas-mapping evidence gaps

> Suggested for extraction to fill the gaps listed in
> `atlas_mapping/evidence_gaps.yaml` (see `atlas_mapping/EVIDENCE_GAPS.md`).
> Bibliographic details were checked against publisher or PubMed Central
> records on 2026-10-21; a missing DOI was not confirmed and should be
> looked up before download. Already-seeded papers for the same gaps:
> @Kummerer2013 (extreme capsule), @Hillis2004 (insula vs IFG).

## @Hillis2002  [seed]
Hillis AE, Wityk RJ, Barker PB, Beauchamp NJ, Gailloud P, Murphy K, Cooper O, Metter EJ.
Subcortical aphasia and neglect in acute stroke: the role of cortical hypoperfusion.
*Brain*. 2002;125(5):1094–1104.

> Gap thalamus_basal_ganglia. Acute DWI/PWI (n=115): aphasia after
> subcortical infarcts largely explained by cortical hypoperfusion and
> resolving with reperfusion. Region-level evidence for putamen, caudate,
> thalamus; DOI not confirmed.

## @Baldo2013  [seed]
Baldo JV, Arévalo A, Patterson JP, Dronkers NF.
Grey and white matter correlates of picture naming: evidence from a voxel-based lesion analysis of the Boston Naming Test.
*Cortex*. 2013;49(3):658–667.
doi:10.1016/j.cortex.2012.03.001

> Gap basal_temporal_naming. VLSM of BNT naming in a large chronic LH
> cohort: anterior-to-posterior MTG/STG, underlying white matter and
> inferior parietal cortex (PMC3613759).

## @Han2013  [seed]
Han Z, Ma Y, Gong G, He Y, Caramazza A, Bi Y.
White matter structural connectivity underlying semantic processing: evidence from brain damaged patients.
*Brain*. 2013;136(10):2952–2965.
doi:10.1093/brain/awt205

> Gap anterior_thalamic_radiation_ifof_semantics. n=76: lesion load and FA
> of left IFOF, anterior thalamic radiation and uncinate fasciculus
> correlate with semantic impairment across three tasks.

## @Sebastian2014  [seed]
Sebastian R, Schein MG, Davis C, Gomez Y, Newhart M, Oishi K, Hillis AE.
Aphasia or neglect after thalamic stroke: the various ways they may be related to cortical hypoperfusion.
*Front Neurol*. 2014;5:231.
doi:10.3389/fneur.2014.00231

> Gap thalamus_basal_ganglia. Acute thalamic infarcts: aphasia after left
> thalamic lesions mostly without cortical hypoperfusion (unlike other
> subcortical infarcts).

## @Xing2016  [seed]
Xing S, et al.; senior author Turkeltaub PE.
Right hemisphere grey matter structure and language outcomes in chronic left hemisphere stroke.
*Brain*. 2016;139(1):227–241.
doi:10.1093/brain/awv323

> Gap right_hemisphere. n=32 chronic LH stroke (WAB-R): right
> temporoparietal grey matter volume relates to speech, naming and
> repetition beyond lesion burden. Full author list to be copied from
> the article.

## @Li2017  [seed]
Li M, Zhang Y, Song L, Huang R, Ding J, Fang Y, Xu Y, Han Z.
Structural connectivity subserving verbal fluency revealed by lesion-behavior mapping in stroke patients.
*Neuropsychologia*. 2017;101:85–96.
doi:10.1016/j.neuropsychologia.2017.05.008

> Gaps frontal_aslant_sma_fluency and anterior_thalamic_radiation_ifof_semantics.
> n=51: integrity of left anterior thalamic radiation, IFOF, uncinate, SLF
> and frontal aslant tract relates to semantic and phonological fluency,
> beyond lesion volume.

## @Oeckel2021  [seed]
Martinez Oeckel A, Rijntjes M, Glauche V, Kümmerer D, Kaller CP, Egger K, Weiller C.
The extreme capsule and aphasia: proof-of-concept of a new way relating structure to neurological symptoms.
*Brain Commun*. 2021;3:fcab040.
doi:10.1093/braincomms/fcab040

> Gap extreme_capsule_ventral_stream. n=123 acute LH stroke without
> cortical language-area lesions: >15 % extreme-capsule damage strongly
> predicts aphasia (OR 16.4); arcuate damage does not.

## @Fritsch2022  [seed]
Fritsch M, Rangus I, Nolte CH.
Thalamic aphasia: a review.
*Curr Neurol Neurosci Rep*. 2022;22(12):855–865.
doi:10.1007/s11910-022-01242-2

> Gap thalamus_basal_ganglia. Review: mostly mild lexical-semantic
> deficits whose profile varies with the thalamic nuclei involved.
> Extract as a review.

---

## Registered automatically

> Entries written by register_papers.py from the PDF's DOI. Each says when; none has been checked by a person until its note is replaced.

## @Brady2022  [seed]
The RELEASE Collaborators, Brady MC, Ali M, VandenBerg K, Williams LJ, Williams LR, Abo M, Becker F, Bowen A, Brandenburg C, Breitenstein C, Bruehl S, et al.
Precision rehabilitation for aphasia by patient age, sex, aphasia severity, and time since stroke? A prespecified, systematic review-based, individual participant data, network, subgroup meta-analysis.
*International Journal of Stroke*. 2022;17(10):1067-1077.
doi:10.1177/17474930221097477

> Registered automatically from the PDF's DOI via Crossref on 2026-10-21 (file: Brandenburg2050354-Published.pdf). Check the entry; add a note on why the paper is in the KB.

## @Ochfeld2010  [seed]
Ochfeld E, Newhart M, Molitoris J, Leigh R, Cloutman L, Davis C, Crinion J, Hillis AE.
Ischemia in Broca Area Is Associated With Broca Aphasia More Reliably in Acute Than in Chronic Stroke.
*Stroke*. 2010;41(2):325-330.
doi:10.1161/strokeaha.109.570374

> Registered automatically from the PDF's DOI via Crossref on 2026-10-21 (file: 00007670-201002000-00034.pdf). Check the entry; add a note on why the paper is in the KB.

## @Corbetta2015  [seed]
Corbetta M, Ramsey L, Callejas A, Baldassarre A, Hacker CD, Siegel JS, Astafiev SV, Rengachary J, Zinn K, Lang CE, Connor LT, Fucetola R, et al.
Common Behavioral Clusters and Subcortical Anatomy in Stroke.
*Neuron*. 2015;85(5):927-941.
doi:10.1016/j.neuron.2015.02.027

> Registered automatically from the PDF's DOI via Crossref on 2026-10-21 (file: 1-s2.0-S0896627315001427-main.pdf). Check the entry; add a note on why the paper is in the KB.

## @Lazar2008  [seed]
Lazar RM, Speizer AE, Festa JR, Krakauer JW, Marshall RS.
Variability in language recovery after first-time stroke.
*Journal of Neurology, Neurosurgery &amp; Psychiatry*. 2008;79(5):530-534.
doi:10.1136/jnnp.2007.122457

> Registered automatically from the PDF's DOI via Crossref on 2026-10-21 (file: 530.full.pdf). Check the entry; add a note on why the paper is in the KB.

## @Hillis2006  [seed]
Hillis AE, Kleinman JT, Newhart M, Heidler-Gary J, Gottesman R, Barker PB, Aldrich E, Llinas R, Wityk R, Chaudhry P.
Restoring Cerebral Blood Flow Reveals Neural Regions Critical for Naming.
*J. Neurosci.*. 2006;26(31):8069-8073.
doi:10.1523/jneurosci.2088-06.2006

> Registered automatically from the PDF's DOI via Crossref on 2026-10-21 (file: 8069.full.pdf). Check the entry; add a note on why the paper is in the KB.

## @Hillis2001  [seed]
Hillis AE, Wityk RJ, Tuffiash E, Beauchamp NJ, Jacobs MA, Barker PB, Selnes OA.
Hypoperfusion of Wernicke's area predicts severity of semantic deficit in acute stroke.
*Annals of Neurology*. 2001;50(5):561-566.
doi:10.1002/ana.1265

> Registered automatically from the PDF's DOI via Crossref on 2026-10-21 (file: Annals of Neurology - 2001 - Hillis - Hypoperfusion of Wernicke s area predicts severity of semantic deficit in acute.pdf). Check the entry; add a note on why the paper is in the KB.

## @Pedersen1995  [seed]
Pedersen PM, Stig Jørgensen H, Nakayama H, Raaschou HO, Olsen TS.
Aphasia in acute stroke: Incidence, determinants, and recovery.
*Annals of Neurology*. 1995;38(4):659-666.
doi:10.1002/ana.410380416

> Registered automatically from the PDF's DOI via Crossref on 2026-10-21 (file: Annals of Neurology - October 1995 - Pedersen - Aphasia in acute stroke  Incidence  determinants  and recovery.pdf). Check the entry; add a note on why the paper is in the KB.

## @Laska2001  [seed]
Laska AC, Hellblom A, Murray V, Kahan T, Von Arbin M.
Aphasia in acute stroke and relation to outcome.
*Journal of Internal Medicine*. 2001;249(5):413-422.
doi:10.1046/j.1365-2796.2001.00812.x

> Registered automatically from the PDF's DOI via Crossref on 2026-10-21 (file: Journal of Internal Medicine - 2001 - Laska - Aphasia in acute stroke and relation to outcome (1).pdf). Check the entry; add a note on why the paper is in the KB.

## @Johnson2019  [seed]
Johnson L, Basilakos A, Yourganov G, Cai B, Bonilha L, Rorden C, Fridriksson J.
Progression of Aphasia Severity in the Chronic Stages of Stroke.
*Am J Speech Lang Pathol*. 2019;28(2):639-649.
doi:10.1044/2018_ajslp-18-0123

> Registered automatically from the PDF's DOI via Crossref on 2026-10-21 (file: Progression_of_Aphasia_Severit.pdf). Check the entry; add a note on why the paper is in the KB.

## @Wilson2023  [seed]
Wilson SM, Entrup JL, Schneck SM, Onuscheck CF, Levy DF, Rahman M, Willey E, Casilio M, Yen M, Brito AC, Kam W, Davis LT, et al.
Recovery from aphasia in the first year after stroke.
*Brain*. 2023;146(3):1021-1039.
doi:10.1093/brain/awac129

> Registered automatically from the PDF's DOI via Crossref on 2026-10-21 (file: awac129.pdf). Check the entry; add a note on why the paper is in the KB.

## @Godecke2021  [seed]
Godecke E, Armstrong E, Rai T, Ciccone N, Rose ML, Middleton S, Whitworth A, Holland A, Ellery F, Hankey GJ, Cadilhac DA, Bernhardt J, et al.
A randomized control trial of intensive aphasia therapy after acute stroke: The Very Early Rehabilitation for SpEech (VERSE) study.
*International Journal of Stroke*. 2021;16(5):556-572.
doi:10.1177/1747493020961926

> Registered automatically from the PDF's DOI via Crossref on 2026-10-21 (file: godecke-et-al-2020-a-randomized-control-trial-of-intensive-aphasia-therapy-after-acute-stroke-the-very-early.pdf). Check the entry; add a note on why the paper is in the KB.

## @Nouwens2017  [seed]
Nouwens F, de Lau LML, Visch-Brink EG, van de Sandt-Koenderman WME(, Lingsma HF, Goosen S, Blom DMJ, Koudstaal PJ, Dippel DWJ.
Efficacy of early cognitive-linguistic treatment for aphasia due to stroke: A randomised controlled trial (Rotterdam Aphasia Therapy Study-3).
*European Stroke Journal*. 2017;2(2):126-136.
doi:10.1177/2396987317698327

> Registered automatically from the PDF's DOI via Crossref on 2026-10-21 (file: nouwens-et-al-2017-efficacy-of-early-cognitive-linguistic-treatment-for-aphasia-due-to-stroke-a-randomised-controlled.pdf). Check the entry; add a note on why the paper is in the KB.

## @Ramsey2017  [seed]
Ramsey LE, Siegel JS, Lang CE, Strube M, Shulman GL, Corbetta M.
Behavioural clusters and predictors of performance during recovery from stroke.
*Nat Hum Behav*. 2017;1(3).
doi:10.1038/s41562-016-0038

> Registered automatically from the PDF's DOI via Crossref on 2026-10-21 (file: s41562-016-0038.pdf). Check the entry; add a note on why the paper is in the KB.

## @Siegel2016  [seed]
Siegel JS, Ramsey LE, Snyder AZ, Metcalf NV, Chacko RV, Weinberger K, Baldassarre A, Hacker CD, Shulman GL, Corbetta M.
Disruptions of network connectivity predict impairment in multiple behavioral domains after stroke.
*Proc. Natl. Acad. Sci. U.S.A.*. 2016;113(30).
doi:10.1073/pnas.1521083113

> Registered automatically from the PDF's DOI via Crossref on 2026-10-21 (file: 26470986.pdf). Check the entry; add a note on why the paper is in the KB.

