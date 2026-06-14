from app.code_embeddings.code_embedding_model import (
    CodeEmbeddingModel,
)
from app.code_vectorstores.code_vector_store import (
    CodeVectorStore,
)
from app.schemas.code_chunk import (
    CodeChunk,
)


class CodeRetrievalService:
    def __init__(
        self,
        embedding_model: (
            CodeEmbeddingModel
        ),
        vector_store: (
            CodeVectorStore
        ),
    ) -> None:
        self.embedding_model = (
            embedding_model
        )

        self.vector_store = (
            vector_store
        )

    async def index_chunks(
        self,
        chunks: list[CodeChunk],
    ) -> None:
        embeddings = (
            await self.embedding_model.embed_chunks(
                chunks
            )
        )

        await self.vector_store.add_embeddings(
            embeddings=embeddings,
            chunks=chunks,
        )

    async def retrieve(
        self,
        query: str,
        k: int = 5,
    ) -> list[CodeChunk]:
        query_embedding = (
            await self.embedding_model.embed_query(
                query
            )
        )

        return (
            await self.vector_store.similarity_search(
                query_embedding=query_embedding,
                k=k,
            )
        )