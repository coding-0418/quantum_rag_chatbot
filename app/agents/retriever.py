"""Retriever agent: dense vector search over the FAISS knowledge base."""

from app.rag.vector_store import FaissVectorStore
from app.services.retrieval import RetrievalService
from app.workflow.state import AgentState, ChunkResult

_store: FaissVectorStore | None = None


class RetrieverAgent:
    def run(self, state: AgentState) -> AgentState:
        return retrieve(state)


def get_store(dim: int = 384) -> FaissVectorStore:
    global _store
    if _store is None:
        _store = FaissVectorStore(dim=dim)
    return _store


def retrieve(state: AgentState, top_k: int = 8) -> AgentState:
    seen: dict[str, ChunkResult] = {}
    retrieval_service = RetrievalService(top_k=top_k, store=get_store())

    for sub_query in state.get("sub_queries", [state["query"]]):
        for hit in retrieval_service.search(sub_query):
            existing = seen.get(hit.chunk_id)
            if existing is None or hit.score > existing["classical_score"]:
                seen[hit.chunk_id] = ChunkResult(
                    chunk_id=hit.chunk_id,
                    content=hit.content,
                    metadata=hit.metadata,
                    classical_score=hit.score,
                )

    ranked = sorted(seen.values(), key=lambda c: c["classical_score"], reverse=True)
    state["retrieved_chunks"] = ranked[: top_k * 2]
    state.setdefault("trace", []).append(
        {"agent": "retriever", "num_candidates": len(state["retrieved_chunks"])}
    )
    return state
