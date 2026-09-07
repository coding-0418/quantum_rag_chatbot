from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=4000)
    conversation_id: str | None = None


class Citation(BaseModel):
    marker: str
    chunk_id: str
    title: str
    source: str
    classical_score: float
    quantum_score: float
    final_score: float


class ChatResponse(BaseModel):
    answer: str
    business_summary: str
    citations: list[Citation]
    trace: list[dict]
