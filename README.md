# Quantum RAG Chatbot

A production-grade, multi-agent Quantum RAG (Retrieval-Augmented Generation)
system. Six specialized agents — **Planner, Retriever, Quantum Re-ranker,
Analyzer, Citation, Business** — are orchestrated with **LangGraph** behind a
**FastAPI** backend, with a **Streamlit** chat frontend. Retrieval combines
dense vector search (**FAISS** + Sentence-Transformers) with a genuine
quantum swap-test re-ranking circuit (**Qiskit** + Aer simulator). Persistence
spans **PostgreSQL** (relational), **Neo4j** (concept graph), and **Redis**
(cache).

## Knowledge base

Seeded with quantum-computing literature:
- Steane — Quantum Computing (error correction)
- Preskill — Quantum Computing in the NISQ Era and Beyond
- Qiskit Development Team — Qiskit paper
- Rietsche et al. — Quantum Computing (business/industry survey)

See `data/knowledge_base/README.md` for how to add source text and
`scripts/ingest_knowledge_base.py` to load it.

## Quick start

```bash
cp .env.example .env
docker compose up --build
```

- API: http://localhost:8000 (docs at `/docs`)
- Streamlit UI: http://localhost:8501
- Neo4j browser: http://localhost:7474

## Local (non-Docker) development

```bash
python -m venv .venv && source .venv/bin/activate
make install
make run           # FastAPI on :8000
streamlit run streamlit_app/app.py   # in a second shell
```

## Testing

```bash
make test
make lint
```

## Documentation

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — system design, agent responsibilities, data model, quantum re-ranking method
- [`docs/API.md`](docs/API.md) — endpoint reference
- [`docs/ROADMAP.md`](docs/ROADMAP.md) — phased roadmap and future enhancements
- [`app/db/schema.sql`](app/db/schema.sql) — PostgreSQL schema

## Repository layout

```
app/
  agents/          # Planner, Retriever, Quantum Re-ranker, Analyzer, Citation, Business
  api/routes/       # FastAPI routers (chat, documents, health)
  core/             # settings, logging
  db/               # SQLAlchemy models, Postgres/Neo4j/Redis clients, schema.sql
  rag/              # embeddings, FAISS vector store, quantum swap-test utilities
  schemas/          # Pydantic request/response models
  services/         # ingestion pipeline
  workflow/         # LangGraph state + graph definition
streamlit_app/       # chat + ingestion UI
tests/                # pytest suite (API, agents, workflow, quantum circuit)
scripts/              # knowledge-base batch ingestion
docs/                 # architecture, API reference, roadmap
.github/workflows/    # CI (lint/test/build) and CD (image publish) pipelines
docker-compose.yml    # api, streamlit, postgres, neo4j, redis
```

## CI/CD

- **CI** (`.github/workflows/ci.yml`): ruff lint, pytest with coverage, Docker image builds — runs on every push/PR.
- **CD** (`.github/workflows/cd.yml`): builds and publishes versioned images to GHCR on `v*.*.*` tags, with a deployment stage placeholder to wire to your target platform.
