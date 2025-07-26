import os
import shutil

target_dir = input("Enter the full path of the folder to organize: ").strip()

if not os.path.isdir(target_dir):
    print("Invalid folder path.")
    exit()

script_path = os.path.abspath(__file__)
script_name = os.path.basename(script_path)

file_types = {
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv"],
}

for file in os.listdir(target_dir):
    path = os.path.join(target_dir, file)
    if os.path.abspath(path) == script_path:
        continue
    if os.path.isfile(path):
        ext = os.path.splitext(file)[1].lower()
        placed = False
        for folder, extensions in file_types.items():
            if ext in extensions:
                folder_path = os.path.join(target_dir, folder)
                os.makedirs(folder_path, exist_ok=True)
                shutil.move(path, os.path.join(folder_path, file))
                placed = True
                break
        if not placed:
            other_path = os.path.join(target_dir, "Others")
            os.makedirs(other_path, exist_ok=True)
            shutil.move(path, os.path.join(other_path, file))