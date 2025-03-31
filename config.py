import os


class Config:
    # ค่าคอนฟิกทั่วไป
    # SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")  # ใช้จาก environment variable หรือค่า default
    FLASK_APP = "MAS_B8-MES_Print-Label"
    FLASK_ENV = "development"  # กำหนดโหมดการทำงานของ Flask

    # # ค่าคอนฟิกสำหรับฐานข้อมูล
    # SQLALCHEMY_TRACK_MODIFICATIONS = False  # ปิดการติดตามการเปลี่ยนแปลง
    # SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///default.db")  # URL ของฐานข้อมูล

    # ค่าคอนฟิกสำหรับการอัปโหลดไฟล์
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "app", "media")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # จำกัดขนาดไฟล์สูงสุด 16MB
