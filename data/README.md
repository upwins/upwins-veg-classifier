# Data

Large data is **not** committed to this repo. Only a small sample lives under
`data/sample/` so a fresh clone can run both notebooks end to end.

## Expected layout

```
data/
├── sample/                     Small committed example (cropped image + a few ROIs)
│   ├── raw_0_ref  raw_0_ref.hdr    A small ENVI reflectance cube
│   └── ...
├── library/
│   └── library_with_Genus_species.pkl   Full spectral library (pickled DataFrame)
├── rois_labeled/               Labeled training ROIs (.pkl), any subfolder depth
├── metrics/                    Per-task metric CSVs written by training
└── output/                     Classification maps written by prediction
```

`metrics/` and `output/` are created on demand and are gitignored — they hold
run artifacts, not inputs. Their locations come from `paths.metrics_dir` and
`prediction.output_dir` in `config.yaml`.

## Where training ROIs come from

The labeled ROI `.pkl` files are produced by the interactive hsiViewer in the
companion **`upwins-hsi-preprocessing`** repo (raw → reflectance → ROIs). They
are pickled `hsiViewer.hsi_viewer_ROI.ROIs_class` objects; this repo bundles a
small dependency-free stand-in for that class (`src/hsiViewer/`) so the training
notebook can load them without the PyQt viewer. Name ROIs with the same
convention as the spectral library (e.g. `Ammo_bre_...`) so their labels line up.

## Getting the full dataset

The full imagery, ROI set, and spectral library are distributed separately
(they are too large for git).

> **TODO (data owner):** add the download link or DOI here. Until this is
> filled in, a fresh clone has no way to obtain the full dataset.

After downloading, place the files to match the layout above, or edit the paths
in `config.yaml` to point at wherever you keep them.

The devcontainer bind-mounts an external data directory
(`~/projects/upwins/data`) to `data/` inside the container, so you can keep the
full dataset outside the repo entirely. That host path is hardcoded in
`.devcontainer/devcontainer.json` and must be edited if yours differs; see the
README's Data section for the details and one gotcha (the mount hides the
committed `data/sample/`).
