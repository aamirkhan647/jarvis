import pytest
from unittest.mock import MagicMock, patch
from models.job_data import JobPost, Scorecard, ATSScorecard
from agents.analyzer_agent import AnalyzerAgent
from agents.tailoring_agent import TailoringAgent
from agents.validation_agent import ValidationAgent
from config.settings import settings

# --- Test Analyzer Agent ---


@patch("agents.analyzer_agent.lightweight_score")
def test_analyzer_agent_high_score_triggers_llm(
    mock_lightweight_score, mock_job_post, mock_resume_text_high_match
):
    # Set a score above the configured threshold (e.g., 0.5)
    mock_lightweight_score.return_value = settings.KEYWORD_THRESHOLD + 0.1

    agent = AnalyzerAgent()
    # Mock the internal LLM output logic (since we are not calling OpenAI)
    agent.analyze_job = MagicMock(wraps=agent.analyze_job)

    result = agent.analyze_job(mock_job_post, mock_resume_text_high_match)

    # Check if the mock LLM branch was hypothetically hit (MOCK)
    assert result.is_llm_scored == True
    assert result.relevance_score > (settings.KEYWORD_THRESHOLD * 100)


@patch("agents.analyzer_agent.lightweight_score")
def test_analyzer_agent_low_score_skips_llm(
    mock_lightweight_score, mock_job_post, mock_resume_text_low_match
):
    # Set a score below the configured threshold (e.g., 0.5)
    mock_lightweight_score.return_value = settings.KEYWORD_THRESHOLD - 0.1

    agent = AnalyzerAgent()
    result = agent.analyze_job(mock_job_post, mock_resume_text_low_match)

    # Check that the lightweight scoring path was taken
    assert result.is_llm_scored == False
    assert result.relevance_score < (settings.KEYWORD_THRESHOLD * 100)


# --- Test Tailoring Agent ---


def test_tailoring_agent_generates_text(mock_job_post, mock_resume_text_high_match):
    # NOTE: Since the agent uses a mock implementation, we check for its mock output pattern.
    agent = TailoringAgent()
    tailored_text = agent.tailor_resume(mock_job_post, mock_resume_text_high_match)

    assert "TAILORED RESUME DRAFT" in tailored_text
    assert "TechCorp" in tailored_text  # Check for company personalization


# --- Test Validation Agent ---


def test_validation_agent_returns_ats_score(mock_job_post):
    agent = ValidationAgent()
    mock_tailored_resume = (
        "This resume is perfect and mentions Python and AWS repeatedly."
    )

    result = agent.score_ats(mock_job_post, mock_tailored_resume)

    assert isinstance(result, ATSScorecard)
    assert result.ats_pass_confidence > 45  # Should be a high score based on the mock
