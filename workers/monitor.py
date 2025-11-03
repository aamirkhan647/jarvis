"""Monitoring helpers for background workers."""

import time
from utils.logger import get_logger

logger = get_logger(__name__)


def watch_worker_pool(pool, interval=5):
    """Periodically log thread pool status (best-effort)."""
    while True:
        try:
            logger.debug("Worker pool status: %s", getattr(pool, "pool", None))
        except Exception:
            pass
        time.sleep(interval)
