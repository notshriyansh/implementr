from app.llm.base import BaseLLM
from app.prompts.rag_prompts import (
    RAG_PROMPT_TEMPLATE,
)
from app.retrieval.retrieval_service import (
    RetrievalService,
)


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
    ) -> str:
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

        response = await self.llm.generate(
            prompt
        )

        return response