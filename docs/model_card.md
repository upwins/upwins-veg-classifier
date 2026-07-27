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
- _Fill in: collection dates, sites, # spectra per class, train/val/test split._

## Intended use
Per-pixel classification of reflectance imagery collected with the **same
sensor and band configuration** as the training reference image. Prediction
asserts a band match before running.

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
- Reproducibility: notebook 01 calls `tf.keras.utils.set_random_seed(42)` and
  seeds both `train_test_split` calls with `random_state=42`, so a rerun in the
  **same environment** reproduces this model. Reproducing it exactly also
  requires the pinned versions in `requirements.txt`; a different TensorFlow,
  scikit-learn or numpy will change the result even with the seeds fixed.
