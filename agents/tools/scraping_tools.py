"""Minimal scraping tools. Replace with real connectors for Indeed/LinkedIn/etc."""

from utils.logger import get_logger

logger = get_logger(__name__)


def search_jobs(keywords: str, location: str, limit: int = 30):
    """
    Stub search function that returns mock job entries.
    Replace with calls to APIs or scraping code.
    """
    logger.info(
        "search_jobs stub called with keywords=%s location=%s", keywords, location
    )
    sample = {
        "job_id": "mock_1",
        "title": f"{keywords} Engineer",
        "company": "ExampleCorp",
        "location": location,
        "posted_date": "2025-10-01",
        "description": "We are looking for an engineer with skills in Python, NLP and ML.",
        "url": "https://example.com/job/mock_1",
    }
    return [sample] * min(limit, 10)
