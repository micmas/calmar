# Atlas → knowledge-base mapping (generated)

Generated from `units.yaml` and `kb_regions.yaml` by `python atlas_mapping.py --write-table`;
do not edit by hand. Rules and decisions: [README.md](README.md). ⚑ = judgement call to review.

## Anatomical units

| Unit | Atlas | Labels | Basis |
|---|---|---|---|
| `ifg_pars_opercularis` Inferior frontal gyrus, pars opercularis (BA 44) | HarvardOxford | Inferior Frontal Gyrus, pars opercularis (side from voxels) | HarvardOxford label of the same structure. |
| `ifg_pars_triangularis` Inferior frontal gyrus, pars triangularis (BA 45) | HarvardOxford | Inferior Frontal Gyrus, pars triangularis (side from voxels) | HarvardOxford label of the same structure. |
| `ifg_pars_orbitalis` Inferior frontal gyrus, pars orbitalis (BA 47) | AAL | left: Frontal_Inf_Orb_L / right: Frontal_Inf_Orb_R | HarvardOxford has no pars orbitalis (only the whole Frontal Orbital Cortex); AAL's inferior frontal orbital part is the pars orbitalis. |
| `frontal_operculum` Frontal operculum | HarvardOxford | Frontal Opercular Cortex (side from voxels) | HarvardOxford label of the same structure. |
| `middle_frontal_gyrus` Middle frontal gyrus | HarvardOxford | Middle Frontal Gyrus (side from voxels) | HarvardOxford label of the same structure. |
| `superior_frontal_gyrus` Superior frontal gyrus | HarvardOxford | Superior Frontal Gyrus (side from voxels) | HarvardOxford label of the same structure. |
| `superior_frontal_gyrus_medial` Superior frontal gyrus, medial part | AAL | left: Frontal_Sup_Medial_L / right: Frontal_Sup_Medial_R | AAL separates the medial superior frontal gyrus; HarvardOxford does not. |
| `frontal_medial_cortex` Frontal medial cortex | HarvardOxford | Frontal Medial Cortex (side from voxels) | HarvardOxford label of the same structure. |
| `frontal_pole` Frontal pole | HarvardOxford | Frontal Pole (side from voxels) | HarvardOxford label of the same structure. |
| `supplementary_motor_area` Supplementary motor area | HarvardOxford | Juxtapositional Lobule Cortex (formerly Supplementary Motor Cortex) (side from voxels) | HarvardOxford's juxtapositional lobule is its supplementary motor cortex. |
| `paracingulate_gyrus` Paracingulate gyrus | HarvardOxford | Paracingulate Gyrus (side from voxels) | HarvardOxford label of the same structure. |
| `precentral_gyrus` Precentral gyrus | HarvardOxford | Precentral Gyrus (side from voxels) | HarvardOxford label of the same structure. |
| `central_operculum` Central (Rolandic) operculum | HarvardOxford | Central Opercular Cortex (side from voxels) | HarvardOxford's central opercular cortex is the Rolandic operculum. |
| `insula` Insula | HarvardOxford | Insular Cortex (side from voxels) | HarvardOxford label of the same structure. |
| `parietal_operculum` Parietal operculum | HarvardOxford | Parietal Opercular Cortex (side from voxels) | HarvardOxford label of the same structure. |
| `temporal_pole` Temporal pole | HarvardOxford | Temporal Pole (side from voxels) | HarvardOxford label of the same structure. |
| `temporal_pole_superior` Temporal pole, superior temporal part | AAL | left: Temporal_Pole_Sup_L / right: Temporal_Pole_Sup_R | AAL divides the temporal pole into superior and middle temporal parts; HarvardOxford does not. |
| `temporal_pole_middle` Temporal pole, middle temporal part | AAL | left: Temporal_Pole_Mid_L / right: Temporal_Pole_Mid_R | AAL divides the temporal pole into superior and middle temporal parts; HarvardOxford does not. |
| `stg_anterior` Superior temporal gyrus, anterior | HarvardOxford | Superior Temporal Gyrus, anterior division (side from voxels) | HarvardOxford label of the same structure. |
| `stg_posterior` Superior temporal gyrus, posterior | HarvardOxford | Superior Temporal Gyrus, posterior division (side from voxels) | HarvardOxford label of the same structure. |
| `planum_polare` Planum polare | HarvardOxford | Planum Polare (side from voxels) | HarvardOxford label of the same structure. |
| `heschls_gyrus` Heschl's gyrus | HarvardOxford | Heschl's Gyrus (includes H1 and H2) (side from voxels) | HarvardOxford label of the same structure. |
| `planum_temporale` Planum temporale | HarvardOxford | Planum Temporale (side from voxels) | HarvardOxford label of the same structure. |
| `mtg_anterior` Middle temporal gyrus, anterior | HarvardOxford | Middle Temporal Gyrus, anterior division (side from voxels) | HarvardOxford label of the same structure. |
| `mtg_posterior` Middle temporal gyrus, posterior | HarvardOxford | Middle Temporal Gyrus, posterior division (side from voxels) | HarvardOxford label of the same structure. |
| `mtg_temporooccipital` Middle temporal gyrus, temporo-occipital part | HarvardOxford | Middle Temporal Gyrus, temporooccipital part (side from voxels) | HarvardOxford label of the same structure. |
| `itg` Inferior temporal gyrus | HarvardOxford | Inferior Temporal Gyrus, anterior division; Inferior Temporal Gyrus, posterior division; Inferior Temporal Gyrus, temporooccipital part (side from voxels) | The three HarvardOxford inferior temporal gyrus divisions together. |
| `itg_temporooccipital` Inferior temporal gyrus, temporo-occipital part | HarvardOxford | Inferior Temporal Gyrus, temporooccipital part (side from voxels) | HarvardOxford label of the same structure. |
| `fusiform_gyrus` Fusiform gyrus | HarvardOxford | Temporal Fusiform Cortex, anterior division; Temporal Fusiform Cortex, posterior division; Temporal Occipital Fusiform Cortex (side from voxels) | HarvardOxford's temporal and temporo-occipital fusiform cortex together (its separate Occipital Fusiform Gyrus is excluded). |
| `temporal_fusiform_anterior` Temporal fusiform cortex, anterior | HarvardOxford | Temporal Fusiform Cortex, anterior division (side from voxels) | HarvardOxford label of the same structure. |
| `temporooccipital_fusiform` Temporo-occipital fusiform cortex | HarvardOxford | Temporal Occipital Fusiform Cortex (side from voxels) | HarvardOxford label of the same structure. |
| `hippocampus` Hippocampus | AAL | left: Hippocampus_L / right: Hippocampus_R | Not in the cortical HarvardOxford atlas; AAL label of the same structure. |
| `postcentral_gyrus` Postcentral gyrus | HarvardOxford | Postcentral Gyrus (side from voxels) | HarvardOxford label of the same structure. |
| `smg_anterior` Supramarginal gyrus, anterior | HarvardOxford | Supramarginal Gyrus, anterior division (side from voxels) | HarvardOxford label of the same structure. |
| `smg_posterior` Supramarginal gyrus, posterior | HarvardOxford | Supramarginal Gyrus, posterior division (side from voxels) | HarvardOxford label of the same structure. |
| `angular_gyrus` Angular gyrus | HarvardOxford | Angular Gyrus (side from voxels) | HarvardOxford label of the same structure. |
| `superior_parietal_lobule` Superior parietal lobule | HarvardOxford | Superior Parietal Lobule (side from voxels) | HarvardOxford label of the same structure. |
| `precuneus` Precuneus | HarvardOxford | Precuneous Cortex (side from voxels) | HarvardOxford label of the same structure. |
| `posterior_cingulate` Posterior cingulate gyrus | HarvardOxford | Cingulate Gyrus, posterior division (side from voxels) | HarvardOxford label of the same structure. |
| `lateral_occipital_superior` Lateral occipital cortex, superior | HarvardOxford | Lateral Occipital Cortex, superior division (side from voxels) | HarvardOxford label of the same structure. |
| `lingual_gyrus` Lingual gyrus | HarvardOxford | Lingual Gyrus (side from voxels) | HarvardOxford label of the same structure. |
| `putamen` Putamen | AAL | left: Putamen_L / right: Putamen_R | Not in the cortical HarvardOxford atlas; AAL label of the same structure. |
| `pallidum` Globus pallidus | AAL | left: Pallidum_L / right: Pallidum_R | Not in the cortical HarvardOxford atlas; AAL label of the same structure. |
| `slf` Superior longitudinal fasciculus (fronto-parietal part) | JHU | left: Superior longitudinal fasciculus L / right: Superior longitudinal fasciculus R | JHU's superior longitudinal fasciculus label (the fronto-parietal body of the SLF). |
| `ilf` Inferior longitudinal fasciculus | JHU | left: Inferior longitudinal fasciculus L / right: Inferior longitudinal fasciculus R | JHU label of the same tract. |
| `ifof` Inferior fronto-occipital fasciculus | JHU | left: Inferior fronto-occipital fasciculus L / right: Inferior fronto-occipital fasciculus R | JHU label of the same tract. |
| ⚑ `forceps` Corpus callosum (forceps major and minor) | JHU | Forceps major; Forceps minor (side from voxels) | Midline labels without a side in JHU, so the side is taken from the lesion voxels. JHU labels only the anterior and posterior callosal radiations (forceps minor, major), not the callosal body; a lesion in the body is not measured. |
| `uncinate_fasciculus` Uncinate fasciculus | XTRACT | left: Uncinate Fasciculus L / right: Uncinate Fasciculus R | XTRACT label of the same tract. JHU lists an uncinate label, but its 50 %-threshold image has no voxels for it (nor for the cingulum or the temporal SLF), so it could never be damaged. |
| `arcuate_fasciculus` Arcuate fasciculus | XTRACT | left: Arcuate Fasciculus L / right: Arcuate Fasciculus R | XTRACT label of the same tract (the whole arcuate; its segments are not separated). |
| `slf_iii` Superior longitudinal fasciculus III (ventral, fronto-parietal) | XTRACT | left: Superior Longitudinal Fasciculus 3 L / right: Superior Longitudinal Fasciculus 3 R | XTRACT label of the same tract; SLF III links the inferior frontal gyrus with the supramarginal gyrus. |
| `frontal_aslant_tract` Frontal aslant tract | XTRACT | left: Frontal Aslant Tract L / right: Frontal Aslant Tract R | XTRACT label of the same tract. |
| `middle_longitudinal_fasciculus` Middle longitudinal fasciculus | XTRACT | left: Middle Longitudinal Fasciculus L / right: Middle Longitudinal Fasciculus R | XTRACT label of the same tract. |
| `optic_radiation` Optic radiation | XTRACT | left: Optic Radiation L / right: Optic Radiation R | XTRACT label of the same tract. |

