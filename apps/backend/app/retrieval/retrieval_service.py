from app.embeddings.base import (
    BaseEmbeddingModel,
)
from app.schemas.chunk import DocumentChunk
from app.vectorstores.base import (
    BaseVectorStore,
)
from app.retrieval.utils import (
    deduplicate_chunks,
    limit_chunks,
)
from app.observability.tracing import (
    trace_execution,
)


class RetrievalService:
    def __init__(
        self,
        embedding_model: BaseEmbeddingModel,
        vector_store: BaseVectorStore,
    ) -> None:
        self.embedding_model = embedding_model

        self.vector_store = vector_store

    async def index_chunks(
        self,
        chunks: list[DocumentChunk],
    ) -> None:
        texts = [
            chunk.text
            for chunk in chunks
        ]

        embeddings = (
            await self.embedding_model.embed_texts(
                texts
            )
        )

        await self.vector_store.add_embeddings(
            embeddings=embeddings,
            chunks=chunks,
        )

    @trace_execution(
    "retrieval_service.retrieve"
)

    async def retrieve(
        self,
        query: str,
        k: int = 5,
    ) -> list[DocumentChunk]:
        query_embedding = (
            await self.embedding_model.embed_text(
                query
            )
        )

        query_embedding = (
            query_embedding.reshape(1, -1)
        )

        results = (
            await self.vector_store.similarity_search(
                query_embedding=query_embedding,
                k=k,
            )
        )

        results = deduplicate_chunks(
            results
        )

        results = limit_chunks(
            results,
            max_chunks=k,
        )

        return results