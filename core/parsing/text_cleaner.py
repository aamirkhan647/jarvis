"""Tiny text cleaning utilities."""

import re
from bs4 import BeautifulSoup


def clean_html_text(html_or_text: str) -> str:
    """Strip HTML and normalize whitespace."""
    if not html_or_text:
        return ""
    # Remove HTML tags if present
    try:
        soup = BeautifulSoup(html_or_text, "html.parser")
        text = soup.get_text(separator="\n")
    except Exception:
        text = html_or_text
    # Normalize whitespace
    text = re.sub(r"\r\n", "\n", text)
    text = re.sub(r"\n{2,}", "\n\n", text)
    return text.strip()
