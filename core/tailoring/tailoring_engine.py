"""Core tailoring engine that orchestrates rewriting and rule-based edits."""

from typing import Dict
from .rules import reorder_skills_section
from .diff_utils import compute_diff
from utils.logger import get_logger
from tools.llm_tools import llm_call

logger = get_logger(__name__)


def tailor_resume_core(
    resume_struct: Dict, job: Dict, company: Dict = None, level: str = "moderate"
) -> Dict:
    """
    Orchestrate tailoring:
    - Use rules to rearrange skills
    - Prepare a prompt and call an LLM (via llm_call) to reword bullets
    - Return a tailored resume structure with 'text' and diffs
    """
    original_text = (
        resume_struct.get("text", "")
        if isinstance(resume_struct, dict)
        else (resume_struct or "")
    )
    # rule-based change
    sections = (
        resume_struct.get("sections", {}) if isinstance(resume_struct, dict) else {}
    )
    reordered = reorder_skills_section(sections.get("skills", []))
    sections["skills"] = reordered

    # Create a prompt
    job_title = job.get("title", "Target Role")
    company_name = company.get("name") if company else "Company"
    prompt = (
        f"Rewrite the resume to better match the job '{job_title}' at '{company_name}'.\n\n"
        f"Original Resume:\n{original_text}\n\nLevel: {level}\n\n"
        "Return the revised resume text only."
    )
    llm_resp = llm_call(prompt)
    revised_text = llm_resp.get("response", "[LLM stub response]")

    diffs = compute_diff(original_text, revised_text)
    tailored = {"text": revised_text, "sections": sections, "diffs": diffs}
    logger.info("Tailoring complete for job %s at %s", job_title, company_name)
    return tailored
