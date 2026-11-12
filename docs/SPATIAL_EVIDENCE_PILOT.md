# Spatial evidence pilot for reports

The KB owns study findings and the shared atlas correspondence engine. CALMaR
owns participant measurements and presentation. This opt-in pilot writes a
separate HTML appendix and JSON audit record; it does not change the participant
report, approve evidence, or predict a participant's symptoms.

Update a Neurodesk checkout with `git pull --ff-only` followed by
`git submodule update --init --recursive`. Inspect the interface with
`python -m calmar.spatial_evidence --help`.

Execution uses the same latest-KB update policy as notebook Setup, including
an explicit warning if the latest version cannot be verified. The JSON records
the update status and exact commit. The submodule pin is a tested fallback;
it does not hold normal runs on an older KB.

## Inputs and execution

Use two versioned atlas manifests and original evidence records in the format
specified in [the KB harmonisation guide](../stroke-aphasia-kb/atlas_mapping/HARMONISATION.md).
Only deterministic, non-overlapping label images are supported. Both images
must have the same explicit template space, grid and affine. The tool does no
registration, resampling, threshold selection or atlas downloading.

An optional lesion manifest describes an already processed binary mask:

```json
{
  "image": "lesion-in-atlas-space.nii.gz",
  "space": "EXACT_TEMPLATE_IDENTIFIER_MATCHING_ATLASES",
  "world_axes": "RAS+",
  "provenance": "Processing run and transform/QC artifact references",
  "qc_status": "Actual documented QC status"
}
```

The supplied QC status is recorded, not verified by this tool. Matching headers
cannot establish anatomical registration quality. Before real-data execution in
Neurodesk, follow AGENTS.md: preflight, verified software versions, retained
analysis script, ASTRA specification, Slurm execution, visual QC and provenance
publication. The command to put in that analysis step is:

```bash
python -m calmar.spatial_evidence \
  --source study-atlas.json --target report-atlas.json \
  --records findings.json --lesion lesion.json \
  --output-dir results/spatial-pilot/participant-01
```

Choose a new output directory for each attempt. The JSON retains image hashes,
engine provenance, KB revision, original findings, directional overlaps and
unmapped tissue. The HTML is an experimental appendix for inspection.

## White matter belongs in both layers

CALMaR already reports normative lesion-based disconnection and participant
tract-microstructure measurements separately. This appendix adds geometry; it
does not replace those sections or merge their evidence.

Evidence records may declare `tissue_class` (`grey_matter`, `white_matter`,
`mixed`, `unspecified`) and `measurement_kind` (`direct_lesion_overlap`,
`normative_disconnection`, `participant_diffusion`, `unspecified`). Missing
values remain unspecified. This metadata must be checked against the paper,
not inferred from a tract name. The appendix records whether a study uses the
same measurement family as its direct lesion measurements, but even a match
requires review and never permits automatic clinical inference.

Keep three quantities distinct:

- Direct lesion intersection: fraction of a labelled tract region inside the
  lesion, not a percentage of fibres severed or a whole-tract disconnection rate.
- Normative disconnection: model-derived estimates from a lesion and reference
  connectivity, with model, thresholds and reference population retained.
- Participant diffusion: the actual metric (e.g. FA or MD), acquisition,
  processing, tract definition and study relationship direction retained.

JHU labels and JHU probabilistic tractography are different atlas products
([FSL documentation](https://fsl.fmrib.ox.ac.uk/fsl/docs/other/datasets.html)).
Overlapping/probabilistic tract maps need a separate implementation; do not
collapse them into exclusive labels just to fit this pilot. A tract not covered
by an atlas is unmeasured, not intact. A tract without an eligible KB finding
has anatomical context only, not evidence of no functional consequence.

## First use cases in Neurodesk

| Case | Inputs | Acceptance criterion |
|---|---|---|
| Broad ROI spans five parcels | Processed lesion, two verified atlases, source-reviewed KB finding | One finding retained with five spatial candidates; direct lesion measurements in each atlas |
| Same broad burden, different locations | Two synthetic masks before using real participants | Same broad damage fraction can produce different child-region damage; never multiply parent damage by overlap weights |
| White-matter lesion and disconnection | Processed lesion plus existing CALMaR disconnectome report and a tract-specific KB finding | Direct intersection and normative disconnection stay separately labelled, even for the same named tract |
| Diffusion association in KB | Source-reviewed FA/MD finding and participant diffusion outputs | Metric and direction retained; not treated as a lesion-overlap effect or counted as independent corroboration from the same cohort |
| Different template or unknown tract definition | Deliberately mismatched manifests or label-only finding | Spatial mismatch refused; unresolved evidence remains unresolved |

Before report integration, inspect overlays and atlas coverage for real data;
check tract laterality, subdivisions, measurement method, population, time since
stroke, outcome, relationship direction and shared cohorts against the source.
A reported coordinate alone must not become an effect over an entire tract.
Current tests validate software behaviour using synthetic data only. No real
atlas equivalence or patient interpretation has yet been validated by this pilot.
