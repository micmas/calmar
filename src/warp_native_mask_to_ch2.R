# Match LINDA 0.5.1's final native -> Penn -> MNI (ch2) transform exactly.
suppressPackageStartupMessages(library(ANTsR))
args <- commandArgs(trailingOnly=TRUE)
stopifnot(length(args) == 6)
input <- args[1]; reference <- args[2]; warp <- args[3]
affine <- args[4]; output <- args[5]; interpolation <- args[6]
template_dir <- system.file("extdata", "pennTemplate", package="LINDA", mustWork=TRUE)
transforms <- c(file.path(template_dir, "templateToCh2_1Warp.nii.gz"),
                file.path(template_dir, "templateToCh2_0GenericAffine.mat"),
                affine, warp)
stopifnot(all(file.exists(c(input, reference, transforms))))
result <- antsApplyTransforms(
    fixed=antsImageRead(reference), moving=antsImageRead(input),
    transformlist=transforms, whichtoinvert=c(FALSE, FALSE, TRUE, FALSE),
    interpolator=interpolation)
antsImageWrite(result, output)
