"""Basic job posting parser to normalize job text and extract fields."""

from typing import Dict
from .text_cleaner import clean_html_text


def parse_job(raw_text: str, source_meta: Dict = None) -> Dict:
    """
    Normalize job posting text into structured fields.
    Very lightweight: looks for 'Responsibilities' and 'Qualifications' markers.
    """
    source_meta = source_meta or {}
    text = clean_html_text(raw_text or "")
    lower = text.lower()
    responsibilities = ""
    qualifications = ""
    # naive split heuristics
    if "responsibilities" in lower:
        idx = lower.find("responsibilities")
        responsibilities = text[idx : idx + 800]
    if "qualifications" in lower:
        idx = lower.find("qualifications")
        qualifications = text[idx : idx + 800]
    return {
        "title": source_meta.get("title", ""),
        "company": source_meta.get("company", ""),
        "location": source_meta.get("location", ""),
        "description": text,
        "responsibilities": responsibilities,
        "qualifications": qualifications,
        "raw": raw_text,
    }
