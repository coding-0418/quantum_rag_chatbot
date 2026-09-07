from typing import Any, TypedDict


class ChunkResult(TypedDict, total=False):
    chunk_id: str
    content: str
    metadata: dict
    classical_score: float
    quantum_score: float
    final_score: float


class AgentState(TypedDict, total=False):
    query: str
    plan: list[str]
    sub_queries: list[str]
    retrieved_chunks: list[ChunkResult]
    reranked_chunks: list[ChunkResult]
    analysis: str
    citations: list[dict[str, Any]]
    business_summary: str
    final_answer: str
    trace: list[dict[str, Any]]
