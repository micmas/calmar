Follow-up scope from notebook use (cell numbers refer to the current notebook):

- Map the essential workflow from configuration through processing, QC, and reports. Move exploratory/debugging cells into a clearly marked optional section or a separate diagnostic notebook, preserving useful checks.
- Consolidate repeated selectors and visualizations without deleting distinct scientific checks. Cell 30 compares masks in native T1 space and reports overlap metrics; cell 84 checks all masks in MNI space. Make these explicit QC modes/stages, with prerequisites visible.
- Keep visualization cells read-only. Warping, cache repair, and inference should have explicit processing steps in retained scripts, rather than being hidden prerequisites inside viewer cells.
- Use consistent subject/session, mask, and atlas selection throughout. Offer only valid combinations and explain missing outputs. Each panel must retain its own callbacks when later cells run.
- Preserve existing outputs, QC ratings, scientific decisions, and provenance during incremental cleanup. Avoid a broad notebook rewrite until the current workflow passes fresh-participant verification.
- Cross-reference #5 for stale atlas tables, subject/session cache keys, and changed-mask invalidation; a functioning selector does not establish that a cached table is current.

Fresh-cohort acceptance run: two or three previously unprocessed participants with T1, T2, and manual masks. The notebook is now configured for sub-M2018/ses-341 and sub-M2034/ses-1568; the run is pending. Verify LINDA, SynthStroke, and manual masks in both spaces; BCBToolkit for each mask; all four DeepDisco models for each mask; and matching mask/atlas selections in tables and viewers. Check cell 30's toggles after later cells execute, switch mask source in cell 67, exercise both selectors in cell 71 and the brain viewer in cell 74, then repeat the viewer cells to check lifecycle behavior.

Immediate fixes are intentionally limited to overlay opacity controls and isolation/validation of the affected selectors. Broader workflow cleanup remains in this issue.
