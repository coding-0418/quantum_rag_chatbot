"""Application service for document ingestion orchestration."""

from dataclasses import dataclass

from app.rag.chunking import TextChunker


@dataclass
class DocumentService:
    chunker: TextChunker

    def prepare_chunks(self, content: str) -> list[str]:
        # TODO: Persist document and chunk records through the repository layer.
        return self.chunker.split(content)