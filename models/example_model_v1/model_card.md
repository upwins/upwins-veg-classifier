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
- _Fill in: per-task test accuracy / weighted F1 from the training notebook's
  evaluation cells._

## Limitations
- Sensitive to the library/version it was trained with (see requirements.txt).
- Not validated on sensors or band configurations other than the training one.

## Provenance
- Trained by: _fill in_
- Date: _fill in_
- Environment: NVIDIA `nvcr.io/nvidia/tensorflow:24.12-tf2-py3` (TF 2.17).
