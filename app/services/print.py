import os
from datetime import datetime

import requests
from dotenv import load_dotenv

from app.helpers import generate_zpl_labels, validatePostPrintLabel
from app.types import TREQ_PostPrintLabel
from app.utils import (convert_image_to_zpl, download_image_url, image,
                       jsonifyError, jsonifySuccess, print_image, validate)

load_dotenv()
DEFAULT_PRINTER = os.getenv("DEFAULT_PRINTER", "mahingsa_printer")  

def print_hello_world():
    try:
        return jsonifySuccess("Hello World!")
    except Exception as e:
        return jsonifyError(str(e))


def print_label(req: TREQ_PostPrintLabel):
    try:
        if not req:
            return jsonifyError("No request body received", [] ,400)
        
        zpl_part = ""
        label_images = []
        
        missing_keys = validatePostPrintLabel(req)
        if  len(missing_keys) > 0:
            return jsonifyError("Missing required fields", missing_keys, 400)
        
        response = requests.get(req['image_url'])
        
        if response.status_code == 200:
            folder_date = datetime.now().strftime("%Y-%m-%d")
            save_folder_image_path = os.path.join("temp", folder_date, "images", "parts")
            save_folder_zpl_part = os.path.join("temp", folder_date, "zpls", "parts")
            
            image_path = download_image_url(req['image_url'], save_folder_image_path)
            zpl_part = convert_image_to_zpl(image_path, 96, 96, save_folder_zpl_part)

        label_images = generate_zpl_labels({**req, "zpl_part": zpl_part})
        if not label_images:
            return jsonifyError("Failed to generate ZPL labels", [], 400)
        
        if  len(label_images) > 0:
            for image in label_images:
                print_image(image, DEFAULT_PRINTER)
 
        return jsonifySuccess(f"Print label {req.get("code", "?")} successfully", [req])
    except Exception as e:
        return jsonifyError(str(e))