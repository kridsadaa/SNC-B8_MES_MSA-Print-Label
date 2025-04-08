import difflib
import os
import re
import shutil
import uuid
from datetime import datetime

import requests

from app.types import TREQ_PostPrintLabel
from app.utils import (convert_zpl_to_image, extract_number, find_part_code,
                       modify_zpl_coordinates, part)


def _increment_last_number(code: str) -> str:
    match = re.search(r'(\d+)(?!.*\d)', code)
    if not match:
        raise ValueError(f"ไม่พบตัวเลขในรหัส: {code}")

    number_str = match.group(1)
    number = int(number_str) - 1
    
    new_number = str(number).zfill(len(number_str))

    new_code = code[:match.start()] + new_number + code[match.end():]
    return new_code

def remove_last_digit(code: str) -> str:
    return re.sub(r'\d(?=\D*$)', '', code)

def increment_last_number(code: str) -> str:
    match = re.search(r'(\d+)(?!.*\d)', code)
    if not match:
        raise ValueError(f"ไม่พบตัวเลขในรหัส: {code}")

    number_str = match.group(1)
    number = int(number_str) + 1
    
    new_number = str(number).zfill(len(number_str))

    new_code = code[:match.start()] + new_number + code[match.end():]
    return new_code


def move_along_lenh(content, default, multiplier):
    move = default - (len(str(content)) * multiplier)
    return move

def move_according_to_conditions(content, conditions, default=0):
    move = next((size for length, size in sorted(conditions.items()) if (len(str(content))) < length), default)
    return move

def font_size(text, conditions, default="25,25"):
    font_size = next((size for length, size in sorted(conditions.items()) if len(text) < length), default)
    return font_size

