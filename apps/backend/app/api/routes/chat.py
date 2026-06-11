from fastapi import APIRouter, Depends

from app.chat.rag_chat_service import (
    RAGChatService,
)
from app.core.dependencies import (
    get_rag_chat_service,
)

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.post("/")
async def chat(
    question: str,
    rag_chat_service: RAGChatService = Depends(
        get_rag_chat_service,
    ),
) -> dict:
    response = await rag_chat_service.chat(
        question=question,
    )

    return {
        "question": question,
        "response": response,
    }