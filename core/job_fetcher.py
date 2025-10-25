# core/job_fetcher.py
"""
Modular job fetchers:
- RSSFetcher: fetch jobs from RSS feeds using feedparser.
- SimpleScraper: a minimal best-effort scraper (non-robust).
- AdzunaFetcher: optional (requires API keys) — lightweight wrapper.
"""

from datetime import datetime
import logging
from pathlib import Path
import requests
import feedparser
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class RSSFetcher:
    @staticmethod
    def fetch(feed_url, limit=50):
        jobs = []
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:limit]:
                jobs.append(
                    {
                        "id": entry.get("id") or entry.get("link"),
                        "title": entry.get("title"),
                        "link": entry.get("link"),
                        "company": entry.get("author", "")
                        or entry.get("source", {}).get("title", ""),
                        "date": entry.get("published", ""),
                        "description": entry.get("summary", "")
                        or entry.get("description", ""),
                    }
                )
        except Exception as e:
            logger.exception("RSS fetch failed for %s: %s", feed_url, e)
        return jobs


class AdzunaFetcher:
    BASE = "https://api.adzuna.com/v1/api/jobs"

    def __init__(self, app_id, api_key, country="gb"):
        self.app_id = app_id
        self.api_key = api_key
        self.country = country

    def search(self, what, where="", results_per_page=20):
        if not (self.app_id and self.api_key):
            logger.info("Adzuna keys missing, skipping AdzunaFetcher.")
            return []
        url = f"{self.BASE}/{self.country}/search/1"
        params = {
            "app_id": self.app_id,
            "app_key": self.api_key,
            "what": what,
            "where": where,
            "results_per_page": results_per_page,
        }
        try:
            r = requests.get(url, params=params, timeout=12)
            r.raise_for_status()
            data = r.json()
            out = []
            for item in data.get("results", []):
                out.append(
                    {
                        "id": item.get("id"),
                        "title": item.get("title"),
                        "company": (item.get("company") or {}).get("display_name", ""),
                        "link": item.get("redirect_url"),
                        "date": item.get("created"),
                        "description": item.get("description"),
                    }
                )
            return out
        except Exception as e:
            logger.exception("Adzuna search failed: %s", e)
            return []


class SimpleScraper:
    HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; jarvis-bot/1.0)"}

    @staticmethod
    def fetch_page(url):
        try:
            r = requests.get(url, headers=SimpleScraper.HEADERS, timeout=10)
            r.raise_for_status()
            return r.text
        except Exception as e:
            logger.debug("Page fetch failed: %s", e)
            return ""

    @staticmethod
    def scrape_remoteok(keyword, limit=20):
        # Best-effort scraping of RemoteOK — sites change often
        jobs = []
        try:
            slug = keyword.replace(" ", "-")
            url = f"https://remoteok.com/remote-{slug}-jobs"
            html = SimpleScraper.fetch_page(url)
            if not html:
                return jobs
            soup = BeautifulSoup(html, "html.parser")
            rows = soup.select("tr.job")
            for r in rows[:limit]:
                title_tag = r.select_one("h2")
                company = r.get("data-company") or (
                    r.select_one(".company") and r.select_one(".company").text.strip()
                )
                link = r.get("data-url") or ""
                desc = r.select_one(".description")
                jobs.append(
                    {
                        "id": link,
                        "title": title_tag.text.strip() if title_tag else None,
                        "company": company,
                        "link": (
                            f"https://remoteok.com{link}"
                            if link and link.startswith("/")
                            else link
                        ),
                        "date": "",
                        "description": desc.text.strip() if desc else "",
                    }
                )
        except Exception as e:
            logger.exception("SimpleScraper failed: %s", e)
        return jobs
