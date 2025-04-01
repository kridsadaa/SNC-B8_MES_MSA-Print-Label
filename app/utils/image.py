import mimetypes
import os
import uuid
from urllib.parse import urlsplit

import requests
from PIL import Image


def download_image_url(image_url, save_folder='temp'):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    img_data = requests.get(image_url, headers=headers).content
    
    path = urlsplit(image_url).path
    file_extension = mimetypes.guess_type(path)[0]
    
    
    if file_extension is None:
        file_extension = '.png'
    elif not file_extension.startswith('.'):
        file_extension = '.' + file_extension.split('/')[1]
    
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    image_name = f"{uuid.uuid4().hex}{file_extension}"  
    image_path = os.path.join(save_folder, image_name)
    
    with open(image_path, 'wb') as handler:
        handler.write(img_data)
    
    print(f'Image saved at: {image_path}')
    return image_path

def resize_image(image_path, max_width, max_height):
    with Image.open(image_path) as img:
        img.thumbnail((max_width, max_height))
        return img