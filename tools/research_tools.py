"""Company research tool stub."""

from utils.logger import get_logger

logger = get_logger(__name__)


def research_company(company_name: str):
    """
    Return a minimal company profile structure.
    Replace with actual web scraping or APIs (Crunchbase, LinkedIn).
    """
    logger.info("research_company stub called for %s", company_name)
    return {
        "name": company_name,
        "size": "50-200",
        "industry": "Software",
        "description": f"{company_name} builds software products.",
        "keywords": ["python", "nlp", "ml"],
    }
