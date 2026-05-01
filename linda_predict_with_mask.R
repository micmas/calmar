#!/usr/bin/env Rscript
# linda_predict_with_mask.R
#
# Thin wrapper around LINDA's linda_predict() that takes a pre-computed
# brain mask. When `brain_mask` is supplied to linda_predict(), LINDA's
# internal n4_skull_strip() is bypassed entirely — see roxygen doc:
# "If this is passed in, then skull stripping is not done."
#
# Why we need this: LINDA's internal brain extraction uses ANTs
# template-based stripping which over-strips on stroke patients (the
# lesion deforms the registration to LINDA's template, dropping cortex
# near the lesion). Passing HD-BET's mask sidesteps that failure mode.
#
# Usage:
#   Rscript linda_predict_with_mask.R \
#       --t1   /path/to/T1w.nii.gz       \
#       --mask /path/to/brain_mask.nii.gz \
#       --outdir /path/to/output
#
# All three args are required. Optional flags:
#   --verbose / --quiet     (default: --verbose)
#   --no-cache              (default: cache enabled)
#
# Exit codes:
#   0  success — LINDA wrote outputs to <outdir>
#   1  argument parsing error
#   2  LINDA package not found
#   3  input file missing
#   4  linda_predict() raised an error (see stderr)

suppressPackageStartupMessages({
  args <- commandArgs(trailingOnly = TRUE)
})

# ---- argparse (rolled by hand to keep this script dependency-free) ----
parse_args <- function(argv) {
  out <- list(t1 = NULL, mask = NULL, outdir = NULL,
              verbose = TRUE, cache = TRUE)
  i <- 1
  while (i <= length(argv)) {
    a <- argv[i]
    if (a == "--t1") {
      out$t1 <- argv[i + 1]; i <- i + 2
    } else if (a == "--mask") {
      out$mask <- argv[i + 1]; i <- i + 2
    } else if (a == "--outdir") {
      out$outdir <- argv[i + 1]; i <- i + 2
    } else if (a == "--quiet") {
      out$verbose <- FALSE; i <- i + 1
    } else if (a == "--verbose") {
      out$verbose <- TRUE; i <- i + 1
    } else if (a == "--no-cache") {
      out$cache <- FALSE; i <- i + 1
    } else if (a %in% c("-h", "--help")) {
      cat("Usage: Rscript linda_predict_with_mask.R --t1 <file> ",
          "--mask <file> --outdir <dir> [--quiet] [--no-cache]\n", sep = "")
      quit(status = 0)
    } else {
      cat("Unknown argument:", a, "\n", file = stderr())
      quit(status = 1)
    }
  }
  out
}

opts <- parse_args(args)
if (is.null(opts$t1) || is.null(opts$mask) || is.null(opts$outdir)) {
  cat("Missing required arg. Need --t1, --mask, and --outdir.\n",
      file = stderr())
  quit(status = 1)
}

if (!file.exists(opts$t1)) {
  cat("T1 not found:", opts$t1, "\n", file = stderr())
  quit(status = 3)
}
if (!file.exists(opts$mask)) {
  cat("Brain mask not found:", opts$mask, "\n", file = stderr())
  quit(status = 3)
}

# ---- load LINDA ----
ok <- requireNamespace("LINDA", quietly = TRUE)
if (!ok) {
  cat("LINDA R package not installed in the current R libpath.\n",
      "Install with: remotes::install_github('dorianps/LINDA')\n",
      file = stderr())
  quit(status = 2)
}
suppressPackageStartupMessages(library(LINDA))

dir.create(opts$outdir, showWarnings = FALSE, recursive = TRUE)

cat(sprintf("[linda_predict_with_mask] T1     = %s\n", opts$t1))
cat(sprintf("[linda_predict_with_mask] mask   = %s\n", opts$mask))
cat(sprintf("[linda_predict_with_mask] outdir = %s\n", opts$outdir))
cat("[linda_predict_with_mask] LINDA's internal skull-stripping ",
    "is bypassed (using supplied brain_mask).\n", sep = "")

# ---- run linda_predict() with brain_mask= bypass ----
result <- tryCatch(
  linda_predict(
    file       = opts$t1,
    brain_mask = opts$mask,
    outdir     = opts$outdir,
    verbose    = opts$verbose,
    cache      = opts$cache
  ),
  error = function(e) {
    cat("linda_predict() failed: ", conditionMessage(e), "\n",
        file = stderr())
    quit(status = 4)
  }
)

cat("[linda_predict_with_mask] DONE — outputs in:", opts$outdir, "\n")
quit(status = 0)
