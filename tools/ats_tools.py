"""ATS simulation tools."""

from utils.logger import get_logger

logger = get_logger(__name__)


def simulate_ats(resume, job):
    """
    Minimal ATS simulation:
    - Works with dict or string inputs.
    - Counts overlap between resume text and job keywords.
    - Returns a dict: {"score": int, "notes": list[str]}.
    """

    # Normalize resume text
    resume_text = resume.get("text", "") if isinstance(resume, dict) else str(resume)

    # Extract keywords from job input
    if isinstance(job, dict):
        keywords = job.get("required_skills") or job.get("keywords") or []
        job_text = job.get("text", "")
    else:
        # If job is string, split words and use them as simple keyword list
        job_text = str(job)
        keywords = job_text.split()

    # Clean keywords (deduplicate, lowercase)
    keywords = list({kw.strip().lower() for kw in keywords if kw.strip()})

    # Count keyword matches
    found = [kw for kw in keywords if kw in resume_text.lower()]

    # Compute ATS-like score
    if keywords:
        score = int(round((len(found) / len(keywords)) * 100))
    else:
        score = 50  # default neutral score if no keywords present

    # Prepare notes
    notes = [f"Found keyword: {k}" for k in found] or [
        "No strong keyword matches found"
    ]

    logger.info(
        f"ATS Simulation -> Score: {score}, Found: {len(found)}/{len(keywords)}"
    )
    return {"score": score, "notes": notes}
