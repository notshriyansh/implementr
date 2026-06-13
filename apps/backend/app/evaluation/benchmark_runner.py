from app.evaluation.benchmark_dataset import (
    BENCHMARK_DATASET,
)
from app.evaluation.rag_eval import (
    RAGEvaluator,
)
from app.evaluation.retrieval_eval import (
    RetrievalEvaluator,
)


class BenchmarkRunner:
    def __init__(
        self,
        retrieval_evaluator: RetrievalEvaluator,
        rag_evaluator: RAGEvaluator,
    ) -> None:
        self.retrieval_evaluator = (
            retrieval_evaluator
        )

        self.rag_evaluator = (
            rag_evaluator
        )

    async def run(self) -> dict:
        retrieval_scores = []

        rag_scores = []

        for example in (
            BENCHMARK_DATASET
        ):
            retrieval_result = (
                await self.retrieval_evaluator.evaluate(
                    question=example.question,
                    expected_keywords=(
                        example.expected_keywords
                    ),
                )
            )

            rag_result = (
                await self.rag_evaluator.evaluate(
                    question=example.question,
                    expected_keywords=(
                        example.expected_keywords
                    ),
                )
            )

            retrieval_scores.append(
                retrieval_result["score"]
            )

            rag_scores.append(
                rag_result["score"]
            )

        avg_retrieval = sum(
            retrieval_scores
        ) / len(retrieval_scores)

        avg_rag = sum(
            rag_scores
        ) / len(rag_scores)

        return {
            "avg_retrieval_score": (
                avg_retrieval
            ),
            "avg_rag_score": avg_rag,
            "total_examples": len(
                BENCHMARK_DATASET
            ),
        }