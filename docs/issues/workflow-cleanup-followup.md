# Interpretation workflow follow-up

Implemented in the current workflow:

- Guided inputs and stable cell IDs, with checkpoints that allow upstream cells to rerun.
- Participant-local QC drafts, save/next navigation, saved-QC reuse that continues after QC, and explicit skip notices.
- One native automatic/manual mask comparison and one lesion/disconnectome comparison. Model changes preserve the selected method and image position.
- Consistent mask-origin colours, deferred image loading, and title-based cell timings.
- Full-cohort atlas selectors, explicit zero/missing status, subject/session cache keys, changed-mask invalidation, and measured overlap laterality.
- Integrated report selection, export and Neurosynth decoding with visible completion/failure status.

The current example cohort is sub-M2066/ses-235, sub-M2075/ses-602 and
sub-M2176/ses-1237. All have local processing outputs. The September 30
verification refreshed overlap tables for these participants and exercised
cached Neurosynth decoding; see `workflow-validation/astra.yaml`. Browser
fixtures exercised model switching, layer reuse and preserved slice position.
These checks do not certify scientific QC or a fresh end-to-end processing run.

Remaining work:

- Complete fresh-cohort acceptance across native/MNI masks, all disconnectome sources and all four DeepDisco models, with scientific visual QC.
- Extract remaining notebook processing into retained scripts so viewing a result never starts registration, inference or acquisition implicitly.
- Continue separating optional diagnostics from the essential processing/QC/report workflow while preserving distinct scientific checks.
- Cross-reference #5 when extending cache invalidation to other scientific outputs; a working selector alone does not establish that all cached results are current.

Keep masks, ratings, manual edits, existing scientific decisions and run
provenance intact during follow-up work. Use panel titles and stable cell IDs
when referring to steps, since notebook cell positions change during cleanup.
