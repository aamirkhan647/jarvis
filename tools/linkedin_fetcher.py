from typing import List
from models.job_data import JobPost


def fetch_jobs(keywords: str, location: str, count: int = 5) -> List[JobPost]:
    """
    MOCK: Simulates calling a LinkedIn scraper or API (Sourcing Agent Tool).
    """

    # Mock data relevant to the "AI Engineer" keyword
    mock_jobs = [
        JobPost(
            title="Senior Python Developer (AI Focus)",
            company="InnovateCorp",
            location="Remote",
            link="http://innovatecorp.com/job1",
            raw_description="Requires 5+ years of Python, strong experience with machine learning, LLMs, and prompt engineering. FastAPI experience preferred. Must be proficient in Kubernetes and cloud deployments (AWS/GCP).",
        ),
        JobPost(
            title="Junior Data Analyst",
            company="DataEntry Inc.",
            location="New York, NY",
            link="http://dataentry.com/job2",
            raw_description="Entry-level position. Focus on Excel and SQL queries. No AI experience necessary. Basic Python knowledge is a plus, but not required.",
        ),
        JobPost(
            title="Agentic AI Engineer",
            company="Future Systems",
            location="Remote",
            link="http://futuresys.com/job3",
            raw_description="Seeking expert in LangChain, multi-agent orchestration, and advanced prompt design. Must have published work in RAG systems or generative AI applications. Experience with vector databases is crucial.",
        ),
    ]
    return mock_jobs[:count]
