import pytest
from tools.ats_tools import simulate_ats


@pytest.mark.parametrize(
    "resume,job",
    [
        ("Python, Machine Learning, APIs", "Looking for a Python ML engineer"),
        ("Java, Spring Boot", "Python developer needed"),
        ("", ""),
    ],
)
def test_ats_score_calculation(resume, job):
    """
    Ensure ATS score dict returns valid structure.
    """
    result = simulate_ats(resume, job)

    # Structure checks
    assert isinstance(result, dict)
    assert "score" in result
    assert "notes" in result
    assert isinstance(result["score"], int)
    assert isinstance(result["notes"], list)
    assert 0 <= result["score"] <= 100
