# File Organizer
# Author: Jatin Dangi   
# Date: 24/07/2025
# Description: A simple file organizer application that helps you categorize and organize your files by type.


import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext


# File type categories
FILE_CATEGORIES = {
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.ppt', '.pptx', '.odt', '.rtf'],
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp'],
    'Videos': ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm'],
}
CATEGORY_NAMES = list(FILE_CATEGORIES.keys()) + ['Others']

selected_dir = None

# --- UI Colors and Fonts ---
BG_COLOR = '#f4f6fb'
FRAME_COLOR = '#e0e7ef'
BTN_COLOR = '#4f8cff'
BTN_TEXT = '#fff'
TITLE_FONT = ('Segoe UI', 18, 'bold')
LABEL_FONT = ('Segoe UI', 11)
BTN_FONT = ('Segoe UI', 11, 'bold')


def get_category(filename):
    ext = os.path.splitext(filename)[1].lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return 'Others'

def organize_files(target_dir, status_label=None):
    if not os.path.isdir(target_dir):
        messagebox.showerror('Error', 'Selected path is not a directory.')
        return
    for category in CATEGORY_NAMES:
        os.makedirs(os.path.join(target_dir, category), exist_ok=True)
    moved_files = {cat: [] for cat in CATEGORY_NAMES}
    for item in os.listdir(target_dir):
        item_path = os.path.join(target_dir, item)
        if os.path.isfile(item_path):
            category = get_category(item)
            dest_dir = os.path.join(target_dir, category)
            shutil.move(item_path, os.path.join(dest_dir, item))
            moved_files[category].append(item)
    # Build summary message
    summary_lines = []
    for category, files in moved_files.items():
        if files:
            summary_lines.append(f'{category}:')
            for f in files:
                summary_lines.append(f'  - {f}')
    if not summary_lines:
        summary = 'No files were moved.'
    else:
        summary = 'Files organized successfully!\n\n' + '\n'.join(summary_lines)
    messagebox.showinfo('Summary', summary)
    if status_label:
        status_label.config(text='Organization complete!')
    # Open the folder in the system's file explorer
    try:
        if os.name == 'nt':  # Windows
            os.startfile(target_dir)
        elif os.name == 'posix':
            import sys
            if sys.platform == 'darwin':  # macOS
                os.system(f'open "{target_dir}"')
            else:  # Linux and others
                os.system(f'xdg-open "{target_dir}"')
    except Exception as e:
        messagebox.showwarning('Warning', f'Could not open folder: {e}')

def show_folder_details(dir_path):
    files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    if not files:
        file_list = 'No files to organize.'
    else:
        file_list = '\n'.join(files)
    details = f'Selected folder:\n{dir_path}\n\nFiles:\n{file_list}'
    return details

def confirm_and_organize(dir_path, status_label):
    details = show_folder_details(dir_path)
    answer = messagebox.askyesno('Confirm Organization', f'{details}\n\nDo you want to organize this folder?')
    if answer:
        organize_files(dir_path, status_label)

def select_directory(folder_var, details_text, organize_btn, status_label):
    global selected_dir
    dir_path = filedialog.askdirectory()
    if dir_path:
        selected_dir = dir_path
        folder_var.set(dir_path)
        details = show_folder_details(dir_path)
        details_text.config(state='normal')
        details_text.delete(1.0, tk.END)
        details_text.insert(tk.END, details)
        details_text.config(state='disabled')
        organize_btn.config(state='normal')
        status_label.config(text='Ready to organize.')
    else:
        organize_btn.config(state='disabled')
        status_label.config(text='No folder selected.')

def on_organize(folder_var, details_text, organize_btn, status_label):
    if selected_dir:
        confirm_and_organize(selected_dir, status_label)
        # Refresh details after organizing
        details = show_folder_details(selected_dir)
        details_text.config(state='normal')
        details_text.delete(1.0, tk.END)
        details_text.insert(tk.END, details)
        details_text.config(state='disabled')
        organize_btn.config(state='disabled')
        status_label.config(text='No folder selected.')

def main():
    root = tk.Tk()
    root.title('File Organizer')
    root.geometry('520x480')
    root.configure(bg=BG_COLOR)
    # root.resizable(False, False)  # Allow resizing for responsiveness

    # Configure grid weights for responsiveness
    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Title
    title = tk.Label(root, text='File Organizer', font=TITLE_FONT, bg=BG_COLOR, fg='#2d3a4a')
    title.grid(row=0, column=0, sticky='ew', pady=(18, 2), padx=10)
    subtitle = tk.Label(root, text='Organize your files by type with one click', font=LABEL_FONT, bg=BG_COLOR, fg='#4f8cff')
    subtitle.grid(row=1, column=0, sticky='ew', pady=(0, 12), padx=10)

    # Frame for folder selection
    frame = tk.Frame(root, bg=FRAME_COLOR, bd=2, relief='groove')
    frame.grid(row=2, column=0, padx=18, pady=8, sticky='ew')
    frame.grid_columnconfigure(1, weight=1)

    folder_var = tk.StringVar()
    folder_label = tk.Label(frame, text='Selected Folder:', font=LABEL_FONT, bg=FRAME_COLOR)
    folder_label.grid(row=0, column=0, padx=8, pady=8, sticky='w')
    folder_entry = tk.Entry(frame, textvariable=folder_var, font=LABEL_FONT, width=40, state='readonly', relief='flat', bg='#f8fafc')
    folder_entry.grid(row=0, column=1, padx=4, pady=8, sticky='ew')
    browse_btn = tk.Button(frame, text='Browse...', font=BTN_FONT, bg=BTN_COLOR, fg=BTN_TEXT, activebackground='#3566b8', activeforeground=BTN_TEXT, command=lambda: select_directory(folder_var, details_text, organize_btn, status_label))
    browse_btn.grid(row=0, column=2, padx=8, pady=8, sticky='e')

    # Details area
    details_label = tk.Label(root, text='Folder Details:', font=LABEL_FONT, bg=BG_COLOR)
    details_label.grid(row=3, column=0, sticky='w', padx=28, pady=(16, 2))
    details_text = scrolledtext.ScrolledText(root, width=60, height=12, font=('Consolas', 10), state='disabled', bg='#f8fafc', relief='solid', bd=1)
    details_text.grid(row=4, column=0, padx=28, pady=(0, 10), sticky='nsew')
    root.grid_rowconfigure(4, weight=1)

    # Organize button
    organize_btn = tk.Button(root, text='Organize Files', font=BTN_FONT, bg=BTN_COLOR, fg=BTN_TEXT, activebackground='#3566b8', activeforeground=BTN_TEXT, width=20, state='disabled', command=lambda: on_organize(folder_var, details_text, organize_btn, status_label))
    organize_btn.grid(row=5, column=0, pady=10)

    # Status label
    status_label = tk.Label(root, text='No folder selected.', font=('Segoe UI', 9), bg=BG_COLOR, fg='#888')
    status_label.grid(row=6, column=0, pady=10, sticky='ew')

    root.mainloop()

if __name__ == '__main__':
    main()