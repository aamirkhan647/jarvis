# core/resume_parser.py
"""
Utilities to extract plain text from common resume formats.
Supports: PDF (pdfplumber), DOCX (docx2txt), and plain text.
"""

from pathlib import Path
import logging

try:
    import pdfplumber
except Exception:
    pdfplumber = None

try:
    import docx2txt
except Exception:
    docx2txt = None

logger = logging.getLogger(__name__)


def extract_text(path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)
    suf = path.suffix.lower()
    if suf == ".pdf":
        return extract_from_pdf(path)
    if suf in (".doc", ".docx"):
        return extract_from_docx(path)
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        logger.exception("Failed to read resume as plain text: %s", e)
        return ""


def extract_from_pdf(path):
    if not pdfplumber:
        logger.warning("pdfplumber not installed; PDF extraction will be limited.")
        return ""
    text_parts = []
    try:
        with pdfplumber.open(str(path)) as pdf:
            for p in pdf.pages:
                t = p.extract_text()
                if t:
                    text_parts.append(t)
    except Exception as e:
        logger.exception("PDF extraction error: %s", e)
    return "\n\n".join(text_parts)


def extract_from_docx(path):
    if not docx2txt:
        logger.warning("docx2txt not installed; DOCX extraction will be limited.")
        return ""
    try:
        return docx2txt.process(str(path)) or ""
    except Exception as e:
        logger.exception("DOCX extraction error: %s", e)
        return ""
