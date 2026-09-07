"""Citation agent: attaches structured, traceable citations to the analysis."""

from app.workflow.state import AgentState


class CitationAgent:
    def run(self, state: AgentState) -> AgentState:
        return cite(state)


def cite(state: AgentState) -> AgentState:
    chunks = state.get("reranked_chunks", [])

    citations = []
    for idx, chunk in enumerate(chunks, start=1):
        citations.append(
            {
                "marker": f"[{idx}]",
                "chunk_id": chunk["chunk_id"],
                "title": chunk["metadata"].get("title", "Unknown source"),
                "source": chunk["metadata"].get("source", ""),
                "classical_score": round(chunk.get("classical_score", 0.0), 4),
                "quantum_score": round(chunk.get("quantum_score", 0.0), 4),
                "final_score": round(chunk.get("final_score", 0.0), 4),
            }
        )

    analysis = state.get("analysis", "")
    footer = "\n\nSources:\n" + "\n".join(
        f"{c['marker']} {c['title']} (score: {c['final_score']})" for c in citations
    )
    state["final_answer"] = analysis + (footer if citations else "")
    state["citations"] = citations
    state.setdefault("trace", []).append({"agent": "citation", "num_citations": len(citations)})
    return state
