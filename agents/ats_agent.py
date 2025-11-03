"""ATSAgent: simulate ATS scoring using a tool."""

from .base_agent import BaseAgent
from agents.tools.tool_registry import get_tool_registry


class ATSAgent(BaseAgent):
    def __init__(self, memory=None):
        tools = get_tool_registry()
        super().__init__(
            name="ATSAgent",
            tools={"simulate_ats": tools["simulate_ats"]},
            memory=memory,
        )

    def think_and_act(self, resume, job):
        self.observe("Running ATS simulation")
        return self.act("simulate_ats", resume=resume, job=job)
