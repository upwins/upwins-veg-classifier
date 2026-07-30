# Repo audit — findings and remediation plan

Audit of `upwins-veg-classifier` for client handoff readiness.
Audited 2026-07-27 on branch `claude/dockerfile-pip-install-editable-fup5kp`.
**Revised 2026-07-27 after implementing Phases 2–5 and Phase 7** on branch
`claude/plan-phases-2-5-71wsyr`. Phase 6 was declined by the client.
**Status reconciled 2026-07-29** against the committed tree — see the overlay
below.
**Closed out 2026-07-30:** the client decided **not to ship any artifacts**
(no A1, A2, A3 — no model bundle, sample data, or executed HTML exports) and
**not to ship test files** (Phase 6). Phase 1 is therefore resolved by the
documentation path, not by shipping artifacts; every phase in this plan is now
either done or a recorded decision. See the Phase 1 and Phase 6 sections.

---

## Status at a glance

> **Status overlay — reconciled against the codebase 2026-07-29.** When this plan
> was written, `main` was at `62675ac` and Phases 2–5 and 7 lived on the unmerged
> branch `claude/plan-phases-2-5-71wsyr`. **Those phases have since merged to
> `main`** (commits `c8e8e69`..`7bb1f2d`), and follow-up commits refined them
> further; `main` is now at `ee8b474`. Each row's status is verified directly
> against `origin/main` (`git log` / `git show` over the committed tree), and
> every Phase heading below carries an inline **Status** line.
>
> Legend — ✅ **Done** (implemented on `main`) · ⛔ **Deferred** (a live client
> decision, intentionally left as-is) · 🔲 **To do** (still open — client input or
> a follow-up commit).

| Phase | Covers | Status on `main` |
|---|---|---|
| 1 — Make the promises true | A1, A2, A3 | ✅ Done (by decision) — client decided **not to ship artifacts** (2026-07-30). The docs are made honest instead: the README and the `models/`, `examples/` and `data/` docs state plainly that the bundle and data are produced/obtained separately, not distributed with the repo. See Phase 1. |
| 2 — Normalization asymmetry | B1 | ✅ Done — `c8e8e69` |
| 3 — Fail loudly | B2, B3 | ✅ Done — `c082a5b` |
| 4 — Reproducible training + metrics doc | B4 | ✅ Done — `d05fe19`; seeding mechanism later corrected in `1006e0e` |
| 5 — Packaging comment | C1 (C2 declined) | ✅ Done — `f23c65c` |
| 6 — Smoke tests; CI | C3 | ⛔ Declined — no test files in this repo (client, 2026-07-27, reaffirmed 2026-07-30); CI moot along with it |
| 7 — Docs and hygiene | C4–C8 | ✅ Done — `7bb1f2d`; data docs relocated & mount simplified in `17c82ac`, metrics comment corrected in `26f1f9c` |

**Net:** every phase is now closed. Phases 2–5 and 7 are implemented on `main`;
**Phase 1 is resolved by the documentation path** — the client decided not to
ship the sample cube, the trained bundle, or the executed HTML exports, so the
docs are made honest about their absence rather than the artifacts being added.
**C2** and **C3 / Phase 6** are the recorded declines. Nothing in Phases 2–5 or 7
was executed end to end — there is still no training data and no GPU in this
environment; verification was static plus targeted unit-level execution of the
extracted logic (details under "What was verified" below).

---

## Context for a fresh implementation session

Read this section first. It contains everything a new session needs that is not
recoverable from the repo itself.

### Repo state

**Updated 2026-07-29. `main` is now at `ee8b474`. Phases 2–5 and 7 (`c8e8e69`..`7bb1f2d`)
have been merged into `main`,** so the branch `claude/plan-phases-2-5-71wsyr` is no
longer the place to start — begin from `main`. Every phase in this plan is now
either done or a recorded decision: Phase 1 was closed on 2026-07-30 by the
client's decision not to ship artifacts (the docs are made honest instead), and
Phase 6 stays declined. There is nothing left to implement.

Six follow-up commits landed on `main` after the phase merge and refine it; do
not redo them:

| Commit | What changed |
|--------|--------------|
| `17c82ac` | Made `data/` purely the mount: `data/README.md` → `docs/data.md`, `data/sample/README.md` → `examples/README.md`, `.gitignore` collapsed to a plain `data/`. The "the mount hides `data/sample/`" warning (Phase 7 / C8) was **deleted** rather than documented, because nothing is committed under `data/` any more. |
| `1006e0e` | Replaced Phase 4a's `tf.keras.utils.set_random_seed(42)` with three direct seed calls (`random.seed`/`np.random.seed`/`tf.random.set_seed`). `set_random_seed` crashed the first `Conv1D` build on Python 3.12 + tf_keras 2.17 (`'float' object cannot be interpreted as an integer`); the direct calls keep determinism unchanged. |
| `26f1f9c` | Corrected the `paths.metrics_dir` comments (C6): the CSVs were **never committed** — cell 59 wrote them untracked into `notebooks/`, a hazard, not an incident. |
| `6da1e5f`, `f2628e9` | Trimmed the `metrics_dir` comments. |
| `ee8b474` | Labeling changes. |

Pre-audit cleanup, already on `main`; do not redo:

