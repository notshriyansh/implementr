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
        self.index = faiss.IndexFlatIP(
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

        embeddings = embeddings.astype(
            "float32"
        )

        faiss.normalize_L2(
            embeddings
        )

        self.index.add(
            embeddings
        )

        print(
            f"Indexed {self.index.ntotal} symbol vectors."
        )

        self.symbols.extend(
            symbols
        )

    async def similarity_search(
        self,
        query_embedding: np.ndarray,
        k: int = 5,
    ) -> list[CodeSymbol]:

        query_embedding = (
            np.asarray(
                query_embedding,
                dtype=np.float32,
            )
            .reshape(1, -1)
        )

        faiss.normalize_L2(
            query_embedding
        )

        scores, indices = (
            self.index.search(
                query_embedding,
                k,
            )
        )

        scored_results: list[
            tuple[float, CodeSymbol]
        ] = []

        for position, idx in enumerate(
            indices[0]
        ):

            if (
                idx == -1
                or idx >= len(
                    self.symbols
                )
            ):
                continue

            symbol = self.symbols[idx]

            final_score = (
                float(
                    scores[0][position]
                )
                * symbol.importance
            )

            scored_results.append(
                (
                    final_score,
                    symbol,
                )
            )

        scored_results.sort(
            key=lambda x: x[0],
            reverse=True,
        )

        return [
            symbol
            for _, symbol in scored_results
        ]