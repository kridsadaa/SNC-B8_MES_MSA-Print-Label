import mimetypes
import os
from urllib.parse import urlsplit

import requests
from PIL import Image


def download_image_url(image_url, save_folder='temp'):
    img_data = requests.get(image_url).content
    
    path = urlsplit(image_url).path
    file_extension = mimetypes.guess_type(path)[0]
    
    if file_extension is None:
        file_extension = '.png'
    elif not file_extension.startswith('.'):
        file_extension = '.' + file_extension.split('/')[1]
    
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    image_name = 'image_name' + file_extension
    image_path = os.path.join(save_folder, image_name)
    
    with open(image_path, 'wb') as handler:
        handler.write(img_data)
    
    print(f'Image saved at: {image_path}')
    return image_path

def resize_image(image_path, max_width, max_height):
    with Image.open(image_path) as img:
        img.thumbnail((max_width, max_height))
        return img