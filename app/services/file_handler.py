import os
import uuid
import fitz  
from fastapi import UploadFile, HTTPException

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "pdf"}


def save_file(file: UploadFile) -> str:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Empty filename")

    ext = file.filename.split(".")[-1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    file_id = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, file_id)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    if ext == "pdf":
        return pdf_to_image(file_path)

    return file_path


def pdf_to_image(pdf_path: str) -> str:
    try:
        doc = fitz.open(pdf_path)

        if doc.page_count == 0:
            doc.close()
            raise HTTPException(
                status_code=422,
                detail="PDF contains no pages"
            )

        page = doc.load_page(0)
        pix = page.get_pixmap(dpi=200)

        image_path = pdf_path.replace(".pdf", ".png")
        pix.save(image_path)

        doc.close()
        os.remove(pdf_path) 

        return image_path

    except Exception as e:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

        raise HTTPException(
            status_code=500,
            detail=f"Failed to process PDF: {str(e)}"
        )
