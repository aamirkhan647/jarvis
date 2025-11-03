"""Core ATS simulator implementing parsing and scoring heuristics."""

from typing import Dict, List
import re


def extract_keywords_from_job(job: Dict) -> List[str]:
    """Try to get required skills from job fields."""
    kws = job.get("required_skills") or job.get("keywords") or []
    if isinstance(kws, str):
        kws = [k.strip() for k in re.split(r"[,\n;]", kws) if k.strip()]
    return kws


def ats_score(resume_text: str, job: Dict) -> Dict:
    """
    Lightweight ATS scoring:
    - required coverage: 60% weight
    - preferred coverage: 20% weight
    - parse confidence: 20% weight
    """
    required = extract_keywords_from_job(job)
    resume_lower = (resume_text or "").lower()

    if not required:
        # fallback to simple keyword presence
        required_found = []
        score = 50
    else:
        required_found = [k for k in required if k.lower() in resume_lower]
        req_cov = len(required_found) / max(1, len(required))
        score = int(round(req_cov * 100))

    return {"score": score, "found": required_found, "required_total": len(required)}