def generate_zpl_labels(req: TREQ_PostPrintLabel):
    res = []
    zpl_part_image = ""
    zpl_content = ""
    folder_date = datetime.now().strftime("%Y-%m-%d")
    save_folder = os.path.join("temp", folder_date, "images", "labels")
        
    if (req['part_name'] == "Insulator A"):
        part_code = [
            {"a": "2PD06236/2-1D", "b": "2PD06237/2-1D", 'mat_no': '49001923, 49001922', 'order': f'{_increment_last_number(req['order_id'])}, {req['order_id']}' }, 
            {"a": "2PD06236/1-1D", "b": "2PD06237/1-1D", 'mat_no': '49001922, 49001923', 'order': f'{req['order_id']}, {increment_last_number(req['order_id'])}' },
            {"a": "2PD04461/1-1", "b": "2PD04462/1-1", 'mat_no': '49001928, 49001929', 'order': f'{req['order_id']}, {increment_last_number(req['order_id'])}' },
            {"a": "2P495491-1/1", "b": "2P495492-1/1", 'mat_no': '', 'order': f'{req['order_id']}, {increment_last_number(req['order_id'])}' },
            {"a": "2PD03599/1-1", "b": "2PD03599/1-1", 'mat_no': '49001930', 'order': f'{req['order_id']}, {increment_last_number(req['order_id'])}'}
        ]
        
        a_codes = [item["a"] for item in part_code]

        closest_match = difflib.get_close_matches(req['part_code'], a_codes, n=1, cutoff=0.5)

        dataPartAB = next((item for item in part_code if item['a'] == closest_match[0]), None) if closest_match else None

        zpl_content = f"""
    ^FO{move_along_lenh(req['tag_no'], 640, 30)},5^A0N,60,60^FD{req['tag_no']}^FS
    
    ^FO10,72^A0N,25,25^FDCustomer Name : {req['customer_name']}^FS
    ^FO480,72^A0N,25,25^FDModel {req['model']}^FS
    ^FO10,112^A0N,25,25^FDSupplier^FS
    ^FO110,112^A0N,25,25^FD{req['supplier']}^FS

    ^FO10,152^A0N,23,23^FDOrder ID^FS
    ^FO110,152^A0N,21,21^FD{dataPartAB['order']}^FS
    ^FO360,152^A0N,23,23^FDMat'l No^FS
    ^FO460,152^A0N,21,21^FD{dataPartAB['mat_no']}^FS

    ^FO10,195^A0N,20,20^FDPart Code^FS
    ^FO200,195^A0N,20,20^FD{dataPartAB['a']}^FS
    ^FO10,245^A0N,20,20^FDPart Name^FS
    ^FO200,245^A0N,20,20^FDInsulator A^FS
    ^FO105,177^BQN,2,3,10^FDQA,{req['code']}^FS

    ^FO360,195^A0N,23,23^FDMat'l^FS
    ^FO460,195^A0N,25,25^FD{req['mat']}^FS
    ^FO360,245^A0N,23,23^FDColor^FS
    ^FO460,245^A0N,25,25^FD{req['color']}^FS

    ^FO10,295^A0N,20,20^FDPart Code^FS
    ^FO110,295^A0N,20,20^FD{dataPartAB['b']}^FS
    ^FO10,345^A0N,20,20^FDPart Name^FS
    ^FO110,345^A0N,20,20^FDInsulator B^FS
    ^FO260,277^BQN,2,3,10^FDQA,{increment_last_number(req['code'])}^FS
    
    ^FO360,295^A0N,23,23^FDProducer^FS
    ^FO460,295^A0N,25,25^FD{req['producer']}^FS
    ^FO360,345^A0N,23,23^FDDate^FS
    ^FO460,345^A0N,25,25^FD{req['date']}^FS

    ^FO10,390^A0N,23,23^FDPicture of Part^FS

    ^FO360,390^A0N,23,23^FDQuantity (Unit)^FS
    ^FO440,420^A0N,50,50^FDA: {req['quantity']}^FS
    ^FO440,460^A0N,50,50^FDB: {req['quantity']}^FS
    ^FO360,505^A0N,20,20^FDRoHS2^FS
    ^FO585,505^A0N,20,20^FDPCS.^FS
     """
    else: 
         zpl_content = f"""
    ^FO{move_along_lenh(req['tag_no'], 640, 30)},5^A0N,60,60^FD{req['tag_no']}^FS
    
    ^FO10,72^A0N,25,25^FDCustomer Name : {req['customer_name']}^FS
    ^FO480,72^A0N,25,25^FDModel {req['model']}^FS
    ^FO10,112^A0N,25,25^FDSupplier^FS
    ^FO110,112^A0N,25,25^FD{req['supplier']}^FS

    ^FO10,152^A0N,25,25^FDOrder ID^FS
    ^FO110,152^A0N,25,25^FD{req['order_id']}^FS
    ^FO360,152^A0N,23,23^FDMat'l No^FS
    ^FO460,152^A0N,25,25^FD{req['sap_no']}^FS

    ^FO10,205^A0N,30,30^FDPart^FS
    ^FO10,235^A0N,30,30^FDCode^FS
    ^FO110,{move_according_to_conditions(req['part_code'], {9: 210, 11: 213, 13: 215}, 210)}
    ^A0N,{font_size(req['part_code'], {9: "60,60", 11: "50,50", 13: "40,40"})}
    ^FD{req['part_code']}^FS

    ^FO360,195^A0N,23,23^FDMat'l^FS
    ^FO460,195^A0N,25,25^FD{req['mat']}^FS
    ^FO360,245^A0N,23,23^FDColor^FS
    ^FO460,245^A0N,25,25^FD{req['color']}^FS

    ^FO10,305^A0N,30,30^FDPart^FS
    ^FO10,335^A0N,30,30^FDName^FS
    ^FO110,{move_according_to_conditions(req['part_name'], {10: 310, 12: 313, 14: 315, 16: 317, 18: 319}, 321)}
    ^A0N,{font_size(req['part_name'], {9: "60,60", 11: "50,50", 13: "40,40", 15: "35,35", 17: "30,30"}, "25,25")}
    ^FD{req['part_name']}^FS


    ^FO360,295^A0N,23,23^FDProducer^FS
    ^FO460,295^A0N,25,25^FD{req['producer']}^FS
    ^FO360,345^A0N,23,23^FDDate^FS
    ^FO460,345^A0N,25,25^FD{req['date']}^FS

    ^FO10,390^A0N,23,23^FDPicture of Part^FS
    ^FO205,370^BQN,2,5,10^FDQA,{req['code']}^FS

    ^FO360,390^A0N,23,23^FDQuantity (Unit)^FS
    ^FO440,420^A0N,100,100^FD{req['quantity']}^FS
    ^FO360,505^A0N,20,20^FDRoHS2^FS
    ^FO585,505^A0N,20,20^FDPCS.^FS
     """
        
    zpl_part_image = modify_zpl_coordinates(req['zpl_part'], 10, 410)
     
    for i in range(req['number_of_tags']):
        number_of_tags = f"^FO2,530^A0N,20,20^FD{req['code']} ({i + 1}/{req['number_of_tags']})^FS"
        if (req['part_name'] == "Insulator A"):
            zpl_code = f"{head_zpl_640x550}{head_label_640x550}{tabel_zpl_2_part}{zpl_content}{zpl_part_image}{number_of_tags}{footer_zpl}"
            image_path = convert_zpl_to_image(zpl_code, 3.15, 2.7, 8, save_folder)
            res.append(image_path)
        else:
            zpl_code = f"{head_zpl_640x550}{head_label_640x550}{tabel_zpl}{zpl_content}{zpl_part_image}{number_of_tags}{footer_zpl}"
            image_path = convert_zpl_to_image(zpl_code, 3.15, 2.7, 8, save_folder)
            res.append(image_path)
        
    return res
 
