# core/scheduler.py
"""
Optional scheduler to run periodic job searches.
This module provides a simple thread-based scheduler you can plug into the GUI.
"""

import threading
import time
import logging

logger = logging.getLogger(__name__)


class SimpleScheduler:
    def __init__(self, interval_seconds, callback):
        self.interval = interval_seconds
        self.callback = callback
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def start(self):
        logger.info("Starting scheduler with interval %s seconds", self.interval)
        self._thread.start()

    def _run(self):
        while not self._stop.is_set():
            try:
                self.callback()
            except Exception as e:
                logger.exception("Scheduled callback failed: %s", e)
            time.sleep(self.interval)

    def stop(self):
        self._stop.set()
        logger.info("Scheduler stopped.")
