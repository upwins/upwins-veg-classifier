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
└── output/                     Classification maps written by prediction
```

## Getting the full dataset

The full imagery, ROI set, and spectral library are distributed separately
(they are too large for git). _Fill in the download link / DOI here._ After
downloading, place them to match the layout above, or edit the paths in
`config.yaml` to point at wherever you keep them.

The devcontainer bind-mounts an external data directory
(`~/projects/upwins/data`) to `data/` inside the container, so you can keep the
full dataset outside the repo entirely.