## Knowledge-base regions

| Region | Side | Units | Basis |
|---|---|---|---|
| ⚑ `bilateral_middle_frontal_gyrus_recovery` | both | `middle_frontal_gyrus` | The entry concerns the middle frontal gyrus of both hemispheres. Its aliases also list right temporo-occipital MTG and right supramarginal gyrus, which are not mapped here. |
| ⚑ `corpus_callosum` | both | `forceps` | Only the callosal forceps are labelled in JHU (units.yaml, forceps). |
| `ho-cort_44` | left | `ifg_pars_opercularis` | Legacy entry for HarvardOxford cortical label 44 region (IFG pars opercularis, BA 44); the entry is the left one. |
| `left_angular_gyrus` | left | `angular_gyrus` | Same structure (BA 39). |
| ⚑ `left_anterior_arcuate_fasciculus` | left | `slf_iii` | The anterior segment (Catani et al. 2005) links the inferior frontal and inferior parietal cortex: in XTRACT, SLF III. |
| `left_anterior_middle_temporal_gyrus` | left | `mtg_anterior` | Same structure. |
| `left_anterior_supramarginal_gyrus` | left | `smg_anterior` | Same structure. |
| ⚑ `left_anterior_temporal_lobe` | left | `temporal_pole`, `stg_anterior`, `mtg_anterior` | Anterior temporal lobe as the entry defines it (aliases ATL, temporal pole) = temporal pole with the anterior superior and middle temporal gyri. |
| ⚑ `left_anterior_temporal_lobe__Robson2014` | left | `temporal_pole`, `stg_anterior`, `mtg_anterior`, `temporal_fusiform_anterior` | Robson et al. 2014 region; its aliases add the anterior fusiform gyrus to the anterior temporal lobe. |
| `left_arcuate_fasciculus` | left | `arcuate_fasciculus` | XTRACT arcuate fasciculus. |
| `left_arcuate_fasciculus_slf` | left | `arcuate_fasciculus`, `slf` | The entry combines the arcuate and the SLF ("dorsal language pathway"), so XTRACT's arcuate and JHU's SLF. |
| `left_central_opercular_cortex` | left | `central_operculum` | Same structure. |
| ⚑ `left_dorsolateral_prefrontal_cortex` | left | `middle_frontal_gyrus` | The dorsolateral prefrontal cortex (BA 9/46) lies mainly on the middle frontal gyrus; the atlases have no DLPFC label. |
| ⚑ `left_dorsomedial_prefrontal_cortex` | left | `superior_frontal_gyrus_medial` | The dorsomedial prefrontal cortex is the medial superior frontal gyrus (AAL Frontal_Sup_Medial). |
| `left_frontal_aslant_tract` | left | `frontal_aslant_tract` | XTRACT frontal aslant tract. |
| `left_fusiform_gyrus` | left | `fusiform_gyrus` | Same structure. |
| `left_heschls_gyrus` | left | `heschls_gyrus` | Same structure. |
| `left_hippocampus` | left | `hippocampus` | Same structure. |
| `left_ifg_pars_opercularis` | left | `ifg_pars_opercularis` | Same structure (BA 44). |
| `left_ifg_pars_orbitalis` | left | `ifg_pars_orbitalis` | Same structure (BA 47). |
| `left_ifg_pars_triangularis` | left | `ifg_pars_triangularis` | Same structure (BA 45). |
| `left_inferior_frontal_occipital_fasciculus` | left | `ifof` | Spelling variant of the inferior fronto-occipital fasciculus. |
| `left_inferior_fronto_occipital_fasciculus` | left | `ifof` | Same tract. |
| `left_inferior_longitudinal_fasciculus` | left | `ilf` | Same tract. |
| `left_inferior_temporal_gyrus` | left | `itg` | Same structure. |
| `left_insula` | left | `insula` | Same structure. |
| ⚑ `left_long_segment_arcuate_fasciculus` | left | `arcuate_fasciculus` | The long (direct fronto-temporal) segment is part of XTRACT's arcuate, which does not separate the segments. |
| `left_middle_frontal_gyrus` | left | `middle_frontal_gyrus` | Same structure. |
| `left_middle_longitudinal_fasciculus` | left | `middle_longitudinal_fasciculus` | XTRACT middle longitudinal fasciculus. |
| `left_middle_temporal_gyrus` | left | `mtg_anterior`, `mtg_posterior`, `mtg_temporooccipital` | Whole middle temporal gyrus. |
| ⚑ `left_occipito_temporal_sulcus` | left | `itg_temporooccipital`, `temporooccipital_fusiform` | The occipito-temporal sulcus has no atlas label; it separates the inferior temporal and fusiform gyri, whose temporo-occipital parts are used. |
| `left_optic_radiations` | left | `optic_radiation` | XTRACT optic radiation. |
| `left_pallidum` | left | `pallidum` | Same structure. |
| `left_paracingulate_gyrus` | left | `paracingulate_gyrus` | Same structure. |
| ⚑ `left_parietal_association_cortex` | left | `smg_anterior`, `smg_posterior`, `angular_gyrus`, `superior_parietal_lobule` | Parietal association cortex = inferior parietal lobule (supramarginal, angular) and superior parietal lobule. |
| `left_parietal_operculum_cortex` | left | `parietal_operculum` | Same structure. |
| `left_planum_temporale` | left | `planum_temporale` | Same structure. |
| `left_postcentral_gyrus` | left | `postcentral_gyrus` | Same structure. |
| ⚑ `left_posterior_arcuate_fasciculus` | left | `arcuate_fasciculus` | The posterior (temporo-parietal) segment has no XTRACT label; XTRACT's arcuate is the closest tract. |
| `left_posterior_cingulate_gyrus` | left | `posterior_cingulate` | Same structure. |
| `left_posterior_middle_temporal_gyrus` | left | `mtg_posterior` | Same structure (the temporo-occipital part is not included). |
| ⚑ `left_posterior_planum_temporale_spt` | left | `planum_temporale` | Area Spt lies in the posterior planum temporale, which the atlases do not subdivide. |
| `left_posterior_stg` | left | `stg_posterior` | Same structure. |
| `left_posterior_superior_temporal_gyrus` | left | `stg_posterior` | Same structure (long form of left_posterior_stg). |
| `left_posterior_supramarginal_gyrus` | left | `smg_posterior` | Same structure. |
| `left_pre_central_gyrus` | left | `precentral_gyrus` | Spelling variant of left_precentral_gyrus. |
| `left_precentral_gyrus` | left | `precentral_gyrus` | Same structure. |
| ⚑ `left_precentral_gyrus_insula` | left | `insula` | The "precentral gyrus of the insula" (Dronkers 1996, apraxia of speech) is the superior precentral gyrus OF THE INSULA, not the motor precentral gyrus; the atlases do not subdivide the insula, so the whole insula is used. |
| `left_precuneus` | left | `precuneus` | Same structure. |
| ⚑ `left_premotor_cortex` | left | `precentral_gyrus`, `supplementary_motor_area` | Premotor cortex (BA 6) has no atlas label; it spans the anterior precentral gyrus laterally and the supplementary motor area medially. |
| `left_putamen` | left | `putamen` | Same structure. |
| `left_rolandic_operculum` | left | `central_operculum` | The Rolandic operculum is HarvardOxford's central opercular cortex. |
| `left_superior_frontal_gyrus` | left | `superior_frontal_gyrus` | Same structure. |
| `left_superior_lateral_occipital_cortex` | left | `lateral_occipital_superior` | Same structure. |
| `left_superior_longitudinal_fasciculus` | left | `slf` | Same tract. |
| `left_superior_temporal_gyrus` | left | `stg_anterior`, `stg_posterior` | Whole superior temporal gyrus (aliases name both anterior and posterior parts). |
| ⚑ `left_superior_temporal_gyrus__Leff2009` | left | `stg_posterior`, `planum_temporale` | Leff et al. 2009 region (aliases posterior STG, posterior superior temporal sulcus, planum temporale); the sulcus has no atlas label. |
| `left_superior_temporal_gyrus_wernicke` | left | `stg_posterior`, `planum_temporale` | Wernicke's area as the entry defines it (aliases: posterior STG, planum temporale). |
| `left_superior_temporal_gyrus_wernickes` | left | `stg_posterior`, `planum_temporale` | Variant of left_superior_temporal_gyrus_wernicke (mid-posterior STG). |
| ⚑ `left_superior_temporal_sulcus` | left | `stg_posterior`, `mtg_posterior` | The superior temporal sulcus has no atlas label; it lies between the superior and middle temporal gyri, whose posterior divisions are used. |
| `left_supplementary_motor_area` | left | `supplementary_motor_area` | Same structure. |
| `left_supramarginal_gyrus` | left | `smg_anterior`, `smg_posterior` | Whole supramarginal gyrus. |
| ⚑ `left_supramarginal_gyrus_premotor` | left | `smg_anterior`, `smg_posterior`, `postcentral_gyrus` | The entry groups the supramarginal gyrus with the inferior postcentral gyrus (aliases). |
| `left_temporal_fusiform_cortex_anterior` | left | `temporal_fusiform_anterior` | Same structure. |
| `left_temporal_lobe` | left | `temporal_pole`, `stg_anterior`, `stg_posterior`, `planum_polare`, `heschls_gyrus`, `planum_temporale`, `mtg_anterior`, `mtg_posterior`, `mtg_temporooccipital`, `itg`, `fusiform_gyrus` | All lateral and basal temporal units. |
| `left_temporal_pole` | left | `temporal_pole` | Same structure. |
| `left_temporal_pole_mtg` | left | `temporal_pole_middle` | Middle temporal part of the temporal pole (AAL Temporal_Pole_Mid). |
| `left_temporal_pole_stg` | left | `temporal_pole_superior` | Superior temporal part of the temporal pole (AAL Temporal_Pole_Sup). |
| ⚑ `left_temporobasal__Goldenberg1994` | left | `itg`, `fusiform_gyrus` | Basal temporal cortex (Goldenberg 1994) = inferior temporal and fusiform gyri. |
| ⚑ `left_temporoparietal_junction` | left | `stg_posterior`, `smg_posterior`, `angular_gyrus` | The temporoparietal junction has no atlas label; taken as the posterior superior temporal, posterior supramarginal and angular gyri. |
| `left_uncinate_fasciculus` | left | `uncinate_fasciculus` | Same tract. |
| `right_anterior_middle_temporal_gyrus` | right | `mtg_anterior` | Same structure, right hemisphere. |
| `right_anterior_superior_temporal_gyrus` | right | `stg_anterior` | Same structure, right hemisphere. |
| `right_arcuate_fasciculus` | right | `arcuate_fasciculus` | XTRACT arcuate fasciculus, right hemisphere. |
| ⚑ `right_dlpfc` | right | `middle_frontal_gyrus` | As left_dorsolateral_prefrontal_cortex, right hemisphere. |
| `right_ifg_pars_opercularis` | right | `ifg_pars_opercularis` | Same structure, right hemisphere. |
| `right_ifg_pars_triangularis` | right | `ifg_pars_triangularis` | Same structure, right hemisphere. |
| ⚑ `right_lateral_frontal_cortex` | right | `ifg_pars_opercularis`, `ifg_pars_triangularis`, `middle_frontal_gyrus` | Lateral frontal cortex taken as the inferior and middle frontal gyri. |
| `right_lingual_gyrus` | right | `lingual_gyrus` | Same structure, right hemisphere. |
| ⚑ `right_medial_frontal_cortex` | right | `frontal_medial_cortex`, `superior_frontal_gyrus_medial` | Medial frontal cortex = HarvardOxford frontal medial cortex plus the medial superior frontal gyrus. |
| `right_middle_temporal_gyrus` | right | `mtg_anterior`, `mtg_posterior`, `mtg_temporooccipital` | Whole middle temporal gyrus, right hemisphere. |
| `right_pars_triangularis_ba45` | right | `ifg_pars_triangularis` | Same structure (right BA 45). |
| ⚑ `right_posterior_perisylvian_cortex` | right | `stg_posterior`, `planum_temporale`, `smg_anterior`, `smg_posterior` | Posterior perisylvian cortex taken as the posterior superior temporal gyrus, planum temporale and supramarginal gyrus. |
| `right_precentral_gyrus` | right | `precentral_gyrus` | Same structure, right hemisphere. |

## Not mappable

| Region | Reason |
|---|---|
| `left_anterior_prefrontal_bottleneck` | As left_frontal_white_matter_bottleneck. |
| `left_extreme_capsule` | No atlas used here (JHU, XTRACT) labels the extreme capsule. It carries the inferior fronto-occipital and uncinate fasciculi, but those tracts are not the extreme-capsule fibre system itself, so it is not approximated. |
| `left_frontal_white_matter_bottleneck` | A "bottleneck" is a region defined in its source paper by the convergence of several tracts, not an atlas structure. |
| `left_perisylvian_network` | A network, not a single anatomical structure. |
| `left_posterior_middle_temporal_white_matter` | White matter under the posterior middle temporal gyrus; no tract label. |
| `left_posterior_temporal_bottleneck` | As left_frontal_white_matter_bottleneck. |
