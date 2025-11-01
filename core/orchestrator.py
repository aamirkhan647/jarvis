from typing import List, Tuple
from models.job_data import JobPost, Scorecard, ATSScorecard
from tools.linkedin_fetcher import fetch_jobs
from agents.analyzer_agent import AnalyzerAgent
from agents.tailoring_agent import TailoringAgent
from agents.validation_agent import ValidationAgent


class Orchestrator:
    """Manages the overall workflow and sequencing of agents."""

    def __init__(self):
        self.analyzer = AnalyzerAgent()
        self.tailor = TailoringAgent()
        self.validator = ValidationAgent()

    def run_initial_search(
        self, keywords: str, location: str, resume_text: str
    ) -> List[Tuple[JobPost, Scorecard]]:
        """Handles job fetching and initial scoring."""

        # 1. Sourcing Agent Tool (fetch_jobs)
        jobs = fetch_jobs(keywords, location)

        results = []
        for job in jobs:
            # 2. Analyzer Agent
            scorecard = self.analyzer.analyze_job(job, resume_text)
            results.append((job, scorecard))

        return results

    def process_tailoring(
        self, job: JobPost, resume_text: str
    ) -> Tuple[str, ATSScorecard]:
        """Handles tailoring and final ATS validation."""

        # 1. Tailoring Agent
        tailored_resume = self.tailor.tailor_resume(job, resume_text)

        # 2. Validation Agent
        ats_score = self.validator.score_ats(job, tailored_resume)

        return tailored_resume, ats_score
