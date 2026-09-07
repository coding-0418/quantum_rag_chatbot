"""Dependency-injection providers for the application boundary."""

from collections.abc import Generator

from fastapi import Depends

from app.core.config import Settings, get_settings
from app.rag.embeddings_pipeline import EmbeddingPipeline
from app.rag.vector_store import VectorStore


def get_embedding_pipeline(settings: Settings = Depends(get_settings)) -> EmbeddingPipeline:
    """Build the embedding service for a request scope."""
    return EmbeddingPipeline(model_name=settings.embedding_model)


def get_vector_store(settings: Settings = Depends(get_settings)) -> VectorStore:
    """Build the vector-store adapter for a request scope."""
    return VectorStore(index_path=settings.faiss_index_path)


def request_scope() -> Generator[None, None, None]:
    """Provide a future hook for request-scoped resources."""
    yield