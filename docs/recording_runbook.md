# Recording Runbook — Vegetation Classifier Tutorial

A high-level guide to follow **while recording**. The detailed narration is
already in the notebooks: the markdown cell above each code cell is your
script, so on camera you can read/paraphrase it and run the cell. This runbook
just gives you the running order, the beats to emphasize, and the gotchas.

> **Scope.** This repo covers the **second half** of the pipeline — training a
> model and classifying imagery. The first half (raw image → reflectance → ROI
> creation) lives in the `species_mapping` repo and is a separate video; a
> matching runbook for it comes later.

---

## 0. Before you hit record

- [ ] `pip install -r requirements.txt && pip install -e .` in a clean env (or open the devcontainer).
- [ ] Edit `config.yaml` so `paths.*` point at your **real** data for the recording.
- [ ] Confirm the data is reachable: the spectral library `.pkl`, the reference image, and the ROI directory.
- [ ] Decide how you'll handle the long training step (see the note in Part 1).
- [ ] `jupyter lab`, both notebooks open, kernels restarted so cell numbers are clean on screen.
- [ ] Clear old outputs (`Kernel → Restart & Clear Outputs`) so the run looks fresh.

**Training-time decision (important):** a full 600-epoch run is too long for a
video. Pick one:
1. **Pre-train off camera**, then on camera run **Option A — load an existing
   model** (cell in Part 1) and skip the train cell. Cleanest for a tutorial.
2. **Show a short live run** — temporarily set `training.epochs` low (e.g. 15)
   in `config.yaml` so training finishes in a minute or two on camera, and say
   the real model was trained for longer.

---

## 1. Part 1 — Training  →  `notebooks/01_train_multitask_cnn.ipynb`

Run top to bottom. Beats to hit (each maps to a narrated cell):

| Section | Say / show |
|---|---|
| Imports & **Configuration** | Everything is config-driven; the model + scaler + label maps + wavelengths are one **bundle** that always travels together. |
| **Load the spectral library** | This is the labeled reference data; mention it can be refreshed from the database but we use the shipped `.pkl`. |
| **Option 1 vs Option 2 (bands)** | The model's band axis comes from either an image or an ROI — run **one**. Explain why the library gets resampled to match the sensor. |
| **Resample the library** | Library + imagery now share one band axis. |
| **ROIs** (finder → find → prepare → combine) | ROIs are labeled pixels drawn on imagery; stratified sampling keeps them balanced; they're combined with the library. |
| **Encode / split / standardize** | Point out that `scaler.pkl` **and** `wavelengths.json` get saved here — that's what makes prediction safe later. |
| **Build → Compile → Train** | One shared CNN backbone, five task heads. Early stopping restores the best weights. *(Apply your training-time decision here.)* |
| **Evaluate** | Show the per-task accuracy, the detailed report, and at least one **confusion matrix** — this is the satisfying payoff shot. |

**Expected result on screen:** `models/example_model_v1/` fills with
`model.keras`, `scaler.pkl`, `label_maps.json`, `wavelengths.json`. Show that
directory before moving on — it's the hand-off to Part 2.

---

## 2. Part 2 — Prediction  →  `notebooks/02_batch_predict_image.ipynb`

Run top to bottom.

| Section | Say / show |
|---|---|
| **Load model & scaler** | We're loading exactly the bundle Part 1 wrote. |
| **Load / preview label maps** | Show the class names the model outputs. |
| **Classify the image** | Highlight the **band-match assertion** — it refuses to run on an image whose bands don't match the model, turning a silent wrong answer into a clear error. Then it classifies chunk-by-chunk. |

**Expected result on screen:** ENVI classification maps appear in
`data/output/` (one per task). If you have a viewer handy, open the `plant`
classification map over the image for the closing shot — collected the same day
as the training image, so its bands already match.

---

## 3. Talking points worth landing

- **Why multi-task:** one network predicts five attributes at once, sharing features.
- **Why library + ROIs:** the library gives clean labeled spectra; ROIs ground it in real imagery.
- **Why the bundle stays together:** a scaler/label-map/model from different runs silently produces wrong class names — keeping them in one dir prevents that.
- **Why the band check:** the #1 way prediction goes wrong is feeding an image with the wrong bands; the assertion catches it.

---

## 4. After recording

- Tag the exact state you filmed so viewers can reproduce it:
  ```bash
  git tag -a v1.0.0-tutorial -m "State used in the tutorial videos"
  git push origin v1.0.0-tutorial
  ```
- Give viewers the pinned clone command:
  ```bash
  git clone --branch v1.0.0-tutorial https://github.com/upwins/upwins-veg-classifier
  ```
- Export executed copies to `docs/` (`jupyter nbconvert --to html --execute ...`) as a static reference viewers can compare against.
