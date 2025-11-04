"""Simple JobSearchAgent that wraps a scraping tool."""

from .base_agent import BaseAgent
from tools.tool_registry import get_tool_registry


class JobSearchAgent(BaseAgent):
    def __init__(self, memory=None):
        tools = get_tool_registry()
        super().__init__(
            name="JobSearchAgent",
            tools={"search_jobs": tools["search_jobs"]},
            memory=memory,
        )

    def think_and_act(self, keywords: str, location: str, limit: int = 30):
        self.observe(f"Thinking: search jobs for '{keywords}' in {location}")
        jobs = self.act(
            "search_jobs", keywords=keywords, location=location, limit=limit
        )
        return jobs
