import pytest
from models.job_data import JobPost


@pytest.fixture
def mock_job_post():
    """Returns a mock JobPost instance."""
    return JobPost(
        title="Senior Python Developer",
        company="TechCorp",
        location="Remote",
        link="http://techcorp.com/job",
        raw_description="Expert in Python, Django, and AWS. Requires strong machine learning background. 5+ years experience.",
    )


@pytest.fixture
def mock_resume_text_high_match():
    """Returns resume text highly relevant to the mock job."""
    return """
    John Doe - Software Engineer (7 Years Experience)
    Skills: Python (Expert), Django, SQL, AWS, Machine Learning.
    Experience: Developed high-scale Python applications. Led a team.
    """


@pytest.fixture
def mock_resume_text_low_match():
    """Returns resume text with low relevance to the mock job."""
    return """
    Jane Smith - Marketing Specialist
    Skills: SEO, CRM, Adobe Suite, Market Analysis.
    Experience: Managed marketing campaigns for three years.
    """
