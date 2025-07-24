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
    try:
        if not req:
            return jsonifyError("No request body received", [], 400)
        
        # Extract parameters from request
        image_url = req.get('image_url', '')
        width = req.get('width', 190)
        height = req.get('height', 110)
        copies = req.get('copies', 1)
        
        if not image_url:
            return jsonifyError("Image URL is required", [], 400)
        
        # Validate URL
        parsed_url = urlparse(image_url)
        if not parsed_url.scheme:
            return jsonifyError(f"Invalid URL: {image_url}", [], 400)
        
        # Download image with timeout
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(image_url, headers=headers, timeout=30)
        
        if response.status_code != 200:
            return jsonifyError(f"Failed to download image: HTTP {response.status_code}", [], 400)
        
        # Create folders
        folder_date = datetime.now().strftime("%Y-%m-%d")
        save_folder_image_path = os.path.join("temp", folder_date, "images", "direct")
        save_folder_zpl_path = os.path.join("temp", folder_date, "zpls", "direct")
        
        # Download and convert
        image_path = download_image_url(image_url, save_folder_image_path)
        zpl_content = convert_image_to_zpl(image_path, width, height, save_folder_zpl_path)
        
        if not zpl_content:
            return jsonifyError("Failed to convert image to ZPL", [], 400)
        
        # Print multiple copies
        for _ in range(copies):
            print_images([zpl_content], PRINTER_PORT_LIST[printer_port])
        
        return jsonifySuccess("Image printed successfully", [{
            "image_url": image_url,
            "printer_port": printer_port,
            "width": width,
            "height": height,
            "copies": copies
        }])
        
    except requests.RequestException as e:
        return jsonifyError(f"Network error: {str(e)}", [], 400)
    except Exception as e:
        return jsonifyError(f"Print error: {str(e)}", [], 500)