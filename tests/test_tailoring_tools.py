"""Tailoring engine smoke test."""

from core.tailoring.tailoring_engine import tailor_resume_core


def test_tailor_core():
    resume = {
        "text": "Experienced data engineer with Python.",
        "sections": {"skills": ["python", "sql"]},
    }
    job = {"title": "Data Engineer", "company": "ACME"}
    tailored = tailor_resume_core(resume, job)
    assert "text" in tailored
    assert "diffs" in tailored


# import pytest
# from unittest.mock import patch, MagicMock
# from jobtailor.agents.tools import tailoring_tools

# @patch("jobtailor.agents.tools.tailoring_tools.llm_call")
# def test_tailor_resume_with_mock_llm(mock_llm):
#     """
#     Ensure tailoring returns a valid resume structure.
#     """
#     mock_llm.return_value = {"response": "Tailored resume for data science job.", "model": "gpt-4o-mini"}

#     tailored = tailoring_tools.tailor_resume("base resume text", "ML Engineer job", {"name": "OpenAI"})
#     assert "Tailored" in tailored
#     assert mock_llm.called
