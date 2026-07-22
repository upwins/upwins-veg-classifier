# UPWINS Vegetation Classifier

Train a multi-task 1D convolutional neural network to identify coastal
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
python -m venv .venv && source .venv/bin/activate    # or use the devcontainer
pip install -r requirements.txt
pip install -e .                                      # makes `upwins_veg` importable

# 2. Point config.yaml at your data (a small sample is included under data/sample/)

# 3. Launch Jupyter and run the two notebooks in order
jupyter lab
```

| Notebook | What it does |
|----------|--------------|
| `notebooks/01_train_multitask_cnn.ipynb` | Loads the spectral library + ROIs, resamples to the sensor's bands, trains the CNN, and writes the model bundle to `models/example_model_v1/`. |
| `notebooks/02_batch_predict_image.ipynb` | Loads that bundle and classifies a reflectance image, writing an ENVI classification map. |
| `notebooks/03_display_classification.ipynb` | Displays an ENVI classification map with a color-coded, labeled legend. |

Each code cell has a short markdown cell above it explaining what it does, so
the notebooks double as a written walkthrough. If you're recording or following
the tutorial videos, `docs/recording_runbook.md` is the high-level guide.

## Layout

```
config.yaml              All paths and hyperparameters live here.
notebooks/               The two deliverable notebooks (run in order).
src/upwins_veg/          Importable support code (installed via `pip install -e .`).
models/example_model_v1/ The trained model bundle (model + scaler + label maps + wavelengths).
data/sample/             Small committed sample so a fresh clone runs.
docs/                    Model card + executed HTML exports of the notebooks.
```

## The model bundle

`models/example_model_v1/` holds four coupled files that must always travel
together — a mismatch silently produces wrong class names:

- `model.keras` — the trained network
- `scaler.pkl` — the `StandardScaler` fit on the training spectra
- `label_maps.json` — maps each output index to a class name
- `wavelengths.json` — the band centers the model expects (checked at predict time)

## Data

Only a small sample ships in the repo. The full imagery, ROIs, and spectral
library are large; see `data/README.md` for how to obtain and place them.

## Acknowledgment

This material is based upon work supported by the National Science Foundation
under Grant No. 2319470.
