from app.llm.base import BaseLLM
from app.prompts.rag_prompts import (
    RAG_PROMPT_TEMPLATE,
)
from app.retrieval.retrieval_service import (
    RetrievalService,
)
from app.schemas.chat import (
    ChatResponse,
    Citation,
)
from collections.abc import AsyncGenerator


class RAGChatService:
    def __init__(
        self,
        retrieval_service: RetrievalService,
        llm: BaseLLM,
    ) -> None:
        self.retrieval_service = (
            retrieval_service
        )

        self.llm = llm

    async def chat(
        self,
        question: str,
    ) -> ChatResponse:
        chunks = (
            await self.retrieval_service.retrieve(
                query=question,
                k=5,
            )
        )

        context = "\n\n".join(
            chunk.text
            for chunk in chunks
        )

        prompt = (
            RAG_PROMPT_TEMPLATE.format(
                context=context,
                question=question,
            )
        )

        answer = await self.llm.generate(
            prompt
        )

        citations = [
            Citation(
                paper_id=chunk.paper_id,
                page_number=chunk.page_number,
                chunk_index=chunk.chunk_index,
            )
            for chunk in chunks
        ]

        return ChatResponse(
            answer=answer,
            citations=citations,
        )
    
    async def stream_chat(
        self,
        question: str,
    ) -> AsyncGenerator[str, None]:
        chunks = (
            await self.retrieval_service.retrieve(
                query=question,
                k=5,
            )
        )

        context = "\n\n".join(
            chunk.text
            for chunk in chunks
        )

        prompt = (
            RAG_PROMPT_TEMPLATE.format(
                context=context,
                question=question,
            )
        )

        async for token in (
            self.llm.stream_generate(
                prompt
            )
        ):
            yield token