# What the pipeline computes

Each stage, the tools it uses and the decisions behind the defaults.
The notebook's markdown cells say the same per step; this page is the
overview. How to drive the notebooks is in
[NOTEBOOK_GUIDE.md](NOTEBOOK_GUIDE.md); how jobs run is in
[RUNNING_JOBS.md](RUNNING_JOBS.md).

```
Dataset (BIDS)
    │
    ├─ Brain mask (HD-BET; + SynthStrip per participant when a cavity is left out)
    ├─ Lesion segmentation (LINDA, optional)      ─┐
    ├─ Lesion segmentation (SynthStroke, optional)  ├─ warped to MNI space (LINDA's registration,
    ├─ (no LINDA: ANTs template registration)        │  or the ANTs registration step)
    └─ Expert/manual mask                          ─┘
    (acute route, MODALITY = "dwi": OpenADS on DWI + ADC, warped with its own registration)
            │
            ├─ QC dashboard (interactive, stage-aware)
            │
            ├─ Group lesion frequency map (glass-brain viewer)
            ├─ Atlas overlap (5 atlases, configurable mask source)
            ├─ Schaefer 7-network summary
            ├─ Per-subject interactive report
            │
            ├─ Disconnectome — BCBToolkit + Tractotron, and DeepDisco (deep-learning)
            ├─ Neurosynth lesion decoding
            │
            └─ KB-driven clinical interpretation
                   ├─ Predicted impairments (lesion location × atlas)
                   ├─ Outcome predictions (WAB-AQ, age, lesion volume)
                   ├─ Therapy recommendations (RTSS-tagged, stage-aware)
                   └─ Printable HTML report (Save as PDF)
```

## Brain mask

`BRAIN_MASK = "hdbet"` (default): the brain mask that LINDA and
SynthStroke use is HD-BET (brain tissue). HD-BET follows surviving
tissue, so a CSF-filled chronic infarct cavity that opens onto the brain
surface can fall outside its mask (more than 5% of the expert lesion in
12 of 36 sessions, worst 35%). `BRAIN_MASK = "hdbet+synthstrip"` adds
SynthStrip's CSF-inclusive mask (2 of 36 sessions above 5%, worst 7%,
plus a ~160 ml CSF rim), but LINDA then also labels CSF next to the
lesion: on 8 sessions its median Dice fell from 0.61 to 0.59 and false
positives rose from 45 to 84 ml. The union helped only where about 40 ml
or more of the lesion lay outside HD-BET (sub-M2045, sub-M2029). It is
therefore applied per participant: tag the skull strip
`lesion_excluded_by_strip` in QC, mark the participant for repair, and
the skull-strip repair uses the union for that participant. Evidence
and the per-session table: [validation/brain-mask/](validation/brain-mask/README.md).
Closing (`calmar.brainmask.close_cavities`) does not recover these
cavities, because they are wider than any closing radius that would not
also fill sulci.

## Template space

LINDA registers each brain to its **ch2 (Colin27)** template
(single-subject anatomy in MNI coordinates). The atlases, BCBToolkit
tractograms and DeepDisco are defined on **FSL MNI152**
(MNI152NLin6Asym), so ch2 is registered to MNI152 once
(`src/analysis_38_template_ch2_to_mni152.sh`, ANTs SyN; transforms in
`atlases/templates/ch2_to_MNI152NLin6Asym/`) and every mask is warped
native → Penn → ch2 → MNI152 in one resampling. `*_in_MNI.nii.gz` are on
MNI152 (182×218×182); LINDA's original ch2 outputs are kept as
`*_in_ch2.nii.gz`.

Native LINDA, manual and SynthStroke masks use LINDA's complete
native→Penn→ch2 transform chain (including the inverse subject affine
and bundled Penn→ch2 transforms), continued ch2→MNI152 in the same
resampling. The final reference is `Subject_in_MNI.nii.gz`; the
intermediate `Reg3_registered_to_template.nii.gz` is not MNI. Alignment
verification and repair records live in `alignment-repair/astra.yaml`.

## Segmentation methods and registration

