"""Top-level orchestrator that coordinates specialized agents."""

from agents.base_agent import BaseAgent
from agents.job_search_agent import JobSearchAgent
from agents.scoring_agent import ScoringAgent
from agents.research_agent import ResearchAgent
from agents.tailoring_agent import TailoringAgent
from agents.ats_agent import ATSAgent
from agents.memory.memory_manager import MemoryManager
from utils.logger import get_logger

logger = get_logger(__name__)


class AgentOrchestrator:
    def __init__(self):
        # Initialize memory subsystem
        self.memory = MemoryManager()
        # Initialize agents with the memory and their tools
        self.search_agent = JobSearchAgent(memory=self.memory)
        self.scoring_agent = ScoringAgent(memory=self.memory)
        self.research_agent = ResearchAgent(memory=self.memory)
        self.tailoring_agent = TailoringAgent(memory=self.memory)
        self.ats_agent = ATSAgent(memory=self.memory)
        logger.info("AgentOrchestrator initialized with agents.")

    def run_search_pipeline(
        self, resume, keywords: str, location: str, threshold: float
    ):
        """Search jobs, score them and return filtered results >= threshold."""
        jobs = self.search_agent.think_and_act(keywords=keywords, location=location)
        scored = self.scoring_agent.think_and_act(resume=resume, jobs=jobs)
        filtered = [j for j in scored if j.get("score", 0) >= threshold]
        # Save to memory an observation
        self.memory.add_observation(
            f"Search returned {len(jobs)} jobs, {len(filtered)} above threshold {threshold}"
        )
        return filtered

    def run_tailor_pipeline(self, resume, job):
        """Research company, tailor resume, and run ATS simulation."""
        company_info = self.research_agent.think_and_act(
            company_name=job.get("company")
        )
        tailored = self.tailoring_agent.think_and_act(
            resume=resume, job=job, company=company_info
        )
        ats_result = self.ats_agent.think_and_act(resume=tailored, job=job)
        # Return tailored resume, ATS score and notes
        return tailored, ats_result.get("score", 0), ats_result.get("notes", [])
