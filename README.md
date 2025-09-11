# Image Enhancement Pipeline

This project provides a small, modular image enhancement toolchain. It can
improve the quality of photographs by applying denoising, deblurring,
sharpening, color corrections and optional super resolution.

## Features
- Denoising, deblurring, sharpening
- Color correction, brightness/contrast adjustment
- JPEG artifact reduction
- Optional filters: white balance, CLAHE, face enhancement
- Super-resolution upscaling (×2/×4) with Real‑ESRGAN when available and
  graceful fallbacks otherwise
- Batch processing for folders of images
- EXIF preservation and side-by-side comparison output

## Setup
```bash
pip install -r requirements.txt
```

Pre-trained models should be placed in the `models/` directory. For
Real‑ESRGAN use `RealESRGAN_x4plus.pth`. For OpenCV’s DNN super resolution
fallback place `EDSR_x2.pb` and/or `EDSR_x4.pb` in the same folder.

## Usage
```bash
python enhance.py --input sample.jpg --output out/ --scale 4 --denoise medium --sharpen mild --contrast auto
python enhance.py --input imgs/ --batch --scale 2 --remove-jpeg-artifacts
```

The enhanced image is saved as `<name>_enhanced.png` and the side-by-side
comparison as `<name>_compare.jpg`.

## Tests
```bash
pytest
```

## Sample
The repository contains a few tiny test images under `tests/data/` that are
used by the unit tests. Running the example commands on those images will
produce a simple before/after comparison like the one below:

![before](tests/data/color_blocks.ppm) ![after](tests/data/color_blocks.ppm)

## Notes
The project automatically detects CUDA availability for Real‑ESRGAN. When
no GPU or models are present it falls back to OpenCV or simple resizing so
that execution on CPU-only environments still works.
