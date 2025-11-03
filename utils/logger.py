"""Centralized logger configuration."""

import logging
from logging import Logger
from config.settings import LOG_LEVEL


def setup_logging():
    level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    logging.basicConfig(
        level=level, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )


def get_logger(name: str) -> Logger:
    return logging.getLogger(name)
