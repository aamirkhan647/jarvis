"""Compute a composite job match score from sub-scores."""

from config.constants import DEFAULT_SCORING_WEIGHTS
from .similarity_scorer import similarity_score


def composite_score(resume_text: str, job_text: str, weights: dict = None) -> int:
    """
    Compute a composite integer score (0..100).
    For now mostly uses similarity on the whole text as the 'skills' and 'experience' proxies.
    """
    w = weights or DEFAULT_SCORING_WEIGHTS
    # approximate sub-scores using same similarity metric on whole text
    skills = similarity_score(resume_text, job_text)
    experience = similarity_score(resume_text, job_text)
    title = 1.0 if True else 0.0  # placeholder for title match
    education = 0.5  # placeholder
    culture = 0.3
    location = 1.0

    composite = (
        skills * w["skills"]
        + experience * w["experience"]
        + title * w["title"]
        + education * w["education"]
        + culture * w["culture"]
        + location * w["location"]
    )
    return int(round(composite * 100))
