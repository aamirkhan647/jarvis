"""Test parsers."""

from core.parsing.resume_parser import parse_resume_text


def test_parse_empty_resume():
    res = parse_resume_text("")
    assert "text" in res
    assert isinstance(res["sections"], dict)


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