head_zpl_640x550 = '^XA^PW640^LL550'
footer_zpl = '^XZ'
logo_zpl_55x55 = '^FO5,0^GFA,385,385,7,,L06C,K01EF,K03EF8,K0FEFE,J01FEFF,J07FEFFC,J0FFEFFE,I03FFEIF8,I07FFEIFC,001IFEJF,003IFEJF8,00JFEJFE,01JFEKF,07JFEKFC,0KFEKFE,1KFELF,07JFEKFC,03JFEKF8,18JFEJFE3,1C7IFEJFCF,1F1IFEJF1F,1F8IFEIFE7F,1FE3FFEIF8FF,1FF1FFEIF3FF,1FFC7FEFFC7FF,1FFE3FEFF9IF,1IF8FEFE3IF,1IFC7EFCJF,0JF1EF1IFE,07IF8EE7IFC,11IFE00JF1,1CJF03IFE7,1E3IFC7IF8F,1F9IFEJF3F,1FC7FFEIFC7F,1FF3FFEIF9FF,1FF8FFEFFE3FF,1FFE7FEFFCIF,1IF1FEFF1IF,07FFCFEFE7FFC,03FFE3EF8IF8,00IF9EF3FFE,007FFC6C7FFC,001IF01IF,I0IF83FFE,I03FFC7FF8,I01FFEIF,J07FEFFC,J03FEFF8,K0FEFE,K07EFC,K01EF,L0EE,,^FS'
head_label_640x550 = f"{logo_zpl_55x55}^FO65,0^GB5,50,5^FS^FO80,0^A0N,40,40^FDMES B8^FS^FO80,35^A0N,20,20^FDManufacturing Execution System B8^FS"
tabel_zpl = '^FO0,60^GB638,2,2^FS^FO1,100^GB638,2,2^FS^FO1,140^GB638,2,2^FS^FO1,180^GB638,2,2^FS^FO350,229^GB288,2,2^FS^FO1,280^GB638,2,2^FS^FO350,329^GB288,2,2^FS^FO1,380^GB638,2,2^FS^FO1,525^GB638,2,2^FS^FO0,62^GB3,464,3^FS^FO100,100^GB3,280,3^FS^FO350,140^GB3,385,3^FS^FO450,140^GB3,240,3^FS^FO637,62^GB3,464,3^FS'
tabel_zpl_2_part = '^FO0,60^GB638,2,2^FS^FO1,100^GB638,2,2^FS^FO1,140^GB638,2,2^FS^FO1,180^GB638,2,2^FS^FO1,229^GB100,2,2^FS^FO195,229^GB155,2,2^FS^FO350,229^GB288,2,2^FS^FO1,280^GB638,2,2^FS^FO1,329^GB100,2,2^FS^FO100,329^GB155,2,2^FS^FO350,329^GB288,2,2^FS^FO1,380^GB638,2,2^FS^FO1,525^GB638,2,2^FS^FO0,62^GB3,464,3^FS^FO100,100^GB3,280,3^FS^FO350,140^GB3,385,3^FS^FO450,140^GB3,240,3^FS^FO637,62^GB3,464,3^FS'