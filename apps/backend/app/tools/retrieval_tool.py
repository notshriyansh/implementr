from app.retrieval.retrieval_service import (
    RetrievalService,
)


class RetrievalTool:
    def __init__(
        self,
        retrieval_service: RetrievalService,
    ) -> None:
        self.retrieval_service = (
            retrieval_service
        )

    async def run(
        self,
        query: str,
    ) -> str:
        chunks = (
            await self.retrieval_service.retrieve(
                query=query,
                k=5,
            )
        )

        return "\n\n".join(
            chunk.text
            for chunk in chunks
        )