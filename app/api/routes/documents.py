from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.schemas.document import DocumentIngestRequest, DocumentIngestResponse
from app.services.knowledge_base import ingest_document, ingest_pdf

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


@router.post("/documents/pdf", response_model=DocumentIngestResponse)
async def ingest_pdf_file(
    file: UploadFile = File(...),
    title: str | None = Form(None),
    source: str | None = Form(None),
    authors: str | None = Form(None),
    chunk_size: int = Form(800, gt=0),
    chunk_overlap: int = Form(100, ge=0),
) -> DocumentIngestResponse:
    """Ingest a PDF upload and preserve page numbers for citations."""

    if file.content_type not in {"application/pdf", "application/octet-stream"}:
        raise HTTPException(status_code=415, detail="Only PDF uploads are supported")
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=415, detail="The uploaded file must have a .pdf extension")
    try:
        document_id, num_chunks = ingest_pdf(
            title=title or file.filename,
            source=source or file.filename,
            pdf=await file.read(),
            authors=authors or "",
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return DocumentIngestResponse(document_id=document_id, num_chunks=num_chunks)
