"""Dependency inversion ports used by application services."""

from typing import Protocol, Sequence

import numpy as np

from app.workflow.state import ChunkResult


class Embedder(Protocol):
    def embed(self, texts: Sequence[str]) -> np.ndarray: ...


class Retriever(Protocol):
    def search(self, query: str, top_k: int = 10) -> list[ChunkResult]: ...


class DocumentRepository(Protocol):
    async def save(self, title: str, source: str, content: str) -> str: ...