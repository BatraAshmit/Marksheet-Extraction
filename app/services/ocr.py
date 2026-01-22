from typing import List, Dict
import easyocr

_reader = None


def _get_reader():
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(['en'], gpu=False)
    return _reader


def extract_text(image_path: str) -> List[Dict]:
    """
    Extract text from an image using EasyOCR.
    Returns a list of {text, confidence, bbox}.
    """
    reader = _get_reader()

    try:
        results = reader.readtext(image_path)
    except Exception as e:
        print("OCR ERROR:", str(e))
        return []

    extracted = []
    for bbox, text, conf in results:
        extracted.append({
            "text": text.strip(),
            "confidence": float(conf),
            "bbox": bbox
        })

    return extracted
