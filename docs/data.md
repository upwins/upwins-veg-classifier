# Data

No data is committed to this repo. Everything under `data/` is external —
either downloaded, bind-mounted, or written by a run — and the whole directory
is gitignored. A fresh clone has no `data/` at all; it is created by the
devcontainer mount, or by the notebooks when they write their outputs.

## Expected layout

```
data/
├── library/
│   └── library_with_Genus_species.pkl   Full spectral library (pickled DataFrame)
├── rois_labeled/               Labeled training ROIs (.pkl), any subfolder depth
├── metrics/                    Per-task metric CSVs written by training
└── output/                     Classification maps written by prediction
```

`metrics/` and `output/` are created on demand — they hold run artifacts, not
inputs. Their locations come from `paths.metrics_dir` and
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

## The devcontainer mount

`.devcontainer/devcontainer.json` bind-mounts an external data directory onto
`data/` inside the container, so the full dataset can live outside the repo
entirely:

```
source=${localEnv:HOME}/projects/upwins/data  ->  /workspaces/upwins-veg-classifier/data
```

**The host path is hardcoded.** If your data is not at `~/projects/upwins/data`,
edit that `mounts` line before opening the container — Docker silently creates
an empty directory for a source path that does not exist, and the notebooks then
fail with confusing missing-file errors rather than saying the mount was wrong.

Because `data/` holds no committed content, the mount hides nothing: inside the
container, `data/` is simply your external directory. Anything the repo ships
that a run needs — such as a small runnable example — lives outside `data/`
(see `examples/`) so the mount cannot cover it.
