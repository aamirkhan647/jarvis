"""ResearchAgent: gather company info using research tool."""

from .base_agent import BaseAgent
from tools.tool_registry import get_tool_registry


class ResearchAgent(BaseAgent):
    def __init__(self, memory=None):
        tools = get_tool_registry()
        super().__init__(
            name="ResearchAgent",
            tools={"research_company": tools["research_company"]},
            memory=memory,
        )

    def think_and_act(self, company_name: str):
        self.observe(f"Researching company: {company_name}")
        if not company_name:
            return {}
        return self.act("research_company", company_name=company_name)
