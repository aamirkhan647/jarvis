"""TailoringAgent: uses tailoring tool to create a tailored resume."""

from .base_agent import BaseAgent
from agents.tools.tool_registry import get_tool_registry


class TailoringAgent(BaseAgent):
    def __init__(self, memory=None):
        tools = get_tool_registry()
        super().__init__(
            name="TailoringAgent",
            tools={
                "tailor_resume": tools["tailor_resume"],
                "llm_call": tools["llm_call"],
            },
            memory=memory,
        )

    def think_and_act(self, resume, job, company=None, level="moderate"):
        self.observe(f"Tailoring resume for job {job.get('job_id')}")
        tailored = self.act(
            "tailor_resume", resume=resume, job=job, company=company, level=level
        )
        return tailored
