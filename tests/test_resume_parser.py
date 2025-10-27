# tests/test_resume_parser.py
import unittest
from core.resume_parser import extract_text


class TestResumeParser(unittest.TestCase):
    def test_extract_text_missing(self):
        with self.assertRaises(FileNotFoundError):
            extract_text("nonexistent_file.pdf")

    def test_extract_pdf(self):
        extracted_text = extract_text("data/resumes/Aamir_Khan_Resume.pdf")
        self.assertIn("Aamir M. Khan", extracted_text)


if __name__ == "__main__":
    unittest.main()