| Commit | What changed |
|--------|--------------|
| `62675ac` | De-duplicated the ROI label taxonomy: notebook 01 now imports `find_roi_files` and the five code tables from `upwins_veg.roi_labels` instead of redefining them. `find_roi_files` matches `.endswith('.pkl')` and returns sorted. |
| `57d7eb1` | Removed outdated commented-out code from the notebooks. Kept the commented entries in `age_codes`/`principal_part_codes`/`health_codes` on purpose — they document folded-in finer-grained codes. |
| `9d0505f` | Moved `hsiViewer/` to `src/hsiViewer/` so `pip install -e .` actually installs it (`pyproject` scans `where = ["src"]` only). Fixes `ModuleNotFoundError` when unpickling ROI files. |
| `4d73b17` | Simplified the devcontainer Dockerfile (dropped the unused `python3-pyqt5` apt install). |
| `62ca834` | Added `"postCreateCommand": "python -m pip install --no-cache-dir -e ."` to `devcontainer.json`. |

Phases 2–5 and 7 — implemented on `claude/plan-phases-2-5-71wsyr`, now merged to `main`:

| Commit | Phase | What changed |
|--------|-------|--------------|
| `c8e8e69` | 2 | New `src/upwins_veg/preprocessing.py` (`PILOTED_SOURCE_PATTERNS`, `is_piloted_source`, `pixel_wise_normalize`). Notebook 01 cell 26 and `batch_predict.py` both call it instead of their own copies. |
| `c082a5b` | 3 | `classify_and_save_image` raises instead of swallowing; `batch_classify` prints each failure and ends with an "N of M classified" count plus the failing paths. Bare `except:` in `spectral_collection.py` narrowed to `except (KeyError, IndexError)` with a skipped-row report. |
| `d05fe19` | 4a/4b/4c | `tf.keras.utils.set_random_seed(42)` in notebook 01's setup cell; split cell stratified on `plant` with a min-3-per-class guard and a derived validation fraction; both model cards document what the held-out metrics do and do not measure. |
| `f23c65c` | 5 | Comments only in `pyproject.toml` and `requirements.txt` explaining the absent `[project.dependencies]` and the deliberate `license` table form. |
| `7bb1f2d` | 7 | Model card deduplicated to a stub; model card filled in from the code (preprocessing, architecture, training config) with a three-way "still to fill in" checklist; metric CSVs redirected to a new `paths.metrics_dir`; unused `import json` dropped; devcontainer bind-mount documented. |

### Environment constraints

- **No training data and no GPU.** `data/` and `models/example_model_v1/`
  contain only READMEs — see findings A1/A2. Any step that needs real spectra
  cannot be verified locally.
- `spectral` will not build from source in this environment (no wheel), so
  `batch_predict` can only be imported with `sys.modules['spectral']` stubbed.
  `numpy` and `scikit-learn` install fine and were used for the Phase 2 and 4b
  checks below.
- `pip install -e .` works and installs no third-party deps (see C1), so a plain
  `python -c "import upwins_veg"` succeeds without TensorFlow.

### Editing notebooks safely — read before touching any `.ipynb`

The notebooks round-trip **exactly** through:

```python
json.dump(nb, f, indent=1, ensure_ascii=True)   # then write a trailing "\n"
```

Using `ensure_ascii=False` (or omitting the trailing newline) rewrites every
non-ASCII character in the file and turns a three-line change into a whole-file
diff. Verify before committing:

```python
orig = open(p).read()
rt = json.dumps(json.load(open(p)), indent=1, ensure_ascii=True) + '\n'
assert orig == rt
```

Also: assert on the exact expected text before deleting or replacing cell source,
and write the edit script so it saves only after every assertion passes — a
partial write to a notebook is painful to unpick. The Phase 2/4 edit script did
this and is worth copying if more notebook work follows.

One more trap, learned in this session: when you write a cell back, store the
source as a **list of lines each ending in `\n`** (last line bare if it has no
trailing newline), not as a single string. A single-string source is legal JSON
and legal nbformat, but it changes the file's shape and produces a whole-cell
diff.

### Cell references in this document

Cell numbers below are **0-based indices into `nb['cells']`, counting markdown
cells**. They are *not* Jupyter's displayed numbering. Phases 2–5 and 7 edited
cells **in place only** — no cell was inserted or removed, so the indices below
are unchanged from the original audit and were re-verified against `main`. The
post-merge follow-ups (`1006e0e` on cell 2, `26f1f9c` on cell 59) also edited in
place, so the indices still hold. Still locate cells by content:

```python
import json
nb = json.load(open('notebooks/01_train_multitask_cnn.ipynb'))
hits = [i for i, c in enumerate(nb['cells'])
        if c['cell_type'] == 'code' and 'ANCHOR TEXT' in ''.join(c['source'])]
```

