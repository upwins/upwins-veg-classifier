"""Dependency-free stand-in for the hsiViewer ROI class.

Labeled training ROIs are drawn with the interactive hsiViewer tool in the
``upwins-hsi-preprocessing`` repo and saved as pickled ``ROIs_class`` instances
whose module path is ``hsiViewer.hsi_viewer_ROI``. To *load* those pickles for
training we only need the class to exist at that import path — not the GUI.

This module intentionally imports nothing heavy (no PyQt5 / pyqtgraph), so the
classifier repo can read ROI files without the viewer's dependencies. If you
need the full interactive viewer (to *create* ROIs), use the
``upwins-hsi-preprocessing`` repo instead.
"""


class ROIs_class:
    """Container for a set of regions of interest.

    Attributes
    ----------
    names : list
        ROI names (from the first column of the ROI table).
    colors : dict
        ROI name -> display color, written by the viewer as a ``'#rrggbb'``
        string (``QColor.name()``), not an ``(r, g, b)`` triple.
    masks : dict
        ROI name -> boolean pixel mask, in the original image orientation even
        when the viewer that drew it was rotated.
    df : pandas.DataFrame
        Pixel locations, names, colors, and spectra for the ROIs. The training
        notebook reads spectra/labels from this DataFrame, and is the only
        attribute it uses -- ``colors`` and ``masks`` are carried for
        round-tripping back into the viewer.
    """

    def __init__(self, names=None, colors=None, masks=None, df=None):
        self.names = names
        self.colors = colors
        self.masks = masks
        self.df = df
