from abc import ABC, abstractmethod

from app.schemas.chunk import DocumentChunk


class BaseVectorStore(ABC):
    @abstractmethod
    async def add_embeddings(
        self,
        embeddings,
        chunks: list[DocumentChunk],
    ) -> None:
        pass

    @abstractmethod
    async def similarity_search(
        self,
        query_embedding,
        k: int = 5,
    ) -> list[DocumentChunk]:
        pass