import faiss
import numpy as np

from app.schemas.code_chunk import (
    CodeChunk,
)


class CodeVectorStore:
    def __init__(
        self,
        embedding_dimension: int = 384,
    ) -> None:
        self.index = faiss.IndexFlatL2(
            embedding_dimension
        )

        self.chunks: list[
            CodeChunk
        ] = []

    async def add_embeddings(
        self,
        embeddings: np.ndarray,
        chunks: list[CodeChunk],
    ) -> None:
        self.index.add(
            embeddings.astype(
                "float32"
            )
        )

        self.chunks.extend(chunks)

    async def similarity_search(
        self,
        query_embedding: np.ndarray,
        k: int = 5,
    ) -> list[CodeChunk]:
        distances, indices = (
            self.index.search(
                query_embedding.astype(
                    "float32"
                ),
                k,
            )
        )

        results = []

        for idx in indices[0]:
            if (
                idx != -1
                and idx < len(
                    self.chunks
                )
            ):
                results.append(
                    self.chunks[idx]
                )

        return results