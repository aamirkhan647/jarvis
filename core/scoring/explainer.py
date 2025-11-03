"""Explainability helpers to break down a composite score."""


def explain(resume_text: str, job_text: str) -> dict:
    """
    Return a breakdown dict with sub-scores and human-readable notes.
    Currently uses naive equal splits and similarity approximations.
    """
    # Use simple heuristics for now
    from .similarity_scorer import similarity_score

    skills = similarity_score(resume_text, job_text)
    experience = similarity_score(resume_text, job_text)
    explanation = {
        "skills": int(round(skills * 100)),
        "experience": int(round(experience * 100)),
        "title": 50,
        "education": 50,
        "culture": 30,
        "location": 100,
    }
    explanation["composite"] = int(round(sum(explanation.values()) / len(explanation)))
    explanation["notes"] = [
        "Explanation is heuristic; replace with more detailed parsing."
    ]
    return explanation
