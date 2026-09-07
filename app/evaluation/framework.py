"""Lightweight evaluation contracts for retrieval and answer quality."""

from collections.abc import Callable, Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationCase:
    query: str
    expected_sources: tuple[str, ...] = ()


@dataclass(frozen=True)
class EvaluationResult:
    query: str
    answer: str
    source_recall: float


class EvaluationRunner:
    def __init__(self, answerer: Callable[[str], dict]) -> None:
        self.answerer = answerer

    def run(self, cases: Sequence[EvaluationCase]) -> list[EvaluationResult]:
        results: list[EvaluationResult] = []
        for case in cases:
            response = self.answerer(case.query)
            # TODO: Add answer faithfulness and latency metrics to the report.
            sources = {item.get("source", "") for item in response.get("citations", [])}
            expected = set(case.expected_sources)
            recall = len(sources & expected) / len(expected) if expected else 0.0
            results.append(EvaluationResult(case.query, response.get("answer", ""), recall))
        return results