`SEGMENTATION_METHODS` (default `["linda", "synthstroke"]`) chooses the
automatic segmentations; at least one is required. LINDA takes 1.5–3.7 h
per participant, almost all of it its registration to the template.
Without LINDA, the **registration step** (`src/analysis_29_registration.sh`,
ANTs 2.6.5) registers the brain-extracted T1w directly to the MNI152
brain, with the SynthStroke lesion (dilated 2 voxels) excluded from the
cost function: an affine stage (Mattes MI, one thread, seeded), then SyN
(cross-correlation, `REGISTRATION_THREADS`), ANTs' documented route to a
reproducible result. It took 9 min with 4 threads for sub-M2051 ses-284
(template correlation 0.66, vs 0.63 for LINDA's registration;
SynthStroke's template-space mask Dice 0.80 between the two
registrations). Its outputs, and the manual mask's products and
template-space SynthStroke mask made with it, are in
`derivatives/registration/`, so masks warped by the two registrations
never share a file.

## Acute route (`MODALITY = "dwi"`)

For acute stroke imaged with diffusion MRI (e.g. ISLES-2022:
`sub-*/ses-*/dwi/*_dwi.nii.gz` with `*_adc.nii.gz`), OpenADS
(`openadscpu/1.0.0`, `src/analysis_43_openads.sh`) segments the lesion
on the DWI and its ADC map. The T1 steps (brain extraction, LINDA,
SynthStroke, registration) are skipped.

- **Guided ISLES input:** choose **ISLES 2022 (local)** and its extracted
  root. The form validates compatible pairs, and the official
  `*_msk.nii.gz` reference masks are discovered automatically.
- **Optional DWI beside a T1 workflow:** after participant discovery,
  the notebooks ask whether to analyse any OpenADS-ready DWI/ADC pair
  they find. A pair may come from the selected T1 session or another
  session and remains labelled with its own session. The choice is
  recorded immediately, but OpenADS runs only after the ordinary
  T1/manual-mask registration inspection and QC. Its registration
  receives a separate QC checkpoint because DWI contrast and lesion
  boundaries can change over time, even when the anatomical lesion is
  expected to be stable in chronic stroke.
- **Template space:** OpenADS also registers the DWI to MNI152 (affine +
  SyN against its JHU ADC template). Its own template-space "stroke"
  image is not the lesion, so the native lesion is warped with those
  transforms (`src/analysis_44_apply_openads_registration.sh`). On 10
  ISLES-2022 cases the side was preserved in all, and OpenADS agreed
  with the expert masks at Dice 0.75–0.91 in template space for most
  lesions; small lesions are often missed.
- **Same downstream steps:** manual masks, disconnectomes, atlas overlap
  and the report work as in the chronic route.
- **Recovery phase:** reports tag each knowledge-base finding with the
  phase it was studied in, so an acute participant sees how much of the
  evidence comes from chronic-stroke studies.

## Directional dMRI (separate opt-in route)

Participant discovery inventories every BIDS `*_dwi.nii.gz` in the
selected and other participant sessions. `calmar.diffusion` checks the
b-values, b-vectors and JSON sidecar without fetching the NIfTI,
requires a b=0 image and at least 30 distinct diffusion directions for
participant reporting, and detects an opposite phase-encoding series
when present. Trace-DWI/ADC cases without gradients remain eligible for
OpenADS but are not treated as tensor or tractography data.

Selected series run after lesion QC through
`src/analysis_45_dmri_preproc.sh` (QSIPrep 26.1.1; TORTOISE
motion/eddy correction by default), `analysis_46_dmri_recon.sh`
(QSIRecon 26.0.1, default `ss3t_fod_autotrack`) and
`analysis_47_dmri_metrics.sh`. `DMRI_HMC_METHOD` can select another
QSIPrep-supported method. TORTOISE is the current default because the
Neurodesk 26.1.1 image ships unreadable FSL-eddy package metadata, which
prevents QSIPrep's `eddy` workflow from being constructed. The selected
native-T1 lesion mask is supplied to QSIPrep as a BIDS lesion ROI.
QSIRecon bundle FA/MD summaries are normalised to
`derivatives/calmar-dmri/<sub>/<ses>/dwi/metrics/*_desc-direct_tractometry.tsv`;
uncomputed fields remain explicitly missing. Reports place these
participant measurements in their own section and never numerically
combine them with BCB/DeepDisco probabilities. Because stroke pathology
can cause registration or tracking failure, a missing bundle is never
called proof of disconnection. Failed tool output appears in the
notebook/job error rather than disappearing with the temporary attempt
directory. The scientific record is `diffusion-tract-analysis/astra.yaml`.

