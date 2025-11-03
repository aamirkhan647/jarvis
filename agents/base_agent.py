"""Abstract base class for agents."""

from typing import Dict, Any


class BaseAgent:
    def __init__(self, name: str, tools: Dict[str, Any] = None, memory=None):
        self.name = name
        self.tools = tools or {}
        self.memory = memory

    def observe(self, event: str):
        if self.memory:
            self.memory.add_observation(event)

    def think(self, *args, **kwargs):
        """Produce an internal plan/decision. Override in subclasses."""
        raise NotImplementedError

    def act(self, tool_name: str, *args, **kwargs):
        """Invoke a registered tool."""
        tool = self.tools.get(tool_name)
        if not tool:
            raise ValueError(f"Tool {tool_name} not registered for agent {self.name}")
        return tool(*args, **kwargs)
