"""Save/load resume files and generated exports."""

import os
import shutil
from utils.logger import get_logger

logger = get_logger(__name__)
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "user_files")


def save_uploaded(path: str, user_filename: str = None) -> str:
    os.makedirs(BASE_DIR, exist_ok=True)
    name = user_filename or os.path.basename(path)
    dest = os.path.join(BASE_DIR, name)
    shutil.copy2(path, dest)
    logger.info("Saved uploaded file to %s", dest)
    return dest


def save_tailored_resume(text: str, filename: str = "tailored_resume.txt") -> str:
    os.makedirs(BASE_DIR, exist_ok=True)
    dest = os.path.join(BASE_DIR, filename)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(text)
    logger.info("Saved tailored resume to %s", dest)
    return dest
