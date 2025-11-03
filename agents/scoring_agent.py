"""ScoringAgent: scores jobs using embedding tools and composite scorer."""

from .base_agent import BaseAgent
from agents.tools.tool_registry import get_tool_registry


class ScoringAgent(BaseAgent):
    def __init__(self, memory=None):
        tools = get_tool_registry()
        super().__init__(
            name="ScoringAgent",
            tools={
                "embed_text": tools["embed_text"],
                "score_similarity": tools["score_similarity"],
                "parse_resume": tools["parse_resume"],
            },
            memory=memory,
        )

    def think_and_act(self, resume, jobs: list):
        # Parse resume to get textual representation
        resume_struct = (
            self.act("parse_resume", resume_file=resume) if resume else {"text": ""}
        )
        resume_text = resume_struct.get("text", "")
        results = []
        for job in jobs:
            job_text = job.get("description", "") or job.get("raw", "")
            score = self.act("score_similarity", a=resume_text, b=job_text)
            job_copy = job.copy()
            job_copy["score"] = score
            results.append(job_copy)
        return results
