"""Wrappers for parsing logic that call core parsing functions."""

from core.parsing.resume_parser import parse_resume
from utils.logger import get_logger

logger = get_logger(__name__)


def parse_resume(resume_file: str):
    """
    Accepts a path to a resume file (pdf/docx/txt) or raw text,
    returns parsed structure: {'text': ..., 'sections': {...}}
    """
    logger.info("parse_resume called for %s", resume_file)
    return parse_resume(resume_file)
