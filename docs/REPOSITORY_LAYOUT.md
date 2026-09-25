# Repository layout and script migration

Open the notebooks and submit analytical jobs from the repository root. The
`calmar/` directory is a regular Python package importable directly from this
checkout; the package initializer does not start processing or initialize UI.
KB tools remain in `aphasia-kb/` with their existing entry points.

```text
calmar/
  qc.py                 # ratings, mask edits, registration, tool dispatch
  masks.py              # existing mask inventory by subject/session/space
  disconnectomes.py     # BCBToolkit and DeepDisco output discovery
  widgets.py            # shared NiiVue lifecycle and volume helpers
  overlay.py            # binary-mask overlay controls
  atlas_ui.py           # independent atlas/mask/subject selection
  synthetic.py          # benchmark phantom generation
src/
  analysis_*.sh         # retained analytical entry points
  python/               # implementations called by those entry points
  r/                    # LINDA API and transform helpers
tests/
container/              # in-container wrapper source and build instructions
aphasia-kb/             # knowledge base, extraction, review, and interpretation
```

## Updated imports and entry points

| Previous path/import | Replacement |
|---|---|
| `import linda_qc as q` | `from calmar import qc as q` |
| `import calmar_masks as cm` | `from calmar import masks as cm` |
| `import calmar_widgets as cw` | `from calmar import widgets as cw` |
| `import calmar_disconnectomes as cd` | `from calmar import disconnectomes as cd` |
| `from calmar_overlay import mask_comparison` | `from calmar.overlay import mask_comparison` |
| `from calmar_atlas_ui import OverlapSelection` | `from calmar.atlas_ui import OverlapSelection` |
| `from synthetic_stroke import synthetic_install` | `from calmar.synthetic import synthetic_install` |
| root `linda_predict_with_mask.sh` | `src/analysis_17_linda_predict_with_mask.sh` |
| root `linda_predict_with_mask.R` | `src/r/linda_predict_with_mask.R` |
| root `warp_native_to_mni.sh` | `src/analysis_15_warp_native_to_mni.sh` (same arguments) |
| `src/inspect_alignment.py` | `src/python/inspect_alignment.py` |
| `src/refresh_corrected_disconnectomes.py` | `src/python/refresh_corrected_disconnectomes.py` |
| `src/warp_native_mask_to_ch2.R` | `src/r/warp_native_mask_to_ch2.R` |

The redundant root warp wrapper has been removed. The actual Neurodesk command
`linda_predict_with_mask.sh` provided by the installed container keeps its name;
notebook calls to that command are intentional. The repository fallback is
analysis step 17, which pins LINDA 0.5.1 in Neurodesk and retains native-R
dispatch outside Neurodesk.

`calmar.qc` resolves repository resources relative to its installed source
location and passes `CALMAR_SOURCE_DIR` to the wrappers. Standalone analytical
scripts resolve `PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"`; they must not infer a
Slurm submission directory from a spool copy's filename. Submit from the project
root and create `logs/` first, following `AGENTS.md` in the execution environment.

## Scope and compatibility

Both notebooks, tests, container build examples, and local benchmark-script
callers use the new locations. Restart an existing notebook kernel after pulling
this change, then rerun Setup. Do not mix old root-module instances with the new
package's viewer registry.

This is a source layout change. Data, derivatives, QC sidecars, report locations,
scientific parameters, and saved provenance remain in place. The two-subject
end-to-end run and browser QC are still required; import and callback tests do
not replace them. Historical scripts are recoverable from the pre-migration Git
commit recorded in `alignment-repair/astra.yaml`; the local cleanup manifest also
preserves unpublished benchmark-script versions.

## Files removed or archived locally

Generated Python bytecode can be removed and regenerated on import. Old notebook
snapshots and checkpoints with recovery value are archived under the ignored
`notes/archive/repository-layout-2026-09-24/` directory with original paths and
SHA-256 hashes in `manifest.json`. They are not scientific results and are not
published as source files.

Preserve the separate, unfinished synthetic-benchmark work and existing ASTRA
records. Absence of a caller in the main notebook does not make benchmark, KB,
container, or provenance files obsolete.
