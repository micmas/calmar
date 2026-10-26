# CT route scope

Status: scoping only. This document adds no dependency, model, processing
script, or report claim.

## Intended route

The first CT route should accept a clinical non-contrast CT (NCCT), preserve
native Hounsfield units and acquisition metadata, produce a candidate stroke
mask in native CT space, register the CT and mask to CALMaR's MNI template,
and require visual review of both segmentation and registration before atlas
overlap or disconnectome analysis. It must support a manual-mask fallback and
must never treat “no automated lesion detected” as “no lesion”.

Acute ischemic change can be genuinely invisible or only subtly hypodense on
NCCT. Hemorrhage, old infarcts, leukoaraiosis, calcification, beam hardening,
motion, thick slices, gantry tilt, partial brain coverage, and postoperative
change can all invalidate assumptions made by an ischemic-lesion model. A CT
route must therefore distinguish at least ischemic versus hemorrhagic stroke,
scan-to-onset interval, and acute versus follow-up CT.

## Candidate lesion-segmentation tools

No candidate below is ready to become CALMaR's default without independent
validation. A model's code being open is not the same as having redistributable
weights, a stable inference command, or evidence of transportability.

| Candidate | Availability and packaging | Evidence and main limitations | Scope decision |
|---|---|---|---|
| `ncct-stroke-seg` (atlas-aligned dual-channel nnU-Net) | Open workflow code, nnU-Net 2.6.2, TotalSegmentator preprocessing; not currently a Neurodesk module. The repository explicitly omits the private training cohort, model weights, and nnU-Net plans, so it is a training/fine-tuning recipe rather than an installable pretrained segmenter. Code is CC BY-NC 4.0. | Technically attractive because it models left/right asymmetry and retains probability maps, but CALMaR cannot reproduce inference from the public repository alone. Atlas alignment before inference also makes registration error part of segmentation error. | Keep as a reference architecture; do not expose until usable weights and their licence/provenance are available. |
| Cl-SegNet | Open GPL-2.0 research code; old pinned stack (Python 3.8, PyTorch 1.11, CUDA 11.4) and a pretrained AISD model hosted on Baidu. Not a Neurodesk module, but container packaging is feasible. | Designed for acute ischemic NCCT and trained on AISD. The public AISD data contain 397 scans, 5-mm slices, <24-hour CT, with DWI-informed annotations. This is a narrow acquisition/population domain and not evidence for hemorrhage, chronic infarct, thinner modern reconstructions, or other scanners. | Best off-the-shelf candidate for a controlled technical benchmark, subject to weight integrity/licence review and external validation. |
| OS-AISeg | The 2024 paper reports public code and NCCT-only student inference, but the cited GitHub location was unavailable during this review. Not a Neurodesk module. | Reported five-fold Dice was 0.6196 on AISD and 0.4841 on ISLES2018. Those figures are useful expectations, not CALMaR performance; the unavailable implementation currently blocks reproducible packaging. | Reassess if a durable source release and weights become available. |
| Plain nnU-Net v2 trained by CALMaR | Open framework and straightforward to containerise, but no live `nnunet` Neurodesk module was found. Requires a curated training set, fixed splits, model cards, and distributable weights. | A transparent baseline is valuable and may transport better after local fine-tuning, but training on AISD alone inherits its 5-mm, <24-hour, DWI-referenced label domain. Small or initially invisible infarcts, posterior-fossa lesions, and severe artefacts remain difficult. | Preferred reproducible baseline if CALMaR undertakes model training; not an immediate clinical route. |
| Manual or assisted delineation | MRIcron/ITK-SNAP-style delineation can be packaged or linked to existing review tooling and does not require a learned model. | Still limited by low NCCT lesion conspicuity and inter-rater variability, but provides a necessary rescue path and validation reference. | Required fallback even if an automated model is later adopted. |

