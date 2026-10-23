from app.evaluation.metrics import (
    evaluate_ranking,
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

    async def evaluate_ranked_relevance(
        self,
        question: str,
        relevant_chunk_ids: set[str],
        k: int = 5,
    ) -> dict:
        chunks = await self.retrieval_service.retrieve(query=question, k=k)
        retrieved_ids = [chunk.chunk_id for chunk in chunks]
        metrics = evaluate_ranking(
            retrieved_ids=retrieved_ids,
            relevant_ids=relevant_chunk_ids,
            k=k,
        )
        return {
            **metrics,
            "retrieved_chunks": len(chunks),
            "retrieved_chunk_ids": retrieved_ids,
        }
