import os
import requests
from pathlib import Path


def load_captions(caption_file):
    """Load captions from a text file."""
    captions = []
    with open(caption_file, 'r', encoding='utf-8') as f:
        for line in f:
            caption = line.strip()
            if caption:
                captions.append(caption)
    return captions


def upload_images(directory, captions, page_id, access_token):
    """Upload images in directory to a Facebook page with captions."""
    session = requests.Session()
    images = sorted(Path(directory).glob('*.*'))
    for idx, image_path in enumerate(images):
        if idx < len(captions):
            caption = captions[idx]
        else:
            caption = ''
        files = {
            'source': open(image_path, 'rb')
        }
        data = {
            'caption': caption,
            'access_token': access_token
        }
        url = f'https://graph.facebook.com/{page_id}/photos'
        resp = session.post(url, files=files, data=data)
        if resp.ok:
            print(f'Uploaded {image_path.name}')
        else:
            print(f'Failed to upload {image_path.name}: {resp.text}')


if __name__ == '__main__':
    IMAGE_DIR = 'path/to/your/image_folder'
    CAPTION_FILE = 'captions.txt'
    PAGE_ID = 'your_page_id'
    ACCESS_TOKEN = 'your_page_access_token'

    captions = load_captions(CAPTION_FILE)
    upload_images(IMAGE_DIR, captions, PAGE_ID, ACCESS_TOKEN)
