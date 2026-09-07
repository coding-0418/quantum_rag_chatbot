# API Reference

Base URL: `http://localhost:8000`

## `GET /health`
Liveness check. Returns `{"status": "ok"}`.

## `GET /health/ready`
Readiness check. Returns `{"status": "ready"}`.

## `POST /api/v1/documents`
Ingest a document into the FAISS knowledge base.

Request body:
```json
{
  "title": "Quantum Computing in the NISQ Era and Beyond",
  "source": "arxiv.org/abs/1801.00862",
  "authors": "John Preskill",
  "content": "...",
  "chunk_size": 800,
  "chunk_overlap": 100
}
```

Response:
```json
{ "document_id": "uuid", "num_chunks": 12 }
```

## `POST /api/v1/chat`
Run the full multi-agent workflow against a query.

Request body:
```json
{ "query": "How does the Steane code perform quantum error correction?" }
```

Response:
```json
{
  "answer": "Synthesis for query: ... \n\nSources:\n[1] ...",
  "business_summary": "Executive summary: ...",
  "citations": [
    {
      "marker": "[1]",
      "chunk_id": "doc-id:3",
      "title": "Steane Quantum Computing",
      "source": "steane_qec.txt",
      "classical_score": 0.81,
      "quantum_score": 0.77,
      "final_score": 0.79
    }
  ],
  "trace": [
    { "agent": "planner", "sub_queries": ["..."] },
    { "agent": "retriever", "num_candidates": 9 },
    { "agent": "quantum_reranker", "top_n": 5, "backend": "aer_simulator" },
    { "agent": "analyzer", "num_sources": 5 },
    { "agent": "citation", "num_citations": 5 },
    { "agent": "business", "impacts": ["risk mitigation"] }
  ]
}
```
