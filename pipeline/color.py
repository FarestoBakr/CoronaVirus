"""Color and tone adjustment utilities."""

from typing import Literal

import numpy as np

try:
    import cv2
except Exception:  # pragma: no cover
    cv2 = None  # type: ignore


def adjust_contrast_brightness(image, contrast: Literal['none', 'auto'] = 'none', brightness: float = 0):
    """Adjust image contrast and brightness."""
    if cv2 is None:  # pragma: no cover
        raise ImportError("OpenCV is required for color adjustments")
    img = image.copy()
    if contrast == 'auto':
        img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
    if brightness != 0:
        img = cv2.convertScaleAbs(img, alpha=1.0, beta=brightness)
    return img


def white_balance(image):
    """Simple gray-world white balance."""
    if cv2 is None:  # pragma: no cover
        raise ImportError("OpenCV is required for white balance")
    result = image.astype(np.float32)
    avg_b, avg_g, avg_r = np.mean(result, axis=(0, 1))
    k = (avg_b + avg_g + avg_r) / 3
    result[:, :, 0] *= k / avg_b
    result[:, :, 1] *= k / avg_g
    result[:, :, 2] *= k / avg_r
    return np.clip(result, 0, 255).astype(np.uint8)


def apply_clahe(image):
    """Apply CLAHE to the luminance channel."""
    if cv2 is None:  # pragma: no cover
        raise ImportError("OpenCV is required for CLAHE")
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    merged = cv2.merge((cl, a, b))
    return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)


def enhance_faces(image):
    """Slightly smooth detected faces using a bilateral filter."""
    if cv2 is None:  # pragma: no cover
        raise ImportError("OpenCV is required for face enhancement")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = cascade.detectMultiScale(gray, 1.1, 4)
    out = image.copy()
    for (x, y, w, h) in faces:
        face = out[y:y + h, x:x + w]
        face = cv2.bilateralFilter(face, 0, 20, 10)
        out[y:y + h, x:x + w] = face
    return out