## Optional brain-health interpretation

`ANALYSE_BRAIN_HEALTH` is an independent opt-in choice. On genuine T1w
entries, `src/analysis_48_brain_health_anatomy.sh` runs robust SynthSeg
8.2.1 parcellation and records brain-tissue fraction and ventricular
volume. These are **atrophy-sensitive descriptive features**, not a
diagnosis: a single scan has no age-/scanner-matched reference, and a
stroke cavity can look like tissue loss. The report therefore also shows
a cavity-adjusted fraction and keeps the caveat visible.

When a same-session FLAIR exists, `analysis_49_brain_health_wmh.sh` runs
DeepWMH 1.0.1. `analysis_50_brain_health_metrics.sh` registers the
selected native stroke lesion to FLAIR with ANTs 2.6.5 and reports both
the raw hyperintensity volume and the remainder after excluding the
lesion plus `BRAIN_HEALTH_LESION_EXCLUSION_MM` (default 3 mm). The
remainder is called a **WMH candidate burden**, not automatically
small-vessel disease. This matters especially in acute stroke, where
infarct-related oedema can extend beyond the exclusion zone. CALMaR
does not infer a Fazekas grade from volume. Results live under
`derivatives/calmar-brain-health/<sub>/<ses>/anat/`, remain provisional
until the saved PNG overlay is reviewed, and appear in a separate report
section. The scientific record is `brain-health-analysis/astra.yaml`.

## Disconnectomes

BCBToolkit and DeepDisco maps are computed for LINDA, SynthStroke and
manual masks. Tractotron is opt-in via `BCB_RUN_TRACTOTRON=True`; its
tables are not required for disconnectome views or interpretation
reports. Tractotron preparation uses the actual bundled atlas geometry
through `src/analysis_36_prepare_tractotron.sh`. The October 2026
container's reference is 157×189×136 at 1 mm despite its module help
describing 2 mm data. The bundled CLI computes `probability.csv` from
thresholded binary tracts, so that file is an overlap indicator, not a
continuous disconnection probability; `proportion.csv` records the
fraction of each thresholded tract overlapping the lesion. Preserve
these native outputs and their logs when comparing tool versions. A BCB
SIGILL fails explicitly: the historical notebook referenced an undefined
Python fallback, which is not a validated alternative.

## Clinical interpretation

The report combines the atlas overlap with the aphasia knowledge base
(the `stroke-aphasia-kb/` submodule) and the participant's clinical data
(`participants.tsv`). `decode_lesion.py` maps the mask to atlas regions
and Neurosynth v7 terms; `aphasia_kb_rag.py` retrieves the matching
approved findings and renders the cited report. Only regions present in
the decoder's atlas map can be reached from a mask;
`python stroke-aphasia-kb/scripts/kb_status.py` lists which KB regions
are currently unreachable. Each report lists the papers behind its
findings and the knowledge-base version it used.

## Provenance model

CALMaR separates two kinds of work.

**Pipeline outputs** (derivatives) are published atomically with a
`*.prov.json` sidecar and a cache record of their inputs (hashes),
parameters and the exact commands that produced them. Re-running reuses
an output only when all of these match; if a parameter changed, the
output is reported as stale and kept until you set the matching
`OVERWRITE` / `BCB_OVERWRITE` / `DEEPDISCO_OVERWRITE` (the old output is
preserved as `*.previous.*`).

**QC ratings and KB claims** earn full provenance: every QC edit is
logged in a sidecar JSON file (`Lesion_in_MNI.qc.json`) with reviewer,
timestamp and a before/after record. Every KB finding carries a
citation, method, sample description and extraction log.
