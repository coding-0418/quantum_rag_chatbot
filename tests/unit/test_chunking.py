from app.rag.chunking import TextChunker


def test_chunker_returns_non_empty_chunks() -> None:
    chunks = TextChunker(chunk_size=5, chunk_overlap=1).split("abcdefghij")
    assert chunks == ["abcde", "efghi", "ij"]