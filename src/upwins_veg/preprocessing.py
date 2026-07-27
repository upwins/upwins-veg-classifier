"""Spectral preprocessing shared by training and prediction.

Training (notebook 01) and prediction (`batch_predict`) must preprocess a
spectrum identically, or the model sees inputs at inference that are scaled
differently from the ones it was trained on. Both sides import from here so the
two cannot drift apart.
"""

import numpy as np

# Data captured from a piloted platform is pixel-wise normalized; data from
# other sources is not. Historically every piloted collect came from the
# Crisfield site, so both names appear in filenames and both must match.
PILOTED_SOURCE_PATTERNS = ("crisfield", "piloted")


def is_piloted_source(filename):
    """True if `filename` names piloted-platform data, which must be normalized.

    Args:
        filename (str): An ROI pickle path or an image header path. Matching is
            case-insensitive and looks anywhere in the string.
    """
    lowered = filename.lower()
    return any(pattern in lowered for pattern in PILOTED_SOURCE_PATTERNS)


def pixel_wise_normalize(spectra):
    """Min-max normalize each spectrum independently onto [0, 1].

    Args:
        spectra (np.ndarray): Shape (num_samples, num_bands).

    Returns:
        np.ndarray: A new array of the same shape. Flat spectra (max == min)
        are divided by 1 rather than 0, leaving them at zero.
    """
    min_vals = np.min(spectra, axis=1, keepdims=True)
    max_vals = np.max(spectra, axis=1, keepdims=True)
    range_vals = max_vals - min_vals
    range_vals[range_vals == 0] = 1
    return (spectra - min_vals) / range_vals
