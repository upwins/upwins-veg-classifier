# UPWINS Vegetation Classifier

Train a multi-task 1D convolutional neural network to identify
vegetation from hyperspectral reflectance, then batch-classify imagery.
The model learns from a labeled **spectral library** combined with labeled
**regions of interest (ROIs)** drawn on imagery, and predicts five attributes
per pixel: *plant, age, part, health, lifecycle*.

This is the training-and-prediction half of the UPWINS pipeline. Producing the
reflectance imagery and ROIs it consumes is covered in the companion
`upwins-hsi-preprocessing` project.

## Quickstart

```bash
# 1. Create the environment (matches the pinned versions the model was built with)
#    The devcontainer does both of these steps for you; skip to step 2 if you use it.
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e .                                      # makes `upwins_veg` importable

# 2. Point config.yaml at your data (see docs/data.md for the expected layout)

# 3. Launch Jupyter and run the three notebooks in order
jupyter lab
```

| Notebook | What it does |
|----------|--------------|
| `notebooks/01_train_multitask_cnn.ipynb` | Loads the spectral library + ROIs, resamples to the sensor's bands, trains the CNN, and writes the model bundle to `models/example_model_v1/`. |
| `notebooks/02_batch_predict_image.ipynb` | Loads that bundle and classifies a reflectance image, writing an ENVI classification map. |
| `notebooks/03_display_classification.ipynb` | Displays an ENVI classification map with a color-coded, labeled legend. |

Each code cell has a short markdown cell above it explaining what it does, so
the notebooks double as a written walkthrough — read top to bottom, they are
the documentation for the pipeline.

## Layout

```
config.yaml              All paths live here. The training hyperparameters are the
                         deliberate exception -- they sit in notebook 01's setup cell,
                         where you tune them by re-running.
notebooks/               The three deliverable notebooks (run in order).
src/upwins_veg/          Importable support code (installed via `pip install -e .`).
src/hsiViewer/           Stand-in ROIs_class so ROI pickles load without the PyQt viewer.
models/example_model_v1/ Where notebook 01 writes the model bundle -- not populated in a fresh clone; see its README.
examples/                No runnable example ships; run against your own data -- see its README.
data/                    Not committed -- external data and run outputs; see docs/data.md.
docs/                    Model card and data guide.
```

## The model bundle

`models/example_model_v1/` is written to hold four coupled files that must
always travel together — a mismatch silently produces wrong class names:

- `model.keras` — the trained network
- `scaler.pkl` — the `StandardScaler` fit on the training spectra
- `label_maps.json` — maps each output index to a class name
- `wavelengths.json` — the band centers the model expects (checked at predict time)

These are **produced by running notebook 01, not distributed with the repo** — a
fresh clone must train first to populate the bundle before running prediction.

Training also writes `best_weights.weights.h5` into the same directory. It is a
by-product of the train cell, not part of the bundle: nothing reads it back, and
prediction needs only the four files above.

## Data

No data ships in the repo. `data/` holds the imagery, ROIs, spectral library and
run outputs, and is gitignored in full — a fresh clone does not have it. See
**`docs/data.md`** for the expected layout and how to obtain the dataset.

### If you use the devcontainer

`.devcontainer/devcontainer.json` bind-mounts an external data directory over
`data/` inside the container, so the full dataset can live outside the repo:

```
source=${localEnv:HOME}/projects/upwins/data  ->  /workspaces/upwins-veg-classifier/data
```

**The host path is hardcoded.** If your data is not at `~/projects/upwins/data`,
edit that `mounts` line before opening the container — Docker silently creates
an empty directory for a source path that does not exist, and the notebooks then
fail with confusing missing-file errors rather than saying the mount was wrong.

Because nothing is committed under `data/`, the mount hides nothing: inside the
container, `data/` is simply your external directory.

## Acknowledgment
