# src/response_parser.py
import json
from .models import ReviewResult

def parse_response(raw_text: str) -> ReviewResult:
    # Clean up potential markdown formatting
    clean_text = raw_text.replace("```json", "").replace("```", "").strip()
    data = json.loads(clean_text)
    return ReviewResult(**data)