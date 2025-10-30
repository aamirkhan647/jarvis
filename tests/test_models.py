import pytest
from pydantic import ValidationError
from models.job_data import JobPost, Scorecard, ATSScorecard


def test_job_post_creation(mock_job_post):
    assert mock_job_post.title == "Senior Python Developer"
    assert mock_job_post.company == "TechCorp"


def test_scorecard_validation():
    # Test valid creation
    score = Scorecard(
        relevance_score=85,
        rationale="Good match.",
        matching_keywords=["Python", "AWS"],
        gaps_identified=["Kubernetes"],
        is_llm_scored=True,
    )
    assert score.relevance_score == 85

    # Test invalid score value (must be int)
    with pytest.raises(ValidationError):
        Scorecard(
            relevance_score="high",
            rationale="Good match.",
            matching_keywords=[],
            gaps_identified=[],
            is_llm_scored=True,
        )


def test_ats_scorecard_validation():
    ats = ATSScorecard(
        keyword_match_score=90,
        formatting_hygiene=95,
        keyword_density=80,
        ats_pass_confidence=92,
        recommendations_for_fix=["Check dates."],
    )
    assert ats.ats_pass_confidence == 92
