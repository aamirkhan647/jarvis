"""Tailoring tool: uses LLM stub to produce a tailored resume text."""

from utils.logger import get_logger
from tools.llm_tools import llm_call

logger = get_logger(__name__)


def tailor_resume(
    resume: str, job: dict, company: dict = None, level: str = "moderate"
):
    """Return a tailored resume. This is a stub: it annotates the resume with tailoring notes."""
    job_title = job.get("title", "Unknown Role")
    prompt = f"Tailor the following resume for the job {job_title} at {company.get('name') if company else 'Unknown Company'}.\n\nResume:\n{resume}\n\nLevel: {level}"
    resp = llm_call(prompt)
    return {
        "text": resume + "\n\n[TAILORED NOTES]\n" + resp.get("response"),
        "notes": resp.get("response"),
    }
