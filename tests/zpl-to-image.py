import os
import shutil
import uuid
from datetime import datetime

import requests


def zpl_to_image(zpl_code, width=4, height=6, dpmm=8):
    folder_name = datetime.now().strftime("%Y-%m-%d")
    folder_path = os.path.join("images", folder_name)
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
 
    file_name = f"{uuid.uuid4().hex}.png"  
    file_path = os.path.join(folder_path, file_name)
 
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

if __name__ == "__main__":
    zpl_code = "^XA^FO50,50^BQN,2,10^FDQA,Hello World!^FS^XZ"
    image_path = zpl_to_image(zpl_code)
    if image_path:
        print(f"ไฟล์ที่บันทึก: {image_path}")
