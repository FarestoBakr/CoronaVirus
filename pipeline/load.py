"""Image loading utilities.

This module provides functions to load images while preserving EXIF metadata
when possible.
"""

from typing import Tuple, Optional

import numpy as np

try:
    from PIL import Image
except Exception:  # pragma: no cover - PIL may be missing
    Image = None  # type: ignore

try:
    import cv2
except Exception:  # pragma: no cover - OpenCV may be missing
    cv2 = None  # type: ignore


def load_image(path: str) -> Tuple[np.ndarray, Optional[bytes]]:
    """Load an image from ``path``.

    Parameters
    ----------
    path: str
        Path to the image file.

    Returns
    -------
    Tuple[np.ndarray, Optional[bytes]]
        The image as a NumPy array in BGR format and raw EXIF data if
        available.  When PIL or OpenCV are not installed, an ``ImportError``
        will be raised.
    """

    exif = None

    if Image is not None:
        try:
            with Image.open(path) as img:
                exif = img.info.get("exif")
                array = np.array(img.convert("RGB"))
            if cv2 is not None:
                array = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
            return array, exif
        except Exception:
            pass

    if cv2 is None:  # pragma: no cover
        raise ImportError("OpenCV is required to load images")

    array = cv2.imread(path)
    if array is None:
        raise FileNotFoundError(path)
    return array, exif
