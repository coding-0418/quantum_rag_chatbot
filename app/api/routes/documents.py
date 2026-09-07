from fastapi import APIRouter, HTTPException

from app.schemas.document import DocumentIngestRequest, DocumentIngestResponse
from app.services.knowledge_base import ingest_document

router = APIRouter(prefix="/api/v1", tags=["documents"])


@router.post("/documents", response_model=DocumentIngestResponse)
async def ingest(request: DocumentIngestRequest) -> DocumentIngestResponse:
    try:
        document_id, num_chunks = ingest_document(
            title=request.title,
            content=request.content,
            source=request.source or "",
            authors=request.authors or "",
            chunk_size=request.chunk_size,
            chunk_overlap=request.chunk_overlap,
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return DocumentIngestResponse(document_id=document_id, num_chunks=num_chunks)
