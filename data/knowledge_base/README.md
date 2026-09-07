# Knowledge Base Sources

This directory is the drop location for the source documents backing the
retrieval index. Place plaintext/markdown extracts here, then run
`scripts/ingest_knowledge_base.py` to embed and load them into FAISS.

Seed corpus referenced by the project brief:

1. **Steane, A. — Quantum Computing (error correction / Steane code)**
2. **Preskill, J. — Quantum Computing in the NISQ Era and Beyond**
3. **Qiskit Development Team — Qiskit: An Open-Source Framework for Quantum Computing**
4. **Rietsche, R. et al. — Quantum Computing (business/industry survey)**

Add each paper as `<slug>.txt` (plaintext extract) in this folder, e.g.:

```
data/knowledge_base/preskill_nisq.txt
data/knowledge_base/steane_qec.txt
data/knowledge_base/qiskit_paper.txt
data/knowledge_base/rietsche_quantum_business.txt
```

Respect each paper's license/terms of use before redistributing full text;
extracts here are for local retrieval indexing only.
