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
from app.memory.conversation_memory import (
    ConversationMemory,
)


class RAGChatService:
    def __init__(
        self,
        retrieval_service: RetrievalService,
        llm: BaseLLM,
        memory: ConversationMemory,
    ) -> None:
        self.retrieval_service = (
            retrieval_service
        )

        self.llm = llm

        self.memory = memory

    async def chat(
        self,
        session_id: str,
        question: str,
    ) -> ChatResponse:
        history_messages = (
            self.memory.get_messages(
                session_id
            )
        )

        recent_history = " ".join(
            msg.content
            for msg in history_messages[-2:]
        )

        retrieval_query = (
            f"{recent_history} {question}"
        )

        chunks = (
            await self.retrieval_service.retrieve(
                query=retrieval_query,
                k=5,
            )
        )

        history_messages = (
            self.memory.get_messages(
                session_id
            )
        )

        history = "\n".join(
            f"{msg.role}: {msg.content}"
            for msg in history_messages
        )

        context = "\n\n".join(
            chunk.text
            for chunk in chunks
        )

        prompt = (
            RAG_PROMPT_TEMPLATE.format(
                history=history,
                context=context,
                question=question,
            )
        )

        answer = await self.llm.generate(
            prompt
        )

        self.memory.add_message(
            session_id=session_id,
            role="user",
            content=question,
        )

        self.memory.add_message(
            session_id=session_id,
            role="assistant",
            content=answer,
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