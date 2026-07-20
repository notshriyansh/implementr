from app.code_embeddings.code_embedding_model import (
    CodeEmbeddingModel,
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
            self.embedding_model.embed_chunks(
                chunks
            )
        )

        await self.vector_store.add_embeddings(
            embeddings=embeddings,
            chunks=chunks,
        )

        del embeddings

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

        results = await (
            self.vector_store.similarity_search(
                query_embedding=query_embedding,
                k=k * 3,
            )
        )

        results = (
            deduplicate_files(
                results
            )
        )

        return results[:k]