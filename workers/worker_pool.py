"""Simple ThreadPool wrapper for background execution."""

from concurrent.futures import ThreadPoolExecutor, Future
from config.settings import WORKER_POOL_MAX_WORKERS
from utils.logger import get_logger

logger = get_logger(__name__)


class WorkerPool:
    def __init__(self, max_workers: int = WORKER_POOL_MAX_WORKERS):
        self.pool = ThreadPoolExecutor(max_workers=max_workers)

    def submit(self, func, *args, **kwargs) -> Future:
        logger.debug("Submitting task %s to worker pool", func.__name__)
        return self.pool.submit(func, *args, **kwargs)

    def shutdown(self, wait=True):
        self.pool.shutdown(wait=wait)
        logger.info("Worker pool shutdown complete.")
