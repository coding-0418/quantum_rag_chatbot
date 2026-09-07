import os
import pickle
from dataclasses import dataclass

import faiss
import numpy as np

from app.core.config import get_settings


@dataclass
class RetrievedChunk:
    chunk_id: str
    content: str
    metadata: dict
    score: float


class FaissVectorStore:
    """Wraps a FAISS flat inner-product index plus a sidecar metadata store."""

    def __init__(self, dim: int, index_path: str | None = None):
        self.dim = dim
        settings = get_settings()
        self.index_path = index_path or settings.faiss_index_path
        self.meta_path = self.index_path + ".meta.pkl"
        self.index = faiss.IndexIDMap2(faiss.IndexFlatIP(dim))
        self._metadata: dict[int, dict] = {}
        self._next_id = 0
        self._load_if_exists()

    def _load_if_exists(self) -> None:
        if os.path.exists(self.index_path) and os.path.exists(self.meta_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.meta_path, "rb") as f:
                data = pickle.load(f)
                self._metadata = data["metadata"]
                self._next_id = data["next_id"]

    def save(self) -> None:
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "wb") as f:
            pickle.dump({"metadata": self._metadata, "next_id": self._next_id}, f)

    def add(self, vectors: np.ndarray, metadatas: list[dict]) -> list[int]:
        ids = np.arange(self._next_id, self._next_id + len(metadatas), dtype="int64")
        self.index.add_with_ids(vectors, ids)
        for vec_id, meta in zip(ids, metadatas):
            self._metadata[int(vec_id)] = meta
        self._next_id += len(metadatas)
        return ids.tolist()

    def search(self, query_vector: np.ndarray, top_k: int = 10) -> list[RetrievedChunk]:
        if self.index.ntotal == 0:
            return []
        scores, ids = self.index.search(query_vector.reshape(1, -1), top_k)
        results = []
        for score, vec_id in zip(scores[0], ids[0]):
            if vec_id == -1:
                continue
            meta = self._metadata.get(int(vec_id), {})
            results.append(
                RetrievedChunk(
                    chunk_id=meta.get("chunk_id", str(vec_id)),
                    content=meta.get("content", ""),
                    metadata=meta,
                    score=float(score),
                )
            )
        return results
