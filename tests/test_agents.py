"""Basic smoke tests for agents (very small)."""

from agents.job_search_agent import JobSearchAgent
from agents.memory.memory_manager import MemoryManager


def test_search_agent_smoke():
    mem = MemoryManager()
    agent = JobSearchAgent(memory=mem)
    jobs = agent.think_and_act("Data Scientist", "Remote", limit=2)
    assert isinstance(jobs, list)
    assert len(jobs) >= 0
