"""Minimal Tkinter GUI for quick manual enhancement."""

import tkinter as tk
from tkinter import filedialog, messagebox

from pipeline import load, denoise, deblur, sharpen, color, superres, save

try:
    import cv2
except Exception:  # pragma: no cover
    cv2 = None  # type: ignore


def enhance_file(path: str):
    img, exif = load.load_image(path)
    img = denoise.denoise_image(img, 'low')
    img = sharpen.sharpen_image(img, 'mild')
    img = superres.super_resolve(img, scale=2)
    out_dir = filedialog.askdirectory(title='Select output directory')
    if out_dir:
        save.save_images(img, img, out_dir, path, exif)
        messagebox.showinfo('Done', f'Enhanced image saved to {out_dir}')


def select_file():
    file = filedialog.askopenfilename(title='Select image')
    if file:
        enhance_file(file)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Image Enhancer')
    btn = tk.Button(root, text='Open Image', command=select_file)
    btn.pack(padx=20, pady=20)
    root.mainloop()
