import pytest
import numpy as np
from tools.keyword_matcher import lightweight_score
from tools.resume_parser import parse_resume
from unittest.mock import MagicMock

# --- Test Keyword Matcher (TF-IDF/Cosine Similarity) ---


def test_lightweight_score_perfect_match():
    jd = "Python Django AWS"
    resume = "Python Django AWS"
    # Should be close to 1.0 (perfect match)
    score = lightweight_score(jd, resume)
    assert score > 0.99


def test_lightweight_score_high_match(mock_job_post, mock_resume_text_high_match):
    # Should be relatively high due to shared keywords (Python, AWS, ML)
    score = lightweight_score(
        mock_job_post.raw_description, mock_resume_text_high_match
    )
    assert score >= 0.35


def test_lightweight_score_low_match(mock_job_post, mock_resume_text_low_match):
    # Should be low due to lack of shared keywords
    score = lightweight_score(mock_job_post.raw_description, mock_resume_text_low_match)
    assert score < 0.1


def test_lightweight_score_empty():
    assert lightweight_score("", "some text") == 0.0


# --- Test Resume Parser (Mocking File Upload) ---


def test_parse_resume_mocked_file():
    # Mock the Streamlit uploaded file object
    mock_file = MagicMock()
    mock_file.read.return_value = b"Name: Alice\nSkills: Python, Go\n"

    result = parse_resume(mock_file)
    # Check for basic cleaning (newline removal, stripping)
    assert result == "Name: Alice Skills: Python, Go"


def test_parse_resume_none_input():
    assert parse_resume(None) == ""
