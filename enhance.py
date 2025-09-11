"""Command line interface for image enhancement."""

import argparse
import glob
import logging
import os
from typing import List

import numpy as np

from pipeline import load, denoise, deblur, sharpen, color, superres, save

try:
    import cv2
except Exception:  # pragma: no cover
    cv2 = None  # type: ignore

try:  # optional metric
    from skimage.metrics import structural_similarity
except Exception:  # pragma: no cover
    structural_similarity = None  # type: ignore


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Enhance images with common techniques.")
    parser.add_argument('--input', required=True, help='Input image file or directory')
    parser.add_argument('--output', required=True, help='Output directory')
    parser.add_argument('--scale', type=int, default=1, choices=[1, 2, 4], help='Upscaling factor')
    parser.add_argument('--denoise', choices=['none', 'low', 'medium', 'high'], default='none')
    parser.add_argument('--deblur', action='store_true', help='Apply deblurring')
    parser.add_argument('--sharpen', choices=['none', 'mild', 'strong'], default='none')
    parser.add_argument('--contrast', choices=['none', 'auto'], default='none')
    parser.add_argument('--brightness', type=float, default=0.0, help='Brightness adjustment')
    parser.add_argument('--remove-jpeg-artifacts', action='store_true', dest='jpeg_artifacts')
    parser.add_argument('--white-balance', action='store_true')
    parser.add_argument('--clahe', action='store_true')
    parser.add_argument('--face-enhance', action='store_true')
    parser.add_argument('--reference', help='Reference image for PSNR/SSIM (optional)')
    parser.add_argument('--batch', action='store_true', help='Process all images in a folder')
    return parser.parse_args()


def collect_images(path: str, batch: bool) -> List[str]:
    if os.path.isdir(path) or batch:
        patterns = ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.tif', '*.ppm']
        files: List[str] = []
        for p in patterns:
            files.extend(glob.glob(os.path.join(path, p)))
        return files
    else:
        return [path]


def process_image(image_path: str, args: argparse.Namespace) -> None:
    logging.info("Processing %s", image_path)
    img, exif = load.load_image(image_path)
    original = img.copy()

    if args.jpeg_artifacts:
        img = denoise.remove_jpeg_artifacts(img)
    if args.denoise != 'none':
        img = denoise.denoise_image(img, args.denoise)
    if args.deblur:
        img = deblur.deblur_image(img)
    if args.sharpen != 'none':
        img = sharpen.sharpen_image(img, args.sharpen)
    if args.white_balance:
        img = color.white_balance(img)
    if args.clahe:
        img = color.apply_clahe(img)
    if args.contrast != 'none' or args.brightness != 0:
        img = color.adjust_contrast_brightness(img, args.contrast, args.brightness)
    if args.face_enhance:
        img = color.enhance_faces(img)
    if args.scale > 1:
        img = superres.super_resolve(img, scale=args.scale)

    save.save_images(original, img, args.output, image_path, exif)

    if args.reference and cv2 is not None and structural_similarity is not None:
        ref, _ = load.load_image(args.reference)
        ref = cv2.resize(ref, (img.shape[1], img.shape[0]))
        psnr = cv2.PSNR(ref, img)
        ssim = structural_similarity(cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY),
                                     cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
        logging.info("PSNR: %.2f SSIM: %.4f", psnr, ssim)


def main():
    args = parse_args()
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    images = collect_images(args.input, args.batch)
    if not images:
        raise FileNotFoundError('No images found to process')
    for img_path in images:
        process_image(img_path, args)


if __name__ == '__main__':
    main()
