"""Deterministic tailoring rules (non-LLM)."""


def reorder_skills_section(skills):
    """Place most technical-looking skills first (naive heuristic)."""
    if not skills:
        return []
    # sort by length (proxy for multi-word skills) and alphabetically
    try:
        return sorted(skills, key=lambda s: (-len(s), s.lower()))
    except Exception:
        return skills
