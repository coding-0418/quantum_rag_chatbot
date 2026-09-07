from pydantic import BaseModel, Field


class DocumentIngestRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=512)
    source: str | None = None
    authors: str | None = None
    content: str = Field(..., min_length=1)
    chunk_size: int = 800
    chunk_overlap: int = 100


class DocumentIngestResponse(BaseModel):
    document_id: str
    num_chunks: int
