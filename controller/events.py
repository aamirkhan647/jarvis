"""Event definitions used between GUI and controller."""

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class SearchRequest:
    resume: str
    keywords: str
    location: str
    threshold: float = None


@dataclass
class SearchResults:
    results: list


@dataclass
class TailorRequest:
    resume: str
    job: Dict[str, Any]
