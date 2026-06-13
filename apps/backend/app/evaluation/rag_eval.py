from app.chat.rag_chat_service import (
    RAGChatService,
)
from app.evaluation.metrics import (
    keyword_match_score,
)


class RAGEvaluator:
    def __init__(
        self,
        rag_service: RAGChatService,
    ) -> None:
        self.rag_service = (
            rag_service
        )

    async def evaluate(
        self,
        question: str,
        expected_keywords: list[str],
    ) -> dict:
        response = (
            await self.rag_service.chat(
                session_id="eval_session",
                question=question,
            )
        )

        score = keyword_match_score(
            response.answer,
            expected_keywords,
        )

        return {
            "score": score,
            "answer": response.answer,
        }