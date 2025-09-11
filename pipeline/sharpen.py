"""Sharpening utilities."""

from typing import Literal

try:
    import cv2
except Exception:  # pragma: no cover
    cv2 = None  # type: ignore


def sharpen_image(image, intensity: Literal['mild', 'strong'] = 'mild'):
    """Sharpen ``image`` using an unsharp mask."""
    if cv2 is None:  # pragma: no cover
        raise ImportError("OpenCV is required for sharpening")
    sigma = 1.0 if intensity == 'mild' else 2.0
    blurred = cv2.GaussianBlur(image, (0, 0), sigma)
    amount = 1.0 if intensity == 'mild' else 1.5
    return cv2.addWeighted(image, 1 + amount, blurred, -amount, 0)
