"""Basic deblurring utilities."""

import numpy as np

try:
    import cv2
except Exception:  # pragma: no cover
    cv2 = None  # type: ignore


def deblur_image(image):
    """Attempt to remove mild blur using a sharpening kernel."""
    if cv2 is None:  # pragma: no cover
        raise ImportError("OpenCV is required for deblurring")
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    return cv2.filter2D(image, -1, kernel)
