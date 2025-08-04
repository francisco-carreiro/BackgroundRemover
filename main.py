#!/usr/bin/env python3.10
import os
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar
from rembg import remove
from PIL import Image
from tkinterdnd2 import DND_FILES, TkinterDnD

class BackgroundRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Background Remover")
        self.root.geometry("500x400")

        self.file_list = []

        self.drop_area = tk.Label(root, text="Drag and drop images here\n(or click to select)", bg="#e0e0e0", height=5)
        self.drop_area.pack(pady=10, fill=tk.X, padx=10)

        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind('<<Drop>>', self.handle_drop)
        self.drop_area.bind("<Button-1>", self.select_files)

        self.listbox = Listbox(root)
        self.listbox.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

        self.scrollbar = Scrollbar(self.listbox, orient="vertical", command=self.listbox.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.process_button = tk.Button(root, text="Remove Backgrounds", command=self.process_files)
        self.process_button.pack(pady=10)

    def select_files(self, event=None):
        file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        for path in file_paths:
            self.add_file(path)

    def handle_drop(self, event):
        dropped_files = self.root.tk.splitlist(event.data)
        for path in dropped_files:
            if os.path.isdir(path):
                for file in os.listdir(path):
                    full_path = os.path.join(path, file)
                    if full_path.lower().endswith((".jpg", ".jpeg", ".png")):
                        self.add_file(full_path)
            elif path.lower().endswith((".jpg", ".jpeg", ".png")):
                self.add_file(path)

    def add_file(self, path):
        if path not in self.file_list:
            self.file_list.append(path)
            self.listbox.insert(tk.END, os.path.basename(path))

    def process_files(self):
        if not self.file_list:
            messagebox.showwarning("No Files", "Please add image files first.")
            return

        output_dir = filedialog.askdirectory(title="Select Output Folder")
        if not output_dir:
            return  # User cancelled

        for path in self.file_list:
            try:
                input_image = Image.open(path)
                output_image = remove(input_image)
                filename = os.path.basename(path)
                name, _ = os.path.splitext(filename)
                output_path = os.path.join(output_dir, name + ".png")
                output_image.save(output_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process {path}:\n{e}")
                continue

        messagebox.showinfo("Done", f"Processed {len(self.file_list)} images.\nSaved to '{output_dir}'.")
        self.file_list.clear()
        self.listbox.delete(0, tk.END)

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = BackgroundRemoverApp(root)
    root.mainloop()
