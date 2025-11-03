"""Controller-level orchestrator: connects GUI to agents & core services."""

from agents.agent_orchestrator import AgentOrchestrator
from utils.logger import get_logger

logger = get_logger(__name__)


class AppOrchestrator:
    """High-level orchestrator used by the GUI. Provides simple sync APIs."""

    def __init__(self):
        self.agent_orch = AgentOrchestrator()
        logger.info("AppOrchestrator initialized.")

    def search_jobs(
        self, resume, keywords: str, location: str, threshold: float = None
    ):
        """Run search -> scoring pipeline and return filtered jobs list."""
        if threshold is None:
            threshold = 60.0
        logger.info("Starting search_jobs pipeline.")
        results = self.agent_orch.run_search_pipeline(
            resume=resume, keywords=keywords, location=location, threshold=threshold
        )
        logger.info("Search pipeline completed with %d results.", len(results))
        return results

    def tailor_resume_for_job(self, resume, job):
        """Run tailoring flow: research, tailor, simulate ATS."""
        logger.info("Starting tailoring pipeline for job %s", job.get("job_id"))
        tailored_resume, ats_score, notes = self.agent_orch.run_tailor_pipeline(
            resume=resume, job=job
        )
        logger.info("Tailoring pipeline completed. ATS score: %s", ats_score)
        return tailored_resume, ats_score, notes
