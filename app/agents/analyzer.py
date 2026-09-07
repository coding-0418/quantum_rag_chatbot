"""Analyzer agent: synthesizes the reranked evidence into a coherent answer draft."""

from app.workflow.state import AgentState


class AnalysisAgent:
    def run(self, state: AgentState) -> AgentState:
        return analyze(state)


def analyze(state: AgentState) -> AgentState:
    chunks = state.get("reranked_chunks", [])

    if not chunks:
        state["analysis"] = (
            "No supporting evidence was found in the knowledge base for this query."
        )
        state.setdefault("trace", []).append({"agent": "analyzer", "num_sources": 0})
        return state

    bullet_points = []
    for chunk in chunks:
        title = chunk["metadata"].get("title", "Unknown source")
        snippet = chunk["content"][:280].strip()
        bullet_points.append(f"- ({title}) {snippet}")

    state["analysis"] = (
        f"Synthesis for query: '{state['query']}'\n\n" + "\n".join(bullet_points)
    )
    state.setdefault("trace", []).append({"agent": "analyzer", "num_sources": len(chunks)})
    return state
