import os
from typing import Optional
from docx import Document
from pypdf import PdfReader, errors as pypdf_errors


def parse_resume(filepath: str) -> Optional[str]:
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
        clean_text = " ".join(content.split()).strip()
        return clean_text

    except pypdf_errors.FileNotDecryptedError:
        return f"Error: PDF file is encrypted and cannot be read."
    except Exception as e:
        # Catch general file-specific errors (e.g., corrupted file)
        return f"Error processing file {filepath}: {type(e).__name__}: {e}"


# Example mock content for testing the agents (unchanged)
def get_mock_resume_text():
    return """
    John Smith - AI Engineer
    Summary: 5 years experience in software development. Strong background in Python.
    Skills: Python, Django, SQL, AWS, some ML concepts.
    Experience: 
      - Developed Python applications for data processing.
      - Worked with large datasets.
      - Led a small team of developers.
    """
