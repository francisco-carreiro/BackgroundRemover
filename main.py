import os
import customtkinter as ctk
from customtkinter import CTkImage
from tkinter import filedialog, messagebox
from PIL import Image
from rembg import remove
from tkinterdnd2 import DND_FILES, TkinterDnD

THUMB_SIZE = (100, 100)

class BackgroundRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Background Remover")
        self.root.geometry("750x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.file_list = []
        self.thumbnail_refs = []

        # Main frame
        self.main_frame = ctk.CTkFrame(root, corner_radius=15)
        self.main_frame.pack(fill="both", expand=True)
        self.root.overrideredirect(True)
        
        # Custom title bar
        self.title_bar = ctk.CTkFrame(self.main_frame, corner_radius=0, height=30, fg_color="#2b2b2b")
        self.title_bar.pack(fill="x", side="top")

        # App title
        self.title_label = ctk.CTkLabel(self.title_bar, text="  Background Remover", font=ctk.CTkFont(size=13, weight="bold"))
        self.title_label.pack(side="left", padx=10)
        
        # Close button
        self.close_button = ctk.CTkButton(self.title_bar, text="✕", width=20, command=self.root.destroy, fg_color="transparent", hover_color="#a00", corner_radius=0)
        self.close_button.pack(side="right")
        
        # Maximize / restore (optional)
        self.maximize_button = ctk.CTkButton(self.title_bar, text="□", width=20, command=self.maximize_window, fg_color="transparent", hover_color="#444", corner_radius=0)
        self.maximize_button.pack(side="right")
        
        # Minimize button
        self.minimize_button = ctk.CTkButton(self.title_bar, text="–", width=20, command=self.minimize_window, fg_color="transparent", hover_color="#444", corner_radius=0)
        self.minimize_button.pack(side="right", padx=(0, 2))

        self.title_bar.bind("<Button-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)
        self.title_label.bind("<Button-1>", self.start_move)
        self.title_label.bind("<B1-Motion>", self.do_move)
        
        # Drop area
        self.drop_area = ctk.CTkButton(
            self.main_frame,
            text="📁 Drag and drop images or click to select",
            command=self.select_files,
            fg_color="#e3eaf0",
            hover_color="#d0d9e2",
            text_color="#333",
            corner_radius=10,
            height=50,
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.drop_area.pack(padx=10, pady=10, fill="x")

        # Drag-and-drop binding
        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind('<<Drop>>', self.handle_drop)
        self.drop_area.bind("<Enter>", lambda e: self.drop_area.configure(fg_color="#dceaf6"))
        self.drop_area.bind("<Leave>", lambda e: self.drop_area.configure(fg_color="#e3eaf0"))

        # Container for scroll area and background watermark
        self.scroll_container = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.scroll_container.pack(padx=10, pady=10, fill="both", expand=True)

        # Load watermark and place it in the background
        watermark_pil = Image.open("watermark.png")
        self.watermark_tk = CTkImage(light_image=watermark_pil, size=(250, 250))
        
        # Scrollable frame layered on top
        self.scroll_frame = ctk.CTkScrollableFrame(self.scroll_container, corner_radius=10, fg_color="transparent")
        self.scroll_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        self.watermark_label = ctk.CTkLabel(self.scroll_container, image=self.watermark_tk, text="")
        self.watermark_label.place(relx=0.5, rely=0.5, anchor="center")

        # Progress bar
        self.progress = ctk.CTkProgressBar(self.main_frame)
        self.progress.pack(padx=10, pady=(10, 0), fill="x")
        self.progress.set(0)

        # Process button
        self.process_button = ctk.CTkButton(
            self.main_frame,
            text="🚀 Remove Background",
            command=self.process_files,
            fg_color="#0078D7",
            hover_color="#005fa3",
            corner_radius=8,
            height=45,
            font=ctk.CTkFont(weight="bold")
        )
        self.process_button.pack(pady=12)
    
    def select_files(self):
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
                thumb = CTkImage(light_image=image, size=THUMB_SIZE)
                self.thumbnail_refs.append(thumb)

                card = ctk.CTkFrame(self.scroll_frame, corner_radius=10)
                card.pack(fill="x", pady=6, padx=10)

                label_img = ctk.CTkLabel(card, image=thumb, text="")
                label_img.pack(side="left", padx=10, pady=5)

                label_name = ctk.CTkLabel(card, text=os.path.basename(path), anchor="w")
                label_name.pack(side="left", fill="x", expand=True, padx=10)

                self.file_list.append(path)
                
                self.watermark_label.place_forget()
                                
            except Exception as e:
                print(f"Error loading thumbnail: {e}")
                
    def process_files(self):
        if not self.file_list:
            messagebox.showwarning("No Files", "Please add image files first.")
            return

        output_dir = filedialog.askdirectory(title="Select Output Folder")
        if not output_dir:
            return

        self.progress.configure(mode="determinate")
        self.progress.set(0)
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

            self.progress.set((i + 1) / len(self.file_list))
            self.root.update_idletasks()

        messagebox.showinfo("Done", f"Processed {len(self.file_list)} images.\nSaved to '{output_dir}'.")
        self.reset()

    def reset(self):
        self.file_list.clear()
        self.thumbnail_refs.clear()
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.watermark_label.place(relx=0.5, rely=0.5, anchor="center")
        self.watermark_label.lower()
        self.progress.set(0)
        
    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        self.root.geometry(f"+{event.x_root - self.x}+{event.y_root - self.y}")
        
    def minimize_window(self):
        self.root.update_idletasks()
        self.root.overrideredirect(False)
        self.root.iconify()
        self.root.after(10, lambda: self.root.overrideredirect(True))
    
    def maximize_window(self):
        if self.root.state() == "zoomed":
            self.root.state("normal")
        else:
            self.root.state("zoomed")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    root.iconbitmap("icon.ico")
    app = BackgroundRemoverApp(root)
    root.mainloop()
