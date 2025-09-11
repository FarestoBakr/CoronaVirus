"""Super-resolution utilities."""

import os

try:
    import cv2
except Exception:  # pragma: no cover
    cv2 = None  # type: ignore


def super_resolve(image, scale: int = 2):
    """Upscale ``image`` by ``scale`` using the best available method."""
    # Try Real-ESRGAN
    try:  # pragma: no cover - optional dependency
        from realesrgan import RealESRGANer
        import torch
        model_path = os.path.join('models', 'RealESRGAN_x4plus.pth')
        if os.path.exists(model_path):
            half = torch.cuda.is_available()
            upsampler = RealESRGANer(
                scale=scale,
                model_path=model_path,
                model=None,
                tile=0,
                tile_pad=10,
                pre_pad=0,
                half=half,
            )
            output, _ = upsampler.enhance(image, outscale=scale)
            return output
    except Exception:
        pass

    # Try OpenCV DNN SuperRes
    if cv2 is not None:
        try:
            sr = cv2.dnn_superres.DnnSuperResImpl_create()
            model_path = os.path.join('models', f'EDSR_x{scale}.pb')
            if os.path.exists(model_path):
                sr.readModel(model_path)
                sr.setModel('edsr', scale)
                return sr.upsample(image)
        except Exception:
            pass

    if cv2 is None:  # pragma: no cover
        raise ImportError("OpenCV is required for super resolution")

    # Fallback to simple resize
    return cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
