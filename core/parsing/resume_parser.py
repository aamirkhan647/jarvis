"""Simple resume parser stub. Replace PDF/DOCX extraction with real logic."""

import os
from typing import Optional, Dict
from utils.logger import get_logger
from docx import Document
from pypdf import PdfReader, errors as pypdf_errors


logger = get_logger(__name__)


def parse_resume(filepath: str) -> Dict:
    """
    Parses a resume file from a path (TXT, DOCX, PDF) into clean text.
    Returns the clean text string or an error message string.
    """
    if not filepath or not os.path.exists(filepath):
        return None

    _, ext = os.path.splitext(filepath)
    ext = ext.lower()

    content = ""

    try:
        if ext == ".txt" or ext == ".md":
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

        elif ext == ".docx":
            # DOCX Parsing (Requires python-docx)
            document = Document(filepath)
            paragraphs = [p.text for p in document.paragraphs]
            content = "\n".join(paragraphs)

        elif ext == ".pdf":
            # PDF Parsing (Requires pypdf)
            reader = PdfReader(filepath)

            # Extract text page by page
            for page in reader.pages:
                content += page.extract_text() + "\n"

        else:
            return f"Error: File type {ext} is not supported (only TXT, MD, DOCX, PDF)."

        # --- Text Cleaning and Normalization ---

        # Remove extra whitespace and normalize line breaks
        if not content:
            return "Error: File content was empty after parsing."

        # Replace common symbols that occur during parsing (e.g., non-breaking spaces)
        content = content.replace("\u200b", " ").replace("\xa0", " ")

        # Clean and normalize the extracted text: Replace all consecutive whitespace with a single space
        text = " ".join(content.split()).strip()

    except pypdf_errors.FileNotDecryptedError:
        return f"Error: PDF file is encrypted and cannot be read."
    except Exception as e:
        # Catch general file-specific errors (e.g., corrupted file)
        return f"Error processing file {filepath}: {type(e).__name__}: {e}"

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
