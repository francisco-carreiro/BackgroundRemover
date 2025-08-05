
# 🧼 Background Remover

A clean, modern desktop app to automatically remove backgrounds from images using AI — with support for batch processing, drag-and-drop, watermark overlay, and a beautiful custom UI built in `customtkinter`.

---

## 🚀 Features

- ✅ Drag & Drop images or folders
- ✅ Automatic background removal (powered by [rembg](https://github.com/danielgatis/rembg))
- ✅ Real-time thumbnail preview
- ✅ Transparent output (`.png`) with background removed
- ✅ Custom title bar with minimize/close buttons
- ✅ Watermark overlay (optional)
- ✅ Dark mode interface
- ✅ Export as a standalone `.exe`

---

## 🖥️ Requirements

- Python 3.10+
- Pip

Install all dependencies:

```bash
pip install -r requirements.txt
```

**Or install them manually:**

```bash
pip install customtkinter rembg pillow tkinterdnd2
```

---

## 📁 Project Structure

```text
BackgroundRemover/
├── main.py                 # Main app code
├── icon.ico               # Window icon
├── watermark.png          # Optional background watermark
├── requirements.txt
```

---

## ▶️ Run the App (Dev Mode)

1. Clone or download this repo
2. Make sure Python 3.10 is installed
3. Run the app:

```bash
python main.py
```

---

## 💻 Build the Executable

To bundle as a `.exe` using [PyInstaller](https://pyinstaller.org/):

```bash
pyinstaller --onefile --noconsole --icon=icon.ico main.py
```

Or faster boot but larger folder:

```bash
pyinstaller --onedir --noconsole --icon=icon.ico main.py
```

---

## 🧪 Tips

- Place images or folders into the drag zone to process them
- Backgrounds will be removed and saved as `.png` files
- Files are saved to your selected output directory
- You can customize `main.py` to add background replacement or format conversion

---

## 📦 Packaging Notes

To ensure assets like `watermark.png` or `icon.ico` are bundled, use:

```bash
pyinstaller --onefile --noconsole --icon=icon.ico --add-data "watermark.png;." main.py
```

---

## 📃 License

MIT License — feel free to fork, modify, and use commercially.

---

## ✨ Credits

Built with:
- [customtkinter](https://github.com/TomSchimansky/CustomTkinter)
- [rembg](https://github.com/danielgatis/rembg)
- [tkinterdnd2](https://github.com/pmgagne/tkinterdnd2)
- Designed and packaged with ❤️ by *Francisco Machado Carreiro*.
