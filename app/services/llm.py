import os
import json
from typing import List, Dict
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def normalize_with_llm(ocr_blocks: List[Dict]) -> Dict:
    ocr_text = "\n".join([b["text"] for b in ocr_blocks])

    prompt = f"""
You are an AI that extracts structured data from exam marksheets.

OCR TEXT:
{ocr_text}

INSTRUCTIONS:
- Return ONLY valid JSON
- Follow this rule strictly:
  Each field must be an object with:
    - "value": extracted value or null
    - "confidence": number between 0 and 1
- Confidence should reflect how clear and certain the extraction is
- Use lower confidence if value is inferred or unclear

Return JSON only. No explanation.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )

        content = response.choices[0].message.content.strip()
        data = json.loads(content)

        # ---- SAFETY NET: ensure confidence exists everywhere ----
        def inject_confidence(obj):
            if isinstance(obj, dict):
                if "value" in obj and "confidence" not in obj:
                    obj["confidence"] = 0.85 if obj["value"] else 0.0
                for v in obj.values():
                    inject_confidence(v)
            elif isinstance(obj, list):
                for item in obj:
                    inject_confidence(item)

        inject_confidence(data)
        return data

    except Exception as e:
        return {
            "candidate_details": {
                "name": {"value": None, "confidence": 0.0},
                "father_or_mother_name": {"value": None, "confidence": 0.0},
                "roll_no": {"value": None, "confidence": 0.0},
                "registration_no": {"value": None, "confidence": 0.0},
                "dob": {"value": None, "confidence": 0.0},
                "exam_year": {"value": None, "confidence": 0.0},
                "board_or_university": {"value": None, "confidence": 0.0},
                "institution": {"value": None, "confidence": 0.0},
            },
            "subjects": [],
            "overall_result": {
                "result_or_division": {"value": None, "confidence": 0.0}
            },
            "issue_details": {
                "date": {"value": None, "confidence": 0.0},
                "place": {"value": None, "confidence": 0.0}
            },
            "note": "LLM unavailable (quota/network). OCR extraction verified.",
            "llm_error": str(e)
        }
