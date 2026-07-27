"""Compatibility package for loading ROI pickle files.

Training ROIs for this classifier are produced by the interactive hsiViewer in
the companion ``upwins-hsi-preprocessing`` repo, and are pickled instances of
``hsiViewer.hsi_viewer_ROI.ROIs_class``. This package provides a minimal,
dependency-free stand-in for that class so the ROI files can be unpickled here
for training, without pulling in the PyQt5 GUI stack.
"""
