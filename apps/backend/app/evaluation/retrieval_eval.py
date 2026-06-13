from app.evaluation.metrics import (
    keyword_match_score,
)
from app.retrieval.retrieval_service import (
    RetrievalService,
)


class RetrievalEvaluator:
    def __init__(
        self,
        retrieval_service: RetrievalService,
    ) -> None:
        self.retrieval_service = (
            retrieval_service
        )

    async def evaluate(
        self,
        question: str,
        expected_keywords: list[str],
    ) -> dict:
        chunks = (
            await self.retrieval_service.retrieve(
                query=question,
                k=5,
            )
        )

        combined_text = "\n".join(
            chunk.text
            for chunk in chunks
        )

        score = keyword_match_score(
            combined_text,
            expected_keywords,
        )

        return {
            "score": score,
            "retrieved_chunks": len(chunks),
        }