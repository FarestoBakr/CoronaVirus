"""Denoising and artifact removal utilities."""

from typing import Literal

try:
    import cv2
except Exception:  # pragma: no cover
    cv2 = None  # type: ignore


def denoise_image(image, level: Literal['low', 'medium', 'high'] = 'medium'):
    """Apply color denoising to ``image``.

    Parameters
    ----------
    image: ndarray
        Input image in BGR format.
    level: {'low', 'medium', 'high'}
        Strength of the denoising filter.
    """
    if cv2 is None:  # pragma: no cover
        raise ImportError("OpenCV is required for denoising")
    h_values = {'low': 5, 'medium': 10, 'high': 15}
    h = h_values.get(level, 10)
    return cv2.fastNlMeansDenoisingColored(image, None, h, h, 7, 21)


def remove_jpeg_artifacts(image):
    """Reduce JPEG compression artifacts using a median filter."""
    if cv2 is None:  # pragma: no cover
        raise ImportError("OpenCV is required for artifact removal")
    return cv2.medianBlur(image, 3)
