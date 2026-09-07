"""Quantum Re-ranker agent: refines retrieval scores using a swap-test overlap circuit."""

from app.rag.embeddings import embed_query
from app.rag.quantum.quantum_utils import quantum_rerank_score
from app.workflow.state import AgentState


class QuantumRerankerAgent:
    def run(self, state: AgentState) -> AgentState:
        return rerank(state)


def rerank(state: AgentState, top_n: int = 5) -> AgentState:
    query_vector = embed_query(state["query"])
    candidates = state.get("retrieved_chunks", [])

    reranked = []
    for chunk in candidates:
        chunk_vector = chunk["metadata"].get("embedding")
        if chunk_vector is None:
            final_score = chunk["classical_score"]
            quantum_score = 0.0
        else:
            quantum_score = quantum_rerank_score(query_vector, chunk_vector, chunk["classical_score"])
            final_score = quantum_score
        reranked.append({**chunk, "quantum_score": quantum_score, "final_score": final_score})

    reranked.sort(key=lambda c: c["final_score"], reverse=True)
    state["reranked_chunks"] = reranked[:top_n]
    state.setdefault("trace", []).append(
        {"agent": "quantum_reranker", "top_n": top_n, "backend": "aer_simulator"}
    )
    return state
