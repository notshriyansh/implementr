from app.code_embeddings.code_embedding_model import (
    CodeEmbeddingModel,
)
from app.code_vectorstores.symbol_vector_store import (
    SymbolVectorStore,
)
from app.schemas.code_symbol import (
    CodeSymbol,
)


class SymbolRetrievalService:
    def __init__(
        self,
        embedding_model: CodeEmbeddingModel,
        vector_store: SymbolVectorStore,
    ) -> None:
        self.embedding_model = (
            embedding_model
        )

        self.vector_store = (
            vector_store
        )

    async def index_symbols(
        self,
        symbols: list[CodeSymbol],
    ) -> None:
        embeddings = (
            self.embedding_model.embed_chunks(
                symbols
            )
        )

        await self.vector_store.add_symbols(
            embeddings,
            symbols,
        )

        del embeddings

    async def retrieve(
        self,
        query: str,
        k: int = 5,
    ) -> list[CodeSymbol]:
        embedding = await (
            self.embedding_model.embed_query(
                query
            )
        )

        return await (
            self.vector_store.similarity_search(
                embedding,
                k,
            )
        )