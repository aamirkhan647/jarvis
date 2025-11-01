from models.job_data import Scorecard, JobPost
from tools.keyword_matcher import lightweight_score
from config.settings import settings
from agents.base_agent import BaseAgent


# MOCK IMPLEMENTATION of the LLM call
class AnalyzerAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        # self.parser = self.get_parser(Scorecard) # Uncomment for real LLM usage

    def analyze_job(self, job: JobPost, resume_text: str) -> Scorecard:
        """
        1. Performs lightweight keyword score.
        2. If above threshold, simulates deep LLM analysis.
        """

        # --- Step 1: Lightweight Scoring (Tool usage) ---
        keyword_sim = lightweight_score(job.raw_description, resume_text)
        initial_score = int(keyword_sim * 100)

        if initial_score < settings.KEYWORD_THRESHOLD * 100:
            return Scorecard(
                relevance_score=initial_score,
                rationale="Basic keyword similarity was too low. Resume lacks critical domain terms.",
                matching_keywords=[],
                gaps_identified=["Primary skill deficiency."],
                is_llm_scored=False,
            )

        # --- Step 2: Deep LLM Analysis (MOCK) ---
        # If the score is high enough, we assume the LLM would validate and refine it.
        # In a real scenario, the prompt would enforce the Scorecard Pydantic schema.

        if job.title == "Agentic AI Engineer":
            return Scorecard(
                relevance_score=90,
                rationale="Outstanding alignment. Direct match on 'Python' and general AI experience, though 'LangChain' needs explicit mention.",
                matching_keywords=["Python", "AI", "machine learning"],
                gaps_identified=["LangChain", "vector databases"],
                is_llm_scored=True,
            )
        else:
            return Scorecard(
                relevance_score=initial_score,
                rationale="Decent overlap, but job focus is SQL/Excel, not AI expertise.",
                matching_keywords=["Python", "SQL"],
                gaps_identified=["Advanced data analysis methodologies."],
                is_llm_scored=True,
            )
