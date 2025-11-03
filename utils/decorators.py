"""Small utility decorators (retry, memoize)."""

import time
import functools
from utils.logger import get_logger

logger = get_logger(__name__)


def retry(times=3, delay=0.5):
    def _decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for i in range(times):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    logger.warning(
                        "Retry %d/%d for %s failed: %s", i + 1, times, fn.__name__, e
                    )
                    time.sleep(delay)
            raise last_exc

        return wrapper

    return _decorator
