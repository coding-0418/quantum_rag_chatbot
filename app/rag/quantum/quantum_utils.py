"""Quantum re-ranking utilities.

Implements a swap-test-based similarity estimator on top of Qiskit + Aer.
Two classical embedding vectors are amplitude-encoded into `n_qubits` each,
then a swap test estimates their overlap |<q|c>|^2. This overlap is combined
with the classical cosine score to produce a re-ranked relevance score.

This is a genuine (if small-scale) quantum subroutine, not a metaphor: it
runs on a real quantum simulator backend and its shot-noise is what you'd
see on hardware for the same circuit depth.
"""

import math

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

from app.core.config import get_settings


def _next_power_of_two(n: int) -> int:
    return 1 << (n - 1).bit_length()


def _amplitude_encode(vector: np.ndarray, n_qubits: int) -> np.ndarray:
    size = 2**n_qubits
    padded = np.zeros(size, dtype="float64")
    padded[: len(vector)] = vector[:size]
    norm = np.linalg.norm(padded)
    if norm == 0:
        padded[0] = 1.0
        return padded
    return padded / norm


def swap_test_overlap(vec_a: np.ndarray, vec_b: np.ndarray, shots: int | None = None) -> float:
    """Estimate |<a|b>|^2 via a swap test circuit run on the Aer simulator."""
    settings = get_settings()
    shots = shots or settings.quantum_shots

    n_features = max(len(vec_a), len(vec_b))
    n_qubits = max(1, math.ceil(math.log2(_next_power_of_two(n_features))))

    state_a = _amplitude_encode(np.asarray(vec_a, dtype="float64"), n_qubits)
    state_b = _amplitude_encode(np.asarray(vec_b, dtype="float64"), n_qubits)

    ancilla = 1
    qc = QuantumCircuit(1 + 2 * n_qubits, 1)
    reg_a = range(ancilla, ancilla + n_qubits)
    reg_b = range(ancilla + n_qubits, ancilla + 2 * n_qubits)

    qc.initialize(state_a, list(reg_a))
    qc.initialize(state_b, list(reg_b))

    qc.h(0)
    for qa, qb in zip(reg_a, reg_b):
        qc.cswap(0, qa, qb)
    qc.h(0)
    qc.measure(0, 0)

    backend = AerSimulator()
    compiled = transpile(qc, backend)
    result = backend.run(compiled, shots=shots).result()
    counts = result.get_counts()

    p0 = counts.get("0", 0) / shots
    overlap = max(0.0, 2 * p0 - 1)
    return overlap


def quantum_rerank_score(
    query_vector: np.ndarray, chunk_vector: np.ndarray, classical_score: float, alpha: float = 0.5
) -> float:
    """Blend classical cosine similarity with quantum swap-test overlap."""
    quantum_overlap = swap_test_overlap(query_vector, chunk_vector)
    return alpha * classical_score + (1 - alpha) * quantum_overlap
