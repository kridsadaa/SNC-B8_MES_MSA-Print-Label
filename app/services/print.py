# app/services/print.py
import os
from datetime import datetime
from urllib.parse import urlparse

import requests

from app.constants.printer import PRINTER_PORT_LIST
from app.helpers import generate_zpl_labels, validatePostPrintLabel
from app.types import TREQ_PostPrintLabel
from app.utils import (convert_image_to_zpl, download_image_url, image,
                       jsonifyError, jsonifySuccess, print_images, validate)


def print_hello_world():
    try:
        return jsonifySuccess("Hello World!")
    except Exception as e:
        return jsonifyError(str(e))


def print_label(req: TREQ_PostPrintLabel, printer_port: int = 0):
    try:
        if not req:
            return jsonifyError("No request body received", [] ,400)
        if (req['part_code'][:2] == '2P' and req['part_name'] == 'Insulator B'):
            return jsonifySuccess(f"Print label {req['code']} successfully", [req])
        
        zpl_part = ""
        label_images = []
        
        missing_keys = validatePostPrintLabel(req)
        if  len(missing_keys) > 0:
            return jsonifyError("Missing required fields", missing_keys, 400)
        
        if not os.path.exists(req['image_url']):
            print(f"Error: {req['image_url']} does not exist")
    
        image_url = req.get('image_url', '')
        
        if image_url:
            parsed_url = urlparse(image_url)
            if not parsed_url.scheme:
                print(f"Error: {image_url} does not have a valid URL scheme (e.g., http:// or https://)")
                return jsonifyError(f"Invalid URL: {image_url}", [], 400)
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(req['image_url'], headers=headers)
            if response.status_code == 200:
                folder_date = datetime.now().strftime("%Y-%m-%d")
                save_folder_image_path = os.path.join("temp", folder_date, "images", "parts")
                save_folder_zpl_part = os.path.join("temp", folder_date, "zpls", "parts")
                
                image_path = download_image_url(req['image_url'], save_folder_image_path)
                zpl_part = convert_image_to_zpl(image_path, 190, 110, save_folder_zpl_part)

        label_images = generate_zpl_labels({**req, "zpl_part": zpl_part})
        if not label_images:
            return jsonifyError("Failed to generate ZPL labels", [], 400)
        
        if  len(label_images) > 0:
            print_images(label_images, PRINTER_PORT_LIST[printer_port])
 
        return jsonifySuccess(f"Print label {req['code']} successfully", [req])
    except Exception as e:
        return jsonifyError(str(e))
    

def print_image_from_url(req: dict, printer_port: int = 0):
    """
    ปริ้นรูปภาพจาก URL - ทำงานคล้าย print_label หลังจากโหลดรูปมาแล้ว
    """
    try:
        if not req:
            return jsonifyError("No request body received", [], 400)
       
        # Extract parameters
        image_url = req.get('image_url', '')
        width = req.get('width', 190)
        height = req.get('height', 110)
        copies = req.get('copies', 1)
       
        if not image_url:
            return jsonifyError("Image URL is required", [], 400)
       
        print(f"🖼️ Print image from URL: {image_url}")
        print(f"📐 Size: {width}x{height}, Copies: {copies}")
       
        # Validate URL
        parsed_url = urlparse(image_url)
        if not parsed_url.scheme:
            return jsonifyError(f"Invalid URL: {image_url}", [], 400)
       
        # Download image (same as print_label)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
       
        print(f"🌐 Downloading image...")
        response = requests.get(image_url, headers=headers, timeout=30)
       
        if response.status_code != 200:
            return jsonifyError(f"Failed to download image: HTTP {response.status_code}", [], 400)
       
        print(f"✅ Image downloaded: {len(response.content)} bytes")
       
        # ✅ ทำงานต่อคล้าย print_label
        image_path = None
       
        if response.status_code == 200:
            folder_date = datetime.now().strftime("%Y-%m-%d")
            save_folder_image_path = os.path.join("temp", folder_date, "images", "parts")
           
            # ใช้ download_image_url เหมือน print_label
            image_path = download_image_url(image_url, save_folder_image_path)
            print(f"💾 Image saved to: {image_path}")
       
        # ✅ เช็คว่ามี image_path และไฟล์มีอยู่จริง
        if not image_path or not os.path.exists(image_path):
            return jsonifyError("Failed to save image file", [], 400)
       
        # ✅ ปริ้นตามจำนวน copies โดยส่ง list ของ image paths
        print(f"🖨️ Sending to printer port {printer_port}...")
        
        # สร้าง list ของ image paths ตามจำนวน copies
        image_paths = [image_path] * copies
        
        # เรียก print_images ครั้งเดียวด้วย list ของ paths
        print_images(image_paths, PRINTER_PORT_LIST[printer_port])
        
        print(f"✅ Successfully sent {copies} copies to printer")
       
        return jsonifySuccess("Image printed successfully", [{
            "image_url": image_url,
            "printer_port": printer_port,
            "width": width,
            "height": height,
            "copies": copies,
            "image_path": image_path,
            "status": "printed"
        }])
       
    except requests.RequestException as e:
        print(f"❌ Network error: {str(e)}")
        return jsonifyError(f"Network error: {str(e)}", [], 400)
    except Exception as e:
        print(f"❌ Print error: {str(e)}")
        return jsonifyError(f"Print error: {str(e)}", [], 500)