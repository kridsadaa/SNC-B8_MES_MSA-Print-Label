import os
import re
import shutil
import uuid
from datetime import datetime
from io import BytesIO

import requests

from app.utils import extract_number, find_part_code, resize_image


def convert_zpl_to_image(zpl_code, width=4, height=6, dpmm=8, save_folder='temp'):    
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
 
    file_name = f"{uuid.uuid4().hex}.png"  
    file_path = os.path.join(save_folder, file_name)
 
    url = f"http://api.labelary.com/v1/printers/{dpmm}dpmm/labels/{width}x{height}/0/"
    files = {"file": zpl_code}
    
    response = requests.post(url, headers={"Accept": "image/png"}, files=files, stream=True)

    if response.status_code == 200:
        response.raw.decode_content = True
        with open(file_path, "wb") as out_file:
            shutil.copyfileobj(response.raw, out_file)
        print(f"✅ บันทึกภาพสำเร็จ: {file_path}")
        return file_path
    else:
        print(f"❌ เกิดข้อผิดพลาด: {response.status_code} - {response.text}")
        return None

def convert_image_to_zpl(image_url, width=100, height=100, save_folder='temp'):
    resized_image = resize_image(image_url, width, height)

    img_byte_arr = BytesIO()
    resized_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    response = requests.post('http://api.labelary.com/v1/graphics', files={'file': img_byte_arr}, headers={'Accept': 'application/zpl'})

    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
        
    file_name = f"{uuid.uuid4().hex}.zpl"
    file_path = os.path.join(save_folder, file_name)
    
    if response.status_code == 200:
        with open(file_path, 'w') as output_file:
            output_file.write(response.text)
        print(f"แปลงภาพเสร็จสิ้นและบันทึกเป็น ZPL ใน '{file_path}'")
        return file_path
    else:
        print(f"เกิดข้อผิดพลาด: {response.status_code} - {response.text}")
        return None
    
def modify_zpl_coordinates(file_path, x, y):
    try:
        zpl_data = read_zpl_file(file_path)
        
        print(f"Reading ZPL file: {file_path}")
        zpl_data = re.sub(r'^\^XA', '', zpl_data, flags=re.MULTILINE)
        zpl_data = re.sub(r'\^XZ$', '', zpl_data, flags=re.MULTILINE)

        zpl_data = re.sub(r'\^FO0,0', f'^FO{x},{y}', zpl_data)

        return zpl_data

    except Exception as e:
        print(f"Error occurred: {e}")
        return ''
    
def read_zpl_file(file_path):
    try:
        with open(file_path, 'r') as file: 
            return file.read()
    except Exception as e:
        print(f"An error occurred while reading the ZPL file: {e}")
        return ""
