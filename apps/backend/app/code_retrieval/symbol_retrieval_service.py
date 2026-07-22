from pathlib import Path

from app.embeddings.base import (
    BaseEmbeddingModel,
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
        embedding_model: BaseEmbeddingModel,
        vector_store: SymbolVectorStore,
    ) -> None:
        self.embedding_model = embedding_model
        self.vector_store = vector_store

    async def index_symbols(
        self,
        symbols: list[CodeSymbol],
    ) -> None:
        texts = [
            (
                f"Symbol Name: {symbol.symbol_name}\n"
                f"Symbol Type: {symbol.symbol_type}\n"
                f"File: {Path(symbol.file_path).stem}"
            )
            for symbol in symbols
        ]

        embeddings = await self.embedding_model.embed_texts(
            texts
        )

        await self.vector_store.add(
            items=symbols,
            embeddings=embeddings,
        )

    async def retrieve(
        self,
        query: str,
        k: int = 5,
    ) -> list[CodeSymbol]:
        query_embedding = (
            await self.embedding_model.embed_text(
                query
            )
        )

        query_embedding = query_embedding.reshape(
            1,
            -1,
        )

        return await self.vector_store.similarity_search(
            query_embedding=query_embedding,
            k=k,
        )