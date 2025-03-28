from io import BytesIO

import requests
from PIL import Image


def zpl_to_image(zpl_code, width=300, height=300, dpi=203):
    url = "http://api.labelary.com/v1/printers/{dpi}dpi/labels/{width}x{height}/0/".format(
        dpi=dpi, width=width, height=height
    )

    response = requests.post(url, data=zpl_code.encode("utf-8"), headers={"Accept": "image/png"})
    
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        return image
    else:
        print(f"เกิดข้อผิดพลาด: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    with open("image.zpl", "r") as file:
        zpl_code = file.read()

    image = zpl_to_image(zpl_code)

    if image:
        image.show()  # แสดงภาพ
        image.save("output.png")  # บันทึกเป็นไฟล์ PNG
        print("บันทึกภาพเป็น 'output.png'")
