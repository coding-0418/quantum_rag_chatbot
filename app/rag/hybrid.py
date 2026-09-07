"""Hybrid dense and lexical retrieval orchestration."""

from app.domain.ports import Retriever
from app.workflow.state import ChunkResult


class HybridRetriever:
    def __init__(self, dense: Retriever, lexical: Retriever) -> None:
        self.dense = dense
        self.lexical = lexical

    def search(self, query: str, top_k: int = 10) -> list[ChunkResult]:
        merged: dict[str, ChunkResult] = {}
        for chunk in [*self.dense.search(query, top_k), *self.lexical.search(query, top_k)]:
            key = chunk.get("chunk_id", chunk.get("content", ""))
            current = merged.get(key)
            if current is None or chunk.get("classical_score", 0.0) > current.get("classical_score", 0.0):
                merged[key] = chunk
        return sorted(merged.values(), key=lambda item: item.get("classical_score", 0.0), reverse=True)[:top_k]