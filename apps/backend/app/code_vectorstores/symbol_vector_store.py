import faiss
import numpy as np

from app.schemas.code_symbol import (
    CodeSymbol,
)


class SymbolVectorStore:
    def __init__(
        self,
        embedding_dimension: int = 384,
    ) -> None:
        self.index = faiss.IndexFlatL2(
            embedding_dimension
        )

        self.symbols: list[
            CodeSymbol
        ] = []

    async def add_symbols(
        self,
        embeddings: np.ndarray,
        symbols: list[CodeSymbol],
    ) -> None:
        self.index.add(
            embeddings.astype(
                "float32"
            )
        )

        self.symbols.extend(
            symbols
        )

    async def similarity_search(
        self,
        query_embedding: np.ndarray,
        k: int = 5,
    ) -> list[CodeSymbol]:
        _, indices = self.index.search(
            query_embedding.astype(
                "float32"
            ),
            k,
        )

        results = []

        for idx in indices[0]:
            if (
                idx != -1
                and idx < len(
                    self.symbols
                )
            ):
                results.append(
                    self.symbols[idx]
                )

        return results