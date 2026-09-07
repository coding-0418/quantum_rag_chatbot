"""Application service for chat workflow execution."""

from app.workflow.graph import run_query
from app.workflow.state import AgentState


class ChatService:
    async def answer(self, query: str) -> AgentState:
        # The current graph nodes are synchronous; this boundary is async-ready.
        return run_query(query)