import argparse
import shutil
from pathlib import Path
from PIL import Image, ImageOps
from PyPDF2 import PdfMerger
from natsort import natsorted


def collect_images(img_dir: Path):
    # Case-insensitive JPG/JPEG collection without duplicates
    valid_exts = {".jpg", ".jpeg"}
    seen = set()
    imgs = []
    for p in img_dir.iterdir():
        if p.is_file() and p.suffix.lower() in valid_exts:
            key = p.resolve().as_posix().lower()
            if key not in seen:
                seen.add(key)
                imgs.append(p)
    return natsorted(imgs, key=lambda x: x.name)


def convert_to_pdfs(imgs, pages_dir: Path, mode):
    pages_dir.mkdir(parents=True, exist_ok=True)
    pdf_paths = []
    for p in imgs:
        with Image.open(p) as im:
            im = ImageOps.exif_transpose(im)  # respect EXIF
            if mode == "portrait" and im.width > im.height:  # enforce portrait
                im = im.rotate(90, expand=True)
            im = im.convert("RGB")
            out = (pages_dir / p.stem).with_suffix(".pdf")
            im.save(out)
            pdf_paths.append(out)
    return pdf_paths


def merge_pdfs(pdf_paths, output_pdf: Path):
    merger = PdfMerger()
    for pdf in pdf_paths:
        merger.append(str(pdf))
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    merger.write(str(output_pdf))
    merger.close()


def main():
    parser = argparse.ArgumentParser(description="Convert JPGs to a merged PDF with optional cleanup.")
    parser.add_argument("-o", "--output", default="merged_notes.pdf",
                        help="Output PDF filename or path (default: merged_notes.pdf)")
    parser.add_argument("--img-dir", default="img",
                        help="Folder containing input images (default: img)")
    parser.add_argument("--pages-dir", default="img/pages",
                        help="Folder to store intermediate single-page PDFs (default: img/pages)")
    parser.add_argument("--cleanup", action="store_true",
                        help="Delete the pages folder after merging")
    parser.add_argument("--mode", choices=["portrait", "landscape"], default="portrait",
                        help="Set the orientation of the output PDF (default: portrait)")
    args = parser.parse_args()

    img_dir = Path(args.img_dir)
    pages_dir = Path(args.pages_dir)
    pdf_dir = Path("pdf_output")
    output_pdf = pdf_dir / f"{args.output}.pdf"
    mode = args.mode

    if output_pdf.suffix.lower() != ".pdf":
        output_pdf = output_pdf.with_suffix(".pdf")

    if not img_dir.exists():
        raise SystemExit(f"Input folder not found: {img_dir}")

    imgs = collect_images(img_dir)
    if not imgs:
        raise SystemExit(f"No JPG/JPEG files found in ./{img_dir}")

    pdf_paths = convert_to_pdfs(imgs, pages_dir, mode)
    merge_pdfs(pdf_paths, output_pdf)

    print(f"\n✅ Done. Created {output_pdf} from {len(pdf_paths)} pages.")
    print(f"📁 Per-page PDFs are in: {pages_dir}")

    if args.cleanup:
        # remove the entire pages_dir safely
        shutil.rmtree(pages_dir, ignore_errors=True)
        print(f"🧹 Cleaned up: {pages_dir} deleted.")

if __name__ == "__main__":
    main()