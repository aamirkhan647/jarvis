# tests/test_fetcher.py
from core.job_fetcher import RSSFetcher


def test_rss_fetcher_remoteok():
    # This test is best-effort and skips if network unavailable.
    feed = "https://remoteok.com/remote-jobs.rss"
    items = RSSFetcher.fetch(feed, limit=3)
    assert isinstance(items, list)
