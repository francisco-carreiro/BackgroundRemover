#!/usr/bin/env python3.10
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from rembg import remove
from tkinterdnd2 import DND_FILES, TkinterDnD

THUMB_SIZE = (100, 100)



class BackgroundRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Background Remover")
        self.root.geometry("640x560")
        self.root.configure(bg="#121212")

        self.file_list = []
        self.thumbnail_refs = []

        # Fonts
        self.font_regular = ("Segoe UI", 10)
        self.font_bold = ("Segoe UI", 11, "bold")

        # Drop Area
        self.drop_area = tk.Label(
            root,
            text="📁  Drag and drop images or click here",
            bg="#282828",
            fg="#fff",
            font=self.font_bold,
            height=3,
            relief="solid",
            bd=1,
            padx=10
        )
        self.drop_area.pack(fill=tk.X, padx=15, pady=12)
        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind('<<Drop>>', self.handle_drop)
        self.drop_area.bind("<Button-1>", self.select_files)

        # File List Area
        self.list_frame = tk.Frame(root, bg="#3f3f3f")
        self.list_frame.pack(fill=tk.BOTH, expand=True, padx=15)

        self.canvas = tk.Canvas(self.list_frame, bg="#ffffff", highlightthickness=1, highlightbackground="#ccc")
        self.scrollbar = tk.Scrollbar(self.list_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#ffffff")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Progress bar
        self.progress = ttk.Progressbar(root, orient="horizontal", mode="determinate")
        self.progress.pack(fill=tk.X, padx=15, pady=(10, 0))

        # Process Button
        self.process_button = tk.Button(
            root,
            text="🚀 Remove Backgrounds",
            command=self.process_files,
            font=self.font_bold,
            bg="#0078D7",
            fg="white",
            activebackground="#005ea6",
            relief="flat",
            bd=0,
            padx=12,
            pady=6
        )
        self.process_button.pack(pady=12)

    def select_files(self, event=None):
        file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        for path in file_paths:
            self.add_file(path)

    def handle_drop(self, event):
        paths = self.root.tk.splitlist(event.data)
        for path in paths:
            if os.path.isdir(path):
                for file in os.listdir(path):
                    full_path = os.path.join(path, file)
                    if full_path.lower().endswith((".jpg", ".jpeg", ".png")):
                        self.add_file(full_path)
            elif path.lower().endswith((".jpg", ".jpeg", ".png")):
                self.add_file(path)

    def add_file(self, path):
        if path not in self.file_list:
            try:
                image = Image.open(path)
                image.thumbnail(THUMB_SIZE)
                thumb = ImageTk.PhotoImage(image)
                self.thumbnail_refs.append(thumb)  # Keep reference!

                card = tk.Frame(self.scrollable_frame, bg="#ffffff", highlightthickness=1, highlightbackground="#cccccc")
                card.pack(fill=tk.X, pady=6, padx=12, ipady=5, ipadx=5)

                label_img = tk.Label(card, image=thumb, bg="#ffffff")
                label_img.pack(side=tk.LEFT, padx=10, pady=5)

                label_name = tk.Label(card, text=os.path.basename(path), bg="#ffffff", fg="#333", anchor="w", font=self.font_regular)
                label_name.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

                self.file_list.append(path)
            except Exception as e:
                print(f"Error loading thumbnail: {e}")

    def process_files(self):
        if not self.file_list:
            messagebox.showwarning("No Files", "Please add image files first.")
            return

        output_dir = filedialog.askdirectory(title="Select Output Folder")
        if not output_dir:
            return

        self.progress["maximum"] = len(self.file_list)
        self.progress["value"] = 0
        self.root.update_idletasks()

        for i, path in enumerate(self.file_list):
            try:
                with Image.open(path) as input_image:
                    output_image = remove(input_image)
                    filename = os.path.basename(path)
                    name, _ = os.path.splitext(filename)
                    output_path = os.path.join(output_dir, name + ".png")
                    output_image.save(output_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process {path}:\n{e}")
                continue

            self.progress["value"] = i + 1
            self.root.update_idletasks()

        messagebox.showinfo("Done", f"Processed {len(self.file_list)} images.\nSaved to '{output_dir}'.")
        self.reset()

    def reset(self):
        self.file_list.clear()
        self.thumbnail_refs.clear()
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.progress["value"] = 0

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    root.iconbitmap("icon.ico")
    app = BackgroundRemoverApp(root)
    root.mainloop()
