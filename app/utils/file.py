import os
import threading


def delete_file_after_delay(file_path, delay_seconds=12 * 60 * 60):
    def delete():
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File {file_path} deleted")
        threading.Timer(delay_seconds, delete).start()

    delete()
    
def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File {file_path} deleted")
 