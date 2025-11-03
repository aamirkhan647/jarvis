"""A tiny job queue to submit background tasks for processing."""

from queue import Queue, Empty
from threading import Thread
from utils.logger import get_logger

logger = get_logger(__name__)


class JobQueue:
    def __init__(self):
        self.q = Queue()
        self._running = False
        self.worker = None

    def start(self):
        if self._running:
            return
        self._running = True
        self.worker = Thread(target=self._run_loop, daemon=True)
        self.worker.start()
        logger.info("JobQueue started.")

    def _run_loop(self):
        while self._running:
            try:
                func, args, kwargs = self.q.get(timeout=0.5)
            except Empty:
                continue
            try:
                func(*args, **(kwargs or {}))
            except Exception:
                logger.exception("JobQueue job failed.")
            finally:
                self.q.task_done()

    def stop(self):
        self._running = False
        logger.info("JobQueue stopping.")

    def submit(self, func, *args, **kwargs):
        self.q.put((func, args, kwargs))
