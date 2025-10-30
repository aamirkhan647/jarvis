import pytest
from unittest.mock import MagicMock, patch
from core.orchestrator import Orchestrator
from models.job_data import Scorecard, ATSScorecard
from typing import Tuple


# Patch the external tools and agent classes used by the Orchestrator
@patch("core.orchestrator.fetch_jobs")
@patch("core.orchestrator.AnalyzerAgent")
@patch("core.orchestrator.TailoringAgent")
@patch("core.orchestrator.ValidationAgent")
def test_orchestrator_initial_search(
    MockValidationAgent,
    MockTailoringAgent,
    MockAnalyzerAgent,
    mock_fetch_jobs,
    mock_job_post,
    mock_resume_text_high_match,
):

    # Setup mock Sourcing Agent Tool output
    mock_fetch_jobs.return_value = [mock_job_post]

    # Setup mock Analyzer Agent output
    mock_analyzer_instance = MockAnalyzerAgent.return_value
    mock_scorecard = Scorecard(
        relevance_score=90,
        rationale="Mocked",
        matching_keywords=[],
        gaps_identified=[],
        is_llm_scored=True,
    )
    mock_analyzer_instance.analyze_job.return_value = mock_scorecard

    orchestrator = Orchestrator()
    results = orchestrator.run_initial_search(
        "Python", "Remote", mock_resume_text_high_match
    )

    # Assertions
    mock_fetch_jobs.assert_called_once()
    mock_analyzer_instance.analyze_job.assert_called_once()
    assert len(results) == 1
    assert (
        results[0][1].relevance_score == 90
    )  # Check the scorecard result was processed


@patch("core.orchestrator.TailoringAgent")
@patch("core.orchestrator.ValidationAgent")
def test_orchestrator_process_tailoring(
    MockValidationAgent, MockTailoringAgent, mock_job_post, mock_resume_text_high_match
):

    # Setup mock Tailoring Agent output
    mock_tailor_instance = MockTailoringAgent.return_value
    mock_tailored_resume = "This is the final perfect resume."
    mock_tailor_instance.tailor_resume.return_value = mock_tailored_resume

    # Setup mock Validation Agent output
    mock_validator_instance = MockValidationAgent.return_value
    mock_ats_score = ATSScorecard(
        keyword_match_score=90,
        formatting_hygiene=95,
        keyword_density=80,
        ats_pass_confidence=92,
        recommendations_for_fix=[],
    )
    mock_validator_instance.score_ats.return_value = mock_ats_score

    orchestrator = Orchestrator()
    tailored_resume, ats_score = orchestrator.process_tailoring(
        mock_job_post, mock_resume_text_high_match
    )

    # Assertions
    mock_tailor_instance.tailor_resume.assert_called_once()
    mock_validator_instance.score_ats.assert_called_once()
    assert tailored_resume == mock_tailored_resume
    assert ats_score.ats_pass_confidence == 92
