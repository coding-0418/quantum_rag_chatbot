from app.rag.quantum.quantum_utils import swap_test_overlap
from app.workflow.graph import run_query


def test_swap_test_overlap_identical_vectors():
    import numpy as np

    vec = np.array([1.0, 0.0, 0.0, 0.0])
    overlap = swap_test_overlap(vec, vec, shots=512)
    assert overlap > 0.85  # near-1 overlap with shot noise tolerance


def test_swap_test_overlap_orthogonal_vectors():
    import numpy as np

    vec_a = np.array([1.0, 0.0])
    vec_b = np.array([0.0, 1.0])
    overlap = swap_test_overlap(vec_a, vec_b, shots=512)
    assert overlap < 0.3  # near-0 overlap with shot noise tolerance


def test_full_workflow_runs_end_to_end():
    state = run_query("What is NISQ era quantum computing?")
    assert "final_answer" in state
    assert "business_summary" in state
    assert len(state["trace"]) == 6  # planner, retriever, reranker, analyzer, citation, business
