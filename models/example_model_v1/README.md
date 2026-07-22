# Model bundle: example_model_v1

Running `notebooks/01_train_multitask_cnn.ipynb` writes the trained bundle here:

- `model.keras`
- `scaler.pkl`
- `label_maps.json`
- `wavelengths.json`

Commit these four (they are small — `model.keras` is only a few MB) so the
client can run prediction without retraining. See `docs/model_card.md`.
