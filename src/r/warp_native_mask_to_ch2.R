# Warp an image into template space with LINDA 0.5.1's own transforms, optionally
# continuing from ch2 (Colin27) to MNI152 with the transform made by analysis_38.
# All transforms are composed, so the image is resampled once.
#
# args: input reference warp affine output interpolation [template_warp template_affine [input_space]]
#   input_space "native" (default): native -> Penn (LINDA Reg3, affine inverted) -> ch2 [-> MNI152]
#   input_space "ch2": the input is already on ch2 (e.g. LINDA's Subject_in_ch2): ch2 -> MNI152 only
#   template_warp/affine "NONE": stop at ch2 (LINDA's original behaviour)
suppressPackageStartupMessages(library(ANTsR))
args <- commandArgs(trailingOnly=TRUE)
stopifnot(length(args) %in% c(6, 8, 9))
input <- args[1]; reference <- args[2]; warp <- args[3]
affine <- args[4]; output <- args[5]; interpolation <- args[6]
template_warp <- if (length(args) >= 8) args[7] else "NONE"
template_affine <- if (length(args) >= 8) args[8] else "NONE"
input_space <- if (length(args) == 9) args[9] else "native"
template_dir <- system.file("extdata", "pennTemplate", package="LINDA", mustWork=TRUE)
transforms <- character(0); invert <- logical(0)
if (input_space == "native") {
    transforms <- c(file.path(template_dir, "templateToCh2_1Warp.nii.gz"),
                    file.path(template_dir, "templateToCh2_0GenericAffine.mat"),
                    affine, warp)
    invert <- c(FALSE, FALSE, TRUE, FALSE)
} else if (input_space != "ch2") {
    stop("input_space must be 'native' or 'ch2'")
}
if (template_warp != "NONE") {
    transforms <- c(template_warp, template_affine, transforms)
    invert <- c(FALSE, FALSE, invert)
}
stopifnot(length(transforms) > 0, all(file.exists(c(input, reference, transforms))))
result <- antsApplyTransforms(
    fixed=antsImageRead(reference), moving=antsImageRead(input),
    transformlist=transforms, whichtoinvert=invert,
    interpolator=interpolation)
antsImageWrite(result, output)
