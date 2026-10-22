"""The scientific choices of a run, as one readable table.

Shown under the configuration cell and suitable for a methods section or a
report appendix. Tool versions are the module pins of the Slurm scripts in
``src/``; values come from CONFIG.
"""
import pandas as pd

TOOLS = {
    "acquisition": "DataLad / local BIDS discovery",
    "brain": "HD-BET (hdbet/1.0.0) + SynthStrip (synthstrip/7.4.1)",
    "linda": "LINDA (linda/0.5.1)",
    "synthstroke": "SynthStroke (synthstroke/0.0.0, synth-plus weights)",
    "manual": "SimpleITK rigid registration + the template registration",
    "registration": "ANTs (ants/2.6.5) antsRegistrationSyN.sh",
    "openads": "OpenADS (openadscpu/1.0.0)",
    "bcb": "BCBToolkit disconnectome (bcbtoolkit/0.0.0, run_disco.sh)",
    "deepdisco": "DeepDisco (deepdisco/20251008)",
    "atlas": "nilearn world-coordinate resampling",
    "report": "CALMaR + aphasia-kb",
}

def methods_table(config):
    c = config.get
    from .study import modality, segmentation_methods, template_source
    route = modality(config)
    methods = segmentation_methods(config)
    optional_dwi = route == "t1" and bool(c("_DWI_ANALYSIS_SELECTED") or c("ANALYSE_DWI") is True)
    dwi_policy = c("ANALYSE_DWI")
    if route == "dwi":
        openads_status = "Primary DWI route"
    elif optional_dwi:
        openads_status = "Selected; runs after T1/manual-mask QC"
    elif dwi_policy is False:
        openads_status = "Available, disabled in configuration"
    else:
        openads_status = "Available; offered when a DWI+ADC pair is discovered"

    registration = template_source(config)
    if registration == "openads":
        registration_tool = "OpenADS (openadscpu/1.0.0) DWI registration + ANTs (ants/2.6.5)"
        registration_parameters = "affine + SyN against OpenADS's JHU ADC template; nearest-neighbour lesion warp"
        registration_meaning = "Registers the primary DWI and its OpenADS lesion to FSL MNI152NLin6Asym."
    elif registration == "linda":
        registration_tool = "LINDA (linda/0.5.1) + ANTs (ants/2.6.5)"
        registration_parameters = (f"LINDA native→Penn→ch2; fixed ch2→MNI152 SyN; "
                                   f"seed={c('REGISTRATION_SEED', 1729)}; LINDA threads={c('LINDA_THREADS', 1)}")
        registration_meaning = "Warps every T1-route mask to FSL MNI152NLin6Asym in one resampling."
    else:
        registration_tool = TOOLS["registration"]
        registration_parameters = (f"affine (Mattes MI, 1 thread) + SyN (CC, "
                                   f"{c('REGISTRATION_THREADS', 4)} threads); seed={c('REGISTRATION_SEED', 1729)}; "
                                   "SynthStroke lesion dilated 2 voxels and excluded from the cost function")
        registration_meaning = "Registers the brain-extracted T1w and every T1-route mask to FSL MNI152NLin6Asym."
    if optional_dwi:
        registration_meaning += " The optional OpenADS mask uses its own DWI affine + SyN registration and QC."
    rows = [
        ("Input discovery and acquisition", TOOLS["acquisition"], "Used",
         "Selected T1w or DWI+ADC content; inventories all participant DWI sessions."),
        ("Brain extraction", TOOLS["brain"] if c("BRAIN_MASK", "hdbet") == "hdbet+synthstrip" else "HD-BET (hdbet/1.0.0)",
         "Used" if route == "t1" else "Not used on the DWI route",
         f"mask={c('BRAIN_MASK', 'hdbet')}, HD-BET mode={c('HDBET_MODE', 'fast')}, device={c('HDBET_DEVICE') or 'cpu'}",
         ("Union of HD-BET (brain tissue) and SynthStrip (brain + CSF), so CSF-filled lesion cavities stay inside; "
          if c("BRAIN_MASK", "hdbet") == "hdbet+synthstrip"
          else "HD-BET alone; a skull-strip repair can add SynthStrip's CSF for a participant whose lesion cavity it left out; ")
         + "used by LINDA (replacing LINDA's own skull strip) and to clip SynthStroke."
         if c("USE_HDBET_PREPROCESSING", True) else "Disabled: LINDA uses its own skull strip."),
        ("Lesion segmentation (LINDA)", TOOLS["linda"],
         "Selected" if "linda" in methods else
         "Not used on the DWI route" if route == "dwi" else "Available, not selected",
         f"brain-mask bypass={bool(c('USE_HDBET_PREPROCESSING', True))}; "
         f"seed={c('REGISTRATION_SEED', 1729)}; threads={c('LINDA_THREADS', 1)}",
         "Chronic T1w lesion segmentation plus LINDA's nonlinear registration to its ch2 template."),
        ("Lesion segmentation (SynthStroke)", TOOLS["synthstroke"],
         "Selected" if "synthstroke" in methods else
         "Not used on the DWI route" if route == "dwi" else "Available, not selected",
         f"TTA={c('SYNTHSTROKE_TTA', True)}; clip to brain mask dilated 2 voxels",
         "Independent chronic-T1w lesion segmentation, warped with the selected template registration."),
        ("Lesion segmentation (OpenADS)", TOOLS["openads"],
         openads_status, "DWI + exact sibling ADC; two passes with regenerated brain-extracted inputs",
         "Segments acute ischaemic lesions; another participant session is allowed and remains separately labelled/QC'd."),
        ("Template registration", registration_tool, "Used", registration_parameters, registration_meaning),
        ("Manual mask", TOOLS["manual"], "Used when a mask is available",
         f"space={c('MANUAL_MASK_SPACE', 't1')}; path={c('MANUAL_MASK_PATH') or 'publisher derivatives (auto)'}; "
         f"rigid-registration seed={c('REGISTRATION_SEED', 1729)}",
         "Reference scan rigidly registered to the T1w with Mattes MI; mask resampled nearest-neighbour for QC."),
        ("Disconnectome 1", TOOLS["bcb"], "Used after QC",
         f"masks={c('BCB_MASKS', 'all')}, input grid={c('BCB_INPUT_GRID', 'mni152')}",
         "Probability that each voxel's tracts pass through the lesion (10 healthy-control tractograms)."),
        ("Disconnectome 2", TOOLS["deepdisco"], "Used after QC",
         f"masks={c('DEEPDISCO_MASK_SOURCE', 'all')}, models={'all four' if c('DEEPDISCO_RUN_ALL', True) else c('DEEPDISCO_MODELS')}, "
         f"downsampling={c('DEEPDISCO_DOWNSAMPLING', 'coverage')}",
         "Deep-learning estimate of the disconnectome on the MNI152 2 mm grid."),
        ("Atlas overlap", TOOLS["atlas"], "Used for every available selected mask",
         f"atlases={', '.join(c('ATLASES', []))}, threshold={c('LESION_THRESHOLD', .5)}",
         "Share of lesion voxels inside each atlas region."),
        ("Evidence report", TOOLS["report"], "Optional participant report",
         "Deterministic atlas/KB matching, citations, QC and provenance; optional Neurosynth decoding."),
    ]
    # Some rows carry both a compact parameter summary and a longer meaning;
    # others need only the concise description. Normalise them for one table.
    normalised = []
    for row in rows:
        if len(row) == 5:
            step, tool, status, parameters, meaning = row
        else:
            step, tool, status, meaning = row
            parameters = "—"
        normalised.append((step, tool, status, parameters, meaning))
    return pd.DataFrame(normalised, columns=["Step", "Tool", "Status / when used", "Parameters", "Meaning"])
