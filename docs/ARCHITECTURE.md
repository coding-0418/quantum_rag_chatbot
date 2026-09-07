# Architecture

## Overview

The system is a multi-agent Retrieval-Augmented Generation (RAG) pipeline
orchestrated with LangGraph, exposed via a FastAPI backend, with a Streamlit
chat frontend. A quantum swap-test circuit (Qiskit + Aer) re-scores the
retrieved candidates alongside classical cosine similarity.

```
                    ┌─────────────┐
                    │  Streamlit  │  (chat UI, document ingestion)
                    └──────┬──────┘
                           │ HTTP
                    ┌──────▼──────┐
                    │   FastAPI   │  /api/v1/chat, /api/v1/documents, /health
                    └──────┬──────┘
                           │
                 ┌─────────▼─────────┐
                 │   LangGraph DAG   │
                 └─────────┬─────────┘
     ┌───────────┬─────────┼─────────┬───────────┬───────────┐
     ▼           ▼         ▼         ▼           ▼           ▼
 Planner    Retriever  Quantum   Analyzer    Citation    Business
                        Re-ranker
     │           │         │         │           │           │
     └─── FAISS (vectors) ─┘         └── Postgres / Neo4j (metadata, graph) ──┘
                           │
                        Redis (response + embedding cache)
```

## Agents

| Agent | Responsibility |
|---|---|
| Planner | Decomposes the user query into topic-scoped sub-queries and defines the execution plan. |
| Retriever | Dense vector search (Sentence-Transformers + FAISS) across sub-queries, deduplicated. |
| Quantum Re-ranker | Runs a swap-test circuit (Qiskit Aer simulator) to estimate embedding overlap and blends it with the classical score. |
| Analyzer | Synthesizes the top reranked chunks into a coherent draft answer. |
| Citation | Attaches structured, scored citations back to source chunks. |
| Business | Produces an executive-facing summary of business implications. |

## Data stores

- **PostgreSQL** — relational system of record: documents, chunks, conversations, messages, citations (see `app/db/schema.sql`).
- **Neo4j** — concept graph: `(Document)-[:HAS_CHUNK]->(Chunk)`, `(Concept)-[:MENTIONED_IN]->(Chunk)`, `(Document)-[:CITES]->(Document)` — powers concept-expansion and cross-document relationship queries.
- **FAISS** — in-process vector index (`IndexFlatIP` wrapped in `IndexIDMap2`) persisted to disk, sidecar pickle for chunk metadata.
- **Redis** — response and embedding cache, TTL-based.

## Quantum re-ranking

Each candidate chunk embedding and the query embedding are amplitude-encoded
into `n_qubits = ceil(log2(next_pow2(dim)))` qubits. A swap test circuit
(Hadamard, controlled-SWAP per qubit pair, Hadamard, measure ancilla)
estimates `|<query|chunk>|^2` from measurement statistics on the Aer
simulator. The final score blends this quantum overlap with the classical
cosine similarity (`app/rag/quantum/quantum_utils.py`).

## LangGraph workflow

`app/workflow/graph.py` builds a linear `StateGraph`:

```
planner -> retriever -> quantum_reranker -> analyzer -> citation -> business -> END
```

State is a single `TypedDict` (`AgentState`) threaded through every node,
accumulating a `trace` list for observability.
