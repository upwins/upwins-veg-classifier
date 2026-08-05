# Model bundle: example_model_v1

Running `notebooks/01_train_multitask_cnn.ipynb` writes the trained bundle here:

- `model.keras`
- `scaler.pkl`
- `label_maps.json`
- `wavelengths.json`

Training also writes `best_weights.weights.h5` here. It is a by-product of the
train cell, not part of the bundle — nothing reads it back.

**None of these files are committed to the repo** — a fresh clone finds only
this README and `model_card.md`. The bundle is produced by training, not
distributed with the repo, so run notebook 01 to populate this directory before
running prediction. The four bundle files are coupled and must always travel
together; see `docs/model_card.md`.
