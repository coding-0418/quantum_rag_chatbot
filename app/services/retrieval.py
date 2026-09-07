"""Application service for dense knowledge-base retrieval."""

from dataclasses import dataclass

from app.rag.embeddings import embed_query
from app.rag.vector_store import FaissVectorStore, RetrievedChunk


@dataclass
class RetrievalService:
    """Coordinate query embedding and FAISS search."""

    top_k: int = 8
    store: FaissVectorStore | None = None

    def search(self, query: str, top_k: int | None = None) -> list[RetrievedChunk]:
        if not query.strip():
            return []
        vector = embed_query(query)
        if self.store is None:
            raise RuntimeError("RetrievalService requires a vector store")
        return self.store.search(vector, top_k or self.top_k)