Relevant sources: the [atlas-aligned nnU-Net repository](https://github.com/IPMI-ICNS-UKE/ncct-stroke-seg),
[Cl-SegNet repository](https://github.com/hulinkuang/Cl-SegNet),
[OS-AISeg paper](https://pubmed.ncbi.nlm.nih.gov/39486307/), and
[AISD dataset description](https://github.com/griffinliang/aisd).

Published NCCT accuracy varies sharply by task and cohort. For calibration,
one multicentre study reported Dice about 0.51 for its model while inter-expert
agreement was about 0.36, and another open model reported about 0.59 Dice on
AISD. These are group summaries, not acceptance thresholds. Dice is also
unstable for small lesions; detection sensitivity, lesion-wise false positives,
surface distance, and volume error are all required.

## CT-to-MNI registration candidates

Live Neurodesk discovery on 2026-10-26 found `ants/2.6.5`, `fsl/6.0.7.23`, and
`niftyreg/2.1.2`. It did not find `nnunet` or `deepmedic` modules.

1. **SPM12 Clinical Toolbox CT normalization** is the most CT-specific
   reference route. It provides age-specific CT templates, Hounsfield-to-Cormack
   conversion, CT normalization, and lesion-aware utilities under a BSD
   licence. It is open but was not confirmed as a live Neurodesk module, so it
   would need a pinned SPM/MATLAB-compatible package or a carefully validated
   standalone route. See the [Clinical Toolbox repository](https://github.com/neurolabusc/Clinical)
   and its age-specific CT-template reference.
2. **FSL affine plus ANTs nonlinear registration** is immediately available in
   Neurodesk. Prior CT stroke work used FLIRT with a cross-modality cost
   function followed by ANTs nonlinear registration and lesion masking. CALMaR
   should use a CT template as the first target, preserve a lesion mask for cost
   function masking, and concatenate into MNI152NLin6Asym only after validation;
   direct unconstrained CT-to-T1 SyN is too easy to misregister. See the
   [published CT-to-MNI stroke pipeline](https://doi.org/10.1017/cjn.2020.112).
3. **NiftyReg** is available and open (BSD-3-Clause). `reg_aladin` offers robust
   rigid/affine block matching; `reg_f3d` offers nonlinear B-spline registration
   with normalized mutual information and bending-energy regularisation. It is
   a credible sensitivity route, not a default until compared with the
   CT-specific route. See the [NiftyReg repository](https://github.com/KCL-BMEIS/niftyreg).

Registration failure modes include invalid DICOM/NIfTI orientation, gantry
tilt, cropped skull or brain, thick/anisotropic slices, extracranial signal,
ventricular enlargement, mass effect, large unilateral or bilateral lesions,
and the optimizer matching lesion or skull edges to normal anatomy. Affine-only
alignment may leave local cortical and ventricular mismatch; nonlinear
alignment may deceptively improve global appearance while distorting the
lesion neighbourhood. Every route needs native-to-template overlays, landmark
or label metrics, deformation/Jacobian checks, and a “registration failed”
outcome that prevents atlas interpretation.

## Report changes required for CT

A CT-derived report must say, near the title and every location result:

- source modality, acquisition date/time relative to stroke, slice thickness,
  reconstruction kernel when known, and whether contrast was used;
- segmentation method and version, model/weight identifier, training domain,
  probability threshold, mask QC status, and any manual edits;
- registration method/version, CT template and final MNI template, lesion-aware
  strategy, interpolation, and registration QC status;
- that NCCT has lower soft-tissue contrast than MRI and an acute ischemic lesion
  may be underestimated, absent, or have uncertain boundaries;
- that atlas overlap, lesion volume, and disconnectome estimates inherit both
  segmentation and registration uncertainty;
- that absence of overlap or disconnection evidence is not evidence of intact
  tissue or tracts; and
- separate wording for hemorrhage, ischemia, mixed/unknown stroke type, and old
  lesions. A model validated only for acute ischemia must refuse hemorrhagic or
  unknown cases rather than silently applying itself.

The report should use “CT-derived candidate lesion mask” until both QC stages
pass. Low-confidence or manually corrected masks should remain usable for
research description but should carry a visible caution and must not be framed
as a participant-level outcome prediction.

## Minimal validation plan

1. Freeze the intended use: adult ischemic NCCT, scan window, slice-thickness
   range, scanner mix, and exclusions. Keep hemorrhage as a separate future
   validation stratum.
2. Assemble a held-out, multi-site set with native CT, expert masks from at
   least two readers, consensus/adjudication, stroke type, onset time, slice
   thickness, lesion visibility, lesion volume, territory, and follow-up
   DWI/MRI where available. Do not tune thresholds on this set.
3. Benchmark manual fallback, nnU-Net baseline, and any packageable pretrained
   candidate. Report case-wise and lesion-wise sensitivity, false-positive
   lesions/case, Dice, precision/recall, absolute and relative volume error,
   Hausdorff/surface distance, and complete misses. Stratify by lesion size,
   onset time, visibility, territory/posterior fossa, slice thickness, scanner,
   artefact, and site.
4. Compare CT-template registration routes using blinded visual QC plus brain
   overlap, midline/ventricle and cortical landmarks, atlas-label overlap where
   manual labels exist, inverse consistency, and local deformation around the
   lesion. Evaluate affine, lesion-masked nonlinear, and the CT-specific
   Clinical Toolbox route; do not choose by global similarity alone.
5. Measure the downstream error that matters to CALMaR: lesion volume, atlas
   region ranking, hemispheric assignment, and tract-disconnection estimates
   versus the consensus mask transformed by an independently reviewed route.
6. Predefine pass/fail gates. Any missing lesion, wrong hemisphere, gross
   extracranial false positive, failed registration, or implausible deformation
   must block automated reporting and route to manual review.
	7. Run a silent prospective pilot on consecutive local cases before enabling
	   the route. Record exclusions and failures, not just successful scans, and
	   retain all software/model versions and QC decisions.
