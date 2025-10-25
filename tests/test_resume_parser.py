# tests/test_resume_parser.py
import unittest
from core.resume_parser import extract_text


class TestResumeParser(unittest.TestCase):
    def test_extract_text_missing(self):
        with self.assertRaises(FileNotFoundError):
            extract_text("nonexistent_file.pdf")


if __name__ == "__main__":
    unittest.main()
