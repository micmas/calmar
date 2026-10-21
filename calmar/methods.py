"""The scientific choices of a run, as one readable table.

Shown under the configuration cell and suitable for a methods section or a
report appendix. Tool versions are the module pins of the Slurm scripts in
``src/``; values come from CONFIG.
"""
import pandas as pd

TOOLS = {
    "brain": "HD-BET (hdbet/1.0.0) + SynthStrip (synthstrip/7.4.1)",
    "linda": "LINDA (linda/0.5.1)",
    "synthstroke": "SynthStroke (synthstroke/0.0.0, synth-plus weights)",
    "manual": "SimpleITK rigid registration + the template registration",
    "registration": "ANTs (ants/2.6.5) antsRegistrationSyN.sh",
    "openads": "OpenADS (openadscpu/1.0.0)",
    "bcb": "BCBToolkit disconnectome (bcbtoolkit/0.0.0, run_disco.sh)",
    "deepdisco": "DeepDisco (deepdisco/20251008)",
}


def _segmentation_rows(config):
    """Lesion segmentations, template registration and manual mask, for the
    selected SEGMENTATION_METHODS."""
    from .study import segmentation_methods, template_source
    c = config.get
    methods = segmentation_methods(config)
    rows = []
    if "linda" in methods:
        rows.append(("Lesion segmentation (LINDA)", TOOLS["linda"],
                     f"brain_mask bypass={bool(c('USE_HDBET_PREPROCESSING', True))}, "
                     f"seed={c('REGISTRATION_SEED', 1729)}, threads={c('LINDA_THREADS', 1)}",
                     "Lesion in native T1w space plus nonlinear registration to LINDA's ch2 (Colin27) template."))
    if "synthstroke" in methods:
        rows.append(("Lesion segmentation (SynthStroke)", TOOLS["synthstroke"],
                     f"TTA={c('SYNTHSTROKE_TTA', True)}, clip to brain mask dilated 2 voxels",
                     "Independent deep-learning segmentation, warped to MNI152 with the template registration."))
    if "openads" in methods:
        rows.append(("Lesion segmentation (OpenADS)", TOOLS["openads"],
                     "DWI (b1000) + ADC; two passes with regenerated brain-extracted images",
                     "Acute (DWI) route: deep-learning segmentation of the acute ischaemic lesion."))
    if template_source(config) == "openads":
        rows.append(("Template registration", "OpenADS's (openadscpu/1.0.0) DWI registration + ants/2.6.5",
                     "affine + SyN against OpenADS's JHU ADC template; one nearest-neighbour resampling",
                     "The native lesion is warped to FSL MNI152NLin6Asym (182×218×182, 1 mm) with OpenADS's "
                     "transforms; the T1 steps (brain extraction, LINDA, SynthStroke) are not run."))
    elif template_source(config) == "linda":
        rows.append(("Template registration", "LINDA's (linda/0.5.1) + ANTs 2.6.5 SyN ch2 -> MNI152 (once)",
                     "FSL MNI152NLin6Asym, 182×218×182, 1 mm",
                     "Every mask: native -> Penn -> ch2 -> MNI152 in one resampling; the space of the atlases, "
                     "BCBToolkit and DeepDisco."))
    else:
        rows.append(("Template registration", TOOLS["registration"],
                     f"affine (Mattes MI, 1 thread) + SyN (CC, {c('REGISTRATION_THREADS', 4)} threads), "
                     f"seed={c('REGISTRATION_SEED', 1729)}, SynthStroke lesion (dilated 2 voxels) excluded",
                     "LINDA not run: the brain-extracted T1w is registered to the FSL MNI152NLin6Asym brain "
                     "(182×218×182, 1 mm); every mask is warped native -> MNI152 in one resampling."))
    rows.append(("Manual mask", TOOLS["manual"],
                 f"space={c('MANUAL_MASK_SPACE', 't1')}, path={c('MANUAL_MASK_PATH') or 'publisher derivatives (auto)'}",
                 "Reference scan rigidly registered to the T1w (Mattes MI); mask resampled nearest-neighbour."))
    return rows


def methods_table(config):
    c = config.get
    from .study import modality
    rows = ([] if modality(config) == "dwi" else [
        ("Brain extraction", TOOLS["brain"] if c("BRAIN_MASK", "hdbet") == "hdbet+synthstrip" else "HD-BET (hdbet/1.0.0)",
         f"mask={c('BRAIN_MASK', 'hdbet')}, HD-BET mode={c('HDBET_MODE', 'fast')}, device={c('HDBET_DEVICE') or 'cpu'}",
         ("Union of HD-BET (brain tissue) and SynthStrip (brain + CSF), so CSF-filled lesion cavities stay inside; "
          if c("BRAIN_MASK", "hdbet") == "hdbet+synthstrip"
          else "HD-BET alone; a skull-strip repair can add SynthStrip's CSF for a participant whose lesion cavity it left out; ")
         + "used by LINDA (replacing LINDA's own skull strip) and to clip SynthStroke."
         if c("USE_HDBET_PREPROCESSING", True) else "Disabled: LINDA uses its own skull strip."),
    ]) + _segmentation_rows(config) + [
        ("Disconnectome 1", TOOLS["bcb"], f"masks={c('BCB_MASKS', 'all')}, input grid={c('BCB_INPUT_GRID', 'mni152')}",
         "Probability that each voxel's tracts pass through the lesion (10 healthy-control tractograms)."),
        ("Disconnectome 2", TOOLS["deepdisco"],
         f"masks={c('DEEPDISCO_MASK_SOURCE', 'all')}, models={'all four' if c('DEEPDISCO_RUN_ALL', True) else c('DEEPDISCO_MODELS')}, "
         f"downsampling={c('DEEPDISCO_DOWNSAMPLING', 'coverage')}",
         "Deep-learning estimate of the disconnectome on the MNI152 2 mm grid."),
        ("Atlas overlap", "nilearn world-coordinate resampling", f"atlases={', '.join(c('ATLASES', []))}, threshold={c('LESION_THRESHOLD', .5)}",
         "Share of lesion voxels inside each atlas region."),
    ]
    return pd.DataFrame(rows, columns=["Step", "Tool", "Parameters", "Meaning"])
