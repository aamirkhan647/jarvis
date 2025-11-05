"""Test parsers."""

from core.parsing.resume_parser import parse_resume


# --- Test Resume Parser (Mocking File Upload) ---


def test_parse_resume_txt_file(tmp_path):

    mock_filepath = tmp_path / "mock_resume.txt"
    file_content = "Name: Alice\nSkills: Python, Go\n"

    with open(mock_filepath, "w", encoding="utf-8") as f:
        f.write(file_content)

    result = parse_resume(str(mock_filepath))
    assert result["text"] == "Name: Alice Skills: Python, Go"


def test_parse_resume_none_input():
    # Since the new parse_resume expects a path, passing None should return None (or handle error)

    assert parse_resume(None) is None


def test_parse_resume_non_existent_file():

    # The function should handle a path that doesn't exist
    result = parse_resume("/this/path/does/not/exist.txt")
    assert result is None or "Error" in result  # Depending on final error handling


# import pytest
# from tools import resume_tools


# def test_extract_skills_and_summary():
#     """
#     Ensure resume parsing extracts basic data fields.
#     """
#     fake_resume = "John Doe\nSkills: Python, ML, Data Science\nExperience: Google"
#     result = resume_tools.extract_resume_data(fake_resume)

#     assert isinstance(result, dict)
#     assert "skills" in result
#     assert "experience" in result


# def test_calculate_similarity_scores(monkeypatch):
#     """
#     Verify resume-job similarity score calculation is numeric.
#     """
#     monkeypatch.setattr(resume_tools, "embed_texts", lambda x: [[0.5, 0.5]] * len(x))
#     score = resume_tools.calculate_similarity(
#         "data science engineer", "data scientist job"
#     )
#     assert 0 <= score <= 1
