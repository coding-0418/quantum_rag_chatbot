# Roadmap

## Phase 1 — Foundation (current)
- [x] Repository architecture, folder structure, Docker Compose stack
- [x] FastAPI service with chat + document ingestion endpoints
- [x] LangGraph 6-agent workflow (Planner, Retriever, Quantum Re-ranker, Analyzer, Citation, Business)
- [x] FAISS vector store + Sentence-Transformers embeddings
- [x] Qiskit swap-test quantum re-ranker (Aer simulator)
- [x] PostgreSQL schema, Neo4j concept graph client, Redis cache
- [x] Streamlit chat UI
- [x] CI (lint, test, docker build) and CD (image publish) pipelines

## Phase 2 — Knowledge base & persistence
- [ ] Wire Postgres persistence for conversations/messages/citations (currently in-memory per request)
- [ ] Ingest the four seed papers (Steane, Preskill NISQ, Qiskit paper, Rietsche) via `scripts/ingest_knowledge_base.py`
- [ ] Neo4j concept extraction pipeline (NER / keyword extraction into `(:Concept)` nodes)
- [ ] Redis-backed response caching on `/api/v1/chat`

## Phase 3 — Quality & scale
- [ ] Swap the Planner/Analyzer/Business agents to LLM-backed prompts (currently rule-based for determinism/testability)
- [ ] Hybrid sparse+dense retrieval (BM25 + FAISS fusion)
- [ ] Batch/async quantum re-ranking (parallel circuit execution)
- [ ] Real quantum-hardware backend option (IBM Quantum) behind a feature flag
- [ ] Authentication (API keys / OAuth) and per-user conversation history

## Phase 4 — Production hardening
- [ ] Structured tracing (OpenTelemetry) across the LangGraph nodes
- [ ] Rate limiting and request quotas
- [ ] Horizontal scaling: stateless API + externalized FAISS (e.g. behind a vector DB service) for multi-replica deployments
- [ ] Kubernetes manifests / Helm chart, staging + production environments in CD
- [ ] Load testing and quantum-circuit-depth cost budgeting
