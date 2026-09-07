import pickle
from dataclasses import dataclass
from pathlib import Path

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
        if Path(self.index_path).exists() and Path(self.meta_path).exists():
            self.index = faiss.read_index(self.index_path)
            if self.index.d != self.dim:
                raise ValueError(
                    f"FAISS index dimension {self.index.d} does not match requested dimension {self.dim}"
                )
            with open(self.meta_path, "rb") as f:
                data = pickle.load(f)
                self._metadata = data["metadata"]
                self._next_id = data["next_id"]

    def save(self) -> None:
        index_path = Path(self.index_path)
        index_path.parent.mkdir(parents=True, exist_ok=True)
        temporary_index = index_path.with_suffix(index_path.suffix + ".tmp")
        temporary_meta = Path(self.meta_path).with_suffix(".tmp")
        faiss.write_index(self.index, str(temporary_index))
        with temporary_meta.open("wb") as f:
            pickle.dump({"metadata": self._metadata, "next_id": self._next_id}, f)
        temporary_index.replace(index_path)
        temporary_meta.replace(self.meta_path)

    def add(self, vectors: np.ndarray, metadatas: list[dict]) -> list[int]:
        if vectors.ndim != 2 or vectors.shape[1] != self.dim:
            raise ValueError(f"Expected vectors with shape (n, {self.dim}), got {vectors.shape}")
        if len(vectors) != len(metadatas):
            raise ValueError("Each vector must have one metadata record")
        if not len(metadatas):
            return []
        vectors = np.asarray(vectors, dtype="float32")
        ids = np.arange(self._next_id, self._next_id + len(metadatas), dtype="int64")
        self.index.add_with_ids(vectors, ids)
        for vec_id, meta in zip(ids, metadatas):
            self._metadata[int(vec_id)] = meta
        self._next_id += len(metadatas)
        return ids.tolist()

    def search(self, query_vector: np.ndarray, top_k: int = 10) -> list[RetrievedChunk]:
        if self.index.ntotal == 0 or top_k <= 0:
            return []
        query_vector = np.asarray(query_vector, dtype="float32").reshape(1, -1)
        if query_vector.shape[1] != self.dim:
            raise ValueError(f"Expected query vector dimension {self.dim}, got {query_vector.shape[1]}")
        scores, ids = self.index.search(query_vector, min(top_k, self.index.ntotal))
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


class VectorStore:
    """Configuration-first vector store facade for dependency injection."""

    def __init__(self, index_path: str | None = None) -> None:
        self.index_path = index_path

    def open(self, dim: int = 384) -> FaissVectorStore:
        return FaissVectorStore(dim=dim, index_path=self.index_path)
