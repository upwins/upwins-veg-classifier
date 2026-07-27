# Example data

Placeholder — **nothing ships here yet.** Whether a small runnable example is
committed to this repo is still an open decision.

If one is added, drop it here so the notebooks run from a fresh clone:

- A spatially cropped ENVI reflectance cube (e.g. 200x200) named
  `raw_0_ref` + `raw_0_ref.hdr`.
- A few labeled ROI `.pkl` files.

Then point `paths.image`, `paths.image_hdr` and `prediction.input_hdr` (and
`paths.roi_dir`, if the ROIs go here too) at `examples/...` in `config.yaml`.

Keep the whole committed example well under ~50 MB so cloning stays fast. Use
your full data for the recorded tutorial by editing `config.yaml`.

## Why this is not under `data/`

The devcontainer bind-mounts an external directory onto `data/`, which replaces
the whole directory inside the container — anything committed under `data/` is
invisible there. `examples/` sits outside the mount, so a committed example
works both in a plain clone and in the container. See `docs/data.md`.
