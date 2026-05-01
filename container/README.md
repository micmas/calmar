# Container additions for the LINDA Neurodesk image

These two files belong **inside** the LINDA singularity container so
that a host user can call `linda_predict_with_mask.sh` exactly the way
they call `linda_predict.sh` today.

## Files

- `linda_predict_with_mask.sh` — bash entrypoint, install on `$PATH` next
  to `linda_predict.sh` (typically `/usr/local/bin/`).
- `../linda_predict_with_mask.R` — R stub that calls
  `linda_predict(file=..., brain_mask=...)`. Install it at
  `/usr/local/share/LINDA/linda_predict_with_mask.R` (or anywhere — set
  the `LINDA_MASK_R_STUB` env var in the container if you choose
  another path).

## Container build snippet (Singularity / Apptainer recipe)

Add a section like this to the existing LINDA recipe:

```Singularity
%files
    linda_predict_with_mask.R  /usr/local/share/LINDA/linda_predict_with_mask.R
    linda_predict_with_mask.sh /usr/local/bin/linda_predict_with_mask.sh

%post
    chmod +x /usr/local/bin/linda_predict_with_mask.sh
    chmod +r /usr/local/share/LINDA/linda_predict_with_mask.R
```

Or as a Docker / `RUN` block:

```Dockerfile
COPY linda_predict_with_mask.R  /usr/local/share/LINDA/
COPY linda_predict_with_mask.sh /usr/local/bin/
RUN  chmod +x /usr/local/bin/linda_predict_with_mask.sh
```

## What Neurodesk does for you after that

When you publish the new container version, Neurodesk's
transparent-singularity layer scans the container's `$PATH` and
auto-generates host-side wrappers. So users will see a new file at:

```
/cvmfs/neurodesk.ardc.edu.au/containers/linda_<ver>_<date>/linda_predict_with_mask.sh
```

That host wrapper does the same `singularity --silent exec --cleanenv ...`
dance as the existing `linda_predict.sh` wrapper, just with a different
argv[0]. From the user's notebook, calling `linda_predict_with_mask.sh
--t1 X --mask Y --outdir Z` then "just works" — same UX as
`linda_predict.sh`.

## Verifying the bypass works

After building and installing, run inside the container:

```bash
linda_predict_with_mask.sh \
    --t1     /sample/T1w.nii.gz \
    --mask   /sample/brain_mask.nii.gz \
    --outdir /tmp/linda_out
```

You should see in the output:
```
[linda_predict_with_mask] LINDA's internal skull-stripping is bypassed (using supplied brain_mask).
```

…and in the resulting `/tmp/linda_out/BrainMask.nii.gz`, the mask
should be exactly equal to the input mask (LINDA wrote it through
unchanged), rather than the smaller template-warped version that
`n4_skull_strip()` would have produced.

## Argument contract

`linda_predict_with_mask.sh` accepts the same args as the R stub it
wraps:

| Flag         | Required | Notes |
|--------------|----------|-------|
| `--t1 PATH`     | yes | Original (skull-on) T1-weighted NIfTI. |
| `--mask PATH`   | yes | Pre-computed brain mask (e.g. from HD-BET). |
| `--outdir DIR`  | yes | Output directory; created if missing. |
| `--quiet`       | no  | Suppress LINDA's verbose chatter. |
| `--no-cache`    | no  | Disable `cache=TRUE` in `linda_predict()`. |

Exit codes propagate from the R stub:
`0` success · `1` arg parse error · `2` LINDA package missing ·
`3` input file missing · `4` `linda_predict()` raised.
