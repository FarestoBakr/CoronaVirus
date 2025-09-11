"""Saving utilities."""

import os
from typing import Optional, Tuple

import numpy as np

try:
    from PIL import Image
except Exception:  # pragma: no cover
    Image = None  # type: ignore

try:
    import cv2
except Exception:  # pragma: no cover
    cv2 = None  # type: ignore


def save_images(original: np.ndarray, enhanced: np.ndarray, out_dir: str,
                input_path: str, exif: Optional[bytes] = None) -> Tuple[str, str]:
    """Save enhanced image and side-by-side comparison."""
    if cv2 is None:  # pragma: no cover
        raise ImportError("OpenCV is required for saving images")

    os.makedirs(out_dir, exist_ok=True)
    base = os.path.splitext(os.path.basename(input_path))[0]
    compare_path = os.path.join(out_dir, f"{base}_compare.jpg")
    enhanced_path = os.path.join(out_dir, f"{base}_enhanced.png")

    comparison = np.hstack((original, enhanced))
    cv2.imwrite(compare_path, comparison)

    try:
        if Image is None:  # pragma: no cover
            raise ImportError
        img = Image.fromarray(cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB))
        img.save(enhanced_path, exif=exif)
    except Exception:
        cv2.imwrite(enhanced_path, enhanced)

    return enhanced_path, compare_path
