"""Support code for the UPWINS vegetation classifier notebooks.

Installed onto the import path by `pip install -e .`, so the notebooks in
`notebooks/` can import it without any `sys.path` mutation or `os.chdir`.

Modules:

- `spectral_collection` -- the labeled spectral library and its label columns.
- `roi_labels`          -- the ROI-filename finder and the label taxonomy
                           (species, age, part, health, lifecycle codes).
- `preprocessing`       -- pixel-wise normalization, shared by training and
                           prediction so the two cannot diverge.
- `batch_predict`       -- chunked classification of a reflectance cube to ENVI
                           classification maps.
- `tf_quiet`            -- stderr redirection around TensorFlow's CUDA/XLA
                           chatter; see the module for what each message means.
"""
