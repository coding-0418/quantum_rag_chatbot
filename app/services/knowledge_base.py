"""Ingestion service: chunks raw text, embeds it, and writes it into the FAISS store."""

import uuid
from pathlib import Path
from typing import BinaryIO

from app.agents.retriever import get_store
from app.rag.chunking import TextChunker
from app.rag.embeddings import embed_texts
from app.rag.ingestion.pdf import PDFIngestor


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
    chunks = TextChunker(chunk_size, chunk_overlap).split(content)
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
        }
        for idx, (chunk, vector) in enumerate(zip(chunks, vectors))
    ]
    store.add(vectors, metadatas)
    store.save()

    return document_id, len(chunks)


def ingest_pdf(
    title: str,
    source: str,
    pdf: str | Path | BinaryIO | bytes,
    authors: str = "",
    chunk_size: int = 800,
    chunk_overlap: int = 100,
) -> tuple[str, int]:
    """Extract, chunk, embed, and index a PDF while retaining page citations."""

    document_id = str(uuid.uuid4())
    pages = PDFIngestor().extract_pages(pdf)
    records: list[tuple[str, int]] = []
    chunker = TextChunker(chunk_size, chunk_overlap)
    for page in pages:
        records.extend((chunk, page.page_number) for chunk in chunker.split(page.text))

    if not records:
        return document_id, 0

    chunks = [chunk for chunk, _ in records]
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
            "page_number": page_number,
        }
        for idx, (chunk, page_number) in enumerate(records)
    ]
    store.add(vectors, metadatas)
    store.save()
    return document_id, len(chunks)
