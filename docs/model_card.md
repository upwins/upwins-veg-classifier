# Model Card — example_model_v1

## Overview
Multi-task 1D CNN that classifies a hyperspectral reflectance *pixel spectrum*
into five attributes: plant, age, part, health, lifecycle.

## Bundle contents
| File | Purpose |
|------|---------|
| `model.keras` | Trained Keras model. |
| `scaler.pkl` | `StandardScaler` fit on the training spectra. Apply before inference. |
| `label_maps.json` | Output index -> class name, per task. |
| `wavelengths.json` | Band centers (nm) the model expects. |

## Training data
- Spectral library: labeled ASD spectra (`plant/age/part/health/lifecycle`).
- Labeled ROIs drawn on reflectance imagery, resampled to the sensor bands.
- ROI pixels are subsampled before training (`stratified_sample_with_min_per_roi`,
  notebook 01): at least 30 pixels from each ROI (`Name` + `Color` group), up to
  300 pixels total, so no single large ROI dominates.
- Split 70 / 15 / 15 train / validation / test, per pixel, stratified on `plant`.
- _Fill in: collection dates, sites, number of spectra per class, library vs.
  ROI counts._

## Intended use
Per-pixel classification of reflectance imagery collected with the **same
sensor and band configuration** as the training reference image. Prediction
asserts a band match before running.

## Preprocessing

Applied in this order, at both training and prediction time:

1. **Resample** to the model's band axis (`spectral.BandResampler`). The axis
   comes from a reference image or a reference ROI and is recorded in
   `wavelengths.json`.
2. **Pixel-wise min-max normalization**, *piloted-platform data only* —
   filenames matching `upwins_veg.preprocessing.PILOTED_SOURCE_PATTERNS`
   (`crisfield`, `piloted`). Training and prediction call the same helper.
3. **Standardization** with the `StandardScaler` in `scaler.pkl`, fit on the
   training split only.
4. Reshape to `(batch, bands, 1)` for the Conv1D input.

## Architecture

`build_spectral_cnn` in notebook 01. Shared 1D-CNN backbone, five softmax heads.

| Stage | Layers |
|-------|--------|
| Block 1 | Conv1D(32, k=7, ReLU, same) → BatchNorm → MaxPool(3) → Dropout(0.25) |
| Block 2 | Conv1D(64, k=5, ReLU, same) → BatchNorm → MaxPool(3) → Dropout(0.25) |
| Block 3 | Conv1D(128, k=3, ReLU, same) → BatchNorm → MaxPool(3) → Dropout(0.30) |
| Shared head | Flatten → Dense(128, ReLU) → BatchNorm → Dropout(0.50) |
| Task heads | `plant`: Dense(64, ReLU) → Dense(n, softmax). `age`, `part`, `health`, `lifecycle`: Dense(32, ReLU) → Dense(n, softmax). |

Input length is the band count in `wavelengths.json`; each `n` is the class count
in `label_maps.json`.

## Training configuration

| Setting | Value |
|---------|-------|
| Optimizer | Adam, learning rate 1e-4 |
| Loss | `sparse_categorical_crossentropy` per head, task weights all 1.0 |
| Batch size | 32 |
| Epochs | up to 600, `EarlyStopping(monitor='val_loss', patience=30, restore_best_weights=True)` |
| Masking | `'N'` (unlabeled) samples get sample weight 0 for `plant`, `age`, `part`, `health`, so they contribute no loss and are excluded from the reported metrics. **`lifecycle` is the exception**: `'N'` ("Neither") is a real trained class there. |
| Seeds | `random.seed(42)`, `np.random.seed(42)`, `tf.random.set_seed(42)`; `random_state=42` on both splits |

- _Fill in: epochs actually run before early stopping._

## Metrics

### What the held-out numbers do and do not measure

The train/val/test split is **per pixel**, not per ROI. Pixels from a single ROI
are therefore spread across all three splits, and pixels within one ROI are
spatially autocorrelated — neighbouring pixels of the same leaf are nearly
identical spectra. The overall test accuracy consequently measures

> *how well the model labels pixels drawn from the same ROIs, on the same
> imagery, that it was trained on*

and **not** how well it will label a fresh image with no ROIs of its own. Expect
performance on new imagery to be lower than the overall number below. A group
split on `roi_name` would remove this leakage; it is deliberately deferred
because it costs whole ROIs of training data while the ROI set is still small.

The split is stratified on `plant`, so every species is represented in all three
splits in proportion — the overall number is not inflated by a species dropping
out of the test set.

### Report both numbers

Notebook 01 evaluates the test set three ways. Record the first two here.

| Metric | Notebook cell | What it means |
|--------|---------------|---------------|
| **Overall test** | "Evaluate on the test set" | Optimistic, for the reason above. Use it to compare training runs, not to predict field performance. |
| **Library-only test** | "Optional — library-only accuracy" | Held-out ASD library spectra only. No ROI pixels, so no per-image leakage — the better partial proxy for generalization beyond the imagery the ROIs came from. |
| ROI-only test | "Optional — ROI-only accuracy" | Held-out ROI pixels only. Carries the full leakage; useful for diagnosis, not for reporting. |

- Overall test, per task (accuracy / weighted F1): _fill in_
- Library-only test, per task (accuracy / weighted F1): _fill in_
- _Fill in: number of test spectra in each of the two groups (printed by the
  split cell)._

## Limitations
- Sensitive to the library/version it was trained with (see requirements.txt).
- Not validated on sensors or band configurations other than the training one.
- Held-out metrics overstate performance on unseen imagery — see Metrics above.
- Pixel-wise min-max normalization is applied to piloted-platform data only,
  selected by filename (`upwins_veg.preprocessing.PILOTED_SOURCE_PATTERNS`).
  Training and prediction share that helper, so they cannot diverge — but
  renaming a file changes how it is preprocessed.

## Provenance
- Trained by: _fill in_
- Date: _fill in_
- Environment: NVIDIA `nvcr.io/nvidia/tensorflow:24.12-tf2-py3` (TF 2.17).
- Reproducibility: notebook 01 seeds Python, NumPy and TensorFlow directly and
  seeds both `train_test_split` calls with `random_state=42`, so a rerun in the
  **same environment** reproduces this model. Reproducing it exactly also
  requires the pinned versions in `requirements.txt`; a different TensorFlow,
  scikit-learn or numpy will change the result even with the seeds fixed.
  The three seed calls are deliberately not replaced by
  `tf.keras.utils.set_random_seed(42)` — under tf_keras 2.17 on Python 3.12 that
  helper makes the first Conv1D fail to build. See the comment in notebook 01's
  setup cell.

## Still to fill in

Everything above that is not marked `_fill in_` was read off the code and is
accurate for any bundle notebook 01 produces. What remains needs either the
trained bundle or facts only the data owner has:

**From the bundle, once it exists** (`models/example_model_v1/`):

- [ ] Band count and wavelength range — `len(wavelengths.json)`, first and last entry.
- [ ] Class counts per task — `{k: len(v) for k, v in label_maps.json.items()}`.
- [ ] Epochs actually run before early stopping.

**From the training run** (printed by notebook 01's evaluation cells):

- [ ] Overall test accuracy / weighted F1, per task.
- [ ] Library-only test accuracy / weighted F1, per task.
- [ ] Test-set size for each of those two groups.

**From you** — nothing in the repo can supply these:

- [ ] Collection dates and sites for the imagery and the ASD library.
- [ ] Number of spectra per class, and the library-vs-ROI breakdown.
- [ ] Who trained the model, and on what date.
- [ ] Any known failure modes observed in the field.
