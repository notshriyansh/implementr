from app.embeddings.base import (
    BaseEmbeddingModel,
)
from app.code_vectorstores.code_vector_store import (
    CodeVectorStore,
)
from app.schemas.code_chunk import (
    CodeChunk,
)
from app.code_retrieval.retrieval_utils import (
    deduplicate_files,
)


class CodeRetrievalService:
    def __init__(
        self,
        embedding_model: BaseEmbeddingModel,
        vector_store: CodeVectorStore,
    ) -> None:
        self.embedding_model = embedding_model
        self.vector_store = vector_store

    async def index_chunks(
        self,
        chunks: list[CodeChunk],
    ) -> None:
        texts = [
            chunk.content
            for chunk in chunks
        ]

        embeddings = await self.embedding_model.embed_texts(
            texts
        )

        await self.vector_store.add(
            items=chunks,
            embeddings=embeddings,
        )

    async def retrieve(
        self,
        query: str,
        k: int = 5,
    ) -> list[CodeChunk]:
        query_embedding = (
            await self.embedding_model.embed_text(
                query
            )
        )

        query_embedding = query_embedding.reshape(
            1,
            -1,
        )

        results = await self.vector_store.similarity_search(
            query_embedding=query_embedding,
            k=k * 3,
        )

        results = deduplicate_files(
            results
        )

        return results[:k]