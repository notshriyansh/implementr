from app.hybrid.hybrid_retrieval_service import (
    HybridRetrievalService,
)
from app.llm.base import BaseLLM
from app.prompts.hybrid_prompts import (
    HYBRID_IMPLEMENTATION_PROMPT,
)


class HybridImplementationAgent:
    def __init__(
        self,
        retrieval_service: (
            HybridRetrievalService
        ),
        llm: BaseLLM,
    ) -> None:
        self.retrieval_service = (
            retrieval_service
        )

        self.llm = llm

    async def analyze(
        self,
        question: str,
    ) -> str:
        (
            paper_chunks,
            code_chunks,
        ) = await (
            self.retrieval_service.retrieve(
                query=question,
            )
        )

        paper_context = "\n\n".join(
            chunk.text
            for chunk in paper_chunks
        )

        code_context = "\n\n".join(
            chunk.content
            for chunk in code_chunks
        )

        prompt = (
            HYBRID_IMPLEMENTATION_PROMPT.format(
                paper_context=(
                    paper_context
                ),
                code_context=(
                    code_context
                ),
                question=question,
            )
        )

        return await self.llm.generate(
            prompt
        )