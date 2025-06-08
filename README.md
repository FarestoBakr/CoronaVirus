# CoronaVirus

## facebook_uploader.py

This script demonstrates how to upload images from a local directory to a Facebook page using the Graph API. Captions are loaded from a text file (one caption per line).

1. Install the required package:
   ```bash
   pip install requests
   ```
2. Update the `IMAGE_DIR`, `CAPTION_FILE`, `PAGE_ID`, and `ACCESS_TOKEN` variables in the script.
3. Run the script with Python:
   ```bash
   python facebook_uploader.py
   ```

Make sure you have a valid Page access token with permissions to upload photos.
