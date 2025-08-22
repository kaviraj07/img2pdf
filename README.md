# :arrows_counterclockwise: img2pdf

A simple Python tool to convert a folder of scanned JPG images into a single merged PDF, with automatic orientation fixes and optional cleanup of intermediate files.

---
## :star: Features

- Reads `.jpg` / `.jpeg` images from a folder (`img/` by default).
- Preserves orientation using EXIF metadata.
- Optionally enforces **portrait** orientation (default) or **landscape**.
- Stores per-page PDFs in a temporary folder (`img/pages/`).
- Merges into a single PDF saved in `pdf_output/`.
- Optional `--cleanup` flag to delete intermediate page PDFs after merging.

---

## :hammer_and_wrench: Requirements
- Python 3.7+
- See `pyproject.toml` for dependencies

---

## :rocket: Usage
1. Place your images (JPG, JPEG) in the `img/` folder.
2. Run the script:
   ```cmd
   python main.py [options]
   ```
   
   **Command Line Arguments:**
   - `-o`, `--output` : Output PDF filename or path (default: merged_notes.pdf)
   - `--img-dir` : Folder containing input images (default: img)
   - `--pages-dir` : Folder to store intermediate single-page PDFs (default: img/pages)
   - `--cleanup` : Delete the pages folder after merging
   - `--mode` : Set orientation of output PDF (`portrait` or `landscape`, default: portrait)

   **Examples:**
   ```cmd
   python main.py --output my_notes --mode landscape --cleanup
   python main.py --img-dir scans --output final --mode portrait
   ```
3. The resulting PDF will be saved in the `pdf_output/` folder.

---
## :file_folder: Project Structure
```
img2pdf/
├── main.py           # Main script to run the conversion
├── pyproject.toml    # Project dependencies and metadata
├── README.md         # Project documentation
├── uv.lock           # Lock file for dependencies
├── img/              # Input images
└── pdf_output/       # Output PDF files
```
---
## :exclamation: Disclaimer
This project was created using **vibe-coding**.

## :scroll: License
MIT
