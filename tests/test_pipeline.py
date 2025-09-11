import os

import numpy as np

from pipeline import load, sharpen, save

try:
    import cv2
except Exception:  # pragma: no cover
    cv2 = None  # type: ignore


def test_load_and_sharpen(tmp_path):
    if cv2 is None:  # pragma: no cover
        import pytest
        pytest.skip("OpenCV not installed")
    img, exif = load.load_image('tests/data/color_blocks.ppm')
    out = sharpen.sharpen_image(img, 'mild')
    enhanced_path, compare_path = save.save_images(img, out, str(tmp_path), 'tests/data/color_blocks.ppm', exif)
    assert os.path.exists(enhanced_path)
    assert os.path.exists(compare_path)
    assert out.shape == img.shape
