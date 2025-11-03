"""Core researcher that aggregates company info (stub)."""

from .summarizer import simple_summarize
from .sentiment_analyzer import analyze_sentiment


def company_profile_from_job(job: dict) -> dict:
    """
    Build a profile from job data and (optionally) external scraping.
    This is a stub that uses job fields and simple heuristics.
    """
    name = job.get("company") or "Unknown"
    description = f"{name} — {job.get('title', '')} role"
    summary = simple_summarize(description)
    sentiment = analyze_sentiment(description)
    return {
        "name": name,
        "description": description,
        "summary": summary,
        "sentiment": sentiment,
        "keywords": ["python", "ml"],  # placeholder
    }
