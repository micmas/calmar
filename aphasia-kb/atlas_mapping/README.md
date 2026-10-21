# Atlas → knowledge-base mapping

How CALMaR decides which knowledge-base (KB) findings apply to a participant's lesion.

## Why this exists

A report needs to know which brain regions a lesion damages, and which KB findings concern those regions. The lesion is measured against brain atlases (one overlap table per atlas, from the reporting job). The KB names regions in its own words (`left_ifg_pars_opercularis`, `left_arcuate_fasciculus`, …).

Until October 2026 the report linked the two **by name**: an atlas label such as "Inferior Frontal Gyrus, pars opercularis" was normalised and looked up among KB names and aliases. An audit found this reached only a quarter of the location evidence:

| Before (name matching), 2026-10-21 | |
|---|---|
| Location-based findings that could reach a report | 80 of 318 (25 %) |
| AAL, Destrieux, Schaefer400 labels matching any KB region | 0 of 666 |
| JHU tract labels matching | 2 of 20, both by accident; *Uncinate fasciculus L* matched `left_extreme_capsule`, a different tract |
| Arcuate fasciculus findings reachable | 0 of 21 |
| Hemisphere | ignored: right-hemisphere damage counted as left (HarvardOxford labels are bilateral and the lookup tried "left …" first) |

The mapping replaces the guessing with an explicit, reviewed table.

| After (this mapping) | |
|---|---|
| Location-based findings naming a mapped region | 301 of 318 (95 %) |
| Findings naming a region no atlas can represent | 17 (listed below, with the reason) |
| Region names neither mapped nor explained | 0 (enforced by `tests/test_kb_atlas_mapping.py`) |

Example, sub-M2030 ses-1454, manual mask: name matching reached 4 findings; the mapping (with JHU only) reached 80, including 17 white-matter findings (the left superior longitudinal fasciculus core is 96 % destroyed).

## The files

| File | What it holds | Edit? |
|---|---|---|
| `units.yaml` | **Anatomical units**: the structures damage is measured in, each defined by named labels of one atlas, with the basis for the choice | yes |
| `kb_regions.yaml` | **KB region names → units**, with side and basis; plus `unmapped`, the names no atlas can represent and why | yes, whenever a paper adds a region name |
| `atlas_labels.json` | The labels each atlas actually has (as in the overlap tables), so a misspelt label is caught | only if an atlas changes |
| `MAPPING.md` | The whole mapping as one table, generated from the YAML | no: `python atlas_mapping.py --write-table` |
| `evidence_gaps.yaml` | Areas needing more evidence, with the papers to extract | yes |
| `EVIDENCE_GAPS.md` | The gaps with current finding counts and paper status, generated | no: `python atlas_mapping.py --write-table` |
| `../atlas_mapping.py` | Loads, checks and applies the mapping | code |

Two levels keep it maintainable. The 90 region names in the KB (84 mapped, 6 not mappable) include many synonyms (`left_superior_temporal_gyrus_wernicke` / `…_wernickes`, `left_precentral_gyrus` / `left_pre_central_gyrus`, four spellings of the arcuate). They point to 54 anatomical units, so each atlas decision is made once.

## Rules

1. **One atlas per unit.**
   - *HarvardOxford* (cortical, max-probability 25 %, 2 mm) for cortex.
   - *AAL* (SPM12) only where HarvardOxford has no label: putamen, pallidum, hippocampus, pars orbitalis, temporal-pole subdivisions, medial superior frontal gyrus.
   - *JHU* (ICBM tracts, max-probability 50 %, 2 mm, from FSL) for the superior longitudinal, inferior longitudinal, inferior fronto-occipital and uncinate fasciculi and the callosal forceps.
   - *XTRACT* (HCP tract atlas, max-probability 5 %, 1 mm, FSL 6.0.7.22; Warrington et al. 2020) for the tracts JHU does not label: arcuate fasciculus, SLF III, frontal aslant tract, middle longitudinal fasciculus, optic radiation. Added 2026-10-21; it closed the arcuate judgement call and made three tracts reachable.
   - Destrieux is not used: it divides the same cortex more finely, adding no region the KB names.
   - Schaefer400 is not used: its parcels are functional networks, not the anatomical structures lesion–symptom studies report.
2. **Hemisphere from the lesion, not the name.**
   - HarvardOxford labels (and JHU's midline forceps) cover both hemispheres, so each lesion voxel is assigned to the left or right side by its MNI x coordinate (x < 0 = left; voxels exactly on the midline are not counted).
   - AAL, JHU and XTRACT labels carry their side (`_L`, `L`).
   - A KB region has `side: left | right | both`. Only damage on that side counts.
3. **Two damage measures**, per unit and side:
   - `lesion_pct`: the share of the whole lesion inside the unit.
   - `region_pct`: the share of the unit destroyed. For bilateral labels this uses the size of that hemisphere's part, which overlap tables record since this change. Older tables lack it, so `region_pct` is empty until the reporting job recomputes them; it does so once, automatically.
   - A KB region's damage is the sum over its units of one atlas (an atlas's labels do not overlap). When a region uses units of two atlases (e.g. XTRACT's arcuate with JHU's SLF), whose labels can overlap, the larger of the two values is taken, never the sum.
