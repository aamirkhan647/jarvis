# tests/test_tailor.py
import tempfile
import os
from core.tailor import create_docx


def test_create_docx():
    resume = "Sample resume content\nExperience: ...\n"
    jd = "Looking for Python developer with flask and AWS experience."
    tf = tempfile.gettempdir()
    out = os.path.join(tf, "test_tailored.docx")
    create_docx(resume, jd, out, name="Test User")
    assert os.path.exists(out)
