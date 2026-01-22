from app.services.ocr import run_ocr

text = run_ocr("samples/marks_sheet_1.webp")
print("OCR OUTPUT:")
print(text)
