"""Quantum-kernel re-ranking port."""

from collections.abc import Sequence

import numpy as np

from app.rag.quantum.quantum_utils import swap_test_overlap


class QuantumKernelReranker:
    def score(self, query_vector: np.ndarray, candidate_vectors: Sequence[np.ndarray]) -> list[float]:
        return [swap_test_overlap(query_vector, vector) for vector in candidate_vectors]