import pytest


@pytest.fixture
def sample_resume():
    return "Jane Doe\nSkills: Python, AI, Data Science\nExperience: Microsoft"


@pytest.fixture
def sample_job():
    return "Hiring Data Scientist with Python and AI experience"
