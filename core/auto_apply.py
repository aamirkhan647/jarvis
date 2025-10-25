# core/auto_apply.py
"""
Auto-apply module (disabled by default). Contains helper stubs and strong warnings.
If you decide to enable automation, implement site-specific flows and respect Terms of Service.
"""

import logging

logger = logging.getLogger(__name__)


def safe_auto_apply_example(job_link, resume_path, profile):
    """
    This function is intentionally a stub. Do NOT enable automation on 3rd-party sites
    without explicit permission. Use Selenium or APIs responsibly.
    """
    logger.warning(
        "Auto-apply called for %s — function is a stub and does nothing.", job_link
    )
    # Example profile dict fields: name, email, phone, linkedin, portfolio
    return {"status": "skipped", "reason": "auto-apply disabled in default build"}
