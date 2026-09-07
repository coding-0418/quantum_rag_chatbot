"""Lexical BM25 retrieval adapter."""

from rank_bm25 import BM25Okapi

from app.workflow.state import ChunkResult


class BM25Retriever:
    def __init__(self, chunks: list[ChunkResult] | None = None) -> None:
        self._chunks = chunks or []
        self._index = BM25Okapi([chunk.get("content", "").lower().split() for chunk in self._chunks]) if self._chunks else None

    def search(self, query: str, top_k: int = 10) -> list[ChunkResult]:
        if self._index is None:
            return []
        scores = self._index.get_scores(query.lower().split())
        ranked = sorted(zip(scores, self._chunks), key=lambda item: item[0], reverse=True)
        return [{**chunk, "classical_score": float(score)} for score, chunk in ranked[:top_k]]