from fastapi import APIRouter, HTTPException

from app.schemas.chat import ChatRequest, ChatResponse
from app.workflow.graph import run_query

router = APIRouter(prefix="/api/v1", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        state = run_query(request.query)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return ChatResponse(
        answer=state.get("final_answer", ""),
        business_summary=state.get("business_summary", ""),
        citations=state.get("citations", []),
        trace=state.get("trace", []),
    )
