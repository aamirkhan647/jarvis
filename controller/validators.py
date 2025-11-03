"""Basic input validators for the controller."""

import os


def is_valid_resume_path(path: str) -> bool:
    if not path:
        return False
    return os.path.exists(path)


def sanitize_keywords(keywords: str) -> str:
    return keywords.strip()


def sanitize_location(location: str) -> str:
    return location.strip()