4. **When a region counts as damaged.** At least `INTERP_MIN_OVERLAP_PCT` (default 5 %) of the lesion lies in it, **or** at least `INTERP_MIN_REGION_PCT` (default 25 %) of it is destroyed.
   - The second criterion is needed for small regions and thin tracts. In sub-M2030 (199 ml lesion) the posterior superior temporal gyrus, Heschl's gyrus, planum temporale and the opercula were 100 % destroyed and the insula 96 %, yet each held under 5 % of the lesion. The left SLF core held 1.1 % of the lesion but was 96 % destroyed.
   - 25 % rather than 10 %: at 10 % slivers counted as damage (pars orbitalis 11 %, pallidum 12 %, precentral gyrus 15 %); 25 % keeps every clearly damaged region (sub-M2030: 225 findings at 25 %, 250 at 10 %, 218 at 50 %).
5. **Findings match by exact name**, in two ways:
   - *Forward:* a finding stored on a region entry (region → what damage to it predicts).
   - *Reversed:* an impairment finding whose target is a region (that impairment ← damage to the region).
6. **Weight of a finding** for this lesion: the share of the region destroyed (`region_pct`, what lesion–symptom studies relate deficits to), or the share of the lesion when the region's size is unknown. It is multiplied, as before, by the finding's strength, evidence quality, confidence and direction.

## Decisions to review (⚑ in MAPPING.md)

`review: true` marks every mapping that is a judgement rather than a same-name match: 23 regions and 2 units. The ones that matter most:

| Decision | Choice made | Alternative |
|---|---|---|
| **Arcuate segments.** XTRACT labels the whole arcuate, not its segments. | `left_arcuate_fasciculus` → XTRACT arcuate (not a judgement). Long and posterior segments → XTRACT arcuate; anterior segment (fronto-parietal) → XTRACT SLF III. | — |
| **"Precentral gyrus of the insula"** (Dronkers 1996, apraxia of speech) | → the insula: it is an insular gyrus, not the motor precentral gyrus; the atlases do not subdivide the insula. | — |
| **Extreme capsule** | Not mapped. The inferior fronto-occipital and uncinate fasciculi run through it, but they are not the extreme-capsule fibre system. | Approximate with those two tracts. |
| **Composite or label-less areas**: anterior temporal lobe, temporoparietal junction, superior temporal sulcus, Spt, DLPFC, premotor cortex, basal temporal cortex, … | Each built from the units its definition or aliases name (basis in `kb_regions.yaml`). | — |
| **Corpus callosum** | → JHU forceps major and minor only; JHU does not label the callosal body. | — |
| **JHU tract masks are thin cores** (50 % probability, 2 mm) | "96 % destroyed" means 96 % of that core. | Use a lower-threshold or probabilistic tract atlas. |

## Not mappable (17 findings)

Extreme capsule, white matter under the posterior middle temporal gyrus, three tract "bottlenecks" and a "perisylvian network". These are regions defined by their source papers (tract convergences, networks) or a fibre system (extreme capsule) that neither JHU nor XTRACT labels. Their findings cannot be matched from lesion location; reports count them as not mappable. The reasons are in `kb_regions.yaml` → `unmapped`.

## Evidence gaps

`evidence_gaps.yaml` lists the areas where reports cannot yet be trusted, and why:

- **atlas gap:** the KB has findings but no atlas label reaches them;
- **no evidence:** lesions hit the structure but no finding concerns it;
- **thin:** 1–3 findings or 1–2 papers;
- **contested:** the literature disagrees.

Each gap names the papers that would close it. Those papers are `[seed]` entries in `../citations.md` (section "added 2026-10-21"), ready for `extract.py`. `EVIDENCE_GAPS.md` is generated with the current counts and each paper's extraction status, so it shrinks as papers are extracted.

The first gap closed was not a paper: adding FSL's **XTRACT** tract atlas (2026-10-21) gave the arcuate fasciculus its own label and made the frontal aslant tract, middle longitudinal fasciculus and optic radiation reachable.

In reports, a damaged region whose findings come from two studies or fewer is marked "⚠ based on N studies".

## Adding a paper with a new region name

`tests/test_kb_atlas_mapping.py` fails, naming the region. Then:

1. Add it to `kb_regions.yaml`: map it to existing units, add a unit to `units.yaml` (with the atlas label and the basis), or list it under `unmapped` with the reason. Mark judgement calls `review: true`.
2. Run `python atlas_mapping.py --write-table --coverage` (checks the files, regenerates `MAPPING.md`, prints the coverage).
3. Run the tests.

## Checking it

```
python aphasia-kb/atlas_mapping.py --coverage        # files consistent? how much evidence is reachable?
python aphasia-kb/kb_status.py                       # "Atlas reachability" section
pytest tests/test_kb_atlas_mapping.py
```
