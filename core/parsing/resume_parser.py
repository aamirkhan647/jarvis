"""Simple resume parser stub. Replace PDF/DOCX extraction with real logic."""

from typing import Dict
from utils.logger import get_logger
import os

logger = get_logger(__name__)


def parse_resume_text(resume_file: str) -> Dict:
    """
    Minimal implementation:
    - If resume_file is a path and file exists, read it as text (txt only).
    - If not a file, treat resume_file as raw text.
    Returns a dict with keys: text, sections.
    """
    text = ""
    if resume_file and os.path.exists(resume_file):
        try:
            with open(resume_file, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception:
            logger.exception("Failed to read resume file as text.")
            text = ""
    else:
        # Accept raw text
        text = resume_file or ""

    # Very naive heuristics to create sections
    sections = {"summary": "", "experience": [], "skills": [], "education": []}
    # Try to extract a skills line
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for ln in lines[:10]:
        if "skills" in ln.lower():
            # next line might be the skills
            idx = lines.index(ln)
            if idx + 1 < len(lines):
                sections["skills"] = [s.strip() for s in lines[idx + 1].split(",")]
            break

    return {"text": text, "sections": sections}
