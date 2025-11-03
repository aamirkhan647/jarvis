"""Definitions of heavy tasks for worker pool."""

from storage.file_store import save_tailored_resume
from utils.logger import get_logger

logger = get_logger(__name__)


def task_save_tailored_resume(tailored: dict, filename: str):
    text = tailored.get("text") if isinstance(tailored, dict) else str(tailored)
    path = save_tailored_resume(text, filename)
    logger.info("Background saved tailored resume to %s", path)
