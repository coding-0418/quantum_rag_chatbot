"""Ingestion service: chunks raw text, embeds it, and writes it into the FAISS store."""

import uuid

from app.agents.retriever import get_store
from app.rag.embeddings import embed_texts


def chunk_text(content: str, chunk_size: int = 800, chunk_overlap: int = 100) -> list[str]:
    if chunk_overlap >= chunk_size:
        chunk_overlap = chunk_size // 4

    chunks = []
    start = 0
    while start < len(content):
        end = start + chunk_size
        chunks.append(content[start:end])
        start = end - chunk_overlap
    return [c.strip() for c in chunks if c.strip()]


def ingest_document(
    title: str, content: str, source: str = "", authors: str = "",
    chunk_size: int = 800, chunk_overlap: int = 100,
) -> tuple[str, int]:
    document_id = str(uuid.uuid4())
    chunks = chunk_text(content, chunk_size, chunk_overlap)
    if not chunks:
        return document_id, 0

    vectors = embed_texts(chunks)
    store = get_store(dim=vectors.shape[1])

    metadatas = [
        {
            "chunk_id": f"{document_id}:{idx}",
            "document_id": document_id,
            "content": chunk,
            "title": title,
            "source": source,
            "authors": authors,
            "embedding": vector,
        }
        for idx, (chunk, vector) in enumerate(zip(chunks, vectors))
    ]
    store.add(vectors, metadatas)
    store.save()

    return document_id, len(chunks)
