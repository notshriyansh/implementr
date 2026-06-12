from fastapi import APIRouter, Depends

from app.chat.rag_chat_service import (
    RAGChatService,
)
from app.core.dependencies import (
    get_rag_chat_service,
)
from app.schemas.chat import ChatResponse
from fastapi.responses import (
    StreamingResponse,
)

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

@router.post("/stream")
async def stream_chat(
    question: str,
    rag_chat_service: RAGChatService = Depends(
        get_rag_chat_service,
    ),
) -> StreamingResponse:
    async def event_generator():
        async for token in (
            rag_chat_service.stream_chat(
                question
            )
        ):
            yield token

    return StreamingResponse(
        event_generator(),
        media_type="text/plain",
    )