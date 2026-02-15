import os
from PIL import Image

from AGI.utility import get_path, get_config


config = get_config.load()

SUPPORTED_EXTENSIONS = {
    # Images
    '.png', '.jpg', '.jpeg', '.webp', '.heic', '.heif',
    # Documents
    '.pdf', '.csv', '.html', '.md', '.py', '.js', '.txt',
    # Audio/Video
    '.mp3', '.wav', '.mp4', '.mov', '.avi'
}

def read_prompt():
    with open(get_path.absolute(config['paths']['prompt']), "r", encoding="utf-8") as f:
        content = f.read().strip()
    return content

def get_uploads(upload_dir, client):
    media_items = []

    for filename in os.listdir(upload_dir):
        file_path = os.path.join(upload_dir, filename)
        ext = os.path.splitext(filename)[1].lower()

        if not os.path.isfile(file_path) or filename.startswith('.') or ext not in SUPPORTED_EXTENSIONS:
            continue

        try:
            if ext in ['.png', '.jpg', '.jpeg', '.webp']:
                img = Image.open(file_path)
                media_items.append(img)
            else:
                uploaded_file = client.files.upload(path=file_path)
                media_items.append(uploaded_file)

        except Exception as e:
            print(f"Failed to process {filename}: {e}")

    return media_items