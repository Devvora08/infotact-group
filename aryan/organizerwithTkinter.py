import os
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# File categories
file_types = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
    'Documents': ['.pdf', '.docx', '.doc', '.txt', '.pptx'],
    'Videos': ['.mp4', '.mkv', '.avi'],
    'Music': ['.mp3', '.wav'],
    'Archives': ['.zip', '.rar', '.tar', '.gz'],
    'Scripts': ['.py', '.js', '.html', '.css'],
    'Others': []
}

# 🔍 Get all files (even inside subfolders)
def get_files_in_folder(folder_path):
    files = []
    for root, _, filenames in os.walk(folder_path):
        for filename in filenames:
            full_path = os.path.join(root, filename)
            files.append(full_path)
    return files

# 📦 Move files
def move_file_to_folder(file_name, from_folder, to_folder, log_callback):
    os.makedirs(to_folder, exist_ok=True)
    source = os.path.join(from_folder, file_name)
    destination = os.path.join(to_folder, file_name)

    if os.path.exists(destination):
        base_name, extension = os.path.splitext(file_name)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        new_file_name = f"{base_name}_{timestamp}{extension}"
        destination = os.path.join(to_folder, new_file_name)

    shutil.move(source, destination)
    log_callback(f"✅ Moved '{file_name}' to → {to_folder}")

# 🧹 Organize the folder
def organize_folder(folder_path, log_callback):
    files = get_files_in_folder(folder_path)

    for file in files:
        file_ext = os.path.splitext(file)[1].lower()
        file_name = os.path.basename(file)
        from_folder = os.path.dirname(file)
        moved = False

        for folder, extensions in file_types.items():
            if file_ext in extensions:
                move_file_to_folder(file_name, from_folder, os.path.join(folder_path, folder), log_callback)
                moved = True
                break

        if not moved:
            move_file_to_folder(file_name, from_folder, os.path.join(folder_path, "Others"), log_callback)

# 🧼 Remove empty folders
def remove_empty_folders(folder_path):
    for root, dirs, _ in os.walk(folder_path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)

# GUI starts here
def start_gui():
    def browse_folder():
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            folder_entry.delete(0, tk.END)
            folder_entry.insert(0, folder_selected)

    def log_message(msg):
        log_box.insert(tk.END, msg + "\n")
        log_box.see(tk.END)

    def organize_action():
        folder_path = folder_entry.get().strip()
        if not folder_path or not os.path.exists(folder_path):
            messagebox.showerror("Error", "Please select a valid folder.")
            return
        log_box.delete(1.0, tk.END)
        log_message("🧹 Organizing files (including subfolders)...\n")
        organize_folder(folder_path, log_message)
        remove_empty_folders(folder_path)
        log_message("\n✨ Done! Your folder is now clean and sorted.")

    # Create main window
    root = tk.Tk()
    root.title("Folder Organizer")
    root.geometry("800x500")  # Increased width & height
    root.resizable(False, False)

    tk.Label(root, text="📁 Select Folder to Organize:", font=("Arial", 12)).pack(pady=10)

    # Folder selection entry and button
    entry_frame = tk.Frame(root)
    entry_frame.pack(pady=5)
    folder_entry = tk.Entry(entry_frame, width=65, font=("Arial", 10))  # Wider entry box
    folder_entry.pack(side=tk.LEFT, padx=5)
    browse_btn = tk.Button(entry_frame, text="Browse", command=browse_folder)
    browse_btn.pack(side=tk.LEFT)

    # Organize button
    organize_btn = tk.Button(root, text="Organize Now", command=organize_action,
                             bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), width=20)
    organize_btn.pack(pady=15)

    # Output log
    log_box = scrolledtext.ScrolledText(root, width=90, height=18, font=("Courier", 10))  # Bigger log box
    log_box.pack(padx=10, pady=10)

    root.mainloop()

# Run GUI
if __name__ == "__main__":
    start_gui()