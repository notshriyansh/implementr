from app.code_retrieval.code_retrieval_service import (
    CodeRetrievalService,
)
from app.retrieval.retrieval_service import (
    RetrievalService,
)
from app.schemas.chunk import (
    DocumentChunk,
)
from app.schemas.code_chunk import (
    CodeChunk,
)


class HybridRetrievalService:
    def __init__(
        self,
        paper_retrieval: (
            RetrievalService
        ),
        code_retrieval: (
            CodeRetrievalService
        ),
    ) -> None:
        self.paper_retrieval = (
            paper_retrieval
        )

        self.code_retrieval = (
            code_retrieval
        )

    async def retrieve(
        self,
        query: str,
        paper_k: int = 3,
        code_k: int = 3,
    ) -> tuple[
        list[DocumentChunk],
        list[CodeChunk],
    ]:
        paper_chunks = (
            await self.paper_retrieval.retrieve(
                query=query,
                k=paper_k,
            )
        )

        code_chunks = (
            await self.code_retrieval.retrieve(
                query=query,
                k=code_k,
            )
        )

        return (
            paper_chunks,
            code_chunks,
        )