| Purpose | Anchor text | Cell |
|---------|-------------|------|
| Setup / seeding | `tf.random.set_seed(42)` *(was `tf.keras.utils.set_random_seed(42)` until `1006e0e`; the old name now survives only in that cell's explanatory comment)* | 2 |
| ROI loader + normalization | `if is_piloted_source(roi_filename):` *(was `if "crisfield" in roi_filename.lower():`)* | 26 |
| Array assembly (library + ROI concat) | `plant_array = np.concatenate((sc.name,` | 29 |
| Label encoding — defines `y_plant_labels`, used by 4b's guard | `y_plant_labels = np.unique(plant_array)` | 32 |
| Train/val/test split | `train_indices, test_indices = train_test_split(` | 34 |
| Metrics + CSV export | `EXPORT_TO_CSV` | 59 |
| Per-species test counts | `Labeled Codes and Counts in Test Set` | 61 |
| Model build | `def build_spectral_cnn(` | 42 |

Each anchor matches exactly one code cell as of `7bb1f2d`.

### How to verify work

```bash
# every code cell still parses, and the file format is unchanged
python - <<'PY'
import ast, json, glob
for p in sorted(glob.glob('notebooks/*.ipynb')):
    nb = json.load(open(p))
    for i, c in enumerate(nb['cells']):
        if c['cell_type'] == 'code' and not any(l.lstrip().startswith(('%','!')) for l in c['source']):
            ast.parse(''.join(c['source']))
    assert open(p).read() == json.dumps(json.load(open(p)), indent=1, ensure_ascii=True) + '\n', p
    print(p, 'ok')
PY

python -m pyflakes src/upwins_veg/*.py src/hsiViewer/*.py
git check-ignore -v <path>    # confirm a file is/isn't ignored before assuming
```

`pyflakes` is **clean** across `src/` as of `7bb1f2d` (Phase 7 cleared the last
item, C7's unused `import json`). Any output at all is therefore new.

---

## Verdict

**Ready to hand over.** The one item that had blocked handoff — the missing
artifacts (no trained model, no sample data) — is now a settled decision: the
client chose **not to ship them** (2026-07-30). A fresh clone therefore cannot
run the notebooks without the user first obtaining data and training a model,
and the docs now say exactly that instead of implying the files are present.
That closes Phase 1.

Everything else the audit found is closed. The correctness issues (B1–B4) are
fixed; the packaging and hygiene items (C1, C2, C4–C8) are either resolved or
explicitly declined with the reasoning recorded in the file itself. C3 (tests) is
out of scope by the client's decision.

Nothing here is a security problem. No secrets are committed, and none appear in
the history.

---

## Findings

### A. Blocking — the repo does not do what it says

**Status (2026-07-30): closed by the client's decision not to ship artifacts.**
The bundle, the sample data, and the executed HTML exports are intentionally
not distributed with the repo, and the documentation is made honest about that:
no doc claims a file a fresh clone lacks, and every place a reader might expect
one now states plainly that it is produced by training or obtained separately.
Phase 1 is resolved on the documentation path; shipping artifacts is no longer
planned.

| # | Finding | Evidence | Status |
|---|---------|----------|--------|
| A1 | **No model bundle.** `models/example_model_v1/` holds only `README.md` and `model_card.md`. None of `model.keras`, `scaler.pkl`, `label_maps.json`, `wavelengths.json` exist. | Notebook 02 cell 3 calls `tf.keras.models.load_model(...)` and will raise immediately. | ✅ Done (by decision) — bundle intentionally not shipped. The README's "The model bundle" section and `models/example_model_v1/README.md` now state the four files are produced by running notebook 01, not distributed with the repo (`67f05a6`, `b69cf35`, and the 2026-07-30 doc pass). |
| A2 | **No sample data.** `data/` no longer holds committed content (`17c82ac`); `examples/` is a placeholder README only. | `config.yaml` points `image: data/sample/raw_0_ref`, an illustrative default a comment now flags as such. | ✅ Done (by decision) — no sample data ships. `examples/README.md`, the README layout line, and `config.yaml`'s comment all state that the notebooks run against your own data (see `docs/data.md`), not a committed sample. |
| A3 | **No executed HTML exports in `docs/`.** `docs/` holds `data.md`, `model_card.md` and `recording_runbook.md`. | Producing the HTML is an action item in `docs/recording_runbook.md` §4, not a committed artifact. | ✅ Done — the README's "executed HTML exports of the notebooks" claim was dropped (`67f05a6`); the exports are a recorder action item in the runbook, not a promised committed artifact. |

A1 and A2 are *not* caused by `.gitignore`. I verified with `git check-ignore`
that all four bundle files were trackable — the files were simply never
committed. (`data/sample/` itself has since been removed from the tree by
`17c82ac`, which made `data/` purely the mount.)

### B. Correctness

| # | Finding | Location | Status |
|---|---------|----------|--------|
| B1 | **Filename-triggered normalization, asymmetric between train and predict.** Prediction normalized on `"crisfield"` **or** `"piloted"`; training on `"crisfield"` only. | `batch_predict.py` vs. notebook 01 cell 26 | ✅ Done `c8e8e69` — both sides now call `upwins_veg.preprocessing`. |
| B2 | **Failures are swallowed and reported as success.** A run that classified nothing still printed "Batch processing complete". | `batch_predict.py` | ✅ Done `c082a5b` — `classify_and_save_image` raises; `batch_classify` prints each failure and a final "N of M" count. |
| B3 | **Bare `except: continue`** silently drops spectral-library rows that fail to parse. | `spectral_collection.py:111` | ✅ Done `c082a5b` — narrowed to `(KeyError, IndexError)`, skipped rows counted and reported. |
| B4 | **Training is not reproducible;** splits not stratified. | notebook 01 cells 2 and 34 | ✅ Done `d05fe19` — deterministic seeding (the initial `set_random_seed(42)` was replaced by direct seed calls in `1006e0e`; see Phase 4a); both splits stratified on `plant` with a min-3-per-class guard. |

Two residual notes on B3: the `try` block still spans the whole per-row append
sequence, so a mid-block failure could in principle append to some metadata lists
but not others and desynchronize them. That was true before and is out of the
audit's remit (see "Out of scope"). And `spectral_collection.py` still carries
C7's unused `import json`, left for Phase 7 so the Phase 3 diff stayed to one
concern.

### C. Packaging, tests, hygiene

| # | Finding | Location | Status |
|---|---------|----------|--------|
| C1 | `pyproject.toml` declares **no `dependencies`**, so the installed package carries no dependency metadata. `pip install -e .` is the correct mechanism and works — it makes `upwins_veg` importable project-wide, which is its purpose — but it installs no third-party packages. **Low practical impact**; the documented workflow and the devcontainer both install `requirements.txt` first. | `pyproject.toml` | ✅ Done (documented) `f23c65c`. Comments in both files record that `requirements.txt` is the single source of truth. No functional change, by decision. |
| C2 | `license = {text = "MIT"}` table form; no `authors`, `urls`, `classifiers`. | `pyproject.toml` | ⛔ Deferred — declined in full (client, 2026-07-27). `f23c65c` adds a comment recording *why*, so it is not re-raised as an oversight. |
| C3 | **No tests and no CI.** | — | ⛔ Declined — out of scope (client, 2026-07-27, reaffirmed 2026-07-30); no test files in this repo. See Phase 6. |
| C4 | `model_card.md` is a **byte-identical duplicate** in `docs/` and `models/example_model_v1/`. | both files | ✅ Done `7bb1f2d` — the `models/` copy is now a stub pointing at `docs/model_card.md`. |
| C5 | **Unfilled placeholders** in client-facing docs. | model cards, `docs/data.md` | ✅ Done (partial) `7bb1f2d` — everything derivable from the code is filled in; the rest is an explicit checklist. The remaining blanks need the bundle or the data owner. |
| C6 | Metric CSVs written to the **current working directory**, not gitignored. | notebook 01 cell 59 | ✅ Done `7bb1f2d` — written to `paths.metrics_dir` (`data/metrics`, gitignored), plus a `classification_report_*.csv` ignore rule; comment framing corrected in `26f1f9c` (the CSVs were never committed — an untracked-accumulation hazard, not an incident). |
| C7 | Unused `import json`. | `spectral_collection.py:7` | ✅ Done `7bb1f2d`. |
| C8 | Devcontainer bind-mount hardcodes a **developer-specific path**. | `devcontainer.json:31` | ✅ Done (documented) `7bb1f2d`, then simplified by `17c82ac` — `data/` is now purely the mount, its docs moved to `docs/data.md`, and the "mount hides `data/sample/`" warning was removed (nothing is committed under `data/` any more). Path left hardcoded by decision; README, `docs/data.md` and a comment on the `mounts` line explain it. |

---

## Plan

Ordered by what unblocks the handoff. Each phase is one commit; phases are
independent, so you can approve any subset.

### Phase 1 — Make the promises true (A1, A2, A3) — DONE (by decision)

> **Status: ✅ Done.** The client decided on **2026-07-30 not to ship any
> artifacts** — no model bundle, no sample data, no executed HTML exports. Phase 1
> is closed on the documentation path: rather than adding the files, the docs are
> made honest that they are not distributed with the repo. The run-from-clone
> experience is intentionally out of scope; a user obtains data and trains a model
> first.

**Decision (2026-07-30): the documentation path, not the artifacts.** Two ways to
close Phase 1 were on the table — ship the artifacts, or correct the docs so they
no longer imply the artifacts are present. The client chose the second.

**What shipped (docs made honest):**

- `models/example_model_v1/README.md` — no longer instructs "commit these four";
  it states the bundle is produced by running notebook 01 and is not committed, so
  a fresh clone must train first.
- `README.md` — the "The model bundle" section notes the four files are produced
  by training, not distributed with the repo; the layout line for `examples/`
  states no runnable example ships.
- `examples/README.md` — resolved from "open decision" to a plain statement that
  no example ships and the notebooks run against your own data (`docs/data.md`).
- `config.yaml` — a comment flags `paths.image`'s `data/sample/...` value as an
  illustrative default to be edited to point at your own cube.
- Earlier doc corrections that already landed remain in force: `67f05a6` dropped
  the README's "executed HTML exports" and "two notebooks" (there are three)
  claims; `b69cf35` softened the model-bundle framing; `17c82ac` moved the data
  docs to `docs/data.md` / `examples/README.md`.

**Left as an unfilled slot, by design:** `docs/data.md`'s "Getting the full
dataset" still carries a `TODO (data owner)` for the download link/DOI — that is
the data owner's to fill, not an artifact this repo ships.

**Note for any future retrain:** Phase 4b altered the split, so any bundle
produced now will differ from one produced before the audit. That is the intended
order — 4b landed first, exactly so a later retrain would not have to be redone.

### Phase 2 — Fix the normalization asymmetry (B1) — DONE (`c8e8e69`)

> **Status: ✅ Done on `main`.** `src/upwins_veg/preprocessing.py` ships
> `PILOTED_SOURCE_PATTERNS`, `is_piloted_source`, and `pixel_wise_normalize`; both
> notebook 01 cell 26 and `batch_predict.py` call them.

**Resolved with the client (2026-07-27):** `"crisfield"` and `"piloted"` name the
same thing — data captured from a piloted platform. All crisfield data in the
test set was piloted data. Piloted data should be pixel-wise normalized at both
training and prediction; everything else should not. So the current behavior was
correct in intent, and training's shorter list was correct only by accident of
naming. This was a latent bug, not an active one: the first piloted ROI from a
non-crisfield site would be normalized at prediction but not at training.

The fix made the two sides structurally unable to diverge, rather than changing
behavior.

**What shipped.** `src/upwins_veg/preprocessing.py`:

```python
PILOTED_SOURCE_PATTERNS = ("crisfield", "piloted")

def is_piloted_source(filename): ...
def pixel_wise_normalize(spectra): ...
```

Notebook 01 cell 26 imports both at the top of the cell and calls them in place
of its own min-max block; `batch_predict.py` imports them with a relative import
(`from .preprocessing import ...`) and does the same. Nothing else changed:
`config.yaml` and the bundle format are untouched.

**Verified:** `pixel_wise_normalize` reproduces the two original blocks exactly
on a hand-checked array, including the flat-spectrum (`max == min`) case, and
does not mutate its input. `is_piloted_source` matches `CRISFIELD` (case), a
`piloted` filename, and rejects an unrelated one. `batch_predict` imports with
`spectral` stubbed and the function body references the helper.

**Risk carried forward:** behavior-preserving *if and only if* every piloted ROI
in the training set is also named `crisfield`. Check before reusing an existing
bundle:

```bash
find <roi_dir> -iname '*piloted*' -not -iname '*crisfield*'
```

Empty result means the existing bundle stays valid. Non-empty means those ROIs
were trained un-normalized and a retrain is required. **This check has not been
run — it needs the ROI directory.** (Moot if Phase 1 retrains anyway, which
Phase 4b already forces.)

Deliberately **not** in scope (see Future work): promoting the pattern list into
`config.yaml`, and recording it in the model bundle so prediction can verify it
against training.

**Longer term (not in this plan):** platform belongs in ROI metadata rather than
the filename — renames silently change preprocessing. That is a change in the
`upwins-hsi-preprocessing` repo.

### Phase 3 — Fail loudly (B2, B3) — DONE (`c082a5b`)

> **Status: ✅ Done on `main`.** `classify_and_save_image` raises; `batch_classify`
> reports each failure and an "N of M" count; the bare `except:` in
> `spectral_collection.py` is narrowed to `(KeyError, IndexError)` with a
> skipped-row report.

- `classify_and_save_image` no longer catches. Its `finally` block (which
  releases the memmap and forces a `gc.collect()`) is kept, so cleanup still runs
  on the way out; only the `except Exception` that turned a failure into a
  normal return is gone. Its docstring now states that it raises.
- `batch_classify` keeps the per-file `try` so one bad image doesn't abort a
  batch, and now prints the failing path with the exception *type* plus message,
  and ends with `"Batch processing complete: N of M images classified."`
  followed by an indented list of the failures when there are any.
- The bare `except:` in `spectral_collection.py` is now
  `except (KeyError, IndexError)` — a missing metadata column, or a spectrum with
  no matching csv row. Skipped rows are collected and reported after the loop
  (first 10 named, then a count). Anything else propagates.

**Verified:** `batch_classify` driven over two stub `.hdr` files with one raising
a band-mismatch `ValueError` prints the per-file error and
`"complete: 1 of 2 images classified"` plus the failing path.

**Risk:** low but real — runs that currently "succeed" quietly will start
reporting errors. That's the point, but it may surface pre-existing data issues.

### Phase 4 — Reproducible training (B4) — DONE (`d05fe19`)

> **Status: ✅ Done on `main`.** Deterministic seeding is in cell 2 and the split
> in cell 34 is stratified on `plant` with the min-3-per-class guard. **The
> seeding mechanism changed after the merge:** `1006e0e` replaced
> `tf.keras.utils.set_random_seed(42)` with three direct seed calls — see 4a.

**4a. Seeding.** *Originally* `tf.keras.utils.set_random_seed(42)` was added to
notebook 01's setup cell (cell 2), immediately before the `# --- Configuration ---`
block. **`1006e0e` then replaced it** with three explicit calls —
`random.seed(42)`, `np.random.seed(42)`, `tf.random.set_seed(42)` — because
`set_random_seed` installs a seed generator that made the first `Conv1D` build
raise `'float' object cannot be interpreted as an integer` on Python 3.12 +
tf_keras 2.17. The three direct calls seed Python, NumPy and TensorFlow with
determinism unchanged, and keep tf_keras on its integer initializer-seed branch.
A comment there, and a Provenance bullet in the model card, record that exact
reproducibility also requires the pinned versions in `requirements.txt`.

**4b. Stratified split on `plant`.** The body of cell 34 above
`X_train, X_val, X_test = ...` is now:

```python
# --- Data Splitting (Train/Validation/Test on features and ORIGINAL labels) ---
# Stratify on plant so every class keeps its proportion in train/val/test.
# Needs >= 3 samples per class (one per split); check first so the failure names
# the classes to fix instead of surfacing as a sklearn error mid-run.
MIN_PER_CLASS = 3
y_strat = y_all_dict_original['plant']

_vals, _counts = np.unique(y_strat, return_counts=True)
_rare = {int(v): int(n) for v, n in zip(_vals, _counts) if n < MIN_PER_CLASS}
if _rare:
    _named = {(str(y_plant_labels[v]) if v >= 0 else 'unlabeled (N)'): n
              for v, n in _rare.items()}
    raise ValueError(
        f"Cannot stratify on plant: {_named} have fewer than {MIN_PER_CLASS} "
        "spectra, so they cannot appear in all of train/val/test. Collect more "
        "samples for them, or remove them from the library/ROIs before training."
    )

# 70 / 15 / 15. The second split takes its share of what the first left, so the
# fraction is derived rather than hardcoded: 0.15 / 0.85 = 0.1765.
TEST_FRAC = 0.15
VAL_FRAC = 0.15

indices = np.arange(len(X_all))
train_indices, test_indices = train_test_split(
    indices, test_size=TEST_FRAC, random_state=42, stratify=y_strat)
train_indices, val_indices = train_test_split(
    train_indices, test_size=VAL_FRAC / (1 - TEST_FRAC), random_state=42,
    stratify=y_strat[train_indices])
```

One deviation from the drafted code: `str(y_plant_labels[v])` rather than
`y_plant_labels[v]`, so the error message reads `{'C': 2}` instead of
`{np.str_('C'): 2}`.

Everything below that in the cell is unchanged, including
`test_indices_library = test_indices[test_indices < len(sc.spectra)]` — no rows
are dropped, so that boundary stays valid. No cells were inserted, no samples
dropped, no classes filtered. Cell 33's markdown description was updated to
match.

This also replaced the bare `0.1765`, which read as a magic number and would
silently stop meaning 15% if anyone edited `test_size=0.15`.

Two details that were easy to get wrong, both handled:

- The **second** split uses `y_strat[train_indices]`, not `y_strat`. The first
  can use `y_strat` directly only because `indices` is `np.arange(len(X_all))`,
  making `y_strat[indices]` identical to `y_strat`.
- `-1` (the ignore value, from ROIs matching no plant code) is a valid stratum
  and needs no special handling; it is reported as `unlabeled (N)` if it is ever
  too small.

**Verified** by extracting the cell body and executing it against synthetic
labels with real `sklearn`: 2000 samples over 8 classes (including `-1`) split
1400/300/300 — exactly 70/15/15, indices disjoint, and every class holds its
proportion to within 0.001 across all three splits. The guard fires on a class
with two members and names it: `Cannot stratify on plant: {'unlabeled (N)': 2,
'C': 2} have fewer than 3 spectra, ...`.

**Where a sub-3 class could come from,** if the guard ever fires — neither is the
target species list:

1. `spectral_collection.py:106` appends `row['sub-category']` as the plant name
   whenever `genus == 'NA'`, so free-text sub-categories for non-target
   vegetation become plant classes outside `plant_codes`.
2. ROIs whose filename matches no `plant_codes` key fall through to `'N'` → `-1`.

**Risk realized:** the split has changed, so a retrain will not reproduce the
current bundle. This landed before Phase 1 generates artifacts, which is the
order the plan called for.

### Phase 4c — Document what the metrics measure (docs only) — DONE (`d05fe19`)

> **Status: ✅ Done on `main`.** `docs/model_card.md` carries the Metrics section
> (leakage block quote + the three-cell mapping table).

The client has decided against a group split (see Future work), so pixels from
one ROI appear in both train and test. Held-out accuracy therefore reads higher
than performance on a fresh image with no ROIs — which is the thing the client
actually cares about.

`docs/model_card.md` now has a Metrics section that says so explicitly, in a
block quote so it cannot be skimmed past, plus a table mapping each of the three
evaluation cells notebook 01 already runs to what its number means:

| Metric | What it means |
|--------|---------------|
| Overall test | Optimistic. Compare training runs with it; do not predict field performance from it. |
| **Library-only test** | Held-out ASD library spectra only, no ROI pixels, so no per-image leakage — the better partial proxy for generalization. |
| ROI-only test | Full leakage; diagnostic, not for reporting. |

Both the overall and library-only numbers are now requested as `_fill in_` slots
rather than one unlabelled figure. Limitations gained two bullets (leakage, and
the filename-driven normalization from Phase 2); Provenance gained the
reproducibility note from 4a.

`models/example_model_v1/model_card.md` received the identical edit at the time,
so the two copies stayed byte-identical and C4 was left exactly as it was. Phase 7
then replaced that copy with a stub, so `docs/model_card.md` is now the only one.

### Phase 5 — Packaging comment only (C1; C2 declined) — DONE (`f23c65c`)

> **Status: ✅ Done on `main` (C1) · ⛔ Deferred (C2).** Explanatory comments in
> `pyproject.toml` and `requirements.txt` shipped; no functional packaging change,
> and the `license` table form is deliberately kept.

**Decided 2026-07-27: no functional packaging changes.** `pip install -e .` is
the right mechanism and works as intended — it puts `upwins_veg` on the path so
notebooks and scripts can import it from anywhere. C1 was only ever about absent
dependency *metadata*, and the client has opted to leave `requirements.txt` as
the single source of truth.

What shipped is a comment in `pyproject.toml` recording that runtime
dependencies live in `requirements.txt` and are deliberately not duplicated, and
a matching four-line header in `requirements.txt` pointing back and stating the
install order (requirements first, then `pip install -e .`).

No `dependencies` key, no extras, no resolver behavior change. This also
sidesteps the NVIDIA TensorFlow question entirely (see Open questions), since pip
is never asked to resolve `tensorflow` or `numpy` at `postCreateCommand` time.

**C2 is declined in full (client, 2026-07-27).** `authors`, `urls` and
`classifiers` stay absent, and **`license = {text = "MIT"}` keeps the table
form**. The rationale is now a comment directly above the key in
`pyproject.toml`, ending "Do not 'modernize'", so it is not re-raised as an
oversight later: the PEP 639 string form `license = "MIT"` requires
**setuptools ≥ 77** (under older setuptools a bare string fails `[project]`
validation, because PEP 621 originally defined `license` as a table). That means
also bumping `[build-system] requires` from `>=61.0`, which only works because
pip's build isolation fetches a newer setuptools — needing network access at
install time and **breaking under `pip install --no-build-isolation`**. The audit
environment had setuptools **68.1.2** and the NGC base image likely ships
something similar.

Revisit only if setuptools actually removes support, and then bump `requires`
deliberately alongside it.

### Phase 6 — Smoke tests (C3) — OUT OF SCOPE

> **Status: ⛔ Declined.** Closed as out of scope by the client (2026-07-27,
> reaffirmed 2026-07-30); no test files in this repo, CI moot along with it.

**Declined by the client, 2026-07-27 and reaffirmed 2026-07-30: no test files in
this repo.** C3 is closed on that basis, not deferred. CI is moot along with it —
there would be nothing for a workflow to run. Confirmed against the tree: the repo
carries no test files and no `.github/workflows`.

Recorded so the reasoning survives: the three tests that were drafted were an
import check for `upwins_veg` and `hsiViewer` (the `src/` packaging bug that
produced `ModuleNotFoundError: hsiViewer` when unpickling ROIs), an `ROIs_class`
pickle round-trip through the shim at its original module path, and a
parse-every-notebook-cell check. Phase 2 would have added a fourth, pinning
`pixel_wise_normalize` on a known array — the one numeric behavior training and
prediction now share.

The parse-and-round-trip check and the pyflakes run under "How to verify work"
above cover the notebook and lint halves of that list without adding files to the
repo. Nothing covers the import and unpickle paths automatically; they have to be
exercised by actually running notebook 01, which is the same thing Phase 1 needs.

### Phase 7 — Docs and hygiene (C4–C8) — DONE (`7bb1f2d`)

> **Status: ✅ Done on `main`.** All of C4–C8 shipped in `7bb1f2d`; two items were
> refined afterward. `26f1f9c` corrected C6's comment wording (the CSVs were never
> committed). `17c82ac` reworked C8: it made `data/` purely the mount, moved
> `data/README.md` → `docs/data.md` and `data/sample/README.md` → `examples/README.md`,
> collapsed `.gitignore` to a plain `data/`, and **deleted** the "the mount hides
> `data/sample/`" warning — with nothing committed under `data/`, there is nothing
> for the mount to hide. Read the C6/C8 notes below with those follow-ups applied.

**C4 — model card deduplicated.** `models/example_model_v1/model_card.md` is now
a four-line stub linking to `docs/model_card.md`, which is the only copy. The two
were still byte-identical when this landed, so nothing had to be reconciled.

**C5 — model card filled in as far as the code allows.** Three new sections, all
read directly off notebook 01 and accurate for any bundle it produces:

- *Preprocessing* — the four steps in order (resample → piloted-only pixel-wise
  min-max → `StandardScaler` fit on train only → reshape for Conv1D).
- *Architecture* — the full layer table for `build_spectral_cnn`: three
  Conv1D/BatchNorm/MaxPool/Dropout blocks (32/k7, 64/k5, 128/k3), the shared
  Dense(128) head, and the five task heads.
- *Training configuration* — Adam at 1e-4, per-head sparse categorical
  cross-entropy with equal task weights, batch 32, up to 600 epochs with
  `EarlyStopping(patience=30, restore_best_weights=True)`, the seeds, and the
  masking rule **including the `lifecycle` exception** (there `'N'` is a real
  trained class, not an ignored label — easy to get wrong when reading the
  metrics).

*Training data* also gained the ROI subsampling rule (≥30 pixels per ROI group,
300 total) and the 70/15/15 stratified split.

What could not be filled is now a **"Still to fill in" checklist** split by who
can answer it: readable from the bundle once it exists (band count, class counts,
epochs run), printed by the training run (the two metric sets and their sample
counts), or known only to the data owner (dates, sites, per-class counts, author,
field failure modes). `data/README.md`'s missing dataset link became an explicit
`TODO (data owner)` block instead of an italicized aside.

**C6 — metric CSVs no longer land in `notebooks/`.** New config key
`paths.metrics_dir: data/metrics`, made absolute by the existing loop in cell 4.
Cell 59 creates it on demand, prints where it is writing, and joins both filenames
against it. `data/*` already ignores it; `classification_report_*.csv` was added
to `.gitignore` as a second net for copies written elsewhere, e.g. by an older
notebook run. Both nets were verified with `git check-ignore`.

**C7 — unused `import json` dropped** from `spectral_collection.py`. pyflakes is
now clean across `src/`, which makes it a usable signal.

**C8 — devcontainer path documented, not parameterized.** The README's Data
section now shows the mount, states plainly that the host path is hardcoded and
must be edited if yours differs, and explains why the failure is confusing
(Docker creates an empty directory for a missing source path). It also notes a
gotcha the original finding did not mention: **the mount replaces the repo's
`data/`, so the committed `data/sample/` is invisible inside the container**
unless the external directory has its own `sample/`. A comment on the `mounts`
line and a pointer from `data/README.md` lead back to it. Left hardcoded on
purpose — a sentence of documentation beats an environment-variable indirection
layer.

---

## What was verified, and what was not

Phases 2–5 and 7 were **not** run end to end — there is still no training data
and no GPU. What was actually checked:

| Check | Result |
|-------|--------|
| Every code cell in all three notebooks parses (`ast.parse`) | pass |
| All three notebooks round-trip byte-identically through `json.dump(..., indent=1, ensure_ascii=True) + '\n'` | pass |
| `pyflakes` over `src/upwins_veg/*.py` and `src/hsiViewer/*.py` | clean (was one item, C7, cleared in Phase 7) |
| `upwins_veg`, `roi_labels`, `preprocessing`, `batch_predict`, `hsiViewer` all import (with `spectral` stubbed) | pass |
| `pyproject.toml` parses under `tomllib`; `pip install -e .` succeeds | pass |
| `pixel_wise_normalize` matches the two original inline blocks, including the flat-spectrum case, and does not mutate its input | pass |
| `is_piloted_source` on `CRISFIELD`, `piloted`, and an unrelated name | pass |
| `batch_classify` over two stub `.hdr` files, one failing | prints the failure and "1 of 2 images classified" |
| Phase 4b split cell executed against synthetic labels with real sklearn | exactly 70/15/15, disjoint, proportions held to 0.001 across all 8 classes |
| Phase 4b guard on a 2-member class | raises, naming `'C'` and `'unlabeled (N)'` |
| `config.yaml` parses; `paths.metrics_dir` reads back as `data/metrics` | pass |
| `git check-ignore` on a CSV in `data/metrics/` and one in `notebooks/` | both ignored, by `data/*` and `classification_report_*.csv` respectively |
| No stale references to `models/example_model_v1/model_card.md` anywhere in the repo | pass — only `models/example_model_v1/README.md`, which points at `docs/` |

Not verified, and not verifiable here:

- Anything requiring real spectra, a real ROI pickle, or TensorFlow — including
  that notebook 01 still runs start to finish, and that cell 59 actually writes
  its CSVs to `data/metrics`.
- `import upwins_veg.batch_predict` against a real `spectral` install.
- The `find <roi_dir> -iname '*piloted*' -not -iname '*crisfield*'` check that
  decides whether the existing bundle survives Phase 2.
- That the devcontainer still builds and mounts as documented (no Docker here).

---

## What I need from you

**Nothing — every open question is now resolved.** For the record:

1. ~~**Phase 2:** the correct normalization behavior for "piloted" imagery.~~
   **Answered 2026-07-27** — see Phase 2. Implemented.
2. ~~**Phase 1:** artifacts, or approval to rewrite the docs instead.~~
   **Answered 2026-07-30** — do **not** ship artifacts; the docs are made honest
   about their absence instead. Phase 1 closed on the documentation path.
3. ~~**Phase 4b:** whether to stratify, and whether to move to a group split.~~
   **Answered 2026-07-27** — stratify on `plant`; raise on a class with fewer
   than 3 spectra; no group split for now. Implemented.
4. ~~Which phases to run.~~ **Answered** — 2 through 5, then 7. Both done and
   pushed to `claude/plan-phases-2-5-71wsyr`.
5. ~~Phase 6.~~ **Answered 2026-07-27, reaffirmed 2026-07-30** — out of scope, no
   test files in this repo.
6. ~~Whether to merge `claude/plan-phases-2-5-71wsyr`.~~ **Resolved** — those
   phases are now merged to `main` (`c8e8e69`..`7bb1f2d`), with follow-up
   refinements on top (`main` at `ee8b474`).

## Open questions (unresolved; not blocking any phase)

- **Does `requirements.txt` clobber NVIDIA's TensorFlow?** The devcontainer
  builds on `nvcr.io/nvidia/tensorflow:24.12-tf2-py3`, which ships NVIDIA's own
  TF build. If NGC versions it with a local suffix (e.g. `2.17.0+nv24.12`), then
  under PEP 440 the pin `tensorflow==2.17.0` is *not* satisfied by it, and pip
  downloads the stock PyPI wheel over the optimized one at image-build time. If
  it reports plain `2.17.0`, pip leaves it alone and all is well. Unverifiable
  without Docker.

  **To settle it,** inside a running container:

  ```bash
  pip list 2>/dev/null | grep -i tensorflow    # does the version carry an +nv suffix?
  python -c "import tensorflow as tf; print(tf.__version__)"
  ```

  Same question applies to `numpy==1.26.4`, which NGC also patches. The answer
  determines whether the TF/numpy pins should be dropped from `requirements.txt`
  and left to the image. It does not affect Phase 5 as implemented, which
  declares no dependencies at all and so never asks pip to resolve them.

## Future work (deliberately deferred, not oversights)

- **Group split on ROI.** Pixels within an ROI are spatially autocorrelated, so
  pixel-level splitting leaks between train and test and inflates reported
  accuracy. A group split (`GroupShuffleSplit` / `StratifiedGroupKFold` on
  `roi_name`, which already exists) would fix it. **Deferred at the client's
  request (2026-07-27):** it removes whole ROIs from training, and maximising ROI
  coverage matters more right now. Revisit when the ROI set is larger. Until
  then, the Phase 4c model-card section documents what the current metric does
  and does not measure.
- **Platform as metadata, not filename.** Pixel-wise normalization keys off
  substrings in filenames; it belongs in ROI/image metadata emitted by
  `upwins-hsi-preprocessing`. The Phase 2 helper narrows this to a single
  function (`is_piloted_source`), so switching to a metadata lookup later is a
  one-function change on this side.
- **Normalization patterns in `config.yaml`.** Phase 2 keeps
  `PILOTED_SOURCE_PATTERNS` as a module constant — one source of truth, which is
  what fixes the bug. Promoting it to config is worthwhile once the list changes
  often enough to justify the indirection.
- **Record preprocessing settings in the model bundle.** Prediction could verify
  the normalization patterns against what training used and fail on mismatch, the
  same way the band check works. Deferred: it changes the bundle format to guard
  a case that has not occurred.
- **Tighten the per-row `try` in `SpectralCollection`.** Phase 3 narrowed the
  exception types but left the block spanning the whole append sequence, so a
  mid-block failure could desynchronize the parallel metadata lists. Fixing it
  properly means building one dict per row and appending atomically — a small
  refactor of code the audit otherwise leaves alone.

## Out of scope unless you ask

Refactoring `spectral_collection.py` (it works and is well past the audit's
remit), restructuring the notebooks, or touching the trained model's
architecture and hyperparameters.

Added 2026-07-27 at the client's direction: **test files and CI** (C3 / Phase 6).
The repo is not to carry a test suite.
