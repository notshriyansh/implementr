from fastapi import APIRouter, Depends

from app.chat.rag_chat_service import (
    RAGChatService,
)
from app.core.dependencies import (
    get_rag_chat_service,
)
from app.schemas.chat import ChatResponse

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.post(
    "/",
    response_model=ChatResponse,
)
async def chat(
    question: str,
    rag_chat_service: RAGChatService = Depends(
        get_rag_chat_service,
    ),
) -> ChatResponse:
    return await rag_chat_service.chat(
        question=question,
    )