"""Base interface for workflow agents."""

from abc import ABC, abstractmethod

from app.workflow.state import AgentState


class Agent(ABC):
    @abstractmethod
    def run(self, state: AgentState) -> AgentState:
        """Transform workflow state and return the updated state."""