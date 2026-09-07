"""Text chunking policies."""

from dataclasses import dataclass


@dataclass(frozen=True)
class TextChunker:
    chunk_size: int = 800
    chunk_overlap: int = 100

    def split(self, text: str) -> list[str]:
        if self.chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        overlap = min(max(self.chunk_overlap, 0), self.chunk_size - 1)
        return [text[start : start + self.chunk_size].strip()
                for start in range(0, max(len(text), 1), self.chunk_size - overlap)
                if text[start : start + self.chunk_size].strip()]