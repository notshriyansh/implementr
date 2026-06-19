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
        self.index = faiss.IndexFlatIP(
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
        embeddings = embeddings.astype(
            "float32"
        )

        faiss.normalize_L2(
            embeddings
        )

        self.index.add(
            embeddings
        )

        self.chunks.extend(chunks)

    async def similarity_search(
        self,
        query_embedding: np.ndarray,
        k: int = 5,
    ) -> list[CodeChunk]:
        query_embedding = (
            query_embedding.astype(
                "float32"
            )
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
