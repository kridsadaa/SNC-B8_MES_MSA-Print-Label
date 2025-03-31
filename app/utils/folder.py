import os
import shutil


def delete_folder(folder_path):
    if os.path.isdir(folder_path):
        shutil.rmtree(folder_path)   
        print(f"Folder {folder_path} deleted")
    else:
        print(f"{folder_path}, Not a folder or the folder was not found")
