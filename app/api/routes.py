from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.file_handler import save_file
from app.services.ocr import extract_text
from app.services.llm import normalize_with_llm

router = APIRouter()

@router.post("/extract")
async def extract_marksheet(file: UploadFile = File(...)):
    if file.content_type not in (
        "image/jpeg",
        "image/png",
        "application/pdf",
    ):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    file_path = save_file(file)

    print("START OCR")
    ocr_blocks = extract_text(file_path)
    print("OCR BLOCKS:", len(ocr_blocks))

    if not ocr_blocks:
        raise HTTPException(
            status_code=422,
            detail="No text detected in image"
        )

    structured_output = normalize_with_llm(ocr_blocks)

    if "llm_error" in structured_output:
        return {
            "ocr_blocks_count": len(ocr_blocks),
            "ocr_text_preview": [b["text"] for b in ocr_blocks[:30]],
            "structured_fallback": structured_output
        }

    return structured_output
