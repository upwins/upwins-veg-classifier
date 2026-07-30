# Model bundle: example_model_v1

Running `notebooks/01_train_multitask_cnn.ipynb` writes the trained bundle here:

- `model.keras`
- `scaler.pkl`
- `label_maps.json`
- `wavelengths.json`

**These four files are not committed to the repo** — a fresh clone finds only
this README. The bundle is produced by training, not distributed with the repo,
so run notebook 01 to populate this directory before running prediction. The
four files are coupled and must always travel together; see `docs/model_card.md`.
