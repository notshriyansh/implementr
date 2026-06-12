from app.llm.base import BaseLLM
from app.prompts.implementation_prompt import (
    IMPLEMENTATION_PROMPT,
)
from app.retrieval.retrieval_service import (
    RetrievalService,
)


class ImplementationAgent:
    def __init__(
        self,
        retrieval_service: RetrievalService,
        llm: BaseLLM,
    ) -> None:
        self.retrieval_service = (
            retrieval_service
        )

        self.llm = llm

    async def generate_plan(
        self,
        question: str,
    ) -> str:
        chunks = (
            await self.retrieval_service.retrieve(
                query=question,
                k=8,
            )
        )

        context = "\n\n".join(
            chunk.text
            for chunk in chunks
        )

        prompt = (
            IMPLEMENTATION_PROMPT.format(
                context=context,
                question=question,
            )
        )

        response = await self.llm.generate(
            prompt
        )

        return response